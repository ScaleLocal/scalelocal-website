# Six Outreach Campaigns — Hickey, Carella, Mill City, Goguen, Dorfman, Mass Tax Pros

**Product:** One website. Built. $997 one time. Nothing monthly, nothing recurring, nothing else pitched.
**Sender:** Matt | ScaleLocal — `matt@scalelocal.net`. No persona, no surname.
**Structure per firm:** four touches, delays **0 / 5 / 7 / 28** days. Mirrors `smartlead_create_kpw.py`.
**Footer on every email, without exception:**

```
ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

All facts in this document were verified live on **2026-07-31** unless stated otherwise. Page counts were counted with `find out/<slug> -name '*.html' | wc -l` on 2026-07-31 and are in the table below. The KPW campaign shipped saying "thirty-four pages" against an actual count of 21; that is why every number here was counted rather than remembered.

| Firm | slug | pages counted | demo |
|---|---|---|---|
| James L. Hickey, CPA PC | `hickeycpa` | **35** | `https://www.scalelocal.net/test-builds/hickeycpa/index.html` |
| Charles M. Carella, CPA | `carellacpa` | **25** | `https://www.scalelocal.net/test-builds/carellacpa/index.html` |
| Mill City Accounting Services LLC | `millcityaccounting` | **12** | `https://www.scalelocal.net/test-builds/millcityaccounting/index.html` |
| Fitzpatrick & Goguen CPAs P.C. | `bgoguen` | **17** | `https://www.scalelocal.net/test-builds/bgoguen/index.html` |
| Dorfman & Dorfman, CPAs | `dorfmancpas` | **13** | `https://www.scalelocal.net/test-builds/dorfmancpas/index.html` |
| Thomas P. Craig, CPA, PC (Mass Tax Pros) | `masstaxpros` | **20** | `https://www.scalelocal.net/test-builds/masstaxpros/index.html` |

All six demo URLs returned HTTP 200 on 2026-07-31.

---

# WHAT I COULD NOT VERIFY, AND THEREFORE LEFT OUT

Read this section before sending anything.

**1. Goguen's email address — a genuine conflict.**
`research/bgoguen.md` (verified 2026-07-30) records the firm inbox as **office@bgoguen.com**. The built site at `out/bgoguen/` uses `mailto:office@bgoguen.com` throughout. But bgoguen.com sits behind a Cloudflare challenge that blocks direct fetching, and reading the live Contact and Our-Services pages through a rendering fetch on 2026-07-31 returned the local part as **info**, not **office**, on both pages independently. One of the two is wrong and I cannot tell which from here.
**Action before send:** open `https://www.bgoguen.com/Contact/` in a browser, read the address, and use that one. I have listed `info@bgoguen.com` below as the address observed today, with `office@bgoguen.com` as the alternate. **Do not send to both** — one will bounce, and a bounce on a domain you are warming is not worth the guess. This is the only recipient in the batch I am not certain of.

**2. No second address at any of the six firms.**
Every one of these firms publishes exactly one email address. There is no confirmed personal-address pattern at any of them, so there is nobody to add. KPW worked because seven partners and a confirmed `FInitialLastname@` pattern existed. Nothing comparable exists here. I have not guessed a single address. That also means the KPW touch-1 line about "I sent this to every partner" does not apply anywhere in this batch — nobody is getting more than one message. Where the address is a role inbox I say so plainly instead, which is the same posture.

**3. Founding years, staff counts, years of experience.**
Not claimed for Hickey (no founding year exists on their site), Carella (no founding year, no named person at all), Goguen (no founding year on the current site), or Mass Tax Pros (their site's own experience figures are stale and are named as a defect rather than repeated). Only used where the firm publishes it: Mill City "since 2018", Dorfman "2008" and Dorfman's firm-level "over 30 years of public accounting experience", both of which appear on their own pages today.

**4. Credentials deliberately not claimed.**
**Joseph W. Brine (Mass Tax Pros) is never described as a CPA** anywhere in this copy. **Scott Marchlik (Mill City) is never described as a CPA or an EA** — his own site claims no credential, and the Mill City copy says "accounting firm", never "CPA firm". Dana Reardon, Sean Malone and Monirina Kim at Goguen are never given credentials. Brian Goguen is never given CFP.

**5. Features not claimed because the built sites do not have them.**
No calculators are claimed for **Goguen, Dorfman or Mill City** — those three builds deliberately have none, and each email says so out loud rather than quietly omitting it. No client portal is claimed for Carella, Mill City, Dorfman or Mass Tax Pros. No online payment is claimed for Carella, Goguen, Dorfman or Mass Tax Pros. Calculator counts in the copy are counted from `out/<slug>/calculators/`: Hickey 8, Carella 7, Mass Tax Pros 5.

**6. Things I found but did not put in an email.**
Carella's logo file being a blank pixel, Hickey's dead portal self-registration link, Goguen's old-brand PDF ranking in Google, and Dorfman's two retired Mass.gov resource links are all in the research but are not used — three defects per email is already the ceiling before it reads as an audit report rather than a note. The mass.gov links in the Dorfman and Mass Tax Pros builds return 403 to an automated fetch, which is bot-blocking rather than a dead link, but because I could not confirm them with a clean 200 I make no "every link checked" claim in any email.

---
---

# 1. James L. Hickey, CPA PC — Tewksbury, MA

**Campaign name:** `ScaleLocal - Hickey_Tewksbury_2026-08`
**Demo:** `https://www.scalelocal.net/test-builds/hickeycpa/index.html`
**Pages built:** 35 (counted 2026-07-31)

## Recipients

| Address | Basis |
|---|---|
| `info@hickeycpa.com` | **Verified 2026-07-31.** Appears as `mailto:info@hickeycpa.com` in the footer of every page fetched on hickeycpa.com. The visible text is deliberately broken up ("info@hi c keycpa.com") as spam obfuscation; the underlying mailto is clean. |

**This firm publishes only one general inbox.** No personal address exists anywhere on the site. Exactly one person is named on the entire site — James L. Hickey — with no title, no bio, no photo and no team page. Merge field for the greeting: `Whoever handles the website`.

## The hook — verified

**Claim:** 147 calculators running on the website vendor's CalcXML license, opening in a bare window away from the firm's own pages; the pay page is a PayPal form.

**Evidence, gathered 2026-07-31:**
- `hickeycpa.com/calc-section.php` lists 13 categories. Fetching each with `?id=N&category=...` and counting distinct `calcloader.php?calc=` targets gives: Cash Flow 12, College 8, Credit 11, Home and Mortgage 14, Insurance 11, Investment 15, Paycheck and Benefits 12, Qualified Plans 14, Retirement 10, Saving 10, Taxation 13, Auto 8, Business 9. **Total 147.** Exact.
- Each calculator link is `<a onclick="window.open(this.href,'_blank');return false;" href="calcloader.php?calc=hom01" target="_blank">`.
- `calcloader.php?calc=hom01` returns a bare document whose only content is `<script src='https://www.calcxml.com/scripts/loadCalc.js?calcTarget=hom01&embed=2&skn=481'></script>` plus an empty `<div id='calc'>`. It also carries `<meta name="robots" content="noindex, nofollow">`. **Skin 481 is the website vendor's CalcXML license** — the identical skin ID appears on Mass Tax Pros' calculator links, a different firm on the same website vendor.
- `paymyfee.php` contains `<form action="https://www.paypal.com/cgi-bin/webscr" method="post">`. Confirmed a form, not a link.

**Supporting findings, same date:**
- `https://www.hickeycpa.com/` and `https://hickeycpa.com/` both fail: `write:errno=104`, `no peer certificate available`. **The site has no HTTPS at all.** `http://` serves normally.
- Every page fetched (home, paymyfee, calc-section, sitemap, a calculator category page) contains a header form with `name="Username"` and `name="Password"` posting to `https://www.securefirmportal.com/Account/Login/4700`. A password box on a page that browsers already mark "Not secure".
- `firmprofile.php` contains: "Our firm is one of the leading firms in the Tewksbury and Merrimack Valley areas."

## What the build actually has (checked in `out/hickeycpa/`)

35 pages. 8 native calculator pages plus an index, with no reference to calcxml.com or cchwebsites.com anywhere in the build. `client-portal.html` and a header, footer and floating-panel link to their real `https://www.securefirmportal.com/Account/Login/4700`. `pay.html` explaining check, in person, and card. Floating "Let's connect" panel carrying click-to-dial `tel:+19788518945`, click-to-email `info@hickeycpa.com`, appointment request, portal and pay. `AccountingService` / `PostalAddress` JSON-LD. Embedded interactive Google map on `index.html` and `contact.html`.

---

## EMAIL 1 — Day 0

**Subject:** I built something for James L. Hickey, CPA PC

```
Whoever handles the website —

info@hickeycpa.com is the only address published anywhere on your site, so
this is going to the front desk. If a decision like this belongs with someone
else, please pass it along — I'd rather say that plainly than guess wrong.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/hickeycpa/index.html

Click around before you read the rest of this. It's the whole practice — tax
preparation and planning, the IRS problem resolution work, small business
services, QuickBooks, estate planning and elder care, and the Tewksbury office
with a map on it.

What you're looking at:

- 100% designed from scratch by ScaleLocal — thirty-five pages, nothing
  templated, written from your own published material
- Your existing client portal wired in — the same securefirmportal.com login
  you use now, in the header, in the footer, and in a panel that follows the
  visitor down every page
- A page that explains how the office takes payment: by check, in person, or
  by card
- Eight financial calculators built into the site itself, on your pages, under
  your name
- Call, email and appointment-request tools on every page
- SEO backend built for Google indexing — structured data, clean markup, an
  interactive Google map on the home and contact pages
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

One thing worth saying before you ask: the logo on the demo is a mark I drew
as a proposal. It isn't yours and I'm not pretending it is.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 2 — Day 5

**Subject:** Your 147 calculators belong to your website vendor

```
Whoever handles the website —

Following up on the site I sent, but this part stands on its own and costs you
nothing to act on.

You have 147 financial calculators on hickeycpa.com. I counted them across all
thirteen categories this week. Not one of them is yours.

Click any of them — "How Much Home Can I Afford?" under Home and Mortgage will
do — and the page opens /calcloader.php, which loads a script from calcxml.com
carrying skn=481. That's CalcXML's calculator on skin 481, which is your
website vendor's license rather than the firm's. The window it opens is bare:
no header, no navigation, no phone number, nothing that says James L. Hickey.
It's also tagged noindex, nofollow, so none of those 147 pages can ever appear
in a Google result.

So you have 147 pages of genuinely useful content that carry none of your
branding, cannot be found in search, and stop working the day you leave the
vendor.

Two other things while I'm in there.

hickeycpa.com has no HTTPS at all. Typing the secure address resets the
connection — there is no certificate to fail, there's nothing listening. So
every visitor gets plain http and every modern browser marks the firm "Not
secure" in the address bar. And the header of every page carries a client
portal box asking for an email address and a password. That's a password field
sitting on a page browsers already flag.

Your pay-my-fee page is a PayPal form. That works, but a form is the only
thing on it — there's nothing telling a client they could also mail a check or
pay at the office, which for a lot of your clients is what they'd rather do.

The build I sent has eight calculators living on your own indexable pages with
your name and number on them, the portal as a link rather than a password box
on an insecure page, and a payment page that explains all three routes.

https://www.scalelocal.net/test-builds/hickeycpa/index.html

Still $997, still nothing monthly. But the HTTPS thing is worth fixing whatever
you decide about me — your host can usually do it in an afternoon.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 3 — Day 7

**Subject:** Last one from me

```
Whoever handles the website —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/hickeycpa/index.html

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

Your firm profile says you're one of the leading firms in Tewksbury and the
Merrimack Valley. I live in Tewksbury. I'd never have guessed it from the
website.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 4 — Day 28

**Subject:** Still have the Hickey site on file

```
Whoever handles the website —

A few weeks back I sent over a website I'd built for the firm. You didn't take
it up, which is fine.

The build is still on file, still $997, and I can have it live on your domain
in a day. If you'd rather I deleted the file, say so and it's gone — I'll
confirm when it is.

Either way, this is the last you'll hear from me.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---
---

# 2. Charles M. Carella, CPA — North Billerica, MA

**Campaign name:** `ScaleLocal - Carella_NorthBillerica_2026-08`
**Demo:** `https://www.scalelocal.net/test-builds/carellacpa/index.html`
**Pages built:** 25 (counted 2026-07-31)

## Recipients

| Address | Basis |
|---|---|
| `CMCCPA@carellacpa.com` | **Verified 2026-07-31, decoded from the firm's own page.** |

The address is hidden on `contact_us.html` behind Obfuscapery, a JS/PHP obfuscator. I decoded it the way a browser does: POST the on-page token to `cch_js/obfuscapery-v2.inc.php`, POST the host to `cch_js/resolve_domain.php` for the key, XOR-decode. The decoded payload declares a count of **1** — the firm publishes exactly one address — and yields `CMCCPA@CARELLACPA.COM`. Send in lower case; it is case-insensitive at the mailbox.

**This firm publishes only one general inbox, and names no individual anywhere on the site.** There is no team page in the navigation. Merge field for the greeting: leave blank and use the neutral opener below.

## The hook — verified

**Claim:** the `tel:` link on the contact page is malformed — it embeds "ext.11" inside the URI, so tapping it on a phone misdials. 40 calculators are Wolters Kluwer pop-outs on a vendor license.

**Evidence, gathered 2026-07-31:**
- `carellacpa.com/contact_us.html` contains, verbatim:
  `Main Number<a href="tel:9786636419ext.11"> (978) 663-6419 ext. 11</a>`
  The visible text is correct. The URI is `tel:9786636419ext.11`, which is not a dialable string.
- The same page also does this to the fax: `<a href="tel:9786637260"> (978) 663-7260</a>`. Tapping the fax number on a phone calls a fax machine.
- `financial_tools.html` contains **40 distinct calculator slugs**, every one wired as
  `<a href="javascript: void(0)" onclick="popup_app('https://www.cchwebsites.com/content/calculators/AutoPayoff.html');">`
  — a pop-out to Wolters Kluwer's servers on Wolters Kluwer's license.
- `https://www.carellacpa.com` serves a certificate whose subject is `C = US, ST = Illinois, L = Riverwoods, O = Wolters Kluwer United States Inc., CN = cchwebsites.com`, issued by DigiCert, valid 2026-07-07 to 2027-01-21. Valid certificate, wrong name — so a browser shows a full-page name-mismatch warning on the https address.
- `firm_profile.html` is two paragraphs of generic text naming nobody, and the page footer reads "Designed by CCH Site Builder".

## What the build actually has (checked in `out/carellacpa/`)

25 pages. 7 native calculator pages plus an index, no calcxml or cchwebsites references anywhere. `tel:+19786636419` with "ext. 11" shown beside it as text. Six situation pages: `self-employed`, `two-states`, `unfiled-years`, `irs-notice`, `new-business`, `financial-statements`. A `what-to-bring` page and a `questions` page. Floating "Let's connect" panel with click-to-dial, click-to-email `CMCCPA@carellacpa.com` and appointment request. **No portal and no payments** — the firm has neither. Full JSON-LD set including `FAQPage`, `Service`, `BreadcrumbList`, `WebSite`. Embedded interactive Google map on `index.html` and `contact.html`.

---

## EMAIL 1 — Day 0

**Subject:** I built something for Charles M. Carella, CPA

```
Hello —

CMCCPA@carellacpa.com is the only address published anywhere on carellacpa.com,
so this is going there. If the website belongs with someone else, please pass
it along.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/carellacpa/index.html

Click around before you read the rest of this. It's the whole office — tax
preparation and planning, bookkeeping, financial statements, consulting — and
the North Billerica office with a map on it.

What you're looking at:

- 100% designed from scratch by ScaleLocal — twenty-five pages, nothing
  templated, written from your own published material
- Seven financial calculators built into the site itself, on your own pages
  rather than someone else's popup
- Six pages written around the situations people actually call about: a first
  year self-employed, income in two states, years that never got filed, an IRS
  notice in the mail, needing a financial statement for a bank, starting a
  business
- A "what to bring" page, so a first appointment starts further along than it
  does now
- Call, email and appointment-request tools on every page
- SEO backend built for Google indexing — structured data, clean markup, an
  interactive Google map on the home and contact pages
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

No client portal and no online payment page, because you don't have either
today and I didn't want to sell you a system you'd then have to run.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

One thing worth saying before you ask: the logo on the demo is a mark I drew
as a proposal. It isn't yours and I'm not pretending it is.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 2 — Day 5

**Subject:** The phone link on your contact page misdials

```
Hello —

Following up on the site I sent, but this part stands on its own and costs you
nothing to act on.

On carellacpa.com/contact_us.html your main number is written up like this:

    <a href="tel:9786636419ext.11"> (978) 663-6419 ext. 11</a>

The part a person reads is right. The part a phone reads is not. "ext.11" is
inside the number itself, so a handset tapping that link isn't dialing
978-663-6419 and then waiting for an extension — it's trying to dial the whole
string as one number. On most phones that fails outright.

Which means anyone who finds you on a phone and taps the number doesn't reach
you. That's the majority of first contacts now, and it's the one moment where
they were already sold.

The fax on the same page has the same problem in reverse: it's also a tel:
link, so tapping "Fax (978) 663-7260" on a phone calls a fax machine.

Two other things while I'm on that site.

Your Financial Tools page carries forty calculators, and every one of them is
a popup_app() call out to cchwebsites.com — Wolters Kluwer's servers, on
Wolters Kluwer's license. The visitor leaves your site to use them and lands
somewhere that doesn't mention you at all. And typing https://www.carellacpa.com
produces a full-page browser security warning, because the certificate served
on that address belongs to cchwebsites.com. I pulled it this week: subject
CN = cchwebsites.com, organization Wolters Kluwer United States Inc. It's a
perfectly valid certificate. It just isn't yours.

In the build I sent, the number is written the way phones expect —
tel:+19786636419, with the extension shown next to it in text — and the seven
calculators live on your own domain.

https://www.scalelocal.net/test-builds/carellacpa/index.html

Still $997, still nothing monthly. But fix the tel: link either way. It's one
line of HTML and it is costing you calls right now.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 3 — Day 7

**Subject:** Last one from me

```
Hello —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/carellacpa/index.html

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

There is no page on carellacpa.com that says who you are. The Firm Profile is
two paragraphs that would fit any accountant in the country, and the footer
underneath them credits CCH Site Builder. Somebody choosing an accountant is
choosing a person. Yours is the only name on the door and the site never
introduces him.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 4 — Day 28

**Subject:** Still have the Carella site on file

```
Hello —

A few weeks back I sent over a website I'd built for the office. You didn't
take it up, which is fine.

The build is still on file, still $997, and I can have it live on your domain
in a day. If you'd rather I deleted the file, say so and it's gone — I'll
confirm when it is.

Either way, this is the last you'll hear from me.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---
---

# 3. Mill City Accounting Services LLC — Lowell, MA

**Campaign name:** `ScaleLocal - MillCity_Lowell_2026-08`
**Demo:** `https://www.scalelocal.net/test-builds/millcityaccounting/index.html`
**Pages built:** 12 (counted 2026-07-31)

## Recipients

| Name | Address | Basis |
|---|---|---|
| Scott Marchlik, Founder | `scott@millcityaccounting.com` | **Verified 2026-07-31.** Printed in plain text in the contact block on `millcityaccounting.com/contact-us`. |

**One address, and it reaches the founder directly.** Sole practitioner — no partner committee, no gatekeeper. Merge field: `Scott`.

**Never describe Scott Marchlik as a CPA or an EA.** His site claims no credential. The only "CPA" on the whole site refers to a former employer. Mill City is an accounting firm, not a CPA firm, and the copy below says so.

## The hook — verified

**Claim as briefed:** the site still shows a moved-from address (97 Central Street) alongside the current one; only five pages for a practice with two real specialisms.

**Verified — with one correction.** The old address is on the page, but it is not presented as a live address. It appears as a vacancy notice. The exact text on `millcityaccounting.com/contact-us`, 2026-07-31:

> "Please note...we vacated the 97 Central Street #403F, Lowell, MA location as of 01/01/2025."

It sits directly above the current address block (`10 Kearney Square #302, Lowell, Massachusetts 01852`). So the honest version of the hook — and the one used in the email below — is that a visitor reads two Lowell addresses on one contact page and has to work out which is live, nineteen months after the move. I have **not** written that they are advertising an address they don't occupy, because they are not.

**The rest, verified 2026-07-31:**
- The site is **five pages**: `/`, `/about-us`, `/reviews`, `/contact-us`, `/blog`. Those five are the entire navigation.
- `/blog` is in the main navigation and **has no posts on it** — the page renders the line "Tips on taxes, payroll, and accounting" and nothing beneath it.
- The two specialisms appear exactly once, on `/about-us`, inside a paragraph about a previous job: "Scott's primary clientele were quick-serve restaurant owners, along with rental real estate owners." They appear nowhere else on the site.
- Same page: "In the spring on 2018, Scott left his position as an accounting supervisor and decided to launch Mill City Accounting Services on his own."
- Site is built on GoDaddy Website Builder (the "Powered by" link on every page points at godaddy.com/websites/website-builder).
- Square payment link `https://square.link/u/1BBydiwq` returned 200.

## What the build actually has (checked in `out/millcityaccounting/`)

12 pages. **No calculators — deliberately, and the email says so.** Dedicated `restaurants.html` and `rentals.html`. Six service pages plus an index — tax preparation, tax planning, bookkeeping, payroll, new business consulting, notarization. The real Square link `https://square.link/u/1BBydiwq` carried over verbatim in the floating "Let's connect" panel, alongside click-to-dial `tel:+19789792904`, click-to-email `scott@millcityaccounting.com` and an appointment request. `OpeningHoursSpecification` in the JSON-LD carrying the published hours. Embedded interactive Google map on `index.html` and `contact.html`. Nothing anywhere in the build calls Scott a CPA or an EA, and `97 Central` appears nowhere in the build.

---

## EMAIL 1 — Day 0

**Subject:** I built something for Mill City Accounting

```
Scott —

scott@millcityaccounting.com is the address on your site, so this is coming
straight to you rather than to a front desk.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/millcityaccounting/index.html

Click around before you read the rest of this. It's twelve pages against the
five you have now, and two of them are the ones I think matter most: one on
quick-serve restaurants, one on rental property owners.

What you're looking at:

- 100% designed from scratch by ScaleLocal — twelve pages, nothing templated,
  written from your own published material
- A page each for quick-serve restaurants and rental real estate — the two
  client types your own bio names
- Separate pages for tax preparation, tax planning, bookkeeping, payroll, new
  business consulting and notarization
- Your Square link carried over exactly as it is — square.link/u/1BBydiwq — in
  a panel that follows the visitor down every page
- Click-to-call, click-to-email and an appointment request on every page, with
  your hours
- SEO backend built for Google indexing — structured data including your
  opening hours, clean markup, an interactive Google map on the home and
  contact pages
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

No calculators, and that's on purpose. A twelve-page site for a one-person
practice doesn't need them, and I'd rather every page you have earn its place.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

Two things worth saying before you ask. The logo on the demo is a mark I drew
as a proposal — it isn't yours. And I've described the practice exactly the way
your own site describes it: an accounting firm, not a CPA firm, with no letters
after your name. That was a deliberate choice, not an oversight.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 2 — Day 5

**Subject:** Two Lowell addresses on your contact page

```
Scott —

Following up on the site I sent, but this part stands on its own and costs you
nothing to act on.

Your contact page still carries this line:

    "Please note...we vacated the 97 Central Street #403F, Lowell, MA location
    as of 01/01/2025."

It sits directly above the 10 Kearney Square address. So the first thing a
new visitor reads on your contact page is a Lowell address you don't occupy,
and then a Lowell address you do. Someone skimming on a phone gets two
addresses for one firm and has to work out which is live. And anyone who
picked up the old address somewhere else now has it confirmed on your own
site, in your own words.

That notice earned its place in January 2025. Nineteen months on it's just
noise on the page where people decide whether to call you.

Two other things on the same site.

Your Blog is in the main navigation and the page has nothing on it — the line
"Tips on taxes, payroll, and accounting" and then blank space. An empty page in
the top nav reads worse than no page at all.

And the whole site is five pages: home, about, reviews, contact, blog. Quick-
serve restaurants and rental real estate — the two client types your bio names,
the two you actually know cold — get one sentence between them, buried in a
paragraph about a job you left in 2018. Someone in Lowell searching for an
accountant who understands restaurant books has no way to find that out.

The build I sent gives each of them a page. That's not decoration. Those are
the two searches worth winning in this city, and right now you're not in either
of them.

https://www.scalelocal.net/test-builds/millcityaccounting/index.html

Still $997, still nothing monthly. But delete the 97 Central line either way —
it's thirty seconds in the GoDaddy editor.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 3 — Day 7

**Subject:** Last one from me

```
Scott —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/millcityaccounting/index.html

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

You've been on your own since 2018 and you are the entire firm. The website is
the only version of you that's working while you're sitting with a client.
Right now it's five pages that could belong to anyone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 4 — Day 28

**Subject:** Still have the Mill City site on file

```
Scott —

A few weeks back I sent over a website I'd built for the firm. You didn't take
it up, which is fine.

The build is still on file, still $997, and I can have it live on your domain
in a day. If you'd rather I deleted the file, say so and it's gone — I'll
confirm when it is.

Either way, this is the last you'll hear from me.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---
---

# 4. Fitzpatrick & Goguen CPAs P.C. — Billerica, MA

**Campaign name:** `ScaleLocal - FitzpatrickGoguen_Billerica_2026-08`
**Demo:** `https://www.scalelocal.net/test-builds/bgoguen/index.html`
**Pages built:** 17 (counted 2026-07-31)

## Recipients

| Address | Basis |
|---|---|
| `info@bgoguen.com` | **Observed 2026-07-31** on both `/Contact/` and `/Our-Services/`. **See the conflict flagged at the top of this document.** |
| `office@bgoguen.com` | Alternate. Recorded in `research/bgoguen.md` on 2026-07-30 and used throughout the built site. |

**Confirm which one is right in a browser before sending. Send to one, not both.** The domain sits behind a Cloudflare challenge, which is why this could not be settled with a plain fetch. This is the only recipient in the batch I am not certain of.

No individual staff addresses are published on any page. Five people are named on the team page — Thomas L. Fitzpatrick IV, Brian D. Goguen, Dana Reardon, Sean Malone, Monirina Kim — with no address against any of them. Merge field for the greeting: leave blank and use the neutral opener.

## The hook — verified, and it is the strongest in the batch

**Claim:** they pay for a live TaxDome client portal at `https://www.bgoguen.com/login` and their website links to it from no page at all.

**Evidence, gathered 2026-07-31. Both halves confirmed.**

*The portal is live.* `https://www.bgoguen.com/login` renders a TaxDome login page carrying the Fitzpatrick & Goguen CPAs P.C. logo, with a CSRF token and a CSP nonce, and a full language/country selector. It is a working portal, not a parked URL.

*Nothing links to it.* I read all five public pages — `/`, `/Our-Services/`, `/Our-Team/`, `/Updates/`, `/Contact/`. That is the entire site. The complete set of outbound links across all five is:

- the five internal nav links to each other
- `https://us.aicpa.org/forthepublic`
- `https://www.naea.org/`
- `https://www.facebook.com/fitzpatrickgoguencpas`
- `https://www.linkedin.com/company/briangoguenpc`
- `https://taxdome.com` — TaxDome's own marketing site, from a "Powered By Taxdome" badge
- `https://news.resourcesforclients.com/?u=5J6SDptdpWBD&n=CU` (Updates page)
- three PDFs in `/gallery/`: the 2023 organizer letter, the 2024 year-end planning letter, the firm transition letter

**There is no link to `/login` on any of the five pages.** The only TaxDome link on the entire site points at TaxDome's own homepage rather than the firm's portal.

**Also verified 2026-07-31:** the firm now trades as Fitzpatrick & Goguen CPAs P.C., while the domain is still bgoguen.com and the LinkedIn company slug is still `/company/briangoguenpc`.

## What the build actually has (checked in `out/bgoguen/`)

17 pages. The real portal `https://www.bgoguen.com/login` linked from the header, the footer, the floating "Let's connect" panel, **and** a dedicated `client-portal.html` explaining what the portal is for. A page each for all five people. Bookkeeping, personal tax and business tax service pages. Two guides. Floating panel with click-to-dial `tel:+19786674595`, click-to-email, appointment request and the portal. `Person` / `Service` / `BreadcrumbList` / `AccountingService` JSON-LD. Embedded interactive Google map on `index.html` and `contact.html`. **No calculators — deliberately, and the email says so.**

**Known constraint, stated up front in Email 1:** `www.bgoguen.com` and the portal are the same TaxDome hostname, so a cutover is not a simple DNS swap. That is disclosed before any money changes hands rather than after.

---

## EMAIL 1 — Day 0

**Subject:** I built something for Fitzpatrick & Goguen

```
Hello —

The only address published on bgoguen.com is the office inbox, so this is
going there. If the website belongs with someone specific, please pass it
along.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/bgoguen/index.html

Click around before you read the rest of this. It's the whole firm —
bookkeeping, personal income tax, small business and non-profit tax — all five
of you with a page each, and the Concord Road office with a map on it.

What you're looking at:

- 100% designed from scratch by ScaleLocal — seventeen pages, nothing
  templated, written from your own published material
- Your TaxDome portal linked from the header, the footer, a panel that follows
  the visitor down every page, and a page of its own explaining what it's for
- A page for each of the five of you, written from your own bios
- Call, email and appointment-request tools on every page
- SEO backend built for Google indexing — structured data, clean markup, an
  interactive Google map on the home and contact pages
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

No calculators. Your site doesn't have any, and for a five-person firm I'd
rather the pages be about the work than about arithmetic widgets.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

Two things I'd rather say now than after you've paid me. The logo on the demo
is a mark I drew as a proposal — it isn't yours. And your marketing site and
your client portal currently sit on the same TaxDome hostname, so switching
sites is not a simple DNS change; the portal has to be dealt with first or
your clients lose their login mid-engagement. That's a real conversation and
I'd want to have it before anything goes live.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 2 — Day 5

**Subject:** Your clients cannot find your portal

```
Hello —

Following up on the site I sent, but this part stands on its own and costs you
nothing to act on. Honestly, it's worth more to you than the website is.

https://www.bgoguen.com/login is live. It's your TaxDome portal, it loads, it
carries your logo, it's ready to take a client right now.

Nothing on your website links to it.

I read all five of your pages this week — Home, Our Services, Our Team,
Updates, Contact. Between them they link out to AICPA, to NAEA, to your
Facebook page, to your LinkedIn page, to three PDFs in your gallery, to the
resourcesforclients newsletter, and to taxdome.com. That last one is TaxDome's
own marketing site, not yours.

There is no link to your login on any of the five pages.

So a client who wants to upload a W-2, sign something, or settle an invoice has
to already know the URL. If they don't, they email the office and somebody
types it out again. You are paying TaxDome every month for a portal that only
the clients who've been told twice can find.

The fix costs nothing and doesn't involve me. Add a "Client Login" item to your
navigation pointing at https://www.bgoguen.com/login. Do that today whether or
not you ever reply to this.

The build I sent has it in the header, in the footer, in a panel that follows
you down every page, and on a page of its own that explains what the portal is
for — documents, signatures, invoices — so a first-time client knows what
they're signing into before they sign into it.

https://www.scalelocal.net/test-builds/bgoguen/index.html

Still $997, still nothing monthly.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 3 — Day 7

**Subject:** Last one from me

```
Hello —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/bgoguen/index.html

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

The firm is Fitzpatrick & Goguen CPAs P.C. now. The domain still says bgoguen,
and the LinkedIn page is still /company/briangoguenpc. A new site is the one
moment you get to settle that in public, on purpose, rather than letting it
settle itself.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 4 — Day 28

**Subject:** Still have the Fitzpatrick & Goguen site on file

```
Hello —

A few weeks back I sent over a website I'd built for the firm. You didn't take
it up, which is fine.

The build is still on file, still $997, and I can have it live on your domain
in a day — with the portal question sorted out first, as I said at the time.
If you'd rather I deleted the file, say so and it's gone. I'll confirm when it
is.

Either way, this is the last you'll hear from me. If you only take one thing
from any of this, link the portal.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---
---

# 5. Dorfman & Dorfman, CPAs — Wilmington, MA

**Campaign name:** `ScaleLocal - Dorfman_Wilmington_2026-08`
**Demo:** `https://www.scalelocal.net/test-builds/dorfmancpas/index.html`
**Pages built:** 13 (counted 2026-07-31)

## Recipients

| Name | Address | Basis |
|---|---|---|
| Estee C. Dorfman, CPA, MSA | `estee@dorfman-cpas.com` | **Verified 2026-07-31.** I crawled all five pages of dorfman-cpas.com (`index`, `about-us`, `accounting`, `resources`, `contact-us`). It is the only email address on the entire site, appearing as a mailto on the homepage and in plain text in the contact block and site footer. |

**No address is published for Marvin H. Dorfman.** I did not guess one. Merge field: `Estee`.

## The hook — verified, and it is the most valuable finding in the batch

**Claim:** their HTTPS certificate is self-signed and expired 19 June 2025, so every visitor gets a full-page browser security warning before they see the site.

**Evidence, gathered 2026-07-31. Confirmed exactly as briefed.**

```
subject   = CN = dorfman-cpas.com
issuer    = CN = dorfman-cpas.com
notBefore = Jun 19 10:12:36 2024 GMT
notAfter  = Jun 19 10:12:36 2025 GMT
SAN       = dorfman-cpas.com, mail., www., cpanel., webmail., webdisk.,
            cpcontacts., cpcalendars., autodiscover.
```

Subject equals issuer, so it is self-signed — nothing vouches for it. It expired **19 June 2025**. `curl https://www.dorfman-cpas.com/` fails with `SSL certificate problem: self-signed certificate`; `http://` serves normally with a 200. The SAN list is the standard cPanel self-signed set, which is the tell for where the fix lives.

**Also verified 2026-07-31, from their own pages:**
- Homepage: "Dorfman & Dorfman, CPAs is a family-owned firm specializing in accounting and tax services for small businesses and individuals, with over 30 years of public accounting experience."
- Homepage: "When you visit us, your work isn't handed off to associates...it's handled by us personally."
- About: "Marvin was a sole practioner from 2004 until 2008 when he formed Dorfman & Dorfman, CPAs." And: "In 2008, she co-founded Dorfman & Dorfman, CPAs."
- About: Estee "was previously employed by the Financial Industry Regulatory Authority (formerly known as the National Association of Securities Dealers) as a Principal Examiner." That is one sentence, and it is the whole of it on their site.
- Footer on every page: "(781) 780-7069 Ext 11 • estee@dorfman-cpas.com".

## What the build actually has (checked in `out/dorfmancpas/`)

13 pages. **No calculators, no portal, no payments — deliberately, and the email says so.** A `regulatory-background.html` page built out from Estee's FINRA history, written to claim familiarity with the regulatory environment and not to claim broker-dealer audit work. A page each for Marvin and Estee. Four service pages plus an index. An FAQ and a resources page. Floating "Let's connect" panel with click-to-dial `tel:+17817807069`, the extension shown as text beside it, click-to-email `estee@dorfman-cpas.com`, and an appointment request. `Person` / `Service` / `BreadcrumbList` JSON-LD. Embedded interactive Google map on `contact.html`.

---

## EMAIL 1 — Day 0

**Subject:** I built something for Dorfman & Dorfman

```
Estee —

estee@dorfman-cpas.com is the only address published on dorfman-cpas.com, so
this is coming to you. If it belongs with Marvin, please pass it along.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/dorfmancpas/index.html

Click around before you read the rest of this. It's the whole practice — tax
returns, bookkeeping through to trial balance, payroll tax, review and
compilation — a page each for you and Marvin, and the Main Street office with
a map on it.

What you're looking at:

- 100% designed from scratch by ScaleLocal — thirteen pages, nothing templated,
  written from your own published material
- A page about your FINRA background and what it means for a client in or near
  the financial services world. On your current site that's one sentence. It's
  the most distinctive thing you have and it's the easiest thing to miss.
- A page each for you and Marvin
- Call, email and appointment-request tools on every page, with the number
  written so a phone actually dials it and the extension shown beside it
- SEO backend built for Google indexing — structured data, clean markup, an
  interactive Google map on the contact page
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

No calculators, no client portal, no payment system. You have none of those
today, and I didn't want to hand a two-person firm three more things to
maintain.

I've also kept the service list to exactly what your site says you do — the
six published services and nothing beyond them. There's no audit work anywhere
in the build, because nothing on your site says you perform audits.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

One thing worth saying before you ask: the logo on the demo is a mark I drew
as a proposal. It isn't yours and I'm not pretending it is.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 2 — Day 5

**Subject:** Your site shows a security warning before anyone sees it

```
Estee —

Following up on the site I sent, but this part matters more than the site does
and it costs you nothing to act on.

Anyone who reaches dorfman-cpas.com over a secure connection gets a full-page
browser security warning before they see a word of your site. Not a small
padlock icon — the whole red interstitial, the one that says the connection is
not private. Most people close the tab there and go back to the search results.

Here is exactly what's wrong. I pulled the certificate on
https://www.dorfman-cpas.com this week:

    subject:    CN = dorfman-cpas.com
    issuer:     CN = dorfman-cpas.com
    expired:    19 June 2025

Two problems in three lines. The subject and the issuer are the same name,
which means it's self-signed — nothing independent vouches for it, so no
browser will trust it. And it ran out on 19 June last year, so even a trusted
version of it would have stopped working thirteen months ago.

This isn't an edge case. Browsers have defaulted to trying the secure address
first for years now, so this is most of your traffic, including everyone who
clicks you from a Google result.

The fix is free and takes about ten minutes at your host, not at mine. The
extra names on that certificate — cpanel, webmail, webdisk, cpcontacts — are
the cPanel defaults, which means your hosting almost certainly has a one-click
Let's Encrypt option sitting in the SSL panel. It issues at no cost and renews
itself. You do not need me for this and you should not wait on me for it.

I'd have told you this even if I had nothing to sell. It's the single most
valuable thing anyone could tell you about that website right now.

The build I sent runs over a valid certificate, so there's no warning standing
in front of it.

https://www.scalelocal.net/test-builds/dorfmancpas/index.html

Still $997, still nothing monthly.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 3 — Day 7

**Subject:** Last one from me

```
Estee —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/dorfmancpas/index.html

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

Your own homepage makes the argument better than I can: the work isn't handed
off to associates, it's handled by the two of you personally. That's the whole
firm in one sentence, and it's been sitting behind a browser warning since June
of last year. Fix the certificate whatever you decide about me.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 4 — Day 28

**Subject:** Still have the Dorfman site on file

```
Estee —

A few weeks back I sent over a website I'd built for the firm. You didn't take
it up, which is fine.

The build is still on file, still $997, and I can have it live on your domain
in a day. If you'd rather I deleted the file, say so and it's gone — I'll
confirm when it is.

Either way, this is the last you'll hear from me. If you do one thing from all
of this, get the certificate replaced.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---
---

# 6. Thomas P. Craig, CPA, PC — Mass Tax Pros — Wilmington, MA

**Campaign name:** `ScaleLocal - MassTaxPros_Wilmington_2026-08`
**Demo:** `https://www.scalelocal.net/test-builds/masstaxpros/index.html`
**Pages built:** 20 (counted 2026-07-31)

## Recipients

| Address | Basis |
|---|---|
| `info@tpc-cpa.com` | **Verified 2026-07-31** on `masstaxpros.com/contact-us/`. It is the only address on the site — and note it is on a different domain from the website. |

**This firm publishes only one general inbox.** No personal addresses for Thomas P. Craig or Joseph W. Brine appear anywhere. Merge field for the greeting: leave blank and use the neutral opener.

**Joseph W. Brine is never called a CPA in any of this copy.** The Mass Tax Pros build and these emails describe no credential for him at all.

**Deliverability note carried over from the audit:** this domain sits behind Proofpoint, the most aggressive filter in the batch, and Dorfman is in the same town. **Separate the Dorfman and Mass Tax Pros sends by at least a fortnight.**

## The hook — verified

**Claim:** the site is content-frozen since 2013 — a placeholder blog post, a 2013 copyright footer, stale experience claims — plus one miswired calculator link.

**Evidence, gathered 2026-07-31. Every element confirmed.**

- **The blog.** `masstaxpros.com/tax-and-accounting-blog/` is in the main navigation and contains exactly one entry: title "The Mass Tax Pros", byline "Posted by admin on Feb 3, 2013 in Uncategorized | 0 comments", body text verbatim:
  > "This post will be deleted when the Mass Tax Pros write their first blog post."
- **The footer**, on every page: `Copyright 2013, Thomas P. Craig, CPA, PC | Heritage Commons 11 Middlesex Avenue, Suite 3, Wilmington, MA 01887 | P: 978-657-5272 | F: 978-657-7994`
- **The stale claims.** Homepage: "For a quarter century, people from all walks of life have entrusted us with improving the quality of their life." Team page: "Tom has been practicing as a licensed CPA for approximately 15 years." Both are counted from 2013 and neither has moved.
- **Asset dating.** Team photos are served from `/wp-content/uploads/2013/01/`.
- **The miswired calculator.** `masstaxpros.com/tax-accounting-resources/` lists 13 calculators, all raw link-outs to calcxml.com on `skn=481` — the website vendor's license, the same skin as another firm's site. Item 11 reads:

  | # | label | destination |
  |---|---|---|
  | 10 | How much life insurance do I need | `life-insurance-calculator?skn=481` |
  | **11** | **Should I lease or buy and auto** | **`life-insurance-calculator?skn=481`** |

  Identical URL, two rows apart. The label's own typo ("and auto") is theirs, quoted verbatim.
- **From their own team page**, usable: "In 2006 Joe and Tom formed Craig, Brine & Associates and today have incorporated the company into Thomas P Craig CPA PC." And the firm-level "more than 50 years of combined experience".

## What the build actually has (checked in `out/masstaxpros/`)

20 pages. 5 native calculator pages plus an index, no calcxml references anywhere in the build. A page each for Thomas P. Craig and Joseph W. Brine written from their own bios, with no credential asserted for Joe. A `representation.html` page. Income tax, financial services, QuickBooks and accounting service pages. An FAQ. A resources page pointing at current IRS and Massachusetts pages. Floating "Let's connect" panel with click-to-dial `tel:+19786575272`, click-to-email `info@tpc-cpa.com` and an appointment request. `FAQPage` / `Person` / `Service` / `BreadcrumbList` JSON-LD. Embedded interactive Google map on `contact.html`. **No portal and no online payments** — the firm has neither. **No copyright year anywhere in the footer**, and no experience figure anywhere in the copy, so there is nothing in the build that can go stale by sitting still.

---

## EMAIL 1 — Day 0

**Subject:** I built something for the Mass Tax Pros

```
Hello —

info@tpc-cpa.com is the only address published on masstaxpros.com, so this is
going there. If the website belongs with someone specific, please pass it
along. Worth mentioning while I'm here: that address is on a different domain
from the website, which is its own small friction for anyone trying to work out
whether they've reached the right firm.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/masstaxpros/index.html

Click around before you read the rest of this. It's the whole practice — income
tax, accounting, financial services, QuickBooks, IRS representation — a page
each for Tom and Joe, and the Heritage Commons office with a map on it.

What you're looking at:

- 100% designed from scratch by ScaleLocal — twenty pages, nothing templated,
  written from your own published material
- Five financial calculators built into the site itself, on your pages, under
  your name
- A page on IRS representation work
- A page each for Tom and Joe, written from your own bios
- A resources page pointing at current IRS and Massachusetts pages
- Call, email and appointment-request tools on every page
- SEO backend built for Google indexing — structured data, clean markup, an
  interactive Google map on the contact page
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

No client portal and no online payments. You have neither today and I didn't
want to sell you a system you'd then have to run.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

One thing worth saying before you ask: the logo on the demo is a mark I drew as
a proposal. It isn't yours and I'm not pretending it is.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 2 — Day 5

**Subject:** Your website has said 2013 for thirteen years

```
Hello —

Following up on the site I sent, but this part stands on its own and costs you
nothing to act on.

Your blog is in the main navigation. It has exactly one post on it. Here it is
in full:

    "The Mass Tax Pros"
    Posted by admin on Feb 3, 2013 in Uncategorized | 0 comments
    "This post will be deleted when the Mass Tax Pros write their first blog
    post."

That's the placeholder your site builder left behind when the site went up. It
has been sitting there, linked from your own navigation, ever since.

It isn't alone. The footer of every page reads "Copyright 2013, Thomas P.
Craig, CPA, PC". Your team photos are served out of /wp-content/uploads/2013/01/.
And two claims on the site are counted from that year and have never moved: the
homepage says "For a quarter century, people from all walks of life have
entrusted us," and Tom's bio says "Tom has been practicing as a licensed CPA for
approximately 15 years." Both were true when they were written. Neither is the
number you'd want a prospect reading now, and anyone who spots the copyright
date knows exactly why they're wrong.

One more, smaller and more concrete. On your resources page the link labeled
"Should I lease or buy and auto" points at:

    http://www.calcxml.com/calculators/life-insurance-calculator?skn=481

That's the same URL as the life insurance calculator two rows above it.
Somebody pasted the wrong line, and in thirteen years nobody has clicked it.
That's really the whole point — not that one link is wrong, but that nobody has
looked.

While I'm there: all thirteen of those calculators are link-outs to calcxml.com
on skin 481, which is your website vendor's license rather than yours. Every
one of them takes the visitor off masstaxpros.com to a page with your name
nowhere on it.

The build I sent has five calculators living on your own pages, and nothing in
it that goes stale by sitting still — no copyright year to forget, no
experience figure counted from a fixed point.

https://www.scalelocal.net/test-builds/masstaxpros/index.html

Still $997, still nothing monthly. But delete that placeholder post today
either way. It's one click and it's the first thing a careful client finds.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 3 — Day 7

**Subject:** Last one from me

```
Hello —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/masstaxpros/index.html

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

Your own team page says Craig, Brine & Associates was incorporated into Thomas
P. Craig, CPA, PC. The firm moved on. The website is still the theme, the
footer and the copyright line it launched with. Those two things should match.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## EMAIL 4 — Day 28

**Subject:** Still have the Mass Tax Pros site on file

```
Hello —

A few weeks back I sent over a website I'd built for the firm. You didn't take
it up, which is fine.

The build is still on file, still $997, and I can have it live on your domain
in a day. If you'd rather I deleted the file, say so and it's gone — I'll
confirm when it is.

Either way, this is the last you'll hear from me.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---
---

# SEQUENCE RULES — all six campaigns

**Re-verify every hook the morning it sends.** These are accountants and two of them are examiners by training. Everything in Email 2 was true on 2026-07-31. If any of it has been fixed by send day, cut that line rather than send a stale claim. Being wrong once costs the whole sequence. The Dorfman certificate and the Goguen portal link are both things a firm might fix in an afternoon after reading Email 1 — check those two in particular.

**One address per firm.** Nobody in this batch receives more than one message, so the KPW "a reply from any of the seven halts the rest" rule reduces to the ordinary one: any reply stops the remaining sends.

**Timing.** Tuesday through Thursday, 9–11 AM Eastern. All six firms are in Massachusetts, so unlike KPW the sender's clock and the recipient's are the same. Never Friday, never Monday, nothing during the week of September 15.

**Separate Dorfman and Mass Tax Pros by at least two weeks.** Both are in Wilmington, which is small enough that two near-identical cold pitches landing the same week get compared.

**Mass Tax Pros sits behind Proofpoint.** Cold mail carrying a link is a coin flip there. If deliverability matters more than reach, that campaign is the one to send last, after the others have built some sending history.

**Unsubscribe means immediate DNC and a clean exit, no last word.** "Not interested" is a DNC for this offer type, not a master DNC.

**Log every send and every reply before it goes out.**

## Before any of this sends

**The logo disclosure is in Email 1 for every firm.** On KPW it was a note-to-self about what to say when someone replied. Here it is in the email, because five of these six firms have either no usable mark or a mark I have replaced, and it is better said before they ask than after.

**Decide what "free deployment" covers before someone replies.** The copy promises deployment to a domain of their choosing and nothing recurring. Whether that includes repointing their existing DNS is a question you will get asked, and the answer needs to exist before it is.

**Goguen is not a normal cutover** and Email 1 says so. Their marketing site and their client portal are the same TaxDome hostname. Do not let that conversation start after money has changed hands.

**The demos are `noindex,nofollow`.** That has to come off at cutover or the new site launches invisible to Google.

**Deliverability.** Every one of these emails carries the demo URL, because the link is the pitch. If `matt@scalelocal.net` carries other sending reputation, warm a separate alias for link-bearing cold sends rather than mixing them.
