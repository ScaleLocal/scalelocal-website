"""Lever public API discovery."""
from __future__ import annotations

import asyncio
import html
import re

import httpx

from ..models import JobPosting
from ._states import location_matches, parse_location
from .seeds import LEVER_SEED_TOKENS


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
    url = f"https://api.lever.co/v0/postings/{token}?mode=json"
    try:
        r = await client.get(url, timeout=20.0)
        if r.status_code != 200:
            return []
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception:
        return []


async def fetch_jobs(target_titles, target_states, *, seed_tokens=None, concurrency=12):
    tokens = list(seed_tokens) if seed_tokens is not None else LEVER_SEED_TOKENS
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
                title = j.get("text", "") or ""
                if not _title_matches(title, target_titles):
                    continue
                cats = j.get("categories") or {}
                loc = cats.get("location", "") or ""
                if not location_matches(loc, target_states):
                    continue
                desc_parts = []
                if j.get("descriptionPlain"):
                    desc_parts.append(j["descriptionPlain"])
                for lst in (j.get("lists") or []):
                    if lst.get("text"):
                        desc_parts.append(lst["text"])
                    if lst.get("content"):
                        desc_parts.append(_strip_html(lst["content"]))
                if j.get("additionalPlain"):
                    desc_parts.append(j["additionalPlain"])
                content = " ".join(desc_parts)[:8000]
                city, state = parse_location(loc)
                board_matches.append(JobPosting(
                    source="lever",
                    source_id=str(j.get("id", "")),
                    company_name=token,
                    company_domain=None,
                    job_title=title,
                    job_location=loc,
                    job_city=city,
                    job_state=state,
                    job_url=j.get("hostedUrl", "") or "",
                    description=content,
                    reports_to_raw=_extract_reports_to(content),
                ))
            return board_matches

        results = await asyncio.gather(*[_one(t) for t in tokens])
        for r in results:
            matches.extend(r)

    return matches
