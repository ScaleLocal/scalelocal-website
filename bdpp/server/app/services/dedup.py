"""Dedup-key helper — must match between server and worker."""
def make_dedup_key(company_name, job_title, job_location):
    return f"{(company_name or '').strip().lower()}|{(job_title or '').strip().lower()}|{(job_location or '').strip().lower()}"
