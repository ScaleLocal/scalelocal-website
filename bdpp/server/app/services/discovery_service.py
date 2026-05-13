"""Discovery service — wraps JobSpy to find jobs matching a SearchRequest.

Runs SYNCHRONOUSLY because JobSpy is blocking. The route hands it off to a worker.
"""
from __future__ import annotations
import re
import warnings
from datetime import datetime, timedelta, timezone

import pandas as pd

warnings.filterwarnings("ignore", message="This pattern is interpreted as a regular expression")


def _state_from_loc(loc):
    if not isinstance(loc, str):
        return None
    parts = loc.split(",")
    return parts[1].strip().upper()[:2] if len(parts) >= 2 else None


def _city_from_loc(loc):
    if not isinstance(loc, str):
        return None
    parts = loc.split(",")
    return parts[0].strip() if parts else None


def _build_title_rx(titles):
    parts = []
    for t in titles:
        toks = t.lower().split()
        if "engineer" in toks:
            base = toks[toks.index("engineer") - 1] if toks.index("engineer") > 0 else ""
            parts.append(rf"\b{base}s?\s+engineer")
            parts.append(rf"\b{base}s?\s+engineering")
        else:
            parts.append(re.escape(t.lower()))
    return r"(?i)" + "|".join(parts)


_STATE_NAME_TO_ABBR = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
    "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH",
    "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
    "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
}


def _norm_state(s):
    if not s:
        return None
    s2 = s.strip().lower()
    if len(s2) == 2:
        return s2.upper()
    return _STATE_NAME_TO_ABBR.get(s2)


def run_discovery(industry, job_titles, locations, hours_old, results_per_query, **kwargs):
    """Returns list of dicts (one per posting). Drop empty/'nan' companies upstream."""
    from jobspy import scrape_jobs
    all_dfs = []
    for state in locations:
        for term in job_titles:
            try:
                df = scrape_jobs(
                    site_name=["indeed"],
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
        return []
    df = pd.concat(all_dfs, ignore_index=True)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_old)
    df["date_posted_dt"] = pd.to_datetime(df["date_posted"], errors="coerce", utc=True)
    df = df[df["date_posted_dt"] >= cutoff]
    title_rx = _build_title_rx(job_titles)
    df = df[df["title"].fillna("").str.contains(title_rx, regex=True, na=False)]
    target = {_norm_state(s) for s in locations}
    df = df[df["location"].fillna("").apply(lambda L: _state_from_loc(L) in target)]
    # Drop empties / NaNs
    df = df[df["company"].fillna("").apply(lambda c: c.strip().lower() not in {"", "nan", "none"})]

    out = []
    for _, row in df.iterrows():
        loc = row.get("location") or ""
        out.append({
            "source": row.get("site") or "indeed",
            "company_name": str(row.get("company") or "").strip(),
            "bd_job_title": str(row.get("title") or "").strip(),
            "bd_job_location": loc,
            "bd_job_city": _city_from_loc(loc),
            "bd_job_state": _state_from_loc(loc),
            "bd_job_url": row.get("job_url") or "",
            "bd_job_description": (row.get("description") or "")[:8000],
            "bd_job_posted_at": row.get("date_posted_dt"),
            "job_type": (row.get("job_type") or "").lower(),
        })
    return out
