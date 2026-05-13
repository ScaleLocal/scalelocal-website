"""Pydantic request/response models for the BD++ API."""
from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel


class SearchRequest(BaseModel):
    industry: str
    job_titles: list[str]
    locations: list[str]
    skills: list[str] = []
    hours_old: int = 72
    results_per_query: int = 50
    exclude_fortune500: bool = True
    max_active_postings: int = 100
    max_office_locations: int = 3
    tag: str = "BD"


class EnrichRequest(BaseModel):
    queue_item_ids: list[int] | None = None  # None = enrich all DISCOVERED
    max_spend_usd: float = 6.0
    max_companies: int = 100
    use_apollo_fallback: bool = True
    intel_position: bool = False
    intel_company: bool = False
    intel_contact: bool = False


class ExportRequest(BaseModel):
    queue_item_ids: list[int] | None = None  # None = all ENRICHED
    statuses: list[str] = ["ENRICHED"]
    mark_as_exported: bool = False
    tag: str = "BD"
    industry: str = ""


class QueueItemOut(BaseModel):
    id: int
    status: str
    discovered_at: datetime
    enriched_at: datetime | None = None
    company_name: str
    company_website: str | None = None
    bd_job_title: str
    bd_job_location: str | None = None
    bd_job_url: str | None = None
    hiring_manager: dict | None = None
    hr_contact: dict | None = None
    skills: list | None = None
    company_intel: str | None = None

    class Config:
        from_attributes = True


class JobOut(BaseModel):
    id: int
    job_type: str
    status: str
    created_at: datetime
    finished_at: datetime | None = None
    progress_done: int
    progress_total: int
    result: dict | None = None
    error: str | None = None

    class Config:
        from_attributes = True


class SpendSummary(BaseModel):
    today_usd: float
    last_7d_usd: float
    lifetime_usd: float
    by_service: dict[str, float]
