# -*- coding: utf-8 -*-
"""
Design systems.

The engine previously exposed six colour tokens and nothing else, so every firm got
the same page in a different paint job. This module is the missing layer: typography,
hero composition, card treatment, nav placement, and the shape language (radius,
border weight, shadow) are all design decisions, and they belong to the firm.

A DESIGN dict is resolved per firm in firms/<slug>.py via `design='<name>'`.
Anything not specified falls back to BASE, so an unset key is never a hard error.
"""

BASE = dict(
    # typography
    serif='"Source Serif 4",Georgia,serif',
    sans='"Inter",-apple-system,"Segoe UI",Arial,sans-serif',
    gfont='Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700',
    h1='clamp(2.15rem,4.6vw,3.45rem)',
    h2='clamp(1.7rem,3.4vw,2.6rem)',
    hweight='600',
    htrack='-.012em',
    body='16.5px',
    lh='1.62',
    # shape language
    radius='16px',
    radius_sm='8px',
    border='1px',
    sh1='0 1px 2px rgba(20,18,12,.04),0 8px 24px rgba(20,18,12,.06)',
    sh2='0 24px 60px rgba(20,18,12,.14)',
    # composition
    hero='classic',        # classic | split | statement | rule | panel
    cards='raised',        # raised | flat | ruled | numbered
    nav='right',           # right | center | stacked
    eyebrow='dashed',      # dashed | caps | bracket | none
    dots=True,             # the dotted texture overlay on dark sections
    sec_pad='88px',
    glyph='columns',
)


SYSTEMS = {

    # ------------------------------------------------------------------ KPW
    # The original. Warm serif, raised cards, dotted navy. Left as-is.
    'ledger': dict(),

    # ------------------------------------------------------------- Hickey
    # Long-established Merrimack Valley practice with a heavy IRS caseload.
    # Wants gravitas and density: a tight slab serif, hard corners, ruled
    # dividers instead of floating cards, no decorative texture.
    'statute': dict(
        glyph='seal',
        serif='"Zilla Slab",Georgia,serif',
        sans='"IBM Plex Sans",-apple-system,"Segoe UI",Arial,sans-serif',
        gfont='Zilla+Slab:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700',
        h1='clamp(2.05rem,4.1vw,3.05rem)',
        h2='clamp(1.55rem,3vw,2.25rem)',
        hweight='600', htrack='-.005em',
        body='16px', lh='1.66',
        radius='3px', radius_sm='3px', border='1px',
        sh1='none', sh2='0 18px 44px rgba(30,12,16,.16)',
        hero='rule', cards='ruled', nav='stacked', eyebrow='bracket',
        dots=False, sec_pad='76px',
    ),

    # ------------------------------------------------------------- Carella
    # One accountant, no staff page, nothing to show off. The design should be
    # quiet and text-first: generous measure, a humanist serif, no cards at all.
    'quiet': dict(
        glyph='none',
        serif='"Lora",Georgia,serif',
        sans='"Karla",-apple-system,"Segoe UI",Arial,sans-serif',
        gfont='Lora:wght@400;500;600&family=Karla:wght@400;500;600;700',
        h1='clamp(1.95rem,3.7vw,2.8rem)',
        h2='clamp(1.45rem,2.7vw,2rem)',
        hweight='500', htrack='0',
        body='17px', lh='1.72',
        radius='0px', radius_sm='2px', border='1px',
        sh1='none', sh2='none',
        hero='statement', cards='flat', nav='center', eyebrow='caps',
        dots=False, sec_pad='94px',
    ),

    # ------------------------------------------------------- Mill City
    # Lowell mill yards: brick, granite, copper. Industrial geometry, a grotesque
    # with real weight, square corners, numbered sections like a works order.
    'millyard': dict(
        glyph='weave',
        serif='"Archivo",Helvetica,Arial,sans-serif',
        sans='"Archivo",-apple-system,"Segoe UI",Arial,sans-serif',
        gfont='Archivo:wght@400;500;600;700;800',
        h1='clamp(2.1rem,4.4vw,3.2rem)',
        h2='clamp(1.6rem,3.1vw,2.3rem)',
        hweight='700', htrack='-.028em',
        body='16px', lh='1.6',
        radius='0px', radius_sm='0px', border='2px',
        sh1='none', sh2='0 20px 50px rgba(10,30,26,.2)',
        hero='panel', cards='numbered', nav='right', eyebrow='caps',
        dots=False, sec_pad='80px',
    ),

    # ------------------------------------------------- Fitzpatrick & Goguen
    # Five people, a real client portal, a stated ambition about clients' lives.
    # Softest of the six: rounded, airy, a friendly geometric sans over a
    # transitional serif. The most "practice-of-people" of the set.
    'openhouse': dict(
        glyph='arc',
        serif='"Fraunces",Georgia,serif',
        sans='"Figtree",-apple-system,"Segoe UI",Arial,sans-serif',
        gfont='Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Figtree:wght@400;500;600;700',
        h1='clamp(2.2rem,4.5vw,3.3rem)',
        h2='clamp(1.65rem,3.2vw,2.4rem)',
        hweight='500', htrack='-.018em',
        body='17px', lh='1.68',
        radius='24px', radius_sm='12px', border='1px',
        sh1='0 2px 4px rgba(14,58,66,.05),0 12px 32px rgba(14,58,66,.08)',
        sh2='0 30px 70px rgba(14,58,66,.16)',
        hero='split', cards='raised', nav='right', eyebrow='dashed',
        dots=True, sec_pad='92px',
    ),

    # ------------------------------------------------------------- Dorfman
    # Two people, same surname, a former FINRA examiner. Formal and symmetrical:
    # a high-contrast didone, centred composition, thin rules, espresso and brass.
    'examiner': dict(
        glyph='rule',
        serif='"Playfair Display",Georgia,serif',
        sans='"Inter Tight",-apple-system,"Segoe UI",Arial,sans-serif',
        gfont='Playfair+Display:wght@400;500;600;700&family=Inter+Tight:wght@400;500;600;700',
        h1='clamp(2.1rem,4.3vw,3.15rem)',
        h2='clamp(1.6rem,3.1vw,2.3rem)',
        hweight='500', htrack='-.008em',
        body='16.5px', lh='1.66',
        radius='4px', radius_sm='4px', border='1px',
        sh1='none', sh2='0 22px 54px rgba(44,37,33,.18)',
        hero='rail', cards='ruled', nav='center', eyebrow='caps',
        dots=False, sec_pad='90px',
    ),

    # --------------------------------------------------------- Mass Tax Pros
    # A trading brand, not a surname — the only one of the six with a real
    # consumer-facing identity. Confident, modern, aubergine: tight display
    # sans headings over a workhorse text face, boxed panels, bold numerals.
    'brandmark': dict(
        glyph='grid',
        serif='"Bricolage Grotesque",Helvetica,Arial,sans-serif',
        sans='"Public Sans",-apple-system,"Segoe UI",Arial,sans-serif',
        gfont='Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Public+Sans:wght@400;500;600;700',
        h1='clamp(2.15rem,4.7vw,3.4rem)',
        h2='clamp(1.65rem,3.3vw,2.45rem)',
        hweight='600', htrack='-.032em',
        body='16.5px', lh='1.62',
        radius='10px', radius_sm='6px', border='1px',
        sh1='0 1px 2px rgba(58,36,64,.05),0 10px 28px rgba(58,36,64,.09)',
        sh2='0 26px 62px rgba(58,36,64,.2)',
        hero='panel', cards='numbered', nav='right', eyebrow='bracket',
        dots=True, sec_pad='86px',
    ),
}


def resolve(name):
    d = dict(BASE)
    d.update(SYSTEMS.get(name, {}))
    return d
