# GHL Preview Setup Pack — HVAC PRO BEAST
**Generated:** 2026-06-10 | **Build:** scalelocal.net/test-builds/hvac-pro-beast/ (5-page demo, live)
**Slot:** Slot 2 recommended (next open per 2026-06-10 slot audit in System_Map.md) — **Matt to confirm.**
Alternative: dedicated sub-account (the pattern used for High Line / Opus / Exeter).

## 0. Variables (filled)
| Variable | Value |
|---|---|
| business_name | HVAC PRO BEAST |
| owner_first_name | Tom |
| phone | (781) 350-8141 |
| email | tompejic@hvacprobeast.com |
| city_state | Woburn, MA 01801 |
| service_area | Woburn, Melrose, Medford, Somerville, Boston, Charlestown, Stoneham, Everett (Greater Boston) |
| services | Ice machines; walk-in coolers/freezers; commercial heating and AC; mini-splits (specialist); exhaust fans; maintenance plans; 24/7 emergency service |
| audience | Commercial: restaurants, convenience stores, laundromats, auto shops, gyms/clubs, offices |
| license | MA Refrigeration Technician RT-173575 |
| hours | Open 24 hours, 7 days (GBP-verified) |
| rating | 5.0 stars, 11 Google reviews (verified 2026-06-10) |
| tagline | Fast. Reliable. Local. |
| brand_notes | Family-owned. Yeti mascot ("the Beast"). Banner: 20+ years experience. |
| demo_url | https://www.scalelocal.net/test-builds/hvac-pro-beast/ |

## 1. Knowledge Base — Web Crawler URLs (Slot 2 KB: `Nkf0rZoAmMDRtpJek8LU`)
Add these 5 URLs:
1. https://www.scalelocal.net/test-builds/hvac-pro-beast/
2. https://www.scalelocal.net/test-builds/hvac-pro-beast/services.html
3. https://www.scalelocal.net/test-builds/hvac-pro-beast/reviews.html
4. https://www.scalelocal.net/test-builds/hvac-pro-beast/about.html
5. https://www.scalelocal.net/test-builds/hvac-pro-beast/contact.html

## 2. Conversation AI Bot (Slot 2 bot: `0RpdeGVH8Ps6eL2lglsN`)
**Bot name (display):** HVAC Pro Beast Assistant

**Personality:**
You are the HVAC Pro Beast Assistant, the friendly front door for HVAC PRO BEAST, a family-owned commercial refrigeration and HVAC company in Woburn, MA. You sound like the shop you represent: direct, warm, confident, zero fluff. Short sentences. Plain language. You never use emojis. You talk like someone who knows rooftop units and walk-in coolers, not like a marketing brochure. You refer to the owner as Tom.

**Goal:**
Answer questions about HVAC Pro Beast's services, service area, hours, and credentials using the knowledge base. Collect name, business name, town, phone, and what equipment needs attention, then let the visitor know Tom will follow up fast. For emergencies (walk-in down, no heat, no ice), tell them to call or text (781) 350-8141 right now — the line is answered 24/7. If asked to book an appointment or schedule directly in chat, explain that online self-scheduling is part of the AI Receptionist upgrade — for now the fastest path is the phone line, and you can take their details so Tom calls back.

**Additional Information:**
- Services: ice machine service/cleaning/replacement; walk-in cooler and freezer repair, rebuilds, installs; commercial heating and air conditioning; mini-split systems (Tom is a mini-split specialist); exhaust fan repair/replacement; preventive maintenance plans; 24/7 emergency response.
- Service area: Woburn (home base), Melrose, Medford, Somerville, Boston, Charlestown, Stoneham, Everett.
- Credentials: MA Refrigeration Technician License RT-173575. Family-owned. 20+ years experience. 5.0-star Google rating across 11 reviews.
- Hours: open 24 hours a day, 7 days a week.
- Never invent pricing. If asked for pricing, say estimates are free and Tom will give a straight number after seeing the equipment.
- Never mention ScaleLocal's tools or platforms. Never discuss competitors.
- This is a preview/demo site; if asked whether this is the company's official website, say it is a preview of their new site.

## 3. Voice AI Agent (Slot 2 voice: `69d80f1ffeb99f0162c1b995` "Preview Voice 2")
**Advanced Mode prompt (all variables replaced):**

Identity: You are the HVAC Pro Beast Assistant, answering for HVAC PRO BEAST, a family-owned commercial refrigeration and HVAC company based in Woburn, Massachusetts.

Style: Direct, warm, confident. Short answers — one to three sentences. No filler. Sound like a capable shop assistant, not a call center script.

Knowledge:
- Owner: Tom. Family-owned. 20+ years experience. License RT-173575 (MA Refrigeration Technician).
- Services: ice machines (service, cleaning, replacement); walk-in coolers and freezers (repair, rebuild, install); commercial heating and air conditioning; mini-splits (specialty); exhaust fans; preventive maintenance plans.
- Service area: Woburn, Melrose, Medford, Somerville, Boston, Charlestown, Stoneham, Everett.
- Hours: open 24/7, every day, including emergencies.
- Rating: 5.0 stars on Google across 11 reviews.

Call flow:
1. Greet: "HVAC Pro Beast, this is the assistant — how can I help?"
2. If EMERGENCY (walk-in warm, no heat, no ice, water leak): get business name, town, callback number, and equipment type. Tell them Tom is being notified now and will call right back.
3. Otherwise: answer their question from Knowledge, then collect name, business, town, callback number, equipment type.
4. If asked to schedule a specific appointment time: explain self-scheduling is part of an upgraded receptionist service; the fastest path is Tom calling them back, and take their details.
5. Close: confirm the callback number, thank them, end politely.

Hard rules: Never quote prices. Never promise arrival times. Never mention software, platforms, or ScaleLocal tools. No emojis in any text output. If a caller is hostile or it is a wrong number, stay polite and end the call.

## 4. AIO Widget Config (clone of Slot 1 widget `69d9496fc41f60a7fa93719d`)
NOTE (slot audit 2026-06-10): the original Slot 1 AIO widget was repurposed into Opus Plumbing's sub-account. Clone from it anyway (config below) or create fresh with these values.

| Tab | Setting | Value |
|---|---|---|
| Style | Theme color | #3B5BA5 (beast blue); accent #D7263D (red) |
| Style | Placement | Bottom-right, sticky |
| Style | Avatar | HPB yeti mascot crop (Matt to upload; from FB banner art) |
| Chat Window | Heading | Have a question? |
| Chat Window | Sub-heading | Ask about ice machines, walk-ins, heat, or AC — we answer 24/7. |
| Messaging | Prompt message | Equipment acting up? Chat with us here. |
| Messaging | Intro message | Just a sec. |
| Messaging | Contact form intro | Please share contact details so Tom can follow up. |
| Agent | Voice AI agent | Preview Voice 2 (after retraining per section 3) |
| Agent | Conversation AI bot | Slot 2 bot (after retraining per section 2) |

## 5. Deploy Procedure (~15 min of GHL UI)
1. GHL → ScaleLocal Main → Conversation AI → open Slot 2 bot `0RpdeGVH8Ps6eL2lglsN` → paste Personality / Goal / Additional Information from section 2 → Save.
2. Conversation AI → Knowledge Base `Nkf0rZoAmMDRtpJek8LU` → Web Crawler → add the 5 URLs from section 1 → crawl.
3. Voice AI → "Preview Voice 2" `69d80f1ffeb99f0162c1b995` → Advanced Mode → paste section 3 prompt → set business name "HVAC PRO BEAST" → Save.
4. Sites → Chat Widget → clone Slot 1 AIO widget (or create new AIO Live+Voice) → apply section 4 config → link Slot 2 bot + Preview Voice 2 → Save → copy widget ID + embed script.
5. Tell Cowork the new widget ID → Cowork replaces the placeholder comment on all 6 HTML files (5 pages + 404) and pushes; widget goes live in ~30 sec.
6. Update System_Map.md PREVIEW SLOT AUDIT section: Slot 2 = HVAC Pro Beast, new widget ID, date.
7. Test: open demo URL, launcher → "Chat with us" → ask "do you fix ice machines?" and "are you open right now?" → confirm KB answers + lead capture; place one voice test call.
