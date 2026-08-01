# -*- coding: utf-8 -*-
"""
All pages for Fitzpatrick & Goguen CPAs P.C. (slug: bgoguen).

Sourcing rule for this module: nothing is asserted about the firm that is not on
the firm's own site. No founding year, no client counts, no memberships beyond
the two board seats the bios state, no credentials for the three people who list
none, and no investment advisory service — two of the five are Investment
Advisor Representatives with North Atlantic Investment Partners, LLC, which is a
fact about those individuals and is stated as such.

24 pages: 5 root, 4 services, 6 team, 3 guides, 6 calculators.
"""
import html, os, re
from build import (FIRM, BASE, T, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   breadcrumb_schema, faq_schema, person_schema, article_schema, OUT)
import calculators as C

PORTAL = 'https://www.bgoguen.com/login'
ORG_ID = BASE + '#firm'
TEL = FIRM['tel']
PH = FIRM['ph']
EMAIL = FIRM['email']

CTA_MAIN = ('Tell us what you are working through.',
            'Call the office at ' + PH + ' or email ' + EMAIL + '. If you are already a client, '
            'the portal is the fastest way to get documents to us.')
CTA_TAX = ('Start before the year closes, not after.',
           'Most of what changes a tax bill is decided during the year. Call ' + PH + ' or email '
           + EMAIL + ' and describe the situation.')
CTA_PORTAL = ('Everything you send us has a home.',
              'The client portal handles documents, signatures, messages and invoices. '
              'Call ' + PH + ' or email ' + EMAIL + ' if you need access.')


# ---------------------------------------------------------------- schema
def org_schema():
    """Firm-specific organisation schema. The engine's org_schema() carries the
    reference firm's memberships, geo and founding date; none of those are
    published by this firm, so it is not reused."""
    return {
        "@context": "https://schema.org", "@type": "AccountingService", "@id": ORG_ID,
        "name": FIRM['name'], "legalName": FIRM['name'], "url": BASE,
        "email": FIRM['email'], "telephone": FIRM['ph'], "faxNumber": FIRM['fax'],
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                    "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                    "postalCode": FIRM['zip'], "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea", "name": "Middlesex County, Massachusetts"}],
        "knowsAbout": ["Bookkeeping", "Personal income tax preparation",
                       "Small business tax planning", "Tax return preparation"],
        "hasMap": FIRM['maps'],
    }


def svc_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "description": desc, "url": url, "serviceType": name,
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "AdministrativeArea", "name": "Middlesex County, Massachusetts"}}


def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()


def _faq_ld(qas):
    return faq_schema([(q, _plain(a)) for q, a in qas])


# ---------------------------------------------------------------- fragments
def sec(inner, cls='sec'):
    return '<section class="' + cls + '"><div class="wrap">' + inner + '</div></section>'


def head_blk(h2, lead=None, eyebrow=None, ondark=False):
    s = '<div class="sec-head reveal">'
    if eyebrow:
        s += '<span class="eyebrow' + (' on-dark' if ondark else '') + '">' + eyebrow + '</span>'
    s += '<h2>' + h2 + '</h2>'
    if lead:
        s += '<p class="lead">' + lead + '</p>'
    return s + '</div>'


def split(main_html, aside_html):
    return '<div class="split">' + main_html + '<div class="aside">' + aside_html + '</div></div>'


def prose(inner):
    return '<div class="prose reveal">' + inner + '</div>'


def acard(title, body, btn_href=None, btn_label=None, ext=False):
    s = '<div class="acard"><div class="t">' + title + '</div>' + body
    if btn_href:
        s += ('<a class="btn b-acc" href="' + btn_href + '"'
              + (' target="_blank" rel="noopener"' if ext else '') + '>' + btn_label + '</a>')
    return s + '</div>'


def lcard(title, items, d=0):
    """items: list of (href, label, external?)"""
    s = '<div class="acard light"><div class="t">' + title + '</div><ul>'
    for it in items:
        href, label = it[0], it[1]
        ext = len(it) > 2 and it[2]
        url = href if ext else rel(d, href)
        s += ('<li><a href="' + url + '"' + (' target="_blank" rel="noopener"' if ext else '')
              + '><span class="ck">&rarr;</span> ' + label + '</a></li>')
    return s + '</ul></div>'


def portal_acard():
    return acard('Client portal',
                 '<p>Send documents, sign what needs signing, message the office and settle '
                 'invoices &mdash; all in one place.</p>',
                 PORTAL, 'Sign in to the portal', ext=True)


def call_acard(text=None):
    return acard('Talk to us',
                 '<p>' + (text or 'Describe the situation in a few minutes. If this is not the '
                          'right firm for it, we will tell you.') + '</p>',
                 'tel:' + TEL, PH)


def _card(d, href, ic, title, text, num=None, ext=False):
    url = href if ext else rel(d, href)
    return ('<a class="card reveal" href="' + url + '"'
            + (' target="_blank" rel="noopener"' if ext else '') + '>'
            + ('<span class="num">' + num + '</span>' if num else '')
            + '<div class="cic">' + icon(ic) + '</div><h3>' + title + '</h3><p>' + text + '</p>'
            '<span class="more">Read more ' + ARROW + '</span></a>')


# ---------------------------------------------------------------- assets
def _write_assets():
    """apple-touch-icon.png is referenced relatively by the engine's <head>, so it
    has to exist in the output tree. og.png is referenced absolutely but is
    generated too so the demo previews properly when shared."""
    ink, ink2, acc = T['ink'], T['ink2'], T['acc']
    icon_path = os.path.join(OUT, 'apple-touch-icon.png')
    og_path = os.path.join(OUT, 'og.png')
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        _solid_png(icon_path, 180, 180, ink)
        _solid_png(og_path, 1200, 630, ink)
        return

    def _font(size, serif=True):
        cands = (['/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf',
                  '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
                  '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf']
                 if serif else
                 ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                  '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'])
        for c in cands:
            if os.path.exists(c):
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def mark(dr, x, y, s, col):
        """The bracketed FG monogram, drawn at scale s from a 64-unit grid."""
        u = s / 64.0
        w = max(2, int(round(3 * u)))
        for x0, x1, foot in ((9.5, 14.5, 1), (54.5, 49.5, -1)):
            dr.rectangle([x + x0 * u, y + 14 * u, x + x0 * u + w, y + 50 * u], fill=col)
            dr.rectangle([x + min(x0, x1) * u, y + 14 * u,
                          x + max(x0, x1) * u, y + 14 * u + w], fill=col)
            dr.rectangle([x + min(x0, x1) * u, y + 50 * u - w,
                          x + max(x0, x1) * u, y + 50 * u], fill=col)
        f = _font(int(round(30 * u)))
        dr.text((x + 32 * u, y + 32 * u), 'FG', font=f, fill=col, anchor='mm')

    # --- apple touch icon
    S = 180
    im = Image.new('RGB', (S, S), ink)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0, 0, S - 1, S - 1], radius=34, fill=ink)
    mark(dr, 18, 18, 144, '#FFFFFF')
    im.save(icon_path)

    # --- open graph card
    W, H = 1200, 630
    og = Image.new('RGB', (W, H), ink)
    d2 = ImageDraw.Draw(og)
    for i in range(H):                      # vertical wash toward ink2
        t = i / float(H)
        d2.line([(0, i), (W, i)], fill=_mix(ink, ink2, t))
    d2.rectangle([0, H - 78, W, H], fill=_mix(ink, '#000000', 0.28))
    mark(d2, 84, 74, 96, '#FFFFFF')
    d2.text((200, 96), 'FITZPATRICK & GOGUEN', font=_font(28, serif=False), fill='#E8D3A8')
    d2.text((200, 132), 'CERTIFIED PUBLIC ACCOUNTANTS', font=_font(20, serif=False), fill='#B6B0A3')
    d2.text((84, 250), 'Helping you achieve', font=_font(70), fill='#FFFFFF')
    d2.text((84, 336), 'your ideal life.', font=_font(70), fill='#FFFFFF')
    d2.text((84, 448), 'Bookkeeping  ·  Personal tax  ·  Small business tax',
            font=_font(27, serif=False), fill='#DCD7CB')
    d2.text((84, H - 52), 'Billerica, Massachusetts', font=_font(22, serif=False), fill='#CDC8BC')
    d2.text((W - 84, H - 52), FIRM['ph'], font=_font(22, serif=False), fill='#FFFFFF', anchor='ra')
    d2.rectangle([84, 214, 150, 218], fill=acc)
    og.save(og_path)


def _mix(a, b, t):
    a = a.lstrip('#')
    b = b.lstrip('#')
    return tuple(int(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t) for i in (0, 2, 4))


def _solid_png(path, w, h, colour):
    """Stdlib-only fallback if PIL is unavailable."""
    import zlib, struct
    r, g, b = _mix(colour, colour, 0)
    raw = b''.join(b'\x00' + bytes([r, g, b]) * w for _ in range(h))

    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(png)


# ================================================================= TEAM DATA
TEAM = [
    dict(slug='thomas-l-fitzpatrick', initials='TF', name='Thomas L. Fitzpatrick IV',
         cred='MBA, EA, CPA', role='President & Shareholder',
         meta='MBA, EA, CPA &middot; President &amp; Shareholder',
         alumni=['University of Massachusetts Dartmouth', 'Bowling Green State University'],
         card='President and shareholder. A CPA and an IRS Enrolled Agent, with an MBA from '
              'Bowling Green State University.',
         title='Thomas L. Fitzpatrick IV, MBA, EA, CPA | Fitzpatrick & Goguen',
         desc='Thomas L. Fitzpatrick IV, MBA, EA, CPA is President and a shareholder of '
              'Fitzpatrick & Goguen CPAs P.C. in Billerica, Massachusetts.',
         h1='Thomas L. Fitzpatrick IV, MBA, EA, CPA',
         sub='President and shareholder &middot; Certified Public Accountant and IRS Enrolled Agent',
         education=[
             'Undergraduate study in marketing, University of Massachusetts Dartmouth',
             'Master of Business Administration, Bowling Green State University',
             'Certified Public Accountant, Commonwealth of Massachusetts &mdash; licensed May 2022',
             'IRS Enrolled Agent &mdash; 2017',
             'Series 65 &mdash; January 2020',
         ],
         history=[
             'President and shareholder, Fitzpatrick &amp; Goguen CPAs P.C.',
             'Investment Advisor Representative, North Atlantic Investment Partners, LLC',
             'Board member, Massachusetts Association of Accountants',
             'Board member, Boys &amp; Girls Club of Greater Billerica',
         ],
         body='''
<h2>Two licences, pointed at the same problem</h2>
<p>Thomas Fitzpatrick holds two credentials that do different jobs. The CPA licence, issued by the Commonwealth of Massachusetts in May 2022, is the state licence that governs public accounting practice. The IRS Enrolled Agent designation, earned in 2017, is a federal credential: an Enrolled Agent is admitted to practice before the Internal Revenue Service and may represent a taxpayer in examinations, collections and appeals.</p>
<p>The practical consequence for a client is that the person who prepared the return is also the person permitted to argue about it. When a notice arrives &mdash; and notices arrive for reasons that have nothing to do with error &mdash; there is no handoff and no re-explanation of the facts to somebody new.</p>
<h2>Business training behind the tax work</h2>
<p>His undergraduate work was in marketing at the University of Massachusetts Dartmouth; the MBA came later, at Bowling Green State University. That is a useful order for someone who spends the year with small business owners. A return is the last four inches of a much longer conversation about pricing, capacity, borrowing and what the owner takes out of the company, and it helps if the accountant has been taught to think about all of it.</p>
<h2>Outside the practice</h2>
<p>He sits on the board of the Massachusetts Association of Accountants and on the board of the Boys &amp; Girls Club of Greater Billerica. He also holds a Series 65, obtained in January 2020, and is an Investment Advisor Representative with North Atlantic Investment Partners, LLC &mdash; a role held in that firm, separate from the accounting and tax services described on this site.</p>
<h2>Where his work shows up</h2>
<p><a href="../services/business-tax.html">Small business tax</a>, <a href="../services/personal-tax.html">personal tax</a>, and the planning conversations that happen long before either return is prepared.</p>
'''),

    dict(slug='brian-d-goguen', initials='BG', name='Brian D. Goguen',
         cred='MST, CPA', role='Certified Public Accountant',
         meta='MST, CPA',
         alumni=['University of Massachusetts Lowell', 'Suffolk University', 'Bentley College'],
         card='A Massachusetts CPA since 1981, with a Master of Science in Taxation from Bentley '
              'College. The practice carried his name for years.',
         title='Brian D. Goguen, MST, CPA | Fitzpatrick & Goguen CPAs P.C.',
         desc='Brian D. Goguen, MST, CPA has been a licensed Certified Public Accountant since '
              '1981 and holds a Master of Science in Taxation from Bentley College.',
         h1='Brian D. Goguen, MST, CPA',
         sub='Certified Public Accountant since 1981 &middot; Master of Science in Taxation, Bentley College',
         education=[
             'Undergraduate study in accounting, University of Massachusetts Lowell',
             'Master of Business Administration, Suffolk University',
             'Master of Science in Taxation, Bentley College',
             'Certified Public Accountant since 1981',
         ],
         history=[
             'Fitzpatrick &amp; Goguen CPAs P.C. &mdash; the practice formerly known as Brian D. Goguen, P.C.',
             'Investment Advisor Representative, North Atlantic Investment Partners, LLC',
             'Board member, Boys &amp; Girls Club of Billerica',
         ],
         body='''
<h2>Forty-five years of Massachusetts tax law</h2>
<p>Brian Goguen has been a licensed Certified Public Accountant since 1981. A practice of that length is not a trophy; it is a data set. It covers the 1986 Tax Reform Act, the growth of the S corporation as the default form for a small company, the 2017 rewrite of the federal code, and every Massachusetts change layered on top of those &mdash; including the ones that arrived quietly and mattered more than the ones that made the news.</p>
<p>What that buys a client is triage. Most tax questions have a settled answer, a few genuinely depend on the facts, and a small number are traps. Knowing which is which, quickly, is most of the value.</p>
<h2>A tax degree, not just a tax practice</h2>
<p>His graduate work went in two directions: a Master of Business Administration at Suffolk University, and then a Master of Science in Taxation at Bentley College. The MST is a specialist degree &mdash; research, the structure of the code, and the way authority actually stacks up &mdash; and it is the reason a question that starts as "can I do this?" ends with a citation rather than an opinion. His undergraduate accounting work was done at the University of Massachusetts Lowell.</p>
<h2>The name on the door</h2>
<p>The practice was known as Brian D. Goguen, P.C. before it became Fitzpatrick &amp; Goguen CPAs P.C. The web address and the client portal still carry the older name, which is worth knowing if you arrive at a sign-in page that says something different from the sign outside.</p>
<h2>Outside the practice</h2>
<p>He sits on the board of the Boys &amp; Girls Club of Billerica, and he is an Investment Advisor Representative with North Atlantic Investment Partners, LLC &mdash; a role held in that firm, separate from the accounting and tax services described on this site.</p>
<h2>Where his work shows up</h2>
<p><a href="../services/personal-tax.html">Personal tax planning and preparation</a> and <a href="../services/business-tax.html">small business tax</a>.</p>
'''),

    dict(slug='dana-reardon', initials='DR', name='Dana Reardon',
         cred='', role='Accountant', meta='Accountant &middot; with the firm since 2000',
         alumni=['Bentley College'],
         card='Accountant. With the firm since 2000, after a start in the mutual fund industry. '
              'Studied accounting at Bentley College.',
         title='Dana Reardon, Accountant | Fitzpatrick & Goguen CPAs P.C.',
         desc='Dana Reardon has been an accountant with Fitzpatrick & Goguen CPAs P.C. in '
              'Billerica since 2000, after beginning in the mutual fund industry.',
         h1='Dana Reardon',
         sub='Accountant &middot; with the firm since 2000',
         education=['Accounting, Bentley College'],
         history=['Fitzpatrick &amp; Goguen CPAs P.C. &mdash; since 2000',
                  'Mutual fund industry &mdash; before joining the firm'],
         body='''
<h2>Twenty-six years in the same chair</h2>
<p>Dana Reardon studied accounting at Bentley College, began work in the mutual fund industry, and joined this practice in 2000. Everything since has been here.</p>
<p>That length of service is the single most useful thing a small firm can offer, and it is the thing most firms cannot. Continuity is not a soft benefit. It is the difference between an accountant who remembers why a fixed asset was capitalised the way it was in 2014 and one who is reading the file for the first time in March.</p>
<h2>What a long tenure changes</h2>
<p>A client whose books, returns and correspondence have passed through the same hands for two decades does not have to re-explain the business each year. Carryforwards, basis, depreciation schedules, the reason a particular account exists at all &mdash; those live in the file and in the memory of the person who built them.</p>
<p>Work at a five-person firm is not narrowly divided. The same practice that keeps a client's books through the year is the practice that sees the return, which is exactly why the two ought to sit under one roof.</p>
<h2>Related</h2>
<p><a href="../services/bookkeeping.html">Bookkeeping</a> and <a href="../services/business-tax.html">small business tax</a>.</p>
'''),

    dict(slug='sean-malone', initials='SM', name='Sean Malone',
         cred='', role='Accountant', meta='Accountant &middot; with the firm since 2000',
         alumni=['University of Massachusetts Lowell'],
         card='Accountant. With the firm since 2000. Studied accounting at the University of '
              'Massachusetts Lowell.',
         title='Sean Malone, Accountant | Fitzpatrick & Goguen CPAs P.C.',
         desc='Sean Malone has been an accountant with Fitzpatrick & Goguen CPAs P.C. in '
              'Billerica, Massachusetts since 2000. He studied accounting at UMass Lowell.',
         h1='Sean Malone',
         sub='Accountant &middot; with the firm since 2000',
         education=['Accounting, University of Massachusetts Lowell'],
         history=['Fitzpatrick &amp; Goguen CPAs P.C. &mdash; since 2000'],
         body='''
<h2>Also since 2000</h2>
<p>Sean Malone studied accounting at the University of Massachusetts Lowell and joined this practice in 2000, the same year Dana Reardon did. Two of the firm's five people have therefore been at the same desk for twenty-six years.</p>
<p>It is worth stating plainly what that means for a client, because it is unusual. Public accounting has high turnover; at a large firm, the staff accountant who prepared your return last year has often moved on before the next one is due. Here, the answer to "who did my return last year" is a name, and that person is still here.</p>
<h2>Local, and staying that way</h2>
<p>UMass Lowell sits about nine miles from the office on Concord Road. A practice that draws its people from the same region it serves tends to know the ground: which employers are hiring, which contractors are busy, and what a normal year actually looks like for a small business in this part of Middlesex County.</p>
<h2>Related</h2>
<p><a href="../services/bookkeeping.html">Bookkeeping</a> and <a href="../services/personal-tax.html">personal tax</a>.</p>
'''),

    dict(slug='monirina-kim', initials='MK', name='Monirina Kim',
         cred='', role='Firm administration', meta='Firm administration &middot; since 2022',
         alumni=['Southern New Hampshire University'],
         card='Firm administration since 2022. BS in Business Administration with a concentration '
              'in business finance, Southern New Hampshire University.',
         title='Monirina Kim, Firm Administration | Fitzpatrick & Goguen CPAs',
         desc='Monirina Kim handles firm administration at Fitzpatrick & Goguen CPAs P.C. and '
              'holds a BS in Business Administration from Southern New Hampshire University.',
         h1='Monirina Kim',
         sub='Firm administration &middot; with the firm since 2022',
         education=['Bachelor of Science in Business Administration, concentration in business '
                    'finance, Southern New Hampshire University'],
         history=['Fitzpatrick &amp; Goguen CPAs P.C. &mdash; since 2022'],
         body='''
<h2>The first voice on the phone</h2>
<p>Monirina Kim joined the firm in 2022 and handles firm administration. She holds a Bachelor of Science in Business Administration from Southern New Hampshire University, with a concentration in business finance.</p>
<p>Administration in a five-person accounting practice is not a peripheral job. It is scheduling during a season when every week has a deadline in it, keeping engagement paperwork moving, chasing the one missing form that is holding up a return, and making sure that when a client calls in the third week of March somebody answers.</p>
<h2>Where the portal fits</h2>
<p>Most of what used to be a phone call and an envelope now runs through the <a href="../client-portal.html">client portal</a>: uploads, signatures, messages and invoices. Administration is where that system is kept honest &mdash; knowing what has arrived, what is outstanding, and who still needs to be asked.</p>
<h2>Related</h2>
<p><a href="../contact.html">Contact the office</a> or <a href="../client-portal.html">read about the client portal</a>.</p>
'''),
]


def _bio(t):
    url = BASE + 'team/' + t['slug'] + '.html'
    ed = ''.join('<li>' + x + '</li>' for x in t['education'])
    hi = ''.join('<li>' + x + '</li>' for x in t['history'])
    p = dict(path='team/' + t['slug'] + '.html', depth=1, nav='team',
             title=t['title'], desc=t['desc'], eyebrow=t['role'], h1=t['h1'], sub=t['sub'],
             cta_args=CTA_MAIN)
    others = [('team/' + o['slug'] + '.html', o['name']) for o in TEAM if o['slug'] != t['slug']]
    p['body'] = phero(p, [('Our team', 'team/index.html'), (t['name'], None)]) + sec(
        split(prose(t['body']
                    + '<h2>Education and credentials</h2><ul>' + ed + '</ul>'
                    + '<h2>Professional history</h2><ul>' + hi + '</ul>'
                    + '<div class="callout"><p><strong>Contact.</strong> '
                      '<a href="tel:' + TEL + '">' + PH + '</a> &middot; '
                      '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a> &middot; '
                      '<a href="' + PORTAL + '" target="_blank" rel="noopener">client portal</a></p></div>'),
              acard(t['name'], '<p>' + t['meta'] + '</p>', 'tel:' + TEL, PH)
              + portal_acard()
              + lcard('The rest of the team', others, 1)))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Our team', BASE + 'team/'), (t['name'], url)]),
                   person_schema(t['name'], _plain(t['cred']), t['role'], url,
                                 {"description": _plain(t['card']),
                                  "alumniOf": [{"@type": "EducationalOrganization", "name": n}
                                               for n in t.get('alumni', [])]})]
    return p


# ================================================================= SERVICES DATA
SERVICES = [
    dict(slug='bookkeeping', ic='ledger', nav_title='Bookkeeping',
         short='Books kept through the year, so the return is an outcome rather than an '
               'excavation.',
         title='Bookkeeping | Fitzpatrick & Goguen CPAs P.C., Billerica MA',
         desc='Bookkeeping for Billerica-area small businesses by a five-person CPA firm. Books '
              'kept through the year by the same people who prepare the tax return.',
         eyebrow='Bookkeeping', h1='Books kept through the year, not reconstructed in March.',
         sub='Bookkeeping is one of the three things this firm does. It is also the one that '
             'decides how much everything else costs.',
         body='''
<h2>The short answer</h2>
<p>We keep books for small businesses. The same practice that records the year is the practice that prepares the return at the end of it, which removes the most expensive step in small business accounting: someone unfamiliar with the business trying to work out what happened, from a bank feed, eleven months after the fact.</p>

<h2>Why the bookkeeping decides the tax bill</h2>
<p>A tax return is a report on a record. If the record is thin, the return is defensive &mdash; deductions get left on the table because nothing supports them, and positions get taken conservatively because nobody can prove otherwise. If the record is good, the return is simply the arithmetic of a year that was already understood.</p>
<p>The gap between those two outcomes is usually larger than the cost of the bookkeeping. That is the honest case for paying someone to do it.</p>

<h2>What is actually involved</h2>
<h3>Recording and categorising</h3>
<p>Every transaction has to land somewhere, and the somewhere matters. A repair and an improvement look identical on a bank statement and are treated very differently on a return. So do a distribution and a wage, a loan draw and revenue, an owner's personal charge and a business expense.</p>
<h3>Reconciliation</h3>
<p>Bank and credit card accounts are reconciled so the books agree with something external. An unreconciled ledger is an opinion. A reconciled one is evidence.</p>
<h3>The balance sheet nobody looks at</h3>
<p>Most small business owners read the profit and loss and ignore the balance sheet. It is the balance sheet that shows whether the books are actually right: a loan balance that does not match the lender's statement, an undeposited funds account that has quietly grown, a payroll liability that never clears, negative inventory. These are where errors hide.</p>
<h3>Owner activity</h3>
<p>In a closely held company, the owner's account is where the year gets confusing. Draws, contributions, personal expenses run through the business and reimbursements all need to be tracked separately, because they change basis, they change what is taxable, and they change what a lender sees.</p>

<div class="callout"><p><strong>Sending us the records.</strong> Statements, receipts and the year-end file all go through the <a href="../client-portal.html">client portal</a> &mdash; upload it once, and it is filed against your account rather than buried in an inbox.</p></div>

<h2>What clean books make possible</h2>
<ul>
<li><strong>Planning that is not guesswork.</strong> You cannot forecast a tax liability in October from a ledger that stops in June.</li>
<li><strong>Quarterly estimates that are close.</strong> See the <a href="../guides/estimated-taxes-and-draws.html">guide to estimated taxes and owner draws</a>.</li>
<li><strong>A borrowing conversation you can win.</strong> Lenders ask for statements in a particular shape, and the request always arrives with a deadline attached.</li>
<li><strong>A price for the business.</strong> Whatever a buyer eventually pays, they will pay less for a company whose numbers cannot be verified.</li>
</ul>

<h2>How this usually runs</h2>
<p>Most bookkeeping clients settle into a monthly rhythm: records in, reconciliation done, questions asked while the answer is still remembered. The alternative &mdash; a shoebox in February &mdash; costs more in fees, produces a worse return, and gives the owner no information during the year when it could still be acted upon.</p>
''',
         faqs=[
             ("Do I have to change accounting software to work with you?",
              "<p>Talk to us about what you already use before assuming anything has to change. The important question is whether the record is complete and reconcilable, not which product produced it.</p>"),
             ("Can you clean up books that have gone wrong?",
              "<p>Bring them in and let us look. Cleanup work is scoped after somebody has actually seen the file &mdash; the honest answer to how long it takes depends entirely on how far back the problem goes and whether the source records still exist.</p>"),
             ("How often should the books be closed?",
              "<p>Monthly, if the business has any complexity at all. A month is short enough that the person who made a transaction still remembers it, which is what makes the questions answerable.</p>"),
             ("Do I still need bookkeeping if my business is small?",
              "<p>You need a record. Whether that record is kept by you, by us, or by some combination is a cost question. What is not optional is being able to substantiate what you claim on a return.</p>"),
         ],
         related=[('services/personal-tax.html', 'Personal tax'),
                  ('services/business-tax.html', 'Small business tax'),
                  ('guides/what-your-accountant-needs.html', 'What we need from you'),
                  ('calculators/break-even.html', 'Break-even calculator')]),

    dict(slug='personal-tax', ic='calc', nav_title='Personal Tax',
         short='Planning during the year and preparation after it, for individuals and families '
               'in and around Billerica.',
         title='Personal Income Tax Planning & Preparation | Billerica, MA CPAs',
         desc='Personal income tax planning and preparation in Billerica, Massachusetts. Federal '
              'and Massachusetts returns prepared by a five-person CPA firm you can call.',
         eyebrow='Personal tax', h1='Personal tax, planned during the year and filed after it.',
         sub='Personal income tax planning and preparation &mdash; two different jobs, and only '
             'one of them can be done in April.',
         body='''
<h2>The short answer</h2>
<p>We plan and prepare personal income tax returns, federal and Massachusetts, for individuals and families. Planning happens during the year, while decisions are still reversible. Preparation happens after it, and is mostly a matter of having done the first part properly.</p>

<h2>Preparation is not planning</h2>
<p>By the time a return is on the desk, almost everything that determines the number has already happened. The stock was sold or it was not. The Roth conversion was made or it was not. The house was sold in December instead of January. The withholding was set in February and never revisited.</p>
<p>A return records those decisions. It does not improve them. The work that changes an outcome happens in the months nobody thinks about tax at all, which is why the useful question to bring to an accountant is "I am about to do this" rather than "I did this, what now?".</p>

<h2>The events that are worth a phone call first</h2>
<ul>
<li><strong>Selling property.</strong> Timing, basis, improvements you paid for years ago and forgot, and whether the principal-residence exclusion applies.</li>
<li><strong>Exercising or selling equity compensation.</strong> Options and restricted stock produce ordinary income, capital gain, and withholding that is frequently not enough.</li>
<li><strong>Retiring, or changing how you are paid.</strong> The year income stops being a paycheque is the year withholding stops working.</li>
<li><strong>A large one-off gain.</strong> Massachusetts applies an additional surtax to income above a threshold that is adjusted each year; a single large transaction can cross it.</li>
<li><strong>Inheritance, or a death in the family.</strong> There is a final return, sometimes an estate return, and a basis question that will matter for decades.</li>
<li><strong>Starting to earn on the side.</strong> Once income arrives without withholding, quarterly estimates start. See the <a href="../guides/estimated-taxes-and-draws.html">guide</a>.</li>
</ul>

<h2>Massachusetts, specifically</h2>
<p>The Massachusetts return is not a copy of the federal one. The state taxes some income differently, allows a different set of deductions and credits, and has its own rules for residency and for income earned across the New Hampshire line &mdash; which, from Billerica, is a common situation rather than an exotic one. Part-year residency and multi-state work are among the more frequent sources of an unexpected balance due.</p>

<h2>What preparation looks like here</h2>
<p>You send documents through the <a href="../client-portal.html">client portal</a> as they arrive rather than in one pile. We prepare, we ask about anything that does not reconcile, and we tell you what we found &mdash; including the things that will matter next year. Signatures happen electronically in the portal.</p>
<p>An extension is a normal event, not a failure. It extends the time to file, not the time to pay, so an extension with a payment attached is a legitimate strategy and an extension with nothing attached is a deferred problem.</p>

<div class="callout"><p><strong>Before the first meeting.</strong> The <a href="../guides/what-your-accountant-needs.html">document list</a> covers what to gather. If some of it is missing, come anyway &mdash; knowing what is absent is itself useful.</p></div>

<h2>Working with the business return</h2>
<p>If you own the company, the personal return and the entity return are one calculation. See <a href="business-tax.html">small business tax</a>.</p>
''',
         faqs=[
             ("When should I get in touch about next year?",
              "<p>Before the transaction, and at the latest before December 31. After the year closes, the set of available moves shrinks to almost nothing.</p>"),
             ("Do you prepare Massachusetts and federal returns together?",
              "<p>Yes, and other states where the facts require it &mdash; New Hampshire employment, a property elsewhere, or a part-year move.</p>"),
             ("I received a notice from the IRS. What now?",
              "<p>Send it before responding to it. Many notices are resolved with a letter and some are simply wrong, but the response window is real and short.</p>"),
             ("Can you help if I have not filed for a couple of years?",
              "<p>Call and say so plainly. Unfiled years are a solvable problem that gets worse with time; the first step is establishing what actually needs to be filed.</p>"),
             ("How do I send my documents?",
              "<p>Through the <a href=\"../client-portal.html\">client portal</a>. Upload them as they arrive rather than waiting to have everything.</p>"),
         ],
         related=[('services/business-tax.html', 'Small business tax'),
                  ('services/bookkeeping.html', 'Bookkeeping'),
                  ('guides/what-your-accountant-needs.html', 'What we need from you'),
                  ('calculators/index.html', 'Financial calculators')]),

    dict(slug='business-tax', ic='building', nav_title='Small Business Tax',
         short='The entity return and the owner\'s return are one problem. We treat them that way.',
         title='Small Business Tax Planning & Preparation | Billerica MA CPAs',
         desc='Small business tax planning and preparation in Billerica, Massachusetts. Entity '
              'returns and owner returns handled together by the same five people.',
         eyebrow='Business tax', h1='The company return and your return are one calculation.',
         sub='Small business tax planning and preparation, done alongside the books and alongside '
             'the owner&rsquo;s personal return.',
         body='''
<h2>The short answer</h2>
<p>We plan and prepare tax returns for small businesses, and for the people who own them. For a closely held company those are not two engagements. Reasonable compensation, distributions, basis, retirement contributions and the timing of income all move numbers on both returns at once, and optimising one in isolation usually costs you on the other.</p>

<h2>What planning actually consists of</h2>
<h3>How the owner is paid</h3>
<p>Salary, distribution, guaranteed payment and draw are not interchangeable words. Which one applies depends on the entity, and the mix determines employment taxes, retirement plan capacity, basis and what a lender will treat as income. It is the single most consequential recurring decision in a small company.</p>
<h3>Timing</h3>
<p>Whether a large invoice is collected in December or January, whether equipment is placed in service before year end, whether a bonus is declared &mdash; all of these shift income between years, and the right answer depends on which year has the higher marginal rate. That is knowable in advance, and only in advance.</p>
<h3>Equipment and depreciation</h3>
<p>Section 179 and bonus depreciation let a business deduct an asset far faster than it wears out. That is usually good and occasionally wrong: a full deduction in a low-income year wastes it, and a deduction taken against income you do not have does not carry the value you expected. The <a href="../calculators/section-179.html">equipment purchase calculator</a> shows what a deduction is worth against a given bracket.</p>
<h3>Entity form</h3>
<p>Sole proprietorship, partnership, LLC and S corporation each produce a different return and a different employment tax outcome from identical underlying profit. The <a href="../guides/entity-choice-small-business.html">guide to entity choice</a> sets out what actually changes.</p>
<h3>Estimated payments</h3>
<p>An owner without withholding pays quarterly. Getting the estimates roughly right avoids both an underpayment penalty and the far more common problem of a surprise in April. See the <a href="../guides/estimated-taxes-and-draws.html">guide to estimated taxes and draws</a>.</p>

<h2>Massachusetts and the border</h2>
<p>Massachusetts adds its own layer: entity-level filings that depend on how the business is classified, sales and use tax where goods or certain services are involved, and the perennial question of what happens when a Billerica business does work over the New Hampshire line. Nexus problems tend to surface late, in the form of a notice, and are much cheaper to handle before that.</p>

<div class="callout"><p><strong>Books first.</strong> Business tax work is only as good as the record underneath it. Where we also keep the <a href="bookkeeping.html">books</a>, the planning conversation in the autumn starts from figures rather than estimates.</p></div>

<h2>What we do not do</h2>
<p>This is a five-person firm doing three things well: bookkeeping, personal tax, and small business tax. If what you need sits outside that &mdash; a formal valuation for a court, a benefit plan filing, a legal opinion &mdash; the useful thing we can do is say so early and point you somewhere sensible.</p>
''',
         faqs=[
             ("Should I elect S corporation status?",
              "<p>Sometimes, and it depends on profit level, what a reasonable salary would be for the work you do, and whether you want the administration that comes with running a payroll. The <a href=\"../guides/entity-choice-small-business.html\">entity guide</a> walks through the trade-off.</p>"),
             ("When are business returns due?",
              "<p>In a normal year, partnership and S corporation returns are due in mid-March and C corporation and individual returns in mid-April, each extendable by six months. Confirm the current year's dates &mdash; they shift for weekends and holidays.</p>"),
             ("Do you do the books as well as the return?",
              "<p>For many clients, yes &mdash; see <a href=\"bookkeeping.html\">bookkeeping</a>. It removes a whole category of March archaeology.</p>"),
             ("I am about to buy equipment. Should I wait until January?",
              "<p>Ask before you buy, not after. The answer depends on which year has more income to absorb the deduction, and once the asset is placed in service the choice is made.</p>"),
             ("Can you handle both the company and my personal return?",
              "<p>Yes. For a closely held business that is the point &mdash; the two returns are the same planning problem seen from two sides.</p>"),
         ],
         related=[('services/personal-tax.html', 'Personal tax'),
                  ('services/bookkeeping.html', 'Bookkeeping'),
                  ('guides/entity-choice-small-business.html', 'Entity choice'),
                  ('calculators/section-179.html', 'Equipment purchase calculator')]),
]


def _service_page(s):
    url = BASE + 'services/' + s['slug'] + '.html'
    rel_items = [(h, l) for h, l in s['related']]
    p = dict(path='services/' + s['slug'] + '.html', depth=1, nav='services',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'],
             cta_args=CTA_TAX if 'tax' in s['slug'] else CTA_MAIN)
    others = [('services/' + o['slug'] + '.html', o['nav_title'])
              for o in SERVICES if o['slug'] != s['slug']]
    p['body'] = phero(p, [('Services', 'services/index.html'), (_plain(s['nav_title']), None)]) + sec(
        split(prose(s['body']
                    + '<h2>Common questions</h2>' + faq_html(s['faqs'])),
              call_acard()
              + portal_acard()
              + lcard('Other services', others, 1)
              + lcard('Related', rel_items, 1)))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/'),
                                      (_plain(s['nav_title']), url)]),
                   svc_schema(_plain(s['nav_title']), s['desc'], url),
                   _faq_ld(s['faqs'])]
    return p


# ================================================================= GUIDES DATA
GUIDES = [
    dict(slug='what-your-accountant-needs', ic='doc',
         nav_title='What we need from you',
         short='The document list, and why uploading it once beats emailing it four times.',
         title='What to Send Your Accountant, and How | Billerica MA CPAs',
         desc='A practical list of what a CPA firm needs to prepare your personal or business '
              'return, and why the client portal is the fastest way to send it.',
         eyebrow='Guide', h1='What to send us, and the fastest way to send it.',
         sub='Every return stalls in the same place: one missing document. This is the list, and '
             'the route that avoids the stall.',
         body='''
<h2>Start before you have everything</h2>
<p>The most common mistake is waiting. People hold their documents until the set feels complete, then send one large batch in the last week of March. That is the worst possible time to discover something is missing, because it is the week when everyone else has discovered the same thing.</p>
<p>Send documents as they arrive. Uploading a single form takes under a minute in the <a href="../client-portal.html">client portal</a>, and it means the gap in the file is visible in February rather than April.</p>

<h2>For a personal return</h2>
<h3>Income</h3>
<ul>
<li>W-2s from every employer, including one you left mid-year</li>
<li>1099-NEC and 1099-MISC for contract work</li>
<li>1099-INT, 1099-DIV and the full year-end consolidated brokerage statement &mdash; not the summary page, the whole document with the realised gain detail</li>
<li>1099-R for retirement distributions, including rollovers, which are reported even when nothing is taxable</li>
<li>1099-G for unemployment or a state refund</li>
<li>SSA-1099 for Social Security</li>
<li>K-1s from partnerships, S corporations, trusts or estates &mdash; these are often the last to arrive and the most likely to trigger an extension</li>
</ul>
<h3>Deductions, credits and adjustments</h3>
<ul>
<li>Mortgage interest (1098) and real estate tax bills actually paid during the year</li>
<li>Tuition (1098-T) plus the account statement showing what was paid and when</li>
<li>Student loan interest (1098-E)</li>
<li>Charitable receipts &mdash; cash and non-cash, with acknowledgements for anything substantial</li>
<li>Health coverage forms, including 1095-A if coverage came through a marketplace</li>
<li>Childcare provider name, address and tax ID</li>
<li>Retirement contributions made outside payroll, and HSA contributions and distributions</li>
<li>Estimated tax payments: dates and amounts, federal and Massachusetts</li>
</ul>
<h3>Things people forget</h3>
<ul>
<li>Last year's return, if this is our first year together &mdash; carryforwards live there</li>
<li>Closing statements from any property bought, sold or refinanced</li>
<li>Basis records for investments not covered by broker reporting</li>
<li>A note about anything that changed: a move, a marriage, a birth, a new state, a business started</li>
</ul>

<h2>For a business return</h2>
<ul>
<li>The year-end accounting file or a full trial balance, profit and loss, and balance sheet</li>
<li>Bank and credit card statements for December, plus reconciliations</li>
<li>Loan statements showing the year-end balance and the interest paid</li>
<li>Payroll reports for the year, including the annual reconciliation filings</li>
<li>A fixed asset list with anything bought or disposed of during the year, with invoices</li>
<li>1099s issued and received</li>
<li>The prior year return, if we did not prepare it</li>
<li>Anything unusual: a new loan, a new state, a partner added or bought out, an insurance settlement, a grant</li>
</ul>

<div class="callout"><p><strong>Upload, do not email.</strong> A document in the <a href="../client-portal.html">portal</a> is filed against your account, visible to whoever is working on your return, and out of an email inbox. Email attachments get lost in threads, and a W-2 is not something to leave sitting in one.</p></div>

<h2>What happens after you send it</h2>
<p>We work through the file and come back with questions. Questions are normal and usually specific: a deposit that does not match anything, a distribution that needs a category, a form that references a document we have not seen. Answering quickly is the single biggest thing a client controls about how fast a return gets done.</p>
<p>When the return is ready, it comes back for review and signature. Signatures happen in the portal.</p>

<h2>If something is missing</h2>
<p>Say so. A return prepared on an assumption is worse than a return that waits a week for a document, and an extension is a normal, boring event rather than a failure. What causes real problems is filing something incomplete and amending it later.</p>
''',
         faqs=[
             ("Can I just bring paper in?",
              "<p>Call the office and ask before making the trip. The portal is faster for most people, but paper is not a problem in itself.</p>"),
             ("How do I send something large, like a full accounting file?",
              "<p>Upload it to the portal. It is built for files rather than attachments, and it does not have an inbox size limit to argue with.</p>"),
             ("What if a document arrives after I have sent everything else?",
              "<p>Upload it when it turns up. Corrected 1099s in particular have a habit of arriving in March, and a corrected form after filing means an amendment.</p>"),
             ("Do I need last year's return?",
              "<p>If we did not prepare it, yes. Carryforwards, basis, depreciation schedules and elections all live in the prior return, and reconstructing them without it is slow.</p>"),
         ]),

    dict(slug='estimated-taxes-and-draws', ic='clock',
         nav_title='Estimated taxes and draws',
         short='Nobody withholds tax from a draw. Here is how the quarterly system works and how '
               'to stay out of trouble with it.',
         title='Quarterly Estimated Taxes When You Take Draws | MA CPA Guide',
         desc='How quarterly estimated tax works for owners paid in draws rather than wages, what '
              'the safe harbour rules do, and why Massachusetts needs its own payment.',
         eyebrow='Guide', h1='Quarterly estimated taxes when you pay yourself in draws.',
         sub='The moment income arrives without withholding, the timing of tax becomes your '
             'problem rather than an employer&rsquo;s.',
         body='''
<h2>What actually changes when you leave a payroll</h2>
<p>An employee never thinks about when tax is paid, because it is deducted from every paycheque and remitted for them. Someone paid in draws or contract income receives the whole amount and owes the same tax &mdash; only later, and only if they have set it aside.</p>
<p>The federal and Massachusetts systems both want tax paid as income is earned. That is what estimated payments are: four instalments across the year, replacing the withholding that used to happen automatically.</p>

<h2>The four dates</h2>
<p>In a normal year the federal instalments fall in mid-April, mid-June, mid-September, and mid-January of the following year. The periods they cover are uneven &mdash; the second instalment covers two months, not three &mdash; which surprises people every year. Massachusetts runs its own schedule alongside the federal one, and a federal payment does not satisfy the state.</p>
<p>Dates move for weekends and holidays. Confirm the current year rather than working from memory.</p>

<h2>The safe harbour is the part worth understanding</h2>
<p>You are not required to predict your income perfectly. The rules provide a safe harbour: pay in enough during the year, measured against a defined benchmark, and no underpayment penalty applies even if the final bill is much larger.</p>
<p>The usual benchmarks are a percentage of what you actually owe for the current year, or a percentage of what you owed last year &mdash; with a higher percentage of the prior year required once income passes a threshold. The prior-year route is the useful one for anyone whose income is volatile, because last year's number is already known and this year's is not.</p>
<div class="callout"><p><strong>The practical version.</strong> If your income is roughly stable, base the instalments on last year and adjust in the autumn. If you are having an unusually good year, expect the April balance to be larger than the instalments implied &mdash; the safe harbour protects you from a penalty, not from the tax.</p></div>

<h2>Self-employment tax is the part people forget</h2>
<p>Income tax is not the whole liability. Net self-employment earnings also carry Social Security and Medicare tax, which for an employee is split with an employer and for a sole proprietor is not. It is a substantial percentage on top of income tax, and it is the single most common reason a first-year owner's estimates are far too low.</p>
<p>The <a href="../calculators/self-employment-tax.html">self-employment tax calculator</a> shows the figure on its own, including the deductible half.</p>

<h2>Where the money should sit</h2>
<p>The mechanical fix that works for most owners is boring: move a fixed percentage of every deposit into a separate account on the day it arrives, and pay the instalments out of that account only. Tax money that stays in the operating account gets spent, not through carelessness but because it looks like working capital.</p>
<p>What percentage depends on the entity, the profit and the household's other income. It is worth calculating once with real numbers instead of using a figure someone mentioned.</p>

<h2>If you are already behind</h2>
<p>Pay what you can as soon as you can rather than waiting for the next quarter. Penalties accrue by period, so a late payment made in September still reduces the exposure compared with one made in January. Then get the remaining instalments right &mdash; the position improves from the moment the pattern changes.</p>

<h2>When the entity changes the answer</h2>
<p>An S corporation owner taking a reasonable salary has withholding again, which changes the estimated payment calculation substantially. See the <a href="entity-choice-small-business.html">guide to entity choice</a> and <a href="../services/business-tax.html">small business tax</a>.</p>
''',
         faqs=[
             ("What happens if I skip a quarter?",
              "<p>An underpayment penalty is calculated by period, so a missed instalment is not fatal but it is not erased by paying later either. Pay as soon as you can and correct the pattern.</p>"),
             ("Can I just pay it all in January?",
              "<p>Generally no &mdash; the penalty is computed period by period, so a single late lump sum still leaves earlier periods short. There is a narrow exception for income genuinely earned late in the year.</p>"),
             ("Does Massachusetts need a separate payment?",
              "<p>Yes. State and federal estimates are separate systems with separate payments, and paying one does not satisfy the other.</p>"),
             ("My spouse has a job with withholding. Does that help?",
              "<p>It can. Withholding is treated as paid evenly through the year regardless of when it happened, so increasing a spouse's withholding late in the year is one of the few ways to fix an earlier shortfall.</p>"),
         ]),

    dict(slug='entity-choice-small-business', ic='merge',
         nav_title='Entity choice',
         short='Sole proprietor, LLC or S corporation: what genuinely changes on the return, and '
               'what only sounds like it does.',
         title='Sole Proprietor, LLC or S Corporation | Massachusetts Tax Guide',
         desc='What actually changes on the tax return between a sole proprietorship, an LLC and '
              'an S corporation, and the Massachusetts angle worth checking before electing.',
         eyebrow='Guide', h1='Sole proprietor, LLC, or S corporation?',
         sub='The forms differ, the employment tax differs, and the administration differs. Most '
             'of the rest is folklore.',
         body='''
<h2>First, separate two questions</h2>
<p>"What entity am I?" is really two questions that people run together.</p>
<p>The first is a legal question: what did you form under state law? A sole proprietorship is nothing &mdash; it is simply a person doing business. An LLC is a state law entity that provides liability separation. A corporation is a different state law entity with its own formalities.</p>
<p>The second is a tax question: how is that entity classified for tax purposes? This is where the confusion lives, because an LLC has no tax form of its own. A single-member LLC is taxed as a sole proprietorship by default. A multi-member LLC is taxed as a partnership by default. Either can elect to be taxed as an S corporation without changing what it is legally.</p>
<div class="callout"><p><strong>So "should I be an LLC or an S corp?" is not one decision.</strong> It is a legal decision about liability and a separate tax election, and they can be made independently. Forming the entity is a legal step &mdash; that belongs with your attorney. What we can tell you is how each choice lands on the return.</p></div>

<h2>What actually changes: employment tax</h2>
<p>Take identical business profit and run it through each option.</p>
<p><strong>Sole proprietor or single-member LLC.</strong> Profit goes on a schedule attached to your personal return. All of it is subject to self-employment tax &mdash; the Social Security and Medicare component &mdash; on top of income tax. There is no payroll and no separate return.</p>
<p><strong>Partnership or multi-member LLC.</strong> The entity files its own return and issues a K-1 to each owner. Each owner's share of ordinary business income generally carries self-employment tax, and guaranteed payments do too.</p>
<p><strong>S corporation.</strong> The entity files its own return and issues a K-1. The owner must be paid a reasonable salary for the work actually performed, which runs through payroll with the usual employment taxes. Profit distributed beyond that salary is not subject to self-employment tax. That difference is the entire reason the election is popular.</p>

<h2>What the S election costs</h2>
<p>The saving is real but it is never the whole picture, and the costs are predictable:</p>
<ul>
<li><strong>Payroll has to exist.</strong> Registration, filings, deposits, year-end reconciliations. Every quarter, whether the business had a good one or not.</li>
<li><strong>"Reasonable" is not your choice alone.</strong> A salary set implausibly low to shrink employment tax is the most examined feature of small S corporations. What counts as reasonable is a facts question about the work performed, not a percentage rule.</li>
<li><strong>A second return.</strong> The entity return is an additional filing with an earlier deadline than your personal return.</li>
<li><strong>Basis matters, and it bites.</strong> Distributions in excess of basis are taxable, and losses are limited by basis. In a sole proprietorship this simply never comes up.</li>
<li><strong>Retirement plan capacity changes.</strong> Contribution limits driven by compensation behave differently when the compensation is a W-2 salary rather than net profit.</li>
</ul>
<p>Broadly, the election starts making arithmetic sense once profit is comfortably above what a reasonable salary would be, and stops making sense when the compliance cost eats the saving. Where that line falls depends on the numbers.</p>

<h2>The Massachusetts layer</h2>
<p>Massachusetts recognises the federal S election, but the state's treatment is not simply a copy of the federal one: there are state filing obligations that depend on classification, and some S corporations face an entity-level charge that a sole proprietorship never encounters. This is worth checking with actual figures before electing rather than after, because the election is not something you want to make and unwind.</p>

<h2>What does not change</h2>
<p>Choosing an entity does not change how much revenue you generate or what your costs are. It changes the wrapper. Owners occasionally reorganise expecting a transformation and get a modest employment tax difference and a new set of filings &mdash; which is a fine outcome if that was the goal, and a disappointing one if it was not.</p>

<h2>Getting to a decision</h2>
<p>The honest way to decide is arithmetic: project the profit, price a defensible salary, add the compliance cost, and compare. That is a short conversation once the books are current, and a long one when they are not. See <a href="../services/business-tax.html">small business tax</a> and <a href="../services/bookkeeping.html">bookkeeping</a>.</p>
<p><em>This guide is general information, not advice about your situation. The right answer depends on facts we would need to see.</em></p>
''',
         faqs=[
             ("Does forming an LLC lower my taxes?",
              "<p>By itself, no. A single-member LLC is taxed exactly as a sole proprietorship unless an election is made. The liability protection is real; the tax change is not automatic.</p>"),
             ("What salary is reasonable for an S corporation owner?",
              "<p>It depends on what the work would cost to hire out &mdash; the role, the hours, the industry and the region. There is no safe percentage, and a figure chosen purely to minimise employment tax is the thing most likely to be questioned.</p>"),
             ("Can I change my mind later?",
              "<p>Elections can be made and revoked, but not freely and not without consequences, including a waiting period before re-electing. Decide with figures rather than by trying it.</p>"),
             ("When during the year should I decide?",
              "<p>Before the year starts, if possible. Elections have timing rules, and a mid-year change means a split year with two sets of records.</p>"),
         ]),
]


def _guide_page(g):
    url = BASE + 'guides/' + g['slug'] + '.html'
    p = dict(path='guides/' + g['slug'] + '.html', depth=1, nav='',
             title=g['title'], desc=g['desc'], eyebrow=g['eyebrow'], h1=g['h1'], sub=g['sub'],
             cta_args=CTA_MAIN)
    others = [('guides/' + o['slug'] + '.html', o['nav_title']) for o in GUIDES if o['slug'] != g['slug']]
    p['body'] = phero(p, [(_plain(g['nav_title']), None)]) + sec(
        split(prose(g['body'] + '<h2>Common questions</h2>' + faq_html(g['faqs'])),
              portal_acard()
              + call_acard('Guides answer the general question. Your situation is specific &mdash; '
                           'call and describe it.')
              + lcard('Other guides', others, 1)
              + lcard('Services', [('services/bookkeeping.html', 'Bookkeeping'),
                                   ('services/personal-tax.html', 'Personal tax'),
                                   ('services/business-tax.html', 'Small business tax')], 1)))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), (_plain(g['nav_title']), url)]),
                   article_schema(g['h1'], g['desc'], url),
                   _faq_ld(g['faqs'])]
    return p


# ================================================================= CALCULATORS
CALC_SLUGS = ['self-employment-tax', 'section-179', 'break-even',
              'retirement-savings', 'mortgage-payment']
CALCS = [c for c in C.CALCULATORS if c['slug'] in CALC_SLUGS]
CALC_BY_SLUG = {c['slug']: c for c in C.CALCULATORS}

CALC_META = {
    'self-employment-tax': dict(
        title='Self-Employment Tax Calculator | Fitzpatrick & Goguen CPAs',
        desc='Estimate Social Security and Medicare tax on net self-employment earnings, with the '
             'deductible half broken out. Runs on this page, no third-party widget.',
        why='<p>This is the number that catches first-year owners out. Income tax gets the '
            'attention; self-employment tax is the one that makes a quarterly estimate wrong by '
            'thousands. Read it alongside the <a href="../guides/estimated-taxes-and-draws.html">'
            'guide to estimated taxes and draws</a>.</p>'),
    'section-179': dict(
        title='Equipment Purchase Tax Saving Calculator | Billerica MA CPAs',
        desc='What a Section 179 or bonus depreciation deduction is worth against your bracket, '
             'and the real after-tax cost of the equipment you are considering.',
        why='<p>Useful before the purchase rather than after it. A deduction is worth your '
            'marginal rate, not the sticker price &mdash; and taken in the wrong year it is worth '
            'less than that. See <a href="../services/business-tax.html">small business tax</a>.</p>'),
    'break-even': dict(
        title='Break-Even Calculator for Small Business | Fitzpatrick & Goguen',
        desc='Work out the revenue and unit volume at which a small business stops losing money, '
             'from fixed costs, unit price and unit variable cost.',
        why='<p>The most useful number a small business can know and the one most owners have '
            'never calculated. It only works from figures you can trust, which is the argument '
            'for <a href="../services/bookkeeping.html">keeping the books current</a>.</p>'),
    'retirement-savings': dict(
        title='Retirement Savings Projection Calculator | Billerica MA CPAs',
        desc='Project what a retirement account will be worth from the current balance plus what '
             'you and an employer add each year, at an assumed rate of return.',
        why='<p>Retirement contributions are one of the few levers that reduce a current tax bill '
            'and build something at the same time. What the account is likely to be worth is the '
            'other half of that decision.</p>'),
    'mortgage-payment': dict(
        title='Monthly Mortgage Payment Calculator | Fitzpatrick & Goguen CPAs',
        desc='Principal, interest, taxes and insurance on a fixed-rate mortgage, plus total '
             'interest over the life of the loan and the loan-to-value ratio.',
        why='<p>Buying or refinancing changes a personal return &mdash; interest, property tax, '
            'points and, on a sale, basis. Worth a conversation before signing rather than after. '
            'See <a href="../services/personal-tax.html">personal tax</a>.</p>'),
}


def _calc_page(c):
    m = CALC_META[c['slug']]
    url = BASE + 'calculators/' + c['slug'] + '.html'
    p = dict(path='calculators/' + c['slug'] + '.html', depth=1, nav='calculators',
             title=m['title'], desc=m['desc'], eyebrow='Calculator',
             h1=c['title'], sub=c['blurb'], cta_args=CTA_MAIN)
    ph = phero(p, [('Calculators', 'calculators/index.html'), (c['title'], None)])
    others = [('calculators/' + o['slug'] + '.html', o['title'])
              for o in CALCS if o['slug'] != c['slug']]
    p['body'] = (
        '<style>' + C.CALC_CSS + '</style>'
        + C.calc_page_body(c, ph, rel, ARROW, 1)
        + sec(split(prose('<h2>Why this one is here</h2>' + m['why']
                          + '<h2>What it does not do</h2><p>' + c['note'] + '</p>'
                          + '<p>A calculator is a way of framing a question, not an answer to it. '
                            'The figures it produces depend entirely on the assumptions you feed '
                            'it. When the number matters, <a href="../contact.html">call the '
                            'office</a> and work through it with someone.</p>'),
                    lcard('Other calculators', others, 1)
                    + call_acard()
                    + portal_acard()), 'sec tint')
        + C.CALC_JS)
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/'),
                                      (c['title'], url)]),
                   {"@context": "https://schema.org", "@type": "WebApplication",
                    "name": c['title'], "description": _plain(c['blurb']), "url": url,
                    "applicationCategory": "FinanceApplication",
                    "operatingSystem": "Any modern web browser",
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                    "publisher": {"@id": ORG_ID}}]
    return p


# ================================================================= HOME FAQS
HOME_FAQS = [
    ("What does this firm actually do?",
     "<p>Three things: bookkeeping, personal income tax planning and preparation, and small "
     "business tax planning and preparation. That is the whole list, and keeping it short is "
     "deliberate. If what you need sits outside it, the useful thing we can do is tell you early "
     "rather than late.</p>"),
    ("How do I get my documents to you?",
     "<p>Through the <a href=\"client-portal.html\">client portal</a>. Upload statements, forms "
     "and files as they arrive, sign electronically, message the office and settle invoices in "
     "the same place. It is faster than email and considerably safer than an envelope.</p>"),
    ("Will I deal with the same people each year?",
     "<p>The firm is five people, all of them named on <a href=\"team/index.html\">this site</a>. "
     "Dana Reardon and Sean Malone have both been here since 2000. In a practice this size the "
     "person looking at your file is someone you can name and reach.</p>"),
    ("When is the right time to talk about tax?",
     "<p>Before the thing happens. Selling property, exercising options, buying equipment, "
     "changing how you pay yourself, starting to earn on the side &mdash; all of those have a "
     "better and a worse version, and the choice closes on 31 December.</p>"),
    ("Do you work with people outside Billerica?",
     "<p>The office is on Concord Road and much of the work is local to this part of Middlesex "
     "County &mdash; Billerica, Chelmsford, Tewksbury, Burlington, Wilmington, Bedford and Lowell. "
     "Geography matters less than it did: documents go through the portal and most conversations "
     "happen by phone.</p>"),
    ("What is the firm's connection to Brian D. Goguen, P.C.?",
     "<p>Same practice, earlier name. The web address, the client portal and some older listings "
     "still carry it, so if you arrive somewhere that says Brian D. Goguen, P.C. you are in the "
     "right place.</p>"),
]


# ================================================================= PAGES
def pages():
    _write_assets()
    P = []

    # ------------------------------------------------------------------ HOME
    svc_cards = ''.join([
        _card(0, 'services/bookkeeping.html', 'ledger', 'Bookkeeping',
              'Books kept through the year by the same people who prepare the return at the end '
              'of it. No March archaeology.', '01'),
        _card(0, 'services/personal-tax.html', 'calc', 'Personal Income Tax',
              'Planning while the decisions are still reversible, preparation once they are not. '
              'Federal and Massachusetts.', '02'),
        _card(0, 'services/business-tax.html', 'building', 'Small Business Tax',
              'The company return and the owner&rsquo;s return treated as the single calculation '
              'they actually are.', '03'),
    ])
    team_preview = ''.join(
        '<a class="tcard reveal" href="team/' + t['slug'] + '.html"><div class="tava">'
        + t['initials'] + '</div><h3>' + t['name'] + '</h3><div class="cred">' + t['meta']
        + '</div><p>' + t['card'] + '</p></a>' for t in TEAM[:3])
    calc_cards = ''.join([
        _card(0, 'calculators/self-employment-tax.html', 'calc', 'Self-employment tax',
              'The figure that makes a first-year owner&rsquo;s quarterly estimate wrong. '
              'Including the deductible half.'),
        _card(0, 'calculators/section-179.html', 'building', 'Equipment purchase',
              'What a Section 179 deduction is worth against your bracket, and the real after-tax '
              'cost of the asset.'),
        _card(0, 'calculators/break-even.html', 'chart', 'Break-even point',
              'The revenue and unit volume at which the business stops losing money.'),
    ])

    body = (
        '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" '
        'aria-hidden="true">' + GLYPH + '</svg><div class="wrap"><div class="reveal in">'
        '<span class="eyebrow on-dark">Certified Public Accountants &middot; Billerica, Massachusetts</span>'
        '<h1>Helping you achieve your ideal life.</h1>'
        '<p class="sub">That is the line this firm leads with, and the accounting behind it is '
        'deliberately narrow: bookkeeping, personal income tax, and small business tax &mdash; '
        'handled by five people you can name.</p>'
        '<div class="acts"><a class="btn b-acc" href="tel:' + TEL + '">Call ' + PH + '</a>'
        '<a class="btn b-gh" href="' + PORTAL + '" target="_blank" rel="noopener">'
        'Client portal sign-in ' + ARROW + '</a></div>'
        '<div class="hero-trust"><span><b>Trust</b></span><span><b>Independence</b></span>'
        '<span><b>Confidentiality</b></span><span><b>Billerica</b>, Massachusetts</span></div>'
        '</div></div></section>'

        '<section class="strip"><div class="wrap reveal">'
        '<div class="cell"><div class="n">1981</div><div class="l">Brian Goguen licensed as a CPA</div></div>'
        '<div class="cell"><div class="n">2000</div><div class="l">the year two of the five joined</div></div>'
        '<div class="cell"><div class="n">Five</div><div class="l">people, every one of them named</div></div>'
        '<div class="cell"><div class="n">Portal</div><div class="l">secure documents, already live</div></div>'
        '</div></section>'

        + sec(head_blk('Three services, done properly.',
                       'A small firm can be excellent at a few things or adequate at many. This '
                       'one has chosen. Bookkeeping, personal tax and small business tax are the '
                       'work &mdash; and they are the same work, seen at three points in the year.',
                       'What we do')
              + '<div class="cards">' + svc_cards + '</div>'
              + '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">'
                'More on each ' + ARROW + '</a></p>')

        + sec(head_blk('Everything you send us goes through the client portal.',
                       'Documents, signatures, messages and invoices in one secure place, on a '
                       'phone or a computer. If you are already a client you already have an '
                       'account &mdash; the link below opens the sign-in page.',
                       'Already a client', ondark=True)
              + '<div class="acts"><a class="btn b-acc" href="' + PORTAL + '" target="_blank" '
                'rel="noopener">Sign in to the client portal ' + ARROW + '</a>'
                '<a class="btn b-gh" href="client-portal.html">What you can do in there</a></div>',
              'sec dark')

        + sec(split(prose(
            '<h2>Trust. Independence. Confidentiality.</h2>'
            '<p>Those are the three principles this firm states, and they are the right three for '
            'the work. You are handing over the complete picture of your finances &mdash; what you '
            'earn, what you owe, what you are worried about &mdash; to people who will still be '
            'holding it next year.</p>'
            '<h3>The tenure is the point</h3>'
            '<p>Brian Goguen has held a Massachusetts CPA licence since 1981. Dana Reardon and '
            'Sean Malone both joined in 2000. Public accounting has high turnover and small '
            'clients feel it most, because the staff member who learned the business leaves and '
            'the file starts again. That has not been the pattern here.</p>'
            '<h3>Two names, one practice</h3>'
            '<p>The firm practises as Fitzpatrick &amp; Goguen CPAs P.C. Thomas L. Fitzpatrick IV '
            'is President and a shareholder, a CPA and an IRS Enrolled Agent with an MBA from '
            'Bowling Green State University. Brian D. Goguen holds a Master of Science in Taxation '
            'from Bentley College. The practice was previously known as Brian D. Goguen, P.C., and '
            'the web address and portal still carry that name.</p>'
            '<h3>What we do not do</h3>'
            '<p>Three services is the whole list. There is no benefit in a five-person firm '
            'claiming a menu it cannot staff, and there is real value in being told early that a '
            'question belongs somewhere else. <a href="about.html">More about the firm</a>.</p>')
            , call_acard() + portal_acard()
            + lcard('The firm', [('about.html', 'About the firm'),
                                 ('team/index.html', 'The five people'),
                                 ('faq.html', 'Common questions'),
                                 ('contact.html', 'Contact')], 0)), 'sec tint')

        + sec(head_blk('Five people. Two of them since 2000.',
                       'Everyone who works here is listed, with their education and their '
                       'credentials exactly as they hold them.', 'The people')
              + '<div class="tgrid">' + team_preview + '</div>'
              + '<p style="margin-top:32px"><a class="btn b-ln" href="team/index.html">'
                'Meet all five ' + ARROW + '</a></p>')

        + sec(head_blk('Run the numbers before the conversation.',
                       'Five calculators that run on this page &mdash; no third-party widget, no '
                       'redirect to somebody else&rsquo;s site, nothing sent anywhere.',
                       'Calculators')
              + '<div class="cards">' + calc_cards + '</div>'
              + '<p style="margin-top:32px"><a class="btn b-ln" href="calculators/index.html">'
                'All calculators ' + ARROW + '</a></p>', 'sec tint')

        + sec(head_blk('Concord Road, Billerica.',
                       'One office, five people, and a phone that is answered by somebody who '
                       'works here.', 'Where we are')
              + split('<div>' + gmap('164 Concord Road, Billerica, Massachusetts 01821.') + '</div>',
                      acard('Billerica',
                            '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state']
                            + ' ' + FIRM['zip'] + '</p><p>Telephone ' + PH + '<br>Facsimile '
                            + FIRM['fax'] + '<br>' + EMAIL + '</p>', 'tel:' + TEL, 'Call ' + PH)
                      + lcard('Getting in touch',
                              [(FIRM['maps'], 'Open in Google Maps', True),
                               ('mailto:' + EMAIL, EMAIL, True),
                               (PORTAL, 'Client portal sign-in', True),
                               ('contact.html', 'Contact page')], 0)))

        + sec(head_blk('Answers before you call.', None, 'Common questions')
              + faq_html(HOME_FAQS)
              + '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">'
                'More questions answered ' + ARROW + '</a></p>', 'sec tint')
    )
    P.append(dict(
        path='index.html', depth=0, nav='home',
        title='Fitzpatrick & Goguen CPAs P.C. | CPAs in Billerica, Massachusetts',
        desc='Certified Public Accountants in Billerica, Massachusetts. Bookkeeping, personal '
             'income tax, and small business tax planning and preparation. Call (978) 667-4595.',
        body=body, cta_args=CTA_MAIN,
        schema=[org_schema(),
                {"@context": "https://schema.org", "@type": "WebSite", "name": FIRM['name'],
                 "url": BASE, "publisher": {"@id": ORG_ID}},
                _faq_ld(HOME_FAQS)]))

    # ------------------------------------------------------------------ ABOUT
    p = dict(path='about.html', depth=0, nav='about',
             title='About the Firm | Fitzpatrick & Goguen CPAs P.C., Billerica MA',
             desc='Fitzpatrick & Goguen CPAs P.C. is a five-person Billerica accounting practice, '
                  'formerly Brian D. Goguen, P.C. Trust, independence, confidentiality.',
             eyebrow='About the firm',
             h1='A five-person practice on Concord Road.',
             sub='Fitzpatrick &amp; Goguen CPAs P.C. does three things, and everyone who does them '
                 'is named on this site.',
             cta_args=CTA_MAIN)
    p['body'] = phero(p, [('About the firm', None)]) + sec(split(prose(
        '<p>This is a small practice in Billerica, Massachusetts, and almost everything worth '
        'knowing about it follows from that. Five people. One office. Three services. A client '
        'base of individuals and the small businesses they run, mostly within a short drive of '
        'Concord Road.</p>'
        '<h2>The name, and the name before it</h2>'
        '<p>The firm practises as Fitzpatrick &amp; Goguen CPAs P.C. It was previously known as '
        'Brian D. Goguen, P.C., and that earlier name is still attached to the web address, to the '
        'client portal, and to a number of older listings. If you land on a sign-in page or a '
        'directory entry carrying it, you are in the right place.</p>'
        '<p>Brian D. Goguen has been a licensed Certified Public Accountant since 1981. He holds a '
        'Master of Science in Taxation from Bentley College and a Master of Business '
        'Administration from Suffolk University, and did his undergraduate accounting work at the '
        'University of Massachusetts Lowell.</p>'
        '<p>Thomas L. Fitzpatrick IV is President and a shareholder. He holds a Massachusetts CPA '
        'licence issued in May 2022 and has been an IRS Enrolled Agent since 2017, which means he '
        'is admitted to practise before the Internal Revenue Service on a client&rsquo;s behalf. '
        'His MBA is from Bowling Green State University.</p>'
        '<h2>Trust. Independence. Confidentiality.</h2>'
        '<p>Three words the firm states as its principles. They are not decoration. Confidentiality '
        'in particular is a professional obligation rather than a policy &mdash; the information a '
        'client hands over is the most complete picture of their finances that exists anywhere, '
        'and it stays inside the practice.</p>'
        '<h2>What the tenure means</h2>'
        '<p>Dana Reardon and Sean Malone both joined in 2000. Monirina Kim joined in 2022 and runs '
        'firm administration. Two people at twenty-six years is not a marketing statistic; it is '
        'the reason a client does not have to re-explain their business every spring. '
        'Carryforwards, basis, depreciation schedules and the reason a particular account exists '
        'at all live in the file and in the memory of the people who built it.</p>'
        '<h2>What we do, and what we do not</h2>'
        '<p>Bookkeeping. Personal income tax planning and preparation. Small business tax planning '
        'and preparation. That is the list.</p>'
        '<p>Two of the five &mdash; Thomas Fitzpatrick and Brian Goguen &mdash; are also Investment '
        'Advisor Representatives with North Atlantic Investment Partners, LLC. That is a role held '
        'in that firm. This site describes accounting and tax services only.</p>'
        '<p>Where a question sits outside the three services, saying so early is more useful than '
        'taking the engagement. That is easier for a firm this size to do, because there is no '
        'utilisation target arguing with it.</p>'
        '<h2>How the work gets to us</h2>'
        '<p>Documents, signatures, messages and invoices run through the '
        '<a href="client-portal.html">client portal</a>. It is live, it is branded, and it works '
        'on a phone. Uploading a form as it arrives is a one-minute job and removes the March '
        'scramble almost entirely.</p>'
        '<h2>Where to go next</h2>'
        '<p>The <a href="services/index.html">services pages</a> cover each of the three in detail. '
        'The <a href="team/index.html">team pages</a> list every person&rsquo;s education and '
        'credentials exactly as they hold them. The <a href="faq.html">questions page</a> answers '
        'what people usually ask before calling.</p>'),
        acard('Firm at a glance',
              '<p><strong style="color:#fff">Office</strong><br>' + FIRM['addr'] + '<br>'
              + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
              '<p><strong style="color:#fff">People</strong><br>Five, all named on this site</p>'
              '<p><strong style="color:#fff">Services</strong><br>Bookkeeping &middot; personal tax '
              '&middot; small business tax</p>'
              '<p><strong style="color:#fff">Principles</strong><br>Trust &middot; independence '
              '&middot; confidentiality</p>', 'contact.html', 'Contact the firm')
        + portal_acard()
        + lcard('Firm pages', [('team/index.html', 'The five people'),
                               ('services/index.html', 'All services'),
                               ('client-portal.html', 'Client portal'),
                               ('faq.html', 'Common questions')], 0)))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('About the firm', BASE + 'about.html')])]
    P.append(p)

    # ------------------------------------------------------------ CLIENT PORTAL
    portal_faqs = [
        ("I am an existing client. Do I already have an account?",
         "<p>Almost certainly. The portal is where documents, signatures and invoices are handled, "
         "so if you have signed a return electronically or been sent a request for documents, an "
         "account exists. Use the sign-in link and the email address the office has for you.</p>"),
        ("I have forgotten my password.",
         "<p>Use the password reset link on the sign-in page. If the reset email does not arrive, "
         "check that you are using the address the office holds for you, then call " + PH + ".</p>"),
        ("I am new. How do I get access?",
         "<p>Access is issued by the office rather than by signing yourself up. Call " + PH
         + " or email <a href=\"mailto:" + EMAIL + "\">" + EMAIL + "</a> and ask for a portal "
         "invitation.</p>"),
        ("Why not just email my documents?",
         "<p>Because a tax document sitting in an email thread is both hard to find and hard to "
         "protect. A portal upload is filed against your account, is visible to whoever is working "
         "on your return, and does not have to survive an inbox.</p>"),
        ("Can I use it on my phone?",
         "<p>Yes. It works in a browser on a phone as well as on a computer, which matters when the "
         "document you need to send is a photograph of something on your kitchen table.</p>"),
        ("Can I pay an invoice through it?",
         "<p>Invoices are handled inside the portal. If you cannot see what you are expecting, call "
         "the office rather than guessing.</p>"),
        ("What runs the portal?",
         "<p>TaxDome. The account, the branding and the sign-in page all belong to the firm.</p>"),
    ]
    p = dict(path='client-portal.html', depth=0, nav='portal',
             title='Client Portal | Fitzpatrick & Goguen CPAs P.C., Billerica MA',
             desc='Sign in to the Fitzpatrick & Goguen secure client portal to send documents, '
                  'sign electronically, message the office and handle invoices.',
             eyebrow='Client portal',
             h1='One secure place for documents, signatures and invoices.',
             sub='The firm runs a client portal. It is live, it is branded, and it is the fastest '
                 'route for anything you need to get to us.',
             cta_args=CTA_PORTAL)
    p['body'] = phero(p, [('Client portal', None)]) + sec(split(prose(
        '<p><a class="btn b-acc" href="' + PORTAL + '" target="_blank" rel="noopener">'
        'Sign in to the client portal ' + ARROW + '</a></p>'
        '<h2>What it is for</h2>'
        '<p>Accounting work is a document exchange with a conversation attached. Historically that '
        'meant envelopes, then it meant email attachments, and both were bad in different ways: '
        'one was slow, the other was insecure and impossible to search. The portal replaces both.</p>'
        '<h3>Sending documents</h3>'
        '<p>Upload W-2s, 1099s, brokerage statements, closing statements, accounting files &mdash; '
        'anything, in whatever form you have it, including a photograph taken on a phone. Each '
        'upload is filed against your account rather than landing in an inbox. Send things as they '
        'arrive; there is no benefit to waiting until the set feels complete.</p>'
        '<h3>Signing</h3>'
        '<p>Returns and engagement paperwork are signed electronically. No printing, no scanning, '
        'no wondering whether the fax went through.</p>'
        '<h3>Messages</h3>'
        '<p>Questions about a specific document are best asked next to that document. A message in '
        'the portal stays attached to your file rather than disappearing into a thread.</p>'
        '<h3>Invoices</h3>'
        '<p>Billing is handled inside the portal.</p>'
        '<div class="callout"><p><strong>What you see depends on your engagement.</strong> The '
        'portal shows what the office has set up for your account, so not every client sees every '
        'feature. If something you expect is not there, call ' + PH + '.</p></div>'
        '<h2>Why the address says bgoguen</h2>'
        '<p>The practice was previously known as Brian D. Goguen, P.C., and the portal address '
        'still carries that name. It is the same firm. If a sign-in page or an email refers to '
        'Brian D. Goguen, P.C., you are in the right place.</p>'
        '<h2>Getting the most out of it</h2>'
        '<ul>'
        '<li><strong>Upload early and often.</strong> One document at a time is fine and takes '
        'under a minute.</li>'
        '<li><strong>Name things plainly.</strong> A file called "2025 W-2 Acme" saves a question.</li>'
        '<li><strong>Answer questions in the portal.</strong> The answer then lives with the file '
        'it relates to.</li>'
        '<li><strong>Check what is outstanding.</strong> Most delays are one missing form, and it '
        'is usually visible before anyone has to chase it.</li>'
        '</ul>'
        '<h2>If you cannot get in</h2>'
        '<p>Use the password reset on the sign-in page first. If that does not work, call '
        '<a href="tel:' + TEL + '">' + PH + '</a> or email '
        '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a> and somebody will sort it out. Do not '
        'email sensitive documents while you wait &mdash; call instead.</p>'
        '<h2>Common questions</h2>' + faq_html(portal_faqs)),
        portal_acard()
        + call_acard('If the portal is not cooperating, the phone still works.')
        + lcard('Related', [('guides/what-your-accountant-needs.html', 'What to send us'),
                            ('services/personal-tax.html', 'Personal tax'),
                            ('services/business-tax.html', 'Small business tax'),
                            ('contact.html', 'Contact the office')], 0)))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Client portal', BASE + 'client-portal.html')]),
                   _faq_ld(portal_faqs)]
    P.append(p)

    # ------------------------------------------------------------------ FAQ
    FAQS = HOME_FAQS + [
        ("What is the difference between a CPA, an accountant and an enrolled agent?",
         "<p>Anyone may call themselves an accountant. A Certified Public Accountant has passed the "
         "Uniform CPA Examination and holds an active state licence &mdash; in this firm's case, "
         "from the Commonwealth of Massachusetts. An Enrolled Agent is licensed federally by the "
         "IRS and is admitted to represent taxpayers before the Service in examinations, "
         "collections and appeals.</p>"
         "<p>Thomas L. Fitzpatrick IV holds both a Massachusetts CPA licence and the EA "
         "designation. Brian D. Goguen has been a licensed CPA since 1981 and holds a Master of "
         "Science in Taxation.</p>"),
        ("How much does this cost?",
         "<p>It depends on the work, which is not an evasion &mdash; a straightforward personal "
         "return and a business with three entities and a year of unreconciled books are not "
         "comparable. Call, describe the situation, and you will get a straight answer about what "
         "the work involves.</p>"),
        ("What should I have ready for a first conversation?",
         "<p>Last year's return, a rough description of what changed, and anything with a deadline "
         "attached &mdash; a notice, a loan application, a letter of intent. The "
         "<a href=\"guides/what-your-accountant-needs.html\">document guide</a> has the full "
         "list. If you do not have all of it, call anyway.</p>"),
        ("Do you keep books as well as prepare returns?",
         "<p>Yes &mdash; <a href=\"services/bookkeeping.html\">bookkeeping</a> is one of the three "
         "services. Where the same practice does both, the return is an outcome of a year that was "
         "already understood rather than a reconstruction of one that was not.</p>"),
        ("I have not filed for a year or two. Is that a problem you handle?",
         "<p>Call and say so plainly. Unfiled years are solvable and they get worse with delay. The "
         "first step is working out what actually needs to be filed, which is often less alarming "
         "than people expect.</p>"),
        ("Can you represent me if the IRS examines my return?",
         "<p>An IRS Enrolled Agent is admitted to practise before the Internal Revenue Service and "
         "may represent a taxpayer in examinations, collections and appeals. "
         "<a href=\"team/thomas-l-fitzpatrick.html\">Thomas L. Fitzpatrick IV</a> holds that "
         "designation. Send the notice before responding to it.</p>"),
        ("Do you handle Massachusetts and federal returns?",
         "<p>Yes, and other states where the facts require one &mdash; New Hampshire employment, a "
         "property elsewhere, or a part-year move. From Billerica, the New Hampshire line comes up "
         "regularly.</p>"),
        ("Are the calculators on this site sending my numbers anywhere?",
         "<p>No. They run entirely in your browser on this page. Nothing is transmitted, stored or "
         "logged, and there is no third-party widget involved.</p>"),
        ("Is my information confidential?",
         "<p>Yes. Confidentiality is one of the three principles the firm states, and for a CPA it "
         "is a professional obligation rather than a policy choice.</p>"),
    ]
    p = dict(path='faq.html', depth=0, nav='about',
             title='Common Questions | Fitzpatrick & Goguen CPAs P.C., Billerica',
             desc='Straight answers about fees, credentials, the client portal, Massachusetts '
                  'returns, unfiled years and how a five-person CPA firm in Billerica works.',
             eyebrow='Answers', h1='Questions people ask before they call.',
             sub='If yours is not here, call ' + PH + ' and ask. Nobody will route you to a form.',
             cta_args=CTA_MAIN)
    p['body'] = phero(p, [('Common questions', None)]) + sec(
        head_blk('About working with the firm',
                 'Fees, credentials, the portal, and what happens first.')
        + faq_html(FAQS)
        + '<div class="sec-head reveal" style="margin-top:56px"><h2>Longer answers</h2>'
          '<p class="lead">Three guides cover the questions that need more than a paragraph: '
          '<a href="guides/what-your-accountant-needs.html">what to send us and how</a>, '
          '<a href="guides/estimated-taxes-and-draws.html">quarterly estimated taxes when you take '
          'draws</a>, and <a href="guides/entity-choice-small-business.html">sole proprietor, LLC '
          'or S corporation</a>.</p></div>')
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Common questions', BASE + 'faq.html')]),
                   _faq_ld(FAQS)]
    P.append(p)

    # ------------------------------------------------------------------ CONTACT
    p = dict(path='contact.html', depth=0, nav='contact',
             title='Contact | Fitzpatrick & Goguen CPAs P.C., Billerica, MA',
             desc='Reach Fitzpatrick & Goguen CPAs P.C. at 164 Concord Road, Billerica, MA. '
                  'Telephone (978) 667-4595, fax (978) 667-4597, office@bgoguen.com.',
             eyebrow='Contact', h1='Call the office. Somebody who works here will answer.',
             sub='Tell us what you are dealing with and we will tell you whether this is the right '
                 'firm for it.',
             cta_args=CTA_MAIN)
    p['body'] = phero(p, [('Contact', None)]) + sec(
        head_blk('164 Concord Road, Billerica',
                 'One office, five people, and a client portal for everything that does not need '
                 'a phone call.')
        + split('<div>' + gmap('Pan, zoom, or open the map full screen for directions.') + '</div>',
                acard('Office',
                      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' '
                      + FIRM['zip'] + '</p>'
                      '<p>Telephone ' + PH + '<br>Facsimile ' + FIRM['fax'] + '<br>' + EMAIL + '</p>',
                      'tel:' + TEL, 'Call ' + PH)
                + portal_acard()
                + lcard('Quick links', [(FIRM['maps'], 'Directions in Google Maps', True),
                                        ('mailto:' + EMAIL, EMAIL, True),
                                        ('guides/what-your-accountant-needs.html', 'What to send us'),
                                        ('faq.html', 'Common questions')], 0))) + sec(split(prose(
        '<h2>What happens on a first call</h2>'
        '<p>You speak to somebody who works at the firm. The first conversation is usually short: '
        'what kind of return, roughly what the year looked like, and what deadline is driving the '
        'question. From that it is normally clear whether the work is bookkeeping, personal tax, '
        'business tax, or some combination of the three.</p>'
        '<p>If it belongs somewhere else, we will say so and point you in a useful direction. A '
        'five-person firm has no incentive to take an engagement it should not.</p>'
        '<h2>What to have handy</h2>'
        '<ul>'
        '<li>Last year&rsquo;s return, if we did not prepare it</li>'
        '<li>For a business, the most recent financial statements in whatever form they exist</li>'
        '<li>Anything with a date on it &mdash; an IRS or Massachusetts notice, a loan application, '
        'a letter of intent</li>'
        '<li>A short description of what changed this year</li>'
        '</ul>'
        '<p>Missing pieces are not a problem. Knowing what is missing is itself useful.</p>'
        '<h2>Sending documents</h2>'
        '<p>Use the <a href="client-portal.html">client portal</a> rather than email. It is faster, '
        'it keeps tax documents out of an inbox, and everything lands filed against your account. '
        'If you do not have access yet, call and ask for an invitation.</p>'
        '<h2>Office hours</h2>'
        '<p>Call ' + PH + ' or email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a> to arrange a '
        'time. Filing season and the rest of the year run at different rhythms, so it is worth '
        'checking rather than assuming.</p>'
        '<h2>Confidentiality</h2>'
        '<p>Client information is confidential, including the fact that you called. For a CPA that '
        'is a professional obligation rather than a policy.</p>'),
        call_acard()
        + lcard('The people', [('team/thomas-l-fitzpatrick.html', 'Thomas L. Fitzpatrick IV'),
                              ('team/brian-d-goguen.html', 'Brian D. Goguen'),
                              ('team/index.html', 'The full team')], 0)))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Contact', BASE + 'contact.html')]),
                   {"@context": "https://schema.org", "@type": "ContactPage",
                    "name": "Contact " + FIRM['name'], "url": BASE + 'contact.html'}]
    P.append(p)

    # ------------------------------------------------------------ SERVICES HUB
    cards = ''.join(_card(1, 'services/' + s['slug'] + '.html', s['ic'], s['nav_title'],
                          s['short'], '0' + str(i + 1))
                    for i, s in enumerate(SERVICES))
    p = dict(path='services/index.html', depth=1, nav='services',
             title='Services | Fitzpatrick & Goguen CPAs P.C., Billerica, MA',
             desc='Bookkeeping, personal income tax planning and preparation, and small business '
                  'tax planning and preparation from a five-person Billerica CPA firm.',
             eyebrow='Services', h1='Three services, and they are the same year seen three times.',
             sub='Bookkeeping records it, business tax reports it, personal tax is where the owner '
                 'feels it. Splitting them across three firms is how detail gets lost.',
             cta_args=CTA_MAIN)
    p['body'] = phero(p, [('Services', None)]) + sec(
        head_blk('What the firm does', 'Each of these is a full page. There is no fourth.')
        + '<div class="cards">' + cards + '</div>') + sec(split(prose(
        '<h2>Why the list is short</h2>'
        '<p>A five-person practice can be genuinely good at a few things or thinly adequate at '
        'many. The published list is bookkeeping, personal income tax planning and preparation, '
        'and small business tax planning and preparation &mdash; and that is what the firm does.</p>'
        '<p>The advantage is not modesty. It is that the same people see the whole year. When the '
        'practice that records a transaction in March is the practice that reports it the '
        'following February, nothing has to be reconstructed and nobody has to guess what a '
        'deposit was.</p>'
        '<h2>How the three connect</h2>'
        '<p><a href="bookkeeping.html">Bookkeeping</a> produces the record. Without it, tax work is '
        'archaeology and planning is guesswork.</p>'
        '<p><a href="business-tax.html">Small business tax</a> turns that record into a return, and '
        '&mdash; more importantly &mdash; into decisions made before the year closes: how the owner '
        'is paid, when equipment is bought, whether an election makes sense.</p>'
        '<p><a href="personal-tax.html">Personal tax</a> is where a closely held business actually '
        'lands. Distributions, basis, retirement contributions and the household&rsquo;s other '
        'income all interact, and optimising the entity return in isolation regularly makes the '
        'personal one worse.</p>'
        '<h2>What sits outside</h2>'
        '<p>Formal business valuations for litigation, benefit plan filings, legal opinions, and '
        'anything requiring an attest report are outside what this firm offers. Saying so early is '
        'more useful than taking the engagement and learning it later.</p>'
        '<h2>Getting documents to us</h2>'
        '<p>Whatever the service, the mechanics are the same: everything goes through the '
        '<a href="../client-portal.html">client portal</a>.</p>'),
        call_acard() + portal_acard()
        + lcard('Guides', [('guides/what-your-accountant-needs.html', 'What to send us'),
                           ('guides/estimated-taxes-and-draws.html', 'Estimated taxes and draws'),
                           ('guides/entity-choice-small-business.html', 'Entity choice'),
                           ('calculators/index.html', 'Financial calculators')], 1)), 'sec tint')
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/')]),
                   {"@context": "https://schema.org", "@type": "ItemList",
                    "name": "Services", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": _plain(s['nav_title']),
                         "url": BASE + 'services/' + s['slug'] + '.html'}
                        for i, s in enumerate(SERVICES)]}]
    P.append(p)
    for s in SERVICES:
        P.append(_service_page(s))

    # ---------------------------------------------------------------- TEAM HUB
    tcards = ''.join(
        '<a class="tcard reveal" href="' + t['slug'] + '.html"><div class="tava">' + t['initials']
        + '</div><h3>' + t['name'] + '</h3><div class="cred">' + t['meta'] + '</div><p>'
        + t['card'] + '</p></a>' for t in TEAM)
    p = dict(path='team/index.html', depth=1, nav='team',
             title='Our Team | Fitzpatrick & Goguen CPAs P.C., Billerica, MA',
             desc='The five people at Fitzpatrick & Goguen CPAs P.C. in Billerica, Massachusetts, '
                  'with their education and credentials exactly as they hold them.',
             eyebrow='The people', h1='Five people, and you can have any of their names.',
             sub='Education and credentials, listed as held. Where somebody holds no professional '
                 'designation, none is invented for them.',
             cta_args=CTA_MAIN)
    p['body'] = phero(p, [('Our team', None)]) + sec(
        head_blk('The whole firm',
                 'Two shareholders, two accountants who joined in 2000, and firm administration.')
        + '<div class="tgrid">' + tcards + '</div>') + sec(split(prose(
        '<h2>Why a firm this size works</h2>'
        '<p>Five people cannot cover everything, and this one does not try. What it can do is '
        'something a larger firm structurally cannot: the person who takes your call is a person '
        'who has seen your file.</p>'
        '<p>There is no account management layer, no annual rotation, and no re-education of a new '
        'junior on how your business works. Dana Reardon and Sean Malone have both been here since '
        '2000, which means a client who arrived in the early 2000s has had the same accountants '
        'for their entire relationship with the firm.</p>'
        '<h2>Credentials, stated exactly</h2>'
        '<ul>'
        '<li><a href="thomas-l-fitzpatrick.html">Thomas L. Fitzpatrick IV</a> &mdash; MBA, IRS '
        'Enrolled Agent (2017), Massachusetts CPA licence (May 2022), Series 65 (January 2020)</li>'
        '<li><a href="brian-d-goguen.html">Brian D. Goguen</a> &mdash; Certified Public Accountant '
        'since 1981, MST (Bentley College), MBA (Suffolk University)</li>'
        '<li><a href="dana-reardon.html">Dana Reardon</a> &mdash; accounting, Bentley College; with '
        'the firm since 2000</li>'
        '<li><a href="sean-malone.html">Sean Malone</a> &mdash; accounting, University of '
        'Massachusetts Lowell; with the firm since 2000</li>'
        '<li><a href="monirina-kim.html">Monirina Kim</a> &mdash; BS Business Administration, '
        'Southern New Hampshire University; firm administration since 2022</li>'
        '</ul>'
        '<h2>Outside the practice</h2>'
        '<p>Thomas Fitzpatrick sits on the boards of the Massachusetts Association of Accountants '
        'and the Boys &amp; Girls Club of Greater Billerica. Brian Goguen sits on the board of the '
        'Boys &amp; Girls Club of Billerica.</p>'
        '<p>Both are also Investment Advisor Representatives with North Atlantic Investment '
        'Partners, LLC &mdash; a role held in that firm. This site describes accounting and tax '
        'services only.</p>'
        '<p><a class="btn b-ln" href="../about.html">More about the firm ' + ARROW + '</a></p>'),
        call_acard() + portal_acard()
        + lcard('Firm pages', [('about.html', 'About the firm'),
                               ('services/index.html', 'All services'),
                               ('faq.html', 'Common questions'),
                               ('contact.html', 'Contact')], 1)), 'sec tint')
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Our team', BASE + 'team/')]),
                   {"@context": "https://schema.org", "@type": "ItemList",
                    "name": "Professionals", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": t['name'],
                         "url": BASE + 'team/' + t['slug'] + '.html'}
                        for i, t in enumerate(TEAM)]}]
    P.append(p)
    for t in TEAM:
        P.append(_bio(t))

    # -------------------------------------------------------------- GUIDES
    for g in GUIDES:
        P.append(_guide_page(g))

    # ---------------------------------------------------------- CALCULATOR HUB
    groups = []
    for cat in C.CATEGORIES:
        items = [c for c in CALCS if c['cat'] == cat]
        if items:
            groups.append((cat, items))
    grid = ''
    for cat, items in groups:
        grid += ('<div class="sec-head reveal" style="margin:44px 0 0"><h2>'
                 + html.escape(cat) + '</h2></div><div class="calcgrid">'
                 + ''.join('<a class="calccard reveal" href="' + c['slug'] + '.html">'
                           '<div class="cc">' + html.escape(c['cat']) + '</div>'
                           '<h3>' + c['title'] + '</h3><p>' + c['blurb'] + '</p></a>'
                           for c in items)
                 + '</div>')
    p = dict(path='calculators/index.html', depth=1, nav='calculators',
             title='Financial Calculators | Fitzpatrick & Goguen CPAs P.C.',
             desc='Five financial calculators that run in your browser: self-employment tax, '
                  'equipment purchase, break-even, retirement savings and mortgage payment.',
             eyebrow='Calculators', h1='Five calculators that run on this page.',
             sub='No third-party widget, no redirect to somebody else&rsquo;s site, and nothing '
                 'you type is sent anywhere.',
             cta_args=CTA_MAIN)
    p['body'] = phero(p, [('Calculators', None)]) + (
        '<style>' + C.CALC_CSS + '</style>'
        + sec(head_blk('Run the numbers first',
                       'These are here because the arithmetic is usually the quick part. Getting '
                       'the assumptions right is the conversation, and that is what the office is '
                       'for.')
              + grid)
        + sec(split(prose(
            '<h2>Why these run here</h2>'
            '<p>Most accounting websites embed calculators licensed from a vendor. The widget sits '
            'on the vendor&rsquo;s account, the click frequently leaves for a third-party site, and '
            'whatever you type goes with it.</p>'
            '<p>These do not. They are plain code on this page. There is no network call, no '
            'cookie, nothing stored and nothing transmitted. Close the tab and the numbers are '
            'gone.</p>'
            '<h2>What a calculator is good for</h2>'
            '<p>Framing a question. A break-even figure tells you what has to be true for the '
            'business to work; it does not tell you whether it will be. A Section 179 result tells '
            'you what a deduction is worth against an assumed bracket; whether this is the right '
            'year to take it is a different question.</p>'
            '<p>When the number matters, work through it with somebody. That is what '
            '<a href="../contact.html">the phone</a> is for.</p>'
            '<h2>Related reading</h2>'
            '<p><a href="../guides/estimated-taxes-and-draws.html">Quarterly estimated taxes when '
            'you take draws</a> pairs with the self-employment tax calculator. '
            '<a href="../guides/entity-choice-small-business.html">Entity choice</a> pairs with '
            'both business calculators.</p>'),
            call_acard() + portal_acard()
            + lcard('Services', [('services/bookkeeping.html', 'Bookkeeping'),
                                 ('services/personal-tax.html', 'Personal tax'),
                                 ('services/business-tax.html', 'Small business tax')], 1)),
              'sec tint'))
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/')]),
                   {"@context": "https://schema.org", "@type": "ItemList",
                    "name": "Financial calculators", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": c['title'],
                         "url": BASE + 'calculators/' + c['slug'] + '.html'}
                        for i, c in enumerate(CALCS)]}]
    P.append(p)
    for c in CALCS:
        P.append(_calc_page(c))

    return P
