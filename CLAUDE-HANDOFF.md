# ScaleLocal — Claude Handoff Document
Updated: March 29, 2026 — ALL TASKS COMPLETE ✅

---

## PROJECT OVERVIEW
- **Product:** ScaleLocal — white-label local business marketing SaaS built on GHL
- **Website:** https://scalelocal.net (hosted on Vercel, DNS at Netlify)
- **GitHub Repo:** https://github.com/ScaleLocal/scalelocal-website
- **GHL Sub-account:** ScaleLocal | Location ID: cbDr5Xe384SCZnhPMvuZ
- **GHL Login:** matt@scalelocal.net
- **Business Phone:** 978.662.7580

---

## CRITICAL BRAND RULES (NEVER VIOLATE)
- NEVER mention GHL, Bolt.new, or any underlying platform to clients — ScaleLocal IS the product
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

## GHL CONFIGURATION — COMPLETE ✅

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

### Stripe Payment Handler Detail
Trigger: tag `deep-audit-paid` →
1. Add tag: `authority-client`
2. Create/Update Opportunity → ScaleLocal Sales Pipeline → Booked stage → $69
3. Send Email: "You're confirmed — your $69 website audit is booked, {{contact.first_name}}"
4. Internal alert to matt@scalelocal.net: "🔔 New $69 Audit Payment..."

### Free Website Delivery Sequence Detail
- Email 1 → Wait 2 days → Email 2 → Wait 3 days → Email 3 → Wait 4 days → Email 4

### Phone / Call Forwarding
- Business number: 978.662.7580
- Forwarding timeout: 20 seconds
- External cell: Matt entered manually ✅

### Matt Must Still Do
- Set up staff member profile so tasks can be auto-assigned
- Delete test contacts from GHL Contacts: Sarah Connor, Payload Capture, Capture Test, and MattYassen@yahoo.com test contacts
- Verify email sequences send correctly from alex@hi.scalelocal.net (check for first sequence triggered on test submissions)

---

## WEBSITE — scalelocal.net — FULLY WORKING ✅

### Infrastructure
- **Hosting:** Vercel project: scalelocal-website (matts-projects-ec31e28f)
- **Vercel URL:** vercel.com/matts-projects-ec31e28f/scalelocal-website
- **DNS:** Netlify DNS panel (domain registered/managed at Netlify)
  - A record: scalelocal.net → 216.198.79.1 (Vercel)
  - CNAME: www → 95de4b6ba3a5ed29.vercel-dns-017.com (Vercel)
  - NOTE: Two NETLIFY-type records were deleted (were overriding the A/CNAME). Do NOT re-add them.
- **Domain:** Both scalelocal.net and www.scalelocal.net → Valid Configuration ✅

### GHL API Token (CRITICAL)
- **Token type:** Location-level Private Integration (sub-account level)
- **Integration name:** "Coworker" in ScaleLocal sub-account Settings → Private Integrations
- **Vercel env var:** GHL_API_KEY (set in Vercel project settings)
- **Active token:** pit-f074b258-6b35-4d69-b928-6cfc73dc7144 (rotated March 29, 2026)
- **Old token:** pit-0580...08e4 (expires ~7 days after rotation)
- **IMPORTANT:** Must use SUB-ACCOUNT level token, NOT agency-level. Agency PIT tokens return 401 "not authorized for this scope" on contacts API.
- Scopes required: contacts.write ✅

### Serverless Function: api/submit-snapshot.js
- Receives POST with JSON: {first_name, last_name, email, phone, business_name, city, industry, source}
- Routes by `source` field:
  - snapshot → tag: snapshot-lead, source: "Website Snapshot Request"
  - audit → tag: audit-lead, source: "Website Audit Request"
  - grow → tag: grow-lead, source: "Website Grow Request"
  - free-website → tag: free-website-lead, source: "Website Free-Website Request"
- POSTs to: POST https://services.leadconnectorhq.com/contacts/
- Auth: Bearer {GHL_API_KEY}
- Version: 2021-07-28
- Always returns 200 to client (never blocks UX flow)

### Forms — All 4 Fixed and Tested ✅
| Page | Form Source | Tag | Confirmation | Tested |
|---|---|---|---|---|
| /snapshot | snapshot | snapshot-lead | Redirect to /snapshot/upgrade/ | ✅ |
| /audit | audit | audit-lead | Inline "You're on the list" | ✅ |
| /grow | grow | grow-lead | Inline "You're on the list" | ✅ |
| /free-website | free-website | free-website-lead | Inline "You're in" | ✅ |

### Upgrade Page (/snapshot/upgrade/)
- Shows upsell: Basic Snapshot ($0) vs Deep Audit ($97 one-time)
- $97 is the PUBLIC website price — separate from the $69 email-only offer
- Stripe link: https://buy.stripe.com/dRm14o6td9zN7J20NL3Je00
- "No thanks" button shows free confirmation inline (no page reload)

### GitHub Commits (March 29, 2026)
| Commit SHA | Description |
|---|---|
| 1549c67 | Add Vercel serverless function for GHL snapshot form submission |
| 698d110 | Add vercel.json config |
| 3a5f918 | Fix snapshot form: POST to Vercel /api/submit-snapshot |
| dbfdcc9 | Fix upgrade page: hoist capFirst/cfn before greeting assignment |
| 1c7254a | Fix: add source-based tagging for audit, grow, free-website pages |
| 0c5cf86 | Fix: audit page - use /api/submit-snapshot |
| 8ed9944 | Fix: grow page - use /api/submit-snapshot |
| a27cf1d | Fix: free-website page - use /api/submit-snapshot |

---

## PRICING REFERENCE
- **$0** — Basic Free Snapshot (delivered by Snapshot Delivery Sequence)
- **$97** — Deep Audit (public website price on /snapshot/upgrade page)
- **$69** — Deep Audit one-time offer (EMAIL ONLY — Email 3 of Snapshot Delivery Sequence)
- **$1,297/mo** — ScaleLocal Momentum System (on /grow page)
- **$497** — Keep the free website if you love it (on /free-website page)

---

## HOW TO START A NEW CLAUDE SESSION
Paste this entire document at the start of the new chat and say:
"Continue from the ScaleLocal handoff doc. The immediate task is [whatever is next]."
Claude will have full context and can pick up immediately.
