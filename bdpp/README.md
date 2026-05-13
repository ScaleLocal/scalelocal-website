# BD++ — Business Development Prospecting Engine

A search-to-CSV pipeline that finds companies hiring for a target role, identifies the hiring manager and HR contact, verifies their email, and exports a sales-ready CSV.

**Built for:** Matt @ ScaleLocal — for a separate full-time-job business-development use case.
**Status:** Engine first, GUI second, .exe last.

---

## What it does

Given **Industry + Location(s) + Job Title(s)** (and optionally skill keywords), BD++:

1. **Discovers** open job postings across Greenhouse, Lever, Google Jobs, and Indeed for the target titles in the target geographies.
2. **Qualifies** each company against three hard size filters (Fortune 500 blacklist, >100 active postings, >3 office locations) plus a soft-size signal.
3. **Identifies** the engineering hiring manager and the HR/recruiter at the matching location.
4. **Verifies** each contact's email via pattern-guess + MillionVerifier.
5. **(Optional)** Generates Position Intel (top 3 skills), Company Intel (one-line descriptor), and Contact Intel (a "since you..." personalization).
6. **Exports** to a CSV in the exact spec:
   `Company, First Name, Last Name, Job Title, Email, Phone, City, State, BD Job Title, BD Job Location, Skill 1, Skill 2, Skill 3, Skill 4, Skill 5, Tag, Industry`

Two rows per qualifying job: one for the hiring manager, one for the HR contact (when both are found).

---

## Folder layout

```
BDPlusPlus/
├── src/bdpp/                  # Python source
│   ├── discovery/             # Stage 1: find live job posts
│   ├── qualify/               # Stage 2: size + industry filter
│   ├── contacts/              # Stage 3: name hiring manager + HR
│   ├── verify/                # Stage 4: email pattern + MillionVerifier
│   ├── intel/                 # Stage 5: 3 intel toggles
│   ├── output/                # CSV writer
│   └── gui/                   # PySide6 BD++ desktop app
├── config/
│   ├── credentials.toml       # API keys (NEVER commit)
│   ├── search.example.toml    # Sample search config
│   └── fortune500.txt         # Bundled blacklist
├── output/                    # Generated CSVs
├── logs/                      # Per-run trace logs
├── build/                     # PyInstaller artifacts
├── build.bat                  # Windows one-click .exe build
├── requirements.txt
└── README.md
```

---

## Running on Windows

```cmd
cd C:\Users\matty\OneDrive\ScaleLocal\BDPlusPlus
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m bdpp --config config\search.example.toml
```

To produce the .exe:

```cmd
build.bat
```

The .exe lands at `build\BDPlusPlus.exe` and is fully standalone (~80 MB, includes Python interpreter). Share it with your team along with the bundled `config/credentials.toml.template` — they fill in their own keys.

---

## Budget controls

Every run has a hard `max_spend_usd` set in the search config (default $6). The pipeline tracks:

- Outscraper credits ($0.001-$0.04/call depending on endpoint)
- MillionVerifier verifications ($0.003/check, capped at 4 per contact)
- Google API calls ($0.017/Places call when used)

When 90% of the budget is consumed, no new enrichment work starts — the pipeline writes whatever it has and exits cleanly.

---

## What BD++ does NOT do (yet)

- It will not bypass LinkedIn's bot detection. If a future version needs LinkedIn Sales Navigator, that's a separate Chrome-MCP-driven module.
- It does not push to a CRM. The CSV is the deliverable. (A future module could push to GHL or HubSpot using the existing ScaleLocal patterns.)
- It does not run scheduled. The .exe is on-demand only.
