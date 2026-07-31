# -*- coding: utf-8 -*-
"""
Firm profile — Thomas P. Craig, CPA, PC, trading as "Mass Tax Pros" (Wilmington, MA).

Every fact below is taken from the firm's own published material; see
research/masstaxpros.md. Deliberately absent, because the firm does not state
them: a founding year, office hours, memberships, a client portal, online
payments, and any years-of-experience figure for an individual. The only
experience figure used anywhere on this site is the firm's own
"more than 50 years of combined experience".

Joseph W. Brine is an Enrolled Agent and is NOT a CPA. The BANNED list below
mechanically enforces that, along with the other omissions.
"""

FIRM = dict(
    name='Thomas P. Craig, CPA, PC',
    short='Mass Tax Pros',
    email='info@tpc-cpa.com',
    addr='Heritage Commons, 11 Middlesex Avenue, Suite 3',
    city='Wilmington', state='MA', state_full='Massachusetts', zip='01887',
    tel='+19786575272', ph='(978) 657-5272', fax='(978) 657-7994',
    # The firm does not publish opening hours. Do not invent them.
    hours='Call the office for current hours',
    office_page=None,
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Thomas+P.+Craig%2C+CPA%2C+PC+11+Middlesex+Avenue+Suite+3+Wilmington+MA+01887'),
    # branding
    favicon_letter='M',
    brand_line='Mass Tax Pros',
    brand_sub='Tax &amp; Accounting Service Professionals',
    nav_cta='Call the Mass Tax Pros',
    topbar='Tax &amp; Accounting Service Professionals &middot; Wilmington, Massachusetts',
    footer_blurb=('Income tax, accounting, QuickBooks and financial services for businesses and '
                  'individuals, from Heritage Commons on Middlesex Avenue in Wilmington.'),
    footer_note=('Thomas P. Craig, CPA and Enrolled Agent &middot; Joseph W. Brine, Enrolled Agent '
                 '&mdash; more than 50 years of combined experience.'),
    footer_services=[
        ('services/income-tax.html', 'Income Tax Services'),
        ('services/accounting.html', 'Accounting Services'),
        ('services/quickbooks.html', 'QuickBooks Services'),
        ('services/financial-services.html', 'Financial Services'),
        ('calculators/index.html', 'Calculators'),
        ('services/index.html', 'All services &rarr;'),
    ],
    footer_firm=[
        ('about.html', 'About the practice'),
        ('team/index.html', 'Tom Craig &amp; Joe Brine'),
        ('guides/cpa-vs-enrolled-agent.html', 'CPA, EA or preparer?'),
        ('faq.html', 'Common questions'),
        ('contact.html', 'Contact &amp; directions'),
    ],
)

# Deep spruce green with a harvest-amber accent — a New England palette,
# deliberately clear of the navy/bronze used elsewhere in the portfolio.
# Verified against every pair in contrast.py's matrix; lowest margin is the
# accent button (6.63:1 against #15130e, required 4.5).
DESIGN = 'brandmark'   # see design.py

T = dict(ink='#3A2440', ink2='#533558', acc='#D09A3C', accd='#86601A',
         accrgb='208,154,60', cream='#F4F0EA')
NAV = [('services/index.html', 'Services', 'services'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('team/index.html', 'Our Team', 'team'),
       ('about.html', 'About', 'about'),
       ('contact.html', 'Contact', 'contact')]

# Logo proposal — "the filed field". Two opposed right-angle brackets crop the
# mark the way corner registration marks crop a field on a filed return, with
# the brand initials set on the diagonal between them in the site serif. Flat,
# one colour, no gradients: it holds at 20px and the brackets alone still read
# as a deliberate device when the letters go soft.
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="5" y="5" width="19" height="3.6" fill="currentColor"/>'
        '<rect x="5" y="5" width="3.6" height="19" fill="currentColor"/>'
        '<rect x="40" y="55.4" width="19" height="3.6" fill="currentColor"/>'
        '<rect x="55.4" y="40" width="3.6" height="19" fill="currentColor"/>'
        '<text x="32" y="39.5" text-anchor="middle" fill="currentColor" '
        'font-size="19" letter-spacing="1.5">MTP</text></svg>')


def pages():
    import content_masstaxpros
    return content_masstaxpros.pages()


# ---------------------------------------------------------------- QA gates
# The office publishes exactly two numbers.
ALLOWED_PHONES = ['(978) 657-5272', '(978) 657-7994']

# Firm-specific forbidden strings. Three groups:
#   1. Credential errors — Joe Brine is an Enrolled Agent, not a CPA, and the
#      firm claims no professional memberships or peer-review enrolment.
#   2. Stale figures on the firm's own live site ("approximately 15 years",
#      "a quarter century") that are 13 years out of date.
#   3. Facilities and facts the firm does not have or does not state — a portal,
#      online payments, attest work, a founding year — plus cross-contamination
#      guards against the other builds sharing this repo.
BANNED = [
    # 1. credentials
    'Brine, CPA', 'Brine CPA', 'Joe Brine, CPA', 'Joseph W. Brine, CPA',
    'Brine is a CPA', 'Brine, a CPA', 'two CPAs', 'both CPAs', 'our CPAs',
    'AICPA', 'peer review', 'peer-reviewed', 'MSCPA',
    'Massachusetts Society of Certified Public Accountants',
    'ProAdvisor', 'Certified QuickBooks',
    # 2. stale time claims
    'quarter century', 'approximately 15 years', 'practicing for approximately',
    # 3. things the firm does not state
    'client portal', 'secure portal', 'document portal',
    'pay online', 'online payment', 'make a payment', 'pay your invoice',
    'financial statement audit', 'audit and assurance', 'audit &amp; assurance',
    'we perform audits', 'review engagement', 'attest',
    'Established 19', 'Established 20', 'Est. 19', 'Est. 20',
    'founded in 19', 'founded in 20', 'in business since', 'practicing since',
    'no hidden fees', 'transparent prices', 'free consultation',
    'CalcXML', 'calcxml',
    # cross-build contamination guards
    # leading spaces: "handover" contains "andover"
    'Kolnicki', 'Downers Grove', 'Illinois', ' Lowell', ' Andover',
]
