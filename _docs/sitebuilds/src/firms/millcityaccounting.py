# -*- coding: utf-8 -*-
"""
Firm profile — Mill City Accounting Services LLC (Lowell, Massachusetts).

Every fact here comes from the firm's own published material. What was
deliberately left out, and what the client must confirm, is listed in the
build report that accompanies this site rather than in a file here.

*** Scott Marchlik claims NO professional credential anywhere on his own site.
    He is not described as a CPA and not described as an EA. The only "CPA" on
    the live site refers to a FORMER EMPLOYER (a CPA firm in Cambridge, MA).
    Nothing in this build may call him a CPA, call this a CPA firm, or imply a
    licence he has not claimed. `brand_sub` is "Accounting & Tax Services".
    `BANNED` below is the mechanical backstop for that rule. ***
"""

FIRM = dict(
    name='Mill City Accounting Services LLC',
    short='Mill City',
    founded=2018,
    years=8,
    email='scott@millcityaccounting.com',
    addr='10 Kearney Square, Suite 302',
    city='Lowell', state='MA', state_full='Massachusetts', zip='01852',
    tel='+19789792904', ph='(978) 979-2904', fax='(978) 856-3515',
    hours='Mon&ndash;Fri 9:00 AM&ndash;5:00 PM &middot; Sat by appointment',
    office_page=None,
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Mill+City+Accounting+Services+10+Kearney+Square+Lowell+MA+01852'),
    # branding
    favicon_letter='M',
    brand_line='Mill City Accounting',
    brand_sub='Accounting &amp; Tax Services',
    nav_cta='Talk to Scott',
    topbar='Accounting &amp; Tax Services &middot; Lowell, MA &middot; Since 2018',
    footer_blurb=('Tax preparation, bookkeeping, payroll and notarization for small businesses '
                  'and individuals in Lowell, Massachusetts. Founded by Scott Marchlik in 2018.'),
    footer_note='Notarization: licensed in the Commonwealth of Massachusetts.',
    footer_services=[
        ('services/tax-preparation.html', 'Tax Preparation'),
        ('services/bookkeeping.html', 'Bookkeeping'),
        ('services/payroll.html', 'Payroll'),
        ('services/notary-services.html', 'Notary Services'),
        ('restaurant-accounting.html', 'Restaurant Accounting'),
        ('rental-property-accounting.html', 'Rental Property Accounting'),
    ],
    footer_firm=[
        ('about.html', 'About Scott Marchlik'),
        ('services/index.html', 'All services'),
        ('calculators/index.html', 'Financial calculators'),
        ('faq.html', 'Common questions'),
        ('contact.html', 'Contact &amp; directions'),
    ],
)

# Spruce and copper — the mill yard rather than the boardroom. Deliberately
# distinct from the navy/bronze used elsewhere in the engine. Every pair in
# contrast.py's matrix clears WCAG AA at these values (verified 2026-07-30).
DESIGN = 'millyard'   # see design.py

T = dict(ink='#0F2E29', ink2='#17423B', acc='#C8763F', accd='#8A4A22',
         accrgb='200,118,63', cream='#F4EDE4')

NAV = [('services/index.html', 'Services', 'services'),
       ('restaurant-accounting.html', 'Restaurants', 'restaurants'),
       ('rental-property-accounting.html', 'Rentals', 'rentals'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('about.html', 'About', 'about'),
       ('contact.html', 'Contact', 'contact')]

# ---------------------------------------------------------------------------
# LOGO — proposal, not the firm's existing mark.
#
# A three-by-three plain weave: warp and weft, each thread broken where it
# passes under the one crossing it. Lowell is the Mill City because of the
# textile mills on the Merrimack, and a plain weave is the most elementary
# thing those mills made. It is also, drawn flat, a ruled grid — the same
# figure as a ledger. Nine rectangles, one flat colour, no outline, no
# gradient: it holds at 50px in the header and still reads as deliberate
# structure at 20px.
# ---------------------------------------------------------------------------
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="11" y="11" width="14.6" height="8" fill="currentColor"/>'
        '<rect x="28" y="11" width="8" height="14.6" fill="currentColor"/>'
        '<rect x="38.4" y="11" width="14.6" height="8" fill="currentColor"/>'
        '<rect x="11" y="21.4" width="8" height="21.2" fill="currentColor"/>'
        '<rect x="21.4" y="28" width="21.2" height="8" fill="currentColor"/>'
        '<rect x="45" y="21.4" width="8" height="21.2" fill="currentColor"/>'
        '<rect x="11" y="45" width="14.6" height="8" fill="currentColor"/>'
        '<rect x="28" y="38.4" width="8" height="14.6" fill="currentColor"/>'
        '<rect x="38.4" y="45" width="14.6" height="8" fill="currentColor"/>'
        '</svg>')

# The nine rectangles above, in the 64-unit logo space, reused to raster the
# apple-touch icon (see _touch_icon below).
_MARK_RECTS = [(11, 11, 14.6, 8), (28, 11, 8, 14.6), (38.4, 11, 14.6, 8),
               (11, 21.4, 8, 21.2), (21.4, 28, 21.2, 8), (45, 21.4, 8, 21.2),
               (11, 45, 14.6, 8), (28, 38.4, 8, 14.6), (38.4, 45, 14.6, 8)]


def _touch_icon(out_dir, size=180):
    """Write apple-touch-icon.png. The engine's <head> links this relatively, so
    the file has to exist or QA's link check fails on every page. render_assets.py
    is hard-wired to another firm and is off-limits, so the mark — nine plain
    rectangles — is rasterised here in pure Python."""
    import os, zlib, struct
    bg = (0x0F, 0x2E, 0x29)
    fg = (0xFF, 0xFF, 0xFF)
    k = size / 64.0
    rows = [bytearray(bytes(bg) * size) for _ in range(size)]
    for x, y, w, h in _MARK_RECTS:
        x0, x1 = int(round(x * k)), int(round((x + w) * k))
        y0, y1 = int(round(y * k)), int(round((y + h) * k))
        for yy in range(max(y0, 0), min(y1, size)):
            row = rows[yy]
            for xx in range(max(x0, 0), min(x1, size)):
                row[xx * 3:xx * 3 + 3] = bytes(fg)
    raw = b''.join(b'\x00' + bytes(r) for r in rows)

    def chunk(tag, data):
        body = tag + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'apple-touch-icon.png'), 'wb') as fh:
        fh.write(png)


_OG_ALT_WRONG = ' — Certified Public Accountants"'
_OG_ALT_RIGHT = ' — accounting, tax, payroll and bookkeeping in Lowell, Massachusetts"'


def _fix_og_alt():
    """The engine hard-codes "Certified Public Accountants" into og:image:alt.
    That is false for this firm and build.py is off-limits, so the emitted head
    is corrected here, in this firm's own module, at render time.

    build.py is normally run as a script, so the engine lives in sys.modules
    under '__main__' as well as under 'build' (content modules import it by
    name). Both copies are patched; nothing outside this process is touched.
    BANNED (below) fails the build if the correction ever stops working."""
    import sys

    def is_engine(m):
        return (m is not None and getattr(m, 'DEMO_NOTICE', None) is not None
                and callable(getattr(m, 'head', None))
                and not getattr(m, '_mca_head_patched', False))

    def wrap(original):
        def head(p):
            return original(p).replace(_OG_ALT_WRONG, _OG_ALT_RIGHT)
        return head

    for mod in list(sys.modules.values()):
        if is_engine(mod):
            mod.head = wrap(mod.head)
            mod._mca_head_patched = True


def pages():
    import build
    _fix_og_alt()
    _touch_icon(build.OUT)
    import content_millcityaccounting
    return content_millcityaccounting.pages()


# QA gates specific to this firm
ALLOWED_PHONES = ['(978) 979-2904', '(978) 856-3515']

BANNED = [
    # Vacated 01/01/2025. The old address must never reappear.
    # ('Central Street' alone is not banned: Kearney Square is where Merrimack,
    #  Bridge and Central streets meet, which is legitimate and useful.)
    '97 Central', 'Suite 403', '403F',
    # No credential is claimed on the firm's own site, so none may be implied.
    # (The engine hard-codes the first of these into og:image:alt; _fix_og_alt
    # removes it, and this entry is what proves the removal worked.)
    'Certified Public Accountant', 'CPAs', 'Enrolled Agent', 'Marchlik, CPA',
    'our CPA', 'CPA firm in Lowell', 'a CPA in Lowell', 'licensed CPA',
    'AICPA', 'Massachusetts Society of', 'accredited in',
    # One person. Nothing may imply staff, partners or a team.
    'our team', 'our staff', 'our partners', 'our accountants', 'our associates',
    'our professionals', 'a partner will', 'one of our', 'meet the team',
    # Things the firm does not have.
    'client portal', 'secure portal', 'peer review', 'free consultation',
]
