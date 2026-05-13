"""Greenhouse public API discovery."""
from __future__ import annotations

import asyncio
import html
import re
from typing import Iterable

import httpx

from ..models import JobPosting
from ._states import location_matches, parse_location
from .seeds import GREENHOUSE_SEED_TOKENS


def _strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _title_matches(job_title, target_titles):
    t = (job_title or "").lower()
    return any(target.lower() in t for target in target_titles)


def _extract_reports_to(description):
    m = re.search(r"reports\s*to\s*[:\-]\s*([^\n\r<.]{3,80})", description or "", re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


async def fetch_board(client, token):
    url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
    try:
        r = await client.get(url, timeout=20.0)
        if r.status_code != 200:
            return []
        data = r.json()
        return data.get("jobs", []) or []
    except Exception:
        return []


async def fetch_jobs(target_titles, target_states, *, seed_tokens=None, concurrency=12):
    tokens = list(seed_tokens) if seed_tokens is not None else GREENHOUSE_SEED_TOKENS
    sem = asyncio.Semaphore(concurrency)
    matches = []

    async with httpx.AsyncClient(
        headers={"User-Agent": "BDPlusPlus/0.1 (+jobs-discovery)"},
        follow_redirects=True,
    ) as client:
        async def _one(token):
            async with sem:
                jobs = await fetch_board(client, token)
            board_matches = []
            for j in jobs:
                title = j.get("title", "") or ""
                if not _title_matches(title, target_titles):
                    continue
                loc = (j.get("location") or {}).get("name", "") or ""
                if not location_matches(loc, target_states):
                    continue
                content = _strip_html(j.get("content", "") or "")
                city, state = parse_location(loc)
                board_matches.append(JobPosting(
                    source="greenhouse",
                    source_id=str(j.get("id", "")),
                    company_name=token,
                    company_domain=None,
                    job_title=title,
                    job_location=loc,
                    job_city=city,
                    job_state=state,
                    job_url=j.get("absolute_url", "") or "",
                    description=content[:8000],
                    reports_to_raw=_extract_reports_to(content),
                ))
            return board_matches

        results = await asyncio.gather(*[_one(t) for t in tokens])
        for r in results:
            matches.extend(r)

    return matches
