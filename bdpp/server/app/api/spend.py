"""GET /api/spend — spend summary today / 7d / lifetime."""
from __future__ import annotations
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..db.models import SpendLedger

router = APIRouter(prefix="/api", tags=["spend"])


@router.get("/spend")
async def spend_summary(db: AsyncSession = Depends(get_session)):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    week_start = now - timedelta(days=7)

    today_total = (await db.execute(
        select(func.coalesce(func.sum(SpendLedger.cost_usd), 0.0))
        .where(SpendLedger.created_at >= today_start)
    )).scalar() or 0.0

    week_total = (await db.execute(
        select(func.coalesce(func.sum(SpendLedger.cost_usd), 0.0))
        .where(SpendLedger.created_at >= week_start)
    )).scalar() or 0.0

    lifetime = (await db.execute(
        select(func.coalesce(func.sum(SpendLedger.cost_usd), 0.0))
    )).scalar() or 0.0

    by_svc = (await db.execute(
        select(SpendLedger.service, func.coalesce(func.sum(SpendLedger.cost_usd), 0.0))
        .group_by(SpendLedger.service)
    )).all()

    return {
        "today_usd": round(float(today_total), 4),
        "last_7d_usd": round(float(week_total), 4),
        "lifetime_usd": round(float(lifetime), 4),
        "by_service": {row[0]: round(float(row[1]), 4) for row in by_svc},
    }
