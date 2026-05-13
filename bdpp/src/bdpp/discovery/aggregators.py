"""Job-aggregator discovery — scrape free public job boards to find postings + parent companies.

This is where most of the 'long tail' manufacturers like Boyd Corp surface. They don't use
Greenhouse or Lever, but their postings get indexed by:
  - jobs.ashbyhq.com (Ashby ATS — public boards)
  - workable.com   (Workable ATS — public boards)
  - smartrecruiters.com (SmartRecruiters — public boards)
  - jobs.smartrecruiters.com
  - boards.greenhouse.io (already covered by greenhouse.py)
  - apply.workable.com
  - bamboohr.com / *.bamboohr.com  (BambooHR boards — public)
  - ats.rippling.com
  - jobs.jobvite.com
  - careers.icims.com  (iCIMS — varying access)

The path: Google a site-restricted query like
  ("Controls Engineer" OR "Electrical Engineer") site:jobs.ashbyhq.com "MA"
extract result URLs, follow each to the ATS, parse company + role.

Google Custom Search is free up to 100 queries/day; we use it when a CSE ID is configured.
Without a CSE ID, this module is a no-op (the Greenhouse + Lever direct seed approach still runs).
"""
from __future__ import annotations

import asyncio
import html
import re
from typing import Iterable
from urllib.parse import urlparse

import httpx

from ..models import JobPosting
from ._states import location_matches, parse_location, normalize_state


ATS_DOMAINS = [
    "jobs.ashbyhq.com",
    "apply.workable.com",
    "jobs.smartrecruiters.com",
    "boards.greenhouse.io",
    "jobs.lever.co",
    "jobs.jobvite.com",
    "bamboohr.com",
    "ats.rippling.com",
    "careers.icims.com",
    "myworkdayjobs.com",
    "phenompeople.com",
    "ultipro.com",
    "paycomonline.net",
    "isolvedhire.com",
    "applytojob.com",
]


async def google_cse_search(
    client: httpx.AsyncClient,
    *,
    api_key: str,
    cse_id: str,
    query: str,
    num: int = 10,
) -> list[dict]:
    """One Google Custom Search call. Free quota: 100/day."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query, "num": min(num, 10)}
    try:
        r = await client.get(url, params=params, timeout=15.0)
        if r.status_code != 200:
            return []
        return (r.json() or {}).get("items", []) or []
    except Exception:
        return []


def _extract_company_from_ats_url(url: str) -> str | None:
    """Pull the company slug out of an ATS URL.

    Examples:
      https://boards.greenhouse.io/boydcorp/jobs/12345 -> 'boydcorp'
      https://jobs.lever.co/boyd-corp/posting-id      -> 'boyd-corp'
      https://jobs.ashbyhq.com/boydcorp/role-id       -> 'boydcorp'
      https://apply.workable.com/boydcorp/j/12345     -> 'boydcorp'
    """
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        parts = [p for p in parsed.path.split("/") if p]
        if not parts:
            return None
        if "greenhouse.io" in host or "lever.co" in host or "ashbyhq.com" in host:
            return parts[0]
        if "workable.com" in host:
            return parts[0]
        if "smartrecruiters.com" in host:
            return parts[0]
        if "bamboohr.com" in host:
            # something.bamboohr.com -> the subdomain is the company
            sub = host.split(".")[0]
            return sub if sub and sub != "www" else None
        return parts[0]
    except Exception:
        return None


async def search_aggregators(
    *,
    api_key: str,
    cse_id: str,
    target_titles: list[str],
    target_states: list[str],
    industry: str = "manufacturing",
    queries_per_site: int = 1,
) -> list[JobPosting]:
    """Use Google CSE to find ATS-hosted postings matching our criteria.

    Returns a 'thin' JobPosting per hit — company_name is the ATS slug, description is the snippet.
    Downstream qualification re-fetches richer data per company.
    """
    if not api_key or not cse_id:
        return []

    results: list[JobPosting] = []
    state_phrase = " OR ".join([f'"{s}"' for s in target_states])
    title_phrase = " OR ".join([f'"{t}"' for t in target_titles])

    async with httpx.AsyncClient(
        headers={"User-Agent": "BDPlusPlus/0.1 (+jobs-discovery)"},
        follow_redirects=True,
    ) as client:
        for site in ATS_DOMAINS:
            q = f"({title_phrase}) ({state_phrase}) site:{site} {industry}"
            items = await google_cse_search(client, api_key=api_key, cse_id=cse_id, query=q, num=10)
            for it in items:
                link = it.get("link", "") or ""
                title = it.get("title", "") or ""
                snippet = it.get("snippet", "") or ""
                company_slug = _extract_company_from_ats_url(link) or ""
                # Light location parse from snippet
                state = None
                city = None
                for s in target_states:
                    if s.lower() in snippet.lower() or s.lower() in title.lower():
                        state = normalize_state(s)
                        break
                if not state:
                    continue
                # Best-effort title extraction — Google title often has " — Company Name" suffix
                job_title = re.split(r"\s[–—\-|@]\s", title)[0].strip()
                results.append(JobPosting(
                    source=f"cse:{urlparse(link).netloc}",
                    source_id=link,
                    company_name=company_slug,
                    company_domain=None,
                    job_title=job_title,
                    job_location=f"{state}",
                    job_city=city,
                    job_state=state,
                    job_url=link,
                    description=snippet,
                ))
    return results
