# -*- coding: utf-8 -*-
"""
Render og.png (1200x630) + apple-touch-icon.png (180x180) for the selected firm.

Firm-driven: theme, name, logo and strapline all come from firms/<slug>.py. This was
previously hardcoded to one firm, which meant every other build either had no OG image
or one produced by a throwaway script — and the hardcoded copy still advertised an
office that had since closed, phone number and all.

    BUILD_FIRM=<slug> python3 render_assets.py
"""
import os, asyncio, importlib, re
import html as _html
from playwright.async_api import async_playwright

SLUG = os.environ.get('BUILD_FIRM', 'kpw-cpa')
_F = importlib.import_module('firms.' + SLUG.replace('-', '_'))
FIRM, T, LOGO = _F.FIRM, _F.T, _F.LOGO
import design as _design
D = _design.resolve(getattr(_F, 'DESIGN', 'ledger'))

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', SLUG)
INK, INK2, ACC = T['ink'], T['ink2'], T['acc']


def _rgb(hexc):
    c = hexc.lstrip('#')
    return ','.join(str(int(c[i:i + 2], 16)) for i in (0, 2, 4))


ACCRGB = T.get('accrgb') or _rgb(ACC)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=' + D['gfont'] + '&display=swap" rel="stylesheet">')

# Strapline: firm may supply og_sub, else fall back to its footer blurb.
SUB = FIRM.get('og_sub') or FIRM['footer_blurb']
SUB = re.sub(r'&amp;', '&', SUB)
if len(SUB) > 150:
    SUB = SUB[:147].rsplit(' ', 1)[0] + '…'

# Bar: this firm's own city and phone. Never a hardcoded office.
BAR_L = '<b>' + _html.escape(FIRM['city']) + '</b> ' + FIRM['ph']
BAR_R = re.sub(r'&amp;', '&', FIRM['brand_sub'])

# LOGO uses fill="currentColor", so setting colour on the wrapper renders it white.
SERIF, SANS, HW = D['serif'], D['sans'], D['hweight']
OG = f'''<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;
background:radial-gradient(760px 420px at 82% 12%,rgba({ACCRGB},.32),transparent 62%),
linear-gradient(155deg,{INK},{INK2});color:#fff;
font-family:{SANS};position:relative}}
body::after{{content:"";position:absolute;inset:0;
background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:24px 24px;opacity:.6}}
.art{{position:absolute;right:-40px;top:50%;transform:translateY(-50%);width:520px;
opacity:.10;stroke:#fff;stroke-width:2.4;fill:none}}
.w{{position:relative;z-index:2;padding:76px 84px;height:100%;display:flex;flex-direction:column;justify-content:center}}
.top{{display:flex;align-items:center;gap:20px;margin-bottom:34px}}
.mk{{width:104px;height:104px;flex:0 0 104px;color:#fff}}
.mk svg{{width:100%;height:100%;display:block}}
.mk svg text{{font-family:{SERIF};font-weight:600}}
.eb{{font-size:15px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:#e8d3a8}}
h1{{font-family:{SERIF};font-weight:{HW};font-size:58px;line-height:1.07;
letter-spacing:-.02em;max-width:17ch}}
.sub{{margin-top:22px;font-size:22px;color:#dcd7cb;max-width:36ch;line-height:1.45}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:74px;background:rgba(0,0,0,.26);
display:flex;align-items:center;justify-content:space-between;padding:0 84px;
font-size:17px;color:#cdc8bc;font-weight:500;border-top:1px solid rgba(255,255,255,.12)}}
.bar b{{color:#fff;font-weight:600}}
</style></head><body>
<svg class="art" viewBox="0 0 128 128"><path d="M34 96V54l16-10v52M58 96V40l16-10v66M82 96V64l16-10v42M24 96h84"/></svg>
<div class="w"><div class="top"><div class="mk">{LOGO}</div>
<div class="eb">{BAR_R}</div></div>
<h1>{_html.escape(FIRM['name'])}</h1>
<div class="sub">{SUB}</div></div>
<div class="bar"><span>{BAR_L}</span><span>{BAR_R}</span></div>
</body></html>'''

ICON = f'''<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0}}
body{{width:180px;height:180px;overflow:hidden;background:{INK};
display:flex;align-items:center;justify-content:center}}
.mk{{width:150px;height:150px;color:#fff}}
.mk svg{{width:100%;height:100%;display:block}}
.mk svg text{{font-family:{SERIF};font-weight:600}}
</style></head><body><div class="mk">{LOGO}</div></body></html>'''


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for src, w, h, name in ((OG, 1200, 630, 'og.png'), (ICON, 180, 180, 'apple-touch-icon.png')):
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            await pg.set_content(src, wait_until='load')
            try:
                await pg.wait_for_function("document.fonts.status === 'loaded'", timeout=6000)
            except Exception:
                pass
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=os.path.join(OUT, name))
            print('  wrote', name, f'({w}x{h})')
            await pg.close()
        await b.close()


if __name__ == '__main__':
    print('assets for', SLUG)
    asyncio.run(main())
