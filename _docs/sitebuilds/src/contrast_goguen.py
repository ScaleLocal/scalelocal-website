# -*- coding: utf-8 -*-
"""WCAG audit for the Fitzpatrick & Goguen build, read from the BUILT stylesheet."""
import os, re, sys
CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'out', 'bgoguen', 'css', 'fg.css')
css = open(CSS_PATH, encoding='utf-8').read()
V = dict(re.findall(r'--([a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})', re.search(r':root\{(.*?)\}', css, re.S).group(1)))

def lum(c):
    c = c.lstrip('#'); o = []
    for i in (0, 2, 4):
        v = int(c[i:i+2], 16)/255.0
        o.append(v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4)
    return 0.2126*o[0] + 0.7152*o[1] + 0.0722*o[2]

def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb)+0.05)/(min(la, lb)+0.05)

P = V
W = '#FFFFFF'
PAIRS = [
    ('body copy on paper',           P['body'],      P['paper'], 4.5),
    ('body copy on white card',      P['body'],      P['card'],  4.5),
    ('body copy on sand card',       P['body'],      P['sand'],  4.5),
    ('headings on paper',            P['ink'],       P['paper'], 4.5),
    ('headings on white card',       P['ink'],       P['card'],  4.5),
    ('headings on sand card',        P['ink'],       P['sand'],  4.5),
    ('muted label on paper',         P['muted'],     P['paper'], 4.5),
    ('muted label on white card',    P['muted'],     P['card'],  4.5),
    ('muted label on sand card',     P['muted'],     P['sand'],  4.5),
    ('link on paper',                P['indigo-dk'], P['paper'], 4.5),
    ('link on white card',           P['indigo-dk'], P['card'],  4.5),
    ('link on sand card',            P['indigo-dk'], P['sand'],  4.5),
    ('link hover on paper',          P['indigo'],    P['paper'], 4.5),
    ('credential line on white',     P['indigo-dk'], P['card'],  4.5),
    ('figure numeral on sand',       P['indigo-dk'], P['sand'],  3.0),
    ('active tab text on indigo',    W,              P['indigo'], 4.5),
    ('portal tab text on paper',     P['indigo-dk'], P['paper'], 4.5),
    ('monogram initials on indigo',  W,              P['indigo'], 4.5),
    ('monogram initials on sand-2',  P['ink'],       P['sand-2'], 4.5),
    ('rail label on white',          P['muted'],     P['card'],  4.5),
    ('rail action on white',         P['ink'],       P['card'],  4.5),
    ('rail key action on indigo',    W,              P['indigo'], 4.5),
    ('row sub-label on white',       P['muted'],     P['card'],  4.5),
    ('row key sub on indigo',        '#D5CFF2',      P['indigo'], 4.5),
    ('deep card body',               '#CFCBDD',      P['deep'],  4.5),
    ('deep card heading',            W,              P['deep'],  4.5),
    ('deep card link',               '#BCB2F0',      P['deep'],  4.5),
    ('deep card figure',             '#BCB2F0',      '#312A4F',  3.0),
    ('deep card fig caption',        '#A9A3C0',      '#312A4F',  4.5),
    ('demo strip text on deep',      '#CFCBDD',      P['deep'],  4.5),
    ('demo strip lead on deep',      '#B9AFEA',      P['deep'],  4.5),
    ('calculator headline on indigo', W,             P['indigo'], 3.0),
    ('calculator label on indigo',   '#C0B8EC',      P['indigo'], 4.5),
    ('calculator value on indigo',   W,              P['indigo'], 4.5),
    ('input value on white field',   P['ink'],       P['card'],  4.5),
    ('input affix on white',         P['muted'],     P['card'],  4.5),
    ('table header on sand',         P['ink'],       P['sand'],  4.5),
    ('footer body on deep',          '#B3AEC6',      P['deep'],  4.5),
    ('footer link on deep',          '#D2CEE4',      P['deep'],  4.5),
    ('footer fine on deep',          '#8D87A5',      P['deep'],  4.5),
    ('skip link on indigo',          W,              P['indigo'], 4.5),
    # non-text UI (1.4.11)
    ('input border on white',        P['field'],     P['card'],  3.0),
    ('input border on paper',        P['field'],     P['paper'], 3.0),
    ('portal tab border on paper',   P['indigo-lt'], P['paper'], 3.0),
    ('focus ring on paper',          P['indigo'],    P['paper'], 3.0),
    ('aside accent bar on white',    P['indigo'],    P['card'],  3.0),
]
print('%-36s %-9s %-9s %6s %5s  %s' % ('PAIR', 'FG', 'BG', 'RATIO', 'REQ', 'RESULT'))
fails = 0
for name, fg, bg, req in PAIRS:
    r = ratio(fg, bg); ok = r >= req; fails += 0 if ok else 1
    print('%-36s %-9s %-9s %6.2f %5.1f  %s' % (name, fg.upper(), bg.upper(), r, req,
                                               'OK' if ok else '*** FAIL ***'))
print('\ntokens read from %s' % os.path.relpath(CSS_PATH))
print('PAIRS: %d   FAILS: %d' % (len(PAIRS), fails))
sys.exit(1 if fails else 0)
