# Build note — Charles M. Carella, CPA (bespoke rebuild, 2026-07-31)

Companion to `research/carellacpa.md`. That file is what the firm publishes; this is
what was done with it, what was deliberately left out, and what the client must confirm.

## Architecture

Standalone module `site_carella.py`. Does not import `build.py`, `design.py`, any
`content_*.py`, or `site_hickey.py`. Own stylesheet, own components, own page
architecture. 26 pages.

The organising decision: this firm publishes nothing about itself, so the site is
organised around the client's situation rather than the firm's story. Six situation
pages are the primary entry point; the four services sit behind them. That is what
justifies the standing left rail — a vertical nav carries seven top-level entries plus
nested children, which a horizontal masthead cannot.

## Deliberately NOT claimed

Founding year, entity suffix, any named individual, staff count, office hours,
memberships, specialisms, credentials beyond "CPA", client portal, online payments,
online booking, fee quotes before work begins, turnaround or response times.

Audited clean: zero occurrences of `we`, `our`, `team`, `staff`, `colleague`,
`associate` or `partners` in visible text or metadata; zero `<form>` elements; zero
rating, review or `openingHours` markup; all 47 `BANNED` strings absent.

## Copy removed from the previous build

- **"a partner will follow up directly"** (closing CTA, every page). The firm names
  nobody and there is no evidence of partners. This was an invented fact on a demo
  addressed to the firm itself.
- **"you will get a straight answer about what the work involves"** (10 pages). An
  outcome promise on the firm's behalf. Reworded to an invitation.
- **"it rarely takes longer than ten minutes" / "ten minutes normally settles"**.
  Assertions about how this office conducts intake. Softened to describe the question,
  not the firm's practice.
- **"including the fact that you called"** (confidentiality). The professional rule
  attaches to clients; a prospective caller who never engages is a harder case.
- **"annual professional education requirements"**. Massachusetts CPE is 80 hours per
  two-year cycle, not annual.
- **"sixteen variations on a mortgage"**. Accurate about their current vendor set, but
  it is a jab at the site the recipient owns, inside a cold pitch to that recipient.

## Tax facts verified 2026-07-31 against irs.gov and mass.gov

Dated figures are stated with their year in the text. Everything else is phrased
durably so it does not go stale.

| Claim | Status |
|---|---|
| MA flat 5%; short-term capital gains at a higher separate rate | verified (STCG 8.5%) |
| MA 4% surtax above a threshold "a little over one million dollars, adjusted annually" | verified; figure deliberately not stated ($1,107,750 for 2026) |
| No MA standard deduction; Form 1 / Form 1-NR/PY | verified |
| MA disallows bonus depreciation; **deferred conformity to the OBBBA §179 limits for TY2025 and TY2026** | verified — TIR 26-4, issued 2026-06-23 |
| MA extension automatic only if 80% of total tax paid; void otherwise | verified |
| MA minimum corporate excise $456 (2025) | verified |
| Failure to file 5%/month vs failure to pay 0.5%/month, both capped at 25% | verified — "ten times", consistent on all four pages |
| Safe harbour 100% / 110% above $150,000 AGI ($75,000 MFS) | verified |
| Federal extension to 15 October, no extension to pay | verified |
| SE tax 15.3%, 92.35% factor, half deductible, wage base **$184,500 for 2026** | verified — corrected from the 2025 figure |
| Assessment 3 years / 6 years where gross income omitted **exceeds 25% of that stated** / unlimited if unfiled | verified, statutory wording |
| Partnership & S corp late filing **$255 per owner per month, max 12 months** (returns filed in 2026) | verified; rises to $260 for 2027 |
| Entity due dates, with "moves to the next business day" caveat | verified — 15 March 2026 is a Sunday |
| E-file signature before transmission; preparer must sign and furnish a copy | verified — Pub 1345 (administrative), IRC §6695(b) and §6107(a) |

No §179 dollar limit, no surtax threshold figure and no minimum-penalty dollar figure
appear anywhere on the site — all three are stated in words instead, so they cannot go
stale.

## Shared-file change

`calculators.py` line 198: Social Security wage base default 176100 → 184500. The
$176,100 was the 2025 figure and was live on Hickey and Mass Tax Pros as well as here.
This is the only shared file touched, and it is a data correction, not layout.

## Verification run

| Gate | Result |
|---|---|
| `BUILD_FIRM=carellacpa python3 qa.py` | PASS — 0 fails, 0 warnings, 26 pages |
| `python3 contrast_carella.py` | 33 pairs, 0 fails |
| `python3 layout_carella.py` | GATE A PASS; GATE B/C/D PASS at 1440 / 1100 / 390 |
| Screenshots reviewed at 1440 and 390 | yes — four defects found visually that no gate caught |
| Claim audit | run adversarially against the research file; six defects, all fixed |

Note on the shipped gates: `contrast.py` and `layout_audit.py` are hardcoded to the
template engine's class names and colour pairs (`.wrap`, hero gradients, the gold chat
pill). Run against a bespoke build they measure nothing and report PASS. The two
`*_carella.py` scripts are the same gates re-pointed at what this site actually uses,
plus a check that the sticky rail fits the viewport, that the fixed mobile bar does not
cover content, and that a table wider than the column sits in a scroll wrapper. Any
future bespoke build needs the same treatment — a green light from the shipped versions
is not evidence.

## For the client to confirm

1. **Office hours.** Not published anywhere. The site says only "Call or email to
   arrange a time". Real hours would improve the contact and situation pages.
2. **Document intake.** Their current site directs clients to print a PDF organiser and
   fax or mail it. The rebuild does not present fax as a feature; it says to ask on the
   call. If they want a secure upload route, that is a decision for cutover.
3. **Representation.** The site states that a CPA holds unlimited representation rights
   and that whether representation forms part of an engagement is to be agreed. Confirm
   they take representation work.
4. **Assurance.** The financial statements pages describe all four service levels and
   the independence constraint, without claiming this office performs reviews or audits.
   Confirm which levels they actually offer.
5. **The logo is a proposal.** An original mark designed for this pitch. The firm has
   no existing mark. Say so before they ask.
6. **`noindex,nofollow`** is on every page and must come off at cutover.
