# Santos & Sons — 5-Page Prospect Demo

**Live:** https://www.scalelocal.net/test-builds/santos-and-sons/
**Status:** Net-new prospect demo (no existing site — Facebook + GBP only)
**Built:** 2026-06-10 by Cowork for Matt @ ScaleLocal

## What this is
A 5-page demo (index, services, about, gallery, contact + 404) Matt can send cold to Santos & Sons. Every photo is from their Facebook page, every service is one they advertise on their own yard sign, brand colors are sampled from their crest, and the copy is tuned to their plain, family-run voice. Reference baseline: Highline Tree structural feel; widget approach: HVAC Pro Beast / TNJ.

## What's intentionally OMITTED (Phase 2 — after Santos & Sons says yes)
- **No SEO scaffolding**: no schema/structured data, no sitemap.xml, no robots.txt, no canonical tags, no OG/Twitter tags beyond basic title + description. Pages carry `noindex,nofollow` (it's a test build).
- **No service-detail subpages, no town pages, no blog.** Services live on one page.
- **No live form handling** — the estimate form is a labeled demo placeholder (alert on submit).
- **Chat widget not yet live** — every page has a labeled HTML comment placeholder before `</body>`; see `GHL_SETUP_SANTOS_AND_SONS.md`. The custom four-action launcher (Urgent text / Chat / Book estimate / Call) IS live; its Chat action falls back to the contact form until the GHL widget is embedded.

## Files
- `index.html` … 4-slide hero carousel (real project photos), trust bar, 3-pillar services, about preview, gallery preview, reviews, CTA
- `services.html` … all services on one page: installation by fence type, repair/replacement, hardscape, dumpster service
- `about.html` … Derek Santos / family story (BBB + FB verified facts only), how-we-work, service area + hours
- `gallery.html` … 8 real project photos with click-to-enlarge
- `contact.html` … estimate form (placeholder), call/text/email, hours, Google Map embed of their actual Dracut listing
- `404.html` … light, on-brand
- `css/site.css`, `js/site.js` (carousel/nav/gallery), `js/launcher.js` (four-action launcher + GHL handoff)
- `RESEARCH_NOTES.md` (all sourced facts), `GHL_SETUP_SANTOS_AND_SONS.md` (slot pack), `COMPLETION_REPORT.md`

## Brand tokens (sampled from their sign/crest — see RESEARCH_NOTES.md §4)
Hunter green `#1F3829` / `#16271C` · antique gold `#B9975B` / `#D6BC8A` · cream `#F7F5F1` · Playfair Display + Inter
