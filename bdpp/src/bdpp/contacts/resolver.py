"""Contact resolution — identify the engineering hiring manager + HR contact at a company.

Strategy (in order of cost):
 1) Free: parse 'Reports to: Name' from job description if present.
 2) Free: fetch the company website and try /team, /about, /people, /leadership pages.
    Look for known titles (Engineering Manager / VP Engineering / Plant Manager / HR Manager /
    Talent Acquisition / Recruiter / People Ops) plus a person's name within the same DOM region.
 3) Paid (budget-gated): Outscraper Contacts & Leads search by domain.

For the demo we focus heavily on (1) and (2) to stay under budget. (3) is gated behind budget.
"""
from __future__ import annotations

import asyncio
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx

from ..budget import BudgetTracker
from ..models import Contact, CompanyProfile, JobPosting


# Titles we care about, ordered by signal strength for each role class
HIRING_MGR_TITLES = [
    "engineering manager", "director of engineering", "director, engineering",
    "vp of engineering", "vp engineering", "vice president of engineering",
    "head of engineering", "engineering director",
    "plant manager", "director of operations", "vp of operations", "vp operations",
    "operations director", "head of operations", "manufacturing engineering manager",
    "director of manufacturing", "controls engineering manager",
    "electrical engineering manager", "chief engineer",
]

HR_TITLES = [
    "hr manager", "human resources manager", "human resources director",
    "director of human resources", "hr director", "vp of hr", "vp human resources",
    "talent acquisition manager", "talent acquisition", "recruiter",
    "senior recruiter", "technical recruiter", "head of people", "people operations",
    "chief people officer", "vp people", "people partner", "hr generalist",
    "hr business partner", "hrbp", "talent partner",
]

TEAM_PATHS = [
    "/team", "/about/team", "/about-us/team", "/about/people", "/people",
    "/leadership", "/company/leadership", "/about/leadership", "/about", "/about-us",
    "/our-team", "/who-we-are", "/management",
]

NAME_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)\b")


def _split_name(full: str) -> tuple[str, str]:
    parts = [p for p in full.strip().split() if p]
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[-1]


def _classify_title(title: str) -> str:
    t = title.lower()
    if any(h in t for h in HR_TITLES):
        return "HR"
    if any(h in t for h in HIRING_MGR_TITLES):
        return "HIRING_MANAGER"
    return "OTHER"


def _domain_from_url(url: str) -> str | None:
    try:
        return urlparse(url).netloc.lower().lstrip("www.")
    except Exception:
        return None


def _extract_contacts_from_html(html: str) -> list[Contact]:
    """Light parser — finds Name + Title pairs in /team-style pages by proximity heuristics."""
    # Strip tags but keep some structure
    text = re.sub(r"<(script|style)[^>]*>.*?</\\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"[ \t]+", " ", text)

    found: dict[tuple[str, str], Contact] = {}
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i, line in enumerate(lines):
        # Look for a line that is a known title; pair with nearby capitalized name.
        title_match = None
        ll = line.lower()
        for t in HIRING_MGR_TITLES + HR_TITLES:
            if t in ll and len(line) < 120:
                title_match = line
                break
        if not title_match:
            continue
        # Search +/- 2 lines for a person name
        window = lines[max(0, i - 2): i + 3]
        for ctx in window:
            m = NAME_RE.search(ctx)
            if m and " " in m.group(1):
                full = m.group(1)
                # filter out obvious non-people
                if any(w in full.lower() for w in ["the", "team", "our", "company", "manager", "engineer", "resources"]):
                    continue
                first, last = _split_name(full)
                role = _classify_title(title_match)
                key = (full.lower(), title_match.lower())
                if key not in found:
                    found[key] = Contact(
                        first_name=first,
                        last_name=last,
                        title=title_match.strip(),
                        role_class=role,
                        source="website_team_page",
                        confidence=0.55,
                    )
    return list(found.values())


async def _fetch_html(client: httpx.AsyncClient, url: str, timeout: float = 10.0) -> str:
    try:
        r = await client.get(url, timeout=timeout, follow_redirects=True)
        if r.status_code == 200 and "text/html" in r.headers.get("content-type", ""):
            return r.text
    except Exception:
        pass
    return ""


async def _scrape_company_team_pages(client: httpx.AsyncClient, base_url: str) -> list[Contact]:
    base = base_url.rstrip("/")
    candidates = [urljoin(base + "/", p.lstrip("/")) for p in TEAM_PATHS]
    sem = asyncio.Semaphore(4)

    async def _one(u: str) -> list[Contact]:
        async with sem:
            html = await _fetch_html(client, u)
            return _extract_contacts_from_html(html) if html else []

    results = await asyncio.gather(*[_one(u) for u in candidates], return_exceptions=True)
    contacts: list[Contact] = []
    for r in results:
        if isinstance(r, list):
            contacts.extend(r)
    return contacts


def _parse_reports_to_name(text: str) -> Optional[str]:
    """If 'Reports to: Some Name, Engineering Manager' is in the JD, extract the name."""
    if not text:
        return None
    m = re.search(r"reports\s*to\s*[:\-]\s*([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)", text)
    return m.group(1) if m else None


async def resolve_for_company(
    client: httpx.AsyncClient,
    posting: JobPosting,
    profile: CompanyProfile,
    budget: BudgetTracker,
) -> dict:
    """Return {'hiring_manager': Contact|None, 'hr': Contact|None}."""
    out = {"hiring_manager": None, "hr": None}

    # 1) Reports-to in job description
    reports_to_name = _parse_reports_to_name(posting.description) or _parse_reports_to_name(posting.reports_to_raw or "")
    if reports_to_name:
        first, last = _split_name(reports_to_name)
        # Title is inferred; we'll mark as Hiring Manager with mid confidence
        out["hiring_manager"] = Contact(
            first_name=first, last_name=last, title="Hiring Manager (named in job post)",
            role_class="HIRING_MANAGER", source="job_post", confidence=0.85,
        )

    # 2) Company website team-page scrape
    base = profile.website or posting.company_domain
    if not base:
        # Derive from job_url where possible
        try:
            base = f"https://{urlparse(posting.job_url).netloc}"
        except Exception:
            base = None
    if base:
        if not base.startswith("http"):
            base = "https://" + base
        team_contacts = await _scrape_company_team_pages(client, base)
        # Score: prefer specifically-titled people; among ties prefer those with deeper title strings
        hm_candidates = [c for c in team_contacts if c.role_class == "HIRING_MANAGER"]
        hr_candidates = [c for c in team_contacts if c.role_class == "HR"]
        hm_candidates.sort(key=lambda c: (-len(c.title), -c.confidence))
        hr_candidates.sort(key=lambda c: (-len(c.title), -c.confidence))
        if not out["hiring_manager"] and hm_candidates:
            out["hiring_manager"] = hm_candidates[0]
        if not out["hr"] and hr_candidates:
            out["hr"] = hr_candidates[0]

    return out


async def resolve_contacts(
    qualified: list[tuple[JobPosting, CompanyProfile]],
    *,
    budget: BudgetTracker,
    concurrency: int = 8,
) -> list[dict]:
    """Resolve hiring + HR contacts for each qualified (posting, profile). Returns a list dict per company."""
    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(
        headers={"User-Agent": "BDPlusPlus/0.1 (+contact-resolver)"},
        follow_redirects=True,
    ) as client:
        async def _one(posting, profile):
            async with sem:
                contacts = await resolve_for_company(client, posting, profile, budget)
            return {"posting": posting, "profile": profile, **contacts}

        return await asyncio.gather(*[_one(p, pr) for p, pr in qualified])
