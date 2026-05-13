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




# ---- ADDITIONAL EXCLUSION RULES ---------------------------------------------

# Contract / temporary indicators in job_type or title
CONTRACT_TYPE_WORDS = {"contract", "contractor", "temp", "temporary", "freelance", "1099", "c2c", "corp-to-corp"}
CONTRACT_TITLE_WORDS = ["contract", "contractor", "1099", "c2c", "corp to corp", "corp-to-corp",
                        "temp ", "temporary", "freelance", "consultant ", "consulting "]

# Co-op / internship indicators
INTERN_TITLE_WORDS = ["intern", "internship", "co-op", "coop", "co op", "(fall ", "(spring ", "(summer ",
                       "fall 20", "spring 20", "summer 20", "fall semester", "spring semester",
                       "rotational program", "early career program", "graduate program", "trainee"]
INTERN_TYPE_WORDS = {"internship", "intern", "co-op", "coop"}

# JD-text patterns indicating the posting is from a recruiter/staffing agency
RECRUITER_JD_PHRASES = [
    "our client is", "we are recruiting for", "on behalf of our client",
    "client is seeking", "our client seeks", "client is looking for",
    "we have an opening with our client", "our client, a", "for our client",
    "looking for someone for our client", "this is a contract role",
    "this is a contract opportunity", "via our staffing", "staffing agency",
    "talent acquisition partner", "recruitment partner",
]

# JD-text patterns indicating the posting is at a publicly-traded company
PUBLIC_COMPANY_PHRASES = [
    "publicly traded", "publicly-traded", "publicly held",
    "fortune 500", "fortune 1000", "fortune 100",
    "nyse:", "nasdaq:", "(nyse:", "(nasdaq:",
    "s&p 500", "russell 1000", "russell 3000",
    "shareholders", "shareholder value", "shareholder return",
    "annual report", "proxy statement", "10-k filing",
]


def _is_intern_role(posting: dict) -> tuple[bool, str]:
    """Return (True, reason) if posting is an internship or co-op."""
    jt = (posting.get("job_type") or "").lower()
    if jt:
        for w in INTERN_TYPE_WORDS:
            if w in jt:
                return True, f"job_type={jt}"
    title = (posting.get("bd_job_title") or "").lower()
    for w in INTERN_TITLE_WORDS:
        if w in title:
            return True, f"title contains {w!r}"
    return False, ""


def _is_contract_role(posting: dict) -> tuple[bool, str]:
    """Return (True, reason) if posting is a contract/temp/freelance role."""
    jt = (posting.get("job_type") or "").lower()
    if jt:
        for w in CONTRACT_TYPE_WORDS:
            if w in jt:
                return True, f"job_type={jt}"
    title = (posting.get("bd_job_title") or "").lower()
    for w in CONTRACT_TITLE_WORDS:
        if w in title:
            return True, f"title contains {w!r}"
    return False, ""


def _is_recruiter_posting(posting: dict) -> tuple[bool, str]:
    """Return (True, reason) if JD body suggests this is a recruiter / staffing posting."""
    desc = (posting.get("bd_job_description") or "").lower()
    if not desc:
        return False, ""
    for phrase in RECRUITER_JD_PHRASES:
        if phrase in desc:
            return True, f"JD contains {phrase!r}"
    return False, ""


def _is_public_company(posting: dict) -> tuple[bool, str]:
    """Return (True, reason) if JD body or company name signals publicly-traded employer."""
    desc = (posting.get("bd_job_description") or "").lower()
    if not desc:
        return False, ""
    for phrase in PUBLIC_COMPANY_PHRASES:
        if phrase in desc:
            return True, f"JD contains {phrase!r}"
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

        # 1. Blacklist (Fortune 500 / 500+ headcount / staffing / consulting)
        if exclude_fortune500:
            blocked, _hit = is_blacklisted(cname, bl)
            if blocked:
                continue

        # 2. Contract / temp role exclusion
        if _is_contract_role(p)[0]:
            continue

        # 2b. Internship / co-op exclusion
        if _is_intern_role(p)[0]:
            continue

        # 3. Recruiter / staffing-agency JD exclusion
        if _is_recruiter_posting(p)[0]:
            continue

        # 4. Publicly-traded company JD exclusion
        if _is_public_company(p)[0]:
            continue

        # 5. Posting-count cap (size proxy)
        same = by_company.get(key, [])
        if len(same) > max_active_postings:
            continue

        # 6. Office-locations cap (size proxy)
        cities = {(x.get("bd_job_city") or "").strip().lower() for x in same if x.get("bd_job_city")}
        if len(cities) > max_office_locations:
            continue

        seen.add(key)
        # Keep the richest description out of all same-company postings
        same.sort(key=lambda x: -len(x.get("bd_job_description") or ""))
        qualified.append(same[0])
    return qualified
