# -*- coding: utf-8 -*-
"""
Page builder for the bespoke James L. Hickey site.

Consumes the honesty-checked prose extracted from the previous build and re-lays it
into the new architecture. No shared engine, no shared CSS, no shared components.

    python3 site_hickey_build.py
"""
import json, os, re, html as H
import site_hickey as S
import calculators as C

B = S.BLOCKS
OUT = S.OUT
F = S.F

# ---------------------------------------------------------------- helpers
SERVICE_ORDER = [
    ('services/tax-preparation.html', 'Tax preparation'),
    ('services/tax-planning.html', 'Tax planning'),
    ('services/small-business-services.html', 'Small business services'),
    ('services/quickbooks.html', 'QuickBooks setup and training'),
    ('services/bank-financing.html', 'Bank financing and business plans'),
    ('services/entity-formation.html', 'Choosing and forming an entity'),
    ('services/business-valuation.html', 'Business valuation'),
    ('services/succession-planning.html', 'Succession planning'),
    ('services/personal-financial-planning.html', 'Personal financial planning'),
    ('services/estate-planning.html', 'Estate planning'),
    ('services/elder-care.html', 'Elder care'),
    ('services/non-profit.html', 'Non-profit organizations'),
]
IRS_ORDER = [
    ('services/irs-representation.html', 'Representation before the IRS',
     'Someone with unlimited practice rights answers the letter, not you.'),
    ('services/non-filed-returns.html', 'Returns you have not filed',
     'Every unfiled year stays open until it is filed. There is an order to fixing it.'),
    ('services/irs-payment-plans.html', 'A balance you cannot pay at once',
     'Instalment agreements and the arithmetic that decides which one you qualify for.'),
    ('services/innocent-injured-spouse.html', 'Liability that is not yours',
     'A joint signature makes both people responsible. Sometimes that can be undone.'),
]


def blocks_html(path, skip_first_p=0, stop_at=None):
    """Re-emit stored blocks. Tables get a scroll wrapper; nothing else is altered.

    The old layout printed the standfirst inside the body as well as above it. Here the
    standfirst is its own element, so an opening paragraph that merely repeats it is
    dropped rather than shown twice."""
    out, seen_p = [], 0
    sub = (B[path].get('sub') or '').strip()
    for i, b in enumerate(B[path]['blocks']):
        if i == 0 and b['tag'] == 'p' and sub and b['text'].strip()[:80] == sub[:80]:
            continue
        if stop_at and b['tag'] == 'h2' and stop_at in b['text']:
            break
        if b['tag'] == 'p' and seen_p < skip_first_p:
            seen_p += 1
            continue
        if b['tag'] == 'table':
            out.append('<div class="tblwrap"><table>' + b['html'] + '</table></div>')
        else:
            out.append('<' + b['tag'] + '>' + b['html'] + '</' + b['tag'] + '>')
    return ''.join(out)


def marginal(title, items, d):
    """items are hrefs relative to the PAGE, not the site root. Prefixing them with
    S.rel(depth,...) produced ../sibling.html for same-directory links."""
    return ('<aside class="marginal"><b>' + title + '</b>' +
            ''.join('<a href="' + h + '">' + l + '</a>' for h, l in items) + '</aside>')


def page_shell(path, depth, nav, title, desc, h1, stand, trail, copy, marg=None, closing=None):
    body = ('<div class="page"><div class="sheet">'
            '<div class="trail">' + trail + '</div>'
            '<h1>' + h1 + '</h1>'
            + ('<p class="stand">' + stand + '</p>' if stand else '')
            + '<div class="rule"></div></div>'
            '<div class="sheet"><div class="body">'
            + (marg or '<div class="marginal"></div>')
            + '<div class="copy">' + copy + '</div>'
            '</div></div></div>')
    p = dict(path=path, depth=depth, nav=nav, title=title, desc=desc, schema=[ORG])
    if closing:
        p['closing'] = closing
    return S.write(p, body)


def trail_of(d, items):
    out = []
    for label, href in items:
        out.append('<a href="' + S.rel(d, href) + '">' + label + '</a>' if href else '<b>' + label + '</b>')
    return '<span>/</span>'.join(out)


ORG = {
    "@context": "https://schema.org", "@type": "AccountingService",
    "@id": S.BASE + "#firm", "name": F['name'], "url": S.BASE,
    "telephone": F['ph'], "faxNumber": F['fax'], "email": F['email'], "priceRange": "$$",
    "address": {"@type": "PostalAddress", "streetAddress": F['addr'], "addressLocality": F['city'],
                "addressRegion": F['state'], "postalCode": F['zip'], "addressCountry": "US"},
    "hasMap": F['maps'],
    "areaServed": [{"@type": "AdministrativeArea", "name": "Merrimack Valley, Massachusetts"}],
}


# ================================================================== HOME
def home():
    h = B['index.html']
    areas = ''.join(
        ('<a href="' + href + '">' + label + '</a><i>&middot;</i>' if i < len(SERVICE_ORDER) - 1
         else '<a href="' + href + '">' + label + '</a>')
        for i, (href, label) in enumerate(SERVICE_ORDER))

    steps = ''
    for i, (href, ttl, note) in enumerate(IRS_ORDER, 1):
        steps += ('<li><span class="n">%02d</span>'
                  '<span class="t">%s<small>%s</small></span>'
                  '<a class="go" href="%s">Read &rarr;</a></li>' % (i, ttl, note, href))

    contents = ''
    for i, (href, label) in enumerate(SERVICE_ORDER, 1):
        contents += ('<a href="' + href + '"><span class="ttl">' + label + '</span>'
                     '<span class="dots"></span><span class="pg">%02d</span></a>' % i)

    body = (
        '<section class="opening"><div class="sheet"><div class="grid"><div>'
        '<div class="kicker">Tewksbury, Massachusetts</div>'
        '<h1>' + h['h1'] + '</h1>'
        '<p class="stand">' + (h['sub'] or '') + '</p>'
        '<p class="after">Or start here: <a href="irs.html">an IRS notice arrived and I don’t know what it means</a>.</p>'
        '</div>'
        '<div class="particulars"><div class="cap">The office</div><dl>'
        '<dt>Address</dt><dd>' + F['addr'] + '<br>' + F['city'] + ', ' + F['state'] + ' ' + F['zip'] + '</dd>'
        '<dt>Telephone</dt><dd><a class="mono" href="tel:' + F['tel'] + '">' + F['ph'] + '</a></dd>'
        '<dt>Facsimile</dt><dd><span class="mono">' + F['fax'] + '</span></dd>'
        '<dt>Email</dt><dd><a href="mailto:' + F['email'] + '">' + F['email'] + '</a></dd>'
        '<dt>Principal</dt><dd>' + F['person'] + '</dd>'
        '</dl><a class="act" href="' + F['portal'] + '" rel="noopener">Client portal sign-in</a></div>'
        '</div>'
        '<div class="areas"><div class="lbl">Practice areas</div><div class="run">' + areas + '</div></div>'
        '</div></section>'

        '<section class="procedure"><div class="sheet">'
        '<h2>If the IRS has written to you, there is an order to doing this.</h2>'
        '<p class="intro">A CPA holds unlimited practice rights before the Internal Revenue Service, '
        'which means this office can deal with them on your behalf rather than coaching you through it. '
        'Most cases start in one of four places.</p>'
        '<ol>' + steps + '</ol>'
        '</div></section>'

        '<section class="index"><div class="sheet">'
        '<h2>The full practice, in one office.</h2>'
        '<p class="note">Twelve areas of work, all of it done in Tewksbury. Nothing is referred out '
        'to a network and nobody is handed to a call centre.</p>'
        '<div class="contents">' + contents + '</div>'
        '</div></section>'

        '<section style="padding:0 0 76px"><div class="sheet"><div class="mapblock">'
        '<iframe title="Map showing James L. Hickey, CPA PC at 170 Main Street, Suite 110, Tewksbury, Massachusetts" '
        'src="https://maps.google.com/maps?q=170+Main+Street,+Tewksbury,+MA+01876&amp;z=15&amp;output=embed" '
        'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
        '<p class="mapcap">170 Main Street, Suite 110 &middot; parking on site.</p>'
        '</div></section>')

    S.write(dict(path='index.html', depth=0, nav=None,
                 title='James L. Hickey, CPA PC | Tewksbury, MA Accountant',
                 desc=B['index.html']['desc'], schema=[ORG]), body)


# ============================================================ IRS HUB (new)
def irs_hub():
    steps = ''
    for i, (href, ttl, note) in enumerate(IRS_ORDER, 1):
        steps += ('<li><span class="n">%02d</span><span class="t">%s<small>%s</small></span>'
                  '<a class="go" href="%s">Read &rarr;</a></li>' % (i, ttl, note, href))
    copy = (
        '<p>An IRS notice is a document with a number on it, and the number tells you what it '
        'is. Before anything else, find that number &mdash; it is usually at the top right, and '
        'it starts CP or LTR. It decides what the letter actually wants and how long you have.</p>'
        '<div class="pull">Do not ignore it, and do not pay it because paying feels simpler. '
        'A notice can be wrong, and agreeing to an amount you do not owe is far harder to undo '
        'than disputing it in the first place.</div>'
        '<h2>Where most cases start</h2>')
    body = ('<div class="page"><div class="sheet">'
            '<div class="trail">' + trail_of(0, [('Home', 'index.html'), ('IRS problems', None)]) + '</div>'
            '<h1>When the IRS writes, you do not have to answer it alone.</h1>'
            '<p class="stand">A CPA holds unlimited practice rights before the Internal Revenue '
            'Service. This office can speak to them for you.</p>'
            '<div class="rule"></div></div>'
            '<div class="sheet"><div class="body">'
            + marginal('On this page', [('services/irs-representation.html', 'Representation'),
                                        ('services/non-filed-returns.html', 'Unfiled returns'),
                                        ('services/irs-payment-plans.html', 'Payment plans'),
                                        ('services/innocent-injured-spouse.html', 'Spousal relief'),
                                        ('guides/irs-notice-what-to-do.html', 'Guide: a notice arrived')], 0)
            + '<div class="copy">' + copy + '</div></div></div>'
            '</div>'
            '<section class="procedure" style="margin-top:0"><div class="sheet"><ol>' + steps + '</ol></div></section>')
    S.write(dict(path='irs.html', depth=0, nav='irs.html',
                 title='IRS Problem Resolution | James L. Hickey, CPA PC',
                 desc='A CPA with unlimited practice rights before the IRS, in Tewksbury, Massachusetts. '
                      'Representation, unfiled returns, payment plans and spousal relief.',
                 schema=[ORG]), body)


# ======================================================== SERVICES INDEX
def services_index():
    rows = ''
    for i, (href, label) in enumerate(SERVICE_ORDER, 1):
        first = next((b['text'] for b in B[href]['blocks'] if b['tag'] == 'p'), '')
        rows += ('<a href="' + os.path.basename(href) + '"><span class="ttl">' + label + '</span>'
                 '<span class="dots"></span><span class="pg">%02d</span></a>' % i)
    body = ('<div class="page"><div class="sheet">'
            '<div class="trail">' + trail_of(1, [('Home', 'index.html'), ('Practice', None)]) + '</div>'
            '<h1>' + B['services/index.html']['h1'] + '</h1>'
            '<p class="stand">' + (B['services/index.html']['sub'] or '') + '</p>'
            '<div class="rule"></div></div>'
            '<div class="sheet"><section class="index" style="padding:34px 0 76px">'
            '<div class="contents">' + rows + '</div></section></div></div>')
    S.write(dict(path='services/index.html', depth=1, nav='services/index.html',
                 title=B['services/index.html']['title'], desc=B['services/index.html']['desc'],
                 schema=[ORG]), body)


# ============================================================ BODY PAGES
def body_pages():
    sibs = [(os.path.basename(h), l) for h, l in SERVICE_ORDER]
    for href, label in SERVICE_ORDER:
        d = B[href]
        others = [(a, b) for a, b in sibs if a != os.path.basename(href)][:6]
        page_shell(href, 1, 'services/index.html', d['title'], d['desc'], d['h1'], d['sub'],
                   trail_of(1, [('Home', 'index.html'), ('Practice', 'services/index.html'), (label, None)]),
                   blocks_html(href),
                   marginal('Also in the practice', others, 1))

    for href, _t, _n in IRS_ORDER:
        d = B[href]
        others = [(os.path.basename(a), t) for a, t, _ in IRS_ORDER if a != href]
        page_shell(href, 1, 'irs.html', d['title'], d['desc'], d['h1'], d['sub'],
                   trail_of(1, [('Home', 'index.html'), ('IRS problems', 'irs.html'), (_t, None)]),
                   blocks_html(href),
                   marginal('IRS practice', others, 1))

    for path, nav, label in (('about.html', 'about.html', 'The firm'),
                             ('faq.html', None, 'Common questions'),
                             ('client-portal.html', None, 'Client portal'),
                             ('pay.html', None, 'Paying an invoice')):
        d = B[path]
        page_shell(path, 0, nav, d['title'], d['desc'], d['h1'], d['sub'],
                   trail_of(0, [('Home', 'index.html'), (label, None)]),
                   blocks_html(path),
                   marginal('The office', [('about.html', 'About the firm'),
                                           ('contact.html', 'Contact'),
                                           ('faq.html', 'Common questions'),
                                           ('client-portal.html', 'Client portal'),
                                           ('pay.html', 'Paying an invoice')], 0))

    for path in ('guides/irs-notice-what-to-do.html', 'guides/quickbooks-year-end-checklist.html'):
        d = B[path]
        page_shell(path, 1, None, d['title'], d['desc'], d['h1'], d['sub'],
                   trail_of(1, [('Home', 'index.html'), ('Guides', None), (d['h1'][:28] + '…', None)]),
                   blocks_html(path),
                   marginal('Related', [('../irs.html', 'IRS problems'),
                                        ('../services/quickbooks.html', 'QuickBooks'),
                                        ('../services/index.html', 'Full practice')], 1))


# ================================================================ CONTACT
def contact():
    d = B['contact.html']
    copy = (blocks_html('contact.html') +
            '<div class="mapblock" style="margin-top:30px">'
            '<iframe title="Map showing James L. Hickey, CPA PC at 170 Main Street, Suite 110, Tewksbury, Massachusetts" '
            'src="https://maps.google.com/maps?q=170+Main+Street,+Tewksbury,+MA+01876&amp;z=15&amp;output=embed" '
            'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
            '<p class="mapcap">Parking on site. The office is on Main Street, Route 38.</p>')
    page_shell('contact.html', 0, 'contact.html', d['title'], d['desc'], d['h1'], d['sub'],
               trail_of(0, [('Home', 'index.html'), ('Contact', None)]), copy,
               marginal('Reach the office', [('contact.html', 'Address and map'),
                                             ('client-portal.html', 'Client portal'),
                                             ('pay.html', 'Paying an invoice')], 0))


# ============================================================ CALCULATORS
def calculators():
    cards = ''
    for i, c in enumerate(C.CALCULATORS, 1):
        cards += ('<a href="' + c['slug'] + '.html"><span class="ttl">' + c['title'] + '</span>'
                  '<span class="dots"></span><span class="pg">%02d</span></a>' % i)
    body = ('<div class="page"><div class="sheet">'
            '<div class="trail">' + trail_of(1, [('Home', 'index.html'), ('Calculators', None)]) + '</div>'
            '<h1>Eight calculators, running on this page.</h1>'
            '<p class="stand">No pop-up, no third-party site, nothing sent anywhere. They work '
            'offline and they belong to this office.</p><div class="rule"></div></div>'
            '<div class="sheet"><section class="index" style="padding:34px 0 76px">'
            '<div class="contents">' + cards + '</div></section></div></div>')
    S.write(dict(path='calculators/index.html', depth=1, nav='calculators/index.html',
                 title='Financial calculators | James L. Hickey, CPA PC',
                 desc='Eight financial calculators that run directly on the page — mortgage, loan, '
                      'retirement, self-employment tax, Section 179, break-even and college saving.',
                 schema=[ORG]), body)

    for c in C.CALCULATORS:
        fields = ''
        for x in c['inputs']:
            pre = '<span>$</span>' if x['kind'] == C.MONEY else ''
            suf = ('<span>%</span>' if x['kind'] == C.PCT else
                   '<span>yrs</span>' if x['kind'] == C.YEARS else '')
            attrs = (' step="%s"' % x['step']) if x.get('step') else ''
            if x.get('min') is not None:
                attrs += ' min="%s"' % x['min']
            if x.get('max') is not None:
                attrs += ' max="%s"' % x['max']
            fields += ('<div class="fld"><label for="f_' + x['id'] + '">' + x['label'] + '</label>'
                       '<span class="inp">' + pre + '<input type="number" inputmode="decimal" id="f_'
                       + x['id'] + '" value="' + str(x['default']) + '"' + attrs + '>' + suf + '</span>'
                       + ('<span class="hint">' + x['hint'] + '</span>' if x.get('hint') else '') + '</div>')
        primary = next((o for o in c['outputs'] if o['primary']), c['outputs'][0])
        rows = ''
        for o in c['outputs']:
            if o['primary']:
                continue
            rows += ('<div class="row"><dt>' + o['label'] + '</dt>'
                     '<dd id="o_' + o['id'] + '">&mdash;</dd></div>'
                     + ('<div class="onote">' + o['note'] + '</div>' if o.get('note') else ''))
        spec = json.dumps(dict(inputs=[dict(id=x['id']) for x in c['inputs']],
                               outputs=[dict(id=o['id'], kind=o['kind']) for o in c['outputs']],
                               js=c['js']))
        body = ('<div class="page"><div class="sheet">'
                '<div class="trail">' + trail_of(1, [('Home', 'index.html'),
                                                     ('Calculators', 'calculators/index.html'),
                                                     (c['title'], None)]) + '</div>'
                '<h1>' + c['title'] + '</h1><p class="stand">' + c['blurb'] + '</p>'
                '<div class="rule"></div></div>'
                '<div class="sheet"><div class="calc" data-calc>'
                '<div class="fields">' + fields + '<p class="calcnote">' + c['note'] + '</p></div>'
                '<div class="result" aria-live="polite"><div class="cap">Result</div>'
                '<div class="head"><div class="l">' + primary['label'] + '</div>'
                '<div class="v" id="o_' + primary['id'] + '">&mdash;</div></div>'
                '<dl>' + rows + '</dl></div></div>'
                '<script type="application/json" id="calcspec">' + spec + '</script></div>'
                + CALC_JS + '</div>')
        S.write(dict(path='calculators/' + c['slug'] + '.html', depth=1, nav='calculators/index.html',
                     title=c['title'] + ' | James L. Hickey, CPA PC',
                     desc=_calc_desc(c), schema=[ORG]), body)


def _calc_desc(c):
    """Meta descriptions must land in 70-175 characters; a few blurbs are shorter."""
    d = c['blurb'].strip()
    if len(d) < 70:
        d = d.rstrip('.') + '. Runs on the page, in the Tewksbury office\'s own calculator set.'
    return d[:175]


CALC_JS = r"""
<script>(function(){
var host=document.querySelector('[data-calc]');if(!host)return;
var spec=JSON.parse(document.getElementById('calcspec').textContent);
var f=spec.inputs,outs=spec.outputs;
var M0=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
var M2=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2});
var N=new Intl.NumberFormat('en-US',{maximumFractionDigits:1});
function fmt(v,k){if(!isFinite(v))return '—';
  if(k==='money')return Math.abs(v)<100?M2.format(v):M0.format(v);
  if(k==='pct')return N.format(v)+'%';return N.format(v);}
var fn=new Function(f.map(function(x){return x.id;}).join(','),spec.js);
function read(){return f.map(function(x){
  var v=parseFloat(String(document.getElementById('f_'+x.id).value).replace(/[^0-9.\-]/g,''));
  return isFinite(v)?v:0;});}
function run(){var r;try{r=fn.apply(null,read());}catch(e){return;}
  outs.forEach(function(o){var el=document.getElementById('o_'+o.id);
    if(el)el.textContent=fmt(r[o.id],o.kind);});}
f.forEach(function(x){var el=document.getElementById('f_'+x.id);
  el.addEventListener('input',run);el.addEventListener('change',run);});
run();})();</script>
"""


def main():
    os.makedirs(os.path.join(OUT, 'css'), exist_ok=True)
    open(os.path.join(OUT, 'css', 'hickey.css'), 'w', encoding='utf-8').write(S.CSS)
    home(); irs_hub(); services_index(); body_pages(); contact(); calculators()
    n = sum(len(f) for _, _, f in os.walk(OUT) for f in [[x for x in f if x.endswith('.html')]])
    print('BUILT ->', OUT)


if __name__ == '__main__':
    main()
