"""Config + credential loading. Single source of truth for both search config and API keys."""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import tomllib  # py311+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


def _project_root() -> Path:
    """Locate project root regardless of whether we're running from source or a PyInstaller .exe."""
    if getattr(sys, "frozen", False):
        # Running as PyInstaller bundle. Config sits next to the .exe.
        return Path(sys.executable).parent
    # Source layout: src/bdpp/config.py -> three .parents up = project root
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = _project_root()
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"

for d in (OUTPUT_DIR, LOGS_DIR, ASSETS_DIR):
    d.mkdir(parents=True, exist_ok=True)


@dataclass
class Credentials:
    google_api_key: str = ""
    google_cse_id: str = ""
    outscraper_token: str = ""
    millionverifier_token: str = ""
    anthropic_api_key: str = ""
    default_max_spend_usd: float = 6.0

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Credentials":
        path = path or (CONFIG_DIR / "credentials.toml")
        if not path.exists():
            raise FileNotFoundError(
                f"Credentials file not found at {path}. "
                f"Copy credentials.toml.template to credentials.toml and fill in your keys."
            )
        with open(path, "rb") as fh:
            data = tomllib.load(fh)
        return cls(
            google_api_key=data.get("google", {}).get("api_key", ""),
            google_cse_id=data.get("google", {}).get("cse_id", ""),
            outscraper_token=data.get("outscraper", {}).get("api_token", ""),
            millionverifier_token=data.get("millionverifier", {}).get("api_token", ""),
            anthropic_api_key=data.get("anthropic", {}).get("api_key", ""),
            default_max_spend_usd=float(data.get("budget", {}).get("default_max_spend_usd", 6.0)),
        )


@dataclass
class FilterConfig:
    exclude_fortune500: bool = True
    max_active_postings: int = 100
    max_office_locations: int = 3
    preferred_max_employees: int = 500


@dataclass
class IntelConfig:
    position_intel: bool = False
    company_intel: bool = False
    contact_intel: bool = False


@dataclass
class SearchConfig:
    industry: str
    job_titles: list[str]
    locations: list[str]
    skills: list[str] = field(default_factory=list)
    filters: FilterConfig = field(default_factory=FilterConfig)
    intel: IntelConfig = field(default_factory=IntelConfig)
    max_spend_usd: float = 6.0
    csv_path: str = "output/bdpp_{timestamp}.csv"
    tag: str = "BD"
    hours_old: int = 72       # Date Posted window (hours). GUI slider: 24/72/168/336/720/2160.
    results_per_query: int = 50

    @classmethod
    def load(cls, path: Path) -> "SearchConfig":
        with open(path, "rb") as fh:
            data = tomllib.load(fh)
        s = data["search"]
        return cls(
            industry=s["industry"],
            job_titles=list(s["job_titles"]),
            locations=list(s["locations"]),
            skills=list(s.get("skills", [])),
            filters=FilterConfig(**data.get("filters", {})),
            intel=IntelConfig(**data.get("intel", {})),
            max_spend_usd=float(data.get("budget", {}).get("max_spend_usd", 6.0)),
            csv_path=data.get("output", {}).get("csv_path", "output/bdpp_{timestamp}.csv"),
            tag=data.get("output", {}).get("tag", "BD"),
            hours_old=int(s.get("hours_old", 72)),
            results_per_query=int(s.get("results_per_query", 50)),
        )
