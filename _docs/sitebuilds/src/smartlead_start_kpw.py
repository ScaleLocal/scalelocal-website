r"""
ScaleLocal — start the KPW Smartlead campaign
=============================================
Flips campaign 3744204 ("ScaleLocal - KPW_DownersGrove_2026-08") from PAUSED
to START. Reads the API key locally, same as smartlead_create_kpw.py, so the
key never leaves this machine.

Before flipping it prints whatever the campaign's current settings say, so you
can eyeball tracking and schedule one last time without opening the UI.

  Pre-flight only, changes nothing:
    python C:\Users\matty\Documents\Claude\ScaleLocalCode\Workflows\smartlead_start_kpw.py

  Actually start it:
    python C:\Users\matty\Documents\Claude\ScaleLocalCode\Workflows\smartlead_start_kpw.py --start

  Put it back to paused at any time:
    python C:\Users\matty\Documents\Claude\ScaleLocalCode\Workflows\smartlead_start_kpw.py --pause

Author: Cowork
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: the 'requests' package is required. Install with: pip install requests")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
SCALELOCAL_ROOT = SCRIPT_DIR.parent
API_KEYS_PATH = SCALELOCAL_ROOT / "Workflows" / "API_Keys.md"
FALLBACK_KEYS_PATH = Path(r"C:\Users\matty\Documents\Claude\System Files\API_KEYS.md")
CAMPAIGN_MAP_PATH = SCRIPT_DIR / "smartlead_campaign_map.json"

SMARTLEAD_BASE = "https://server.smartlead.ai/api/v1"
CAMPAIGN_KEY = "kpw_cpa"


def load_smartlead_key() -> str | None:
    for path in (API_KEYS_PATH, FALLBACK_KEYS_PATH):
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
            m = re.search(r"##\s*Smartlead.*?\*\*Value:\*\*\s*([^\n]+)", text,
                          re.DOTALL | re.IGNORECASE)
            if m:
                v = m.group(1).strip()
                if v and not v.startswith("["):
                    return v
        except Exception as e:
            print(f"WARN: could not read {path.name} ({e})")
    return os.environ.get("SMARTLEAD_API_KEY", "").strip() or None


def req(method, path, api_key, json_body=None):
    try:
        r = requests.request(method, f"{SMARTLEAD_BASE}{path}",
                             params={"api_key": api_key}, json=json_body, timeout=30)
    except Exception as e:
        print(f"  network error {method} {path}: {e}")
        return None
    if not r.ok:
        print(f"  {r.status_code} on {method} {path}: {r.text[:300]}")
        return None
    try:
        return r.json()
    except ValueError:
        return {}


def campaign_id() -> str | None:
    if not CAMPAIGN_MAP_PATH.exists():
        return None
    try:
        return json.loads(CAMPAIGN_MAP_PATH.read_text(encoding="utf-8")).get(CAMPAIGN_KEY)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--start", action="store_true", help="Set campaign status to START.")
    g.add_argument("--pause", action="store_true", help="Set campaign status back to PAUSED.")
    args = ap.parse_args()

    cid = campaign_id()
    if not cid:
        print(f"ERROR: no '{CAMPAIGN_KEY}' entry in {CAMPAIGN_MAP_PATH.name}. "
              "Run smartlead_create_kpw.py --live first.")
        sys.exit(1)

    api_key = load_smartlead_key()
    if not api_key:
        print("ERROR: no Smartlead API key found.")
        sys.exit(1)

    print("=" * 72)
    print(f"KPW campaign {cid}")
    print("=" * 72)

    info = req("GET", f"/campaigns/{cid}", api_key)
    if isinstance(info, dict) and info:
        d = info.get("data") if isinstance(info.get("data"), dict) else info
        for k in ("name", "status", "track_settings", "stop_lead_settings",
                  "unsubscribe_text", "min_time_btwn_emails", "max_leads_per_day",
                  "send_as_plain_text", "follow_up_percentage"):
            if k in d:
                print(f"  {k}: {d[k]}")
    else:
        print("  (could not read campaign settings — check tracking in the UI)")

    if not (args.start or args.pause):
        print("\nPre-flight only. Nothing changed.")
        print("Re-run with --start to begin sending, or --pause to hold.")
        return

    status = "START" if args.start else "PAUSED"
    print(f"\nsetting status -> {status}")
    if req("POST", f"/campaigns/{cid}/status", api_key, {"status": status}) is None:
        print("FAILED. Status unchanged.")
        sys.exit(1)

    print(f"status is now {status}")
    if args.start:
        print("\nCampaign is LIVE.")
        print("Sending window is Tue/Wed/Thu 09:00-11:00 America/Chicago,")
        print("so the first touch goes out in the next window that opens.")
        print("To stop it at any point:  smartlead_start_kpw.py --pause")
    print("=" * 72)


if __name__ == "__main__":
    main()
