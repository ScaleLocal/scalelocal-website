# -*- coding: utf-8 -*-
"""
Firm profile — Dorfman & Dorfman, CPAs (Wilmington, Massachusetts).

Every fact below is taken from the firm's own published material (see the
research note for dorfmancpas). Two owners, both CPAs, both named on the site.
Nothing on their site suggests audit or attest work, so none is claimed here;
no memberships, no staff beyond the two owners, no office hours (they publish
none) and no portal or payment system (they have none).
"""

FIRM = dict(
    name='Dorfman & Dorfman, CPAs',
    short='Dorfman',
    founded=2008,
    years=18,
    email='estee@dorfman-cpas.com',
    addr='402 Main Street, Suite #2',
    city='Wilmington', state='MA', state_full='Massachusetts', zip='01887',
    tel='+17817807069', ph='(781) 780-7069', fax='(781) 780-7062',
    # The firm publishes no office hours. Do not invent any.
    hours='Call the office for current hours',
    office_page=None,
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Dorfman+%26+Dorfman%2C+CPAs+402+Main+Street+Suite+2+Wilmington+MA+01887'),
    # branding
    favicon_letter='D',
    brand_line='Dorfman &amp; Dorfman',
    brand_sub='Certified Public Accountants',
    nav_cta='Talk to a CPA',
    topbar='Certified Public Accountants &middot; Wilmington, MA &middot; Est. 2008',
    footer_blurb=('A family-owned CPA firm on Main Street in Wilmington, providing accounting and '
                  'tax services to small businesses and individuals across Massachusetts since 2008.'),
    footer_note='Marvin H. Dorfman, CPA &middot; Estee C. Dorfman, CPA, MSA &mdash; the two people who own the firm and do the work.',
    footer_services=[
        ('services/individual-tax.html', 'Individual Tax Preparation'),
        ('services/business-tax.html', 'Business Tax Preparation'),
        ('services/bookkeeping-write-up.html', 'Bookkeeping &amp; Write-Up'),
        ('services/payroll.html', 'Payroll'),
        ('services/small-business-consulting.html', 'Small Business Consulting'),
        ('services/index.html', 'All services &rarr;'),
    ],
    footer_firm=[
        ('about.html', 'About the firm'),
        ('team/marvin-h-dorfman.html', 'Marvin H. Dorfman, CPA'),
        ('team/estee-c-dorfman.html', 'Estee C. Dorfman, CPA, MSA'),
        ('regulatory-background.html', 'Regulatory background'),
        ('calculators/index.html', 'Calculators'),
        ('faq.html', 'Common questions'),
    ],
)

# Deep pine green with a clay accent — deliberately distinct from the navy/bronze
# used elsewhere in the engine. Verified against the WCAG pair list.
DESIGN = 'examiner'   # see design.py

T = dict(ink='#2C2521', ink2='#453A32', acc='#B8913F', accd='#795C16',
         accrgb='184,145,63', cream='#F4F0E5')
NAV = [('services/index.html', 'Services', 'services'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('regulatory-background.html', 'Regulatory Background', 'regulatory'),
       ('about.html', 'About', 'about'),
       ('contact.html', 'Contact', 'contact')]

# Mirrored-D monogram. Two Dorfmans, one firm: a single heavy stem carries a
# bowl on each side, so the mark reads as two facing D's that share a spine
# rather than as two separate letters. Flat top and bottom terminals keep it
# legible as a letterform; the stem is heavier than the bowls, which gives it
# the thick/thin contrast of the serif face used across the site. Nothing to
# lose at 20px — it stays a symmetrical, deliberate shape in one flat colour.
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path d="M32 12.5 H37 C48 12.5 55.5 21 55.5 32 C55.5 43 48 51.5 37 51.5 H32" '
        'fill="none" stroke="currentColor" stroke-width="3.4"/>'
        '<path d="M32 12.5 H27 C16 12.5 8.5 21 8.5 32 C8.5 43 16 51.5 27 51.5 H32" '
        'fill="none" stroke="currentColor" stroke-width="3.4"/>'
        '<rect x="29.7" y="11" width="4.6" height="42" fill="currentColor"/>'
        '</svg>')


def pages():
    import content_dorfmancpas
    return content_dorfmancpas.pages()


# QA gates specific to this firm
ALLOWED_PHONES = ['(781) 780-7069', '(781) 780-7062']

# Claims this firm does NOT make on its own site, and cross-contamination from
# the other builds in this repo. Any of these appearing in output is a bug.
BANNED = [
    # no attest practice of any kind is claimed anywhere on their site
    'audit services', 'audit engagement', 'our audit', 'we audit', 'attest',
    'compilation', 'reviewed financial statements', 'broker-dealer audit',
    'audits broker', 'securities audit',
    # no memberships are claimed
    'AICPA', 'American Institute of Certified Public Accountants',
    'Massachusetts Society of Certified Public Accountants', 'MassCPAs',
    'peer review', 'Enrolled Agent',
    # no portal, payments or online forms exist today
    'client portal', 'secure portal', 'pay online', 'online payment',
    'upload your documents', 'submit the form',
    # staff and scale claims that are not supported
    'our staff of', 'our associates', 'our team of', 'clients served',
    # other firms in this build directory
    'Kolnicki', 'Downers Grove', 'Illinois', 'CalcXML', 'cchwebsites',
]
