# HANDOFF — ScaleLocal bespoke CPA site builds

Paste this whole file into a new Cowork session to resume. Everything below is current
as of **2026-07-31**, verified live, not remembered.

---

## 1. The mission

Matt (ScaleLocal, Tewksbury/Abington MA) sells completed websites to small accounting
firms as **spec builds**: the site is designed and built before any contact, then pitched
cold at **$997 one time, nothing monthly**. Seven demo sites exist. All seven are now
bespoke standalone builds.

---

## 2. THE HARD STANDARD — read this before writing a line of code

> **Every site is designed and built from scratch, with its own layout architecture.
> A shared template reskinned in different colors, fonts and config is NOT an
> acceptable deliverable and will be rejected.**

This is in Matt's memory (`/preferences.md`) because it was learned the hard way.

**It matters extra because five of the six Massachusetts firms are inside a fifteen-mile
circle** — Tewksbury, North Billerica, Lowell, Billerica, and **two in Wilmington a mile
apart**. These firms plausibly know each other. Near-identical demos into one small
market actively signal that nothing was built for them.

### 2.1 The same-agency test is about PROSE and SKELETON, not CSS

This is the single most important lesson of 2026-07-31 and it was learned by failing it.

After every site had its own palette, typefaces, tokens, shadows and breakpoints — all
genuinely bespoke — an adversarial cross-site audit still **failed** the batch. The tells
were not visual:

- **Dorfman and Mass Tax Pros are a mile apart in Wilmington and shipped the same
  sentence in the same slot on the same page**: *"Two people, and one of them will be the
  one who does the work."* Two more matched on their resources pages.
- *"the person who does the work"* appeared on **35 pages across five firms**. It was the
  agency's sales pitch, not any firm's proposition.
- The map caption *"Pan, zoom, or open the map full screen for directions"* was
  **identical on all seven sites** — same microcopy, same slot, same iframe.
- The financial-statement service ladder was one table pasted into two firms.
- Three sites rendered the same calculator suite: same H1s, same input labels, same JS.
- Massachusetts tax facts were repeated word-for-word across three sites.

**Therefore: a build is not finished until `dupcheck.py` reports zero.**

```bash
python3 dupcheck.py          # pairwise sentence overlap between built sites
```

It extracts every sentence of ≥8 words from a site's built HTML, normalizes it, and
reports any appearing in two firms' output. The ScaleLocal demonstration notice is
filtered by name — it is legal boilerplate and stays deliberately uniform. **Target is
literally zero across all 21 pairs.** Extend it whenever a site is added.

Facts may of course be shared — Massachusetts filing thresholds are what they are. The
*sentences* may not. Restate them per site, in different forms: a table on one, running
prose on another, a bullet list on a third. **When restating a fact, every figure, form
number, percentage and date must survive unchanged.** Diff the built output to prove it.

### 2.2 Structural fingerprints count too

Identical HTML skeletons under different CSS still read as one agency to anyone who views
source. Vary the actual element order per site — nav before brand on one, `<nav>` as the
top-level landmark on another, the demo notice in the footer on a third — and vary the
schema.org block ordering rather than emitting the same `AccountingService` key sequence
seven times. Class *names* leak too: rename `.btn/.hero/.foot` per site, don't ship the
same vocabulary with different values.

---

## 3. THE CORRECTED DESIGN DIRECTION — read before designing anything

An earlier pass over-corrected from "six sites from one template" into **structural
radicalism**, which has its own signature. Standing left rails, no hero, homepages that
opened straight into a data spine. Matt's verdict, and he was right on all four counts:

1. Left panels go against norms; almost every firm site has a conventional top nav.
2. The sites *"just jump right into data and information"* instead of having a beautiful,
   inviting home page.
3. Being uniformly unusual **still reads as one agency** — unusualness is itself a style.
4. Leading with the entire partner list is *"a little aggressive."*

**The shape every build now follows:**

- **Conventional top bar** — wordmark left, nav, phone, one action right. A visitor should
  not have to learn a navigation scheme before they can use an accountant's website.
- **A warm inviting hero on the homepage** — eyebrow, h1, short subheading, **ONE** primary
  CTA plus one secondary link, a phone line, and hero art.
- **Services before people.** Never open on the full partner roster. Introduce the team in
  prose and link the full page.
- **A closing action band**, then the footer.
- **A small-screen `<details>` nav disclosure.**
- **The comms widget** (§7) on every page.

Within that shape, everything else must differ per firm — that is where the
distinctiveness lives now, not in the skeleton.

`site_dorfman.py` and `site_carella.py` are the two reference builds. Read both end to
end before designing the next one.

---

## 4. Where things stand

| Firm | Slug | Pages | Design identity |
|---|---|---|---|
| James L. Hickey, CPA PC | `hickeycpa` | 35 | paper letterhead — dense serif, ruled indexes, dot leaders, claret/brass, filing-tab widget |
| Charles M. Carella, CPA | `carellacpa` | 25 | one sans at every size, marginal gutter labels, hairline index rows, chalk/pine |
| Mill City Accounting Services LLC | `millcityaccounting` | 12 | filled and signage-like, Archivo at 112% width, live open/closed status, chalk/slate/vermilion |
| Fitzpatrick & Goguen CPAs P.C. | `bgoguen` | 17 | soft shadowed rounded cards, Fraunces + Figtree, indigo/sand |
| Dorfman & Dorfman, CPAs | `dorfmancpas` | 13 | outlined "filed" boxes with a label tab, Spectral + Barlow SC, slate/warm |
| Thomas P. Craig, CPA, PC (Mass Tax Pros) | `masstaxpros` | 20 | **dark-first chrome**, Space Grotesk + IBM Plex, brass on ink, mono step numerals |
| Kolnicki, Peterson & Wirth, LLC | `kpw-cpa` | 21 | the record — ruled dated rows, Instrument Serif + Inter Tight, navy/gold/cream |

**143 pages total.** All live and private (`noindex,nofollow`) at
`https://www.scalelocal.net/test-builds/<slug>/index.html`.
**Note the trailing `index.html`** — bare directory URLs 404 (`vercel.json` gap, open item).

---

## 5. RE-VERIFY THE FIRM'S SITE LIVE. EVERY TIME.

**The research files in `research/` were substantially wrong on every single firm they
were checked against.** Not once did a live re-crawl agree with the file. Examples:

- **Mill City** — seven services, not four; the "moved from" address is still live.
- **Goguen** — the recorded phone number was wrong (real: **(978) 667-4595**); three
  services not four; a live "over 25 years" claim the file missed entirely.
- **Dorfman** — all six service wordings were invented by the file; "compilation" was
  wrongly banned when it is the firm's own first service bullet; the HTTPS certificate is
  self-signed and expired 19 June 2025, which the file never mentioned.
- **Mass Tax Pros** — 12 calculators, not 13. And critically: the file said Joe Brine is
  an Enrolled Agent. Their site says only that he was ***pursuing*** Enrolled Agent
  status — it never says he completed it. Even "EA" is not safe to assert.
- **KPW** — the profile carried a **fax number and a suite number that appear nowhere on
  their site** (they came from a stale sister domain, `kpwcpachicago.com`, © 2015). Its
  phone number is printed malformed as `+1 0630 3901140`.

**Procedure before any build:** crawl the firm's live site page by page, quote everything
exactly, and mark anything not found as **NOT STATED** rather than inferring it. Treat the
research file as a lead, never as a source. Where a number can't be confirmed from the
firm's own material, confirm it against independent listings and say what confirmed it —
or ship without it. **A wrong phone number on a demo site is worse than a missing one.**

---

## 6. Only offer what the firm already offers

Matt's rule, stated 2026-07-31 and now in his memory:

> *"We want to offer the same offers that they have on their website, not go above and
> beyond and give them things they may not need, or may actually hurt them."*

He is right, and for a bigger reason than convenience. A calculator on a CPA's own site
computes figures that change annually — the SE wage base moved 176,100 → 184,500 during
this project. A stale calculator on an accountant's website is a professional
embarrassment they never asked for. And a shared calculator module was the single most
provably identical artifact across the portfolio.

| Firm | Real site publishes | Build |
|---|---|---|
| Carella | 40 calculators (cchwebsites.com) | **keep** |
| Hickey | 147 calculators (CalcXML skin 481) | **keep** |
| Mass Tax Pros | 12 calculators (CalcXML skin 481) | **keep** |
| Dorfman | none | **none** — Resources page instead, carrying their own five links repaired |
| Goguen | none | **none** |
| Mill City | none | **none** |
| KPW | none | **none** |

Same logic for portals, payment routes, booking, newsletters and blogs. Build what they
have. Where they have a real one, surface it — Goguen pays for a TaxDome portal their own
site links from nowhere, and putting it in the widget is the most valuable thing that
build does.

**Calculator architecture:** `calculators.py` holds structure and arithmetic ONLY — slugs,
input ids, kinds, defaults, the JS compute bodies, output ids. Every reader-facing string
lives in a per-site `CALC_COPY` dict and is applied through `C.dress(slug, copy)`.
`dress()` **raises** on a missing label rather than falling back, because a shared default
is exactly how the duplication came back last time. Never fork `calculators.py` — the
formulas must not drift.

---

## 7. THE COMMS WIDGET — the one deliberate constant

**Matt's spec, verbatim:** *"comms widget floating bottom right is what it should be…
Maybe says 'Let's Connect' and then they click and it's click to dial, click to email, and
click to book an appointment… The widget needs to be an absolute must have for all of
these websites, not just a floating contact block or what you have at the top."*

**The contract, gated by `gates_bespoke.py` GATE E on every page at every viewport:**

- A floating launcher **bottom right**, with a **visible text label** ("Let's connect")
  and an accessible name.
- It **must be a `<details>` element** — so it works with JavaScript disabled, is keyboard
  operable natively, and announces its own open/closed state without scripting.
- The panel offers **click-to-dial**, **click-to-email** and **click-to-book** as separate
  links, plus a **portal or payment route where the firm actually has one**.
- **No `<script>`, no `<iframe>`, no network call, no third party.**
- Open state hides the label and shows "Close".

**Same function everywhere; different execution per site.** Pine rectangle (Carella),
slate bordered box (Dorfman), indigo pill (Goguen), vermilion (Mill City), brass on ink
(Mass Tax Pros), navy with an inset gold rule (KPW), claret filing tab clipped to the
bottom edge (Hickey).

> **Two failures worth remembering.** Carella's first version put the widget inside the
> left rail, where it was technically present and read as navigation — Matt said there was
> no contact widget, and he was right: *a widget a user cannot recognize is not a widget.*
> Then GATE E was over-corrected to demand "visible without interaction", which came from
> misreading that complaint and forced a permanently-open block. The gate now matches the
> spec above.

**Still open:** the panel *construction* is one component in six skins (`summary > .ic +
.lbl + .x`, panel widths clustered 292–308px, `z-index:80` on all seven). Re-plumb two or
three into genuinely different constructions.

---

## 8. AMERICAN ENGLISH

These are American firms. The whole batch was written in British English and had to be
corrected: **716 replacements across 69 source files**, plus a second pass. "Authorised"
alone was on the demonstration notice of all 138 pages.

Watch for: `authorise · organise · licence · practise · enquiry · dependants · instalment
· judgement · acknowledgement · cheque · programme · per cent · towards · centre · colour
· favour · labour · defence · travelled · cancelled · ageing · whilst · amongst · harbour
· specialism · notarisation · enrolment · fulfil · skilful · grey · maths · realisable ·
storey · learnt · spelt`

**Do NOT "correct" these — they are already correct American English:** `analysis`,
`specialist`, `expertise`, `enterprise`, `advertise`, `exercise`, `supervise`.

Two are also professional-terminology errors, not just spelling: **`enquiry` → `inquiry`**
(AICPA SSARS language for a review engagement is "inquiry of management and analytical
procedures") and **`dependants` → `dependents`** (the IRS term).

Also: **every one of these firms publishes "Fax"**, never "Facsimile". Goguen's letterhead
uses "F:". "Facsimile" was an affectation that reached 43 pages before Matt caught it.

The scanner used is reproducible — see §13.

---

## 9. Deployment — do it yourself, directly

Matt has repeatedly and correctly pushed back on being handed commands to run.

**Direct push from the sandbox using the GitHub PAT.** The PAT is in
`System Files/API_KEYS.md` under `## GitHub Personal Access Token (Universal)`.
⚠️ **There are TWO entries with that heading and different tokens.** Use the one whose
Scope field ends "Administration scope confirmed working 2026-06-26".

```bash
python3 - <<'PY'
import os
tok = "<paste from API_KEYS.md>"
open(os.path.expanduser('~/.netrc'),'w').write(
    "machine github.com\nlogin x-access-token\npassword %s\n" % tok)
os.chmod(os.path.expanduser('~/.netrc'), 0o600)
PY

export GIT_TERMINAL_PROMPT=0
git clone --depth 1 https://github.com/ScaleLocal/scalelocal-website.git /tmp/slrepo
cd /tmp/slrepo && git config user.email "matt@scalelocal.net" && git config user.name "ScaleLocal Cowork"
rm -rf test-builds/<slug> && cp -r /home/claude/sitebuilds/sitebuilds/out/<slug> test-builds/<slug>
git add -A -- test-builds/<slug>
git commit -m "..." && git push origin main 2>&1 | sed 's/github_pat_[A-Za-z0-9_]*/[REDACTED]/g'
```

Always pipe git output through that `sed`. Vercel builds in 1–2 minutes; the CDN can serve
stale HTML for another minute after that, so **verify with a cache-busting query string**
before reporting live.

⚠️ **`rm -rf test-builds/<slug> && cp -r out/<slug>` will delete any file that lives in the
repo but is not regenerated by the build.** This silently dropped Hickey's `og.png` and
`apple-touch-icon.png`. They are now in `static/hickeycpa/` and copied in by
`site_hickey_build.py`. Audit every site's assets after a deploy.

**Do not use** `_deploy_request.txt` + `autodeploy.bat` — that watcher runs hourly.
`device_bash` on the bridge has **no network**, so git push cannot run there.

---

## 10. The verification stack — all of it, every build

```bash
python3 site_<firm>.py                                # build
python3 assets_<firm>.py && python3 art.py <slug>     # og image, touch icon, hero art
python3 contrast_<firm>.py                            # must end  PAIRS: n   FAILS: 0
BUILD_FIRM=<slug> python3 qa.py                       # RESULT: PASS, 0 fails, 0 warnings
BUILD_FIRM=<slug> python3 gates_bespoke.py            # GATE A, B/C/D/E, F all PASS
python3 dupcheck.py                                   # TOTAL SHARED: 0
```

Plus, by hand every time:
- **Walk every relative href and `#fragment`** and assert the target exists.
- **Sweep viewport widths for horizontal overflow.** Not just 1440/390 — sweep. Carella
  overflowed from **1184px to 1348px**, which put **1280 — one of the commonest laptop
  widths there is** — inside a broken band on all 26 pages. Three green gates missed it
  because they only sampled 1512/1440/1100/390.
- **Look at screenshots.** Gates pass on plenty of things that look broken to a human.
- **Run the adversarial cross-site audit** (§2.1) before declaring a batch finished.

⚠️ **`contrast.py` and `layout_audit.py` GATE B pass VACUOUSLY on a bespoke build** — they
are welded to the retired template's `.wrap` class and its color pairs, so they measure
nothing and print PASS. Use `gates_bespoke.py` + a per-site `contrast_<firm>.py` that
parses `:root` out of the **built** stylesheet. A green light from the shipped versions is
not evidence.

**Never weaken a gate to make it pass.** If a gate reports a real defect, fix the site.
The only legitimate gate edit is adding a site's entry to `SITES`/`CONTRAST_SCRIPT`, or
correcting a container contract when the architecture genuinely changed.

---

## 11. The honesty rules — non-negotiable

Every factual claim must trace to the firm's own published material. These are demos sent
to the firms themselves; an invented fact is caught instantly and costs the pitch.

Currently holding — do not break:

- **Scott Marchlik (Mill City) is NOT a CPA and NOT an EA.** The only "CPA" on his site
  describes a former employer.
- **Joseph W. Brine (Mass Tax Pros) is NOT a CPA.** Their site says only that he was
  *pursuing* Enrolled Agent status — do not flatly assert "EA" either.
- **Michael J. Kolnicki (KPW) has no printed title and is not a CPA** — `EA, CFP®` only.
- **Brian Goguen has no CFP** on the current site.
- **Mass Tax Pros advertise compilation only** — never audit or review. **KPW genuinely
  advertise audit, review and compilation** — but say "audit, review, and compilation",
  never "assurance", which is their wording.
- **Hickey names exactly one person**, no founding year, no office hours.
- **Carella names nobody at all.**
- **No years-of-experience figures anywhere.** Mass Tax Pros' site is frozen at 2013 and
  every one of its claims ("a quarter century", "approximately 15 years", "more than 50
  years combined") is thirteen years stale. KPW's site says "started in 1974" — write the
  founding year, never a year-count, which goes stale the moment it ships.
- No fee-timing promises; no ratings, stars or review markup.
- Every logo is an **original design offered as a proposal**, never the firm's existing
  mark.
- **KPW's peer review** (Klesman & Company, letter 2/28/2022, year ended 6/30/2021, rating
  *pass*) must be described by its period and letter date, **never as current**.

---

## 12. Art direction

`art.py` generates original hero plates as SVG → PNG at 2× via Playwright. **There is no
image-generation tool in this session**, and stock photography is not acceptable anyway:
none of these firms publishes photographs of its office or people, so implying either is a
false claim.

Registered: Dorfman (offset record cards), Carella (three documents on a desk), Mill City
(a Lowell mill wall and a receipt tape), Goguen (pieced quarter-rounds), Mass Tax Pros
(four ascending tiers), KPW (a ruled register struck with a seal). **Hickey gets none by
judgement** — its austerity is the design.

**Image acquisition from the web is not possible in this session.** Wikimedia returns
"domain is cache-only", LOC returns 403, WebFetch returns markdown not binary, Chrome on
Matt's machine resolves at `tier: "read"` only, and `device_bash` has no network. If real
photography is wanted, a free **Pexels** or **Unsplash** API key is the route — both are
reachable (401 = needs key) and both licenses permit commercial use and local storage.
A drop folder exists at `C:\Users\matty\ScaleLocalCode\SitePhotos\`.

---

## 13. Reproducible tooling written this session

- **`dupcheck.py`** — pairwise sentence-overlap between built sites. Target zero.
- **The British-English scanner** — regex pairs with case-preserving replacement, with
  `analysis`/`specialist`/`expertise` explicitly excluded. Recreate from §8 if lost.
- **`gates_bespoke.py`** — slug-parameterised GATES A–F. Its exit code was broken for
  every build until 2026-07-31: `'FAIL' in cres` matched the substring inside the clean
  summary `FAILS: 0`, so it exited 1 on every firm regardless of result. Fixed.
- **`/tmp/shot.py`** pattern — Playwright screenshot helper, `url out w h [full]`.
- **Math-invariance harness** — before refactoring anything numeric, render every
  calculator's outputs at its defaults to a file; after, render again and diff. Used to
  prove the calculator presentation split changed no arithmetic: 113 rendered values,
  zero drift.

---

## 14. Outreach state

**KPW — LIVE.** Campaign `3744204`, status **ACTIVE**, 7 leads, 4 touches at delays
`[0,5,7,28]`, Tue/Wed/Thu 09:00–11:00 America/Chicago, sending from
`matt@hi.scalelocal.net` (15/day, warmup active). Zero sent as of 2026-07-31 — it is
waiting on its next Tuesday window, not stalled.

⚠️ **Three false claims were found in it and corrected on 2026-07-31, after Matt had
already reviewed it.** It said the site was *"thirty-four pages"* (the rebuild is 21), it
claimed *"plain-English guides"* the rebuild does not contain, and it asserted *"Fifty-two
years"* — a year-count the site itself deliberately avoids. A recipient address was also
misspelled `rwirth@` and would have bounced (`rdwirth@` is correct).

> **Rule this establishes: whenever a site is rebuilt, re-read every email that links to
> it and re-verify every claim against the built output.** Page counts, feature lists and
> anything numeric. Campaign copy goes stale the moment the site changes.

Touch 2's claims about `kpwcpachicago.com` were **re-verified true on 2026-07-31**: 954 W
Washington Blvd Suite 320 and 312.421.5780 still published; the Downers Grove listing
still routes to `Chicago@kpwcpa.com`; HTTPS still fails outright; footer still © 2015.

**ALL SEVEN CAMPAIGNS ARE LIVE**, and all seven send on **Tuesday 4 August 2026** —
Matt's call, made after the stagger below was proposed.

| Campaign | ID | Leads |
|---|---|---|
| KPW_DownersGrove | 3744204 | 7 |
| Hickey_Tewksbury | 3748518 | 1 |
| Carella_NorthBillerica | 3748521 | 1 |
| MillCity_Lowell | 3748522 | 1 |
| FitzpatrickGoguen_Billerica | 3748523 | 1 |
| Dorfman_Wilmington | 3748524 | 1 |
| MassTaxPros_Wilmington | 3748529 | 1 |

All Tue/Wed/Thu 09:00-11:00, `min_time_btw_emails` 15. KPW runs America/Chicago, the six
MA firms America/New_York. Delays `[0,5,7,28]` throughout, so the whole batch moves in
lockstep: touch 1 Tue 4 Aug, touch 2 Tue 11 Aug, touch 3 Tue 18 Aug, touch 4 Tue 15 Sep.

**Volume: 13 emails per send day against a 15/day inbox cap** on the single warming inbox
`matt@hi.scalelocal.net`. It fits, with two to spare. If a firm is added, raise the inbox
cap first — do not let a campaign silently defer.

**A stagger was proposed and overridden.** The original plan spread the six MA firms over
two weeks and put the two Wilmington firms three weeks apart, because Dorfman and Mass Tax
Pros are a mile from each other. They now land the same morning. That is a real
adjacency risk, and it is materially reduced by the fact that the two sites share zero
sentences and zero layout after this session's work — but if either firm mentions the
other, that is why.

Goguen's address was settled as **office@bgoguen.com**, confirmed by reading their live
contact page through a renderer after Cloudflare 403'd direct fetches.

Pre-flight check run on all 24 rendered emails before starting: postal address present,
opt-out line present, demo link present and pointing at the right slug, no British
spellings, no unresolved merge tags, page-count word matching the real build. Zero
problems. **Re-run that check after any site rebuild.**

The original drafts, hooks and evidence are in `CAMPAIGNS_SIX_FIRMS.md` — `CAMPAIGNS_SIX_FIRMS.md`
holds the full copy, verified recipients and per-firm hooks, all re-verified live
2026-07-31. The hooks:

| Firm | Hook |
|---|---|
| Goguen | **Strongest in the batch.** Live TaxDome portal at `/login`, linked from **no page** of their site. |
| Dorfman | HTTPS cert self-signed, expired 19 Jun 2025 — every visitor gets a full-page security warning. |
| Hickey | 147 calculators pop out to a vendor domain; **no HTTPS at all** (`errno=104`). |
| Carella | `tel:` link is malformed — `tel:9786636419ext.11` misdials from a phone. |
| Mass Tax Pros | Frozen at 2013, incl. a live placeholder post; one calculator link miswired. |
| Mill City | Two Lowell addresses on one contact page nineteen months after the move; blog in nav with zero posts. |

**One unresolved:** Goguen's published address reads `info@bgoguen.com` on two live reads
today but `office@bgoguen.com` in the research and the built site. Cloudflare challenges
automated fetches. **Eyeball it in a browser before sending; send to one, not both.**

Other outreach facts:
- CAN-SPAM footer, verbatim, company name only:
  `ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351`
- Opt-out line: `Reply "stop" and I'll take you off my list the same day.`
- `hi.scalelocal.net` has valid SPF, Google DKIM, DMARC `p=none`. **Root `scalelocal.net`
  has NO SPF and NO DMARC** — open item.
- Each of the six MA firms publishes **exactly one** address. **Do not guess patterns.**
- Mass Tax Pros sits behind **Proofpoint Essentials**. **Dorfman and Mass Tax Pros are both
  in Wilmington — separate their sends by ≥2 weeks.**

---

## 15. Open items

1. **All seven campaigns are live** — watch the inbox. Reply-stop behavior may be
   per-lead rather than per-domain; if a firm replies, pause by hand.
2. Comms-widget panel construction is still one component in six skins (§7).
4. Class-name vocabulary (`.btn`, `.hero`, `.foot`) still recurs across six sites (§2.2).
5. `vercel.json` — bare directory URLs 404; only `/index.html` resolves.
6. Delete the duplicate/stale GitHub PAT entry in `API_KEYS.md`.
7. Smartlead API key carries a **ROTATE-ME flag from 2026-06-04** — and it has now been
   read into a second session. Rotate it.
8. `Free_Website_Delivery_Sequence.md` quotes retired pricing ($297/$497).
9. Decide what "free deployment to a domain of your choosing" includes — if it covers
   repointing existing DNS that is unpaid support already promised in the copy.
10. `noindex,nofollow` is on 4 layers of every site — **must come off at cutover** or the
    client's new site launches invisible.
11. **Goguen hard constraint:** `www.bgoguen.com` is a CNAME to TaxDome — marketing site
    and client portal share a hostname, so a straight DNS swap takes the portal down. Do
    not pitch a simple swap.
12. Hickey open questions for the client: office hours, the PayPal button ID, whether "our
    staff" implies anyone nameable, and whether they issue audit/review reports.

---

## 16. Traps that already cost time — don't repeat them

- **The device bridge cannot `unlink`.** `git add` stages 0 files there; `tar -x` fails
  with "Cannot open: File exists". To "delete" on Matt's machine, `mv` into `_to_delete/`.
- **`device_bash` has no network.**
- **`dig` is not installed.** Use `dnspython`.
- **Playwright must block `https?://` routes** when screenshotting local files, or the maps
  iframe stalls page load. Use `route.fulfill(status=204)`, **not** `route.abort()` — an
  aborted subresource leaves the load event pending forever. Do **not** block
  `fonts.googleapis.com`: a shot in a fallback face is not evidence about a design whose
  whole system is typography.
- **Playwright measurements at `domcontentloaded` can precede the stylesheet.** Wait on a
  computed value only your CSS sets, or the audit reports confident nonsense.
- **`width`/`height` do nothing on an inline element.** A `<span>` with no `display` made
  the Carella logo render at 300px and the nav rail 1101px tall in a 900px viewport.
- **Never derive display copy by splitting on `'. '`** — it breaks on "Charles M. Carella"
  and shipped a demo strip reading *"Demonstration site. Carella, CPA by ScaleLocal"*.
- **Entities inside meta descriptions get escaped twice.** `&mdash;` ships as
  `&amp;mdash;`. Use plain punctuation there.
- **Wide tables need a scroll wrapper**, and grid children need `min-width:0`.
- **Verify shared data, not just your own copy.** `calculators.py` still carried the 2025
  Social Security wage base ($176,100) — wrong on three sites. Now $184,500. Re-check every
  dated figure in shared files at the start of each build.
- **A patch script that dies mid-way leaves the file half-written.** An `AssertionError` in
  a multi-replacement script aborted before the write, so a CSS change and a function swap
  never landed, and the next script failed with `NameError`. Write atomically or verify
  after.
- **Meta descriptions must be 70–175 characters** or `qa.py` warns. Count the rendered
  string, not the source — entities expand.

---

## 17. Working with Matt

Direct, expert-led, no padding. He delegates design and architecture decisions and expects
them **made, not asked about**. He pushes back hard and accurately when output is below
standard — when he does, **fix the actual cause, don't make another cosmetic pass**. Own
mistakes plainly and move on. Deploy things yourself; don't hand him commands to run.

He notices real things. Every single correction he made this project was right: the
template reskin, the missing widget, the left-panel direction, "facsimile", the calculators
Dorfman never asked for, and the British English. When he says something is off, it is off
— the job is to find the actual cause, which has usually been deeper than the symptom he
named.
