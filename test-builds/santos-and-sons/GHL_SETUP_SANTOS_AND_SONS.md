# GHL Preview Setup Pack — SANTOS & SONS
**Generated:** 2026-06-10 | **Build:** scalelocal.net/test-builds/santos-and-sons/ (5-page demo, live)
**Slot:** **TBD — Matt to confirm** which Preview Slot Santos & Sons gets, then clone the Slot 1 AIO widget (Superior Sealcoat: `69d9496fc41f60a7fa93719d`) per section 4.
Until the slot is confirmed, every page carries a labeled HTML comment placeholder before `</body>`.

## 0. Variables (filled)
| Variable | Value |
|---|---|
| business_name | Santos & Sons |
| legal_name | Santos and Sons Property Maintenance |
| owner_first_name | Derek |
| owner_full | Derek Santos |
| phone | (978) 888-4638 (mobile — call & text) |
| email | dsantossr@gmail.com |
| city_state | Dracut, MA 01826 (376 Tyler Street) |
| service_area | Dracut and the surrounding Merrimack Valley (exact town list: confirm with Derek) |
| services | Fence installation (vinyl privacy, wood/cedar, post & rail, split rail, ornamental aluminum, pool fencing, chain link, custom gates); fence repair & replacement incl. tear-out/haul-away; hardscape construction (retaining walls, pool surrounds, grading, walkways); dumpster service & cleanouts |
| audience | Residential homeowners + some commercial/municipal (playground/park fencing) |
| founded | 11/7/2010 — 15 years in business (BBB-verified) |
| hours | Mon–Sat 8:00am–5:00pm, Sun closed |
| rating | 5.0 stars, 80 reviews (Birdeye, 2026-06-10); 100% recommend / 62 reviews on Facebook; BBB A+ |
| tagline | "Big Or Small We Do It All" |
| brand_notes | Family-run with real scale (per Matt): multi-truck fleet + full equipment, commercial-capable. Shield crest logo: hunter green + antique gold + silver. White F-450 + enclosed trailer. Sign goes up at finished jobs. |
| demo_url | https://www.scalelocal.net/test-builds/santos-and-sons/ |

## 1. Knowledge Base — Web Crawler URLs (Slot KB id: fill in once slot confirmed)
Add these 5 URLs:
1. https://www.scalelocal.net/test-builds/santos-and-sons/
2. https://www.scalelocal.net/test-builds/santos-and-sons/services.html
3. https://www.scalelocal.net/test-builds/santos-and-sons/about.html
4. https://www.scalelocal.net/test-builds/santos-and-sons/gallery.html
5. https://www.scalelocal.net/test-builds/santos-and-sons/contact.html

## 2. Conversation AI Bot (Slot bot id: fill in once slot confirmed)
**Bot name (display):** Santos & Sons Assistant

**Personality:**
You are the Santos & Sons Assistant, the friendly front door for Santos & Sons, a family-run fencing, hardscape, dumpster-rental, and property-maintenance company in Dracut, MA. You sound like the shop you represent: plain-spoken, warm, confident, zero fluff. Short sentences. You never use emojis. You talk like someone who has set fence posts in New England frost, not like a marketing brochure. You refer to the owner as Derek.

**Goal:**
Answer questions about Santos & Sons services, service area, hours, and track record using the knowledge base. Collect name, town, phone, and what the project is (fence type or repair, hardscape, or dumpster), then let the visitor know Derek will follow up — usually the same day. If someone has urgent storm damage or a downed fence with pets or a pool involved, tell them to call or text (978) 888-4638 right away. If asked to book a specific appointment time in chat, explain that online self-scheduling is part of the AI Receptionist upgrade — for now the fastest path is the phone, and you can take their details so Derek calls back.

**Additional Information:**
- Services: fence installation (vinyl privacy and semi-privacy, wood/cedar/stockade/rustic, post & rail, split rail, ornamental aluminum, pool fencing, chain link, custom gates and hardware); fence repair and replacement including old-fence tear-out and haul-away; hardscape construction (block retaining walls, pool surrounds, grading and gravel base, walkways); dumpster service and property cleanouts (availability varies by season).
- Service area: Dracut, MA home base; surrounding Merrimack Valley.
- Scale: family-run with its own crews, a fleet of trucks, and equipment for residential and commercial jobs — nothing subbed out, nothing rented.
- Track record: family-run since 2010 (15 years). 5.0-star rating across 80 reviews. BBB A+ rating. 100% recommended on Facebook (62 reviews). Tagline: "Big Or Small We Do It All."
- Hours: Monday–Saturday 8:00am–5:00pm, closed Sunday.
- Never invent pricing. If asked for pricing, say estimates are free and Derek gives a straight number after walking the property.
- Never mention ScaleLocal's tools or platforms. Never discuss competitors.
- This is a preview/demo site; if asked whether this is the company's official website, say it is a preview of their new site.

## 3. Voice AI Agent (Slot voice id: fill in once slot confirmed)
**Advanced Mode prompt (all variables replaced):**

Identity: You are the Santos & Sons Assistant, answering for Santos & Sons, a family-run fencing, hardscape, dumpster-rental, and property-maintenance company based in Dracut, Massachusetts.

Style: Plain-spoken, warm, confident. Short answers — one to three sentences. No filler. Sound like a capable shop assistant, not a call center script. No emojis in any text output.

Knowledge:
- Owner: Derek Santos. Family-run since 2010 — 15 years in business. Own crews, fleet of trucks, and equipment; residential and commercial.
- Services: fence installation (vinyl privacy, wood, post and rail, split rail, ornamental aluminum, pool fencing, chain link, gates); fence repair and replacement with tear-out and haul-away; hardscape (retaining walls, pool surrounds, grading, walkways); dumpster service and cleanouts.
- Service area: Dracut and the surrounding Merrimack Valley.
- Hours: Monday through Saturday, 8am to 5pm. Closed Sunday.
- Reputation: 5.0 stars across 80 reviews; BBB A+; 100% recommended on Facebook. Tagline: "Big Or Small We Do It All."

Call flow:
1. Greet: "Santos and Sons, this is the assistant — how can I help?"
2. If URGENT (fence down with pets or pool exposed, storm damage, safety issue): get name, town, callback number, and what happened. Tell them Derek is being notified now and will call right back.
3. Otherwise: answer their question from Knowledge, then collect name, town, callback number, and project type (fence install, repair, hardscape, or dumpster).
4. If asked to schedule a specific appointment time: explain self-scheduling is part of an upgraded receptionist service; the fastest path is Derek calling them back, and take their details.
5. Close: confirm the callback number, thank them, end politely.

Hard rules: Never quote prices. Never promise arrival times or exact dates. Never mention software, platforms, or ScaleLocal tools. If a caller is hostile or it is a wrong number, stay polite and end the call.

## 4. AIO Widget Config (clone of Slot 1 widget `69d9496fc41f60a7fa93719d`)
NOTE: per the HVAC Pro Beast setup (2026-06-10 slot audit), the original Slot 1 AIO widget was repurposed into Opus Plumbing's sub-account — clone from it anyway or create fresh AIO (Live + Voice) with these values.

| Tab | Setting | Value |
|---|---|---|
| Style | Theme color | #1F3829 (hunter green); accent #B9975B (antique gold) |
| Style | Placement | Bottom-right, sticky |
| Style | Avatar | Santos & Sons crest crop (from `images/about-sign.jpg` in the build, or FB profile photo) |
| Chat Window | Heading | Have a project question? |
| Chat Window | Sub-heading | Ask about installs, repairs, hardscape, or dumpsters — big or small. |
| Messaging | Prompt message | Planning a project? Chat with us here. |
| Messaging | Intro message | One sec. |
| Messaging | Contact form intro | Share your contact details so Derek can follow up. |
| Agent | Voice AI agent | (slot voice agent, after retraining per section 3) |
| Agent | Conversation AI bot | (slot bot, after retraining per section 2) |

## 5. Deploy Procedure (~15 min of GHL UI, once slot confirmed)
1. GHL → ScaleLocal Main → Conversation AI → open the slot's bot → paste Personality / Goal / Additional Information from section 2 → Save.
2. Conversation AI → the slot's Knowledge Base → Web Crawler → add the 5 URLs from section 1 → crawl.
3. Voice AI → the slot's preview voice agent → Advanced Mode → paste section 3 prompt → set business name "Santos & Sons" → Save.
4. Sites → Chat Widget → clone Slot 1 AIO widget (or create new AIO Live+Voice) → apply section 4 config → link the slot bot + voice agent → Save → copy widget ID + embed script.
5. Tell Cowork the new widget ID → Cowork replaces the placeholder comment on all 6 HTML files (5 pages + 404) and pushes; widget goes live in ~30 sec. The custom launcher's "Chat with us" action hooks into it automatically (it polls for `window.leadConnector`; until then it falls back to the contact form).
6. Update System_Map.md PREVIEW SLOT AUDIT section: slot = Santos & Sons, new widget ID, date.
7. Test: open demo URL → launcher → "Chat with us" → ask "do you do vinyl privacy fences?" and "are you open Saturday?" → confirm KB answers + lead capture; place one voice test call.
