# -*- coding: utf-8 -*-
"""
Layout audit for the Carella build.

layout_audit.py's GATE B keys on `.wrap`, which is the template engine's container.
This build has no `.wrap`, so that gate finds no reference element and silently
skips every geometric check — it would report PASS while measuring nothing. This
is the same audit re-pointed at the class names this site actually uses, plus two
gates the original does not have.

  GATE A  container nesting never goes negative and returns to 0 at </body>
  GATE B  every major block sits inside the content column and within its gutters;
          a table wider than the column must sit inside a .tscroll wrapper
  GATE C  no h1 squeezed into a sliver of its container
  GATE D  the sticky rail is shorter than the viewport (otherwise it detaches),
          and the fixed contact bar never covers the last line of content
  GATE E  a contact widget is present, VISIBLE WITHOUT INTERACTION, and offers call,
          email and appointment on every page at every viewport — and makes no
          network call. This gate exists because the first version of this site had
          a widget that was technically present but read as navigation, so a human
          looking at the page concluded there wasn't one.

    python3 layout_carella.py
"""
import os, re, sys, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'carellacpa')
PAGES = sorted(os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/')
               for dp, dn, fn in os.walk(ROOT) for f in fn if f.endswith('.html'))

TAG = re.compile(r'<(/?)(div|section|main|header|footer|nav|article|aside|details)\b[^>]*?(/?)>', re.I)


def gate_a():
    fails = []
    for p in PAGES:
        html = open(os.path.join(ROOT, p), encoding='utf-8').read()
        body = html.split('<body', 1)[-1]
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
() => {
  const col = document.querySelector('.col');
  if (!col) return {err: 'no .col'};
  const cr = col.getBoundingClientRect();
  const sel = '.band, .prose, .index, .parts, .flow, .qa, .calc, .calcform, .calcout,' +
              ' .map, .tscroll, .remark, .foot, .open, table.plain';
  const out = [];
  document.querySelectorAll(sel).forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    out.push({cls: el.className.toString().slice(0, 50), tag: el.tagName.toLowerCase(),
              left: Math.round(r.left), right: Math.round(r.right),
              inCol: !!el.closest('.col'),
              // a wide table is allowed to exceed the column ONLY inside a scroll
              // wrapper; one without a wrapper pushes the whole document sideways
              scrolled: !!el.closest('.tscroll'),
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
  // GATE E — the contact widget, as a user actually encounters it
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
      external: /https?:\/\/|<script|<iframe/i.test(el.innerHTML),
      // does it sit on top of the reading column?
      // A bottom-anchored bar legitimately sits over the column; GATE D checks the
      // footer clears it. What is NOT acceptable is a floating panel parked in the
      // middle of the reading column, covering body text.
      overlapsCol: !(r.right <= cr.left + 1 || r.left >= cr.right - 1
                     || r.bottom <= cr.top + 1 || r.top >= cr.bottom - 1)
                   && getComputedStyle(el).position === 'fixed'
                   && !(r.bottom >= window.innerHeight - 2
                        && r.width >= window.innerWidth * 0.55),
    };
  });
  const rail = document.querySelector('.rail');
  const bar = document.querySelector('.reachbar');
  const foot = document.querySelector('.foot .fine');
  return {
    vw: window.innerWidth, vh: window.innerHeight,
    col: {left: Math.round(cr.left), right: Math.round(cr.right), width: Math.round(cr.width)},
    out, head,
    railH: rail ? Math.round(rail.getBoundingClientRect().height) : 0,
    barShown: bar ? getComputedStyle(bar).display !== 'none' : false,
    barH: bar ? Math.round(bar.getBoundingClientRect().height) : 0,
    footBottomGap: foot ? Math.round(parseFloat(getComputedStyle(foot).paddingBottom)) : 0,
    scrollW: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
    widgetsTotal: widgets.length, widgets: wdata,
  };
}
"""


async def gates_bcd():
    fails, warns = [], []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for w, h in ((1440, 900), (1100, 900), (390, 844)):
            pg = await b.new_page(viewport={'width': w, 'height': h})
            # no route to fonts.googleapis.com or maps.google.com in the sandbox;
            # aborting external requests stops the map iframe stalling page load
            await pg.route(re.compile(r'^https?://'), lambda r: asyncio.ensure_future(r.abort()))
            for p in PAGES:
                await pg.goto('file://' + os.path.join(ROOT, p), wait_until='domcontentloaded')
                # The Google Fonts <link> is aborted in the sandbox, and DOMContentLoaded
                # can fire before the local stylesheet has been applied. Measuring then
                # yields unstyled geometry and silently bogus results — wait for a value
                # that only the site stylesheet sets.
                await pg.wait_for_function(
                    "() => getComputedStyle(document.body).lineHeight !== 'normal'"
                    " && getComputedStyle(document.body).backgroundColor"
                    " === 'rgb(252, 252, 251)'", timeout=5000)
                d = await pg.evaluate(PROBE)
                if d.get('err'):
                    fails.append('%dpx %s :: %s' % (w, p, d['err']))
                    continue
                if d['scrollW'] > w + 1:
                    fails.append('%dpx %s :: document scrollWidth %d exceeds viewport'
                                 % (w, p, d['scrollW']))
                L, R = d['col']['left'], d['col']['right']
                for e in d['out']:
                    if not e['inCol']:
                        fails.append('%dpx %s :: <%s class="%s"> outside .col — "%s"'
                                     % (w, p, e['tag'], e['cls'], e['text']))
                        continue
                    if e['left'] < L - 2:
                        fails.append('%dpx %s :: .%s starts x=%d, column starts x=%d — "%s"'
                                     % (w, p, e['cls'], e['left'], L, e['text']))
                    if e['right'] > R + 2 and not e['scrolled']:
                        fails.append('%dpx %s :: .%s ends x=%d, column ends x=%d — "%s"'
                                     % (w, p, e['cls'], e['right'], R, e['text']))
                    elif e['right'] > R + 2 and e['tag'] != 'table':
                        fails.append('%dpx %s :: <%s class="%s"> overflows the column inside '
                                     'a scroll wrapper — only tables may — "%s"'
                                     % (w, p, e['tag'], e['cls'], e['text']))
                hd = d['head']
                if hd and w >= 1000 and hd['host'] > 0:
                    frac = hd['w'] / hd['host']
                    if frac < 0.34 and hd['lines'] >= 4:
                        fails.append('%dpx %s :: h1 is %d%% of its column over %d lines — '
                                     'squeezed — "%s"' % (w, p, round(frac * 100), hd['lines'],
                                                          hd['text']))
                # GATE D
                if w >= 1000 and d['railH'] > d['vh']:
                    fails.append('%dpx %s :: sticky rail is %dpx tall in a %dpx viewport — '
                                 'it will detach' % (w, p, d['railH'], d['vh']))
                if d['barShown'] and d['footBottomGap'] < d['barH'] + 8:
                    fails.append('%dpx %s :: fixed contact bar is %dpx tall but the footer '
                                 'only clears %dpx — it covers content'
                                 % (w, p, d['barH'], d['footBottomGap']))
                # GATE E
                if not d['widgetsTotal']:
                    fails.append('%dpx %s :: NO element carries [data-contact-widget]' % (w, p))
                elif not d['widgets']:
                    fails.append('%dpx %s :: a contact widget exists in the markup but none is '
                                 'visible at this viewport — a user sees no way to make contact'
                                 % (w, p))
                for wd in d['widgets']:
                    who = '.%s' % (wd['cls'] or '?')
                    if wd['offscreen']:
                        fails.append('%dpx %s :: contact widget %s is off-screen' % (w, p, who))
                    for key, what in (('tel', 'a tel: link'), ('mail', 'a mailto: link'),
                                      ('appt', 'an appointment link')):
                        if not wd[key]:
                            fails.append('%dpx %s :: contact widget %s offers no %s'
                                         % (w, p, who, what))
                    if wd['overlapsCol']:
                        fails.append('%dpx %s :: contact widget %s is fixed and overlaps the '
                                     'reading column — it covers body text' % (w, p, who))
                    if wd['external']:
                        fails.append('%dpx %s :: contact widget %s makes an external request '
                                     'or embeds a script — it must be fully static'
                                     % (w, p, who))
                    if not wd['label']:
                        warns.append('%dpx %s :: contact widget %s has no aria-label'
                                     % (w, p, who))
            await pg.close()
        await b.close()
    return fails, warns


if __name__ == '__main__':
    print('CARELLA LAYOUT AUDIT — %d pages at 1440 / 1100 / 390\n' % len(PAGES))
    a = gate_a()
    print('GATE A  container nesting ................ %s'
          % ('FAIL (%d)' % len(a) if a else 'PASS'))
    for p, why, ctx in a:
        print('   FAIL %-40s %s' % (p, why))
        if ctx:
            print('        near: %s' % ctx.strip()[:150])
    f, wn = asyncio.run(gates_bcd())
    print('GATE B/C/D/E  geometry, headings, widget . %s'
          % ('FAIL (%d)' % len(f) if f else 'PASS'))
    for x in f[:50]:
        print('   FAIL %s' % x)
    if len(f) > 50:
        print('   ... +%d more' % (len(f) - 50))
    for x in wn[:10]:
        print('   WARN %s' % x)
    sys.exit(1 if (a or f) else 0)
