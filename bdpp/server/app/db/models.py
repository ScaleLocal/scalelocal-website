"""SQLAlchemy ORM models — BD++ queue + spend + jobs."""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class QueueItem(Base):
    """Persistent queue of (company, job_posting) — one row per company-job pair."""
    __tablename__ = "queue_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="DISCOVERED", index=True)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    enriched_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    exported_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Search metadata
    search_tag: Mapped[str | None] = mapped_column(String(200), nullable=True)
    search_industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)

    # Company
    company_name: Mapped[str] = mapped_column(String(300), index=True)
    company_domain: Mapped[str | None] = mapped_column(String(300), nullable=True)
    company_website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    company_intel: Mapped[str | None] = mapped_column(String(500), nullable=True)
    employee_band: Mapped[str | None] = mapped_column(String(50), nullable=True)
    company_linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # BD job posting
    bd_job_title: Mapped[str] = mapped_column(String(500))
    bd_job_location: Mapped[str | None] = mapped_column(String(300), nullable=True)
    bd_job_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bd_job_state: Mapped[str | None] = mapped_column(String(10), nullable=True)
    bd_job_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    bd_job_source: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bd_job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    bd_job_reports_to: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bd_job_posted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Enrichment results (JSON for flexibility — fields evolve)
    hiring_manager: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    hr_contact: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    contact_intel: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Tracking
    enrichment_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    dedup_key: Mapped[str] = mapped_column(String(700), unique=True, index=True)

    __table_args__ = (
        Index("idx_status_discovered", "status", "discovered_at"),
    )


class SpendLedger(Base):
    """Per-day spend tracking — append-only."""
    __tablename__ = "spend_ledger"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    service: Mapped[str] = mapped_column(String(100))     # millionverifier | outscraper | apollo | google_cse
    detail: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    queue_item_id: Mapped[int | None] = mapped_column(ForeignKey("queue_items.id"), nullable=True)
    user: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)


class BackgroundJob(Base):
    """Tracks long-running tasks: search, enrich, export. Frontend polls /api/jobs/:id."""
    __tablename__ = "background_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    job_type: Mapped[str] = mapped_column(String(50))     # search | enrich | export
    status: Mapped[str] = mapped_column(String(20), default="PENDING")  # PENDING | RUNNING | DONE | ERROR
    params: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    progress_done: Mapped[int] = mapped_column(Integer, default=0)
    progress_total: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
