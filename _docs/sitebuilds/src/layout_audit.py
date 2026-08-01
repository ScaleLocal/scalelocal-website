# -*- coding: utf-8 -*-
"""
QA pass #9b - site-wide LAYOUT audit.

Two independent gates, because the contact-page bug slipped past every
existing check (valid HTML fragments, no overflow, all links fine):

  GATE A  structural: div/section nesting depth must never go negative and
          must return to exactly 0 at </body>. Catches orphaned or surplus
          containers - the actual root cause.

  GATE B  geometric: load every page in Chromium at 1440px and 390px and
          measure the real box of every major content block. Any block that
          sits outside the .wrap gutter, or spans wider than the site's
          max-width, is a deadzone/left-flush bug.
"""
import os, re, sys, asyncio, json
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', os.environ.get('BUILD_FIRM','kpw-cpa'))

PAGES = []
for dp, dn, fn in os.walk(ROOT):
    for f in sorted(fn):
        if f.endswith('.html'):
            PAGES.append(os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/'))
PAGES.sort()

# ---------------------------------------------------------------- GATE A
TAG = re.compile(r'<(/?)(div|section|main|header|footer|nav|article|aside)\b[^>]*?(/?)>', re.I)
VOID_OK = ('br', 'img', 'input', 'meta', 'link', 'hr', 'source')


def gate_a():
    fails = []
    for p in PAGES:
        html = open(os.path.join(ROOT, p), encoding='utf-8').read()
        body = html.split('<body', 1)[-1]
        depth, worst, line = 0, 0, None
        for m in TAG.finditer(body):
            closing, self_close = m.group(1), m.group(3)
            if self_close:
                continue
            depth += -1 if closing else 1
            if depth < worst:
                worst = depth
                line = body[max(0, m.start() - 60):m.start() + 60].replace('\n', ' ')
        if depth != 0:
            fails.append((p, 'unbalanced containers: final depth %d (expected 0)' % depth, line))
        elif worst < 0:
            fails.append((p, 'nesting went negative (depth %d) - surplus closing tag' % worst, line))
    return fails


# ---------------------------------------------------------------- GATE B
PROBE = r"""
() => {
  const vw = window.innerWidth;
  const wraps = [...document.querySelectorAll('.wrap')];
  // reference gutter: where a known-good .wrap starts
  const ref = wraps.length ? wraps[0].getBoundingClientRect() : null;
  const sel = '.prose, .sec-head, .split, .cards, .grid, .faq, .offices, .mapwrap, .aside, .acard, .cta .wrap, .steps, .tbl';
  const out = [];
  document.querySelectorAll(sel).forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;           // hidden
    // is it inside a .wrap (or is a .wrap itself)?
    const inWrap = !!el.closest('.wrap');
    out.push({
      cls: el.className.toString().slice(0, 60),
      tag: el.tagName.toLowerCase(),
      left: Math.round(r.left), right: Math.round(r.right),
      width: Math.round(r.width), inWrap,
      text: (el.textContent || '').trim().slice(0, 45)
    });
  });
  const h1 = document.querySelector('h1');
  let head = null;
  if (h1) {
    const hr = h1.getBoundingClientRect();
    const host = h1.closest('.wrap') || document.body;
    const cr = host.getBoundingClientRect();
    head = {w: Math.round(hr.width), host: Math.round(cr.width),
            lines: Math.round(hr.height / (parseFloat(getComputedStyle(h1).lineHeight) || 1)),
            text: (h1.textContent || '').trim().slice(0, 40)};
  }
  return {vw, ref: ref ? {left: Math.round(ref.left), width: Math.round(ref.width)} : null, out, head};
}
"""


async def gate_b():
    fails, warns = [], []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for w, h in ((1440, 900), (390, 844)):
            pg = await b.new_page(viewport={'width': w, 'height': h})
            # the sandbox has no route to maps.google.com; abort external requests
            # so the map iframe does not stall page load.
            await pg.route(re.compile(r'^https?://'), lambda r: asyncio.ensure_future(r.abort()))
            for p in PAGES:
                await pg.goto('file://' + os.path.join(ROOT, p), wait_until='domcontentloaded')
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                sw = await pg.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
                if sw > w + 1:
                    fails.append('%dpx %s :: document scrollWidth %d exceeds viewport' % (w, p, sw))
                d = await pg.evaluate(PROBE)
                # GATE C - a squeezed heading. A hero h1 rendered into a sliver of its
                # container means a composition rule is fighting the markup.
                hd = d.get('head')
                if hd and w >= 1000 and hd['host'] > 0:
                    frac = hd['w'] / hd['host']
                    if frac < 0.34 and hd['lines'] >= 4:
                        fails.append('%dpx %s :: h1 is %d%% of its container over %d lines - squeezed - "%s"'
                                     % (w, p, round(frac * 100), hd['lines'], hd['text']))
                if not d['ref']:
                    continue
                gutter = d['ref']['left']
                for e in d['out']:
                    if not e['inWrap']:
                        fails.append('%dpx %s :: <%s class="%s"> is OUTSIDE any .wrap - "%s"'
                                     % (w, p, e['tag'], e['cls'], e['text']))
                        continue
                    # a block inside .wrap must never start left of the gutter
                    if e['left'] < gutter - 2:
                        fails.append('%dpx %s :: .%s starts at x=%d, gutter is x=%d - "%s"'
                                     % (w, p, e['cls'], e['left'], gutter, e['text']))
                    # ...nor run past the right gutter
                    if e['right'] > d['vw'] - gutter + 2:
                        warns.append('%dpx %s :: .%s ends at x=%d, expected <= %d'
                                     % (w, p, e['cls'], e['right'], d['vw'] - gutter))
            await pg.close()
        await b.close()
    return fails, warns


if __name__ == '__main__':
    print('LAYOUT AUDIT over %d pages\n' % len(PAGES))

    a = gate_a()
    print('GATE A  container nesting .......... %s' % ('FAIL (%d)' % len(a) if a else 'PASS'))
    for p, why, ctx in a:
        print('   FAIL %-42s %s' % (p, why))
        if ctx:
            print('        near: %s' % ctx.strip())

    bf, bw = asyncio.run(gate_b())
    print('\nGATE B/C block geometry + headings . %s' % ('FAIL (%d)' % len(bf) if bf else 'PASS'))
    for f in bf[:40]:
        print('   FAIL %s' % f)
    if len(bf) > 40:
        print('   ... +%d more' % (len(bf) - 40))
    if bw:
        print('\n  %d right-edge warnings (usually full-bleed by design):' % len(bw))
        for f in bw[:10]:
            print('   WARN %s' % f)

    sys.exit(1 if (a or bf) else 0)
