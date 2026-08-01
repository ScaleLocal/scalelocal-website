# -*- coding: utf-8 -*-
"""og.png + apple-touch-icon.png for the Mill City build, in its own visual language."""
import os, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'millcityaccounting')
CHALK, SLATE, VERM, QUIET = '#F2F0EA', '#232A2E', '#C4401A', '#6A7278'
FONT = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100,400;'
        '100,600;112,700&display=swap" rel="stylesheet">')
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M10 30a22 22 0 0 1 44 0v6H10z" fill="%s"/>'
        '<rect x="10" y="42" width="44" height="6" fill="%s"/>'
        '<rect x="10" y="52" width="44" height="4" fill="%s" opacity=".55"/></svg>')

OG = """<!DOCTYPE html><html><head><meta charset="utf-8">%s<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:%s;font-family:"Archivo",Arial,sans-serif;
  display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}
.top{flex:1;padding:64px 76px 0;display:flex;flex-direction:column;justify-content:center}
.brand{display:flex;align-items:center;gap:18px;margin-bottom:34px}
.mk{width:56px;height:56px}
.nm{font-size:25px;font-weight:700;font-stretch:expanded;color:#1A1F22;line-height:1.15}
.nm span{display:block;font-size:14px;font-weight:400;font-stretch:normal;color:%s;margin-top:5px}
h1{font-size:60px;font-weight:700;font-stretch:expanded;color:#1A1F22;line-height:1.07;
  letter-spacing:-.015em;max-width:20ch}
.bar{background:%s;border-top:7px solid %s;padding:22px 76px;display:flex;
  justify-content:space-between;align-items:center;color:#E8EAEB;font-size:19px}
.bar b{color:#fff;font-weight:700}
.bar .r{color:#9FA8AD;font-size:17px}
</style></head><body>
<div class="top"><div class="brand"><div class="mk">%s</div>
<div class="nm">Mill City Accounting<span>Lowell, Massachusetts &middot; since 2018</span></div></div>
<h1>An accountant on Kearney Square who has already seen your year.</h1></div>
<div class="bar"><span><b>Restaurants</b> &nbsp;and&nbsp; <b>rental property</b></span>
<span class="r">(978) 979-2904 &middot; 10 Kearney Square, Lowell</span></div>
</body></html>""" % (FONT, CHALK, QUIET, SLATE, VERM, MARK % (VERM, CHALK, CHALK))

ICON = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0}body{width:180px;height:180px;background:%s;display:flex;
align-items:center;justify-content:center}svg{width:120px;height:120px}
</style></head><body>%s</body></html>""" % (SLATE, MARK % (VERM, CHALK, CHALK))


async def run():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        await pg.set_content(OG, wait_until='networkidle')
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(OUT, 'og.png'))
        await pg.close()
        pg = await b.new_page(viewport={'width': 180, 'height': 180})
        await pg.set_content(ICON, wait_until='domcontentloaded')
        await pg.screenshot(path=os.path.join(OUT, 'apple-touch-icon.png'))
        await pg.close()
        await b.close()
    for f in ('og.png', 'apple-touch-icon.png'):
        print('%-22s %6d bytes' % (f, os.path.getsize(os.path.join(OUT, f))))

if __name__ == '__main__':
    asyncio.run(run())
