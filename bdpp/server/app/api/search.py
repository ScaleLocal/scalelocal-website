"""POST /api/search — kicks off discovery as a background job."""
from __future__ import annotations
import json
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_session
from ..db.models import BackgroundJob, QueueItem
from ..db.schemas import SearchRequest, JobOut
from ..services.dedup import make_dedup_key
from ..services.discovery_service import run_discovery
from ..services.qualify_service import qualify_postings

router = APIRouter(prefix="/api", tags=["search"])


async def _run_search_job(job_id: int, params: dict):
    """Runs in a background task. Updates BackgroundJob status + creates QueueItems."""
    from ..db.base import SessionLocal
    async with SessionLocal() as db:
        job = await db.get(BackgroundJob, job_id)
        if job is None:
            return
        job.status = "RUNNING"
        await db.commit()

        try:
            postings = run_discovery(
                industry=params["industry"],
                job_titles=params["job_titles"],
                job_title_exact=params.get("job_title_exact") or [],
                locations=params["locations"],
                hours_old=params["hours_old"],
                results_per_query=params["results_per_query"],
            )
            qualified = qualify_postings(
                postings,
                exclude_fortune500=params["exclude_fortune500"],
                max_active_postings=params["max_active_postings"],
                max_office_locations=params["max_office_locations"],
            )
            added = 0
            skipped = 0
            for q in qualified:
                key = make_dedup_key(q["company_name"], q["bd_job_title"], q["bd_job_location"])
                # Check dedup
                existing = (await db.execute(
                    select(QueueItem).where(QueueItem.dedup_key == key)
                )).scalar_one_or_none()
                if existing:
                    skipped += 1
                    continue
                item = QueueItem(
                    status="DISCOVERED",
                    search_tag=params.get("tag"),
                    search_industry=params.get("industry"),
                    company_name=q["company_name"],
                    bd_job_title=q["bd_job_title"],
                    bd_job_location=q.get("bd_job_location"),
                    bd_job_city=q.get("bd_job_city"),
                    bd_job_state=q.get("bd_job_state"),
                    bd_job_url=q.get("bd_job_url"),
                    bd_job_source=q.get("source"),
                    bd_job_description=q.get("bd_job_description"),
                    dedup_key=key,
                )
                db.add(item)
                added += 1
            job.status = "DONE"
            job.finished_at = datetime.utcnow()
            job.result = {
                "discovered_postings": len(postings),
                "qualified": len(qualified),
                "added_to_queue": added,
                "skipped_duplicates": skipped,
            }
            job.progress_done = job.progress_total = len(qualified)
            await db.commit()
        except Exception as e:
            job.status = "ERROR"
            job.finished_at = datetime.utcnow()
            job.error = str(e)[:2000]
            await db.commit()


@router.post("/search", response_model=JobOut)
async def start_search(
    req: SearchRequest,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_session),
):
    """Start a search job. Returns immediately with the job id; client polls /api/jobs/{id}."""
    job = BackgroundJob(
        job_type="search",
        status="PENDING",
        params=req.model_dump(),
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    background.add_task(_run_search_job, job.id, req.model_dump())
    return job
