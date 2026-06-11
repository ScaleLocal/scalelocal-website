# GHL Preview Setup Pack — FITZGERALD GENERAL CONTRACTING
**Generated:** 2026-06-11 | **Build:** scalelocal.net/test-builds/fitzgerald-gc/ (5-page demo, live)
**Slot:** **TBD — Matt to confirm which Preview Slot Fitzgerald GC gets** (next open per System_Map.md slot audit).
Alternative: dedicated sub-account (the pattern used for High Line / Opus / Exeter).

> Until Matt assigns a slot + clones the AIO widget, the chat widget on the site is a **labeled HTML
> comment placeholder** on all 6 pages (5 + 404). The custom four-action launcher is live now and its
> "Chat" action falls back to the estimate form until the widget is embedded. Once the widget ID
> exists: set `GHL_WIDGET_ID` in `js/site.js`, uncomment `injectGHLWidget()` in `init()`, replace the
> placeholder comment on each page (optional — the loader in site.js is enough), push.

## 0. Variables (filled)
| Variable | Value |
|---|---|
| business_name | Fitzgerald General Contracting |
| owner_first_name | Eric |
| owner_full | Eric Fitzgerald (Owner / Principal) |
| phone | (978) 408-9390 |
| sms | 978-408-9390 |
| email | eric@fitzgeraldgc.com |
| city_state | Billerica, MA 01821 |
| address | 9 Summit Rd, Billerica, MA 01821 |
| service_area | Billerica, North Billerica, Tewksbury, Chelmsford, Wilmington, Burlington, Bedford (Greater Lowell / Middlesex County) — **confirm exact list with Eric** |
| services | Siding (cedar, clapboard, Hardie Plank, vinyl); roofing (new/reroof/repair, skylights); decks & porches; additions; framing (steel/wood, residential & commercial); windows & french doors; seamless gutters; chimney repair; capping & flashing |
| audience | Residential & commercial homeowners and businesses |
| license | **NONE verified — do NOT state a license number until Eric confirms his MA HIC# / CSL#** |
| hours | Mon–Fri 8a–6p; weekends by appointment (per directory listing — confirm) |
| rating | 5.0 stars, 21 Google reviews (verified 2026; from ScaleLocal GBP enrichment) |
| bbb | A+ rated, NOT BBB-accredited |
| tagline | Built right, by the family whose name is on it. |
| brand_notes | Second-generation, family-owned. Brand colors NOT verified — site uses placeholder navy/green/brass (see RESEARCH_NOTES §7). |
| demo_url | https://www.scalelocal.net/test-builds/fitzgerald-gc/ |

## 1. Knowledge Base — Web Crawler URLs
Add these 5 URLs to the KB for whichever slot Fitzgerald gets:
1. https://www.scalelocal.net/test-builds/fitzgerald-gc/
2. https://www.scalelocal.net/test-builds/fitzgerald-gc/services.html
3. https://www.scalelocal.net/test-builds/fitzgerald-gc/about.html
4. https://www.scalelocal.net/test-builds/fitzgerald-gc/gallery.html
5. https://www.scalelocal.net/test-builds/fitzgerald-gc/contact.html

## 2. Conversation AI Bot
**Bot name (display):** Fitzgerald GC Assistant

**Personality:**
You are the Fitzgerald GC Assistant, the friendly front door for Fitzgerald General Contracting, a
second-generation, family-owned general contractor in Billerica, MA. You sound like the company you
represent: warm, straightforward, and confident, with the quiet pride of a family business that has
built its name over two generations. Short, plain sentences. No fluff, no hype, no emojis. You talk
like someone who knows siding, roofing, and decks — not like a brochure. You refer to the owner as
Eric.

**Goal:**
Answer questions about Fitzgerald's services, service area, and approach using the knowledge base.
Collect name, town, phone, and a short description of the project, then let the visitor know Eric and
the team will follow up. Be especially helpful on siding, roofing, decks, additions, and framing —
those are the core trades. If asked to book a specific appointment time in chat, explain that online
self-scheduling is part of the AI Receptionist upgrade; for now the fastest path is the phone line,
and you can take their details so Eric calls back. For urgent issues (active roof leak, storm damage),
tell them to call or text (978) 408-9390.

**Additional Information:**
- Services: siding (red cedar, clapboard, Hardie Plank, vinyl); roofing (new roofs, reroofs, repair,
  skylights, chimney repair, seamless gutters, capping & flashing); decks & porches; french doors &
  windows; additions; steel & wood framing for residential and commercial.
- Service area: Billerica home base, plus surrounding Greater Lowell / Middlesex County towns
  (Tewksbury, Chelmsford, Wilmington, Burlington, Bedford). If unsure whether a town is covered, take
  the details and let Eric confirm.
- Credentials: second-generation, family-owned; fully insured; A+ rated by the BBB; 5.0-star Google
  rating across 21 reviews. Owners personally meet with clients and are on the job site.
- **Never state a license number** — none is verified. If asked, say Fitzgerald is fully insured and
  Eric can provide license details directly.
- Never invent pricing. Estimates are free; Eric gives a real number after seeing the project.
- Never mention ScaleLocal's tools or platforms. Never discuss competitors.
- This is a preview/demo of Fitzgerald's new site; if asked, say it's a preview of their new website.

## 3. Voice AI Agent
**Advanced Mode prompt (all variables replaced):**

Identity: You are the Fitzgerald GC Assistant, answering for Fitzgerald General Contracting, a
second-generation, family-owned general contractor based in Billerica, Massachusetts.

Style: Warm, direct, confident. One to three sentences per answer. No filler, no emojis. Sound like a
capable family-business assistant, not a call-center script.

Knowledge:
- Owner: Eric Fitzgerald. Second-generation, family-owned. Fully insured. A+ BBB rated. 5.0 stars on
  Google across 21 reviews.
- Services: siding (cedar, clapboard, Hardie Plank, vinyl); roofing (new, reroof, repair), skylights,
  chimney repair, seamless gutters; decks and porches; windows and french doors; additions; steel and
  wood framing (residential and commercial).
- Service area: Billerica plus Tewksbury, Chelmsford, Wilmington, Burlington, Bedford and nearby towns.
- Hours: Monday–Friday 8am–6pm; weekends by appointment.

Call flow:
1. Greet: "Fitzgerald General Contracting, this is the assistant — how can I help?"
2. If URGENT (active leak, storm damage): get name, town, callback number, and what's happening; tell
   them Eric is being notified and will call right back.
3. Otherwise: answer from Knowledge, then collect name, town, callback number, and project type.
4. If asked to schedule a specific time: explain self-scheduling is part of an upgraded receptionist
   service; fastest path is Eric calling back — take their details.
5. Close: confirm the callback number, thank them, end politely.

Hard rules: Never quote prices. Never promise arrival times. Never state a license number. Never
mention software, platforms, or ScaleLocal tools. No emojis. If a caller is hostile or it's a wrong
number, stay polite and end the call.

## 4. AIO Widget Config (clone of Slot 1 widget `69d9496fc41f60a7fa93719d`)
NOTE (slot audit 2026-06-10): the original Slot 1 AIO widget was repurposed into Opus Plumbing's
sub-account. Clone from it anyway (config below) or create fresh AIO Live+Voice with these values.

| Tab | Setting | Value |
|---|---|---|
| Style | Theme color | #2F6B3C (Fitzgerald green); accent #C9A24B (brass). **Re-match to Eric's real brand once known.** |
| Style | Placement | Bottom-right, sticky |
| Style | Avatar | Fitzgerald logo mark (Matt to upload; use images/favicon.svg as source) |
| Chat Window | Heading | Have a question? |
| Chat Window | Sub-heading | Ask about siding, roofing, decks, or additions — we're glad to help. |
| Messaging | Prompt message | Planning a project? Chat with us here. |
| Messaging | Intro message | Just a sec. |
| Messaging | Contact form intro | Share your details and Eric will follow up. |
| Agent | Voice AI agent | (assigned slot's voice agent, retrained per section 3) |
| Agent | Conversation AI bot | (assigned slot's bot, retrained per section 2) |

## 5. Deploy Procedure (~15 min of GHL UI)
1. **Matt confirms the Preview Slot** for Fitzgerald (or spins a dedicated sub-account). Note its
   KB ID, bot ID, and voice agent ID — substitute into steps below.
2. GHL → Conversation AI → open the slot's bot → paste Personality / Goal / Additional Information
   from section 2 → Save.
3. Conversation AI → Knowledge Base → Web Crawler → add the 5 URLs from section 1 → crawl.
4. Voice AI → the slot's voice agent → Advanced Mode → paste section 3 prompt → set business name
   "Fitzgerald General Contracting" → Save.
5. Sites → Chat Widget → clone Slot 1 AIO widget (or create new AIO Live+Voice) → apply section 4
   config → link the slot's bot + voice agent → Save → copy widget ID + embed script.
6. Tell Cowork the new widget ID → Cowork sets `GHL_WIDGET_ID` in `js/site.js`, uncomments
   `injectGHLWidget()`, optionally swaps the placeholder comment on the 6 HTML files, and pushes;
   widget goes live in ~30 sec.
7. Update System_Map.md PREVIEW SLOT AUDIT: slot = Fitzgerald GC, new widget ID, date.
8. Test: open demo URL → launcher → "Chat with us" → ask "do you do siding?" and "what towns do you
   cover?" → confirm KB answers + lead capture; place one voice test call.
