# -*- coding: utf-8 -*-
"""
og.png (1200x630) and apple-touch-icon.png (180x180) for the Carella build.

render_assets.py is driven by design.py and firms/<slug>.py — i.e. by the retired
template engine — so it would produce a share card in the wrong visual language.
This renders both assets in this site's own: cool paper, graphite ink, one pine
accent, one typeface, hairline rules.

    python3 assets_carella.py
"""
import os, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'carellacpa')

PAPER, INK, SOFT, RULE, PINE = '#FCFCFB', '#131511', '#4E5149', '#DFE0D8', '#1E4437'

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700'
        '&display=swap" rel="stylesheet">')

MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M53 11H11v42h42" fill="none" stroke="%s" stroke-width="5.5" '
        'stroke-linecap="square"/>'
        '<rect x="39" y="28" width="9" height="8" fill="%s"/></svg>')

OG = """<!DOCTYPE html><html><head><meta charset="utf-8">%s<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:%s;color:%s;
  font-family:"Public Sans",Arial,sans-serif;display:flex;flex-direction:column;
  justify-content:space-between;padding:74px 88px;-webkit-font-smoothing:antialiased}
.top{display:flex;align-items:flex-start;gap:26px}
.mk{width:64px;height:64px;flex:0 0 64px}
.nm{font-size:31px;font-weight:700;letter-spacing:-.03em;line-height:1.15}
.sb{font-size:13px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
  color:%s;margin-top:9px}
h1{font-size:66px;font-weight:700;letter-spacing:-.035em;line-height:1.06;max-width:19ch}
.rule{height:2px;background:%s;margin:0 0 26px}
.foot{display:flex;justify-content:space-between;align-items:flex-end;
  border-top:1px solid %s;padding-top:22px;font-size:19px;color:%s;
  font-variant-numeric:tabular-nums}
.foot b{color:%s;font-weight:600}
</style></head><body>
<div class="top"><div class="mk">%s</div>
<div><div class="nm">Charles M. Carella, CPA</div>
<div class="sb">Certified Public Accountant</div></div></div>
<div><div class="rule" style="width:104px"></div>
<h1>Tax and accounting for people and the businesses they run.</h1></div>
<div class="foot"><span><b>330 Boston Road, Suite 12</b> &middot; North Billerica, Massachusetts</span>
<span>(978) 663-6419</span></div>
</body></html>""" % (FONT, PAPER, INK, SOFT, PINE, RULE, SOFT, INK, MARK % (PINE, PINE))

ICON = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0}
body{width:180px;height:180px;background:%s;display:flex;align-items:center;
  justify-content:center}
svg{width:112px;height:112px}
</style></head><body>%s</body></html>""" % (PINE, MARK % (PAPER, PAPER))


async def run():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1200, 'height': 630},
                              device_scale_factor=1)
        await pg.set_content(OG, wait_until='networkidle')
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(OUT, 'og.png'))
        await pg.close()
        pg = await b.new_page(viewport={'width': 180, 'height': 180})
        await pg.set_content(ICON, wait_until='domcontentloaded')
        await pg.screenshot(path=os.path.join(OUT, 'apple-touch-icon.png'))
        await pg.close()
        await b.close()
    for f in ('og.png', 'apple-touch-icon.png'):
        p = os.path.join(OUT, f)
        print('%-22s %6d bytes' % (f, os.path.getsize(p)))


if __name__ == '__main__':
    asyncio.run(run())
