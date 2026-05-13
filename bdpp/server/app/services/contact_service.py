"""Contact resolver — hybrid Free→Apollo strategy.

FREE LAYER (no cost, no API key required):
  1. Parse 'Reports to: <Name>' from the job description
  2. Google search: '"[Company]" "Engineering Manager"' / '"HR Manager"' — via Google CSE if key present
  3. Company website /team /leadership /about scrape — async HTTP, BS4 parse

APOLLO LAYER (paid, fallback only):
  - POST https://api.apollo.io/v1/people/search with q_organization_domains=[domain]
    and person_titles=['Engineering Manager', 'HR Manager', ...]
  - $0.10 per credit on Basic plan; only invoked if free layer found nothing
"""
from __future__ import annotations
import asyncio
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx


HIRING_MGR_TITLES = [
    "engineering manager", "director of engineering", "vp engineering",
    "vp of engineering", "head of engineering", "plant manager",
    "director of operations", "vp of operations", "manufacturing engineering manager",
    "controls engineering manager", "electrical engineering manager", "chief engineer",
]
HR_TITLES = [
    "hr manager", "human resources manager", "talent acquisition manager",
    "talent acquisition", "recruiter", "senior recruiter", "technical recruiter",
    "head of people", "people operations", "vp human resources", "hr generalist",
    "hr business partner", "hrbp",
]
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


def parse_reports_to(text):
    if not text:
        return None
    m = re.search(r"reports\s*to\s*[:\-]\s*([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)", text)
    return m.group(1) if m else None


_NAME_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)\b")


def _scrape_team_html(html):
    """Pull (Name, Title) pairs from a team-page HTML. Best-effort."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    found = {}
    for i, line in enumerate(lines):
        ll = line.lower()
        title_hit = None
        for t in HIRING_MGR_TITLES + HR_TITLES:
            if t in ll and len(line) < 120:
                title_hit = line
                break
        if not title_hit:
            continue
        window = lines[max(0, i - 2): i + 3]
        for ctx in window:
            m = _NAME_RE.search(ctx)
            if m and " " in m.group(1):
                full = m.group(1)
                if any(w in full.lower() for w in ["the", "team", "our", "company", "manager", "engineer", "resources"]):
                    continue
                first, last = _split_name(full)
                role = _classify_title(title_hit)
                key = (full.lower(), title_hit.lower())
                if key not in found:
                    found[key] = {
                        "first_name": first, "last_name": last,
                        "title": title_hit.strip(), "role_class": role,
                        "source": "website_team_page", "confidence": 0.55,
                    }
    return list(found.values())


async def _fetch(client, url, timeout=10.0):
    try:
        r = await client.get(url, timeout=timeout, follow_redirects=True)
        if r.status_code == 200 and "text/html" in r.headers.get("content-type", ""):
            return r.text
    except Exception:
        pass
    return ""


async def resolve_from_website(client, website):
    """Try /team etc. pages on the company website."""
    if not website:
        return []
    if not website.startswith("http"):
        website = "https://" + website
    base = website.rstrip("/")
    urls = [urljoin(base + "/", p.lstrip("/")) for p in TEAM_PATHS]
    sem = asyncio.Semaphore(4)

    async def _one(u):
        async with sem:
            html = await _fetch(client, u)
            return _scrape_team_html(html) if html else []

    chunks = await asyncio.gather(*[_one(u) for u in urls], return_exceptions=True)
    out = []
    for c in chunks:
        if isinstance(c, list):
            out.extend(c)
    return out


# ── Google CSE search for "[Company] Engineering Manager" / "HR Manager"
async def google_search_contacts(client, *, api_key, cse_id, company_name, target_role):
    if not api_key or not cse_id:
        return []
    q = f'"{company_name}" "{target_role}" site:linkedin.com/in'
    url = "https://www.googleapis.com/customsearch/v1"
    try:
        r = await client.get(url, params={"key": api_key, "cx": cse_id, "q": q, "num": 5}, timeout=15.0)
        if r.status_code != 200:
            return []
        items = (r.json() or {}).get("items", []) or []
    except Exception:
        return []
    out = []
    for it in items:
        title = it.get("title") or ""
        snippet = it.get("snippet") or ""
        link = it.get("link") or ""
        m = _NAME_RE.search(title)
        if not m:
            m = _NAME_RE.search(snippet)
        if not m:
            continue
        full = m.group(1)
        if " " not in full:
            continue
        first, last = _split_name(full)
        # Heuristic: if "target_role" appears in title/snippet, classify accordingly
        joined = (title + " " + snippet).lower()
        role = "OTHER"
        if any(h in joined for h in HR_TITLES):
            role = "HR"
        elif any(h in joined for h in HIRING_MGR_TITLES):
            role = "HIRING_MANAGER"
        else:
            role = _classify_title(target_role)
        out.append({
            "first_name": first, "last_name": last,
            "title": target_role, "role_class": role,
            "linkedin_url": link, "source": "google_cse_linkedin",
            "confidence": 0.6,
        })
    return out


# ── Apollo fallback
async def apollo_search(client, *, api_key, company_name, domain):
    """Apollo /v1/people/search. Returns Engineering Manager + HR Manager when found."""
    if not api_key:
        return []
    titles_payload = ["Engineering Manager", "Director of Engineering",
                      "VP Engineering", "HR Manager", "Talent Acquisition",
                      "Recruiter", "Human Resources Manager"]
    body = {
        "api_key": api_key,
        "page": 1, "per_page": 10,
        "person_titles": titles_payload,
    }
    if domain:
        body["q_organization_domains"] = [domain]
    else:
        body["organization_name"] = company_name
    try:
        r = await client.post("https://api.apollo.io/v1/people/search", json=body, timeout=20.0)
        if r.status_code != 200:
            return []
        data = r.json()
    except Exception:
        return []
    people = data.get("people") or []
    out = []
    for p in people:
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
            "source": "apollo", "confidence": 0.85,
        })
    return out


def _pick_best(candidates, role_class):
    cands = [c for c in candidates if c.get("role_class") == role_class]
    cands.sort(key=lambda c: (-len(c.get("title", "")), -float(c.get("confidence") or 0)))
    return cands[0] if cands else None


async def resolve_contacts_for_company(
    *,
    company_name,
    website,
    domain,
    job_description,
    google_api_key=None,
    google_cse_id=None,
    apollo_api_key=None,
    use_apollo_fallback=True,
):
    """Returns {'hiring_manager': dict|None, 'hr': dict|None, 'cost_usd': float}."""
    cost = 0.0
    candidates = []

    # 1) Reports-to in job description
    rt = parse_reports_to(job_description)
    if rt:
        first, last = _split_name(rt)
        candidates.append({
            "first_name": first, "last_name": last,
            "title": "Hiring Manager (named in job post)",
            "role_class": "HIRING_MANAGER",
            "source": "job_post_reports_to", "confidence": 0.9,
        })

    async with httpx.AsyncClient(
        headers={"User-Agent": "BDPlusPlus/0.2"},
        follow_redirects=True,
    ) as client:
        # 2) Free: company website /team scrape
        if website:
            candidates.extend(await resolve_from_website(client, website))

        # 3) Free: Google CSE LinkedIn search (optional — needs CSE key)
        if google_api_key and google_cse_id:
            for role in ["Engineering Manager", "HR Manager"]:
                hits = await google_search_contacts(
                    client, api_key=google_api_key, cse_id=google_cse_id,
                    company_name=company_name, target_role=role,
                )
                candidates.extend(hits)
                cost += 0.005  # Google CSE: 100/day free, then $5/1k = $0.005

        hiring = _pick_best(candidates, "HIRING_MANAGER")
        hr = _pick_best(candidates, "HR")

        # 4) Apollo fallback ONLY if either slot is still empty
        if use_apollo_fallback and apollo_api_key and (hiring is None or hr is None):
            apollo_hits = await apollo_search(
                client, api_key=apollo_api_key,
                company_name=company_name, domain=domain,
            )
            candidates.extend(apollo_hits)
            cost += 0.10 * len(apollo_hits)   # rough — Apollo charges per credit
            if hiring is None:
                hiring = _pick_best(apollo_hits, "HIRING_MANAGER")
            if hr is None:
                hr = _pick_best(apollo_hits, "HR")

    return {"hiring_manager": hiring, "hr": hr, "cost_usd": cost}
