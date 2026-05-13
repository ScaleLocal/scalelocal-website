"""Budget tracker — hard caps API spend across the run.

Every API client passes its estimated cost through .charge(). When .remaining() drops below 10%
of the cap, .can_afford() starts returning False for non-critical operations so the pipeline
gracefully stops new enrichment and writes what it has.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import LOGS_DIR


@dataclass
class BudgetEntry:
    timestamp: str
    service: str
    detail: str
    cost_usd: float


class BudgetTracker:
    def __init__(self, cap_usd: float):
        self.cap_usd = float(cap_usd)
        self.spent_usd = 0.0
        self.entries: list[BudgetEntry] = []
        self._lock = threading.Lock()
        self._log_path = LOGS_DIR / f"budget_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(self._log_path, "w", encoding="utf-8") as fh:
            fh.write("timestamp,service,detail,cost_usd,running_total_usd\n")

    def charge(self, service: str, detail: str, cost_usd: float) -> None:
        with self._lock:
            self.spent_usd += cost_usd
            entry = BudgetEntry(
                timestamp=datetime.now().isoformat(timespec="seconds"),
                service=service,
                detail=detail,
                cost_usd=cost_usd,
            )
            self.entries.append(entry)
            with open(self._log_path, "a", encoding="utf-8") as fh:
                # CSV-quote detail to be safe
                safe_detail = '"' + detail.replace('"', "''") + '"'
                fh.write(f"{entry.timestamp},{service},{safe_detail},{cost_usd:.5f},{self.spent_usd:.5f}\n")

    def remaining(self) -> float:
        return max(0.0, self.cap_usd - self.spent_usd)

    def percent_used(self) -> float:
        return 0.0 if self.cap_usd == 0 else (self.spent_usd / self.cap_usd)

    def can_afford(self, cost_usd: float, *, critical: bool = False) -> bool:
        """Return True if the operation fits within the cap.

        Non-critical operations are blocked once we hit 90% of the cap to leave headroom
        for the final output. Critical ops (e.g. cheap verification of an already-paid-for contact)
        are allowed up to 100%.
        """
        ceiling = self.cap_usd if critical else self.cap_usd * 0.90
        return (self.spent_usd + cost_usd) <= ceiling

    def summary(self) -> dict:
        by_service: dict[str, float] = {}
        for e in self.entries:
            by_service[e.service] = by_service.get(e.service, 0.0) + e.cost_usd
        return {
            "cap_usd": self.cap_usd,
            "spent_usd": round(self.spent_usd, 4),
            "remaining_usd": round(self.remaining(), 4),
            "percent_used": round(self.percent_used() * 100, 1),
            "by_service": {k: round(v, 4) for k, v in by_service.items()},
            "log_path": str(self._log_path),
        }
