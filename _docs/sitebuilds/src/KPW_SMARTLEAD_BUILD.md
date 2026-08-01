# Smartlead build sheet — KPW campaign

**Campaign name:** `CPA_KPW_DownersGrove_2026-08`
**Leads:** `kpw_leads.csv` — 7 rows, all at kpwcpa.com
**Product:** one website, $997 one time, nothing recurring
**Demo:** https://www.scalelocal.net/test-builds/kpw-cpa/

> **Footer address set** — CMRA mailbox in Abington, MA. Company name only, no personal name. Campaign is created **paused**; nothing sends until you press start.

---

## Campaign settings

| Setting | Value | Why |
|---|---|---|
| Schedule | Tue / Wed / Thu, 9:00–11:00 AM, America/Chicago | KPW is in Downers Grove. Their timezone, not yours. |
| Sending gap | 15 min minimum | Seven near-identical emails hitting one domain in one burst is the fastest way to quarantine the whole firm. |
| Daily limit | Leave low — this is 7 leads total | No reason to touch your volume ceiling |
| Link tracking | **OFF** | Tracking rewrites the demo URL through a redirect domain. On a 7-lead campaign the data is worthless and the deliverability hit is real. |
| Open tracking | **OFF** | Adds a tracking pixel, buys you nothing at this volume |
| Stop on reply | ON | See the warning below |
| Stop on auto-reply | OFF | Out-of-office shouldn't kill the sequence |

**The reply-stop gotcha.** Reply detection in most sending tools is per-*lead*, not per-*domain*. If Ken Peterson replies on Wednesday, the other five partners can still receive step 2 on Friday — six partners getting a follow-up after one of them already started a conversation is the single worst outcome available here. Check whether your Smartlead plan does company-level reply pausing. If it doesn't, this is seven leads: eyeball the inbox each morning and pause the campaign by hand the moment anyone answers.

---

## CSV mapping

`email` → Email · `first_name` → First Name · `last_name` → Last Name · `company_name` → Company Name · `title` → custom variable

Variables are `{{first_name}}` style and **case sensitive**. The info@ row carries "Whoever handles the website" as its first name on purpose, so the greeting renders naturally without a separate campaign.

---

## STEP 1 — Day 0

**Subject:** I built something for Kolnicki, Peterson & Wirth

```
{{first_name}} —

Before anything else: I sent this same message to every partner at KPW and to
the main office inbox. From the outside I couldn't tell who owns a decision
like this, and I'd rather say that plainly than guess wrong.

Your website needed a refresh. I already built it.

https://www.scalelocal.net/test-builds/kpw-cpa/

Click around before you read the rest of this. It's the whole firm — every
service, every partner, the Downers Grove office with a live map, and a set
of plain-English guides on what clients actually call to ask.

What you're looking at:

- 100% designed from scratch by ScaleLocal — thirty-four pages, nothing
  templated, written from your own published material
- Call, email, and appointment-request tools built into every page
- SEO backend built for Google indexing — structured data, clean markup, an
  interactive Google map on the location and contact pages
- Free deployment to a domain of your choosing
- $997 one time. No monthly fee, no maintenance contract, nothing recurring.

That price is low because the work is already finished. There's no discovery
phase to bill you for, no revision cycle, no project manager. You're buying a
completed site, not a project.

Reply and I'll walk you through it. If it isn't for you, I'll send two more
notes at most and then leave you alone.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## STEP 2 — Day 5 (lands the following Tuesday)

**Subject:** The Chicago page

```
{{first_name}} —

Following up on the site I sent last week, but this part stands on its own and
costs you nothing to act on.

kpwcpachicago.com is still up and still selling an office you don't have. The
contact page lists 954 W Washington Blvd, Suite 320, with 312.421.5780 as a
live number. Anyone who lands there calls a number that doesn't reach you or
drives to a suite that isn't yours.

Three more things on that domain, in case nobody's looked at it lately:

The Downers Grove listing on that same page routes to Chicago@kpwcpa.com — the
office you still have is pointing its email at the one you closed.

The site won't load over https at all. The secure address resets the
connection, so every visitor gets it over http and every modern browser marks
the firm "Not secure" in the address bar. For a practice handling client
financials, that's the wrong first impression.

And the footer still reads 2015.

Google is meanwhile reading that domain as a second location for the firm,
which splits your local signal away from the office you actually have.

The build I sent you has none of that — one office, one address, one phone
number, one set of hours, and a map embedded where Google weights it.

https://www.scalelocal.net/test-builds/kpw-cpa/

Still $997, still nothing monthly. But fix the old domain either way.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

**Re-verify every claim in this step the morning it sends.** All four were confirmed live on 2026-07-30. If they've fixed one, cut that line. These are auditors — they will check, and being wrong once costs the sequence.

---

## STEP 3 — Day 12

**Subject:** Last one from me

```
{{first_name}} —

Last note, as promised.

The site is finished and sitting on a private link. It doesn't expire, and I'm
not going to invent a deadline for it.

https://www.scalelocal.net/test-builds/kpw-cpa/

$997, once. I deploy it to whatever domain you want and hand it over. After
that you owe me nothing and you never hear from me again unless you want to.

Fifty-two years is a long time to be the firm people in DuPage County call
first. Your site should say that. Right now it doesn't.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

---

## STEP 4 — Day 40 (re-engagement)

**Subject:** Still have the KPW site on file

```
{{first_name}} —

A few weeks back I sent over a website I'd built for the firm. You didn't take
it up, which is fine.

Extension season is about to land on you. If the Chicago domain or the current
site ever becomes a real annoyance, the build is still on file, still $997, and
I can have it live on your domain in a day.

Say the word and I'll clear the file instead. Either way, this is the last
you'll hear from me.

— Matt | ScaleLocal

ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351
Reply "stop" and I'll take you off my list the same day.
```

Timed to land just after the September 15 partnership and S-corp extension deadline and before October 15. Nothing sends during the week of September 15.

---

## Footer address — resolved

`ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351`

A private mailbox at a commercial mail receiving agency, which is exactly what the FTC names as acceptable alongside a street address or a USPS-registered PO box. Company name only — no personal name, per your call. The `PMB 2777` designation is the correct CMRA format, so mail routes properly and the address reads as a real business location rather than a mail drop.

Paired with the reply-based opt-out line in every step, the footer requirement is satisfied.
