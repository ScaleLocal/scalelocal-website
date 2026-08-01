# -*- coding: utf-8 -*-
"""
Original hero art, generated per firm.

There is no stock photography on any of these sites and no invented offices or
people. Where a site benefits from imagery, the image is an original abstract
composition built here as SVG and rendered to PNG — colour-matched to that
firm's palette, and nobody else's. Real photography replaces it at cutover.

Judgement, per firm: art earns its place on Mill City, Goguen, Mass Tax Pros and
KPW. Hickey, Carella and Dorfman are better served by space and typography, so
they get a restrained device or nothing at all.

    python3 art.py <slug>
"""
import os, sys, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


def dorfman():
    """Restrained: offset record cards on a warm ground, ruled like a register.
    No illustration, no metaphor pushed too far — a quiet object."""
    slate, dk, lt, warm, sheet, rule = '#2F4E6E', '#233B54', '#4E7398', '#F4EFE7', '#FFFFFF', '#DDE1E4'
    rows = ''
    for i in range(7):
        y = 236 + i * 26
        w = [300, 232, 268, 190, 254, 212, 160][i]
        rows += ('<rect x="196" y="%d" width="%d" height="5" fill="%s" opacity="%.2f"/>'
                 % (y, w, dk, 0.30 - i * 0.028))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720" width="960" height="720">
<rect width="960" height="720" fill="{warm}"/>
<g>
  <rect x="96" y="112" width="520" height="470" fill="{lt}" opacity=".16"/>
  <rect x="136" y="86" width="520" height="470" fill="{slate}" opacity=".13"/>
  <rect x="176" y="60" width="560" height="500" fill="{sheet}" stroke="{rule}" stroke-width="2"/>
  <rect x="176" y="60" width="560" height="10" fill="{slate}"/>
  <rect x="196" y="104" width="180" height="9" fill="{dk}" opacity=".72"/>
  <rect x="196" y="130" width="118" height="7" fill="{dk}" opacity=".36"/>
  <line x1="196" y1="168" x2="716" y2="168" stroke="{rule}" stroke-width="2"/>
  <rect x="196" y="192" width="238" height="14" fill="{slate}" opacity=".85"/>
  {rows}
  <line x1="196" y1="452" x2="716" y2="452" stroke="{rule}" stroke-width="2"/>
  <rect x="196" y="476" width="132" height="9" fill="{dk}" opacity=".5"/>
  <rect x="612" y="470" width="104" height="34" fill="{slate}"/>
</g>
<g opacity=".9">
  <circle cx="742" cy="606" r="74" fill="none" stroke="{slate}" stroke-width="3"/>
  <circle cx="742" cy="606" r="46" fill="none" stroke="{lt}" stroke-width="2"/>
  <line x1="794" y1="658" x2="856" y2="700" stroke="{slate}" stroke-width="10" stroke-linecap="round"/>
</g>
</svg>'''


ART = {'dorfmancpas': (dorfman, 'out/dorfmancpas/img/hero.png', 960, 720)}


async def render(slug):
    fn, out, w, h = ART[slug]
    svg = fn()
    path = os.path.join(HERE, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            '*{margin:0;padding:0}body{width:%dpx;height:%dpx;overflow:hidden}'
            'svg{display:block}</style></head><body>%s</body></html>' % (w, h, svg))
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        await pg.set_content(html, wait_until='domcontentloaded')
        await pg.wait_for_timeout(150)
        await pg.screenshot(path=path)
        await b.close()
    print('%-34s %7d bytes' % (out, os.path.getsize(path)))


if __name__ == '__main__':
    for s in (sys.argv[1:] or list(ART)):
        asyncio.run(render(s))
