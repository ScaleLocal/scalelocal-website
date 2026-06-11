# Research Notes — Fitzgerald General Contracting (Billerica, MA)

**Compiled:** 2026-06-11 · **For:** 5-page prospect demo build
**Build target:** https://www.scalelocal.net/test-builds/fitzgerald-gc/

> ⚠️ **Why this file matters:** The live site (fitzgeraldgc.com) returns **403 Forbidden** on
> every subpage (server reports "unable to read htaccess file, denying access to be safe").
> The homepage still served plain text via headless fetch, but Services / About / Gallery /
> Testimonials are all inaccessible. So most detail below is mined from **third-party sources**.
> Everything is tagged **[VERIFIED]**, **[REPORTED]** (single third-party, treat with care), or
> **[UNVERIFIED / DO NOT STATE AS FACT]**. The demo uses conservative language wherever a fact
> could not be confirmed from a reliable source.

---

## 1. Core business facts

| Field | Value | Confidence | Source |
|---|---|---|---|
| Business name | **Fitzgerald General Contracting** | [VERIFIED] | Live homepage, Google, FB, Yelp, BBB |
| BBB legal name | "Fitzgerald Construction" | [VERIFIED] | BBB profile |
| Owner / principal | **Eric Fitzgerald** (Owner / President / Principal) | [VERIFIED] | ScaleLocal enrichment (eric@fitzgeraldgc.com), BBB ("Mr. Eric Fitzgerald, Principal") |
| Family structure | "owned and operated by two brothers"; homepage says "owners" (plural); 2nd-generation family business | [REPORTED] | Search snippets + homepage copy |
| Address | **9 Summit Rd, Billerica, MA 01821** (BBB: 01821-6302) | [VERIFIED] | Google, BBB, eHardhat |
| Phone | **(978) 408-9390** | [VERIFIED] | Homepage, Google, BBB, ScaleLocal enrichment |
| Email | **eric@fitzgeraldgc.com** | [VERIFIED] | ScaleLocal enrichment, business domain |
| Website | fitzgeraldgc.com (currently **403 / broken**) | [VERIFIED] | Direct fetch + Chrome (403) |
| Google rating | **5.0 stars, 21 reviews** | [VERIFIED] | ScaleLocal GBP enrichment 2026-04 (gbp_verified: true) — **clears the 4.5★ display bar** |
| Google place_id | ChIJqQhTt9OVCwsRtSNET_G6o6o | [VERIFIED] | ScaleLocal enrichment |
| Google CID (for map) | 12295876953231336373 | [VERIFIED] | ScaleLocal enrichment google_maps_url |
| BBB rating | **A+** (NOT BBB-accredited) | [VERIFIED] | BBB profile |
| Residential? | YES | [VERIFIED] | eHardhat, homepage |
| Commercial? | YES | [VERIFIED] | eHardhat, homepage ("residential or commercial") |
| Emergency service? | YES | [REPORTED] | eHardhat structured field |
| Financing? | NO | [REPORTED] | eHardhat |
| Credit cards? | NO | [REPORTED] | eHardhat |
| Employees (BBB record) | 1 | [REPORTED] | BBB (likely undercounts crew) |

## 2. Hours

eHardhat (call to confirm): **Mon–Fri 8:00am–6:00pm, Sat & Sun Closed.**  [REPORTED]
→ Demo uses "Mon–Fri 8a–6p · Weekends by appointment" softened, with a "call to confirm" implied
by the estimate CTA. Matt to confirm exact hours with Eric.

## 3. Founding year — ⚠️ CONFLICT, DO NOT PUT A HARD DATE ON SITE

- Homepage copyright reads "Copyright 2012."
- Homepage + several directories: "2nd generation, family owned … **since 1975**" / "45+ years."
- **BBB: Business Started 1/1/2003; "Years in Business: 23"; BBB file opened 2003.**

These don't reconcile cleanly. Most likely: the **family's** contracting lineage goes back decades
(father's business, ~1975), while **this legal entity** (Eric's) was established ~2003. Because we
cannot confirm a single founding year, the demo says **"second-generation, family-owned"** and
**"decades of experience"** — NO specific founding year, NO "since 1975," NO "since 2003."
**Matt: confirm the real story with Eric and we'll add the exact year.**

## 4. Services offered  [VERIFIED — homepage + corroborated across directories]

Confirmed mix (general contractor, residential + commercial):
- **Siding** — red cedar, clapboard, Hardie Plank, "siding of any type" (a clear core specialty;
  the lead Google discovery query that surfaced them was literally "siding contractor")
- **Roofing** — new roofs, reroofs, roof repair, skylights
- **Carpentry & decks** — decks, porches, french doors, light carpentry
- **Additions** — home/room additions, residential & commercial
- **Framing** — steel or wood framing, new construction and additions, residential & commercial
- **Windows** — window installation/replacement
- **Exterior trim/finish** — seamless gutters, chimney repairs, capping & flashing

Positioning words straight from the homepage: "experts in installing siding of any type… as well
as light carpentry including decks, french doors, additions." "On schedule and within budget."
"Owners personally meet with all clients and are present working and overseeing each job site."
"Fully insured." "2nd generation, family owned … outstanding reputation for quality and
professionalism." "We take pride in our work and are constantly striving for excellence."

## 5. Service area  [INFERRED — verify with Eric]

No explicit town list published. Billerica home base; the ScaleLocal discovery query was
"siding contractor in **Tewksbury** MA," implying they work the surrounding Middlesex County towns.
Demo uses a conservative, true-by-default phrasing: **"Billerica and surrounding Greater Lowell /
Middlesex County communities"** and names nearby towns (Billerica, Tewksbury, Chelmsford,
Wilmington, Burlington, Bedford, North Billerica) as *representative* of the area served, not as a
hard guarantee. **Matt: confirm the real service-area town list.**

## 6. Reviews  [VERIFIED aggregate; individual quotes NOT verbatim-confirmed]

- **Google: 5.0★ across 21 reviews** — verified, displayable (>4.5★ rule satisfied).
- Search surfaced paraphrased review sentiment (NOT exact quotes — search engine summaries):
  - Siding job: "looks great, high quality work"; "the owner was on the job and was easy to work with."
  - "Jamie P.": "very professional and do amazing work… HIGHLY RECOMMENDED."
- ⚠️ Could not retrieve **verbatim** review text with reviewer names (Yelp/FB/Google review bodies
  are behind JS + login; Chrome reads were blocked this session).
- **Decision (legal hard line):** the demo does **NOT** print these as real testimonials. It shows
  the verified **5.0★ / 21-review** Google badge, plus clearly-labeled **"Sample testimonial ·
  preview content"** cards (same pattern as the TNJ build) with a visible note that Eric's real
  Google reviews drop in once the site is live. No fabricated quotes, no invented names.

## 7. Brand colors  [UNVERIFIED — could not access FB banner / Yelp / truck wraps this session]

The live homepage is plain unstyled text (no usable brand palette), and FB/Yelp imagery was not
retrievable. **No confirmed brand hex codes.** The demo uses a classic, contractor-appropriate
palette that reads as trustworthy and "built to last" and is safe to re-skin once Eric's real
colors are known:
- Ink / charcoal: `#14202B` (near-black navy)
- Primary "Fitzgerald green": `#2F6B3C` (forest green — common, credible GC color; easily swapped)
- Warm accent: `#C9A24B` (brass/gold)
- Stone neutrals: `#F6F4EF`, `#ECE7DA`, `#D9D2BE`
**Matt: if Eric has brand colors (truck wraps, logo, FB banner), send them and we recolor in ~10 min.**

## 8. Photos  [GAP — none retrievable; see COMPLETION_REPORT open items]

- Site Gallery page: **403 Forbidden.**
- Google Business Profile: **gbp_photo_count = 0** (no business-uploaded photos on Google).
- Facebook photo albums + Yelp photos: behind JS/login; Chrome reads blocked this session.
- **Result:** the demo ships with high-quality, neutral, contractor-appropriate **stock imagery as
  clearly-labeled temporary placeholders.** Every image slot is documented in COMPLETION_REPORT.md
  so Eric's real project photos can be dropped in 1-for-1. **This is the #1 thing to swap before the
  site goes from "demo" to "live."**

## 9. Licenses / certifications  [NOT INCLUDED — none verified]

No MA HIC# or CSL# was verifiable from any reliable source this session. **Per the legal hard line,
NO license numbers appear on the demo.** BBB lists the MA Office of Public Safety & Inspections as a
resource but does not publish a license number. The site says only what's verified: "fully insured"
(stated on their own homepage) and "A+ rated by the BBB" (verified on BBB). Matt: collect Eric's MA
HIC / CSL numbers and we'll add them.

## 10. Things flagged / ambiguous

- A **separate** Yelp listing "FITZGERALD ERIC T — CLOSED" exists. This is an old/duplicate listing.
  The active "Fitzgerald General Contracting" GC + roofing Yelp listings, the 5.0★/21 Google reviews,
  and the A+ BBB profile all indicate the business is **operating**. The demo treats it as active.
  (If Eric has in fact wound down, stop — but all current signals say open.)
- "Two brothers" vs "Eric, owner" — demo uses "the Fitzgerald family" / "owner-operated" to stay
  accurate without over-claiming a specific second person's name.

## Sources
- Live homepage (text only): https://fitzgeraldgc.com/
- BBB profile: https://www.bbb.org/us/ma/billerica/profile/construction-management/fitzgerald-construction-0021-86449
- eHardhat directory: https://www.ehardhat.com/directory/additions-and-remodels/MA/billerica/eric-fitzgerald-general-contracting/1622031
- Facebook: https://www.facebook.com/p/Fitzgerald-General-Contracting-100054647280737/  (not readable this session)
- Yelp (GC): https://www.yelp.com/biz/fitzgerald-general-contracting-billerica  (not readable this session)
- Google Maps (CID): https://maps.google.com/?cid=12295876953231336373
- ScaleLocal first-party enrichment: Prospects/pipeline_v2_discovery_2026-04-21.csv, TUESDAY_ENROLLMENT.csv, Reporting/Audits/place_ChIJqQhTt9OVCwsRtSNET_G6o6o.json
