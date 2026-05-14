"""CSV export — exact BD++ column spec."""
from __future__ import annotations
import csv
import io


BD_COLUMNS = [
    "Company", "First Name", "Last Name", "Job Title", "Email", "Phone",
    "City", "State", "BD Job Title", "BD Job Location",
    "Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5",
    "Tag", "Industry",
    "Job URL", "Contact Source", "Email Status", "Contact Intel",
]


def queue_items_to_csv_bytes(items, *, tag, industry, intel_position=False, intel_company=False, intel_contact=False, only_with_contact=False):
    """Convert a list of QueueItem ORM rows into CSV bytes."""
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(BD_COLUMNS)

    for it in items:
        # Skip rows without contacts when filtering
        if only_with_contact and not (it.hiring_manager or it.hr_contact):
            continue
        hiring = it.hiring_manager or None
        hr = it.hr_contact or None
        skills = list(it.skills or [])

        # Pad to 5 skills
        cols = (skills + ["", "", "", "", ""])[:5]
        if intel_company and it.company_intel:
            cols[3] = it.company_intel

        def _emit(contact, default_title):
            if contact is None:
                contact = {}
            w.writerow([
                it.company_name,
                contact.get("first_name", ""),
                contact.get("last_name", ""),
                contact.get("title") or default_title,
                contact.get("email") or "",
                "",  # phone
                it.bd_job_city or "",
                it.bd_job_state or "",
                it.bd_job_title,
                it.bd_job_location or "",
                cols[0], cols[1], cols[2], cols[3], cols[4],
                tag, industry,
                it.bd_job_url or "",
                contact.get("source", "") if contact else "(needs manual lookup)",
                contact.get("email_verification_status", "") if contact else "",
                (it.contact_intel or "") if intel_contact else "",
            ])

        if hiring or hr:
            if hiring:
                _emit(hiring, "Hiring Manager")
            if hr:
                _emit(hr, "HR Contact")
        else:
            _emit(None, "(no contact found)")

    return buf.getvalue().encode("utf-8")
