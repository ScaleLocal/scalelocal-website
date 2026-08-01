# Build spec — how to add a firm to the engine

Read this fully before writing anything. `firms/kpw_cpa.py` plus `content_core.py`
are the worked reference; copy their shape.

## Files you own

You may create/edit **only** these two files:

- `firms/<slug_underscored>.py` — firm profile (facts, theme, nav, logo, QA gates, `pages()`)
- `content_<slug_underscored>.py` — the page content

**Do not edit** `build.py`, `qa.py`, `contrast.py`, `layout_audit.py`, `shots.py`,
`calculators.py`, or any `content_core/services/industries/team/guides.py`.
Other agents are working in this repo at the same time. Touching shared files
breaks their builds.

## Build and verify

```
BUILD_FIRM=<slug> python3 build.py
BUILD_FIRM=<slug> python3 qa.py
BUILD_FIRM=<slug> python3 contrast.py
BUILD_FIRM=<slug> timeout 600 python3 layout_audit.py
```

**You are not done until all four are green** — QA `RESULT: PASS` with 0 fails and
0 warnings, contrast `FAILS: 0`, layout GATE A and GATE B both PASS. Iterate until
they are. Report the final output of each.

## `firms/<slug>.py` — required exports

```python
FIRM = dict(
    name='...',              # exact legal name; may contain '&' — engine escapes it
    short='...',             # 2-6 char short name for the chat widget
    founded=2008, years=18,  # omit years if unknown
    email='...',
    addr='...', city='...', state='MA', state_full='Massachusetts', zip='...',
    tel='+1978...',          # E.164, used in tel: links
    ph='(978) 555-1212', fax='...',
    hours='Mon&ndash;Fri 9:00 AM&ndash;5:00 PM',
    maps='https://www.google.com/maps/search/?api=1&query=<urlencoded+name+and+address>',
    office_page=None,        # or 'locations/<slug>.html' if you build one
    favicon_letter='H',      # single letter — multi-letter marks blur at 16px
    brand_line='Firm Name',  # header wordmark; use &amp; for ampersands
    brand_sub='Certified Public Accountants',
    nav_cta='Talk to a CPA',
    topbar='... &middot; City, ST &middot; Est. 1974',
    footer_blurb='One sentence, under 40 words.',
    footer_note=None,        # optional second line, e.g. memberships
    footer_services=[('services/x.html','Label'), ...],   # 5-6 entries
    footer_firm=[('about.html','About the firm'), ...],   # 5-6 entries
)

T = dict(ink='#RRGGBB', ink2='#RRGGBB', acc='#RRGGBB', accd='#RRGGBB',
         accrgb='r,g,b', cream='#RRGGBB')

NAV = [('services/index.html','Services','services'), ..., ('contact.html','Contact','contact')]

LOGO = '<svg viewBox="0 0 64 64" ...>...</svg>'   # see LOGO rules below

ALLOWED_PHONES = ['(978) 555-1212', ...]   # every phone that may appear in output
BANNED = [...]                             # firm-specific forbidden strings

def pages():
    import content_<slug>
    return content_<slug>.pages()
```

## Page dicts

`pages()` returns a list of dicts:

```python
dict(path='services/tax.html',   # relative to out/<slug>/
     depth=1,                    # number of directories deep; 0 for root pages
     nav='services',             # matches the 3rd element of a NAV entry, for aria-current
     title='... | Firm',         # <= 72 chars
     desc='...',                 # 70-175 chars, unescaped
     eyebrow='Services', h1='...', sub='...',
     body='<section>...</section>',   # full HTML
     schema=[...],                    # list of JSON-LD dicts
     cta_args=())                     # optional (title, text) for the closing CTA
```

Import helpers from `build`:

```python
from build import (FIRM, BASE, T, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   org_schema, breadcrumb_schema, faq_schema, service_schema)
```

`phero(p, crumbs)` renders the page hero + breadcrumbs; `crumbs` is a list of
`(label, url_or_None)`. Call it as the first thing in `body`.

## Hard rules — these are QA-gated

1. **Exactly one `<h1>` per page**, supplied via `h1`. Headings must not skip levels.
2. **`title` <= 72 chars. `desc` 70-175 chars.** Both are checked.
3. **Every `<img>` needs alt text. Every `<iframe>` needs `title` and `loading="lazy"`.**
   Use `gmap()` for maps — it already complies.
4. **No rating or review markup.** No stars, no AggregateRating, no "5-star".
5. **Only phones in `ALLOWED_PHONES` may appear anywhere.**
6. **No orphan pages** — every page must be linked from somewhere.
7. **Container balance**: every `<div>`/`<section>` you open must close. Layout GATE A
   walks nesting depth and fails on any negative or non-zero final depth. This is the
   single most common way a build breaks — count your closing tags.
8. **Content blocks must sit inside `<section class="sec"><div class="wrap">`.**
   GATE B measures real geometry and fails anything outside the gutter.
9. **Wide tables**: use `<table class="plain">`. The engine wraps it in a scroll
   container automatically. Do not hand-roll wide layouts.

## Honesty rules — non-negotiable

**Every factual claim must come from the firm's own website, or be something you can
cite.** This is a demo sent to the firm itself; they will spot an invented fact
instantly and it costs the whole campaign.

- Do not invent founding years, staff counts, client counts, credentials, awards,
  memberships, specialisms, or years of experience.
- If the audit says a credential was not found, **do not assert one**. A firm that
  never claims CPA on its own site must not be called a CPA firm.
- Do not claim the firm quotes fees before work starts, or any other operational
  promise, unless their site says so.
- Preserve the firm's own hedged wording where they hedge.
- Where a fact is unknown, write around it rather than filling it in.

Put anything you deliberately left out, or that the client must confirm, in a
`RESEARCH_<slug>.md` note at the end.

## Calculators

`import calculators as C` gives you `C.CALCULATORS` (8 verified calculators),
`C.CATEGORIES`, `C.CALC_CSS`, `C.CALC_JS`, and `C.calc_page_body(...)`.

Only add calculator pages if the firm currently has calculators (the research note
says so). Build a hub at `calculators/index.html` plus one page per calculator,
and append `C.CALC_CSS` into your page via a `<style>` block in the body and
`C.CALC_JS` at the end of the body.

## Logo rules

You are designing a real mark, not a placeholder. It is presented to the firm as a
**proposal**, never as their existing logo.

- Pure inline SVG on a 64x64 viewBox, `fill="currentColor"` so it inherits theme colour.
- No external fonts inside the SVG beyond the `.mark svg text` rule the engine sets
  (it applies the site serif). Do not put `font-family` inside the SVG string —
  quoting breaks the Python literal.
- It must read at 50px in the header and as a single letter at 16px in the favicon.
- Avoid: generic bar charts, generic upward arrows, clip-art buildings, dollar signs,
  swooshes. Those read as clip art and will be rejected.
- Good directions: a ruled lettermark (hairlines above and below the initials, like a
  ledger rule); a monogram built from the initials with one considered join; a
  geometric mark derived from something specific to the firm.
- Test it: does it still look deliberate in one flat colour at 20px? If not, simplify.

## Site size

Right-size to the firm. A sole practitioner with a five-page site should get roughly
14-18 pages; a six-partner firm can carry 30+. Padding a small firm with thin pages
looks worse than a tight small site. Every page must justify itself.

Typical shape: home, about, services hub + one page per real service, team (only if
the firm names people), FAQ, contact, plus 2-3 genuine guides written for this firm's
actual clients, plus calculators where applicable.
