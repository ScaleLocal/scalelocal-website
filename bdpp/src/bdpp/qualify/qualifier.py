"""Qualification — applies F500 blacklist, posting count, location count."""
from __future__ import annotations
import re
from collections import defaultdict
from pathlib import Path
from ..config import CONFIG_DIR
from ..models import CompanyProfile, JobPosting


def load_blacklist(path=None):
    path = path or (CONFIG_DIR / "fortune500.txt")
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line.lower())
    return out


def _normalize_name(n):
    """Strip punctuation, common suffixes, lowercase, collapse whitespace."""
    n = (n or "").lower()
    # Remove Inc, Corp, LLC, Ltd, Co., Corporation, Company suffix
    n = re.sub(r"\b(inc|corp|corporation|company|co|llc|ltd|plc|limited|holdings)\.?\b", " ", n)
    n = re.sub(r"[^a-z0-9\s]", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n


def _is_blacklisted(company_name, blacklist):
    """Word-boundary match: a blacklist entry must appear as a complete word phrase."""
    norm_company = _normalize_name(company_name)
    if not norm_company:
        return False, ""
    company_tokens = set(norm_company.split())
    for entry in blacklist:
        norm_entry = _normalize_name(entry)
        if not norm_entry:
            continue
        # Skip very short blacklist tokens like "ati", "hp", "ge" — only allow them if they're THE entire company name
        if len(norm_entry) <= 4:
            if norm_company == norm_entry:
                return True, entry
            continue
        # For longer entries: require the entry to appear as a contiguous word sequence in the company name
        # Or the company name to be entirely contained in the entry (e.g. "raytheon" in "raytheon technologies")
        if norm_entry == norm_company:
            return True, entry
        # Word-boundary substring check
        if re.search(rf"\b{re.escape(norm_entry)}\b", norm_company):
            return True, entry
        if re.search(rf"\b{re.escape(norm_company)}\b", norm_entry):
            return True, entry
    return False, ""


def _count_locations(postings_for_company):
    cities = {(p.job_city or "").strip().lower() for p in postings_for_company if p.job_city}
    return len(cities)


def qualify_companies(
    postings,
    *,
    exclude_fortune500=True,
    max_active_postings=100,
    max_office_locations=3,
    blacklist=None,
    all_postings_for_count=None,
):
    bl = blacklist if blacklist is not None else load_blacklist()
    bigpool = all_postings_for_count or postings
    by_company = defaultdict(list)
    for p in bigpool:
        by_company[(p.company_name or "").strip().lower()].append(p)

    out = []
    for posting in postings:
        cname = (posting.company_name or "").strip()
        if not cname:
            continue
        profile = CompanyProfile(name=cname, domain=posting.company_domain)
        if exclude_fortune500:
            is_bl, hit = _is_blacklisted(cname, bl)
            if is_bl:
                profile.is_fortune500 = True
                profile.qualification_status = "fail"
                profile.qualification_reason = f"Blacklisted: matched {hit!r}"
                continue
        same = by_company.get(cname.lower(), [])
        profile.active_postings_count = len(same)
        if profile.active_postings_count > max_active_postings:
            profile.qualification_status = "fail"
            profile.qualification_reason = f">{max_active_postings} active postings"
            continue
        loc_count = _count_locations(same)
        profile.location_count = loc_count
        if loc_count > max_office_locations:
            profile.qualification_status = "fail"
            profile.qualification_reason = f">{max_office_locations} locations"
            continue
        profile.qualification_status = "pass"
        out.append((posting, profile))
    return out
