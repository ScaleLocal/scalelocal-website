# HANDOFF — ScaleLocal bespoke CPA site builds

Paste this whole file into a new Cowork session to resume. Everything below is current
as of 2026-07-31, verified live, not remembered.

---

## 1. The mission

Matt (ScaleLocal, Tewksbury/Abington MA) sells completed websites to small accounting
firms as **spec builds**: the site is designed and built before any contact, then pitched
cold at **$997 one time, nothing monthly**. Seven demo sites exist. Six are prospects,
one (KPW) is a completed pitch already staged in Smartlead.

## 2. THE HARD STANDARD — read this before writing a line of code

> **Every site is designed and built from scratch, with its own layout architecture.
> A shared template reskinned in different colours, fonts and config is NOT an
> acceptable deliverable and will be rejected.**

This is in Matt's memory (`/preferences.md`) because it was learned the hard way.
Earlier in this project six sites were generated from one parameterised engine, then
"differentiated" with per-firm palettes, typefaces and four hero variants. Matt spotted
it instantly: same masthead, same hero block, same card grid, same footer, same floating
gold pill, six times over. Two cosmetic passes made it worse, not better.

**It matters extra here because five of the six firms are inside a fifteen-mile circle**
— Tewksbury, North Billerica, Lowell, Billerica, and two in Wilmington. These firms
plausibly know each other. Near-identical demos into one small market actively signal
that nothing was built for them.

**What "from scratch" means in practice:** its own page architecture, its own navigation
model, its own homepage section order and section *types*, its own components, its own
stylesheet. Not a variant of one design — a different design. `site_hickey.py` and
`site_carella.py` are the two references for what clears the bar — and they are
deliberately unlike **each other**, which is the actual test. Hickey is a dense paper
letterhead with ruled indexes, dot leaders and monospace figures; Carella is an open
single-typeface reading column with a standing left rail and a situations spine.

## 3. Where things stand

| Firm | Slug | Pages | Status |
|---|---|---|---|
| James L. Hickey, CPA PC | `hickeycpa` | 35 | ✅ **BESPOKE** — `site_hickey.py` |
| Charles M. Carella, CPA | `carellacpa` | 26 | ✅ **BESPOKE** — `site_carella.py`, deployed 2026-07-31 |
| Mill City Accounting Services LLC | `millcityaccounting` | 17 | ✅ **BESPOKE** — `site_millcity.py`, deployed 2026-07-31 |
| Fitzpatrick & Goguen CPAs P.C. | `bgoguen` | 24 | ⚠️ template build — **rebuild next** |
| Dorfman & Dorfman, CPAs | `dorfmancpas` | 18 | ⚠️ template build — rebuild |
| Thomas P. Craig, CPA, PC (Mass Tax Pros) | `masstaxpros` | 22 | ⚠️ template build — rebuild |
| Kolnicki, Peterson & Wirth, LLC | `kpw-cpa` | 34 | ⚠️ template build (Illinois; campaign already staged) |

All seven are live and private (`noindex,nofollow`) at
`https://www.scalelocal.net/test-builds/<slug>/index.html`.
**Note the trailing `index.html`** — bare directory URLs 404. That is a `vercel.json`
routing gap and is an open item.

**Next job: rebuild Goguen, then Dorfman, Mass Tax Pros, then KPW.** One at a time,
each pushed and shown to Matt before starting the next.

Goguen carries the hardest constraint of the four — see §8. `www.bgoguen.com` is a
CNAME to TaxDome, so their marketing site and their client portal are the same
hostname, and a straight swap takes the portal down. Do not pitch one. Their cheaper
real problem is that the portal is not linked from any page of the public site.

**Three bespoke builds now exist and are deliberately unlike one another. Read all
three before designing the fourth:**
- **Hickey** — a paper letterhead. Dense, serif, ruled indexes with dot leaders,
  monospace figures, claret and brass, static top chrome, a filing-tab widget.
- **Carella** — an open reading column. One sans at every size, a standing left rail,
  a situations spine, hairlines everywhere, chalk-white and pine, a sticky card widget.
- **Mill City** — filled and signage-like. Two audience doors, solid colour surfaces
  instead of rules, Archivo at 112% width, chalk and slate with a vermilion signal,
  and a counter-strip widget carrying a live open/closed state.

`site_carella.py` and `site_millcity.py` also show two different ways to source
content: Carella was written in one pass by hand, Mill City was fanned out to one
agent per page against a fixed component vocabulary and a verified-facts sheet, then
edited. The second is much faster and the component contract held perfectly — but
every page still needs the adversarial claim audit afterwards, which found fifteen
things on Mill City including an invented fee promise and a service count that
disagreed with its own list.

## 4. DEPLOYMENT — do it yourself, directly

Matt has repeatedly and correctly pushed back on being handed commands to run. Per
`BOOT.md` line 316: *"Cowork no longer says 'you have to run it yourself' when Cowork
has computer-use available."*

**The correct method is a direct push from the sandbox using the GitHub PAT.**

The PAT is in `C:\Users\matty\Documents\Claude\System Files\API_KEYS.md` under
`## GitHub Personal Access Token (Universal)` → `**Value:**`.
⚠️ **There are TWO entries with that heading (around lines 331 and 638) with different
tokens.** Use the one whose Scope field has a real description ending "Administration
scope confirmed working 2026-06-26", not the one with bracketed placeholder text.

```bash
# 1. credentials, kept out of argv/history/URLs
python3 - <<'PY'
import os
tok = "<paste from API_KEYS.md>"
open(os.path.expanduser('~/.netrc'),'w').write(
    "machine github.com\nlogin x-access-token\npassword %s\n" % tok)
os.chmod(os.path.expanduser('~/.netrc'), 0o600)
PY

# 2. clone, replace one site, push
export GIT_TERMINAL_PROMPT=0
git clone --depth 1 https://github.com/ScaleLocal/scalelocal-website.git /tmp/slrepo
cd /tmp/slrepo && git config user.email "matt@scalelocal.net" && git config user.name "ScaleLocal Cowork"
rm -rf test-builds/<slug> && cp -r /home/claude/kpw-build/out/<slug> test-builds/<slug>
git add -A -- test-builds/<slug>
git commit -m "..." && git push origin main 2>&1 | sed 's/github_pat_[A-Za-z0-9_]*/[REDACTED]/g'
```

Always pipe git output through that `sed` so a token can never land in the transcript.
Vercel builds in 1–2 minutes. Verify with `curl -o /dev/null -w "%{http_code}"` before
telling Matt it's live.

**Do not use** `_deploy_request.txt` + `autodeploy.bat` for routine work. That watcher
exists on Matt's machine and runs only **hourly**, so requests sit for up to an hour —
this caused real frustration. It is a fallback, not the mechanism. `device_bash` on the
bridge has **no network**, so git push cannot run there.

Computer-use on Matt's machine also works (`mcp__remote-devices__computer_*`). File
Explorer grants at `full` tier; Command Prompt only at `click` tier (visible, clickable,
**no typing**). Navigating Explorer and double-clicking a `.bat` is viable but slower
than the PAT push.

## 5. What to reuse, and what not to

**REUSE these — they are firm-agnostic infrastructure, not layout:**

- `qa.py` — 35-check harness. `BUILD_FIRM=<slug> python3 qa.py`. Reads `ALLOWED_PHONES`
  and `BANNED` from `firms/<slug>.py`. Gate: `RESULT: PASS` with **0 fails and 0 warnings**.
- **`gates_bespoke.py`** — the replacement for `contrast.py` + `layout_audit.py` on a
  bespoke build. Parameterised by slug: add an entry to its `SITES` dict naming the
  classes the build actually uses, plus a `contrast_<slug>.py`, then
  `BUILD_FIRM=<slug> python3 gates_bespoke.py`. Working entries exist for
  `carellacpa` and `millcityaccounting` — copy either.
  Gates A–F: nesting, block geometry, squeezed headings, sticky-rail and fixed-bar
  furniture, the contact widget (§7), and contrast. It refuses to run on a slug it has
  no config for rather than passing vacuously.
- `layout_audit.py` — GATE A (container nesting) is generic and worth running on anything.

⚠️ **`contrast.py` and `layout_audit.py`'s GATE B are NOT reusable on a bespoke build,
and they fail SILENTLY.** `contrast.py` checks a fixed list of pairs from the template
stylesheet — hero gradients, the gold chat pill, cream cards — none of which exist in a
bespoke site; it compares colours the site never puts together and prints a pass.
`layout_audit.py`'s GATE B keys on `.wrap`; with no `.wrap` present it finds no reference
element and skips every geometric check, printing PASS while measuring nothing. Both did
exactly this on Hickey.

Fork them per build instead. `contrast_carella.py` parses the `:root` custom properties
out of the *built* stylesheet and checks the pairs the site actually renders — it caught
input borders at 1.67:1 against paper, failing WCAG 1.4.11. `layout_carella.py` re-points
GATE B at the real class names and adds GATE D: the sticky rail must fit the viewport,
the fixed mobile bar must not cover content, and a table wider than its column must sit
in a `.tscroll` wrapper. Copy those two as the starting point for the next build.
**A green light from the shipped versions is not evidence.**
- `calculators.py` — 8 native calculators (mortgage, refinance break-even, loan payoff,
  retirement, self-employment tax, Section 179, break-even, college). Formulas verified
  against node. **Data only** — each bespoke site renders them in its own markup.
- `render_assets.py` — og.png + apple-touch-icon per firm.
- `research/<slug>.md` — verified facts and explicit do-not-claim lists. **Read before writing.**

**DO NOT extend for new sites:** `build.py`, `design.py`, `content_*.py`, `firms/*.py`
beyond QA metadata. That is the retired template engine. It still builds the five
remaining template sites so they stay live; it must not be the basis of a new one.

**REFERENCE, don't copy:** `site_hickey.py` + `site_hickey_build.py`. Read them to
understand the *shape* of a bespoke build — standalone module, own CSS string, own
components, zero `import build`. Then design something genuinely different.

### Preserving verified prose when rebuilding

The existing template sites contain honesty-checked copy that must not be lost or
rewritten. Extract it before deleting the layout:

```python
from bs4 import BeautifulSoup   # extracts h2/h3/p/ul/ol/table blocks per page
# see the extractor used for Hickey — it produced /tmp/hickey_blocks.json,
# 786 blocks / 24,832 words, all re-laid into the new architecture unchanged
```

## 6. The honesty rules — non-negotiable

Every factual claim must trace to the firm's own published material. These are demos
sent to the firms themselves; an invented fact is caught instantly and costs the pitch.
`BOOT.md` §"PRE-PUBLISH CLAIM AUDIT" makes this a hard gate.

Live examples currently holding, do not break them:

- **Scott Marchlik (Mill City) is NOT a CPA.** His site claims no credential. The only
  "CPA" on it describes a former employer. Never call him one, and never call Mill City
  a CPA firm.
- **Joseph W. Brine (Mass Tax Pros) is an Enrolled Agent, not a CPA.**
- **Brian Goguen has no CFP** on the current site (an archived PDF shows one — ignore it).
- **Hickey names exactly one person** and states no founding year and no office hours.
  No team page, no invented tenure, no invented hours.
- **Carella names nobody at all.** No person, no history, no founding year.
- No fee-timing promises ("quoted before work begins") anywhere — QA bans the phrases.
- No ratings, stars or review markup on any site.
- Every logo is an **original design offered as a proposal**, never presented as the
  firm's existing mark. Say so before the prospect asks.

## 7. Every site needs the contact widget — and it must LOOK like one

Static contact widget on **every page of every site**: **call, email, request an
appointment**, plus **client portal** and **payment link** where one exists.
Explicitly **no GHL, no AI chat, no third-party script, no network call.** If a
calendar integration is wanted later it's added free.

Same *function* on every site, **different execution per site**. Hickey's is a claret
filing tab that opens a panel built like its particulars block. Carella's is a bordered
card with a pine top rule, sticky in its own grid track on wide viewports and a fixed
bar below 1400px. Do not reuse either; design the next one to fit the next site.

> **The failure to avoid.** Carella's first version put the widget inside the left
> rail, where it was technically present on every page and read as navigation. Matt
> looked at the site and said there was no contact widget. He was right — a widget a
> user cannot recognise is not a widget. It has to be a distinct *object*: its own
> border or ground, its own label, visually separate from the nav and the footer.

**This is now gated, not trusted.** `gates_bespoke.py` GATE E fails the build unless,
on every page at every viewport:

- an element carries `data-contact-widget` (tag every variant — desktop and mobile)
- at least one such element is **visible without interaction** — a widget behind a
  toggle that starts closed fails
- it offers a `tel:` link, a `mailto:` link and an appointment/payment route
- it embeds no `<script>` and no `<iframe>`
- it is not `position:fixed` overlapping the reading column. A bottom-anchored
  full-width bar is exempt, because GATE D separately checks the footer's bottom
  padding clears it. A floating panel parked mid-column is not exempt — Carella's
  second attempt sat directly on top of the body text and this is what caught it.

Add the build's `data-contact-widget` elements before writing the CSS, not after.

## 8. Preserved features, by firm (audited live 2026-07-30)

Every calculator on every one of these sites is a **vendor-licensed widget on the
vendor's account** — CalcXML skin 481 (Hickey, Mass Tax Pros) or cchwebsites.com
(Carella). None of it transfers. Article libraries are syndicated vendor feeds and
likewise don't transfer. **Rebuild calculators natively; replace articles with genuine
firm-specific guides.**

| Firm | Portal | Payments | Calculators today |
|---|---|---|---|
| Hickey | CPA Site Solutions — `securefirmportal.com/Account/Login/4700` (self-registration **dead, 503**) | PayPal hosted button (button ID must be re-pasted by the firm at cutover) | 147, vendor |
| Mill City | none | Square — `https://square.link/u/1BBydiwq` | none |
| Goguen | TaxDome — `https://www.bgoguen.com/login` | in-portal only | none |
| Carella / Dorfman / Mass Tax Pros | none | none | 40 / none / 13 |

**Goguen carries a hard constraint:** `www.bgoguen.com` is a CNAME to
`briangoguenpc.cd.taxdome.com` — their marketing site and client portal are the same
hostname. Replacing the site means repointing DNS, which takes the portal down unless it
moves to a subdomain first. Do not pitch a simple swap. Their cheaper real problem: the
portal isn't linked from any page on the public site.

## 9. Outreach state

- **`THREE_PITCHES.md`** — three segmented pitches: **A "Not Secure"** (Hickey, Carella,
  Dorfman — all three fail HTTPS differently), **B "Frozen"** (Mass Tax Pros, publicly
  stuck at 2013 with a live WordPress placeholder post), **C "Invisible"** (Mill City,
  Goguen — nothing broken, the problem is what's absent).
- **KPW campaign is built and PAUSED** in Smartlead: id **3744204**, 4 touches at
  delays `[0,5,7,28]`, 7 leads, Tue/Wed/Thu 09:00–11:00 America/Chicago.
  Scripts: `smartlead_create_kpw.py`, `smartlead_start_kpw.py` (both live on Matt's
  machine in `ScaleLocalCode\Workflows\`; they read the Smartlead key locally).
- **CAN-SPAM footer address** (settled, use verbatim, company name only):
  `ScaleLocal, 1035 Bedford St, Ste 103 PMB 2777, Abington, MA 02351`
- Sending subdomain `hi.scalelocal.net` has valid SPF, Google DKIM and DMARC `p=none`.
  **Root `scalelocal.net` has NO SPF and NO DMARC** — open item, unrelated to this work.
- Only Mill City and Dorfman publish an inferable `firstname@` pattern. The other four
  give one role inbox each — **do not guess addresses**, bounces cost sender reputation.
- Mass Tax Pros sits behind **Proofpoint Essentials** (aggressive filtering).
  **Dorfman and Mass Tax Pros are both in Wilmington** — separate their sends by ≥2 weeks.

## 10. Open items

1. **Rebuild Carella from scratch** — one accountant, no team page, no portal, no
   payments, nothing to show off. The answer is quiet and text-led with almost no
   chrome: the opposite of Hickey's density. Then Mill City, Goguen, Dorfman,
   Mass Tax Pros, KPW.
2. `vercel.json` — bare directory URLs 404; only `/index.html` resolves.
3. Delete the duplicate/stale GitHub PAT entry in `API_KEYS.md`.
4. Smartlead API key still carries a **ROTATE-ME flag from 2026-06-04**.
5. `Free_Website_Delivery_Sequence.md` still quotes retired pricing (Presence $297 /
   Foundation $497) — will misprice the next prospect who runs through it.
6. Decide what "free deployment to a domain of your choosing" includes — if it covers
   repointing existing DNS, that's unpaid support already promised in the copy.
7. `noindex,nofollow` is on 4 layers of every site — must come off at production cutover
   or the client's new site launches invisible.
8. Hickey open questions for the client: office hours (unpublished), PayPal button ID,
   whether "our staff" implies anyone nameable, and whether they issue audit/review reports.

## 11. Traps that already cost time — don't repeat them

- **The device bridge cannot `unlink`.** `git add` stages 0 files there, and `tar -x`
  fails with "Cannot open: File exists" when overwriting. Extract to a staging dir and
  `cp -rf` over instead. To "delete" on Matt's machine, `mv` into `_to_delete/`.
- **`device_bash` has no network.** Nothing that fetches or pushes runs there.
- **`dig` is not installed in the sandbox.** Use `dnspython`. A blank `dig` result with
  stderr suppressed once produced a false "no SPF/DMARC" finding.
- **Playwright must block `https?://` routes** when screenshotting local files, or the
  Google Maps iframe stalls page load until timeout.
- Wide tables need a scroll wrapper, and grid children need `min-width:0`, or they push
  the whole document sideways on a 390px viewport.
- **Look at screenshots.** Gates pass on plenty of things that look broken to a human —
  a hero h1 crushed into a 200px column passed every check until GATE C was written. On
  Carella, four defects survived all three green gates and were caught only by looking:
  a mangled demo strip, a logo rendering at 300px, band headings breaking into three
  short lines, and index rules running far wider than their text.
- **`width`/`height` do nothing on an inline element.** The Carella logo wrapper was a
  `<span>` with no `display`, so the SVG rendered at its default size and made the nav
  rail 1101px tall in a 900px viewport. Set `display:block` on any sized span.
- **Splitting a string on `'. '` breaks on "Charles M. Carella".** The demo strip shipped
  reading "Demonstration site. Carella, CPA by ScaleLocal". Never derive display copy by
  splitting on a full stop — store the two halves separately.
- **Screenshot runs stall on `wait_until='load'` if you `route.abort()` a subresource.**
  Use `route.fulfill(status=204)` for the map host. And do NOT block fonts.googleapis.com
  when screenshotting — it is reachable from the sandbox, and a shot in a fallback face
  is not evidence about a design whose whole system is typography.
- **Playwright measurements at `domcontentloaded` can precede the stylesheet.** Wait on a
  computed value only your CSS sets, or the audit reports confident nonsense — mine
  produced four phantom failures before I caught it.
- **Entities inside meta descriptions get escaped twice.** `&mdash;` in a `desc` string
  ships as a literal `&amp;mdash;` in the share preview. Use plain punctuation there.
- **Verify shared data, not just your own copy.** `calculators.py` still defaulted to the
  2025 Social Security wage base ($176,100) — wrong on Hickey and Mass Tax Pros too. Now
  $184,500. Re-check every dated figure in shared files at the start of each build.

## 12. Working with Matt

Direct, expert-led, no padding. He delegates design and architecture decisions and
expects them made, not asked about. He pushes back hard and accurately when output is
below standard — when he does, **fix the actual cause, don't make another cosmetic
pass**. Own mistakes plainly and move on. Deploy things yourself. Don't hand him
commands to run.
