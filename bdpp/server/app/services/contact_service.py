"""Contact resolver — hybrid free-first, Apollo-fallback strategy.

DESIGN RULES (post-2026-05-14 rework):
  1. Free attempts cost $0. We charge nothing for JD-parsing, website scraping,
     or Google CSE searches. If the user wants to know we tried, the queue row
     shows resolution_attempts: ["jd_reports_to", "site_scrape", "google_cse"].
  2. Paid attempts charge ONLY on success. MillionVerifier verify-email charges
     only when we actually call the API; Apollo charges only when it returns a
     person record.
  3. Every contact gets a confidence_level: HIGH (Apollo/verified email),
     MEDIUM (named in JD or Google CSE LinkedIn hit), LOW (website scrape only).
"""
from __future__ import annotations
import asyncio
import os
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx


# ── TITLE TAXONOMIES ─────────────────────────────────────────────────────────
HIRING_MGR_TITLES = [
    "engineering manager", "director of engineering", "vp engineering",
    "vp of engineering", "head of engineering", "plant manager",
    "director of operations", "vp of operations", "manufacturing manager",
    "manufacturing engineering manager", "controls engineering manager",
    "electrical engineering manager", "chief engineer", "principal engineer",
    "engineering director", "operations manager", "production manager",
]
HR_TITLES = [
    "hr manager", "human resources manager", "talent acquisition manager",
    "talent acquisition", "recruiter", "senior recruiter", "technical recruiter",
    "head of people", "people operations", "vp human resources", "hr generalist",
    "hr business partner", "hrbp", "people partner", "talent partner",
    "director of human resources", "chro", "vp of hr", "people manager",
]
ALL_TARGET_TITLES = HIRING_MGR_TITLES + HR_TITLES

TEAM_PATHS = [
    "/team", "/about/team", "/about-us/team", "/people", "/leadership",
    "/company/leadership", "/about", "/about-us", "/our-team", "/management",
]


def _classify_title(title):
    t = (title or "").lower()
    if any(h in t for h in HR_TITLES):
        return "HR"
    if any(h in t for h in HIRING_MGR_TITLES):
        return "HIRING_MANAGER"
    return "OTHER"


def _split_name(full):
    parts = [p for p in (full or "").strip().split() if p]
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[-1]


# ── ATTEMPT 1: PARSE THE JOB DESCRIPTION ─────────────────────────────────────
_NAME_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)\b")

def parse_jd_for_contact(jd_text: str) -> list[dict]:
    """Scan the JD body for 'Reports to', 'Hiring Manager:', or 'Contact:' patterns.

    Stronger than the original — handles:
      Reports to: Jane Smith
      Reports to: Jane Smith, Director of Engineering
      Hiring Manager: John Doe
      Hiring manager - John Doe
      Please contact Jane Smith
      For questions, reach out to John Doe
    """
    if not jd_text:
        return []
    found = []
    triggers = [
        r"reports?\s+to\s*[:\-]\s*",
        r"reporting\s+to\s*[:\-]\s*",
        r"hiring\s+manager\s*[:\-]\s*",
        r"manager\s*[:\-]\s*",
        r"supervisor\s*[:\-]\s*",
        r"contact\s*[:\-]\s*",
        r"please\s+contact\s+",
        r"reach\s+out\s+to\s+",
    ]
    for trigger in triggers:
        for m in re.finditer(trigger, jd_text, re.IGNORECASE):
            tail = jd_text[m.end(): m.end() + 200]
            name_m = _NAME_RE.search(tail)
            if not name_m:
                continue
            full = name_m.group(1)
            # Look for a title that follows the name within 80 chars
            after_name = tail[name_m.end(): name_m.end() + 120]
            # Capture sequences of (Title-cased words) plus optional connectors like 'of', 'and', '&'
            title_m = re.search(
                r"[,\s\-:]+\s*((?:[A-Z][a-zA-Z\-&]+|of|and|&|\s)+(?:Manager|Director|VP|Lead|Head|Officer|Engineer|Recruiter|Specialist|Coordinator|Partner|Generalist|Architect))",
                after_name
            )
            if title_m:
                title = title_m.group(1).strip().rstrip(",.;:")
            else:
                title = "Hiring Manager (named in JD)"
            first, last = _split_name(full)
            found.append({
                "first_name": first, "last_name": last,
                "title": title, "role_class": _classify_title(title),
                "source": "jd_parse", "confidence": "MEDIUM",
            })
    return found


# ── ATTEMPT 2: COMPANY WEBSITE TEAM PAGE SCRAPE ──────────────────────────────
async def _fetch_html(client, url, timeout=8.0):
    try:
        r = await client.get(url, timeout=timeout, follow_redirects=True)
        if r.status_code == 200 and "text/html" in r.headers.get("content-type", ""):
            return r.text
    except Exception:
        pass
    return ""


def _scrape_team_html(html: str) -> list[dict]:
    if not html:
        return []
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    found = {}
    for i, line in enumerate(lines):
        ll = line.lower()
        title_hit = None
        for t in ALL_TARGET_TITLES:
            if t in ll and len(line) < 120:
                title_hit = line
                break
        if not title_hit:
            continue
        for ctx in lines[max(0, i - 2): i + 3]:
            m = _NAME_RE.search(ctx)
            if not m:
                continue
            full = m.group(1)
            if any(w in full.lower() for w in ["the", "team", "our", "company", "manager",
                                                "engineer", "resources", "department"]):
                continue
            first, last = _split_name(full)
            key = (full.lower(), title_hit.lower())
            if key not in found:
                found[key] = {
                    "first_name": first, "last_name": last,
                    "title": title_hit.strip(), "role_class": _classify_title(title_hit),
                    "source": "site_scrape", "confidence": "LOW",
                }
    return list(found.values())


async def scrape_company_team(client, website: str) -> list[dict]:
    if not website:
        return []
    if not website.startswith("http"):
        website = "https://" + website
    base = website.rstrip("/")
    urls = [urljoin(base + "/", p.lstrip("/")) for p in TEAM_PATHS]
    sem = asyncio.Semaphore(4)
    async def _one(u):
        async with sem:
            html = await _fetch_html(client, u)
            return _scrape_team_html(html) if html else []
    results = await asyncio.gather(*[_one(u) for u in urls], return_exceptions=True)
    out = []
    for r in results:
        if isinstance(r, list):
            out.extend(r)
    return out


# ── ATTEMPT 3: GOOGLE CSE LinkedIn SEARCH ────────────────────────────────────
async def google_cse_linkedin_search(client, company: str, target_role: str) -> list[dict]:
    """Use Google Programmable Search Engine to find named contacts at the company.

    Query example: "Engineering Manager" "Boyd Corporation" site:linkedin.com/in
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    cse_id = os.environ.get("GOOGLE_CSE_ID", "")
    if not api_key or not cse_id:
        return []
    q = f'"{target_role}" "{company}" site:linkedin.com/in'
    try:
        r = await client.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": api_key, "cx": cse_id, "q": q, "num": 5},
            timeout=15.0,
        )
        if r.status_code != 200:
            return []
        items = r.json().get("items", []) or []
    except Exception:
        return []
    out = []
    for it in items:
        title_str = it.get("title", "") or ""
        snippet = it.get("snippet", "") or ""
        link = it.get("link", "") or ""
        # LinkedIn page titles look like: "Jane Smith - Engineering Manager at Boyd Corporation | LinkedIn"
        m = re.match(r"^([A-Z][a-zA-Z\.\-]+(?:\s+[A-Z][a-zA-Z\.\-]+){1,3})\s*[-–|]\s*(.+?)\s+at\s+", title_str)
        if not m:
            # Looser: try _NAME_RE on the title text
            nm = _NAME_RE.search(title_str)
            if not nm:
                continue
            full = nm.group(1)
            inferred_title = target_role
        else:
            full = m.group(1).strip()
            inferred_title = m.group(2).strip() or target_role
        first, last = _split_name(full)
        out.append({
            "first_name": first, "last_name": last,
            "title": inferred_title, "role_class": _classify_title(inferred_title),
            "linkedin_url": link, "source": "google_cse",
            "confidence": "MEDIUM",
        })
    return out




async def bing_linkedin_search(client, company: str, target_role: str) -> list[dict]:
    """Bing Web Search API — same purpose as Google CSE, independent service.

    Requires BING_SEARCH_KEY env var. Free tier: 1000 transactions/month, no billing required.
    Endpoint: https://api.bing.microsoft.com/v7.0/search
    """
    key = os.environ.get("BING_SEARCH_KEY", "")
    if not key:
        return []
    q = f'"{target_role}" "{company}" site:linkedin.com/in'
    try:
        r = await client.get(
            "https://api.bing.microsoft.com/v7.0/search",
            params={"q": q, "count": 5, "mkt": "en-US"},
            headers={"Ocp-Apim-Subscription-Key": key},
            timeout=15.0,
        )
        if r.status_code != 200:
            return []
        items = r.json().get("webPages", {}).get("value", []) or []
    except Exception:
        return []
    out = []
    for it in items:
        title_str = it.get("name", "") or ""
        link = it.get("url", "") or ""
        snippet = it.get("snippet", "") or ""
        m = re.match(r"^([A-Z][a-zA-Z\.\-]+(?:\s+[A-Z][a-zA-Z\.\-]+){1,3})\s*[-\u2013|]\s*(.+?)\s+at\s+", title_str)
        if not m:
            nm = _NAME_RE.search(title_str)
            if not nm:
                continue
            full = nm.group(1)
            inferred_title = target_role
        else:
            full = m.group(1).strip()
            inferred_title = m.group(2).strip() or target_role
        first, last = _split_name(full)
        out.append({
            "first_name": first, "last_name": last,
            "title": inferred_title, "role_class": _classify_title(inferred_title),
            "linkedin_url": link, "source": "bing_search",
            "confidence": "MEDIUM",
        })
    return out


# ── ATTEMPT 4 (paid): APOLLO ─────────────────────────────────────────────────
async def apollo_search(client, api_key: str, company: str, domain: Optional[str]) -> list[dict]:
    if not api_key:
        return []
    titles = HIRING_MGR_TITLES[:6] + HR_TITLES[:4]
    body = {
        "api_key": api_key, "page": 1, "per_page": 10,
        "person_titles": [t.title() for t in titles],
    }
    if domain:
        body["q_organization_domains"] = [domain]
    else:
        body["organization_name"] = company
    try:
        r = await client.post("https://api.apollo.io/v1/people/search",
                              json=body, timeout=20.0)
        if r.status_code != 200:
            return []
        data = r.json()
    except Exception:
        return []
    out = []
    for p in data.get("people") or []:
        first = (p.get("first_name") or "").strip()
        last = (p.get("last_name") or "").strip()
        title = (p.get("title") or "").strip()
        if not first or not last:
            continue
        out.append({
            "first_name": first, "last_name": last,
            "title": title, "role_class": _classify_title(title),
            "email": p.get("email"),
            "linkedin_url": p.get("linkedin_url"),
            "source": "apollo", "confidence": "HIGH",
        })
    return out


# ── MAIN RESOLVER ────────────────────────────────────────────────────────────
def _pick_best(candidates, role_class):
    confidence_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    cands = [c for c in candidates if c.get("role_class") == role_class]
    cands.sort(key=lambda c: (
        -confidence_order.get(c.get("confidence", "LOW"), 0),
        -len(c.get("title", "")),
    ))
    return cands[0] if cands else None


async def resolve_contacts_for_company(
    *, company_name, website, domain, job_description,
    google_api_key=None, google_cse_id=None, apollo_api_key=None,
    use_apollo_fallback=True,
):
    """Returns dict with hiring_manager, hr, attempts[], cost_usd, plus resolution metadata."""
    attempts = []
    candidates = []

    async with httpx.AsyncClient(
        headers={"User-Agent": "BDPlusPlus/0.3 (+contact-resolver)"},
        follow_redirects=True,
    ) as client:
        # 1) Free: JD parse
        attempts.append("jd_parse")
        candidates.extend(parse_jd_for_contact(job_description or ""))

        # 2) Free: company website team scrape
        if website:
            attempts.append("site_scrape")
            candidates.extend(await scrape_company_team(client, website))

        # 3a) Free: Google CSE LinkedIn search
        if os.environ.get("GOOGLE_CSE_ID") and os.environ.get("GOOGLE_API_KEY"):
            attempts.append("google_cse")
            for target in ["Engineering Manager", "Director of Engineering",
                           "VP Engineering", "HR Manager", "Talent Acquisition",
                           "Human Resources Manager"]:
                hits = await google_cse_linkedin_search(client, company_name, target)
                candidates.extend(hits)

        # 3b) Free: Bing Web Search (parallel to Google CSE; independent free quota)
        if os.environ.get("BING_SEARCH_KEY"):
            attempts.append("bing_search")
            for target in ["Engineering Manager", "Director of Engineering",
                           "VP Engineering", "HR Manager", "Talent Acquisition",
                           "Human Resources Manager"]:
                hits = await bing_linkedin_search(client, company_name, target)
                candidates.extend(hits)

        hiring = _pick_best(candidates, "HIRING_MANAGER")
        hr = _pick_best(candidates, "HR")

        # 4) Paid: Apollo (only if free path failed AND key is configured)
        cost = 0.0
        if use_apollo_fallback and apollo_api_key and (hiring is None or hr is None):
            attempts.append("apollo")
            apollo_hits = await apollo_search(client, apollo_api_key, company_name, domain)
            candidates.extend(apollo_hits)
            cost = 0.10 * len(apollo_hits)  # only charge for actual returns
            if hiring is None:
                hiring = _pick_best(apollo_hits, "HIRING_MANAGER")
            if hr is None:
                hr = _pick_best(apollo_hits, "HR")

    return {
        "hiring_manager": hiring,
        "hr": hr,
        "attempts": attempts,
        "cost_usd": cost,  # ZERO for free path, only Apollo charges
        "candidates_found": len(candidates),
    }
