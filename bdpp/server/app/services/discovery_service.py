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
    """Build a flexible regex from target title phrases.

    For each title like "Controls Engineer":
      - lowercase, split into words
      - require each word to appear as a whole word in the job title (in any order would be too loose,
        but in original order with anything between is right)
      - allow common engineering modifiers between words (Sr/Senior/Principal/Staff/Lead/Associate/etc.)
    Examples that should match for "Controls Engineer":
      - "Controls Engineer"
      - "Senior Controls Engineer"
      - "Principal Controls Engineering"
      - "Controls and Automation Engineer"
      - "Lead Controls Engineer III"
    """
    parts = []
    for t in titles:
        words = [re.escape(w) for w in t.lower().split() if w]
        if not words:
            continue
        # Require each word to appear (in order) as a whole word, with anything between
        # The last word allows an optional "s" or "ing" suffix for plural/gerund variants
        seq = []
        for i, w in enumerate(words):
            if i == len(words) - 1:
                # final word: allow engineer/engineering/engineers, etc.
                seq.append(rf"\b{w}(?:s|ing|ers|ering)?\b")
            else:
                seq.append(rf"\b{w}s?\b")
        # Join with ".{0,40}?" — anything (up to 40 chars) can appear between consecutive words
        pattern = ".{0,40}?".join(seq)
        parts.append(pattern)
    if not parts:
        return r"^$"  # match nothing if no titles
    return r"(?i)(" + "|".join(parts) + ")"


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
    """Returns list of dicts (one per posting). Drop empty/'nan' companies upstream.

    Defensive: wrapped in try/except so a single bad title-state combo can't take
    the whole search down. Returns [] on any unrecoverable parse error.
    """
    try:
        return _run_discovery_inner(industry, job_titles, locations, hours_old, results_per_query, **kwargs)
    except Exception as e:
        import logging
        logging.warning(f"[discovery] failed cleanly with {type(e).__name__}: {e}")
        return []


def _run_discovery_inner(industry, job_titles, locations, hours_old, results_per_query, **kwargs):
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
                if df is None or len(df) == 0:
                    continue
                all_dfs.append(df)
            except Exception:
                continue
    if not all_dfs:
        return []
    df = pd.concat(all_dfs, ignore_index=True)
    if df.empty:
        return []
    # Guard: JobSpy occasionally drops columns when no rows match. Ensure required columns exist.
    for col in ["company", "title", "location", "date_posted", "job_url", "description", "job_type", "site"]:
        if col not in df.columns:
            df[col] = ""

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_old)
    df["date_posted_dt"] = pd.to_datetime(df["date_posted"], errors="coerce", utc=True)
    df = df[df["date_posted_dt"] >= cutoff]
    if df.empty or "company" not in df.columns:
        return []
    title_rx = _build_title_rx(job_titles)
    df = df[df["title"].fillna("").str.contains(title_rx, regex=True, na=False)]
    if df.empty or "company" not in df.columns:
        return []
    target = {_norm_state(s) for s in locations}
    df = df[df["location"].fillna("").apply(lambda L: _state_from_loc(L) in target)]
    if df.empty or "company" not in df.columns:
        return []
    # Drop empties / NaNs
    df = df[df["company"].fillna("").apply(lambda c: str(c).strip().lower() not in {"", "nan", "none"})]
    if df.empty:
        return []

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
            "job_type": (str(row.get("job_type") or "") if not isinstance(row.get("job_type"), list) else " ".join(str(x) for x in (row.get("job_type") or []))).lower(),
        })
    return out
