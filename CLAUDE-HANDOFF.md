# ScaleLocal — Claude Handoff Document
Generated: March 29, 2026

---

## PROJECT OVERVIEW
- **Product:** ScaleLocal — white-label local business marketing SaaS built on GHL
- **Website:** https://scalelocal.net
- **GitHub Repo:** https://github.com/ScaleLocal/scalelocal-website
- **GHL Sub-account:** ScaleLocal | Location ID: cbDr5Xe384SCZnhPMvuZ
- **GHL Login:** matt@scalelocal.net
- **Business Phone:** 978.662.7580

---

## CRITICAL BRAND RULES (NEVER VIOLATE)
- NEVER mention GHL, Bolt.new, or any underlying platform to clients
- ScaleLocal IS the product — GHL is just the engine
- Named persona: **Alex from ScaleLocal** for all prospect-facing emails
- From Email: alex@hi.scalelocal.net | Reply-to: alex@scalelocal.net
- **$69 audit upgrade offer lives ONLY in Email 3 of Snapshot Delivery Sequence** — never on website, never in cold outreach
- Cold email window: Tuesday–Thursday, 9–11AM local only
- DNC check before every sequence load
- NEVER send Stripe payment links directly — prepare only, flag Matt
- NEVER send GHL contracts/proposals without Matt's review
- Matt must enter his own personal cell number — never enter it for him

### GHL Brand Name Substitutions
| GHL Term | ScaleLocal Term |
|---|---|
| GHL CRM | ScaleLocal Dashboard |
| GHL Chatbot | ScaleLocal Chat |
| GHL Calendar | ScaleLocal Booking |
| GHL Call Tracking | ScaleLocal Tracking |
| GHL Voice AI | ScaleLocal Receptionist |

---

## GHL CONFIGURATION — COMPLETED ✅

### Pipelines (both built)
1. **ScaleLocal Sales Pipeline** — 9 stages
2. **AI Website Agent Pipeline** — 4 stages

### Workflows (all Published ✅)
| Workflow | Trigger | Status |
|---|---|---|
| New Lead Notification + Assignment | Contact Created | Published |
| Source Auto-Tagger | Contact Created | Published |
| Snapshot | Contact Tag: snapshot-lead | Published |
| Snapshot Delivery Sequence | Contact Tag: snapshot-lead | Published |
| Free Website Delivery Sequence | Contact Tag: free-website-lead | Published |
| Stripe Payment Handler | Contact Tag: deep-audit-paid | Published |

### Snapshot Delivery Sequence Detail
- Email 1: "Your free digital snapshot for {{contact.company_name}} is ready, {{contact.first_name}}"
- Wait: 2 days
- Email 2: "Did you get a chance to look at your snapshot, {{contact.first_name}}?"
- Wait: 3 days
- Email 3: "Last note on your snapshot + a special offer, {{contact.first_name}}"
  - **THIS IS THE ONLY PLACE THE $69 AUDIT OFFER APPEARS**
  - Subject intentionally soft — offer is inside the email body only

### Stripe Payment Handler Detail
Trigger: tag `deep-audit-paid` →
1. Add tag: `authority-client`
2. Create/Update Opportunity → ScaleLocal Sales Pipeline → Booked stage → $69
3. Send Email to contact: "You're confirmed — your $69 website audit is booked, {{contact.first_name}}"
4. Internal alert email to matt@scalelocal.net: "🔔 New $69 Audit Payment — {{contact.first_name}} {{contact.last_name}}"

### Free Website Delivery Sequence Detail
- Email 1: "Your free website for {{contact.company_name}} is ready, {{contact.first_name}}"
- Wait: 2 days
- Email 2: "Did you get a chance to check out your free website, {{contact.first_name}}?"
- Wait: 3 days
- Email 3: "Quick question about your free website, {{contact.first_name}}"
- Wait: 4 days
- Email 4: "Closing the loop on your free website, {{contact.first_name}}"

### Phone / Call Forwarding
- Business number: 978.662.7580
- Forwarding timeout: 20 seconds
- External cell: Matt entered manually ✅

### Matt Must Still Do
- Set up staff member profile so tasks can be auto-assigned

---

## WEBSITE — scalelocal.net

### Forms (4 pages)
All 4 forms connect to GHL via the same form ID: `tfnHv9TG6B8I6gf6Varo`
- /snapshot — Free Digital Audit request
- /audit — Google Ads audit
- /grow — Growth consultation
- /free-website — Free website offer

### Known Bug — FIXED IN GITHUB (not yet live, awaiting Vercel deploy)
**Problem:** The /snapshot form was POSTing to `api.leadconnectorhq.com/widget/form/tfnHv9TG6B8I6gf6Varo` which returns 503 consistently. Submissions were NOT reaching GHL for ~5 days.

**Root cause:** Deprecated GHL widget endpoint. The correct GHL endpoint is `backend.leadconnectorhq.com/forms/form-survey-event` but that requires same-origin (GHL hosted). Custom forms on external sites need to use the GHL Contacts API directly.

**Fix committed to GitHub (March 29, 2026):**
1. `api/submit-snapshot.js` — Vercel serverless function that receives form POST and forwards to GHL Contacts API using Bearer token auth
2. `vercel.json` — Vercel config
3. `snapshot/index.html` — form now POSTs to `/api/submit-snapshot` (JSON) instead of GHL widget
4. `snapshot/upgrade/index.html` — fixed `undefined` greeting bug (var hoisting issue — cfn was used before declaration)

### TO COMPLETE THE FIX — ACTION REQUIRED
1. Go to vercel.com → **Add New Project** → Import `ScaleLocal/scalelocal-website` repo
2. Add environment variable: `GHL_API_KEY` = [GHL location-level API key from Settings → API Key]
3. Set custom domain: `scalelocal.net`
4. Deploy
5. Test: submit /snapshot form → verify contact appears in GHL Contacts with correct fields

### Upgrade Page (/snapshot/upgrade/)
- Shows upsell: Basic Snapshot ($0) vs Deep Audit ($97 one-time)
- $97 is the PUBLIC website price — completely separate from the $69 email-only offer
- Stripe link: https://buy.stripe.com/dRm14o6td9zN7J20NL3Je00
- "No thanks" button shows free confirmation inline (no page reload)
- "Yes" button goes to Stripe with prefilled_email param

---

## REMAINING TASKS

### Immediate (blocking)
- [ ] Create new Vercel project for scalelocal-website repo
- [ ] Add GHL_API_KEY env var to that Vercel project
- [ ] Point scalelocal.net domain to new Vercel project
- [ ] Test /snapshot form end-to-end (submit → verify GHL contact created)

### Other forms not yet fixed
The /audit, /grow, and /free-website pages likely have the same 503 issue (same form ID used). Once /snapshot is confirmed working via Vercel, the same pattern needs to be applied to those pages.

### GHL Form Variables — Working Correctly
When a submission DOES reach GHL (confirmed via Matt's Mar 23 test submission):
- First Name → `{{contact.first_name}}`
- Last Name → `{{contact.last_name}}`
- Business Name → `{{contact.company_name}}`
- City → `{{contact.city}}`
- Phone → `{{contact.phone}}`
- Email → `{{contact.email}}`
- Industry → custom field

### Task 2a — Verify All 4 Forms
Pending Vercel deploy. After deploy, test all 4 forms:
- /snapshot ← fixed, test first
- /audit, /grow, /free-website ← likely need same Vercel function fix

---

## KEY TECHNICAL DETAILS

### GHL API (for Vercel function)
- Endpoint: `POST https://services.leadconnectorhq.com/contacts/`
- Auth header: `Authorization: Bearer {GHL_API_KEY}`
- Version header: `Version: 2021-07-28`
- Location ID: `cbDr5Xe384SCZnhPMvuZ`
- The function also applies tag `snapshot-lead` on creation, which triggers the Source Auto-Tagger and Snapshot Delivery Sequence workflows automatically

### GitHub Commits (March 29, 2026)
| Commit SHA | Description |
|---|---|
| 1549c67 | Add Vercel serverless function for GHL snapshot form submission |
| 698d110 | Add vercel.json config |
| 3a5f918 | Fix snapshot form: POST to Vercel /api/submit-snapshot |
| dbfdcc9 | Fix upgrade page: hoist capFirst/cfn before greeting assignment |

---

## HOW TO START A NEW CLAUDE SESSION
Paste this entire document at the start of the new chat and say:
"Continue from the ScaleLocal handoff doc. The immediate task is [whatever is next]."

Claude will have full context and can pick up immediately.
