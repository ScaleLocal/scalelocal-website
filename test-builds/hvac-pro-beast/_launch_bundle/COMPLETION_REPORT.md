# HVAC Pro Beast — Demo Build Completion Report
**Date:** 2026-06-10 | **Live URL:** https://www.scalelocal.net/test-builds/hvac-pro-beast/
**Repo commits:** bc11db7 (21-page v1), follow-up (5-page trim + OG/icons + launch bundle)

## What shipped (5-page demo, per Matt's 2026-06-10 direction)
- index.html — 4-slide hero carousel (real GBP photos), trust bar (License RT-173575 / Family-Owned / 20+ Years / 24-7), three-pillar grid (Refrigeration / HVAC / Service), about split w/ Tom's real photo, stats band, 4 verbatim Google reviews + 5.0 rating banner, real-photo gallery strip, why-us grid, 7-town service-area cards, CTA band
- services.html — all 7 service sections w/ anchor quick-links (refrigeration, ice machines, walk-ins, HVAC, mini-splits, exhaust fans, maintenance + 24/7) + FAQPage schema
- reviews.html — 5 verbatim GBP review quotes w/ first names, rating verified 2026-06-10
- about.html — owner story (verified facts only) + full real-photo gallery (#work)
- contact.html — estimate form (demo alert), 3 contact methods, Google Map embed, 24/7 hours
- 404.html, sitemap.xml (5 URLs), robots.txt (disallow — preview)
- Branded OG/social card (FB + LinkedIn preview) on every page; favicon set (SVG + 32/16 PNG + apple-touch-icon)
- Custom 4-action launcher (Urgent text / Chat / Book estimate / Call) bottom-right, TNJ pattern
- GHL AIO widget: labeled HTML placeholder comment on all 6 HTML files (NOT embedded — awaiting Matt's slot decision + clone)
- vercel.json: 308 no-slash redirect + case-variant rewrites/redirects (TNJ pattern)
- Schema: HVACBusiness + AggregateRating 5.0/11 (verified at build time), Service schema per area of services page, FAQPage

## QA checklist results (all verified against the LIVE deploy 2026-06-10)
| Check | Result |
|---|---|
| All pages HTTP 200 | PASS (5 pages + 404 + sitemap + robots) |
| css/site.css content-type text/css | PASS |
| JS files application/javascript | PASS |
| Images 200 + image content-types | PASS (spot: hero, og, apple-touch-icon, favicon.svg) |
| No emojis anywhere | PASS (automated scan, all HTML+JS) |
| No fabricated reviews/testimonials | PASS — only verbatim GBP quotes w/ real first names |
| Aggregate rating only if verified 4.5+ | PASS — 5.0/11 verified via Places API 2026-06-10 |
| Schema validates | PASS (all JSON-LD blocks parse; spot-checked structure) |
| Widget launcher renders + opens | PASS (renders bottom-right; chat falls back to estimate form until widget cloned) |
| Chat widget placeholder is labeled comment | PASS (all 6 HTML files) |
| Mobile 390px clean | PASS — scrollWidth 390 = viewport (no horizontal scroll), nav collapses, CTAs stack |
| /test-builds/hvac-pro-beast no-slash | PASS — 308 to canonical slash |
| /Test-Builds/HVAC-Pro-Beast/ case variant | PASS — rewrites to canonical (200) |
| Phone/area/owner consistent on every page | PASS — single source generator; (781) 350-8141 everywhere |
| Screenshots | 2 desktop (1440) + 2 mobile (390) in _launch_bundle/screenshots/ |
| Internal links resolve | PASS (automated check) |
| BOOT v2.8 claim-source ledger | PASS — see RESEARCH_NOTES.md (every claim traced to FB/GBP/banner/card) |

## Image sourcing (BOOT v2.8 #4)
All 13 site photos are HVAC Pro Beast's own GBP uploads (attribution verified "HVAC PRO BEAST" via Places API). Zero stock, zero AI-generated photos, no watermarks. Tom's photo on About = his own published GBP/FB profile photo. OG card composed from brand colors + their own rooftop photo.

## Open items for Matt
1. **Slot decision** — Slot 2 (next open) vs dedicated sub-account (newer High Line/Opus/Exeter pattern). GHL_SETUP doc is written for Slot 2; IDs swap cleanly if you choose otherwise.
2. **Clone + train widget** — ~15 min via GHL_SETUP_HVAC_PRO_BEAST.md, then give Cowork the widget ID to replace placeholders.
3. **Yeti mascot file** — pasted in chat but never landed as a file. Save the PNG into the Claude folder and Cowork will add it to header/hero/widget avatar in a follow-up commit.
4. **Superior Sealcoat misroute** — unrelated to this build: superior-sealcoat pages open Opus Plumbing's assistant (Slot 1 widget was repurposed). Needs a fix.
5. **BOOT.md truncation** — BOOT.md ends mid-sentence at line 569 (RESPONSE PRIORITY MATRIX). Restore from backup.
6. **Owner surname** — "Tom Pejic" inferred from email only; site says "Tom" everywhere. Confirm spelling before any Phase-2 domain/about expansion.
7. **21-page version** — preserved in git history (commit bc11db7): 7 service detail pages + 7 town pages + gallery/reviews pages, ready to roll out if Tom upgrades.
8. **Public bundle note** — per TNJ precedent this _launch_bundle (research notes, GHL setup) deploys with the site; it is unlinked, noindexed, and robots-disallowed, but technically fetchable at the URL. Say the word and I'll strip it from the deploy.

## Definition-of-done check
Every photo is theirs (GBP uploads). Every service is from their own banner/card (ice machines, walk-ins, exhaust fans, heat+AC, mini-splits, 24/7). Every town is from Matt's confirmed list. Voice matches the shop: direct, confident, family-owned, "beast" energy without the emojis. Cold-send ready pending widget embed.

## v2 addendum — Beast branding pass (2026-06-10, same session)
Per Matt's direction after first ship:
- **Beast mascot vectorized in-house** (original PNG never survived chat upload; recreation explicitly authorized). Hand-built SVG matching their first-party art: blue yeti, white beard, orange HVAC BEAST cap, red/blue refrigerant gauges, YETI-branded condenser. 4 design iterations (fierce eyes, connected grin, gauge z-order). Strict-XML validated (first deploy hit an unbalanced tag that broke <img> rendering — fixed).
- **Stacked logo lockup** (beast above HVAC PRO BEAST / FAST · RELIABLE · LOCAL) in header + footer, per Matt's mock.
- Beast placements: hero (above trust bar), all inner-page sub-heroes, CTA bands, 404, OG card, favicon set (16/32/180/512 from beast head), beast-head-512.png ready as chat-widget avatar.
- **Rating badge redesigned**: white card, 5.0 in display italic + five SVG stars + "Google rating · 11 reviews · verified June 2026".
- **Full 5-page audit @1440+390**: fixed services-page mobile horizontal overflow (quick-link grid now responsive); zero broken images; zero horizontal scroll on all 10 page/viewport combos; all content-types correct.
- Note: rebased over a concurrent LawnWize test-build push to main during deploy.
- Remaining nice-to-have: swap vector beast for the original raster art if Matt drops the PNG into the Claude folder (file-drop, not chat paste).
