"""BD++ engine — three-button queue-based architecture.

  stage_search()   -> appends qualified companies to the persistent queue (DISCOVERED)
  stage_enrich()   -> processes DISCOVERED rows up to budget, marks them ENRICHED
  stage_output()   -> exports ENRICHED rows to CSV, marks them EXPORTED (optional)

The queue persists in SQLite at <project>/queue.db across runs.
"""
from __future__ import annotations

import asyncio
import csv
import json
import re
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from .budget import BudgetTracker
from .config import Credentials, SearchConfig, PROJECT_ROOT
from .contacts import resolve_contacts
from .discovery import discover_jobs
from .discovery.orchestrator import dedup_one_per_company
from .discovery.seeds import KNOWN_NE_MANUFACTURERS
from .intel import extract_skills_heuristic, run_intel
from .models import Contact, EnrichedRow, JobPosting, CompanyProfile
from .output import write_csv
from .output.apollo_assist import write_apollo_assist
from . import queue as q
from . import spend
from .session import BDSession
from .verify import verify_or_guess


def _is_valid_company(name):
    if not name:
        return False
    return name.strip().lower() not in {"nan", "none", "n/a", ""}


def _resolve_company_display_name(token):
    for m in KNOWN_NE_MANUFACTURERS:
        if (m["name"].lower().replace(" ", "").replace(",", "").replace(".", "")
                == token.lower().replace("-", "")):
            return m["name"]
    return re.sub(r"[-_]+", " ", token).strip().title()


def _company_what(name):
    for m in KNOWN_NE_MANUFACTURERS:
        if m["name"].lower() == (name or "").lower():
            return m["what"]
    return None


def _company_website(name):
    for m in KNOWN_NE_MANUFACTURERS:
        if m["name"].lower() == (name or "").lower():
            return m["website"]
    return None


def _domain_from_website(website):
    if not website:
        return None
    try:
        return urlparse(website).netloc.lower().lstrip("www.")
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────────────────────
# STAGE 1 — SEARCH (adds to queue)
# ──────────────────────────────────────────────────────────────────────────────
async def stage_search(search: SearchConfig, creds: Credentials):
    """Discover + qualify, append qualified rows to the persistent queue."""
    raw_no_dedup = await discover_jobs(
        target_titles=search.job_titles,
        target_states=search.locations,
        industry=search.industry,
        hours_old=search.hours_old,
        results_per_query=search.results_per_query,
        one_per_company=False,
    )
    raw_no_dedup = [p for p in raw_no_dedup if _is_valid_company(p.company_name)]
    deduped = dedup_one_per_company(raw_no_dedup)

    from .qualify import qualify_companies
    qualified = qualify_companies(
        deduped,
        exclude_fortune500=search.filters.exclude_fortune500,
        max_active_postings=search.filters.max_active_postings,
        max_office_locations=search.filters.max_office_locations,
        all_postings_for_count=raw_no_dedup,
    )
    for posting, profile in qualified:
        if posting.source in ("greenhouse", "lever"):
            profile.name = _resolve_company_display_name(profile.name)
        profile.website = _company_website(profile.name)
        if not profile.domain:
            profile.domain = _domain_from_website(profile.website) or profile.domain
        profile.company_intel = _company_what(profile.name)

    enqueue_result = q.enqueue_search_results(
        qualified,
        {"tag": search.tag, "industry": search.industry},
    )
    return {
        "discovered_postings": len(raw_no_dedup),
        "qualified": len(qualified),
        "queued_new": enqueue_result["added"],
        "queued_skipped_duplicates": enqueue_result["skipped_duplicates"],
        "queue_counts": q.queue_counts(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# STAGE 2 — ENRICH (pulls DISCOVERED from queue, marks ENRICHED)
# ──────────────────────────────────────────────────────────────────────────────
async def stage_enrich(creds: Credentials, *, max_companies: int = 50, max_spend_usd: float = 6.0):
    """Pull DISCOVERED rows from queue, enrich, mark ENRICHED."""
    rows = q.pop_for_enrichment(max_companies)
    if not rows:
        return {"enriched": 0, "message": "No DISCOVERED rows in queue.", "queue_counts": q.queue_counts()}

    budget = BudgetTracker(cap_usd=max_spend_usd)

    # Rehydrate JobPosting + CompanyProfile from queue rows
    rehydrated = []
    for r in rows:
        posting = JobPosting(
            source=r["bd_job_source"] or "indeed",
            source_id=str(r["id"]),
            company_name=r["company_name"],
            company_domain=r["company_domain"],
            job_title=r["bd_job_title"],
            job_location=r["bd_job_location"],
            job_city=r["bd_job_city"],
            job_state=r["bd_job_state"],
            job_url=r["bd_job_url"],
            description=r["bd_job_description"] or "",
            reports_to_raw=r["bd_job_reports_to"],
        )
        profile = CompanyProfile(
            name=r["company_name"],
            domain=r["company_domain"],
            website=r["company_website"],
            company_intel=r["company_intel"],
        )
        rehydrated.append((r["id"], posting, profile))

    # Resolve contacts (website scraping + reports-to extraction — free)
    pairs = [(p, pr) for _, p, pr in rehydrated]
    resolved = await resolve_contacts(pairs, budget=budget, concurrency=8)

    # Map resolved back to queue ids, do email verify, then mark ENRICHED
    enriched_count = 0
    for (qid, posting, profile), res in zip(rehydrated, resolved):
        hiring = res.get("hiring_manager")
        hr = res.get("hr")
        domain = profile.domain or _domain_from_website(profile.website)
        for contact in (hiring, hr):
            if contact and domain and creds.millionverifier_token:
                email, status = await verify_or_guess(
                    contact.first_name, contact.last_name, domain,
                    mv_token=creds.millionverifier_token, budget=budget,
                )
                if email:
                    contact.email = email
                    contact.email_verification_status = status
        skills = extract_skills_heuristic(posting.description or "", max_skills=3)
        q.mark_enriched(qid, hiring_manager=hiring, hr_contact=hr, skills=skills)
        enriched_count += 1
        # Stop if we've hit the soft cap — leave remaining DISCOVERED for later
        if budget.percent_used() >= 0.95:
            break

    spend.add_spend(budget.spent_usd)
    spend_summary = spend.get_summary()
    remaining_discovered = q.queue_counts().get("DISCOVERED", 0)
    budget_capped = budget.percent_used() >= 0.95 and remaining_discovered > 0

    return {
        "enriched": enriched_count,
        "budget_spent_this_run_usd": round(budget.spent_usd, 4),
        "budget_cap_usd": budget.cap_usd,
        "budget_capped": budget_capped,
        "remaining_discovered": remaining_discovered,
        "spend_today_usd": spend_summary["today_usd"],
        "spend_last_7d_usd": spend_summary["last_7_days_usd"],
        "spend_lifetime_usd": spend_summary["lifetime_usd"],
        "queue_counts": q.queue_counts(),
        "message": (f"Budget cap reached. {remaining_discovered} companies remain DISCOVERED "
                    f"in queue. Run 'enrich' again with higher --max-spend to continue, or "
                    f"manually delete the ones you don't want.")
                   if budget_capped else
                   (f"Enriched {enriched_count} companies. ${round(budget.spent_usd,4)} spent."),
    }


# ──────────────────────────────────────────────────────────────────────────────
# STAGE 3 — OUTPUT (pulls ENRICHED from queue, writes CSV, marks EXPORTED)
# ──────────────────────────────────────────────────────────────────────────────
def stage_output(search: SearchConfig, *, status_filter="ENRICHED", mark_as_exported=True):
    """Pull ENRICHED rows, write CSV in BD++ format. Optionally include DISCOVERED rows too."""
    if status_filter == "ENRICHED_AND_DISCOVERED":
        rows = q.list_queue(status="ENRICHED", limit=10000) + q.list_queue(status="DISCOVERED", limit=10000)
    else:
        rows = q.list_queue(status=status_filter, limit=10000)
    if not rows:
        return {"error": f"No {status_filter} rows in queue."}

    erows = []
    qualified_for_apollo = []
    for r in rows:
        hiring = None
        hr = None
        if r.get("hiring_manager_json"):
            try:
                d = json.loads(r["hiring_manager_json"])
                hiring = Contact(**d)
            except Exception:
                pass
        if r.get("hr_contact_json"):
            try:
                d = json.loads(r["hr_contact_json"])
                hr = Contact(**d)
            except Exception:
                pass
        skills = [r.get("skill_1") or "", r.get("skill_2") or "", r.get("skill_3") or ""]
        intel = run_intel(
            description=r.get("bd_job_description", "") or "",
            enable_position=search.intel.position_intel,
            enable_company=search.intel.company_intel,
            enable_contact=search.intel.contact_intel,
            company_what=r.get("company_intel"),
        )
        # If position-intel toggle is ON, prefer freshly-extracted skills over stored ones
        if search.intel.position_intel and intel["position_skills"]:
            skills = list(intel["position_skills"])
        cols = (skills + ["", "", "", "", ""])[:5]
        if search.intel.company_intel and intel["company_intel"]:
            cols[3] = intel["company_intel"]

        def _emit(contact, default_title):
            erows.append(EnrichedRow(
                company=r["company_name"],
                first_name=getattr(contact, "first_name", "") if contact else "",
                last_name=getattr(contact, "last_name", "") if contact else "",
                job_title=(getattr(contact, "title", "") or default_title) if contact else default_title,
                email=getattr(contact, "email", "") or "" if contact else "",
                phone="",
                city=r.get("bd_job_city") or "",
                state=r.get("bd_job_state") or "",
                bd_job_title=r["bd_job_title"],
                bd_job_location=r["bd_job_location"],
                skill_1=cols[0], skill_2=cols[1], skill_3=cols[2],
                skill_4=cols[3], skill_5=cols[4],
                tag=search.tag, industry=search.industry,
                job_url=r.get("bd_job_url") or "",
                contact_source=getattr(contact, "source", "") if contact else "(needs Apollo / manual lookup)",
                email_verification_status=getattr(contact, "email_verification_status", "") or "" if contact else "",
                contact_intel=intel["contact_intel"] or "",
            ))

        if hiring:
            _emit(hiring, "Hiring Manager")
        if hr:
            _emit(hr, "HR Contact")
        if not hiring and not hr:
            _emit(None, "(no contact found)")

        # Build qualified for apollo-assist
        posting = JobPosting(
            source=r.get("bd_job_source") or "indeed",
            source_id=str(r["id"]),
            company_name=r["company_name"],
            company_domain=r.get("company_domain"),
            job_title=r["bd_job_title"],
            job_location=r["bd_job_location"],
            job_city=r.get("bd_job_city"),
            job_state=r.get("bd_job_state"),
            job_url=r.get("bd_job_url"),
        )
        profile = CompanyProfile(name=r["company_name"], domain=r.get("company_domain"),
                                 website=r.get("company_website"), company_intel=r.get("company_intel"))
        qualified_for_apollo.append((posting, profile))

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rel = search.csv_path.replace("{timestamp}", ts)
    out_path = (PROJECT_ROOT / rel) if not Path(rel).is_absolute() else Path(rel)
    write_csv(erows, out_path)
    apollo_path = out_path.parent / f"{out_path.stem}_apollo_assist.csv"
    write_apollo_assist(qualified_for_apollo, apollo_path)

    if mark_as_exported:
        ids = [r["id"] for r in rows]
        q.mark_exported(ids)

    return {
        "csv_path": str(out_path),
        "apollo_csv_path": str(apollo_path),
        "rows_written": len(erows),
        "queue_counts": q.queue_counts(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# CONVENIENCE — run all three (used by CLI for one-shot demo)
# ──────────────────────────────────────────────────────────────────────────────
async def run_search(search, creds, *, max_rows_companies=50, auto_enrich=False, auto_export=False):
    """Convenience runner. By default ONLY runs Search — explicit user action required for Enrich+Output.

    Pass auto_enrich=True and/or auto_export=True for end-to-end demos.
    """
    search_result = await stage_search(search, creds)
    summary = {"search": search_result}
    if auto_enrich:
        enrich_result = await stage_enrich(creds, max_companies=max_rows_companies,
                                           max_spend_usd=search.max_spend_usd)
        summary["enrich"] = enrich_result
    if auto_export:
        output_result = stage_output(search, status_filter="ENRICHED")
        summary["output"] = output_result
        return Path(output_result["csv_path"]), summary
    return None, summary
