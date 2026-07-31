# -*- coding: utf-8 -*-
"""Mobile 390px + desktop 1440px screenshot gate (QA pass #8)."""
import os, asyncio, sys
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', os.environ.get('BUILD_FIRM','kpw-cpa'))
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots')
os.makedirs(SHOTS, exist_ok=True)

import re as _re
TARGETS = []
for _dp, _dn, _fn in os.walk(ROOT):
    for _f in sorted(_fn):
        if _f.endswith('.html'):
            TARGETS.append(os.path.relpath(os.path.join(_dp, _f), ROOT).replace('\\', '/'))
TARGETS.sort()

async def main():
    overflow_problems = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for label, w, h in (('m', 390, 844), ('d', 1440, 900)):
            for t in TARGETS:
                pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                await pg.route(_re.compile(r'^https?://'), lambda r: asyncio.ensure_future(r.abort()))
                await pg.goto('file://' + os.path.join(ROOT, t), wait_until='domcontentloaded')
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                await pg.wait_for_timeout(250)
                # horizontal overflow check
                ow = await pg.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
                if ow > w + 1:
                    overflow_problems.append(f'{label} {t}: scrollWidth {ow} > viewport {w}')
                name = label + '_' + t.replace('/', '__').replace('.html', '') + '.png'
                await pg.screenshot(path=os.path.join(SHOTS, name), full_page=True)
                await pg.close()
            print('captured', label, len(TARGETS), 'pages')
        await b.close()
    print('\nOVERFLOW PROBLEMS:', len(overflow_problems))
    for o in overflow_problems:
        print('  FAIL', o)
    return 1 if overflow_problems else 0

sys.exit(asyncio.run(main()))
