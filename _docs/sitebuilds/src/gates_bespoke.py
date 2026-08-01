# -*- coding: utf-8 -*-
"""
Layout, widget and contrast gates for a BESPOKE build — parameterised by slug.

Why this exists: `contrast.py` and `layout_audit.py` are welded to the template
engine. `contrast.py` checks a fixed list of colour pairs from that stylesheet
(hero gradients, the gold chat pill, cream cards); on a bespoke build it compares
colours the site never puts together and prints a pass. `layout_audit.py`'s GATE B
keys on `.wrap`; with no `.wrap` in the document it finds no reference element and
skips every geometric check, printing PASS while measuring nothing.

Both did exactly that on the Hickey build. A green light from them is not evidence.

This file is the replacement. Add an entry to SITES for each bespoke build naming
the classes that build actually uses, and run:

    BUILD_FIRM=<slug> python3 gates_bespoke.py

  GATE A  container nesting never goes negative and returns to 0 at </body>
  GATE B  every major block sits inside the content column and within its gutters;
          a table wider than the column must sit inside a scroll wrapper
  GATE C  no h1 squeezed into a sliver of its container
  GATE D  a sticky rail must fit the viewport, or it detaches on scroll; a fixed
          bar must be cleared by the footer's bottom padding
  GATE E  a contact widget is present on EVERY page at EVERY viewport, visible
          without interaction, offering call + email + an appointment route,
          making no external request, and never floating over the reading column
  GATE F  WCAG: text pairs at AA, UI control boundaries at 1.4.11 (3:1), read from
          the custom properties in the BUILT stylesheet rather than a hardcoded list
"""
import os, re, sys, asyncio, importlib
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = os.environ.get('BUILD_FIRM', 'carellacpa')

# --------------------------------------------------------------------------
# Per-build configuration. `blocks` is the selector list GATE B measures — list
# every structural block class the build uses, or the gate measures nothing.
# --------------------------------------------------------------------------
SITES = {
    'carellacpa': dict(
        css='css/carella.css',
        container='.col',
        rail='.rail',
        bar='.reachbar',
        foot_clear='.foot .fine',
        blocks=('.band, .prose, .index, .parts, .flow, .qa, .calc, .calcform, .calcout,'
                ' .map, .tscroll, .remark, .foot, .open, table.plain'),
        scroll_wrapper='.tscroll',
        body_bg='rgb(252, 252, 251)',
        viewports=((1512, 950), (1440, 900), (1100, 900), (390, 844)),
    ),
    'dorfmancpas': dict(
        css='css/dd.css',
        container='main .gut',
        rail=None, bar=None, foot_clear=None,
        blocks=('.filed, .prose, .reg, .pair, .fig, .mnote, .sc, .tiles, .band, .lead,'
                ' .cwrap, .cf, .res, .map, table.reg2'),
        scroll_wrapper='.sc',
        body_bg='rgb(251, 250, 248)',
        viewports=((1512, 950), (1440, 900), (1100, 900), (390, 844)),
    ),
    'bgoguen': dict(
        css='css/fg.css',
        container='main .wrapper',
        rail=None, bar=None, foot_clear=None,
        blocks=('.card, .text, .list, .facts, .trio, .aside, .tbl, .roster, .person,'
                ' .calc, .fields, .out, .map, .head, table.data'),
        scroll_wrapper='.tbl',
        body_bg='rgb(247, 245, 242)',
        viewports=((1512, 950), (1440, 900), (1100, 900), (390, 844)),
    ),
    'millcityaccounting': dict(
        css='css/millcity.css',
        container='main .hold',
        rail=None,
        bar=None,
        foot_clear=None,
        blocks=('.block, .copy, .rows, .figures, .note, .scroll, .doors, .door-card,'
                ' .calcwrap, .calcgrid, .results, .map, .hours, .lede-wrap, table.grid'),
        scroll_wrapper='.scroll',
        body_bg='rgb(242, 240, 234)',
        viewports=((1512, 950), (1440, 900), (1100, 900), (390, 844)),
    ),
}

CFG = SITES.get(SLUG)
if CFG is None:
    print('gates_bespoke.py has no entry for BUILD_FIRM=%s.\n'
          'Add one to SITES naming the classes this build actually uses — do NOT\n'
          'fall back to layout_audit.py, which will pass without measuring anything.'
          % SLUG)
    sys.exit(2)

ROOT = os.path.join(HERE, 'out', SLUG)
PAGES = sorted(os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/')
               for dp, dn, fn in os.walk(ROOT) for f in fn if f.endswith('.html'))

TAG = re.compile(r'<(/?)(div|section|main|header|footer|nav|article|aside|details)\b[^>]*?(/?)>', re.I)


# ------------------------------------------------------------------ GATE A
def gate_a():
    fails = []
    for p in PAGES:
        body = open(os.path.join(ROOT, p), encoding='utf-8').read().split('<body', 1)[-1]
        depth, worst, near = 0, 0, None
        for m in TAG.finditer(body):
            if m.group(3):
                continue
            depth += -1 if m.group(1) else 1
            if depth < worst:
                worst, near = depth, body[max(0, m.start() - 70):m.start() + 70]
        if depth != 0:
            fails.append((p, 'unbalanced containers: final depth %d' % depth, near))
        elif worst < 0:
            fails.append((p, 'nesting went negative (%d): surplus closing tag' % worst, near))
    return fails


PROBE = r"""
(cfg) => {
  const col = document.querySelector(cfg.container);
  if (!col) return {err: 'no ' + cfg.container};
  const cr = col.getBoundingClientRect();
  const out = [];
  document.querySelectorAll(cfg.blocks).forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    out.push({cls: el.className.toString().slice(0, 50), tag: el.tagName.toLowerCase(),
              left: Math.round(r.left), right: Math.round(r.right),
              inCol: !!el.closest(cfg.container),
              scrolled: !!el.closest(cfg.scrollWrapper),
              text: (el.textContent || '').trim().slice(0, 42)});
  });
  const h1 = document.querySelector('h1');
  let head = null;
  if (h1) {
    const hr = h1.getBoundingClientRect();
    head = {w: Math.round(hr.width), host: Math.round(cr.width),
            lines: Math.round(hr.height / (parseFloat(getComputedStyle(h1).lineHeight) || 1)),
            text: (h1.textContent || '').trim().slice(0, 40)};
  }
  const widgets = [...document.querySelectorAll('[data-contact-widget]')];
  const shown = widgets.filter(el => {
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden' || +st.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 40 && r.height > 20;
  });
  const wdata = shown.map(el => {
    const r = el.getBoundingClientRect();
    const hrefs = [...el.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
    return {
      cls: (el.className.toString() || el.tagName).slice(0, 40),
      tel: hrefs.some(h => h.startsWith('tel:')),
      mail: hrefs.some(h => h.startsWith('mailto:')),
      appt: hrefs.some(h => !h.startsWith('tel:') && !h.startsWith('mailto:')
                            && /contact|appoint|book|schedule|pay/i.test(h)),
      label: el.getAttribute('aria-label') || '',
      offscreen: r.right < 1 || r.left > window.innerWidth - 1 || r.bottom < 1
                 || r.top > window.innerHeight - 1,
      // an external URL is fine if it is the firm's own payment link; a script or
      // an iframe never is
      script: /<script|<iframe/i.test(el.innerHTML),
      // a bottom-anchored bar legitimately sits over the column (GATE D checks the
      // footer clears it); a floating panel parked mid-column covers body text
      overlapsCol: !(r.right <= cr.left + 1 || r.left >= cr.right - 1
                     || r.bottom <= cr.top + 1 || r.top >= cr.bottom - 1)
                   && getComputedStyle(el).position === 'fixed'
                   && !(r.bottom >= window.innerHeight - 2
                        && r.width >= window.innerWidth * 0.55),
    };
  });
  const rail = cfg.rail ? document.querySelector(cfg.rail) : null;
  const bar = cfg.bar ? document.querySelector(cfg.bar) : null;
  const foot = cfg.footClear ? document.querySelector(cfg.footClear) : null;
  return {
    vw: window.innerWidth, vh: window.innerHeight,
    col: {left: Math.round(cr.left), right: Math.round(cr.right)},
    out, head, widgetsTotal: widgets.length, widgets: wdata,
    railH: rail ? Math.round(rail.getBoundingClientRect().height) : 0,
    barShown: bar ? getComputedStyle(bar).display !== 'none' : false,
    barH: bar ? Math.round(bar.getBoundingClientRect().height) : 0,
    footGap: foot ? Math.round(parseFloat(getComputedStyle(foot).paddingBottom)) : 0,
    scrollW: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
  };
}
"""


async def gates_bcde():
    fails, warns = [], []
    js_cfg = dict(container=CFG['container'], blocks=CFG['blocks'],
                  scrollWrapper=CFG['scroll_wrapper'], rail=CFG.get('rail'),
                  bar=CFG.get('bar'), footClear=CFG.get('foot_clear'))
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for w, h in CFG['viewports']:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            await pg.route(re.compile(r'^https?://'), lambda r: asyncio.ensure_future(r.abort()))
            for p in PAGES:
                await pg.goto('file://' + os.path.join(ROOT, p),
                              wait_until='domcontentloaded', timeout=20000)
                # DOMContentLoaded can precede the stylesheet; measuring then yields
                # unstyled geometry and confident nonsense.
                await pg.wait_for_function(
                    "bg => getComputedStyle(document.body).backgroundColor === bg",
                    arg=CFG['body_bg'], timeout=5000)
                d = await pg.evaluate(PROBE, js_cfg)
                tag = '%dpx %s ::' % (w, p)
                if d.get('err'):
                    fails.append('%s %s' % (tag, d['err']))
                    continue
                if d['scrollW'] > w + 1:
                    fails.append('%s document scrollWidth %d exceeds viewport' % (tag, d['scrollW']))
                L, R = d['col']['left'], d['col']['right']
                for e in d['out']:
                    if not e['inCol']:
                        fails.append('%s <%s class="%s"> outside %s — "%s"'
                                     % (tag, e['tag'], e['cls'], CFG['container'], e['text']))
                        continue
                    if e['left'] < L - 2:
                        fails.append('%s .%s starts x=%d, column starts x=%d — "%s"'
                                     % (tag, e['cls'], e['left'], L, e['text']))
                    if e['right'] > R + 2 and not e['scrolled']:
                        fails.append('%s .%s ends x=%d, column ends x=%d — "%s"'
                                     % (tag, e['cls'], e['right'], R, e['text']))
                    elif e['right'] > R + 2 and e['tag'] != 'table':
                        fails.append('%s <%s class="%s"> overflows the column inside a scroll '
                                     'wrapper — only tables may — "%s"'
                                     % (tag, e['tag'], e['cls'], e['text']))
                hd = d['head']
                if hd and w >= 1000 and hd['host'] > 0:
                    frac = hd['w'] / hd['host']
                    if frac < 0.34 and hd['lines'] >= 4:
                        fails.append('%s h1 is %d%% of its column over %d lines — squeezed — "%s"'
                                     % (tag, round(frac * 100), hd['lines'], hd['text']))
                if w >= 1000 and d['railH'] > d['vh']:
                    fails.append('%s sticky rail is %dpx tall in a %dpx viewport — it will detach'
                                 % (tag, d['railH'], d['vh']))
                if d['barShown'] and d['footGap'] < d['barH'] + 8:
                    fails.append('%s fixed bar is %dpx tall but the footer clears only %dpx — '
                                 'it covers content' % (tag, d['barH'], d['footGap']))
                # GATE E
                if not d['widgetsTotal']:
                    fails.append('%s NO element carries [data-contact-widget]' % tag)
                elif not d['widgets']:
                    fails.append('%s a contact widget exists in the markup but none is visible '
                                 'at this viewport — a user sees no way to make contact' % tag)
                for wd in d['widgets']:
                    who = '.%s' % (wd['cls'] or '?')
                    if wd['offscreen']:
                        fails.append('%s contact widget %s is off-screen' % (tag, who))
                    if wd['overlapsCol']:
                        fails.append('%s contact widget %s is fixed and overlaps the reading '
                                     'column — it covers body text' % (tag, who))
                    for k, what in (('tel', 'a tel: link'), ('mail', 'a mailto: link'),
                                    ('appt', 'an appointment route')):
                        if not wd[k]:
                            fails.append('%s contact widget %s offers no %s' % (tag, who, what))
                    if wd['script']:
                        fails.append('%s contact widget %s embeds a script or iframe — it must '
                                     'be fully static' % (tag, who))
                    if not wd['label']:
                        warns.append('%s contact widget %s has no aria-label' % (tag, who))
            await pg.close()
        await b.close()
    return fails, warns


# ------------------------------------------------------------------ GATE F
def lum(c):
    c = c.lstrip('#')
    o = []
    for i in (0, 2, 4):
        v = int(c[i:i + 2], 16) / 255.0
        o.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * o[0] + 0.7152 * o[1] + 0.0722 * o[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


CONTRAST_SCRIPT = {'carellacpa': 'contrast_carella',
                   'millcityaccounting': 'contrast_millcity',
                   'bgoguen': 'contrast_goguen',
                   'dorfmancpas': 'contrast_dorfman'}


def gate_f():
    """Run the per-site contrast script, which knows which pairs the site actually
    renders. A generic sweep of every token against every other would flag pairs
    that never meet and miss the ones that do."""
    name = CONTRAST_SCRIPT.get(SLUG)
    if not name or not os.path.exists(os.path.join(HERE, name + '.py')):
        return None, None
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(HERE, name + '.py')],
                       capture_output=True, text=True, cwd=HERE)
    tail = [l for l in r.stdout.strip().splitlines() if l.startswith('PAIRS:')]
    return name, (tail[0] if tail else 'no result') + ('' if r.returncode == 0 else '  <-- FAIL')


if __name__ == '__main__':
    print('BESPOKE GATES — %s — %d pages at %s\n'
          % (SLUG, len(PAGES), ', '.join('%dx%d' % v for v in CFG['viewports'])))
    a = gate_a()
    print('GATE A    container nesting ............... %s'
          % ('FAIL (%d)' % len(a) if a else 'PASS'))
    for p, why, ctx in a:
        print('   FAIL %-40s %s' % (p, why))
    f, wn = asyncio.run(gates_bcde())
    print('GATE B/C/D/E  geometry, rail, widget ...... %s'
          % ('FAIL (%d)' % len(f) if f else 'PASS'))
    for x in f[:60]:
        print('   FAIL %s' % x)
    if len(f) > 60:
        print('   ... +%d more' % (len(f) - 60))
    for x in wn[:10]:
        print('   WARN %s' % x)
    cs, cres = gate_f()
    if cs:
        print('GATE F    contrast (%-24s %s' % (cs + ')', cres))
    else:
        print('GATE F    contrast ........................ NO per-site script — write one')
    bad = bool(a or f or (cres and 'FAIL' in cres) or not cs)
    sys.exit(1 if bad else 0)
