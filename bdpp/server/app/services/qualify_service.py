"""Qualify discovered postings against size + industry filters.

Loads fortune500.txt blacklist (bundled with project root). Applies word-boundary matching.
"""
from __future__ import annotations
import re
from collections import defaultdict
from pathlib import Path


def _project_root_blacklist():
    """Locate fortune500.txt; bundled into the repo."""
    # server/app/services/qualify_service.py -> ../../../config/fortune500.txt
    here = Path(__file__).resolve()
    bl = here.parents[3] / "config" / "fortune500.txt"
    if bl.exists():
        return bl
    return None


def load_blacklist():
    path = _project_root_blacklist()
    if not path:
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line.lower())
    return out


def _normalize_name(n):
    n = (n or "").lower()
    n = re.sub(r"\b(inc|corp|corporation|company|co|llc|ltd|plc|limited|holdings)\.?\b", " ", n)
    n = re.sub(r"[^a-z0-9\s]", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def is_blacklisted(name, blacklist):
    nc = _normalize_name(name)
    if not nc:
        return False, ""
    for entry in blacklist:
        ne = _normalize_name(entry)
        if not ne:
            continue
        if len(ne) <= 4:
            if nc == ne:
                return True, entry
            continue
        if ne == nc:
            return True, entry
        if re.search(rf"\b{re.escape(ne)}\b", nc):
            return True, entry
        if re.search(rf"\b{re.escape(nc)}\b", ne):
            return True, entry
    return False, ""


def qualify_postings(postings, *, exclude_fortune500, max_active_postings, max_office_locations):
    """In: list of dict postings from discovery_service. Out: list of qualifying dicts."""
    bl = load_blacklist() if exclude_fortune500 else []
    by_company = defaultdict(list)
    for p in postings:
        by_company[(p.get("company_name") or "").strip().lower()].append(p)

    seen = set()
    qualified = []
    for p in postings:
        cname = (p.get("company_name") or "").strip()
        if not cname:
            continue
        key = cname.lower()
        if key in seen:
            continue  # one row per company
        if exclude_fortune500:
            blocked, _hit = is_blacklisted(cname, bl)
            if blocked:
                continue
        same = by_company.get(key, [])
        if len(same) > max_active_postings:
            continue
        cities = {(x.get("bd_job_city") or "").strip().lower() for x in same if x.get("bd_job_city")}
        if len(cities) > max_office_locations:
            continue
        seen.add(key)
        # Keep the richest description out of all same-company postings
        same.sort(key=lambda x: -len(x.get("bd_job_description") or ""))
        qualified.append(same[0])
    return qualified
