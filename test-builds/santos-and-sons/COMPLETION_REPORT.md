# COMPLETION REPORT — Santos & Sons 5-Page Demo
**Date:** 2026-06-10 · **Live URL:** https://www.scalelocal.net/test-builds/santos-and-sons/
**Repo:** ScaleLocal/scalelocal-website → `test-builds/santos-and-sons/` (commits `51e3b17`, `75c555a`, `37f60c7`)

## What was built
5-page prospect demo per spec: `index` (4-slide hero carousel of real FB project photos, trust bar, 3-pillar services, about preview w/ their yard-sign crest photo, gallery preview, 3 real review quotes, CTA band), `services` (all on one page: installation by fence type, repair/replacement, hardscape, dumpster service), `about` (Derek Santos story — BBB/FB-verified facts only), `gallery` (8 real photos, click-to-enlarge), `contact` (placeholder estimate form, call/text/email/hours, embedded Google Map of their actual GBP listing), plus on-brand `404`.

Custom four-action launcher (Urgent text Derek / Chat / Book estimate / Call) bottom-right on every page — TNJ pattern, `santos`-prefixed, with the GHL shadow-DOM bubble-hide + `openWidget()` handoff pre-wired. Chat falls back to the estimate form until the widget is embedded.

Brand: hunter green + antique gold sampled from their crest sign; Playfair Display + Inter (Highline editorial pattern); inline SVG nav/trust icons (no emoji, no Font Awesome); typographic shield-crest logo lockup in header/footer.

## QA results (all verified live, 2026-06-10)
| Check | Result |
|---|---|
| 6 pages return HTTP 200 | PASS |
| `css/site.css` → `text/css` (not 404 fallback) | PASS |
| `js/site.js`, `js/launcher.js` → `application/javascript` | PASS |
| All 17 images + 2 SVGs → 200, correct content-type | PASS |
| No schema / sitemap / robots.txt / canonical / OG / structured data | PASS (grep-verified; pages carry `noindex,nofollow` only) |
| Widget placeholder comment (exact spec text) on all 6 pages | PASS |
| Four-action launcher renders bottom-right, opens on click | PASS (screenshot: `screenshots/desktop-launcher-open.png`) |
| Hero carousel cycles + overlay headline swaps per slide | PASS (slide-2 state captured in screenshots) |
| Logo renders header + footer | PASS |
| No SVG color-block placeholders; every photo is theirs | PASS |
| Mobile 390px: no horizontal scroll, nav collapses to fullscreen overlay, CTAs stack | PASS (post-fix; see below) |
| `/test-builds/santos-and-sons` (no slash) → 308 → canonical | PASS |
| `/Test-Builds/Santos-And-Sons/`, `/TEST-BUILDS/SANTOS-AND-SONS/`, `/test-builds/Santos-And-Sons` etc. → 308 → canonical | PASS (deep case-variant paths rewrite-serve 200) |
| Phone (978) 888-4638 / owner Derek / service-area phrasing consistent on every page | PASS |
| No emoji anywhere | PASS |
| No fabricated testimonials | PASS — 3 quotes, all real + attributed (Caroline R. / Finnegan D. / Meg M., sources in RESEARCH_NOTES §2) |
| Star rating ≥4.5 verified today | PASS — 5.0★/80 (Birdeye) + 5.0★/57 (Chamber) + FB 100%/62 + BBB A+, verified 2026-06-10 |
| Browser console errors | None |
| Screenshots saved to build folder | `screenshots/desktop-1440.png`, `screenshots/mobile-390.png` (+ launcher-open, nav-open) |
| `git ls-tree` file count after commit | 31 files; `css/` and `js/` confirmed in tree (TNJ failure mode checked) |

## Bugs found & fixed during QA
1. **Mobile nav overlay trapped in header** — `backdrop-filter` on the sticky header made it the containing block for the fixed-position menu. Fixed: `backdrop-filter: none` on mobile (`75c555a`).
2. **site.css tail truncated at write time** — last ~6 rules of the 480px block were cut, breaking small-mobile footer/topbar/launcher rules. Restored (`37f60c7`).
3. **Oversized phone icon in hero CTA on mobile** — `.btn svg` had no size constraint. Fixed (`75c555a`).

## Open items for Matt
1. **Preview Slot** — confirm which slot Santos & Sons gets, then run `GHL_SETUP_SANTOS_AND_SONS.md` (~15 min: bot prompt, KB crawl of the 5 URLs, voice prompt, clone Slot 1 AIO widget `69d9496fc41f60a7fa93719d`). Tell Cowork the new widget ID → placeholder comment gets swapped on all 6 pages.
2. **GBP eyeball check** — I could not load the Google listing directly this session (browser was busy); 5.0★ basis is Birdeye (Google-synced) + Chamber. Glance at the live GBP before sending the demo to confirm rating/name/hours match.
3. **Towns** — site says "Dracut & the surrounding Merrimack Valley" (only Dracut is verifiable). Get Derek's real town list for Phase 2 copy + town pages.
4. **Gallery depth** — 8 full-res photos shipped (spec target 12–20). Photo capture was cut short on request; identified-but-not-captured on their FB: June-4 black aluminum pool fence post, retaining-wall/pool-surround set, truck+trailer cover photo, dumpster/teardown shots. ~10 min to backfill on the next pass.
5. **Perf (Phase 2)** — hero-1.jpg is 456KB; fine for a demo, compress on rebuild. Fonts via Google CDN.
6. **Form** — static placeholder by design; wire to GHL in Phase 2.

## Definition-of-done check
Every photo is theirs (FB-mined, full-res). Every service is from their own yard sign + FB category. The only named town is the one they're registered in. Colors are sampled from their crest. Voice matches their plain, proud, family-run posts. Widget placeholder is labeled and swap-ready. Demo is cold-send ready pending the GBP eyeball check above.

## Revision — 2026-06-10 (afternoon)
Matt's feedback: homepage read fence-only and undersold a multi-million-dollar, multi-truck operation; overlay text needed more pop.
- Hero slide 1 now leads with their own tagline ("Big Or Small, We Do It All") naming all four service lines; remaining slides reframed around whole-property capability.
- Added a persistent four-chip service strip inside the hero (Fencing / Hardscapes / Dumpster Rental / Property Maintenance), visible on every slide, desktop + mobile, each chip deep-linking to its services section (new #maintenance anchor added).
- Homepage pillar grid expanded 3 → 4 to mirror the four service lines.
- Overlay legibility: dual-gradient scrim (left vignette + bottom fade) + stronger text shadows on hero headline/copy.
- Copy elevated from "small crew" to "family-run, fully equipped" — own crews/fleet/equipment, residential + commercial — per Matt's direction (qualitative only; no headcount/revenue/truck-count claims). Index title/description, footer, services lead, about page updated to name all four lines.
- GHL setup pack bot/voice knowledge updated to match the scale framing.
Commits: `41f7747` (reposition) + this revision. Screenshots in `screenshots/` refreshed.

## Revision — 2026-06-11 (brand pass + image-caption audit fix)
Matt flagged that 3 of 4 homepage service cards used fence photos as stand-ins, and requested branded link previews (FB/Twitter/iOS) + the real crest as the site logo.
- **Image-caption audit resolved:** Hardscapes card/section now uses a real finished paver patio; Property Maintenance card + about page use their crested "Property Maintenance Division" trailer; Dumpster Rental card is icon-led (honest — still no dumpster photo); Fencing keeps the true gate photo. Source: GBP photos mirrored on Wheree (full URLs in RESEARCH_NOTES §8).
- **Gallery 8 → 13 photos**, all captions subject-accurate (3 hardscape, fleet trailer, vinyl run added).
- **Link previews:** og:title/description/image + twitter:card on all 6 pages; og-image.jpg is a 1200×630 sign-style card (SANTOS & SONS · Property Maintenance · 5.0 stars · Local & Family-Run · Dracut, MA · Fencing/Hardscapes/Cleanouts/Dumpster Rentals · tagline + phone). iOS: apple-touch-icon 180px; favicons 32/16 from the real crest.
- **Logo:** real crest (from trailer wrap photo) in header + footer; placeholder SVG retired. Crest v2 upgrade pending Matt's clean sign-art file.
- **Services page:** maintenance section now lists trailer-verified offerings (mowing, cleanups, tree service, snow plowing, landscape design).
- Open: real dumpster photo + GBP review quotes still blocked on browser permissions (sticky deny on facebook.com network reads); fbid list + method documented for a 10-min finish.
Commit: `3d1b628`.
