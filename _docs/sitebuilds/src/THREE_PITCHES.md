# Three pitches — six firms, segmented by what's actually wrong

The audit sorted these firms into three genuinely different problems, so three pitches rather than three arbitrary copy variants. Same structure as KPW throughout: multi-send disclosure up front, one verifiable finding doing the work, $997, no manufactured deadline, signed Matt | ScaleLocal.

| Pitch | Firms | The hook |
|---|---|---|
| **A — Not Secure** | Hickey, Carella, Dorfman | Their site fails HTTPS. A CPA site collecting client data over plain HTTP. |
| **B — Frozen** | Mass Tax Pros | Publicly frozen at 2013, with a live WordPress placeholder post. |
| **C — Invisible** | Mill City, Fitzpatrick & Goguen | Nothing is broken. The problem is what isn't there. |

Every claim below was verified live on 2026-07-30. **Re-verify the specific finding the morning each one sends** — these are accountants, they will check, and being wrong once costs the sequence.

---

# PITCH A — "Not Secure"

**For:** James L. Hickey CPA PC · Charles M. Carella, CPA · Dorfman & Dorfman, CPAs
**Why it works:** the prospect can confirm it in five seconds by typing their own domain with `https://`.

Each firm fails differently, so the second paragraph swaps. Everything else holds.

### Step 1 — Day 0

**Subject:** Your site says "Not Secure"

```
{{first_name}} —

Before anything else: I sent this same message to everyone at the firm whose
address I could find. From the outside I couldn't tell who owns a decision like
this, and I'd rather say that plainly than guess wrong.

[FINDING — see per-firm variants below]

I rebuilt your site. It's finished, it's private, and you can look at it now:

[DEMO URL]

[PRESERVED — see per-firm variants below]

$997 one time. No monthly fee, no maintenance contract, nothing recurring. That
price is low because the work is already done — there's no discovery phase to
bill you for and no revision cycle.

Reply and I'll walk you through it. If it isn't for you, two more notes at most
and then I'll leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

### Per-firm FINDING paragraph

**Hickey** — the strongest of the three:
> Type `https://hickeycpa.com` into a browser and nothing loads. Your site only answers on plain http, which means every visitor sees "Not secure" in the address bar. That matters more for you than for most businesses, because the client portal login sits in the header of all 68 pages — so the password field is on an unencrypted page, sitewide. While I was in there I also noticed your portal's "register here" link is dead, so new clients can't create an account at all.

**Carella:**
> Type `https://carellacpa.com` into a browser and you get a full-page security warning before you can reach your own site. The certificate being served belongs to Wolters Kluwer, not to you — so any client who follows an https link, or whose browser upgrades automatically, hits a red screen first. Your appointment form is collecting names, emails and phone numbers over an unencrypted connection.

**Dorfman:**
> Type `https://dorfman-cpas.com` and every browser will warn the visitor away — the certificate is self-signed, which browsers treat as no certificate at all. I checked the public certificate logs and no trusted certificate has ever been issued for the domain.

### Per-firm PRESERVED paragraph

**Hickey** — the one with real preservation work:
> Everything that works today still works. Your client portal login and the PayPal payment page are wired in exactly as they are. The calculators are the one thing I changed on purpose: yours currently hand the visitor off to calcxml.com, on the website vendor's licence, with your name nowhere on the page. I rebuilt them to run on your own site instead — they load instantly, they work on a phone, Google can index them, and they don't disappear if you ever leave your website vendor.

**Carella:**
> Your forty calculators currently open a pop-up on cchwebsites.com — Wolters Kluwer's domain, on Wolters Kluwer's licence, with your firm's name nowhere on the page. I rebuilt the ones people actually use so they run on your own site: instant, mobile, indexable by Google, and yours to keep.

**Dorfman:**
> I added the things the current site doesn't have — a working contact form, a map, and a set of financial calculators that run on your own pages rather than linking out to somebody else's.

### Step 2 — Day 5

**Subject:** One more thing on the site

Hickey:
```
{{first_name}} —

Following up on the rebuild I sent, but this stands on its own.

Your "Services For Individuals" page is live right now and its entire contents
are the words "This is filler text." repeated ten times. It's linked from your
own sitemap.

Two others are empty shells — the Business Services and Tax Services pages
contain a heading and nothing else. And your "Dirty Dozen" tax scams page, which
sits in the main navigation, is showing the IRS list for 2015.

Worth fixing regardless of whether you ever reply to me.

[DEMO URL]

Still $997, still nothing monthly.

— Matt | ScaleLocal
```

Carella:
```
{{first_name}} —

Following up on the rebuild, but this part stands on its own.

Your logo file is a blank pixel. The image the site loads in the header is a
43-byte transparent 1×1 GIF, so the firm's branding renders as plain text on
every page. It's been that way since the site was last touched.

Your Links page also points clients at two dead addresses — the Massachusetts
DOR and Secretary of State links both go to hostnames that no longer exist.

Worth ten minutes regardless.

[DEMO URL]

— Matt | ScaleLocal
```

Dorfman:
```
{{first_name}} —

Following up on the rebuild, but this stands on its own.

Your contact page has a form label on it with no form attached — the input was
removed or never finished, so the only way to reach you from the site is the
mailto link. Two of the five links on your Resources page also land on the
Mass.gov homepage rather than the Department of Revenue and the Attorney
General, because they use query strings from a version of Mass.gov retired
in 2017.

The site hasn't been edited since August 2020.

[DEMO URL]

— Matt | ScaleLocal
```

### Step 3 — Day 12

**Subject:** Last one from me

```
{{first_name}} —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire and I'm
not going to invent a deadline for it.

[DEMO URL]

$997, once. I deploy it to your domain — with a proper certificate — and hand
it over. After that you owe me nothing.

— Matt | ScaleLocal
```

---

# PITCH B — "Frozen"

**For:** Thomas P. Craig, CPA, PC (Mass Tax Pros)
**Note:** their mail runs through Proofpoint Essentials, the most aggressive filter in this batch. Their published address is `info@tpc-cpa.com` — a different domain from the website.

### Step 1 — Day 0

**Subject:** The placeholder post

```
{{first_name}} —

Before anything else: I sent this to every address I could find for the firm,
because I couldn't tell from outside who owns a decision like this.

There's a page live on masstaxpros.com right now whose entire text reads: "This
post will be deleted when the Mass Tax Pros write their first blog post."

It's dated February 2013. It's in your sitemap, so Google indexes it.

That's the site in miniature. Every page was last edited in 2013 — the footer
still says "Copyright 2013," and your team page says Tom has been practising
"approximately 15 years," which was written thirteen years ago.

I rebuilt it. Finished, private, look at it now:

[DEMO URL]

Your thirteen calculators came across, but rebuilt to run on your own site
instead of linking out to calcxml.com. Worth knowing: the one currently labelled
"Should I lease or buy and auto" points at the life insurance calculator. That's
fixed too.

$997 one time. Nothing monthly, no maintenance contract. The price is low
because the work is already done.

Reply and I'll walk you through it. Otherwise, two more notes and I'm gone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

### Step 2 — Day 5

**Subject:** Two dead links on your Resources page

```
{{first_name}} —

Following up, but this one stands alone.

Two of the links on your Resources page are dead. The "Apply for an EIN Online"
link returns a 404 — the IRS changed that URL. And the Record Retention Guide
PDF you point clients to has been gone from cpa.net for years.

There's also a feedback widget loading on your contact and blog pages from
justellus.com that returns a 404 — the script is dead, so the blog page still
tells visitors to "click the below box" when there's no box.

None of that costs anything to fix. Worth doing whether or not you reply.

[DEMO URL]

Still $997, still nothing monthly.

— Matt | ScaleLocal
```

### Step 3 — Day 12

**Subject:** Last one from me

```
{{first_name}} —

Last note.

Site's finished, sitting on a private link, no expiry and no deadline from me.

[DEMO URL]

$997 once, deployed to whatever domain you want. Then you owe me nothing.

Twenty-five years of practice deserves a site that isn't dated 2013.

— Matt | ScaleLocal
```

---

# PITCH C — "Invisible"

**For:** Mill City Accounting Services LLC · Fitzpatrick & Goguen CPAs P.C.
**Why it's different:** neither site is broken. Both are reasonably modern. The pitch can't be "yours is falling apart" — it would be untrue and they'd know it. So it's about what a visitor can't find.

**Goguen carries a constraint:** `www.bgoguen.com` is a CNAME to TaxDome, so their website and client portal are the same hostname. Do not pitch a full domain replacement — pitch the narrower fix.

### Step 1 — Day 0 — Mill City

**Subject:** Your site doesn't say you're qualified

```
Scott —

Straight to it: nowhere on millcityaccounting.com does it say what you're
licensed or qualified to do. The About page tells a good story — UMass Lowell,
eleven years at a Cambridge firm, quick-serve restaurant and rental real estate
clients, out on your own since 2018 — and then stops short of the part a
prospect is actually looking for.

Someone comparing three accountants closes the tab at that point. Not because
you're not qualified, but because they can't tell.

I rebuilt the site. It's finished and private:

[DEMO URL]

Five pages became a proper site: the restaurant and rental-property specialisms
each get their own page, and there's a set of financial calculators that run
directly on your pages. Your Square payment link is wired in exactly as it is.

$997 one time. Nothing monthly, no contract. The work's already done, which is
why it's that number.

Reply and I'll walk you through it, or tell me it's not for you and I'll stop.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

### Step 1 — Day 0 — Fitzpatrick & Goguen

**Subject:** Your client portal isn't linked from your website

```
{{first_name}} —

Before anything else: I sent this to the office address because it's the only
one published, so apologies if it lands with the wrong person.

Your TaxDome portal at bgoguen.com/login works and it's fully branded. But there
is no link to it from anywhere on your website — not the homepage, not the
footer, not the Contact page. A client can only get there if they already know
the URL or dig out an old email from you.

Every one of those is a phone call to your office that didn't need to happen.

Two smaller things while I was looking. The top Google result for your domain
isn't your homepage — it's a PDF newsletter still branded "Brian D. Goguen,
P.C.," so the first thing a searcher sees is the name you moved on from. And
your footer links one LinkedIn company page while your newsletter links a
different one.

I rebuilt the marketing site:

[DEMO URL]

One thing I want to flag honestly rather than sell around: your website and your
portal are the same TaxDome hostname, so this isn't a simple swap — the portal
would need to move to its own subdomain first, and your clients would need to be
told. That's a real conversation, not a footnote, and it's why I'd rather raise
it now than after you'd paid me.

$997 one time, nothing monthly.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

### Step 2 — Day 5 — both

Mill City:
```
Scott —

Following up on the site, but this stands alone.

Your Reviews page loads empty — the widget ships with no reviews in it, so
anyone clicking "Reviews" in your nav gets a blank page. That's worse than not
having the page.

Your blog has two posts. The newer one is a single sentence; the older is from
2019 and says the ACA mandate penalty "was eliminated this year."

Neither costs anything to fix.

[DEMO URL]

— Matt | ScaleLocal
```

Goguen:
```
{{first_name}} —

Following up once, then I'll leave it.

The transition letter on your Updates page is a scanned image with no text
layer — so it can't be searched, selected, read by a screen reader, or indexed.
Clients on a phone will struggle with it.

The same page lists a "2023 Client Tax Organizer Letter" linking to a file named
Organizer Letter 2024.pdf, which is the kind of thing that generates a phone
call during the worst week of your year.

[DEMO URL]

— Matt | ScaleLocal
```

### Step 3 — Day 12 — both

```
{{first_name}} —

Last note, as promised.

The site's finished and sitting on a private link. No expiry, no deadline
invented by me.

[DEMO URL]

$997 once. I deploy it wherever you want and hand it over.

— Matt | ScaleLocal
```

---

## Sending notes across all three

**Wilmington.** Dorfman and Mass Tax Pros are both in Wilmington. Separate those two by at least a fortnight — a town that size, partners talk.

**Tewksbury.** Hickey is in Tewksbury, where your own business certificate is filed. If that ever comes up in conversation, being local is an asset, but don't lead with it in cold copy — it reads as a small-world coincidence you're leveraging.

**Reply-stop.** Where a firm has multiple addresses, a reply from any of them must halt every remaining send to all of them.

**What we can't say.** No claim that we preserved syndicated article libraries — Hickey's ~249 guides and Carella's newsletters are the vendors', not the firms', and don't transfer. If a prospect asks, the honest answer is that we replaced them with guides written for their firm, which is what earns search traffic anyway.
