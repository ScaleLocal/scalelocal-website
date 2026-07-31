# -*- coding: utf-8 -*-
"""
Firm profile — Charles M. Carella, CPA (North Billerica, MA).

Every fact below is taken from the firm's own published material and nothing else.
The current site names no individual, states no founding year, uses no entity
suffix, claims no memberships or specialisms, and does not publish office hours.
None of those gaps are filled in here. Where a value would normally carry a claim
(hours, founding year, staff size), it is either omitted or replaced with an
instruction rather than an assertion.

Telephone: published as "(978) 663-6419 ext. 11". The visible string keeps the
extension; the tel: URI must not. The firm's current site embeds "ext.11" inside
the tel: URI, which misdials from a mobile handset.
"""

FIRM = dict(
    name='Charles M. Carella, CPA',
    short='CMC',
    email='CMCCPA@carellacpa.com',
    addr='330 Boston Road, Suite 12',
    city='North Billerica', state='MA', state_full='Massachusetts', zip='01862',
    # E.164 only — the extension is dialled after the call connects, never inside the URI.
    tel='+19786636419',
    ph='(978) 663-6419 ext. 11',
    fax='(978) 663-7260',
    # Hours are not published by the firm. This is an instruction, not a claim.
    hours='Call or email to arrange a time',
    office_page=None,
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Charles+M.+Carella+CPA+330+Boston+Road+Suite+12+North+Billerica+MA+01862'),
    # branding
    favicon_letter='C',
    brand_line='Charles M. Carella',
    brand_sub='Certified Public Accountant',
    nav_cta='Talk to a CPA',
    topbar='Certified Public Accountant &middot; North Billerica, Massachusetts',
    footer_blurb=('A Certified Public Accountant at 330 Boston Road in North Billerica, '
                  'Massachusetts, working with individuals and small businesses.'),
    footer_note=None,
    footer_services=[
        ('services/tax-preparation-planning.html', 'Tax Preparation &amp; Planning'),
        ('services/accounting-bookkeeping.html', 'Accounting &amp; Bookkeeping'),
        ('services/financial-statements.html', 'Financial Statements'),
        ('services/business-consulting.html', 'Business Consulting'),
        ('services/index.html', 'All services &rarr;'),
    ],
    footer_firm=[
        ('about.html', 'About the practice'),
        ('about.html#engagement', 'How an engagement runs'),
        ('faq.html', 'Common questions'),
        ('calculators/index.html', 'Financial calculators'),
        ('contact.html', 'Contact the office'),
    ],
)

# Deep pine and clay. Chosen to sit well away from the navy/bronze used elsewhere in
# the engine, and verified against every foreground token the stylesheet pairs with
# --ink, --ink2, --acc, --accd and --cream (including the calculator panel, which is
# painted on the ink -> ink2 gradient).
DESIGN = 'quiet'   # see design.py

T = dict(ink='#223140', ink2='#34495D', acc='#C0783C', accd='#83461A',
         accrgb='192,120,60', cream='#F1F1ED')
NAV = [('services/index.html', 'Services', 'services'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('about.html', 'About', 'about'),
       ('faq.html', 'Questions', 'faq'),
       ('contact.html', 'Contact', 'contact')]

# ---------------------------------------------------------------------------
# LOGO — proposal, not the firm's existing mark (their current logo file is a
# 43-byte blank 1x1 pixel; there is nothing to preserve).
#
# A squared C drawn as a ledger bracket: one stem joining a head rule and a foot
# rule, with a shorter rule floating inside the counter, right-aligned to the same
# edge the arms end on — the way a total rule sits under a column of figures. It
# reads as the initial at 50px and as ruled stationery at 20px, and it rhymes with
# the engine's single-letter favicon (a C set between two rules) without repeating
# it. No text element, so nothing depends on a font loading.
# ---------------------------------------------------------------------------
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="9" y="14" width="46" height="2.8" fill="currentColor"/>'
        '<rect x="9" y="14" width="2.8" height="36" fill="currentColor"/>'
        '<rect x="9" y="47.2" width="46" height="2.8" fill="currentColor"/>'
        '<rect x="31" y="30.6" width="24" height="2.6" fill="currentColor"/>'
        '</svg>')


def pages():
    import content_carellacpa
    return content_carellacpa.pages()


# QA gates specific to this firm
ALLOWED_PHONES = ['(978) 663-6419', '(978) 663-7260']

# Everything the audit says is NOT established about this firm. These strings are
# the shapes an invented fact would take, so the harness fails the build if one
# ever creeps in from a draft, a template, or a helpful autocomplete.
BANNED = [
    # the malformed tel: URI on the current site
    'ext.11', 'tel:+19786636419,11', 'ext11',
    # founding year / longevity — the firm states none
    'founded in', 'established in 19', 'established in 20', 'since 19', 'since 20',
    'Est. 19', 'Est. 20', 'years of experience', 'decades of experience',
    'years in practice', 'for over ', 'more than 30 years', 'generations',
    # staff size / named people — the firm names nobody and gives no headcount
    'our team', 'our staff', 'sole practitioner', 'our partners', 'the partners',
    'our professionals', 'one-man', 'two-person', 'small team',
    # credentials and memberships beyond the bare 'CPA' the firm claims
    'AICPA', 'American Institute of Certified', 'Massachusetts Society of CPAs',
    'MSCPA', 'peer review', 'peer-reviewed', 'Enrolled Agent', 'CERTIFIED FINANCIAL',
    'QuickBooks ProAdvisor', 'accredited in', 'award',
    # facilities and features the firm does not have
    'portal', 'pay online', 'online payment', 'book online', 'schedule online',
    'cchwebsites', 'CalcXML',
    # specialisms the firm does not claim
    'we specialize', 'our specialty', 'niche', 'industries we serve',
]
