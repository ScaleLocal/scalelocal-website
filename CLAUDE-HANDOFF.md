# ScaleLocal — Claude Handoff Document
Last Updated: March 29, 2026 — ALL SETUP COMPLETE

---

## HOW TO START A NEW CLAUDE SESSION
Paste this entire document at the start of a new chat and say:
"Continue from the ScaleLocal handoff doc. The task today is [whatever you need]."
Claude will have full context and can pick up immediately.

---

## OPEN TASK LIST

### Matt Must Do Manually (Before Next Session)
- [ ] Accept GHL invitation at alex@scalelocal.net (set password, log in)
- [ ] Accept GHL invitation at olivia@scalelocal.net (set password, log in)
- [ ] Delete test contacts from GHL Contacts:
  - Sarah Connor (sarah.connor.greenthumb@example.com)
  - Payload Capture (payload.capture.ghl@example.com)
  - Capture Test (capture.test.payload@...)
  - Matt Yassen test contact (MattYassen@yahoo.com)
- [ ] Check yahoo inbox (MattYassen@yahoo.com) — confirm Snapshot Delivery Sequence emails arriving from alex@hi.scalelocal.net

### Future / Next Claude Session
- [ ] Cold email list upload — when ready for outreach, load prospect list and enroll in sequences (Tue-Thu 9-11AM only, DNC check first)
- [ ] Buy tracking phone numbers via Phone System for call tracking per campaign
- [ ] Set up Google review request automation (post job-completion trigger)
- [ ] Configure ScaleLocal Chat (chatbot) for website
- [ ] Set up ScaleLocal Booking (calendar) for prospect calls

---

## PROJECT OVERVIEW
- **Product:** ScaleLocal — white-label local business marketing platform (built on GHL)
- **Website:** https://scalelocal.net
- **GitHub Repo:** https://github.com/ScaleLocal/scalelocal-website
- **GitHub PAT:** Stored in Matt's 1Password / provided at session start — do not hardcode here
- **GHL Sub-account:** ScaleLocal | Location ID: cbDr5Xe384SCZnhPMvuZ
- **GHL Login:** matt@scalelocal.net
- **Business Phone:** 978.662.7580

---

## CRITICAL BRAND RULES (NEVER VIOLATE)
- NEVER mention GHL, Bolt.new, or any underlying platform to clients — ScaleLocal IS the product
- Named personas: **Alex** and **Olivia** from ScaleLocal — all prospect-facing communication
- From Email: alex@hi.scalelocal.net | Reply-to: alex@scalelocal.net
- **$69 audit upgrade offer lives ONLY in Email 3 of Snapshot Delivery Sequence** — never on website, never in cold outreach, nowhere else
- Cold email window: Tuesday-Thursday, 9-11AM local only
- DNC check before every sequence load — no exceptions
- NEVER send Stripe payment links directly — prepare only, flag Matt
- NEVER send GHL contracts/proposals without Matt's review
- NEVER enter Matt's personal cell — he must enter it himself

### GHL Brand Name Substitutions
| GHL Term | ScaleLocal Term |
|---|---|
| GHL CRM | ScaleLocal Dashboard |
| GHL Chatbot | ScaleLocal Chat |
| GHL Calendar | ScaleLocal Booking |
| GHL Call Tracking | ScaleLocal Tracking |
| GHL Voice AI | ScaleLocal Receptionist |

---

## GHL CONFIGURATION — COMPLETE

### Staff / Team Members
| Name | Email | Role |
|---|---|---|
| Alex ScaleLocal | alex@scalelocal.net | ACCOUNT-ADMIN |
| Olivia ScaleLocal | olivia@scalelocal.net | ACCOUNT-ADMIN |

### Lead Assignment
- Workflow: New Lead Notification + Assignment
- Method: Round-robin, equally split between Alex and Olivia
- Only applies to unassigned contacts
- Follow-up task auto-assigned to Contact's Assigned User

### Pipelines
1. ScaleLocal Sales Pipeline — 9 stages
2. AI Website Agent Pipeline — 4 stages

### Workflows (all Published)
| Workflow | Trigger | Notes |
|---|---|---|
| New Lead Notification + Assignment | Contact Created | Round-robin Alex/Olivia, notify, task, create opportunity |
| Source Auto-Tagger | Contact Created | Tags by source path |
| Snapshot | Contact Tag: snapshot-lead | Snapshot delivery |
| Snapshot Delivery Sequence | Contact Tag: snapshot-lead | 3 emails — $69 offer in Email 3 only |
| Free Website Delivery Sequence | Contact Tag: free-website-lead | 4 emails |
| Stripe Payment Handler | Contact Tag: deep-audit-paid | Confirms payment, notifies Matt |

### Snapshot Delivery Sequence
- Email 1: Snapshot ready
- Wait 2 days
- Email 2: Did you get a chance to look?
- Wait 3 days
- Email 3: Last note + $69 one-time upgrade offer (ONLY place this appears)

### Stripe Payment Handler
Trigger: tag deep-audit-paid
1. Add tag: authority-client
2. Create opportunity in ScaleLocal Sales Pipeline, Booked stage, $69
3. Email contact confirmation
4. Internal alert to matt@scalelocal.net

### Phone / Call Forwarding
- Business number: 978.662.7580
- Forwarding timeout: 20 seconds
- External cell: Matt entered manually

---

## WEBSITE — scalelocal.net — FULLY WORKING

### Infrastructure
- Hosting: Vercel — project scalelocal-website (matts-projects-ec31e28f)
- DNS: Netlify DNS panel
  - A record: scalelocal.net -> 216.198.79.1
  - CNAME: www -> 95de4b6ba3a5ed29.vercel-dns-017.com
  - WARNING: Do NOT re-add NETLIFY-type records — deleted March 29, caused conflicts
- Auto-deploys on every push to GitHub main branch

### GHL API Token
- Type: Sub-account (location-level) Private Integration — NOT agency-level
- Integration name: "Coworker" in ScaleLocal sub-account Settings -> Private Integrations
- Vercel env var: GHL_API_KEY
- Current token set: March 29, 2026 (valid; old token expires ~7 days after rotation)
- WARNING: Agency-level tokens return 401 on contacts API — must use sub-account token

### Serverless Function: api/submit-snapshot.js
Creates GHL contacts from all website form submissions. Routes by source field:
| source value | GHL Tag | GHL Source Label |
|---|---|---|
| snapshot | snapshot-lead | Website Snapshot Request |
| audit | audit-lead | Website Audit Request |
| grow | grow-lead | Website Grow Request |
| free-website | free-website-lead | Website Free-Website Request |

### Forms — All Fixed and Tested
| Page | Confirmation UX |
|---|---|
| /snapshot | Redirect to /snapshot/upgrade/ with prefilled URL params |
| /audit | Inline confirmation: "You're on the list" |
| /grow | Inline confirmation after "I'd rather talk" toggle |
| /free-website | Inline confirmation: "You're in" |

### Upgrade Page (/snapshot/upgrade/)
- Shows upsell: Basic Snapshot (free) vs Deep Audit ($97)
- $97 is the PUBLIC website price — completely separate from the $69 email-only offer
- Stripe link: https://buy.stripe.com/dRm14o6td9zN7J20NL3Je00

---

## PRICING REFERENCE
| Price | What | Where it appears |
|---|---|---|
| $0 | Basic Snapshot | Delivered via Snapshot Delivery Sequence |
| $97 | Deep Audit | Public price on /snapshot/upgrade page |
| $69 | Deep Audit one-time offer | Email 3 of Snapshot Delivery Sequence ONLY |
| $1,297/mo | ScaleLocal Momentum System | /grow page |
| $497 | Keep the free website | /free-website page |

---

## KEY TECHNICAL REFERENCE

### GHL Contacts API
- Endpoint: POST https://services.leadconnectorhq.com/contacts/
- Auth header: Authorization: Bearer {GHL_API_KEY}
- Version header: 2021-07-28
- Location ID: cbDr5Xe384SCZnhPMvuZ

### Token Rotation (if GHL_API_KEY expires)
1. GHL -> sub-account -> Settings -> Private Integrations -> Coworker -> rotate token
2. Vercel -> project -> Settings -> Environment Variables -> update GHL_API_KEY
3. Redeploy (or any push to main triggers auto-deploy)

### Vercel Project
- URL: vercel.com/matts-projects-ec31e28f/scalelocal-website
- Deployments tab shows full history and live status
