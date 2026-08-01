# Build note — Mill City Accounting Services LLC (bespoke rebuild, 2026-07-31)

Companion to `research/millcityaccounting.md`. That file is what the firm publishes;
this is what was done with it, what was corrected, and what the client must confirm.

## Corrections to the research file

Two things in `research/millcityaccounting.md` were wrong or incomplete. Both were
found by re-verifying the live site during this build, and the research file should
be updated:

1. **There are SEVEN named services, not four.** The file lists tax preparation,
   payroll, bookkeeping and notarization. The homepage also names **New Business
   Consulting** and **Tax Planning**, and the business tax-prep line explicitly
   covers non-profits (Form 990) and fiduciary returns (Form 1041). Both extra
   services now have pages. (Seven *names*, six *pages* — tax preparation is listed
   by the firm under both Business and Personal. The first draft of this build said
   "seven services" above a list of six; the audit caught it.)
2. **"97 Central Street" IS on their live site.** The research file says it does not
   appear. It does — the contact page carries a moved-from notice dated 01/01/2025,
   still up nineteen months later. The guidance was right (never use it as the
   address); the premise was wrong. The rebuild does not carry the notice.

## Architecture

Standalone module `site_millcity.py`. Does not import `build.py`, `design.py`, any
`content_*.py`, `site_hickey.py` or `site_carella.py`. Own stylesheet, own
components, own page architecture. 17 pages.

**Premise: "Open on Kearney Square."** Scott holds no credential, so the site cannot
lean on letters and does not try. It leans instead on what the other firms in this
batch do not publish: a named person, a real address, stated hours, and a phone that
gets answered. His two genuine specialisms — quick-serve restaurants and rental real
estate, both evidenced by his own bio — are the primary navigation axis, ahead of the
service menu.

**Contact widget:** a full-width filled counter strip under the masthead on every
page, carrying call, email, the firm's real Square payment link, and a booking route,
plus a live open/closed state. The state is computed in `America/New_York`, not the
visitor's timezone — a visitor in California was otherwise told the Lowell office was
open when it was shut. With JavaScript off it degrades to "Mon–Fri, 9am–5pm".

## Deliberately NOT claimed

CPA, EA or any credential for Scott; staff, partners or a team; client counts; years
of experience beyond what the bio's dates support; a client portal; online booking; a
contact form; a second location; fee quotes, free consultations, response times or
turnaround times. The only licence claimed anywhere is the notary commission, and it
is attributed to Scott personally, not to the LLC.

## Fixed before publishing, found by the claim audit

- "Seven services" above a list of six, on three pages.
- "Eleven years" at the Cambridge firm — the bio runs summer 2007 to spring 2018,
  which is not eleven years, and four other places on the site said "a decade".
  Standardised on the decade.
- "where he spent his twenties and his thirties" — his age is not known.
- "Nothing is charged for the first call" — an invented fee promise, and a functional
  restatement of a banned claim.
- "the four things that turn a two-week return into a two-month one" — establishes a
  turnaround baseline the firm has never published.
- "Mill City Accounting Services holds a notary commission" — a Massachusetts notary
  commission is issued to a natural person, and the notary page said so correctly, so
  the two pages contradicted each other on the one licence the firm has.
- Two passages disparaging other small accounting offices, in a document being emailed
  cold to one.
- "Massachusetts taxes rental income at the flat 5% rate" with no mention of the 4%
  surtax — stated to the one audience most likely to reach it in a sale year.
- "271 municipalities" softened to "more than 270"; the figure drifts as towns adopt
  the local option.
- "Talk to us" — the only first-person plural on a one-person firm's site. It came
  from the shared `calculators.py` note, now overridden per-site.
- `calculators.py` said the Social Security wage base is "set by the IRS". It is set
  by the Social Security Administration. Corrected at source, so Hickey and Carella
  get the fix too.

## Verified 2026-07-31 against irs.gov, mass.gov and sec.state.ma.us

Restaurant track: Lowell meals tax 7.00% (6.25% state + 0.75% local option, Lowell
confirmed adopting via DLS FY2026 distribution data); monthly ST-MAB-4 with no
threshold; tip reporting at $20/month by the 10th on Form 4070; Form 8027 above 10
employees; IRC 45B credit on Form 8846 with the frozen $5.15 reference; **IRC 224
qualified-tips deduction, $25,000, TY2025–2028, phasing out over $150,000 MAGI
($300,000 joint) — and Massachusetts does NOT conform (DOR TIR 26-4)**; MA minimum
wage $15.00 and service rate $6.75; Tips Act c.149 s.152A; service charges are non-tip
wages; MA UI wage base $15,000 for 2026.

Rental track: Schedule E and the Schedule C boundary; 27.5-year GDS, mid-month, land
not depreciable; $25,000 passive allowance tapering at 50% of MAGI over $100,000 and
gone at $150,000; real estate professional 750-hour and majority tests; BAR framework;
unrecaptured 1250 gain at up to 25%; 1031 real property only, 45/180 days; MA 5% flat
plus the surtax caveat; MA short-term rental excise 5.7% plus local option plus DOR
registration.

General: deposit schedules and the lookback; 941/944; FUTA 6.0% on $7,000 with the
5.4% credit; the 2/5/10/15% late-deposit ladder; Trust Fund Recovery Penalty under
6672; MA new hire reporting within 14 days; 1099-NEC by 31 January; the MA ABC test at
c.149 s.148B; notary commissioned by the Governor for seven years, $1.25 maximum
acknowledgement fee, Chapter 2 of the Acts of 2023 for remote notarisation.

No section 179 dollar limit appears anywhere on the site — it is described in words.

## Verification run

| Gate | Result |
|---|---|
| `BUILD_FIRM=millcityaccounting python3 qa.py` | PASS — 0 fails, 0 warnings, 17 pages |
| `BUILD_FIRM=millcityaccounting python3 gates_bespoke.py` | GATE A–E PASS at 1512 / 1440 / 1100 / 390 |
| `python3 contrast_millcity.py` | 44 pairs, 0 fails (8 failed on the first palette and were fixed, not reclassified) |
| Screenshots reviewed at 1440 and 390 | yes — three defects found visually that no gate caught |
| Claim audit | run adversarially; 15 findings, all resolved or dismissed with reasons |

## For the client to confirm

1. **Every dated figure.** The meals tax rate, the IRC 224 amounts, the MA minimum
   wage and service rate, the MA UI wage base, FUTA figures, the MA short-term rental
   excise and the notary fee are all current as of 31 July 2026 and all will move.
2. **Whether he still takes 990 and 1041 work** — it is on his homepage, and this
   build makes a feature of it.
3. **Whether tax planning and new business consulting are still offered.**
4. **The 97 Central Street notice** on his current contact page is nineteen months
   old and should come down whatever happens with this site.
5. **The logo is a proposal.** An original mark drawn for this pitch; the firm has no
   existing one. Say so before he asks.
6. **`noindex,nofollow`** is on every page and must come off at cutover.
