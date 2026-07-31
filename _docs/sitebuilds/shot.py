import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    url, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    full = len(sys.argv) > 5
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        await pg.goto(url, wait_until='networkidle')
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=out, full_page=full)
        await b.close()
asyncio.run(main())
