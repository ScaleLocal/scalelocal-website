"""Discovery orchestrator."""
from __future__ import annotations
import asyncio
from typing import Optional
from ..budget import BudgetTracker
from ..models import JobPosting
from . import jobspy_source


def _dedup_key(p):
    return (
        (p.company_name or "").strip().lower(),
        (p.job_title or "").strip().lower(),
        (p.job_city or "").strip().lower(),
    )


def dedup_one_per_company(postings):
    by_company = {}
    for p in postings:
        key = (p.company_name or "").strip().lower()
        if not key:
            continue
        existing = by_company.get(key)
        if not existing:
            by_company[key] = p
            continue
        if p.reports_to_raw and not existing.reports_to_raw:
            by_company[key] = p
            continue
        if existing.reports_to_raw and not p.reports_to_raw:
            continue
        if len(p.description or "") > len(existing.description or ""):
            by_company[key] = p
    return list(by_company.values())


async def discover_jobs(
    target_titles,
    target_states,
    *,
    industry: str = "manufacturing",
    hours_old: int = 72,
    results_per_query: int = 50,
    one_per_company: bool = True,
    **kwargs,
):
    postings = await jobspy_source.fetch_jobs(
        target_titles, target_states,
        hours_old=hours_old, results_per_query=results_per_query,
    )
    seen = {}
    for p in postings:
        k = _dedup_key(p)
        if k not in seen:
            seen[k] = p
    out = list(seen.values())
    if one_per_company:
        out = dedup_one_per_company(out)
    return out
