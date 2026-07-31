# -*- coding: utf-8 -*-
"""
Firm profile — Fitzpatrick & Goguen CPAs P.C. (Billerica, MA).

Every fact below is taken from the firm's own published material (team page,
contact block, homepage tagline and stated principles) as verified 2026-07-30.
No founding year is claimed because the firm does not state one. Credentials are
reproduced exactly: two of the five people hold credentials; three do not, and
none are invented for them.

The firm's TaxDome client portal at https://www.bgoguen.com/login is live and
fully branded but is not linked from any page of their current site. It is
surfaced here in the top bar of every page, in the main navigation, on a
dedicated page, in the hero, and in the footer.
"""

PORTAL = 'https://www.bgoguen.com/login'

FIRM = dict(
    name='Fitzpatrick & Goguen CPAs P.C.',
    short='F&amp;G',
    # No founding year is published by the firm. Deliberately absent — the
    # engine only reads FIRM['founded'] from its KPW-specific org_schema(),
    # which this build does not use.
    email='office@bgoguen.com',
    addr='164 Concord Road',
    city='Billerica', state='MA', state_full='Massachusetts', zip='01821',
    tel='+19786674595', ph='(978) 667-4595', fax='(978) 667-4597',
    # The firm does not publish office hours. Do not invent them.
    hours='Call or email for current office hours',
    office_page=None,
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Fitzpatrick+%26+Goguen+CPAs+P.C.+164+Concord+Road+Billerica+MA+01821'),
    # branding
    favicon_letter='F',
    brand_line='Fitzpatrick &amp; Goguen',
    brand_sub='Certified Public Accountants',
    nav_cta='Talk to us',
    topbar=('Certified Public Accountants &middot; Billerica, Massachusetts &middot; '
            '<a href="' + PORTAL + '" target="_blank" rel="noopener">Client portal sign-in &rarr;</a>'),
    footer_blurb=('Certified Public Accountants on Concord Road in Billerica, Massachusetts. '
                  'Bookkeeping, personal tax, and small business tax for people who want to '
                  'know their accountant by name.'),
    footer_note=('Existing clients: <a href="' + PORTAL + '" target="_blank" rel="noopener">'
                 '<strong>sign in to the secure client portal &rarr;</strong></a>'),
    footer_services=[
        ('services/personal-tax.html', 'Personal Tax Planning &amp; Preparation'),
        ('services/business-tax.html', 'Small Business Tax'),
        ('services/bookkeeping.html', 'Bookkeeping'),
        ('calculators/index.html', 'Financial calculators'),
        ('services/index.html', 'All services &rarr;'),
    ],
    footer_firm=[
        ('about.html', 'About the firm'),
        ('team/index.html', 'Our team'),
        ('client-portal.html', 'Client portal'),
        ('guides/what-your-accountant-needs.html', 'Guides'),
        ('faq.html', 'Common questions'),
        ('contact.html', 'Contact'),
    ],
)

# Pine green and terracotta — deliberately away from the navy/bronze used on the
# reference build. Every pair in the WCAG table clears AA at these values.
DESIGN = 'openhouse'   # see design.py

T = dict(ink='#0E3A42', ink2='#14535E', acc='#D08A50', accd='#8A4A1C',
         accrgb='208,138,80', cream='#F0F2F1')
NAV = [('services/index.html', 'Services', 'services'),
       ('team/index.html', 'Our Team', 'team'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('about.html', 'About', 'about'),
       ('client-portal.html', 'Client Portal', 'portal'),
       ('contact.html', 'Contact', 'contact')]

# Logo — an accounting bracket enclosing the FG monogram. Two names, one firm,
# held inside the bracket an accountant uses to enclose a figure. Set in the
# site serif so the mark and the wordmark are the same voice.
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path d="M14.5 14H9.5v36h5" fill="none" stroke="currentColor" stroke-width="3"/>'
        '<path d="M49.5 14h5v36h-5" fill="none" stroke="currentColor" stroke-width="3"/>'
        '<text x="32" y="42.5" text-anchor="middle" fill="currentColor" '
        'font-size="29" letter-spacing="-1">FG</text></svg>')


def pages():
    import content_bgoguen
    return content_bgoguen.pages()


# QA gates specific to this firm
ALLOWED_PHONES = ['(978) 667-4595', '(978) 667-4597']

# Honesty guards. An archived PDF credits Brian Goguen with a CFP mark; the
# current site does not, so it must never appear. Dana Reardon, Sean Malone and
# Monirina Kim have no credentials listed anywhere and must not acquire any.
# Two of the five are Investment Advisor Representatives with North Atlantic
# Investment Partners, LLC — a fact about those individuals, never a firm
# service. The firm publishes no founding year and no office hours.
BANNED = [
    'CFP', 'Certified Financial Planner', 'Personal Financial Specialist',
    'Reardon, CPA', 'Malone, CPA', 'Kim, CPA', 'Reardon, EA', 'Malone, EA',
    'Reardon, MBA', 'Malone, MBA', 'Dana Reardon, C', 'Sean Malone, C',
    'investment advisory service', 'investment advice', 'wealth management',
    'asset management', 'portfolio management', 'manage your investments',
    'financial planning service', 'we manage money', 'assets under management',
    'founded in', 'we were founded', 'the firm was founded', 'since our founding',
    'years in business', 'decades of serving',
    'audit and assurance', 'audited financial statements', 'assurance services',
    'attest engagement', 'peer review',
    'payroll processing', 'we process payroll', 'we run payroll',
    'five CPAs', 'all of our CPAs', 'our CPAs',
    'domain', 'migrate your site', 'switch your website', 'new website',
]
