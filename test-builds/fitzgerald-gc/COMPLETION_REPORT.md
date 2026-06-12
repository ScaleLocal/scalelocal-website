# Completion Report — Fitzgerald General Contracting Demo

**Built:** 2026-06-11 / 12 · **Status:** Live · **By:** ScaleLocal (Cowork)
**Live URL:** https://www.scalelocal.net/test-builds/fitzgerald-gc/

## What was built
A 5-page (+404) static prospect demo for Fitzgerald General Contracting (Billerica, MA),
same scope as the HVAC Pro Beast / Santos and Sons / TNJ builds. A demo Matt can send cold.

- **index.html** — 4-slide hero carousel (real project photos), trust bar, 3-pillar services,
  family/"Fitzy" story, stats, gallery preview, Google rating + sample-review carousel, CTA
- **services.html** — all services on one page (siding, roofing, decks/carpentry, additions/framing,
  gutters/exterior). No subpages.
- **about.html** — second-generation family story (run by "Fitzy"), how-we-work, service area
- **gallery.html** — 14-image grid of real Fitzgerald project photos
- **contact.html** — estimate form (mailto:), phone, hours, service area, embedded Google Map
- **404.html** — light, on-brand

## Style / brand
- **Rugged Irish working-class** rebrand (per Matt's direction): deep Irish green + cream + worn
  gold + brick-red, heavy condensed type (Oswald) + Roboto Condensed body, bold borders and
  drop-shadows, shamrock dividers. Blue-collar, not elegant.
- **Official Fitzgerald logo** (from Matt's `IMG_1126.jpeg` — the truck/GBP brand mark) dropped in
  as-is at `images/logo-fitzgerald.png`. Header background set to white to match the logo's white
  tile. Footer uses the same logo on a white rounded tile with padding.
- **Voice:** moderate "Fitzy" — owner is Fitzy, plain-spoken working-class tone, still lands with
  any homeowner. (Removed the "since the old man started it" line per Matt.)

## Real data used (the "wait, you built this for us?" factor)
- **Real project photos** pulled from Fitzgerald's verified Google Business Profile via the Google
  Places API (10 photos: siding, roofing, decks, additions, a shed, exteriors). Used throughout —
  heroes, service tiles, gallery. No stock photos remain.
- **Official logo** supplied by Matt and used as-is.
- **Verified facts:** owner Eric Fitzgerald (goes by "Fitzy"), phone (978) 408-9390 / 978-408-9390
  (matches the logo), 9 Summit Rd Billerica MA 01821, 5.0★ / 23 Google reviews, A+ BBB, services,
  family/2-generation history. See RESEARCH_NOTES.md for sources.

## Chat widget (placeholder — action needed)
- Per scope, the GHL AIO chat widget is a **labeled HTML comment placeholder** on all 6 pages
  (no Preview Slot assigned yet).
- The **custom four-action launcher** (Urgent text / Chat / Book estimate / Call) is live bottom-right
  on every page. Its "Chat" action falls back to the estimate form until the GHL widget is embedded.
- `GHL_SETUP_FITZGERALD_GC.md` has the full pre-filled setup pack (KB URLs, bot prompt, voice prompt,
  AIO widget config). ~15 min in the GHL UI once Matt confirms the slot.

## Deploy / technical
- Committed to `ScaleLocal/scalelocal-website` → `test-builds/fitzgerald-gc/`; Vercel auto-deploy.
- `vercel.json` updated with case-insensitive + trailing-slash 308 redirects for `/test-builds/
  fitzgerald-gc/` (existing tnj / hvac / santos redirects preserved).
- Verified live: all 6 pages HTTP 200; `css/site.css` = `text/css`; JS = `application/javascript`;
  images 200 with correct types; `/test-builds/fitzgerald-gc` (no slash) and case variants → 308 to
  canonical; mobile (390px) has zero horizontal overflow; hero/review dots no longer collide.
- 1 desktop (1440px) + 1 mobile (390px) screenshot saved in this folder.
- No SEO scaffolding (Phase 1): no schema, sitemap, robots, canonical, or OG beyond title/description.
  Pages carry noindex,nofollow while it's a preview.

## OPEN ITEMS for Matt
1. **Assign the GHL Preview Slot** for Fitzgerald, then I'll set the widget ID, enable the loader in
   `js/site.js`, and push (~30 sec to go live). See GHL_SETUP_FITZGERALD_GC.md.
2. **Confirm with Eric / "Fitzy":**
   - Exact **service-area towns** (demo lists Billerica + Tewksbury, Chelmsford, Wilmington, Burlington,
     Bedford as representative — verify).
   - **Founding year** — NOT stated on the site (BBB says 2003; site/directories imply a ~1975 family
     lineage; they don't reconcile, so the demo says "two generations" / "family-run", no hard date).
   - **License numbers** (MA HIC# / CSL#) — NOT on the site (none verified). The logo itself says
     "Licensed & Insured," which the site echoes. Add numbers once confirmed.
   - **Hours** (demo: Mon–Fri 8a–6p, weekends by appointment — from a directory; confirm).
3. **Reviews:** demo shows the verified 5.0★ / 23-review Google badge + clearly-labeled *sample*
   testimonial cards (no fabricated quotes). Swap in real featured reviews when live.
4. Phase 2 (if Fitzgerald says yes): SEO, more pages, service-detail/town pages, real review embeds.

## Could NOT be verified directly
- fitzgeraldgc.com returns **403 Forbidden** on subpages (server htaccess error) — the existing site
  couldn't be mined beyond its homepage. All detail came from third-party sources + the GBP API.
