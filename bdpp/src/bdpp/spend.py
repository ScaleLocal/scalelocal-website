"""Daily spend tracker — persisted across runs. Stored next to the queue DB."""
from __future__ import annotations
import json
import os
from datetime import date
from pathlib import Path


def _spend_path():
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "BDPlusPlus"
    else:
        base = Path.home() / ".bdplusplus"
    base.mkdir(parents=True, exist_ok=True)
    return base / "spend.json"


def get_today_spend() -> float:
    p = _spend_path()
    if not p.exists():
        return 0.0
    try:
        data = json.loads(p.read_text())
        today = date.today().isoformat()
        return float(data.get(today, 0.0))
    except Exception:
        return 0.0


def get_all_spend() -> dict:
    p = _spend_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def add_spend(amount: float):
    p = _spend_path()
    data = get_all_spend()
    today = date.today().isoformat()
    data[today] = round(data.get(today, 0.0) + amount, 4)
    p.write_text(json.dumps(data, indent=2))


def get_summary() -> dict:
    """Return total spend today + last 7 days + lifetime."""
    data = get_all_spend()
    today = date.today().isoformat()
    today_amt = data.get(today, 0.0)
    from datetime import datetime, timedelta
    cutoff_7 = (date.today() - timedelta(days=7)).isoformat()
    last7 = sum(v for k, v in data.items() if k >= cutoff_7)
    lifetime = sum(data.values())
    return {
        "today_usd": round(today_amt, 4),
        "last_7_days_usd": round(last7, 4),
        "lifetime_usd": round(lifetime, 4),
        "today_iso": today,
    }
