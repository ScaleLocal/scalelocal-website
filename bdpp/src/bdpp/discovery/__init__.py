"""Discovery layer — finds live job postings across multiple sources, deduplicated."""
from .orchestrator import discover_jobs, dedup_one_per_company

__all