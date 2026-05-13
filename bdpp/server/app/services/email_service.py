"""Email pattern-guess + MillionVerifier deliverability."""
from __future__ import annotations
import re
import httpx


COST_PER_VERIFY_USD = 0.003


def _norm(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())


def email_patterns(first, last, domain):
    f, l = _norm(first), _norm(last)
    if not f or not domain:
        return []
    out = []
    if l:
        out.append(f"{f}.{l}@{domain}")
        out.append(f"{f[0]}{l}@{domain}")
    out.append(f"{f}@{domain}")
    if l:
        out.append(f"{f}.{l[0]}@{domain}")
    seen = set()
    deduped = []
    for p in out:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped[:4]


async def verify_email_once(client, token, email):
    if not token or not email:
        return "error"
    try:
        r = await client.get(
            "https://api.millionverifier.com/api/v3/",
            params={"api": token, "email": email, "timeout": 10},
            timeout=15.0,
        )
        if r.status_code != 200:
            return "error"
        return ((r.json() or {}).get("result") or "unknown").lower()
    except Exception:
        return "error"


async def verify_or_guess(first, last, domain, *, mv_token):
    """Return (email, status, cost_usd). Capped at 4 verify calls per contact."""
    cost = 0.0
    if not mv_token or not domain:
        return None, None, cost
    patterns = email_patterns(first, last, domain)
    fallback = None
    async with httpx.AsyncClient() as client:
        for pat in patterns:
            cost += COST_PER_VERIFY_USD
            status = await verify_email_once(client, mv_token, pat)
            if status == "deliverable":
                return pat, "deliverable", cost
            if status == "catch-all" and not fallback:
                fallback = (pat, "catch-all")
    if fallback:
        return fallback[0], fallback[1], cost
    return None, None, cost
