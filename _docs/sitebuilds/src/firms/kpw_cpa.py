# -*- coding: utf-8 -*-
"""
Firm profile — Kolnicki, Peterson & Wirth, LLC (Downers Grove, IL).
Facts sourced only from the firm's own published material; see RESEARCH_NOTES.md.
"""

FIRM = dict(
    name='Kolnicki, Peterson & Wirth, LLC',
    short='KPW',
    founded=1974,
    years=52,
    email='info@kpwcpa.com',
    addr='1400 Opus Place, Suite 100',
    city='Downers Grove', state='IL', state_full='Illinois', zip='60515',
    tel='+16303901140', ph='(630) 390-1140', fax='(630) 390-1150',
    hours='Mon&ndash;Fri 9:00 AM&ndash;5:00 PM',
    office_page='locations/downers-grove.html',
    opens='09:00', closes='17:00',
    member_of=['American Institute of Certified Public Accountants', 'Illinois CPA Society'],
    area_served=['Chicagoland, Illinois'],
    geo=(41.8301728, -88.0236974),
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Kolnicki%2C+Peterson+%26+Wirth%2C+LLC+1400+Opus+Place+Downers+Grove+IL+60515'),
    # branding
    favicon_letter='K',
    brand_line='Kolnicki, Peterson &amp; Wirth',
    brand_sub='Certified Public Accountants',
    nav_cta='Talk to a CPA',
    topbar='Certified Public Accountants &middot; Downers Grove, IL &middot; Est. 1974',
    footer_blurb=('Certified Public Accountants serving privately held businesses, individuals, '
                  'and public-sector organizations from Downers Grove, Illinois since 1974.'),
    footer_note='Members, American Institute of Certified Public Accountants and Illinois CPA Society.',
    footer_services=[
        ('services/tax-planning-preparation.html', 'Tax Planning &amp; Preparation'),
        ('services/audit-assurance.html', 'Audit &amp; Assurance'),
        ('services/accounting-compilation.html', 'Accounting Services'),
        ('services/business-advisory.html', 'Business Advisory'),
        ('services/business-valuation.html', 'Business Valuation'),
        ('services/index.html', 'All services &rarr;'),
    ],
    footer_firm=[
        ('about.html', 'About the firm'),
        ('team/index.html', 'Our team'),
        ('peer-review.html', 'Peer review &amp; quality'),
        ('industries/index.html', 'Industries'),
        ('faq.html', 'Common questions'),
        ('guides/cpa-cost-small-business.html', 'Guides'),
    ],
)

DESIGN = 'ledger'   # see design.py

T = dict(ink='#142A44', ink2='#24405E', acc='#B98D43', accd='#7E5E20',
         accrgb='185,141,67', cream='#F6F2E9')

NAV = [('services/index.html', 'Services', 'services'),
       ('industries/index.html', 'Industries', 'industries'),
       ('team/index.html', 'Our Team', 'team'),
       ('about.html', 'About', 'about'),
       ('locations/downers-grove.html', 'Location', 'locations'),
       ('contact.html', 'Contact', 'contact')]

# Concept B — ruled lettermark. Two hairlines set the initials the way a
# ledger rules a column; the serif face ties it to the body typography.
LOGO = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="6" y="17.5" width="52" height="1.6" fill="currentColor"/>'
        '<rect x="6" y="45.5" width="52" height="1.6" fill="currentColor"/>'
        '<text x="32" y="39" text-anchor="middle" fill="currentColor" '
        'font-size="19.5" letter-spacing="1.4">KPW</text></svg>')


def pages():
    import content_core, content_services, content_industries, content_team, content_guides
    out = []
    for mod in (content_core, content_services, content_industries, content_team, content_guides):
        out += mod.pages()
    return out


# QA gates specific to this firm
ALLOWED_PHONES = ['(630) 390-1140', '(630) 390-1150']

# The Chicago office is closed. Their old kpwcpachicago.com site still advertises
# it, so it can creep back in from sources. "University of Chicago" and
# "Chicagoland" are legitimate and deliberately NOT banned.
BANNED = ['954 W Washington', '(312) 421', '+13124215780', 'West Loop',
          'Chicago office', 'locations/chicago', 'Chicago@kpwcpa',
          'Downers Grove &amp; Chicago', 'Downers Grove and Chicago',
          'two offices', 'Two offices', 'both offices', 'Both offices', 'either office']
