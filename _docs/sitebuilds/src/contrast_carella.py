# -*- coding: utf-8 -*-
"""
WCAG contrast audit for the Carella build.

contrast.py checks a fixed list of pairs belonging to the template engine's
stylesheet — hero gradients, gold chat pills, topbars, cream cards. None of those
exist here, so running it against this build would compare colours the site never
puts together and report a meaningless pass.

This reads the ACTUAL custom properties out of the built stylesheet and checks the
pairs this site actually renders. Text is held to AA (4.5:1, or 3:1 at >=24px);
borders and other non-text UI to 1.4.11 (3:1).

    python3 contrast_carella.py
"""
import os, re, sys

CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'out', 'carellacpa', 'css', 'carella.css')
css = open(CSS_PATH, encoding='utf-8').read()
root = re.search(r':root\{(.*?)\}', css, re.S).group(1)
V = dict(re.findall(r'--([a-z0-9]+):\s*(#[0-9A-Fa-f]{6})', root))
missing = {'paper', 'panel', 'ink', 'soft', 'faint', 'rule', 'rule2', 'field',
           'pine', 'pinelt', 'dark'} - set(V)
if missing:
    print('could not read tokens from the stylesheet:', missing)
    sys.exit(2)
WHITE, INPUT_BG = '#FFFFFF', '#FFFFFF'
NOTICE_FG, NOTICE_ACC = '#DCDED4', '#9EC3B2'


def lum(c):
    c = c.lstrip('#')
    out = []
    for i in (0, 2, 4):
        v = int(c[i:i + 2], 16) / 255.0
        out.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


P = V
PAIRS = [
    # --- body and prose ---------------------------------------------------
    ('body text on paper',                P['ink'],    P['paper'], 4.5),
    ('body text on panel (row hover)',    P['ink'],    P['panel'], 4.5),
    ('lede / secondary prose on paper',   P['soft'],   P['paper'], 4.5),
    ('index row detail on panel',         P['soft'],   P['panel'], 4.5),
    ('remark body on paper',              P['soft'],   P['paper'], 4.5),
    # --- small labels: 10-13px, so AA normal text applies ------------------
    ('marginal band label on paper',      P['faint'],  P['paper'], 4.5),
    ('kicker / breadcrumb on paper',      P['faint'],  P['paper'], 4.5),
    ('wordmark strapline on paper',       P['faint'],  P['paper'], 4.5),
    ('table head label on paper',         P['faint'],  P['paper'], 4.5),
    ('calculator hint on paper',          P['faint'],  P['paper'], 4.5),
    ('calculator note on paper',          P['faint'],  P['paper'], 4.5),
    ('output note on paper',              P['faint'],  P['paper'], 4.5),
    ('map caption on paper',              P['faint'],  P['paper'], 4.5),
    ('footer fine print on paper',        P['faint'],  P['paper'], 4.5),
    ('reachbar sub-label on paper',       P['faint'],  P['paper'], 4.5),
    ('parts key on paper',                P['faint'],  P['paper'], 4.5),
    # --- accent -----------------------------------------------------------
    ('link (pine) on paper',              P['pine'],   P['paper'], 4.5),
    ('link hover (pinelt) on paper',      P['pinelt'], P['paper'], 4.5),
    ('link (pine) on panel',              P['pine'],   P['panel'], 4.5),
    ('active nav item on paper',          P['pine'],   P['paper'], 4.5),
    ('question group label on paper',     P['pine'],   P['paper'], 4.5),
    ('remark label on paper',             P['pine'],   P['paper'], 4.5),
    ('calculator headline figure',        P['pine'],   P['paper'], 3.0),   # 38px, large text
    ('skip link text on pine',            WHITE,       P['pine'],  4.5),
    # --- calculator inputs ------------------------------------------------
    ('input value on white field',        P['ink'],    INPUT_BG,   4.5),
    ('input prefix/suffix on white',      P['faint'],  INPUT_BG,   4.5),
    # --- demo notice strip ------------------------------------------------
    ('demo notice text on dark',          NOTICE_FG,   P['dark'],  4.5),
    ('demo notice label on dark',         NOTICE_ACC,  P['dark'],  4.5),
    # --- non-text UI (WCAG 1.4.11, 3:1) -----------------------------------
    ('input border on paper',             P['field'],  P['paper'], 3.0),
    ('map frame border on paper',         P['field'],  P['paper'], 3.0),
    ('focus ring on paper',               P['pine'],   P['paper'], 3.0),
    ('focus ring on panel',               P['pine'],   P['panel'], 3.0),
    ('heavy rule (ink) on paper',         P['ink'],    P['paper'], 3.0),
]

print('%-38s %-9s %-9s %6s %5s  %s'
      % ('PAIR', 'FG', 'BG', 'RATIO', 'REQ', 'RESULT'))
fails = 0
for name, fg, bg, req in PAIRS:
    r = ratio(fg, bg)
    ok = r >= req
    fails += 0 if ok else 1
    print('%-38s %-9s %-9s %6.2f %5.1f  %s'
          % (name, fg.upper(), bg.upper(), r, req, 'OK' if ok else '*** FAIL ***'))

# Hairline rules are decorative separators, not UI controls or meaningful
# boundaries, so 1.4.11 does not apply. Reported for information only.
for name, fg in (('hairline rule', P['rule']), ('heavier hairline', P['rule2'])):
    print('%-38s %-9s %-9s %6.2f %5s  info (decorative separator)'
          % (name + ' on paper', fg.upper(), P['paper'].upper(),
             ratio(fg, P['paper']), '-'))

print('\ntokens read from %s' % os.path.relpath(CSS_PATH))
print('PAIRS: %d   FAILS: %d' % (len(PAIRS), fails))
sys.exit(1 if fails else 0)
