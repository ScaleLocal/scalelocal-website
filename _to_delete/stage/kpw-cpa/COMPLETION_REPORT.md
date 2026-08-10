# COMPLETION REPORT — Kolnicki, Peterson & Wirth, LLC
**Build:** `test-builds/kpw-cpa/` · **Date:** 2026-07-29 · **Pipeline:** HANDOFF_WEBSITE_DEMOS v2.2
**Posture:** A — PRIVATE STAGING (all four blocking layers, §10.1) · **Status:** ready for your review

---

## 1. What was built

**34 pages** — exceeds the 25+ page target in §1/§11. (Was 35; the Chicago location page was deleted when that office closed.)

| Section | Count | Pages |
|---|---|---|
| Core | 5 | Home, About the firm, Peer review & quality control, Common questions, Contact |
| Services | 13 | Hub + tax planning & preparation, audit & assurance, financial statements, accounting services, business advisory, business valuation, estate & trust planning, litigation support, mergers & acquisitions, asset protection, business management (entertainment/sports), employee benefit plans |
| Industries | 5 | Hub + privately held businesses, government & non-profit, entertainment & sports, real estate & construction |
| Team | 7 | Hub + 6 individual professional bios |
| Location | 1 | Downers Grove (Chicago office closed — removed 2026-07-30) |
| Guides (AEO layer) | 3 | What a CPA costs a small business · Audit vs. review vs. compilation · How to choose a CPA firm in Illinois |

Total build: 1.2 MB, self-contained (one shared `css/site.css`, no external dependencies beyond Google Fonts).

**Typeface (revised 2026-07-30):** headings are **Source Serif 4**, body **Inter**. The original build used Fraunces, a deliberately wonky soft-serif whose irregular letterforms Matt rejected; Source Serif 4 is a straight, screen-optimised text serif. Heading weight moved 500 -> 600 and hero measure widened to 21ch to suit the wider face.

## 2. Engine — the P0 build-out, started

Per the **engine-split default (§8.1/§13)**, `gen_sites.py` was **not touched**. This build runs on a **new, separate multi-page engine** at `WebsiteDemos/generator/multipage/`:

| File | What it is |
|---|---|
| `build.py` | The engine — shared header/footer/nav/hero/CTA/widget components, per-page templates, theme tokens, schema builders, relative-depth link resolution |
| `content_core.py` / `content_services.py` / `content_industries.py` / `content_team.py` / `content_guides.py` | The site model — page data + content, one module per section |
| `qa.py` | QA harness (§5.3 passes 2, 4, 6, 9 mechanical parts) — links, headings, meta, schema, NAP, orphans, banned claims, AI-tell screen |
| `contrast.py` | WCAG AA audit, 34 foreground/background pairs |
| `shots.py` | 390px mobile + 1440px desktop capture with horizontal-overflow assertion |
| `render_assets.py` | og.png (1200×630) + apple-touch-icon.png (180×180) via headless Chromium |
| `../../logo/marks.py`, `sheet.py` | The four identity concepts explored, and the comparison sheet that stress-tested each at header / 32px / 16px / reversed / one-colour |

The engine **inherits** the `gen_sites.py` design system rather than forking it: same component and token architecture, same token names (`--ink/--ink2/--acc/--accd/--accrgb/--cream`), same card/hero/strip/CTA/footer/widget components, same breakpoints (920/860/560), same `prefers-reduced-motion` handling. New theme (navy `#142A44` / bronze `#B98D43`) and the Source Serif 4 heading face are local to this build — `gen_sites.py` and its six trade themes are untouched, so the single-page hook tool still ships Fraunces unless you want that changed too (say the word and I'll swap it there as well).

Re-runnable for the next build: swap the content modules, keep the engine.

## 3. Data sources ingested (§3.0)

| Channel | Result |
|---|---|
| (a) Google Business Profile | Downers Grove listing found: NAP, hours, **3.9★ / 15 reviews**. No separate Chicago GBP exists. |
| (b) Facebook-only | N/A — they have real websites |
| (c) **Existing websites** | **Both** mined in full. `kpwcpa.com` (5 pages) and `kpwcpachicago.com` (14 pages, © 2015 — HTTPS broken, raw fetch blocked, pulled via Chrome). Every service, bio, credential, address, phone, fax, and email extracted. |
| (d) Contact enrichment | Partner emails recovered from their own site (kpeterson@, meckel@, Chicago@) |

**The Chicago office was only discoverable on the old site.** `kpwcpa.com` shows one address and never mentions Chicago; `kpwcpachicago.com/contact.php` carries the West Loop address, both fax numbers, and nine service pages that do not exist on the current site. The new build is a strict **superset** of both.

### The honesty decision you should know about
Their Google rating is **3.9★ across 15 reviews**. That is real but it is not a selling asset, so per §5.2 ("real numbers only, or omit") **the build shows no star rating anywhere and emits no AggregateRating/Review schema.** Trust is carried instead by the peer-review and credential story, which is far stronger for a CPA firm. A QA gate now fails the build if rating markup ever appears.

**Recommend to the client separately:** claim/create a Chicago GBP (none exists — a free local-search asset they are simply not using), and work the Downers Grove rating up before surfacing it.

## 4. QA — all nine passes (§5.3)

| # | Pass | Method | Result |
|---|---|---|---|
| 1 | Grammar / style / readability | Independent adversarial reviewer over all 35 pages | **PASS** — 12 findings, all fixed |
| 2 | Factual / claims accuracy | Every assertion checked against `RESEARCH_NOTES.md` | **PASS** — 23 findings, all fixed or removed (§5 below) |
| 3 | E-E-A-T / Helpful-Content | Sourced credentials only; no thin or spun content; every page answers a real question | **PASS** |
| 4 | Keyword + AEO coverage | Question-first answers, FAQ blocks on 21 pages, 3 long-form guides on mined question clusters | **PASS** |
| 5 | AI-tell removal | Automated 20-phrase screen + reviewer voice pass + cross-page repetition audit | **PASS** — 8 findings fixed |
| 6 | Technical validation | 35/35 exactly one H1, clean heading hierarchy, all JSON-LD parses, **0 broken links, 0 orphan pages** | **PASS** |
| 7 | Accessibility / WCAG AA | 34 contrast pairs, all ≥4.5:1 (one footer colour corrected from 3.40 → passing); alt text on all images; visible focus rings; `aria-expanded` on nav and widget | **PASS — 0 fails** |
| 8 | Mobile 390px + desktop 1440px | 22 full-page captures with programmatic horizontal-overflow assertion | **PASS — 0 overflow** |
| 9 | NAP / brand consistency | Automated: any phone number outside the four real ones fails the build | **PASS** |

Final gate run: **0 fails, 0 warnings** across all 35 pages.

## 5. Content-accuracy work worth flagging

An independent adversarial reviewer checked every factual claim against the research file. **23 factual and 10 technical issues were found and fixed** before this reached you. The full list is in `RESEARCH_NOTES.md` §8a. The ones that mattered most:

- **"The firm's home since 1974"** — the source supports the founding *year*, not the founding *location*. The GBP identifies 1400 Opus Place as a **Regus serviced suite**, which makes continuous 52-year occupancy almost certainly false and trivially contradictable by the client. Removed.
- **"Help with controlling inventory"** as audit scope — verbatim from their own site, but it describes a *management* function that would raise an **auditor-independence question** under the AICPA Code. Rewritten as inventory observation, with the advisory items moved to a separately-engaged advisory paragraph. This one was worth catching before a CPA read it.
- **"the AICPA code of conduct governs our Illinois licenses"** — Illinois licensure runs through the Illinois Public Accounting Act and IDFPR rules. Legally inaccurate as written; corrected.
- **"the AICPA sets audit standards"** — true for non-issuers only; PCAOB sets them for public-company audits. Qualified.
- **AICPA "more than 330,000 members"** — verbatim from their 2015 page, now stale by roughly 100,000. Number removed rather than updated.
- Invented statistics removed: an industry-average tenure comparison, "thousands of engagements," "a century and a half of combined practice" (the real figure is ~250 years), and "two recessions since 1974" (there have been at least six).
- **"2,000+ clients"** was silently converted to a 52-year cumulative total in two places. Their site states a *present* count. Time qualifier removed.
- Invented biography removed — a founding motive for Mr. Kolnicki, and a claim that Mr. Wirth advises "the second generation of families he began working with."

### Three items need the client's confirmation before launch
1. **Monthly newsletters and the tax seminar series.** Sourced verbatim — from the **2015** site. Advertising a programme that may have ended a decade ago generates inbound requests they cannot fill. Currently removed from the build.
2. **The published fee policy — RESOLVED 2026-07-30.** Verified verbatim on kpwcpa.com/services ("Fair Prices" pillar): *"we believe in offering fair and transparent prices with no hidden fees or extra charges."* That wording is theirs and is used as-is. Separately, ~20 instances of **"we quote before the work starts"** were removed — their site says nothing about quoting timing, and I had extrapolated an operational practice from a pricing philosophy. `qa.py` now fails the build on any quoting-timing phrasing.
3. **Depth of the real estate & construction practice.** Both appear in the source only as *M&A transaction* industries. That page now leads with the sourced basis (facilities taxation, leasing, M&A experience) and presents bonding/job-costing as industry considerations rather than claimed service lines. If they do run a contractor practice, the page can be strengthened considerably.

## 6. Technical SEO / AEO shipped (§6)

- **Per-page** unique title, meta description, self-referencing canonical, full Open Graph set (with 1200×630 `og.png`), Twitter `summary_large_image`, `theme-color`, inline SVG favicon + `apple-touch-icon.png`.
- **JSON-LD:** `AccountingService` with **both office locations**, `WebSite`, `Service` (×12), `FAQPage` (×21 — distinct question sets, no duplication), `Person` (×6, with `alumniOf`, `honorificSuffix`, `worksFor`), `BreadcrumbList` on every deep page, `Article` on the guides, `ItemList` on hubs. **No AggregateRating/Review** (§3 above).
- **Hub-and-spoke internal linking** — services ↔ industries ↔ team ↔ locations ↔ guides. Zero orphans, verified programmatically.
- **AEO:** every service, industry, and guide page opens with a "short answer" block, then detail. 21 pages carry structured FAQ markup fed from mined question clusters (CPA cost, audit vs. review vs. compilation, choosing a firm, S corporations, valuation purpose, benefit plan selection).
- **Core Web Vitals:** static HTML, one shared stylesheet, ~4 KB of vanilla JS, no frameworks, no external calls except Google Fonts.

## 7. Staging posture — verified (§10.1)

| Layer | State |
|---|---|
| 1. Per-page meta | ✅ `noindex, nofollow` + `googlebot` on **35/35** pages |
| 2. `robots.txt` | ✅ Already covered by the live `Disallow: /test-builds/` |
| 3. `X-Robots-Tag` | ⚠️ **Action needed — see §8** |
| 4. Unlinked | ✅ Not referenced from any public page or sitemap |

Canonicals: 35/35 point at `scalelocal.net/test-builds/kpw-cpa/`, correct for staging. **All of these invert at cutover** (§9).

## 8. What you need to do

1. **Deploy:** the build is at `scalelocal-website\test-builds\kpw-cpa\`. Run `deploy.bat`.
2. **Widen the `X-Robots-Tag` header** — this is the outstanding §10.1 layer-3 item from the handoff, and it now matters because this build has assets (`og.png`, icons) directly hittable. In `scalelocal-website\vercel.json`, **replace** the `/test-builds/ns-builders/(.*)` entry with:
   ```json
   {
     "source": "/test-builds/(.*)",
     "headers": [
       { "key": "X-Robots-Tag", "value": "noindex, nofollow" }
     ]
   }
   ```
3. **Check the bare URL resolves.** A new `test-builds/{company}/` folder may need a trailing-slash redirect + directory rewrite in `vercel.json` — copy the `tnj-landscape` pattern.
4. **Review the three client-confirm items** in §5.

## 9. Cutover checklist (§2.1 — for when they approve)

Production is a **separate Vercel project on their own domain** — not a folder in `scalelocal-website`, and **no redirect** from `/test-builds/`.

- [ ] Rewrite every absolute URL to the client domain: canonicals, `og:url`, `og:image`, JSON-LD `url`/`@id`, sitemap
- [ ] Remove `noindex, nofollow` from all 35 pages; `robots.txt` → `Allow: /` + real `Sitemap:` line
- [ ] No `X-Robots-Tag` on the client domain
- [ ] Generate `sitemap.xml` (35 URLs, client-domain, `lastmod`)
- [ ] **Grep the built files for `scalelocal.net` and `test-builds` — require zero matches**
- [ ] New dedicated Vercel project; client points A record (apex) / CNAME (www)
- [ ] Verify the client domain in Google Search Console, submit the sitemap, request indexing on Home / Services / both Locations
- [ ] Delete the staging copy

The engine takes `BASE` as a single constant — the URL rewrite is a one-line change plus a rebuild, and `qa.py` can be extended with the residue grep as a hard gate.

## 10. Known limitations

- **No photographs.** They have none on either site and none on the GBP. The build uses the designed gradient hero + line-art glyph fallback rather than stock imagery implying their offices or staff (guardrail #9). **Real photos of the partners and both offices would materially improve this site** — headshots especially, since the team pages are the strongest asset here.
- **Logo is a PROPOSAL, not their existing mark.** Their real identity is a photographed door plaque (circular K/P/W badges, purple on brushed metal) — unusable on the web. Matt directed a designed alternative. The build ships the "Ruled Lettermark": KPW between two hairlines, the typographic language of a certificate or audit opinion. No container shape, no gradient, one-colour safe, with a simplified single-letter "K" variant for favicon sizes where three letters turn to mush. **The demo must not be presented as their current logo.**
- **Chicago office removed 2026-07-30.** The firm no longer has a Chicago location. Every trace was stripped: the location page deleted, the address/phone/fax/email retired, header, footer, chat widget, CTA buttons, JSON-LD `location` array, nav label, hero trust strip, page titles and meta, and the West Loop framing on the litigation-support and business-management pages. `qa.py` now hard-fails on `954 W Washington`, `(312) 421`, `West Loop`, `Chicago office`, `two offices`, `both offices`, `either office` and the retired phone numbers, and `ALLOWED_PHONES` is narrowed to the two Downers Grove numbers. **Deliberately kept:** "University of Chicago" and "Chicago Circle" (real partner education) and "Chicagoland"/"Chicago metropolitan area" (accurate service area). **Flag for the client:** their kpwcpachicago.com site still advertises the closed office.
- **Interactive Google Map added 2026-07-30.** On the home, contact and location pages. Uses the keyless `maps.google.com/?output=embed` endpoint — fully interactive (pan, zoom, Street View, Directions) with no API key and no billing account, so nothing to configure at cutover. Lazy-loaded, 16:9 on desktop and 4:3 on mobile, with a descriptive `title` for screen readers; `qa.py` now fails any iframe missing one. `hasMap` and `geo` coordinates added to the LocalBusiness JSON-LD.
- **Their own strongest claims added 2026-07-30.** Two sourced lines were found during verification but initially left out: the Quality-pillar guarantee ("We won't stop until you're 100% satisfied – that's a guarantee") and the home-page availability claim ("We guarantee fast and discrete handling of all your accounting needs. Our team of highly qualified CPA's can be available day and night"). Both are verbatim theirs and are now on the home, about, and contact pages plus the hero trust strip. The hedge "can be available" is preserved.
- **Chat launcher restyled 2026-07-30.** It was navy on a navy hero and disappeared. Now bright gold `#E8B33F` with navy text: 7.58:1 for the label, 6.69:1 against the hero backdrop, both well past AA. Hover lifts to `#F5C453` (8.93:1). Panel border matches so the open widget reads as one object.
- **Book button is a stub.** Call and text work as `tel:`/`sms:`; the Book action only reveals a "call or email to arrange one" note. Nothing on the site implies it schedules anything (guardrail #5).
- **No client testimonials.** Neither site carries any, and Google reviews are not being surfaced per §3. If they can supply attributable client quotes, there is a natural place for them on the home page and the industry pages.
