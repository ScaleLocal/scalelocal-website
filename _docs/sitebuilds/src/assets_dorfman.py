# -*- coding: utf-8 -*-
"""og.png + apple-touch-icon.png for the Mill City build, in its own visual language."""
import os, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'dorfmancpas')
CHALK, SLATE, VERM, QUIET = '#F4EFE7', '#1B2530', '#2F4E6E', '#5B646B'
FONT = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;600&family=Barlow+Semi+Condensed:wght@500;600&display=swap" rel="stylesheet">')
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">'
        '<rect x="7" y="17" width="24" height="30" fill="none" stroke="%s" stroke-width="4"/>'
        '<rect x="33" y="17" width="24" height="30" fill="%s"/>'
        '<rect x="0" y="0" width="0" height="0" fill="%s"/></svg>')

OG = """<!DOCTYPE html><html><head><meta charset="utf-8">%s<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:%s;font-family:"Barlow Semi Condensed",Arial,sans-serif;
  display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}
.top{flex:1;padding:64px 76px 0;display:flex;flex-direction:column;justify-content:center}
.brand{display:flex;align-items:center;gap:18px;margin-bottom:34px}
.mk{width:56px;height:56px}
.nm{font-family:"Spectral",Georgia,serif;font-size:25px;font-weight:600;color:#1A1F22;line-height:1.15}
.nm span{display:block;font-size:14px;font-weight:400;font-stretch:normal;color:%s;margin-top:5px}
h1{font-family:"Spectral",Georgia,serif;font-size:58px;font-weight:600;color:#1A1F22;line-height:1.07;
  letter-spacing:-.015em;max-width:20ch}
.bar{background:%s;border-top:7px solid %s;padding:22px 76px;display:flex;
  justify-content:space-between;align-items:center;color:#E8EAEB;font-size:19px}
.bar b{color:#fff;font-weight:700}
.bar .r{color:#9FA8AD;font-size:17px}
</style></head><body>
<div class="top"><div class="brand"><div class="mk">%s</div>
<div class="nm">Dorfman &amp; Dorfman, CPAs<span>Wilmington, Massachusetts &middot; since 2008</span></div></div>
<h1>Accounting that holds up when somebody checks.</h1></div>
<div class="bar"><span><b>Two</b> &nbsp;Certified Public Accountants</span>
<span class="r">(781) 780-7069 &middot; 402 Main Street, Wilmington</span></div>
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
