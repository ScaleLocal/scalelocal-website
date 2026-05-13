"""GET/PATCH /api/queue — list, filter, manipulate queue items."""
from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..db.models import QueueItem
from ..db.schemas import QueueItemOut

router = APIRouter(prefix="/api/queue", tags=["queue"])


@router.get("", response_model=list[QueueItemOut])
async def list_queue(
    status: Optional[str] = Query(default=None),
    limit: int = Query(default=200, le=2000),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(QueueItem)
    if status:
        if status == "ALL":
            stmt = stmt.where(QueueItem.status != "DELETED")
        else:
            stmt = stmt.where(QueueItem.status == status)
    else:
        stmt = stmt.where(QueueItem.status != "DELETED")
    stmt = stmt.order_by(QueueItem.id.desc()).limit(limit)
    items = (await db.execute(stmt)).scalars().all()
    return items


@router.get("/counts")
async def queue_counts(db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(
        select(QueueItem.status, func.count()).group_by(QueueItem.status)
    )).all()
    return {row[0]: row[1] for row in rows}


@router.post("/delete")
async def delete_items(ids: list[int], db: AsyncSession = Depends(get_session)):
    for iid in ids:
        item = await db.get(QueueItem, iid)
        if item:
            item.status = "DELETED"
    await db.commit()
    return {"deleted": len(ids)}


@router.post("/reset")
async def reset_status(ids: list[int], new_status: str = "DISCOVERED",
                      db: AsyncSession = Depends(get_session)):
    for iid in ids:
        item = await db.get(QueueItem, iid)
        if item:
            item.status = new_status
    await db.commit()
    return {"reset": len(ids), "new_status": new_status}
