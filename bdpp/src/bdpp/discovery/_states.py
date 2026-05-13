"""US state name/abbreviation maps used across the discovery layer."""

STATE_NAME_TO_ABBR = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
}
STATE_ABBR_TO_NAME = {v: k.title() for k, v in STATE_NAME_TO_ABBR.items()}


def normalize_state(s: str) -> str | None:
    """Take 'Massachusetts' or 'MA' or 'mass.' and return 'MA' (or None)."""
    if not s:
        return None
    key = s.strip().lower().rstrip(".")
    if len(key) == 2 and key.upper() in STATE_ABBR_TO_NAME:
        return key.upper()
    return STATE_NAME_TO_ABBR.get(key)


def parse_location(loc: str) -> tuple[str | None, str | None]:
    """Parse 'Woburn, MA' or 'Boston, Massachusetts' -> ('Woburn', 'MA')."""
    if not loc:
        return (None, None)
    parts = [p.strip() for p in loc.split(",")]
    if len(parts) >= 2:
        city = parts[0]
        state = normalize_state(parts[1])
        return (city if city else None, state)
    # Single-token location — might be just state, or "Remote", or city only
    abbr = normalize_state(parts[0])
    if abbr:
        return (None, abbr)
    return (parts[0] if parts[0] else None, None)


def location_matches(job_loc: str, target_states: list[str]) -> bool:
    """Return True iff the job's location is in one of the target states."""
    _, state = parse_location(job_loc)
    if state is None:
        return False
    target_abbrs = {normalize_state(s) for s in target_states}
    return state in target_abbrs
