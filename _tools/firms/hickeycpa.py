# -*- coding: utf-8 -*-
"""
Firm profile — James L. Hickey, CPA PC (Tewksbury, Massachusetts).

Every fact below is taken from the firm's own published site (verified 2026-07-30).
The site states no founding year, no staff list, no memberships and no office hours,
and names exactly one person with no title and no bio. Nothing in that category is
asserted anywhere in this build. See the notes returned with the deliverable.
"""

FIRM = dict(
    name='James L. Hickey, CPA PC',
    short='Hickey',
    email='info@hickeycpa.com',
    addr='170 Main Street, Suite 110',
    city='Tewksbury', state='MA', state_full='Massachusetts', zip='01876',
    tel='+19788518945', ph='(978) 851-8945', fax='(978) 851-9314',
    # The site states no office hours. Nothing is invented here; the footer and the
    # contact widget carry an instruction rather than a claim.
    hours='Call or email to arrange a time',
    office_page=None,
    maps=('https://www.google.com/maps/search/?api=1&query='
          'James+L.+Hickey%2C+CPA+PC+170+Main+Street+Suite+110+Tewksbury+MA+01876'),
    # branding
    favicon_letter='H',
    brand_line='James L. Hickey, CPA',
    brand_sub='Tax, Accounting &amp; Business Consulting',
    nav_cta='Talk to a CPA',
    topbar='Tax, Accounting &amp; Business Consulting &middot; Tewksbury, Massachusetts',
    footer_blurb=('A full service tax, accounting and business consulting firm on Main Street '
                  'in Tewksbury, working with individuals, small businesses and non-profit '
                  'organizations across the Merrimack Valley.'),
    footer_note='Secure client portal available for exchanging documents with the office.',
    footer_services=[
        ('services/tax-preparation.html', 'Tax Return Preparation'),
        ('services/irs-representation.html', 'IRS Problem Resolution'),
        ('services/small-business-services.html', 'Small Business Services'),
        ('services/quickbooks.html', 'QuickBooks Consulting'),
        ('services/business-valuation.html', 'Business Valuation'),
        ('services/index.html', 'All services &rarr;'),
    ],
    footer_firm=[
        ('about.html', 'About the firm'),
        ('client-portal.html', 'Client portal'),
        ('pay.html', 'Paying your invoice'),
        ('calculators/index.html', 'Financial calculators'),
        ('guides/irs-notice-what-to-do.html', 'Guide: an IRS notice arrived'),
        ('faq.html', 'Common questions'),
    ],
)

# Deep evergreen with a clay accent — chosen to sit apart from the navy-and-bronze
# palette used elsewhere in this engine, and verified against every contrast pair
# the audit checks (lowest ratio in the set is 3.13:1 on a 3.0 requirement, and
# every 4.5 pair clears 5.7:1 or better).
DESIGN = 'statute'   # see design.py

T = dict(ink='#16171A', ink2='#2A2B2F', acc='#A8842F', accd='#6E1F2A',
         accrgb='168,132,47', cream='#F4F1EA')   # bespoke palette, see site_hickey.py
NAV = [('services/index.html', 'Services', 'services'),
       ('services/irs-representation.html', 'IRS Problems', 'irs'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('client-portal.html', 'Client Portal', 'portal'),
       ('about.html', 'About', 'about'),
       ('contact.html', 'Contact', 'contact')]

# LOGO — "the total rule".
# One vertical hairline runs down the left as the rule of a ledger column; the
# initials sit in the column; a heavier horizontal rule closes it underneath, the
# way a column of figures is ruled off before the total. The weight difference
# between the two lines (1.5 against 2.8) is the whole idea and it is the part
# that survives at 20px, where the mark reads as JH over a single firm rule.
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6"><rect x="6" y="14" width="52" height="36"/><rect x="13" y="34" width="22" height="9" stroke-width="2"/><path d="M6 14l26 18 26-18" stroke-width="2"/></svg>')   # window-envelope mark, see site_hickey.py
def pages():
    import content_hickeycpa
    return content_hickeycpa.pages()


# QA gates specific to this firm --------------------------------------------
# Office line and fax only. 800-896-4500 and 802-655-1519 appear on the current
# site but belong to the website vendor, not the firm.
ALLOWED_PHONES = ['(978) 851-8945', '(978) 851-9314']

BANNED = [
    # vendor phone numbers that must never surface as the firm's
    '800-896-4500', '8008964500', '+18008964500',
    '802-655-1519', '8026551519', '+18026551519',
    # the firm states no founding year and no tenure anywhere on its site
    'founded', 'est. 19', 'est. 20', 'established in 19', 'established in 20',
    'years of experience', 'decades of experience', 'over 20 years',
    'for more than', 'since 19',
    # exactly one person is named, with no title and no bio
    'founder', 'managing partner', 'our partners', 'a partner will',
    'our team of', 'meet the team', 'our staff of', 'principal of the firm',
    # no membership of any professional body is claimed on the site
    'AICPA', 'American Institute of Certified Public Accountants',
    'Massachusetts Society of CPAs', 'MSCPA', 'peer review', 'peer-reviewed',
    # the self-registration link on the current site is dead; never reproduce it
    'securefirmportal.com/Account/Register', 'self-register',
    # no fee-timing or outcome promises
    'settle your debt for', 'pennies on the dollar', 'we can eliminate',
]
