# -*- coding: utf-8 -*-
"""
Screenshots of the Carella build, for looking at.

Google Fonts is reachable from the sandbox, so this does NOT block it — blocking
every https route (as the layout audit must, to stop the map iframe stalling) also
strips the typeface, and a screenshot in a fallback face is not evidence about a
design whose whole system is typography. Only the map host is blocked.

    python3 shots_carella.py [--full]
"""
import os, sys, asyncio, re
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'out', 'carellacpa')
SHOTS = os.path.join(HERE, 'shots', 'carellacpa')
FULL = '--full' in sys.argv

PAGES = ['index.html', 'situations/index.html', 'situations/irs-notice.html',
         'situations/new-business.html', 'services/index.html', 'services/tax.html',
         'services/bookkeeping.html', 'calculators/index.html',
         'calculators/mortgage-payment.html', 'calculators/self-employment-tax.html',
         'about.html', 'what-to-bring.html', 'questions.html', 'contact.html']


async def run():
    os.makedirs(SHOTS, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        modes = (('mob', 390, 844),) if '--mob' in sys.argv else (('desk', 1440, 900), ('mob', 390, 844))
        for label, w, h in modes:
            pg = await b.new_page(viewport={'width': w, 'height': h},
                                  device_scale_factor=2 if w < 500 else 1)
            await pg.route(re.compile(r'^https?://(maps|www)\.google\.com'),
                           lambda r: asyncio.ensure_future(r.abort()))
            for p in PAGES:
                await pg.goto('file://' + os.path.join(ROOT, p), wait_until='load')
                try:
                    await pg.wait_for_function(
                        "() => document.fonts.check('700 20px \"Public Sans\"')", timeout=8000)
                except Exception:
                    print('  ! webfont not applied on', p)
                await pg.wait_for_timeout(250)
                name = '%s__%s.png' % (label, p.replace('/', '_').replace('.html', ''))
                await pg.screenshot(path=os.path.join(SHOTS, name), full_page=FULL)
            await pg.close()
        await b.close()
    print('%d shots -> %s' % (len(os.listdir(SHOTS)), SHOTS))


if __name__ == '__main__':
    asyncio.run(run())
