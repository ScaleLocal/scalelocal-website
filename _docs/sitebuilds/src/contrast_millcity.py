# -*- coding: utf-8 -*-
"""WCAG audit for the Mill City build, read from the BUILT stylesheet's tokens."""
import os, re, sys
CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'out', 'millcityaccounting', 'css', 'millcity.css')
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
PAIRS = [
    ('body copy on chalk',            P['body'],   P['chalk'],  4.5),
    ('body copy on white panel',      P['body'],   P['paper'],  4.5),
    ('headings on chalk',             P['ink'],    P['chalk'],  4.5),
    ('headings on white panel',       P['ink'],    P['paper'],  4.5),
    ('quiet label on chalk',          P['quiet'],  P['chalk'],  4.5),
    ('quiet label on white panel',    P['quiet'],  P['paper'],  4.5),
    ('quiet label on chalk-2 note',   P['quiet'],  P['chalk-2'], 4.5),
    ('note body on chalk-2',          P['body'],   P['chalk-2'], 4.5),
    ('link on chalk',                 P['vermilion-dk'], P['chalk'], 4.5),
    ('link on white panel',           P['vermilion-dk'], P['paper'], 4.5),
    ('link hover on chalk',           '#8E2D0C',         P['chalk'], 4.5),
    ('figure number on white',        P['vermilion-dk'], P['paper'], 3.0),
    ('row right label on chalk',      P['vermilion-dk'], P['chalk'], 4.5),
    ('note label on chalk-2',         P['vermilion-dk'], P['chalk-2'], 4.5),
    # reversed out on slate
    ('body on slate panel',           '#D6DADC',  P['slate'],  4.5),
    ('heading on slate panel',        '#FFFFFF',  P['slate'],  4.5),
    ('link on slate panel',           '#F0A78F',  P['slate'],  4.5),
    ('counter action on slate',       '#FFFFFF',  P['slate'],  4.5),
    ('counter detail on slate',       '#9FA8AD',  P['slate'],  4.5),
    ('counter label on slate',        '#98A1A6',  P['slate'],  4.5),
    ('counter open state on slate',   '#8FE7BB',  P['slate'],  4.5),
    ('counter detail on hover slate', '#CFD4D6',  P['slate-2'], 4.5),
    ('pay action on vermilion-dk',    '#FFFFFF',  P['vermilion-dk'], 4.5),
    ('pay detail on vermilion-dk',    '#FADFD8',  P['vermilion-dk'], 4.5),
    ('pay detail on vermilion hover', '#FFF6F3',  P['vermilion'], 4.5),
    ('demo strip text on slate',      '#CFD4D6',  P['slate'],  4.5),
    ('demo strip lead on slate',      P['vermilion-lt'], P['slate'], 4.5),
    ('door card body on slate',       '#D6DADC',  P['slate'],  4.5),
    ('door card go-link on slate',    '#F0A78F',  P['slate'],  4.5),
    ('door card who-label on slate',  '#98A1A6',  P['slate'],  4.5),
    ('table header on slate',         '#FFFFFF',  P['slate'],  4.5),
    ('results figure on slate',       '#FFFFFF',  P['slate'],  3.0),
    ('results dt on slate',           '#9FA8AD',  P['slate'],  4.5),
    ('footer body on slate',          '#B9C0C4',  P['slate'],  4.5),
    ('footer link on slate',          '#D6DADC',  P['slate'],  4.5),
    ('footer legal on slate',         '#8A9297',  P['slate'],  4.5),
    ('eyebrow white on slate',        '#FFFFFF',  P['slate'],  4.5),
    ('eyebrow white on vermilion-dk', '#FFFFFF',  P['vermilion-dk'], 4.5),
    # non-text UI (1.4.11)
    ('input border on white',         P['field'], P['paper'],  3.0),
    ('input border on chalk',         P['field'], P['chalk'],  3.0),
    ('focus ring on chalk',           P['vermilion'], P['chalk'], 3.0),
    ('focus ring on white',           P['vermilion'], P['paper'], 3.0),
    ('list bullet on white',          P['vermilion'], P['paper'], 3.0),
    ('counter top edge on chalk',     P['vermilion'], P['chalk'], 3.0),
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
