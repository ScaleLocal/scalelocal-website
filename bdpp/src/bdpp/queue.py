"""BD++ persistent Enrichment Queue.

A SQLite-backed queue that survives between runs of the .exe. Three operations:

  enqueue_search_results(qualified, search_meta)  -> adds rows with status=DISCOVERED
  enrich_next(budget, max_companies)              -> processes DISCOVERED rows, marks ENRICHED
  export_enriched(filter=...)                     -> writes CSV from ENRICHED rows, marks EXPORTED

Status transitions:
    DISCOVERED  --enrich-->  ENRICHED  --export-->  EXPORTED  --user_action-->  DELETED

User can also Delete or Skip from any state.
"""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Iterator

from .config import PROJECT_ROOT
from .models import JobPosting, CompanyProfile, Contact


import os
# Queue DB lives outside the OneDrive folder (sync would corrupt SQLite).
# Windows: %LOCALAPPDATA%\BDPlusPlus\queue.db   POSIX: ~/.bdplusplus/queue.db
def _queue_db_path():
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "BDPlusPlus"
    else:
        base = Path.home() / ".bdplusplus"
    base.mkdir(parents=True, exist_ok=True)
    return base / "queue.db"

QUEUE_DB_PATH = _queue_db_path()


SCHEMA = """
CREATE TABLE IF NOT EXISTS queue_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL,                    -- DISCOVERED | ENRICHED | EXPORTED | DELETED
    discovered_at TEXT NOT NULL,
    enriched_at TEXT,
    exported_at TEXT,
    search_tag TEXT,
    search_industry TEXT,
    -- Company
    company_name TEXT NOT NULL,
    company_domain TEXT,
    company_website TEXT,
    company_intel TEXT,
    employee_band TEXT,
    -- Job posting (BD job)
    bd_job_title TEXT,
    bd_job_location TEXT,
    bd_job_city TEXT,
    bd_job_state TEXT,
    bd_job_url TEXT,
    bd_job_source TEXT,
    bd_job_description TEXT,
    bd_job_reports_to TEXT,
    -- Contacts (JSON)
    hiring_manager_json TEXT,
    hr_contact_json TEXT,
    -- Position intel
    skill_1 TEXT, skill_2 TEXT, skill_3 TEXT,
    -- Dedup key
    dedup_key TEXT UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_status ON queue_items(status);
CREATE INDEX IF NOT EXISTS idx_company ON queue_items(company_name);
CREATE INDEX IF NOT EXISTS idx_dedup ON queue_items(dedup_key);
"""


@contextmanager
def _conn():
    conn = sqlite3.connect(QUEUE_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def _dedup_key(company_name, job_title, job_location):
    return f"{(company_name or '').strip().lower()}|{(job_title or '').strip().lower()}|{(job_location or '').strip().lower()}"


def enqueue_search_results(qualified, search_meta):
    """Insert each (posting, profile) into the queue with status=DISCOVERED. Idempotent via dedup_key."""
    added = 0
    skipped = 0
    now = datetime.now().isoformat(timespec="seconds")
    with _conn() as conn:
        for posting, profile in qualified:
            key = _dedup_key(profile.name, posting.job_title, posting.job_location)
            try:
                conn.execute("""
                    INSERT INTO queue_items
                    (status, discovered_at, search_tag, search_industry,
                     company_name, company_domain, company_website, company_intel,
                     bd_job_title, bd_job_location, bd_job_city, bd_job_state, bd_job_url,
                     bd_job_source, bd_job_description, bd_job_reports_to, dedup_key)
                    VALUES ('DISCOVERED', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (now, search_meta.get("tag"), search_meta.get("industry"),
                      profile.name, profile.domain, profile.website, profile.company_intel,
                      posting.job_title, posting.job_location, posting.job_city, posting.job_state,
                      posting.job_url, posting.source, (posting.description or "")[:8000],
                      posting.reports_to_raw, key))
                added += 1
            except sqlite3.IntegrityError:
                # already in queue
                skipped += 1
    return {"added": added, "skipped_duplicates": skipped}


def list_queue(status=None, limit=200):
    """Return rows in the queue, optionally filtered by status."""
    with _conn() as conn:
        if status:
            rows = conn.execute("SELECT * FROM queue_items WHERE status = ? ORDER BY id DESC LIMIT ?",
                                (status, limit)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM queue_items WHERE status != 'DELETED' ORDER BY id DESC LIMIT ?",
                                (limit,)).fetchall()
    return [dict(r) for r in rows]


def queue_counts():
    with _conn() as conn:
        rows = conn.execute("SELECT status, COUNT(*) AS n FROM queue_items GROUP BY status").fetchall()
    return {r["status"]: r["n"] for r in rows}


def pop_for_enrichment(limit):
    """Return up to `limit` DISCOVERED rows, ordered by oldest first."""
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM queue_items WHERE status='DISCOVERED' ORDER BY id ASC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def mark_enriched(item_id, hiring_manager=None, hr_contact=None, skills=None):
    now = datetime.now().isoformat(timespec="seconds")
    with _conn() as conn:
        conn.execute("""
            UPDATE queue_items SET status='ENRICHED', enriched_at=?,
              hiring_manager_json=?, hr_contact_json=?,
              skill_1=?, skill_2=?, skill_3=?
            WHERE id=?
        """, (
            now,
            json.dumps(asdict(hiring_manager)) if hiring_manager else None,
            json.dumps(asdict(hr_contact)) if hr_contact else None,
            (skills or ["", "", ""])[0] if skills else "",
            (skills or ["", "", ""])[1] if skills and len(skills)>1 else "",
            (skills or ["", "", ""])[2] if skills and len(skills)>2 else "",
            item_id,
        ))


def mark_exported(item_ids):
    if not item_ids:
        return
    now = datetime.now().isoformat(timespec="seconds")
    with _conn() as conn:
        for iid in item_ids:
            conn.execute("UPDATE queue_items SET status='EXPORTED', exported_at=? WHERE id=?", (now, iid))


def delete_items(item_ids):
    if not item_ids:
        return
    with _conn() as conn:
        for iid in item_ids:
            conn.execute("UPDATE queue_items SET status='DELETED' WHERE id=?", (iid,))


def clear_all():
    """Nuke the queue (admin use)."""
    with _conn() as conn:
        conn.execute("DELETE FROM queue_items")


def reset_status(item_ids, new_status):
    """Move items back to a previous state, e.g. ENRICHED -> DISCOVERED to re-enrich."""
    with _conn() as conn:
        for iid in item_ids:
            conn.execute("UPDATE queue_items SET status=? WHERE id=?", (new_status, iid))
