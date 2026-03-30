# ScaleLocal — Claude Handoff Document
Last Updated: March 30, 2026 — CHECKOUT LIVE, STRIPE INTEGRATED

## HOW TO START A NEW CLAUDE SESSION
Paste this entire document at the start of a new chat and say: "Continue from the ScaleLocal handoff doc. The task today is [whatever you need]." Claude will have full context and can pick up immediately.

## OPEN TASK LIST

### CoWork Must Do First Session
- [ ] Fix Snapshot Delivery Sequence trigger (change from snapshot-lead to snapshot-delivered) — emails firing before PDF exists
- [ ] Build audit delivery pipeline (snapshot PDF + deep audit generation)
- [ ] Paste $69 Stripe link into GHL Snapshot Delivery Sequence Email 3
- [ ] Check email warming status in GHL
- [ ] Build onboarding workflows in GHL (tag-triggered: welcome email + data sheet + access grants per tier)
- [ ] Set up daily operations schedule (5 scheduled tasks, status emails at 7/9/12/3/7)
- [ ] Configure ScaleLocal Chat (chatbot) for website
- [ ] Configure ScaleLocal Booking (calendar) for prospect calls

### Matt Must Do
- [ ] Rotate Stripe API key (used in session)
- [ ] Rotate GitHub PAT (used for 25+ commits)
- [ ] Create Google Ads MCC (ads.google.com/home/tools/manager-accounts)
- [ ] Create Meta Business Manager (business.facebook.com)
- [ ] Keep desktop awake 6 AM – 12 AM for CoWork scheduled tasks
- [ ] Reapply for Google Business Profile
- [ ] Submit sitemap to Google Search Console
- [ ] Configure Stripe webhook endpoint: https://www.scalelocal.net/api/stripe-webhook (events: checkout.session.completed)
- [ ] Service agreement attorney review

## PROJECT OVERVIEW
- Product: ScaleLocal — white-label local business marketing platform (built on GHL)
- Website: https://scalelocal.net (Vercel, auto-deploys on GitHub push)
- GitHub Repo: https://github.com/ScaleLocal/scalelocal-website
- GHL Sub-account: ScaleLocal | Location ID: cbDr5Xe384SCZnhPMvuZ
- GHL Login: matt@scalelocal.net
- Business Phone: 978.662.7580
- Google API Key: AIzaSyCVPo1T_toVUwBieeD04eTgpeWo_qklPFQ (Places + PageSpeed)

## CRITICAL BRAND RULES
- NEVER mention GHL, GoHighLevel, Bolt.new, or any platform name to clients
- Named personas: Alex and Olivia — all prospect-facing communication
- From Email: alex@hi.scalelocal.net | Reply-to: alex@scalelocal.net
- $69 audit offer ONLY in Snapshot Delivery Sequence Email 3 — nowhere else
- Cold email window: Tue-Thu 9-11 AM local only
- NEVER send Stripe links without flagging Matt
- NEVER enter Matt's personal cell number

## GHL CONFIGURATION — COMPLETE
- Staff: Alex ScaleLocal (alex@scalelocal.net) + Olivia ScaleLocal (olivia@scalelocal.net), ACCOUNT-ADMIN
- Lead Assignment: Round-robin, equally split
- Pipelines: ScaleLocal Sales Pipeline (9 stages) + AI Website Agent (4 stages)
- Workflows: New Lead Notification, Source Auto-Tagger, Snapshot Delivery Sequence, Free Website Delivery Sequence, Stripe Payment Handler
- Tags: 71 tags covering all products, onboarding stages, and operations
- Custom Fields: Town, Business Name, Industry, Biggest Challenge, Plan Tier, Commitment Term, Onboarding Status, Monthly Revenue, Signup Date, Commitment End Date, Lead Guarantee, Account Manager
- Phone: 978.662.7580 with call forwarding to Matt's cell (20s timeout, whisper)

## WEBSITE — FULLY WORKING
- Hosting: Vercel (auto-deploys on GitHub push to main)
- Serverless Functions: api/submit-snapshot.js (form handler), api/stripe-webhook.js (payment webhook)
- Pages: / (homepage), /menu, /checkout, /snapshot, /snapshot/upgrade, /audit, /grow, /free-website, /websites, /receptionist, /reactivation, /start, /quiz, /recommendation, /welcome, /terms, /privacy, /blog (17 posts), /local (20 cities)
- Checkout: Redirects to Stripe Payment Links (real payments, not simulated). Supports focused mode for standalone products.

## STRIPE — FULLY CONFIGURED
- 14 products, 27 payment links, 3 coupons (12mo-loyalty-free-month, audit-credit-69, audit-credit-97)
- Webhook endpoint: /api/stripe-webhook (needs Stripe Dashboard configuration)
- Full catalog: ScaleLocal_Stripe_Payment_Links.md

## PRICING (SIMPLIFIED)
- Monthly price is the SAME regardless of term
- M2M: $497 base setup ($249 Starter), waived on 6mo/12mo
- 12-month: month 12 free via coupon
- Authority: $497 base + $997 AI Receptionist setup (stacked, receptionist never waived)
- AI Receptionist Momentum add-on: $997 setup + $297/mo
- NO 3-month tier exists

## AD ACCOUNT ARCHITECTURE
- Google Ads: ScaleLocal MCC (Matt creates), sub-accounts per client, ScaleLocal pays
- Meta: ScaleLocal Business Manager (Matt creates), ad accounts per client, ScaleLocal pays
- LSAs: Client account (business verification required), ScaleLocal added as agency manager
- Client never touches ad platforms

## KEY TECHNICAL REFERENCE
- GHL API: Sub-account token via Vercel env var GHL_API_KEY
- Google APIs: AIzaSyCVPo1T_toVUwBieeD04eTgpeWo_qklPFQ (Places + PageSpeed)
- Token Rotation: GHL → Private Integrations → Coworker → rotate → update Vercel env var → redeploy
