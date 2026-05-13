"""GET /api/export — stream CSV of selected items."""
from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..db.models import QueueItem
from ..services.csv_service import queue_items_to_csv_bytes

router = APIRouter(prefix="/api", tags=["export"])


@router.get("/export")
async def export_csv(
    status: str = Query("ENRICHED", description="ENRICHED, DISCOVERED, EXPORTED, ENRICHED_AND_DISCOVERED, ALL"),
    tag: str = Query("BD"),
    industry: str = Query(""),
    mark_as_exported: bool = Query(False),
    intel_position: bool = Query(False),
    intel_company: bool = Query(False),
    intel_contact: bool = Query(False),
    ids: list[int] | None = Query(None),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(QueueItem)
    if ids:
        stmt = stmt.where(QueueItem.id.in_(ids))
    elif status == "ENRICHED_AND_DISCOVERED":
        stmt = stmt.where(QueueItem.status.in_(["ENRICHED", "DISCOVERED"]))
    elif status == "ALL":
        stmt = stmt.where(QueueItem.status != "DELETED")
    else:
        stmt = stmt.where(QueueItem.status == status)
    items = (await db.execute(stmt.order_by(QueueItem.id.desc()))).scalars().all()
    if not items:
        raise HTTPException(404, "No matching items")

    csv_bytes = queue_items_to_csv_bytes(
        items, tag=tag, industry=industry,
        intel_position=intel_position, intel_company=intel_company, intel_contact=intel_contact,
    )

    if mark_as_exported:
        for it in items:
            it.status = "EXPORTED"
            it.exported_at = datetime.utcnow()
        await db.commit()

    filename = f"bdpp_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
