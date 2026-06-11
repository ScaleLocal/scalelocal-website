# Fitzgerald General Contracting — Prospect Demo Build

A 5-page static demo site built for **Fitzgerald General Contracting** (Billerica, MA) as a cold
prospect demo. Same scope and approach as the HVAC Pro Beast, Santos and Sons, and TNJ builds.

**Live test URL:** https://www.scalelocal.net/test-builds/fitzgerald-gc/

## What this is
A polished, send-it-cold demo Matt can show Fitzgerald to land the deal — built from real research
(their services, their reviews, their town, their voice) so it reads as "you built this for us
already." Every service shown is one they actually offer; every fact is sourced or conservatively
worded (see `RESEARCH_NOTES.md`).

## Pages
- `index.html` — hero carousel (4 slides) + trust bar, 3-pillar services, about preview, stats,
  gallery preview, reviews (verified rating + clearly-labeled sample cards), CTA
- `services.html` — all services on one page (siding, roofing, decks/carpentry, additions/framing,
  gutters/exterior). No subpages.
- `about.html` — second-generation family story, how-we-work, service area
- `gallery.html` — 14-image project grid
- `contact.html` — estimate request form (mailto:), phone, hours, service area, embedded Google Map
- `404.html` — light, on-brand

## Intentionally OMITTED (Phase 1 scope — added in Phase 2 if Fitzgerald says yes)
This is a **Phase 1 demo**. The following are deliberately **not** included and come later:
- **No SEO scaffolding** — no schema/structured data, no `sitemap.xml`, no `robots.txt`, no canonical
  tags, no OG tags beyond basic title/description. (Pages carry `noindex,nofollow` so the demo
  doesn't get crawled while it's a preview.)
- **No service-detail subpages, no town pages, no blog.**
- **No live chat widget yet** — the GHL AIO chat widget is a **labeled HTML comment placeholder** on
  every page until Matt assigns a Preview Slot. See `GHL_SETUP_FITZGERALD_GC.md`.
- The custom four-action launcher (Urgent text / Chat / Book estimate / Call) **is** live; its "Chat"
  action falls back to the estimate form until the GHL widget is embedded.

## Tech
- Static HTML/CSS/JS. No build step, no framework.
- `css/site.css` — editorial GC theme (charcoal-navy + forest green + brass). Brand colors are
  **placeholders** — swap the `--fitz-*` tokens to match Fitzgerald's real brand once known.
- `js/site.js` — hero carousel, mobile nav, reviews carousel, launcher injection, GHL loader (ready
  but disabled until a slot exists).
- `js/launcher.js` — four-action launcher behavior + chat handoff/fallback.
- Inline SVG (Lucide-style) nav + UI icons. No emoji, no icon fonts, no raster icons.
- Mobile-responsive at 1024 / 720 / 480 breakpoints.

## ⚠️ Before this goes from demo to live (top items)
1. **Real photos** — every image is a clearly-labeled stock placeholder. Swap in Fitzgerald's own
   project photos (Facebook/Yelp galleries) 1-for-1. This is the #1 swap. See `COMPLETION_REPORT.md`.
2. **Brand colors** — confirm from Eric's logo / truck wraps and re-skin (~10 min).
3. **Confirm details** — founding year (do NOT state one yet — see research notes), exact service-area
   towns, hours, and any MA HIC#/CSL# license numbers (omitted until verified).
4. **Assign GHL slot + embed the chat widget.**

See `RESEARCH_NOTES.md` for sources and what couldn't be verified, and `COMPLETION_REPORT.md` for the
full open-items list.
