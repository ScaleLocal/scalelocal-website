# Six-firm audit — findings before build

Audited live 2026-07-30 by six parallel agents, one per site. Mail exchangers verified independently. Everything below was observed, not inferred.

---

## The headline

**The features you asked me to preserve are mostly not the firms' to give.**

Every calculator on every one of these sites is a vendor-licensed widget running on the vendor's account, not the firm's. Hickey's 147 calculators and Mass Tax Pros' 13 are both **CalcXML skin 481** — the *same* skin ID, because both sites were built by CPA Site Solutions and both are riding that vendor's CalcXML licence. Carella's 40 are Wolters Kluwer's, served from `cchwebsites.com`. None of it is portable. If a firm leaves the vendor, the calculators go with the vendor.

The same is true of the article libraries. Hickey's ~249 "financial guides," 191 QuickBooks tips and monthly newsletter are all CPA Site Solutions syndicated feed. Carella's entire newsletter section is CCH's. Goguen's newsletter is `resourcesforclients.com`. None of it is firm-written and none of it transfers.

So "no degradation" can't mean lift-and-shift. What it can mean — and what I'd argue is a stronger pitch — is below.

---

## What each firm actually has

| Firm | Town | Calculators | Portal | Payments | Real gaps |
|---|---|---|---|---|---|
| **James L. Hickey, CPA PC** | Tewksbury | 147 (CalcXML, vendor skin 481) | CPA Site Solutions Secure Firm Portal — **self-registration dead (503)** | PayPal button | **No HTTPS at all.** Portal password field on every page over plain HTTP |
| **Charles M. Carella, CPA** | N. Billerica | 40 (CCH pop-outs) | **None** | **None** | HTTPS serves Wolters Kluwer's cert → browser security interstitial. Logo file is a 1×1 blank pixel |
| **Mill City Accounting Services LLC** | Lowell | **None** | **None** | Square link | 5 pages total, 2 one-sentence blog posts, no credentials claimed anywhere |
| **Fitzpatrick & Goguen CPAs P.C.** | Billerica | **None** | TaxDome — **and the whole site IS TaxDome** | In-portal only | Portal is not linked from a single page on the public site |
| **Dorfman & Dorfman, CPAs** | Wilmington | **None** | **None** | **None** | Zero `<script>`, `<iframe>` or `<form>` on the entire site. Self-signed SSL cert |
| **Thomas P. Craig, CPA, PC** (Mass Tax Pros) | Wilmington | 13 (CalcXML link-outs) | **None** | **None** | Everything frozen at 2013, footer copyright says 2013, WordPress placeholder post still live |

Three of the six have no calculators, no portal and no payments at all. The preservation problem is much smaller than it looked — it's really only Hickey.

---

## What we can honestly promise

**Calculators — rebuild natively, don't relink.** Financial calculators are standard math. Building them into the site directly means the firm owns them, they load instantly, they work on a phone, they're indexable by Google, and they survive leaving the vendor. That's strictly better than what any of these firms has today, where the click hands the visitor off to `calcxml.com` or `cchwebsites.com` with the firm's branding nowhere in sight. I'd build the ten or fifteen that actually get used rather than 147 that don't.

**Portals and payments — preserve verbatim.** These are external URLs. Hickey's `securefirmportal.com/Account/Login/4700`, Mill City's Square checkout, Goguen's TaxDome login. They carry over as links with zero risk, and I'd fix the two that are broken.

**Syndicated articles — cannot carry, and shouldn't.** What KPW got instead was a set of genuine plain-English guides written for that firm. That's the honest replacement, and it's the part that actually earns search traffic.

---

## Two things that change the plan

### Goguen is not a normal rebuild

`www.bgoguen.com` is a CNAME to `briangoguenpc.cd.taxdome.com`. Their marketing site and their client portal are the same product on the same hostname. Replacing the website means repointing DNS, which takes the portal login down with it unless the portal moves to a subdomain first — a change their clients would have to be told about mid-engagement.

That's not a reason to skip them, but it is a reason not to pitch them the same way. Their real problem is smaller and cheaper to fix anyway: **the portal isn't linked from anywhere on their public site.** Also worth knowing before you write to them — the firm renamed from Brian D. Goguen, P.C. to Fitzpatrick & Goguen CPAs P.C., and the top Google result for their domain is still an old-brand PDF.

### Four of the six publish no personal email addresses

| Firm | Addresses found | Pattern inferable? | MX |
|---|---|---|---|
| Hickey | `info@hickeycpa.com` only | **No** | Google |
| Carella | `CMCCPA@carellacpa.com` only (initials+CPA, obfuscated in JS) | **No** | USA.net |
| Mill City | `scott@millcityaccounting.com` | Yes — `firstname@` | Microsoft 365 |
| Goguen | `office@bgoguen.com` only | **No** | Microsoft 365 |
| Dorfman | `estee@dorfman-cpas.com` | Yes — `firstname@` | Microsoft 365 |
| Mass Tax Pros | `info@tpc-cpa.com` — **different domain from the website** | **No** | Proofpoint |

KPW worked because we had a confirmed pattern and seven named partners. Here, four firms give us one role inbox each. Guessing addresses at these volumes buys bounces, and bounces cost you sender reputation on a subdomain you've only just started warming.

Two specifics worth planning around. Mass Tax Pros sits behind **Proofpoint Essentials**, which is the most aggressive filter in this group — cold mail with a link is a coin flip there. And **Dorfman and Mass Tax Pros are both in Wilmington**, small enough that two near-identical pitches landing the same week is a real risk; those two should be separated by at least a fortnight.

---

## Suggested build order

Ordered by the strength of the pitch, not by ease.

1. **Thomas P. Craig / Mass Tax Pros** — a site publicly frozen at 2013, with a live WordPress placeholder post reading "This post will be deleted when the Mass Tax Pros write their first blog post." Thirteen years. The 13 calculators rebuild natively and one of them currently points at the wrong calculator entirely.
2. **James L. Hickey** — the strongest single finding in the batch: no HTTPS anywhere, with a portal password field embedded in the header of all 68 pages. Also a service page that reads "This is filler text." ten times, and a "Dirty Dozen" scams page still showing the IRS's 2015 list. This is the one where preservation work is real: 147 calculators, a portal, and PayPal.
3. **Charles M. Carella** — typing `https://` gets a full browser security warning because the certificate belongs to Wolters Kluwer. No portal, no payments, no named people, and the logo is a blank pixel.
4. **Dorfman & Dorfman** — self-signed certificate, untouched since August 2020, and an abandoned contact-form label with no form attached. Nothing to preserve, so it's the fastest build.
5. **Mill City Accounting** — newest and least broken. Five pages, no credentials stated anywhere, blog abandoned since 2019. Lowest urgency but easiest yes: sole practitioner, no partner committee.
6. **Fitzpatrick & Goguen** — hold until the DNS question above is answered.

---

## Decisions I need from you

1. **Calculators: rebuild natively, or link out to the existing vendor ones?** I recommend native. It costs me build time and it's the single biggest quality gap between your build and theirs.
2. **Do we send to role inboxes only where that's all we have?** The alternative is guessing, which I'd advise against.
3. **Does $997 still hold** where the build includes a rebuilt calculator suite and portal wiring? Hickey is materially more work than Dorfman.
4. **Goguen — hold, or pitch the narrower "your portal isn't linked" angle?**

---

## Notes for the build

Each firm gets an original logo designed from scratch, presented as a proposal and labelled as such — same posture as KPW, where the mark was never passed off as their existing one. Carella and Dorfman have no usable mark at all, so there's a clean slate.

Every build carries the same demo-notice strips top and bottom, the same private `noindex` posture, and has to clear the same gates: QA, contrast across all pairs, both layout gates, and screenshot capture at 390 and 1440.
