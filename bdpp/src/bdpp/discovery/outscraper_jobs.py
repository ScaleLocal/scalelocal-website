"""Outscraper Indeed search — primary discovery layer for BD++.

Now filters to postings <= 72 hours old, via both the Indeed `fromage` query param
(server-side, last-N-days) and a client-side check on Outscraper's createDate / pubDate
timestamps (Unix milliseconds).
"""
from __future__ import annotations

import asyncio
import html
import re
import time

import httpx

from ..models import JobPosting
from ._states import normalize_state


# Outscraper Indeed: ~$0.001 per record (May 2026)
COST_INDEED_PER_RECORD_USD = 0.001

# Freshness window: posts must be <= this many hours old
MAX_AGE_HOURS = 72


def _strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _job_url(record):
    for k in ("applyUrl", "url", "viewJobUrl", "indeedApplyUrl"):
        v = record.get(k)
        if v:
            return v
    jk = record.get("jobkey") or record.get("jobKey")
    if jk:
        return f"https://www.indeed.com/viewjob?jk={jk}"
    return record.get("indeedCompanyUrl") or ""


def _title_matches(title, target_titles):
    t = (title or "").lower()
    return any(target.lower() in t for target in target_titles)


def _extract_reports_to(description):
    m = re.search(r"reports\s*to\s*[:\-]\s*([^\n\r<.]{3,80})", description or "", re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def _is_fresh(record, max_age_hours=MAX_AGE_HOURS):
    """Check if posting was published within `max_age_hours`. Returns True if so, OR if no date."""
    now_ms = int(time.time() * 1000)
    cutoff = now_ms - (max_age_hours * 3600 * 1000)
    pub = record.get("pubDate") or record.get("createDate") or 0
    try:
        pub = int(pub)
    except (TypeError, ValueError):
        pub = 0
    if pub == 0:
        # Unknown date — let it through; better than missing fresh postings with bad metadata
        return True
    return pub >= cutoff


async def search_indeed(
    *,
    api_token,
    budget,
    target_titles,
    target_states,
    industry,
    per_query_limit=100,
    concurrency=8,
    max_age_hours=MAX_AGE_HOURS,
):
    """Run an Indeed query per (title, state). Filters to fresh (<= max_age_hours) postings only."""
    if not api_token:
        return []
    results = []
    sem = asyncio.Semaphore(concurrency)
    headers = {"X-API-KEY": api_token}
    # Indeed's fromage param wants days, ceil(72/24) = 3
    fromage_days = max(1, (max_age_hours + 23) // 24)

    async def _one(client, title, state):
        async with sem:
            est_cost = COST_INDEED_PER_RECORD_USD * per_query_limit
            if not budget.can_afford(est_cost):
                return []
            params = {
                "query": f"{title} {industry}",
                "location": state,
                "limit": per_query_limit,
                "async": "false",
                "fromage": fromage_days,   # Indeed: limit to last N days
            }
            try:
                r = await client.get(
                    "https://api.app.outscraper.com/indeed-search",
                    params=params, headers=headers, timeout=120.0,
                )
                if r.status_code != 200:
                    return []
                data = r.json()
            except Exception:
                return []
            records = data.get("data") or []
            if records and isinstance(records[0], list):
                records = records[0]
            actual_cost = COST_INDEED_PER_RECORD_USD * len(records)
            budget.charge("outscraper-indeed", f"{title}/{state}:{len(records)}rec", actual_cost)

            postings = []
            target_abbr = normalize_state(state)
            for rec in records:
                # Freshness check (post-hoc — Outscraper may return some stale even with fromage)
                if not _is_fresh(rec, max_age_hours):
                    continue
                jt = rec.get("displayTitle") or rec.get("normTitle") or ""
                if not _title_matches(jt, target_titles):
                    continue
                rec_state = (rec.get("jobLocationState") or "").upper()
                if rec_state and target_abbr and rec_state != target_abbr:
                    continue
                company = rec.get("company") or ""
                if not company:
                    continue
                city = rec.get("jobLocationCity") or ""
                loc = rec.get("formattedLocation") or f"{city}, {rec_state}".strip(", ")
                description = _strip_html(rec.get("snippet") or "")
                postings.append(JobPosting(
                    source="indeed",
                    source_id=f"indeed:{rec.get('jobkey') or company + ':' + jt}",
                    company_name=company,
                    company_domain=None,
                    job_title=jt,
                    job_location=loc,
                    job_city=city,
                    job_state=rec_state or None,
                    job_url=_job_url(rec),
                    description=description[:8000],
                    reports_to_raw=_extract_reports_to(description),
                ))
            return postings

    async with httpx.AsyncClient() as client:
        tasks = []
        for title in target_titles:
            for state in target_states:
                tasks.append(_one(client, title, state))
        chunks = await asyncio.gather(*tasks, return_exceptions=True)
        for c in chunks:
            if isinstance(c, list):
                results.extend(c)
    return results
