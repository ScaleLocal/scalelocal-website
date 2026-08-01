# -*- coding: utf-8 -*-
"""WCAG AA contrast audit. Theme comes from the selected firm profile (QA pass #7)."""
def hx(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def lum(c):
    def f(v):
        v /= 255.0
        return v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    r, g, b = hx(c)
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)

# Theme MUST come from the selected firm profile. This was hardcoded to one firm's
# palette, which silently made the whole gate a no-op for every other build.
import os, importlib
SLUG = os.environ.get('BUILD_FIRM', 'kpw-cpa')
_T = importlib.import_module('firms.' + SLUG.replace('-', '_')).T
INK, INK2, ACC, ACCD, CREAM = _T['ink'], _T['ink2'], _T['acc'], _T['accd'], _T['cream']
PAPER, LINE, MUTED = '#fffdf8', '#e7e2d7', '#5d5f58'
def _darken(hexc, f=0.62):
    r, g, b = hx(hexc)
    return '#%02x%02x%02x' % (int(r*(1-f)), int(g*(1-f)), int(b*(1-f)))
FOOT = _darken(INK)

PAIRS = [
 ('body text on paper',        INK,      PAPER,  4.5),
 ('body text on cream',        INK,      CREAM,  4.5),
 ('prose text on paper',       '#3c4038', PAPER, 4.5),
 ('prose text on cream',       '#3c4038', CREAM, 4.5),
 ('muted lead on paper',       MUTED,    PAPER,  4.5),
 ('muted lead on cream',       MUTED,    CREAM,  4.5),
 ('link (accd) on paper',      ACCD,     PAPER,  4.5),
 ('link (accd) on cream',      ACCD,     CREAM,  4.5),
 ('eyebrow (accd) on paper',   ACCD,     PAPER,  4.5),
 ('card icon (accd) on tint',  ACCD,     '#F1E9DA', 4.5),
 ('white on ink (hero)',       '#ffffff', INK,   4.5),
 ('white on ink2',             '#ffffff', INK2,  4.5),
 ('hero sub #ece7dc on ink',   '#ece7dc', INK,   4.5),
 ('hero sub #ece7dc on ink2',  '#ece7dc', INK2,  4.5),
 ('phero sub #e6e1d5 on ink',  '#e6e1d5', INK,   4.5),
 ('hero-trust #d7d3c9 on ink', '#d7d3c9', INK,   4.5),
 ('crumbs #c9c4b8 on ink',     '#c9c4b8', INK,   4.5),
 ('crumb link #e8d3a8 on ink', '#e8d3a8', INK,   4.5),
 ('eyebrow on-dark #e8d3a8/ink2', '#e8d3a8', INK2, 4.5),
 ('strip label #b9b5ab on ink', '#b9b5ab', INK,  4.5),
 ('strip number #fff on ink',  '#ffffff', INK,   3.0),
 ('acard body #c4c0b6 on ink', '#c4c0b6', INK,   4.5),
 ('btn b-acc text on acc',     '#15130e', ACC,   4.5),
 ('btn b-dk text on ink',      '#ffffff', INK,   4.5),
 ('footer body #a7a39a on foot', '#a7a39a', FOOT, 4.5),
 ('footer link #cfcbc1 on foot', '#cfcbc1', FOOT, 4.5),
 ('footer head #fff on foot',  '#ffffff', FOOT,  4.5),
 ('footer legal #918d84 on foot', '#918d84', FOOT, 4.5),
 ('topbar #cfcbc1 on ink',     '#cfcbc1', INK,   4.5),
 ('nav link on paper',         INK,      PAPER,  4.5),
 ('faq summary on paper',      INK,      PAPER,  4.5),
 ('table header on cream',     INK,      CREAM,  4.5),
 ('tcard cred (accd) on paper', ACCD,    PAPER,  4.5),
 ('office oloc (accd) on paper', ACCD,   PAPER,  4.5),
 ('chat pill: navy text on gold',  '#142A44', '#E8B33F', 4.5),
 ('demo strip: body text on charcoal', '#E8E3D8', '#23211D', 4.5),
 ('demo strip: gold label on charcoal','#E8B33F', '#23211D', 4.5),
 ('chat pill hover: navy on gold', '#142A44', '#F5C453', 4.5),
 ('chat pill vs hero backdrop',    '#E8B33F', '#1B3350', 3.0),
]

fails = 0
print('%-34s %-9s %-9s %6s  %5s  %s' % ('PAIR', 'FG', 'BG', 'RATIO', 'REQ', 'RESULT'))
for name, fg, bg, req in PAIRS:
    r = ratio(fg, bg)
    ok = r >= req
    if not ok:
        fails += 1
    print('%-34s %-9s %-9s %6.2f  %5.1f  %s' % (name, fg, bg, r, req, 'OK' if ok else '*** FAIL ***'))
print('\nfirm:', SLUG, '  ink', INK, ' acc', ACC)
print('FAILS:', fails)
raise SystemExit(1 if fails else 0)
