# LawnWize Rebuild — Research Notes

Compiled 2026-06-10 from the live lawnwize.com (WordPress 7.0 site).

## Business Facts (from current site)

- **Name:** LawnWize, "a Wize Enterprise Company" (Wize Enterprise LLC)
- **Tagline:** "Cut Sharp. Look Smart." (also: "Smarter lawn care powered by precision and speed" / "We trim the grass, not the standards")
- **Phone:** (810) 224-1089
- **Email:** info@lawnwize.com
- **Hours:** Mon–Fri 7:00 am – 7:00 pm, Sat 8:00 am – 5:00 pm, Sun closed
- **Service area:** Livingston County, MI (map on their site centers on Howell/Fowlerville). Contact page lists "Ingham County (Coming Soon)" and "Eaton County (Coming Soon)"
- **Positioning:** family-owned, locally operated, new business launched 2026, backed by 10+ years of professional lawn care experience; satisfaction guarantee; transparent pricing
- **Socials:** Facebook (profile.php?id=61587145201168), Instagram @lwnwze

## People (from /our-staff)

- **Evan** — Owner & Founder. Hands-on, works in the field, built the company on reliability, communication, superior results.
- **Dylan** — Operations Manager. 10+ years professional lawn care and outdoor maintenance experience; leads daily ops, trains crews, in the field weekly.

## Services (from /services + detail pages)

1. **Residential Lawn & Grounds Maintenance:** mowing, edging, cleanup, aeration, thatching, leaf removal, over-seeding
2. **Commercial Lawn & Grounds Maintenance:** commercial mowing, edging, cleanup, aeration, thatching, leaf removal
3. **Snow & Ice Services:** snow plowing & site clearing, sidewalk shoveling & snow removal, salt & de-icing, custom service plans, flat-rate monthly billing
4. **Landscape Design & Installation:** softscape installation, mulch & rock, landscape lighting, holiday lighting (Govee smart lighting), irrigation maintenance, flower & garden bed design, garden bed maintenance, pergolas & outdoor structures, fire pits & outdoor heating, patios & decks

## "Our Core Standards" (from /about-us)

1. Professional, high-quality results — clean cuts, sharp edges, polished lawn
2. Reliable, on-time service — dependable scheduling, clear communication
3. Family-owned care & pride — personal attention, integrity
4. 10+ years of proven experience — tailored to Michigan lawns
5. Transparent, fair pricing — honest quotes, no hidden fees

## Brand / Visual

- **Logo:** italic heavy wordmark — "LAWN" in green over "WIZE" in black with a green grass-blade swoosh between; tagline "CUT SHARP. LOOK SMART." beneath; small gold "Part of Wize Enterprise LLC" badge. Dominant colors sampled from logo PNG: green ~#199500, near-black #161918.
- Rebuilt as clean inline SVG (green #1B8E20 / ink #161918, accent #2DB535) — `images/logo-lawnwize.svg`.
- Current site photos are AI-generated (Microsoft Copilot/Designer filenames) — not used. All build photography sourced as stock instead.

## Photography Sourced

All images downloaded (not hotlinked) from Unsplash and Pexels free-license libraries, resized and compressed locally. Subjects: residential mowing/edging, manicured Midwest homes and lawns, striped commercial turf, garden beds and softscape, landscape lighting at dusk, outdoor living, soil/planting closeups, Michigan-style winter scenes. No staged "team" photos were used and none were fabricated; team section uses monogram avatars.

## Decisions / Notes for Matt

- Copy uses only verifiable claims from their own site (10+ years experience, family-owned, satisfaction guarantee). No testimonials or review stars anywhere — none exist yet for this business.
- "Holiday Lighting (Govee)" kept brand-generic as "app-controlled smart holiday lighting" on the rebuild; easy to re-add the Govee name if Evan wants it.
- Their homepage "kicking off our lawn care business this year" framing was softened to "family-owned crew with a decade in the field" to stay accurate while not leading with "brand new."
- Contact form is static (mailto compose) with a clearly-commented swap point for Evan's preferred form provider.
- Map embed: Google Maps embed of Livingston County, MI (keyless embed URL).
