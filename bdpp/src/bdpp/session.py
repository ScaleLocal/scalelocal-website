"""BD++ Session — persists pipeline state between the Search / Enrichment / Output buttons.

GUI workflow:
  1. User clicks SEARCH  -> stage_search() runs discovery + qualify, populates session.qualified[]
                            Display in GUI: list of companies + roles found
  2. User clicks ENRICH  -> stage_enrich() runs contact resolution + email verification
                            Updates session.enriched[]
                            Display in GUI: contacts found, emails verified
  3. User clicks OUTPUT  -> stage_output() applies Intel toggles + writes CSV
                            Display in GUI: download link / file path
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .budget import BudgetTracker
from .config import OUTPUT_DIR, LOGS_DIR
from .models import CompanyProfile, JobPosting


@dataclass
class BDSession:
    """Holds state across the three pipeline stages so they can be invoked separately."""
    search_config: Optional[Any] = None       # SearchConfig
    creds: Optional[Any] = None               # Credentials
    budget: Optional[BudgetTracker] = None

    # Stage outputs
    raw_postings: list[JobPosting] = field(default_factory=list)
    qualified: list[tuple[JobPosting, CompanyProfile]] = field(default_factory=list)
    enriched: list[dict] = field(default_factory=list)
    rows: list[Any] = field(default_factory=list)
    csv_path: Optional[Path] = None
    apollo_csv_path: Optional[Path] = None

    # Stage timing/status
    last_search_at: Optional[str] = None
    last_enrich_at: Optional[str] = None
    last_output_at: Optional[str] = None

    def snapshot_summary(self) -> dict:
        return {
            "discovered": len(self.raw_postings),
            "qualified": len(self.qualified),
            "enriched": len(self.enriched),
            "rows": len(self.rows),
            "budget": self.budget.summary() if self.budget else {},
            "csv_path": str(self.csv_path) if self.csv_path else None,
            "apollo_csv_path": str(self.apollo_csv_path) if self.apollo_csv_path else None,
            "last_search_at": self.last_search_at,
            "last_enrich_at": self.last_enrich_at,
            "last_output_at": self.last_output_at,
        }
