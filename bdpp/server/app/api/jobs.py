"""GET /api/jobs/:id — poll status of a background job."""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_session
from ..db.models import BackgroundJob
from ..db.schemas import JobOut

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: int, db: AsyncSession = Depends(get_session)):
    job = await db.get(BackgroundJob, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@router.get("", response_model=list[JobOut])
async def list_jobs(limit: int = 20, db: AsyncSession = Depends(get_session)):
    stmt = select(BackgroundJob).order_by(BackgroundJob.id.desc()).limit(limit)
    jobs = (await db.execute(stmt)).scalars().all()
    return jobs
