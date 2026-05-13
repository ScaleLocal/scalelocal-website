"""BD++ single-password auth via API key header or query param.

Frontend sends header: X-BDPP-Token: <SHARED_PASSWORD>
Or for CSV downloads (which can't easily set headers from <a> tags): ?token=<SHARED_PASSWORD>

Configured via env var BDPP_ACCESS_TOKEN. If unset, auth is disabled (dev mode).
"""
from __future__ import annotations
import os
from fastapi import Header, HTTPException, Query


def get_required_token():
    return os.environ.get("BDPP_ACCESS_TOKEN", "")


def require_auth(
    x_bdpp_token: str | None = Header(default=None, alias="X-BDPP-Token"),
    token: str | None = Query(default=None),
):
    """FastAPI dependency: enforce shared-password auth on a route."""
    required = get_required_token()
    if not required:
        return True  # dev mode — auth disabled
    supplied = x_bdpp_token or token
    if supplied != required:
        raise HTTPException(401, "Invalid or missing BD++ access token")
    return True
