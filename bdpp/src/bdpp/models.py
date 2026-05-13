"""Data models that flow between pipeline stages."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class JobPosting:
    """A single live job post that matched the search criteria."""
    source: str                # 'greenhouse' | 'lever' | 'indeed' | 'google_jobs' | 'company_site'
    source_id: str             # ATS-provided unique id, used for dedup
    company_name: str
    company_domain: Optional[str] = None   # canonical domain, e.g. "boydcorp.com"
    job_title: str = ""        # title exactly as posted
    job_location: str = ""     # "Woburn, MA" — exactly as posted
    job_city: Optional[str] = None
    job_state: Optional[str] = None
    job_url: str = ""
    description: str = ""      # raw HTML or plain text
    reports_to_raw: Optional[str] = None   # extracted "Reports to: ..." text if present
    discovered_at: Optional[str] = None


@dataclass
class CompanyProfile:
    """Aggregated info per unique company across multiple postings."""
    name: str
    domain: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    employee_band: Optional[str] = None    # "1-10" | "11-50" | "51-200" | "201-500" | "501-1000" | etc.
    employee_estimate_high: Optional[int] = None  # upper bound, used for filtering
    headquarters_city: Optional[str] = None
    headquarters_state: Optional[str] = None
    industry: Optional[str] = None
    is_fortune500: bool = False
    active_postings_count: int = 0
    location_count: Optional[int] = None
    company_intel: Optional[str] = None    # one-line descriptor (if Company Intel toggle is on)
    qualification_status: str = "unknown"   # 'pass' | 'fail' | 'unknown'
    qualification_reason: str = ""


@dataclass
class Contact:
    """A named person at a company, with role-based classification."""
    first_name: str
    last_name: str
    title: str
    role_class: str = "OTHER"   # 'HIRING_MANAGER' | 'HR' | 'OTHER'
    email: Optional[str] = None
    email_verification_status: Optional[str] = None  # 'deliverable' | 'catch-all' | 'undeliverable' | 'unknown'
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: str = ""           # 'job_post' | 'outscraper_contacts' | 'website_team_page' | 'pattern_guess' | ...
    confidence: float = 0.0     # 0.0-1.0
    contact_intel: Optional[str] = None  # if Contact Intel toggle is on


@dataclass
class EnrichedRow:
    """The final row(s) produced for each qualifying (job, contact) pair."""
    company: str
    first_name: str
    last_name: str
    job_title: str           # the contact's role at the company (Engineering Manager, HR Manager, ...)
    email: str
    phone: str
    city: str
    state: str
    bd_job_title: str        # exact job title as posted
    bd_job_location: str     # exact location as posted
    skill_1: str = ""
    skill_2: str = ""
    skill_3: str = ""
    skill_4: str = ""        # Company Intel injects here when enabled
    skill_5: str = ""
    tag: str = ""
    industry: str = ""
    # Extra columns for spot-checking; can be hidden at write time
    job_url: str = ""
    contact_source: str = ""
    email_verification_status: str = ""
    contact_intel: str = ""   # exposed as additional column for the "since you..." injection
