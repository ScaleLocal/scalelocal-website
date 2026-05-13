"""POST /api/enrich — kicks off enrichment as a background job."""
from __future__ import annotations
import asyncio
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_session
from ..db.models import BackgroundJob, QueueItem, SpendLedger
from ..db.schemas import EnrichRequest, JobOut
from ..services.contact_service import resolve_contacts_for_company
from ..services.email_service import verify_or_guess
from ..services.intel_service import extract_skills
from ..settings import get_settings

router = APIRouter(prefix="/api", tags=["enrich"])


async def _run_enrich_job(job_id: int, params: dict):
    from ..db.base import SessionLocal
    settings = get_settings()
    spent = 0.0
    enriched_count = 0
    async with SessionLocal() as db:
        job = await db.get(BackgroundJob, job_id)
        if job is None:
            return
        job.status = "RUNNING"
        await db.commit()
        try:
            # Select rows: either explicit IDs or first N DISCOVERED
            if params.get("queue_item_ids"):
                stmt = select(QueueItem).where(QueueItem.id.in_(params["queue_item_ids"]))
            else:
                stmt = (select(QueueItem)
                        .where(QueueItem.status == "DISCOVERED")
                        .order_by(QueueItem.id.asc())
                        .limit(params.get("max_companies", 100)))
            items = (await db.execute(stmt)).scalars().all()
            job.progress_total = len(items)
            await db.commit()

            cap = params.get("max_spend_usd", 6.0)

            for item in items:
                if spent >= cap * 0.95:
                    break  # leave headroom; remaining stay DISCOVERED
                # Mark ENRICHING for live UI feedback
                item.status = "ENRICHING"
                await db.commit()

                # Resolve contacts
                domain = item.company_domain or (
                    item.company_website.replace("https://", "").replace("http://", "").lstrip("www.").split("/")[0]
                    if item.company_website else None
                )
                result = await resolve_contacts_for_company(
                    company_name=item.company_name,
                    website=item.company_website,
                    domain=domain,
                    job_description=item.bd_job_description or "",
                    google_api_key=settings.google_api_key,
                    google_cse_id=settings.google_cse_id,
                    apollo_api_key=settings.apollo_api_key,
                    use_apollo_fallback=params.get("use_apollo_fallback", True),
                )
                spent += result.get("cost_usd", 0.0)

                hiring = result.get("hiring_manager")
                hr = result.get("hr")

                # Email verify each
                for contact in (hiring, hr):
                    if contact and domain and settings.millionverifier_token:
                        if spent >= cap:
                            break
                        email, status, cost = await verify_or_guess(
                            contact.get("first_name"), contact.get("last_name"),
                            domain, mv_token=settings.millionverifier_token,
                        )
                        spent += cost
                        if email:
                            contact["email"] = email
                            contact["email_verification_status"] = status

                item.hiring_manager = hiring
                item.hr_contact = hr
                item.skills = extract_skills(item.bd_job_description or "", n=3)
                item.enrichment_cost_usd = round(result.get("cost_usd", 0.0), 4)
                item.status = "ENRICHED"
                item.enriched_at = datetime.utcnow()

                # Spend ledger
                if result.get("cost_usd", 0.0) > 0:
                    db.add(SpendLedger(
                        service="contact_resolver",
                        detail=item.company_name,
                        cost_usd=result["cost_usd"],
                        queue_item_id=item.id,
                    ))
                enriched_count += 1
                job.progress_done = enriched_count
                await db.commit()

            remaining = (await db.execute(
                select(QueueItem).where(QueueItem.status == "DISCOVERED")
            )).scalars().all()
            job.status = "DONE"
            job.finished_at = datetime.utcnow()
            job.result = {
                "enriched": enriched_count,
                "spent_usd": round(spent, 4),
                "cap_usd": cap,
                "budget_capped": spent >= cap * 0.95 and len(remaining) > 0,
                "remaining_discovered": len(remaining),
            }
            await db.commit()
        except Exception as e:
            job.status = "ERROR"
            job.finished_at = datetime.utcnow()
            job.error = str(e)[:2000]
            await db.commit()


@router.post("/enrich", response_model=JobOut)
async def start_enrich(
    req: EnrichRequest,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_session),
):
    job = BackgroundJob(
        job_type="enrich",
        status="PENDING",
        params=req.model_dump(),
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    background.add_task(_run_enrich_job, job.id, req.model_dump())
    return job
