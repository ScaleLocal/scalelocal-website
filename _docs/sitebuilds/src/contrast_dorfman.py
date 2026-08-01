# -*- coding: utf-8 -*-
"""WCAG audit for the Dorfman & Dorfman build, read from the BUILT stylesheet."""
import os, re, sys
CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'out', 'dorfmancpas', 'css', 'dd.css')
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
    ('body on page',                 P['body'],     P['page'],  4.5),
    ('body on sheet',                P['body'],     P['sheet'], 4.5),
    ('body on warm hero',            P['body'],     P['warm'],  4.5),
    ('body on tint',                 P['body'],     P['tint'],  4.5),
    ('headings on page',             P['ink'],      P['page'],  4.5),
    ('headings on sheet',            P['ink'],      P['sheet'], 4.5),
    ('headings on warm',             P['ink'],      P['warm'],  4.5),
    ('note text on page',            P['note'],     P['page'],  4.5),
    ('note text on sheet',           P['note'],     P['sheet'], 4.5),
    ('note text on tint',            P['note'],     P['tint'],  4.5),
    ('note text on warm',            P['note'],     P['warm'],  4.5),
    ('link on page',                 P['slate-dk'], P['page'],  4.5),
    ('link on sheet',                P['slate-dk'], P['sheet'], 4.5),
    ('link on warm',                 P['slate-dk'], P['warm'],  4.5),
    ('link on tint',                 P['slate-dk'], P['tint'],  4.5),
    ('link hover on page',           P['slate'],    P['page'],  4.5),
    ('eyebrow on warm',              P['slate-dk'], P['warm'],  4.5),
    ('tagline on warm',              P['slate-dk'], P['warm'],  4.5),
    ('nav link on page',             P['body'],     P['page'],  4.5),
    ('nav current on page',          P['slate-dk'], P['page'],  4.5),
    ('nav CTA text on slate',        W,             P['slate'], 4.5),
    ('utility bar text on tint',     P['body'],     P['tint'],  4.5),
    ('utility bar bold on tint',     P['ink'],      P['tint'],  4.5),
    ('filed tab text on slate',      W,             P['slate'], 4.5),
    ('figure numeral on sheet',      P['slate-dk'], P['sheet'], 3.0),
    ('figure numeral on page',       P['slate-dk'], P['page'],  3.0),
    ('tile title on sheet',          P['ink'],      P['sheet'], 4.5),
    ('tile go-label on sheet',       P['slate-dk'], P['sheet'], 4.5),
    ('register title on page',       P['ink'],      P['page'],  4.5),
    ('register right label on page', P['note'],     P['page'],  4.5),
    ('dark panel body',              '#C6CCD2',     P['dark'],  4.5),
    ('dark panel heading',           W,             P['dark'],  4.5),
    ('dark panel link',              '#9CC0DE',     P['dark'],  4.5),
    ('dark panel figure',            '#9CC0DE',     P['dark'],  3.0),
    ('dark panel fig caption',       '#9AA6B2',     P['dark'],  4.5),
    ('filed tab on dark panel',      W,             P['slate'], 4.5),
    ('demo strip text on dark',      '#C6CCD2',     P['dark'],  4.5),
    ('demo strip lead on dark',      '#9CC0DE',     P['dark'],  4.5),
    ('closing CTA body',             '#C6CCD2',     P['dark'],  4.5),
    ('closing CTA heading',          W,             P['dark'],  4.5),
    ('closing CTA solid btn',        P['dark'],     W,          4.5),
    ('calculator head on slate',     W,             P['slate'], 4.5),
    ('calculator value on sheet',    P['slate-dk'], P['sheet'], 3.0),
    ('calculator dt on sheet',       P['note'],     P['sheet'], 4.5),
    ('input value on sheet',         P['ink'],      P['sheet'], 4.5),
    ('input affix on sheet',         P['note'],     P['sheet'], 4.5),
    ('footer body on page',          P['body'],     P['page'],  4.5),
    ('footer fine on page',          P['note'],     P['page'],  4.5),
    ('skip link on slate',           W,             P['slate'], 4.5),
    # non-text UI (1.4.11)
    ('input border on sheet',        P['field'],    P['sheet'], 3.0),
    ('ghost button border on warm',  P['slate-lt'], P['warm'],  3.0),
    ('focus ring on page',           P['slate'],    P['page'],  3.0),
    ('list marker on sheet',         P['slate-lt'], P['sheet'], 3.0),
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
