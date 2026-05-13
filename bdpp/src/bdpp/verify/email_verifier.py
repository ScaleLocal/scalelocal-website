"""Email guessing + MillionVerifier deliverability check.

Patterns tried, in order (max 4 verifies per contact to honor the cap):
  1) firstname.lastname@domain
  2) flastname@domain
  3) firstname@domain
  4) first.l@domain

Returns first verified-deliverable hit. 'catch-all' is treated as risky-yes (still returned but flagged).
"""
from __future__ import annotations

import asyncio
import re
from typing import Optional

import httpx

from ..budget import BudgetTracker

COST_PER_VERIFY_USD = 0.003


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())


def email_patterns(first: str, last: str, domain: str) -> list[str]:
    f = _normalize(first)
    l = _normalize(last)
    if not f or not domain:
        return []
    pats: list[str] = []
    if l:
        pats.append(f"{f}.{l}@{domain}")
        pats.append(f"{f[0]}{l}@{domain}")
    pats.append(f"{f}@{domain}")
    if l:
        pats.append(f"{f}.{l[0]}@{domain}")
    # dedupe preserving order
    seen = set()
    out = []
    for p in pats:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out[:4]


async def verify_email(client: httpx.AsyncClient, api_token: str, email: str) -> str:
    """Returns 'deliverable' | 'catch-all' | 'undeliverable' | 'unknown' (or 'error')."""
    url = "https://api.millionverifier.com/api/v3/"
    params = {"api": api_token, "email": email, "timeout": 10}
    try:
        r = await client.get(url, params=params, timeout=15.0)
        if r.status_code != 200:
            return "error"
        data = r.json() or {}
        result = (data.get("result") or "").lower()
        return result or "unknown"
    except Exception:
        return "error"


async def verify_or_guess(
    first: str, last: str, domain: str,
    *, mv_token: str, budget: BudgetTracker,
) -> tuple[Optional[str], Optional[str]]:
    """Return (best_email, verification_status) — or (None, None) if no token / budget."""
    if not mv_token or not domain:
        return None, None
    patterns = email_patterns(first, last, domain)
    if not patterns:
        return None, None

    async with httpx.AsyncClient() as client:
        for pat in patterns:
            cost = COST_PER_VERIFY_USD
            if not budget.can_afford(cost, critical=True):
                return None, None
            status = await verify_email(client, mv_token, pat)
            budget.charge("millionverifier", f"verify:{pat}", cost)
            if status == "deliverable":
                return pat, "deliverable"
            if status == "catch-all":
                # accept catch-all but keep trying — a deliverable would be better
                # save it as fallback
                catch_all = (pat, "catch-all")
                # try the rest
                for pat2 in patterns[patterns.index(pat) + 1:]:
                    if not budget.can_afford(COST_PER_VERIFY_USD, critical=True):
                        break
                    s2 = await verify_email(client, mv_token, pat2)
                    budget.charge("millionverifier", f"verify:{pat2}", COST_PER_VERIFY_USD)
                    if s2 == "deliverable":
                        return pat2, "deliverable"
                return catch_all
    return None, None
