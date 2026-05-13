"""JobSpy-based discovery — aggregator-first via Indeed (free, accurate, fast)."""
from __future__ import annotations

import asyncio
import re
import warnings
from datetime import datetime, timedelta, timezone
from typing import Iterable

import pandas as pd

from ..models import JobPosting

# Silence the regex match-group warning from pandas
warnings.filterwarnings("ignore", message="This pattern is interpreted as a regular expression")


def _strip_html(s):
    if not s or not isinstance(s, str):
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _extract_reports_to(description):
    m = re.search(r"reports\s*to\s*[:\-]\s*([^\n\r<.]{3,80})", description or "", re.IGNORECASE)
    return m.group(1).strip() if m else None


def _state_from_location(loc):
    if not isinstance(loc, str):
        return None
    parts = loc.split(",")
    if len(parts) >= 2:
        st = parts[1].strip().upper()[:2]
        return st
    return None


def _city_from_location(loc):
    if not isinstance(loc, str):
        return None
    parts = loc.split(",")
    return parts[0].strip() if parts else None


def _build_title_regex(target_titles):
    """Looser regex that catches Sr/Senior/Principal variants."""
    parts = []
    for t in target_titles:
        # 'Controls Engineer' -> r"\bcontrols?\s+engineer"
        toks = t.lower().split()
        if "engineer" in toks:
            base = toks[toks.index("engineer") - 1] if toks.index("engineer") > 0 else ""
            parts.append(rf"\b{base}s?\s+engineer")
            parts.append(rf"\b{base}s?\s+engineering")
        else:
            parts.append(re.escape(t.lower()))
    return r"(?i)" + "|".join(parts)


def _run_blocking(target_titles, target_states, *, hours_old=72, results_per_query=40, sites=("indeed",)):
    """Blocking JobSpy call — runs in a thread executor."""
    from jobspy import scrape_jobs
    all_dfs = []
    for state in target_states:
        for term in target_titles:
            try:
                df = scrape_jobs(
                    site_name=list(sites),
                    search_term=term,
                    location=state,
                    results_wanted=results_per_query,
                    hours_old=hours_old,
                    country_indeed="USA",
                )
                all_dfs.append(df)
            except Exception:
                continue
    if not all_dfs:
        return pd.DataFrame()
    return pd.concat(all_dfs, ignore_index=True)


async def fetch_jobs(target_titles, target_states, *, hours_old=72, results_per_query=40, sites=("indeed",)):
    """Async wrapper — runs JobSpy in thread executor and filters."""
    loop = asyncio.get_event_loop()
    df = await loop.run_in_executor(
        None,
        lambda: _run_blocking(target_titles, target_states, hours_old=hours_old,
                              results_per_query=results_per_query, sites=sites),
    )
    if df.empty:
        return []

    # Date-posted freshness filter
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_old)
    df['date_posted_dt'] = pd.to_datetime(df['date_posted'], errors='coerce', utc=True)
    df = df[df['date_posted_dt'] >= cutoff]

    # Title match
    title_rx = _build_title_regex(target_titles)
    df = df[df['title'].fillna('').str.contains(title_rx, regex=True, na=False)]

    # State in target set
    target_abbrs = {s[:2].upper() if len(s) == 2 else _STATE_MAP.get(s.lower(), s[:2].upper())
                    for s in target_states}
    df = df[df['location'].fillna('').apply(lambda L: _state_from_location(L) in target_abbrs)]

    postings = []
    for _, row in df.iterrows():
        loc = row.get('location') or ''
        postings.append(JobPosting(
            source=row.get('site') or 'indeed',
            source_id=str(row.get('id') or row.get('job_url') or row.get('title')),
            company_name=str(row.get('company') or '').strip(),
            company_domain=None,
            job_title=str(row.get('title') or '').strip(),
            job_location=loc,
            job_city=_city_from_location(loc),
            job_state=_state_from_location(loc),
            job_url=row.get('job_url') or '',
            description=_strip_html(row.get('description') or row.get('description_html') or '')[:8000],
            reports_to_raw=_extract_reports_to(row.get('description') or ''),
        ))
    return postings


_STATE_MAP = {
    "massachusetts": "MA", "rhode island": "RI", "new hampshire": "NH",
    "vermont": "VT", "maine": "ME",
}
