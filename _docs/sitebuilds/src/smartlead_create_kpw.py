r"""
ScaleLocal — Smartlead campaign creator: KPW (Kolnicki, Peterson & Wirth)
========================================================================
One-off sibling of smartlead_create_campaigns.py for the KPW spec-build pitch.
Same conventions: dry-run by default, leaves the campaign PAUSED, never
activates unless --activate is passed explicitly.

What it does, in order:
  1. POST /campaigns/create                    -> "ScaleLocal - KPW_DownersGrove_2026-08"
  2. POST /campaigns/{id}/sequences            -> 4 touches, delays [0, 5, 7, 28]
  3. GET  /email-accounts + POST .../email-accounts (optional inbox linking)
  4. POST /campaigns/{id}/schedule             -> Tue/Wed/Thu 09:00-11:00 America/Chicago
  5. POST /campaigns/{id}/leads                -> the 7 KPW addresses
  6. Leaves status PAUSED. Writes the id into smartlead_campaign_map.json.

HARD GATE — POSTAL ADDRESS
  Commercial email needs a valid postal address. The script REFUSES to run
  live until one is supplied, either with --address or by editing
  POSTAL_ADDRESS below. Use a USPS-registered PO box or a CMRA street address.
  Do not use a home address, yours or anyone else's.

EXACT WINDOWS RUN COMMANDS
  Dry run (no API calls at all — prints exactly what it would send):
    python C:\Users\matty\Documents\Claude\ScaleLocalCode\Workflows\smartlead_create_kpw.py --dry-run

  Create for real, leave PAUSED (this is the one you want):
    python C:\Users\matty\Documents\Claude\ScaleLocalCode\Workflows\smartlead_create_kpw.py --live

  Link specific inboxes only:
    ... --live --address "..." --inbox-ids 101,102

Author: Cowork
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: the 'requests' package is required. Install with: pip install requests")
    sys.exit(1)

# ============================================================================
# PATHS / CONSTANTS
# ============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
SCALELOCAL_ROOT = SCRIPT_DIR.parent
API_KEYS_PATH = SCALELOCAL_ROOT / "Workflows" / "API_Keys.md"
FALLBACK_KEYS_PATH = Path(r"C:\Users\matty\Documents\Claude\System Files\API_KEYS.md")
CAMPAIGN_MAP_PATH = SCRIPT_DIR / "smartlead_campaign_map.json"

SMARTLEAD_BASE = "https://server.smartlead.ai/api/v1"

CAMPAIGN_KEY = "kpw_cpa"
CAMPAIGN_NAME = "ScaleLocal - KPW_DownersGrove_2026-08"

DEMO_URL = "https://www.scalelocal.net/test-builds/kpw-cpa/"

# CMRA / private mailbox (Abington MA). Company name only, no personal name.
POSTAL_ADDRESS = "1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351"

OPT_OUT_LINE = 'Reply "stop" and I\'ll take you off my list the same day.'

# Tue/Wed/Thu, 9-11am, KPW's timezone (Downers Grove IL) — not ours.
SCHEDULE = {
    "timezone": "America/Chicago",
    "days_of_the_week": [2, 3, 4],
    "start_hour": "09:00",
    "end_hour": "11:00",
    "min_time_btw_emails": 15,      # 7 near-identical mails at one domain: spread them
    "max_new_leads_per_day": 7,
    "schedule_start_time": None,
}

CADENCE_DELAYS = [0, 5, 7, 28]

LEADS = [
    {"email": "KKolnicki@kpwcpa.com", "first_name": "Kenneth",  "last_name": "Kolnicki"},
    {"email": "KPeterson@kpwcpa.com", "first_name": "Kenneth",  "last_name": "Peterson"},
    {"email": "RWirth@kpwcpa.com",    "first_name": "Richard",  "last_name": "Wirth"},
    {"email": "MEckel@kpwcpa.com",    "first_name": "Michael",  "last_name": "Eckel"},
    {"email": "GByers@kpwcpa.com",    "first_name": "Glenn",    "last_name": "Byers"},
    {"email": "MKolnicki@kpwcpa.com", "first_name": "Michael",  "last_name": "Kolnicki"},
    # No personal name on the shared inbox — the greeting is written to absorb this.
    {"email": "info@kpwcpa.com", "first_name": "Whoever handles the website", "last_name": ""},
]
for _l in LEADS:
    _l["company_name"] = "Kolnicki, Peterson & Wirth, LLC"


# ============================================================================
# SEQUENCE COPY
# ============================================================================
TOUCHES = [
    {
        "touch": 1,
        "subject": "I built something for Kolnicki, Peterson & Wirth",
        "body": """{{first_name}} —

Before anything else: I sent this same message to every partner at KPW and to the main office inbox. From the outside I couldn't tell who owns a decision like this, and I'd rather say that plainly than guess wrong.

Your website needed a refresh. I already built it.

""" + DEMO_URL + """

Click around before you read the rest of this. It's the whole firm — every service, every partner, the Downers Grove office with a live map, and a set of plain-English guides on what clients actually call to ask.

What you're looking at:

- 100% designed from scratch by ScaleLocal — thirty-four pages, nothing templated, written from your own published material
- Call, email, and appointment-request tools built into every page
- SEO backend built for Google indexing — structured data, clean markup, an interactive Google map on the location and contact pages
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

That price is low because the work is already finished. There's no discovery phase to bill you for, no revision cycle, no project manager. You're buying a completed site, not a project.

Reply and I'll walk you through it. If it isn't for you, I'll send two more notes at most and then leave you alone.

— Matt | ScaleLocal""",
    },
    {
        "touch": 2,
        "subject": "The Chicago page",
        "body": """{{first_name}} —

Following up on the site I sent last week, but this part stands on its own and costs you nothing to act on.

kpwcpachicago.com is still up and still selling an office you don't have. The contact page lists 954 W Washington Blvd, Suite 320, with 312.421.5780 as a live number. Anyone who lands there calls a number that doesn't reach you or drives to a suite that isn't yours.

Three more things on that domain, in case nobody's looked at it lately:

The Downers Grove listing on that same page routes to Chicago@kpwcpa.com — the office you still have is pointing its email at the one you closed.

The site won't load over https at all. The secure address resets the connection, so every visitor gets it over http and every modern browser marks the firm "Not secure" in the address bar. For a practice handling client financials, that's the wrong first impression.

And the footer still reads 2015.

Google is meanwhile reading that domain as a second location for the firm, which splits your local signal away from the office you actually have.

The build I sent you has none of that — one office, one address, one phone number, one set of hours, and a map embedded where Google weights it.

""" + DEMO_URL + """

Still $997, still nothing monthly. But fix the old domain either way.

— Matt | ScaleLocal""",
    },
    {
        "touch": 3,
        "subject": "Last one from me",
        "body": """{{first_name}} —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm not going to invent a deadline for it.

""" + DEMO_URL + """

$997, once. I deploy it to whatever domain you want and hand it over. After that you owe me nothing and you never hear from me again unless you want to.

Fifty-two years is a long time to be the firm people in DuPage County call first. Your site should say that. Right now it doesn't.

— Matt | ScaleLocal""",
    },
    {
        "touch": 4,
        "subject": "Still have the KPW site on file",
        "body": """{{first_name}} —

A few weeks back I sent over a website I'd built for the firm. You didn't take it up, which is fine.

Extension season is about to land on you. If the Chicago domain or the current site ever becomes a real annoyance, the build is still on file, still $997, and I can have it live on your domain in a day.

Say the word and I'll clear the file instead. Either way, this is the last you'll hear from me.

— Matt | ScaleLocal""",
    },
]


# ============================================================================
# API KEY LOADING (mirrors smartlead_create_campaigns.load_smartlead_key)
# ============================================================================
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
            print(f"WARN: could not read {path.name} ({e}); trying next source.")
    env_key = os.environ.get("SMARTLEAD_API_KEY", "").strip()
    return env_key or None


# ============================================================================
# HTTP
# ============================================================================
def smartlead_request(method: str, path: str, api_key: str,
                      json_body: dict | None = None, retries: int = 4):
    url = f"{SMARTLEAD_BASE}{path}"
    for attempt in range(retries):
        try:
            r = requests.request(method, url, params={"api_key": api_key},
                                 json=json_body, timeout=30)
        except Exception as e:
            print(f"  network error on {method} {path}: {e}")
            time.sleep(2 ** attempt)
            continue
        if r.status_code in (429, 500, 502, 503, 504):
            wait = 2 ** attempt
            print(f"  {r.status_code} on {method} {path} — retrying in {wait}s")
            time.sleep(wait)
            continue
        if not r.ok:
            print(f"  ERROR {r.status_code} on {method} {path}: {r.text[:400]}")
            return None
        try:
            return r.json()
        except ValueError:
            return {}
    print(f"  giving up on {method} {path} after {retries} attempts")
    return None


# ============================================================================
# BUILD
# ============================================================================
def normalize_address(addr: str) -> str:
    """Ensure the footer reads 'ScaleLocal, <address>' exactly once."""
    addr = addr.strip().lstrip(",").strip()
    if addr.lower().startswith("scalelocal"):
        addr = addr[len("scalelocal"):].lstrip(",").strip()
    return f"ScaleLocal, {addr}"


def build_sequence(postal_address: str) -> list[dict]:
    """Smartlead renders email_body as HTML, so newlines must become <br>."""
    footer = f"\n\n{normalize_address(postal_address)}\n{OPT_OUT_LINE}"
    seq = []
    for i, t in enumerate(TOUCHES):
        body = t["body"] + footer
        seq.append({
            "seq_number": t["touch"],
            "seq_delay_details": {"delay_in_days": CADENCE_DELAYS[i]},
            "subject": t["subject"],
            "email_body": body.replace("\n", "<br>\n"),
        })
    return seq


def write_campaign_map(campaign_id: str):
    data = {}
    if CAMPAIGN_MAP_PATH.exists():
        try:
            data = json.loads(CAMPAIGN_MAP_PATH.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data[CAMPAIGN_KEY] = str(campaign_id)
    CAMPAIGN_MAP_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"  campaign map updated: {CAMPAIGN_KEY} -> {campaign_id}")


# ============================================================================
# MAIN
# ============================================================================
def main():
    ap = argparse.ArgumentParser(description="Create the KPW Smartlead campaign (paused).")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True,
                      help="Default. Print what would be sent; make no API calls.")
    mode.add_argument("--live", action="store_true", help="Actually create the campaign.")
    ap.add_argument("--address", default="", help="Postal address for the CAN-SPAM footer.")
    ap.add_argument("--inbox-ids", default="", help="Comma-separated inbox ids. Omit to link all.")
    ap.add_argument("--activate", action="store_true",
                    help="Start the campaign immediately. Almost never what you want.")
    args = ap.parse_args()

    dry = not args.live
    address = (args.address or POSTAL_ADDRESS).strip()

    print("=" * 72)
    print(f"KPW Smartlead campaign  [{'DRY RUN' if dry else 'LIVE'}]")
    print("=" * 72)

    if not address:
        print("\nREFUSING TO RUN: no postal address supplied.")
        print("Commercial email needs a valid postal address and a working opt-out.")
        print("Use a USPS-registered PO box or a CMRA street address — not a home address.")
        print('Then re-run with:  --live --address "ScaleLocal, <street>, <city> <state> <zip>"')
        sys.exit(1)

    api_key = load_smartlead_key()
    if not api_key and not dry:
        print("\nERROR: no Smartlead API key found.")
        print(f"Looked in: {API_KEYS_PATH}, {FALLBACK_KEYS_PATH}, then $SMARTLEAD_API_KEY.")
        sys.exit(1)
    if api_key:
        print(f"api key: loaded ({len(api_key)} chars, not printed)")

    sequence = build_sequence(address)
    print(f"footer:  {normalize_address(address)}")
    print(f"touches: {len(sequence)}  delays={CADENCE_DELAYS}")
    print(f"leads:   {len(LEADS)}  (all @kpwcpa.com)")
    print(f"window:  {SCHEDULE['start_hour']}-{SCHEDULE['end_hour']} "
          f"{SCHEDULE['timezone']}, days={SCHEDULE['days_of_the_week']}\n")

    if dry:
        for s in sequence:
            print(f"  [DRY] touch {s['seq_number']} "
                  f"(+{s['seq_delay_details']['delay_in_days']}d): {s['subject']}")
        print("\n  [DRY] POST /campaigns/create")
        print("  [DRY] POST /campaigns/{id}/sequences")
        print("  [DRY] POST /campaigns/{id}/schedule")
        print("  [DRY] POST /campaigns/{id}/leads")
        print("  [DRY] campaign would be left PAUSED")
        print("\nDry run only. Nothing was sent. Re-run with --live when ready.")
        return

    # 1. campaign
    data = smartlead_request("POST", "/campaigns/create", api_key,
                             json_body={"name": CAMPAIGN_NAME})
    if not data:
        sys.exit(1)
    cid = data.get("id") or data.get("campaign_id") or (data.get("data") or {}).get("id")
    if not cid:
        print(f"ERROR: campaign created but no id in response: {data}")
        sys.exit(1)
    cid = str(cid)
    print(f"  created '{CAMPAIGN_NAME}' -> id={cid}")

    # 2. sequence
    if smartlead_request("POST", f"/campaigns/{cid}/sequences", api_key,
                         json_body={"sequences": sequence}) is not None:
        print(f"  sequence set ({len(sequence)} touches)")

    # 3. inboxes
    if args.inbox_ids:
        ids = [int(x) for x in args.inbox_ids.split(",") if x.strip()]
    else:
        accounts = smartlead_request("GET", "/email-accounts", api_key) or []
        accounts = accounts if isinstance(accounts, list) else accounts.get("data", [])
        ids = [a.get("id") for a in accounts if a.get("id") is not None]
    if ids:
        if smartlead_request("POST", f"/campaigns/{cid}/email-accounts", api_key,
                             json_body={"email_account_ids": ids}) is not None:
            print(f"  linked {len(ids)} inbox(es)")
    else:
        print("  (no inboxes linked — do this in the UI before starting)")

    # 4. schedule
    if smartlead_request("POST", f"/campaigns/{cid}/schedule", api_key,
                         json_body=SCHEDULE) is not None:
        print(f"  schedule set ({SCHEDULE['start_hour']}-{SCHEDULE['end_hour']} "
              f"{SCHEDULE['timezone']})")

    # 5. leads
    if smartlead_request("POST", f"/campaigns/{cid}/leads", api_key,
                         json_body={"lead_list": LEADS}) is not None:
        print(f"  uploaded {len(LEADS)} leads")

    # 6. status
    status = "START" if args.activate else "PAUSED"
    if smartlead_request("POST", f"/campaigns/{cid}/status", api_key,
                         json_body={"status": status}) is not None:
        print(f"  status -> {status}")

    write_campaign_map(cid)

    print("\n" + "=" * 72)
    if args.activate:
        print("CAMPAIGN IS LIVE. First send goes out in the next scheduled window.")
    else:
        print("Campaign created and PAUSED. Nothing has been sent.")
        print("Before you press start in the Smartlead UI:")
        print("  - confirm link tracking and open tracking are OFF")
        print("  - confirm reply-stop behaviour; if it is per-lead rather than")
        print("    per-domain, watch the inbox and pause by hand on first reply")
        print("  - re-verify the four kpwcpachicago.com claims in touch 2")
    print("=" * 72)


if __name__ == "__main__":
    main()
