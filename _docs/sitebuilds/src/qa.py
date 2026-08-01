# -*- coding: utf-8 -*-
"""QA harness — operationalizes HANDOFF v2.2 §5.3 passes 2, 4, 6, 9 (mechanical parts)."""
import os, re, json, sys
from urllib.parse import urlparse, unquote

SLUG = os.environ.get('BUILD_FIRM', 'kpw-cpa')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', SLUG)
import importlib
_F = importlib.import_module('firms.' + SLUG.replace('-', '_'))
fails, warns = [], []

def F(m): fails.append(m)
def W(m): warns.append(m)

htmls = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.endswith('.html'):
            htmls.append(os.path.join(dp, f))
htmls.sort()
relpaths = {os.path.relpath(h, ROOT).replace('\\', '/') for h in htmls}
assets = set()
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        assets.add(os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/'))

print('PAGES:', len(htmls))

inbound = {p: 0 for p in relpaths}
NAP = {
 'dg_phone': '(630) 390-1140', 'chi_phone': '(312) 421-5780',
 'dg_tel': '+16303901140', 'chi_tel': '+13124215780',
 'dg_addr': '1400 Opus Place', 'chi_addr': '954 W Washington Blvd',
}
phone_pat = re.compile(r'\(\d{3}\)\s\d{3}-\d{4}')
# Chicago office CLOSED 2026-07-30. Only the Downers Grove numbers are valid.
ALLOWED_PHONES = set(_F.ALLOWED_PHONES)

for h in htmls:
    rp = os.path.relpath(h, ROOT).replace('\\', '/')
    src = open(h, encoding='utf-8').read()
    d = rp.count('/')

    # --- pass 6: headings
    h1s = re.findall(r'<h1[ >]', src)
    if len(h1s) != 1:
        F(f'{rp}: {len(h1s)} H1 tags (expected exactly 1)')
    # heading hierarchy: no h3 before any h2 inside prose
    order = [int(m) for m in re.findall(r'<h([1-4])[ >]', src)]
    prev = 0
    for lvl in order:
        if prev and lvl > prev + 1:
            W(f'{rp}: heading jump h{prev} -> h{lvl}')
            break
        prev = lvl

    # --- staging posture (§10.1 layer 1)
    if 'name="robots" content="noindex, nofollow"' not in src:
        F(f'{rp}: missing robots noindex,nofollow')
    if 'name="googlebot" content="noindex, nofollow"' not in src:
        F(f'{rp}: missing googlebot noindex,nofollow')

    # --- per-page SEO
    t = re.search(r'<title>(.*?)</title>', src, re.S)
    if not t or not t.group(1).strip():
        F(f'{rp}: missing title')
    elif len(__import__('html').unescape(t.group(1))) > 72:
        W(f'{rp}: title {len(__import__("html").unescape(t.group(1)))} chars — long ({t.group(1)[:64]})')
    ds = re.search(r'<meta name="description" content="(.*?)">', src, re.S)
    if not ds or not ds.group(1).strip():
        F(f'{rp}: missing meta description')
    elif not (70 <= len(__import__('html').unescape(ds.group(1))) <= 175):
        W(f'{rp}: description {len(__import__("html").unescape(ds.group(1)))} chars (target 70-175)')
    if '<link rel="canonical"' not in src:
        F(f'{rp}: missing canonical')
    for og in ('og:title', 'og:description', 'og:url', 'og:image', 'og:image:width', 'twitter:card'):
        if og not in src:
            F(f'{rp}: missing {og}')
    # alt text on every img
    for img in re.findall(r'<img [^>]*>', src):
        if 'alt=' not in img:
            F(f'{rp}: <img> without alt: {img[:70]}')
    # every iframe (Google Map embeds) needs an accessible name + lazy loading
    for ifr in re.findall(r'<iframe [^>]*>', src):
        if 'title=' not in ifr:
            F(f'{rp}: <iframe> without title (a11y): {ifr[:70]}')
        if 'loading="lazy"' not in ifr:
            W(f'{rp}: <iframe> not lazy-loaded: {ifr[:70]}')

    # --- pass 6: JSON-LD validity
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    if not blocks:
        F(f'{rp}: no JSON-LD')
    for b in blocks:
        try:
            o = json.loads(b)
        except Exception as e:
            F(f'{rp}: JSON-LD parse error: {e}')
            continue
        if '@context' not in o or '@type' not in o:
            F(f'{rp}: JSON-LD missing @context/@type')
        # honesty gate: no rating markup anywhere (§2 decision)
        if 'aggregateRating' in b or 'AggregateRating' in b or '"reviewCount"' in b:
            F(f'{rp}: rating/review schema present — violates honesty decision')

    # --- pass 9: NAP consistency
    for ph in phone_pat.findall(src):
        if ph not in ALLOWED_PHONES:
            F(f'{rp}: unknown phone number rendered: {ph}')

    # --- links
    for m in re.findall(r'(?:href|src)="([^"]+)"', src):
        if m.startswith(('http://', 'https://', 'mailto:', 'tel:', 'sms:', 'data:', '#')):
            continue
        target = m.split('#')[0].split('?')[0]
        if not target:
            continue
        full = os.path.normpath(os.path.join(os.path.dirname(rp), unquote(target))).replace('\\', '/')
        if full not in assets:
            F(f'{rp}: broken link -> {m}  (resolved {full})')
        elif full in inbound and full != rp:
            inbound[full] += 1

# --- orphans
for p, n in sorted(inbound.items()):
    if n == 0 and p != 'index.html':
        F(f'ORPHAN: {p} has no inbound internal links')

# --- forbidden / dated claims (pass 2 mechanical screen)
BANNED = ['5-star', '★', 'Google reviews', 'award-winning', 'best in',
          '#1 ',
          # Marketing guarantees only. A bare 'guaranteed' over-matches legitimate
          # accounting language ('personally guaranteed debt', 'guaranteed payments'),
          # and a firm may genuinely state a guarantee on its own site.
          'guaranteed results', 'guaranteed savings', 'guaranteed refund',
          'guarantee your refund', 'guaranteed return',
          # Fee-timing claims are invented unless the firm's own site states them.
          'quoted before it starts', 'quoted before work begins', 'quote before we begin',
          'quotes before beginning', 'bill surprises', 'quoted before the work',
          'quoted up front', 'priced before we begin',
          ] + list(getattr(_F, 'BANNED', []))
for h in htmls:
    src = open(h, encoding='utf-8').read()
    rp = os.path.relpath(h, ROOT).replace('\\', '/')
    for b in BANNED:
        if b.lower() in src.lower():
            F(f'{rp}: banned/dated claim present -> "{b}"')

# --- AI-tell screen (pass 5 mechanical assist)
TELLS = ["in today's fast-paced", 'in today’s fast-paced', 'ever-evolving', 'delve into',
         'it is important to note', 'in conclusion', 'navigate the complexities',
         'tailored solutions', 'cutting-edge', 'seamlessly', 'robust suite', 'leverage our',
         'unlock the', 'take your business to the next level', 'we understand that',
         'rest assured', 'look no further', 'trusted partner', 'a myriad of', 'plethora']
for h in htmls:
    src = open(h, encoding='utf-8').read().lower()
    rp = os.path.relpath(h, ROOT).replace('\\', '/')
    for t in TELLS:
        if t in src:
            F(f'{rp}: AI tell -> "{t}"')

print('\n--- FAILS (%d) ---' % len(fails))
for f in fails: print('  FAIL', f)
print('\n--- WARNINGS (%d) ---' % len(warns))
for w in warns: print('  warn', w)
print('\nRESULT:', 'PASS' if not fails else 'FAIL')
sys.exit(1 if fails else 0)
