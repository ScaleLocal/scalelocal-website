# Maine General Contractors — Demo Build

Built 2026-07-17 by ScaleLocal (Cowork session). 5 pages, modern craftsman
design, static HTML/CSS/JS — no GHL, no trackers, no form backend.

**Live at:** https://www.scalelocal.net/test-builds/mainegcs/

## Verified business facts (sources: mainegcs.com + their Houzz profile)

- Name: Maine General Contractors ("MGC") — Freeport, ME 04032
- Phone: (207) 272-4923 (Houzz business listing)
- Mission: "change the status quo in construction by fostering relationships
  and delivering on our promises" (their own copy — quoted on homepage)
- Positioning: locally owned · high-end · custom work · design-build
- Typical job cost: $5,000 – $1.5M (Houzz)
- Named projects: Harris Ave Bathroom (Portland), Auburn Camp, Kitchen
  Renovation (Portland), Sunroom Addition (Portland) — from Houzz
- Areas: 36 towns, Greater Portland + Midcoast (Houzz areas-served list)
- Services list: from Houzz services-provided section
- Photos: THEIR OWN project photography, hotlinked from their GoDaddy CDN
  (img1.wsimg.com). For a production handoff, download + optimize locally.

## Config — one place: js/site.js CONFIG block

- PHONE: verified, wired to every call/text button
- EMAIL: `info@mainegcs.com` is a PLACEHOLDER — confirm their real email
  (GBP or ask) before pitching hard on the form
- CALENDAR_URL: empty. Paste a Calendly/Google booking link and every
  "Book an appointment" button lights up automatically. Until then the
  widget shows a friendly "coming soon — call or text" note and inline
  book links fall back to a phone call.

## Custom contact widget

Floating "Let's talk" launcher (bottom-right, every page): Call us ·
Text us · Email us · Book an appointment. Pure vanilla JS, no GHL, no
third-party embeds. The contact form composes an email in the visitor's
mail app (nothing stored server-side).

## Honest-claims policy

No fabricated reviews, testimonials, or stats. All claims trace to their
own site or Houzz profile. They have 5 GBP reviews — we deliberately did
NOT quote or invent review content; a reviews section can be added with
their permission using real review text.

## Mobile sign-off gate (added 2026-07-17 after the mobile miss)

No demo build ships without a REAL 375px-width screenshot check verifying:
- [ ] Logo present and legible in the header
- [ ] Nav collapsed to hamburger (breakpoint 860px)
- [ ] Hero text padded, readable over a gradient scrim (never raw over photo)
- [ ] CTAs stacked full-width, primary on top
- [ ] Stats/metrics in their own band below the hero, never overlaid
- [ ] Floating widget is a compact icon that obscures no content
