# -*- coding: utf-8 -*-
"""
Mill City Accounting Services LLC — Lowell, Massachusetts
=========================================================
A standalone site. It shares NO layout, CSS, component or template with any other
build in this repo. build.py, site_hickey.py and site_carella.py are not imported
and must never be.

THE DESIGN PREMISE — "Open on Kearney Square"
---------------------------------------------
Scott Marchlik is NOT a CPA and his site claims no credential. Every other firm in
this batch leans on letters after a name. This one cannot, and should not try.

What it has instead is the thing none of the others publish: a named human being,
at a street address on a real square in downtown Lowell, with stated hours, who
will answer the phone. Hickey names one person and no hours. Carella names nobody
at all. So the organising idea here is *reachability* — the site behaves like a
door that is open at stated times, with a counter you walk up to.

The second idea is that Scott has two real specialisms, evidenced by his own bio:
quick-serve restaurant owners and rental real estate owners. Those are not service
lines, they are audiences, and they are the primary axis of the site.

Concretely, and deliberately unlike anything else in this repo:
  * the contact widget is a full-width filled COUNTER STRIP directly under the
    masthead on every page — not a floating tab (Hickey), not a card in a spare
    grid track (Carella). It carries a live open/closed state computed in-page
    from the published hours, and it carries the firm's real Square payment link.
  * two audience "doors" rather than a service menu as the primary split
  * filled surfaces and solid colour as the structural device — the other two
    builds are flat and hairline-ruled throughout
  * Archivo, not IBM Plex and not Public Sans; figures set in the display face at
    display size, not in a monospace and not merely tabular
  * a chalk ground with slate as a real surface and one vermilion signal — two
    working colours, not a single accent on near-white

Prose is the existing honesty-checked copy re-laid, plus new copy for the two
audience tracks whose every factual claim was verified against irs.gov and
mass.gov on 2026-07-31. See RESEARCH_millcityaccounting.md.

    python3 site_millcity.py
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'millcityaccounting')
BASE = 'https://www.scalelocal.net/test-builds/millcityaccounting/'

F = dict(
    name='Mill City Accounting Services LLC',
    short='Mill City',
    person='Scott Marchlik',
    person_title='Founder',
    addr='10 Kearney Square #302',
    city='Lowell', state='MA', state_full='Massachusetts', zip='01852',
    tel='+19789792904', ph='(978) 979-2904',
    fax='(978) 856-3515',
    email='scott@millcityaccounting.com',
    square='https://square.link/u/1BBydiwq',
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Mill+City+Accounting+Services+10+Kearney+Square+Lowell+MA+01852'),
    mapembed=('https://maps.google.com/maps?q=10+Kearney+Square+%23302%2C+Lowell%2C+MA+01852'
              '&t=&z=15&ie=UTF8&iwloc=&output=embed'),
)

# Published hours, verbatim from the firm's contact page. The counter strip reads
# its live state from this table and nowhere else.
HOURS = [('Monday', '9am', '5pm'), ('Tuesday', '9am', '5pm'), ('Wednesday', '9am', '5pm'),
         ('Thursday', '9am', '5pm'), ('Friday', '9am', '5pm'),
         ('Saturday', 'By appointment', None), ('Sunday', 'Closed', None)]

DEMO_LEAD = 'Demonstration site.'
DEMO_BODY = ('Prepared for Mill City Accounting Services LLC by ScaleLocal. Not affiliated '
             'with, authorised by, or endorsed by the firm. Reproduction or use of this site '
             'or its contents is prohibited.')

# The mark: a mill-window arch over a solid base — Lowell's mill sawtooth reduced to
# one form. Presented to the firm as a proposal; they have no existing mark.
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path d="M10 30a22 22 0 0 1 44 0v6H10z" fill="currentColor"/>'
        '<rect x="10" y="42" width="44" height="6" fill="currentColor"/>'
        '<rect x="10" y="52" width="44" height="4" fill="currentColor" opacity=".55"/>'
        '</svg>')

FAVICON = (
    "data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2064%2064%27"
    "%3E%3Crect%20width%3D%2764%27%20height%3D%2764%27%20fill%3D%27%23232A2E%27/%3E"
    "%3Cpath%20d%3D%27M12%2030a20%2020%200%200%201%2040%200v6H12z%27%20fill%3D%27%23D14A21%27/%3E"
    "%3Crect%20x%3D%2712%27%20y%3D%2742%27%20width%3D%2740%27%20height%3D%276%27%20fill%3D%27%23F2F0EA%27/%3E%3C/svg%3E")

CSS = r"""
/* Mill City Accounting Services LLC — bespoke stylesheet. Shared with no other build. */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --chalk:#F2F0EA;
  --chalk-2:#E7E4DA;
  --slate:#232A2E;
  --slate-2:#333D43;
  --slate-3:#4C575E;
  --ink:#1A1F22;
  --body:#3E464B;
  --quiet:#5F666B;
  --vermilion:#C4401A;
  --vermilion-lt:#F07A57;
  --vermilion-dk:#A5350F;
  --open:#1D6B4F;
  --paper:#FFFFFF;
  --edge:#D5D1C5;
  /* UI control boundaries need 3:1 (WCAG 1.4.11); --edge is a decorative rule at 1.5 */
  --field:#8F8A7F;
  --face:"Archivo",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  --r:3px;
}
html{-webkit-text-size-adjust:100%}
body{background:var(--chalk);color:var(--body);font-family:var(--face);
  font-size:16px;line-height:1.68;font-weight:400;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  overflow-wrap:break-word}
img{max-width:100%;display:block}
a{color:var(--vermilion-dk);text-underline-offset:2px}
a:hover{color:#8E2D0C}
:focus-visible{outline:3px solid var(--vermilion);outline-offset:2px}
h1,h2,h3,h4{color:var(--ink);font-weight:700;line-height:1.14}
h1,h2,.figure{font-stretch:112%}
strong,b{font-weight:600;color:var(--ink)}
.skip{position:absolute;left:-9999px;background:var(--vermilion);color:#fff;padding:10px 16px;
  z-index:99;font-weight:600;font-size:14px;border-radius:var(--r)}
.skip:focus{left:10px;top:10px}
.hold{max-width:1200px;margin:0 auto;padding:0 32px}

/* ------------------------------------------------------------ demo notice */
.demo{background:var(--slate);color:#CFD4D6;font-size:12.5px;line-height:1.5;padding:8px 0}
.demo b{color:var(--vermilion-lt);font-weight:600}
@media print{.demo{background:#fff;color:#000}}

/* ---------------------------------------------------------------- masthead */
.mast{background:var(--chalk);padding:26px 0 22px}
.mast .hold{display:flex;align-items:center;justify-content:space-between;gap:28px;
  flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none;color:var(--ink)}
.brand .mk{display:block;width:42px;height:42px;flex:0 0 42px;color:var(--vermilion)}
.brand .mk svg{width:100%;height:100%;display:block}
.brand .nm{font-size:21px;font-weight:700;font-stretch:112%;line-height:1.1;
  letter-spacing:-.005em}
.brand .nm span{display:block;font-size:11.5px;font-weight:500;font-stretch:100%;
  color:var(--quiet);margin-top:4px;letter-spacing:.01em}
.brand:hover .nm{color:var(--vermilion-dk)}
.mastright{display:flex;align-items:center;gap:26px;flex-wrap:wrap}
.mastright .where{font-size:13.5px;color:var(--quiet);line-height:1.5;text-align:right}
.mastright .where b{display:block;color:var(--ink);font-weight:600;font-size:14.5px}

/* nav: sentence-case links, no band rule, no sticky bar, no CTA pill */
.nav{background:var(--chalk);padding-bottom:20px}
.nav .hold{display:flex;gap:26px;flex-wrap:wrap;align-items:center}
.nav a{font-size:15px;font-weight:500;color:var(--body);text-decoration:none;
  padding:3px 0 4px;border-bottom:3px solid transparent}
.nav a:hover{color:var(--ink);border-bottom-color:var(--edge)}
.nav a[aria-current]{color:var(--ink);font-weight:700;border-bottom-color:var(--vermilion)}
.nav .door{color:var(--vermilion-dk);font-weight:600}
.nav .door[aria-current]{color:var(--vermilion-dk)}

/* =========================================================== THE COUNTER
   The contact widget. A full-width filled strip directly under the masthead on
   every page — never a floating tab, never a card in a side track. Four actions
   and a live open/closed state read from the firm's published hours. No script
   beyond that state, no network call, no third party. */
.counter{background:var(--slate);border-top:4px solid var(--vermilion);color:#E8EAEB}
.counter .hold{display:grid;grid-template-columns:auto repeat(4,minmax(0,1fr));
  align-items:stretch;gap:0}
.counter .state{display:flex;flex-direction:column;justify-content:center;
  padding:14px 26px 14px 0;min-width:200px}
.counter .state .lab{font-size:11px;font-weight:600;color:#98A1A6;letter-spacing:.02em}
.counter .state .now{font-size:17px;font-weight:700;font-stretch:112%;line-height:1.25;
  margin-top:2px;color:#fff;display:flex;align-items:center;gap:8px}
.counter .state .dot{width:9px;height:9px;border-radius:50%;background:var(--quiet);
  flex:0 0 9px}
.counter .state.is-open .dot{background:#4ED08F}
.counter .state.is-open .now{color:#8FE7BB}
.counter a{display:flex;flex-direction:column;justify-content:center;gap:2px;
  padding:14px 18px;text-decoration:none;color:#E8EAEB;
  border-left:1px solid var(--slate-2)}
.counter a .act{font-size:15px;font-weight:700;color:#fff;line-height:1.25}
.counter a .det{font-size:12.5px;color:#9FA8AD;line-height:1.35}
.counter a:hover{background:var(--slate-2);color:#fff}
.counter a:hover .det{color:#CFD4D6}
.counter a.pay{background:var(--vermilion-dk)}
.counter a.pay .det{color:#FADFD8}
.counter a.pay:hover{background:var(--vermilion)}
.counter a.pay:hover .det{color:#FFF6F3}

/* ------------------------------------------------------------------- page */
main{padding:44px 0 0}
.lede-wrap{max-width:780px}
.eyebrow{display:inline-block;background:var(--slate);color:#fff;font-size:12px;
  font-weight:600;padding:4px 10px;border-radius:var(--r);margin-bottom:16px}
.eyebrow.hot{background:var(--vermilion-dk)}
h1{font-size:clamp(30px,4.2vw,46px);letter-spacing:-.01em;line-height:1.08}
.stand{margin-top:16px;font-size:19px;line-height:1.55;color:var(--body);max-width:60ch}
.crumb{font-size:13px;color:var(--quiet);margin-bottom:14px}
.crumb a{color:var(--quiet);text-decoration:none}
.crumb a:hover{color:var(--vermilion-dk);text-decoration:underline}
.crumb i{font-style:normal;padding:0 8px;color:var(--edge)}

/* block: a filled panel, the site's primary structural device */
.block{margin-top:38px;background:var(--paper);border-radius:var(--r);padding:30px 32px;
  box-shadow:0 1px 2px rgba(26,31,34,.06),0 8px 22px rgba(26,31,34,.05)}
.block.plainbg{background:transparent;box-shadow:none;padding:0}
.block.dark{background:var(--slate);color:#D6DADC}
.block.dark h2,.block.dark h3{color:#fff}
.block.dark a{color:#F0A78F}
.block.dark a:hover{color:#fff}
.block > h2:first-child,.block > .bh:first-child{margin-top:0}
h2{font-size:26px;letter-spacing:-.008em}
h3{font-size:17px;letter-spacing:-.004em}
.bh{display:flex;align-items:baseline;justify-content:space-between;gap:20px;flex-wrap:wrap}
.bh .tag{font-size:12px;font-weight:600;color:var(--quiet)}
.copy p,.copy li,.copy h3,.copy h4,.copy .after{max-width:72ch}
.copy p{margin-top:14px;font-size:16px;line-height:1.7}
.copy h3{margin-top:26px}
.copy h3 + p{margin-top:8px}
.copy h4{margin-top:20px;font-size:14.5px}
.copy ul,.copy ol{margin-top:13px;padding-left:0;list-style:none}
.copy li{position:relative;padding-left:26px;margin-top:9px}
.copy ul li::before{content:"";position:absolute;left:3px;top:10px;width:9px;height:9px;
  background:var(--vermilion);border-radius:1px}
.copy ol{counter-reset:c}
.copy ol li{counter-increment:c}
.copy ol li::before{content:counter(c);position:absolute;left:0;top:2px;width:19px;height:19px;
  background:var(--slate);color:#fff;border-radius:var(--r);font-size:11.5px;font-weight:700;
  display:flex;align-items:center;justify-content:center}
.copy .after{margin-top:20px;font-size:14.5px;color:var(--quiet);line-height:1.6}

/* the two doors */
.doors{margin-top:38px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.door-card{display:block;text-decoration:none;background:var(--slate);color:#D6DADC;
  border-radius:var(--r);padding:30px 30px 26px;position:relative;overflow:hidden}
.door-card::after{content:"";position:absolute;left:0;right:0;top:0;height:5px;
  background:var(--vermilion)}
.door-card:hover{background:var(--slate-2);color:#E8EAEB}
.door-card .who{font-size:12px;font-weight:600;color:#98A1A6}
.door-card h2{color:#fff;margin-top:8px;font-size:27px}
.door-card p{margin-top:12px;font-size:15.5px;line-height:1.6;max-width:40ch}
.door-card .go{margin-top:18px;display:inline-block;font-size:14.5px;font-weight:700;
  color:#F0A78F}
.door-card:hover .go{color:#fff}

/* a run of plain rows — services, deadlines, links */
.rows{margin-top:20px}
.rows a,.rows .row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;
  align-items:center;padding:15px 0;border-top:1px solid var(--edge);text-decoration:none;
  color:var(--ink)}
.rows > *:last-child{border-bottom:1px solid var(--edge)}
.rows .t{font-size:16.5px;font-weight:700;line-height:1.3}
.rows .d{display:block;font-weight:400;font-size:14.5px;color:var(--body);margin-top:3px;
  max-width:62ch;line-height:1.55}
.rows a:hover{color:var(--vermilion-dk)}
.rows a:hover .d{color:var(--body)}
.rows .when{font-size:13.5px;font-weight:700;color:var(--vermilion-dk);white-space:nowrap;
  text-align:right}

/* a stat / figure set — numbers in the display face, not a mono */
.figures{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  gap:2px;background:var(--edge);border-radius:var(--r);overflow:hidden}
.figures div{background:var(--paper);padding:18px 20px}
.block.dark .figures{background:var(--slate-3)}
.block.dark .figures div{background:var(--slate)}
.figures .figure{display:block;font-size:29px;font-weight:700;line-height:1.1;
  color:var(--vermilion-dk);letter-spacing:-.015em}
.block.dark .figures .figure{color:#F0A78F}
.figures .cap{display:block;margin-top:5px;font-size:13px;line-height:1.45;color:var(--quiet)}
.block.dark .figures .cap{color:#9FA8AD}

/* callout */
.note{margin-top:24px;background:var(--chalk-2);border-radius:var(--r);padding:18px 22px}
.note .nl{font-size:12px;font-weight:700;color:var(--vermilion-dk);margin-bottom:5px}
.note p{font-size:15px;line-height:1.62;color:var(--body)}
.note p + p{margin-top:10px}

/* tables */
.scroll{margin-top:18px;overflow-x:auto;-webkit-overflow-scrolling:touch}
table.grid{border-collapse:collapse;width:100%;min-width:460px;font-size:15px}
table.grid th,table.grid td{text-align:left;padding:11px 16px;vertical-align:top;
  line-height:1.5;border-bottom:1px solid var(--edge)}
table.grid th{background:var(--slate);color:#fff;font-size:12.5px;font-weight:600;
  border-bottom:0}
table.grid tr:last-child td{border-bottom:0}
table.grid td.n{font-weight:700;color:var(--ink);white-space:nowrap}

/* hours table */
.hours{margin-top:18px;width:100%;border-collapse:collapse;font-size:15px}
.hours td{padding:9px 0;border-bottom:1px solid var(--edge)}
.hours td:last-child{text-align:right;font-weight:700;color:var(--ink)}
.hours tr.today td{color:var(--vermilion-dk)}
.hours tr.today td:first-child::after{content:" — today";font-weight:600;font-size:13px}

/* map */
.map{margin-top:22px;border-radius:var(--r);overflow:hidden;background:var(--chalk-2)}
.map iframe{width:100%;height:320px;border:0;display:block}
.map + .cap{margin-top:10px;font-size:13px;color:var(--quiet)}

/* calculator */
.calcwrap{margin-top:24px}
.calcgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}
.fieldrow label{display:block;font-size:13.5px;font-weight:600;color:var(--ink);
  margin-bottom:5px}
.fieldbox{display:flex;align-items:center;background:var(--paper);border:2px solid var(--field);
  border-radius:var(--r);height:44px}
.fieldbox:focus-within{border-color:var(--vermilion)}
.fieldbox .pre,.fieldbox .suf{font-size:13px;font-weight:700;color:var(--quiet);padding:0 11px}
.fieldbox input{width:100%;min-width:0;border:0;background:transparent;height:100%;
  padding:0 6px;font:inherit;font-size:16px;font-weight:600;color:var(--ink);text-align:right}
.fieldbox input:focus{outline:0}
.hint{margin-top:5px;font-size:12.5px;color:var(--quiet);line-height:1.45}
.results{margin-top:26px;background:var(--slate);border-radius:var(--r);padding:26px 28px;
  color:#D6DADC}
.results .head{font-size:12px;font-weight:600;color:#98A1A6}
.results .big{font-size:44px;font-weight:700;font-stretch:112%;color:#fff;line-height:1.05;
  margin-top:4px;letter-spacing:-.02em}
.results dl{margin-top:22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
  gap:1px;background:var(--slate-3);border-radius:var(--r);overflow:hidden}
.results dl > div{background:var(--slate);padding:13px 16px}
.results dt{font-size:13px;color:#9FA8AD;line-height:1.4}
.results dd{font-size:19px;font-weight:700;color:#fff;margin-top:3px}
.results .onote{grid-column:1/-1;background:var(--slate);padding:0 16px 13px;font-size:12.5px;
  color:#9FA8AD;line-height:1.5}

/* footer */
.foot{margin-top:64px;background:var(--slate);color:#B9C0C4;padding:40px 0 30px}
.foot a{color:#D6DADC;text-decoration:none}
.foot a:hover{color:#fff;text-decoration:underline}
.foot .grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:36px}
.foot .fh{color:#fff;font-size:13px;font-weight:600;margin-bottom:12px}
.foot .who{font-size:15px;line-height:1.6}
.foot .who b{color:#fff;display:block;font-size:16.5px;font-weight:700;font-stretch:112%;
  margin-bottom:8px}
.foot ul{list-style:none;font-size:14.5px;line-height:2}
.foot .legal{margin-top:32px;padding-top:20px;border-top:1px solid var(--slate-2);
  font-size:12.5px;line-height:1.6;color:#8A9297}

/* ========================================================== responsive */
@media (max-width:1080px){
  .counter .hold{grid-template-columns:repeat(2,minmax(0,1fr))}
  .counter .state{grid-column:1/-1;padding:13px 0;border-bottom:1px solid var(--slate-2)}
  .counter a{border-left:1px solid var(--slate-2);border-top:1px solid var(--slate-2)}
  .counter a:nth-child(2),.counter a:nth-child(4){border-left:0}
}
@media (max-width:820px){
  .hold{padding:0 20px}
  .doors{grid-template-columns:minmax(0,1fr)}
  .foot .grid{grid-template-columns:minmax(0,1fr);gap:26px}
  .mast .hold{gap:16px}
  .mastright{width:100%;justify-content:space-between}
  .mastright .where{text-align:left}
  .block{padding:24px 22px}
  main{padding-top:32px}
}
@media (max-width:520px){
  .counter .state{padding:11px 0}
  .counter .state .now{font-size:15.5px}
  .counter a{padding:11px 13px}
  .counter a .act{font-size:14px}
  .counter a .det{font-size:11.5px;white-space:nowrap;overflow:hidden;
    text-overflow:ellipsis}
  .demo{font-size:11.5px;padding:7px 0}
  .results .big{font-size:36px}
  .rows a,.rows .row{grid-template-columns:minmax(0,1fr)}
  .rows .when{text-align:left}
}
@media print{
  .demo,.nav,.counter,.map{display:none}
  body{background:#fff;font-size:12pt}
}
"""

# ==========================================================================
# Navigation. Audience first: the two doors sit in the nav as coloured links,
# because "which of these are you" is the site's primary question.
# ==========================================================================
NAV = [
    ('restaurants.html',      'Restaurants',    'restaurants',  True),
    ('rentals.html',          'Rental property', 'rentals',     True),
    ('services/index.html',   'Services',       'services',     False),
    ('calculators/index.html', 'Calculators',   'calculators',  False),
    ('about.html',            'About Scott',    'about',        False),
    ('contact.html',          'Visit or call',  'contact',      False),
]

SERVICES = [
    ('services/tax-preparation.html', 'Tax preparation',
     'Business returns &mdash; 1120, 1120-S, 1065, Schedules C and E, 990 and 1041 &mdash; '
     'and personal 1040s with every state filing they require.'),
    ('services/bookkeeping.html', 'Bookkeeping',
     'Monthly, quarterly or annual compilation, including accounts payable and accounts '
     'receivable.'),
    ('services/payroll.html', 'Payroll',
     'Weekly or bi-weekly processing, including all required federal and state tax filings.'),
    ('services/new-business.html', 'New business consulting',
     'Forming the entity, drafting the operating agreement, annual reports, and applying '
     'for tax identification numbers.'),
    ('services/tax-planning.html', 'Tax planning',
     'Forecasting what next year&rsquo;s liability is going to be, while there is still '
     'time to change it.'),
    ('services/notary.html', 'Notarization',
     'Licensed in the Commonwealth of Massachusetts.'),
]


def rel(depth, target):
    if target.startswith(('http', 'mailto:', 'tel:', '#')):
        return target
    return ('../' * depth) + target


def esc(s):
    return H.escape(s, quote=True)


def nav_html(depth, active):
    out = ['<div class="nav"><div class="hold">']
    for href, label, key, door in NAV:
        cur = ' aria-current="page"' if key == active else ''
        cls = ' class="door"' if door else ''
        out.append('<a href="%s"%s%s>%s</a>' % (rel(depth, href), cls, cur, label))
    out.append('</div></div>')
    return ''.join(out)


def counter(depth):
    """THE CONTACT WIDGET.

    A filled strip under the masthead on every page. Four actions — call, email,
    pay an invoice, book a time — plus a live open/closed state read from the
    firm's own published hours. Entirely static: the only script is the clock,
    it makes no network call, loads nothing third-party, and degrades to a plain
    'Mon-Fri, 9am-5pm' label with JavaScript off."""
    return (
        '<div class="counter" data-contact-widget aria-label="Contact Mill City Accounting">'
        '<div class="hold">'
        '<div class="state" data-hours>'
        '<span class="lab">The office</span>'
        '<span class="now"><span class="dot" aria-hidden="true"></span>'
        '<span data-state-text>Mon&ndash;Fri, 9am&ndash;5pm</span></span>'
        '</div>'
        '<a href="tel:%s"><span class="act">Call Scott</span>'
        '<span class="det">%s</span></a>'
        '<a href="mailto:%s"><span class="act">Email</span>'
        '<span class="det">%s</span></a>'
        '<a class="pay" href="%s" target="_blank" rel="noopener">'
        '<span class="act">Pay an invoice</span>'
        '<span class="det">Secure card payment</span></a>'
        '<a href="%s"><span class="act">Book a time</span>'
        '<span class="det">Weekdays, or Saturday by appointment</span></a>'
        '</div></div>'
    ) % (F['tel'], F['ph'], F['email'], F['email'], F['square'],
         rel(depth, 'contact.html#book'))


COUNTER_JS = """<script>(function(){
var el=document.querySelector('[data-hours]');if(!el)return;
var t=el.querySelector('[data-state-text]');
var day,mins;
try{
  var f=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',weekday:'short',
        hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date()),g={};
  f.forEach(function(x){g[x.type]=x.value;});
  day={Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[g.weekday];
  mins=(parseInt(g.hour,10)%24)*60+parseInt(g.minute,10);
}catch(e){var d=new Date();day=d.getDay();mins=d.getHours()*60+d.getMinutes();}
var openNow=day>=1&&day<=5&&mins>=540&&mins<1020;
if(openNow){el.classList.add('is-open');
  var left=1020-mins,h=Math.floor(left/60);
  t.textContent=h>=1?('Open now \\u2014 until 5pm'):('Open \\u2014 closing in '+left+' min');
}else if(day>=1&&day<=5&&mins<540){t.textContent='Opens at 9am today';
}else if(day===6){t.textContent='Saturday \\u2014 by appointment';
}else if(day===0){t.textContent='Closed today \\u2014 opens Monday 9am';
}else{t.textContent='Closed \\u2014 opens '+(day===5?'Monday':'tomorrow')+' at 9am';}
})();</script>"""


def footer(depth):
    svc = ''.join('<li><a href="%s">%s</a></li>' % (rel(depth, h), t) for h, t, _ in SERVICES)
    return (
        '<footer class="foot"><div class="hold">'
        '<div class="grid">'
        '<div><div class="who"><b>%s</b>'
        '%s<br>%s, %s %s<br>'
        '<a href="tel:%s">%s</a> &nbsp;&middot;&nbsp; fax %s<br>'
        '<a href="mailto:%s">%s</a></div></div>'
        '<div><div class="fh">What Scott does</div><ul>%s</ul></div>'
        '<div><div class="fh">Who he does it for</div><ul>'
        '<li><a href="%s">Quick-serve restaurants</a></li>'
        '<li><a href="%s">Rental property owners</a></li>'
        '<li><a href="%s">About Scott</a></li>'
        '<li><a href="%s">Calculators</a></li>'
        '<li><a href="%s">Visit or call</a></li>'
        '<li><a href="%s" target="_blank" rel="noopener">Pay an invoice</a></li>'
        '</ul></div>'
        '</div>'
        '<p class="legal">%s %s</p>'
        '</div></footer>'
    ) % (F['name'], F['addr'], F['city'], F['state'], F['zip'], F['tel'], F['ph'],
         F['fax'], F['email'], F['email'], svc,
         rel(depth, 'restaurants.html'), rel(depth, 'rentals.html'),
         rel(depth, 'about.html'), rel(depth, 'calculators/index.html'),
         rel(depth, 'contact.html'), F['square'],
         DEMO_LEAD, DEMO_BODY)


def crumbs_html(depth, crumbs):
    if not crumbs:
        return ''
    bits = []
    for label, href in crumbs:
        bits.append('<a href="%s">%s</a>' % (rel(depth, href), label) if href else
                    '<span>%s</span>' % label)
    return '<div class="crumb">%s</div>' % '<i>/</i>'.join(bits)


def page(path, depth, nav, title, desc, h1, stand='', eyebrow='', eyebrow_hot=False,
         crumbs=(), body='', schema=(), tail=''):
    url = BASE + ('' if path == 'index.html' else path)
    ld = ''.join('<script type="application/ld+json">%s</script>'
                 % json.dumps(s, separators=(',', ':')) for s in schema)
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<title>%(title)s</title>'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="description" content="%(desc)s">'
        '<meta name="robots" content="noindex, nofollow">'
        '<meta name="googlebot" content="noindex, nofollow">'
        '<link rel="canonical" href="%(url)s">'
        '<meta name="theme-color" content="#232A2E">'
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="%(name)s">'
        '<meta property="og:title" content="%(title)s">'
        '<meta property="og:description" content="%(desc)s">'
        '<meta property="og:url" content="%(url)s">'
        '<meta property="og:image" content="%(base)sog.png">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Mill City Accounting Services, Lowell, Massachusetts">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="%(title)s">'
        '<meta name="twitter:description" content="%(desc)s">'
        '<meta name="twitter:image" content="%(base)sog.png">'
        '<link rel="apple-touch-icon" href="%(atouch)s">'
        '<link rel="icon" type="image/svg+xml" href="%(fav)s">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100,400;100,500;100,600;100,700;112,700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="%(css)s">%(ld)s</head>'
    ) % dict(title=esc(title), desc=esc(desc), url=url, name=esc(F['name']), base=BASE,
             css=rel(depth, 'css/millcity.css'), fav=FAVICON,
             atouch=rel(depth, 'apple-touch-icon.png'), ld=ld)

    eb = ('<span class="eyebrow%s">%s</span>' % (' hot' if eyebrow_hot else '', eyebrow)
          if eyebrow else '')
    doc = (
        head + '<body>'
        '<a class="skip" href="#main">Skip to content</a>'
        '<div class="demo"><div class="hold"><b>' + DEMO_LEAD + '</b> ' + DEMO_BODY + '</div></div>'
        '<header class="mast"><div class="hold">'
        '<a class="brand" href="' + rel(depth, 'index.html') + '">'
        '<span class="mk">' + MARK + '</span>'
        '<span class="nm">Mill City Accounting<span>Lowell, Massachusetts &middot; since 2018</span></span></a>'
        '<div class="mastright"><div class="where"><b>' + F['addr'] + '</b>'
        + F['city'] + ', ' + F['state'] + ' ' + F['zip'] + '</div></div>'
        '</div></header>'
        + nav_html(depth, nav)
        + counter(depth) +
        '<main id="main"><div class="hold">'
        '<div class="lede-wrap">'
        + crumbs_html(depth, crumbs) + eb +
        '<h1>' + h1 + '</h1>'
        + ('<p class="stand">' + stand + '</p>' if stand else '') +
        '</div>'
        + body +
        '</div></main>'
        + footer(depth)
        + COUNTER_JS + tail +
        '</body></html>'
    )
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(doc)
    return path


# ------------------------------------------------------------------ schema
def org_schema():
    return {
        '@context': 'https://schema.org', '@type': 'AccountingService',
        '@id': BASE + '#firm', 'name': F['name'], 'url': BASE,
        'email': F['email'], 'telephone': F['ph'], 'faxNumber': F['fax'],
        'founder': {'@type': 'Person', 'name': F['person'], 'jobTitle': F['person_title']},
        'address': {'@type': 'PostalAddress', 'streetAddress': F['addr'],
                    'addressLocality': F['city'], 'addressRegion': F['state'],
                    'postalCode': F['zip'], 'addressCountry': 'US'},
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification',
             'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
             'opens': '09:00', 'closes': '17:00'}],
        'hasMap': F['maps'],
    }


def crumb_schema(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n,
                                 'item': BASE + (u if u != 'index.html' else '')}
                                for i, (n, u) in enumerate(items)]}


def page_schema(name, path, desc):
    return {'@context': 'https://schema.org', '@type': 'WebPage', 'name': name,
            'description': desc, 'url': BASE + ('' if path == 'index.html' else path),
            'isPartOf': {'@id': BASE + '#firm'}}


def service_schema(name, desc, path):
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': name,
            'description': desc, 'url': BASE + path, 'provider': {'@id': BASE + '#firm'},
            'areaServed': {'@type': 'State', 'name': 'Massachusetts'}}


def faq_schema(pairs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                           for q, a in pairs]}


# -------------------------------------------------------- component helpers
def block(inner, dark=False, plain=False):
    cls = 'block' + (' dark' if dark else '') + (' plainbg' if plain else '')
    return '<section class="%s">%s</section>' % (cls, inner)


def bh(title, tag=''):
    return ('<div class="bh"><h2>%s</h2>%s</div>'
            % (title, '<span class="tag">%s</span>' % tag if tag else ''))


def rows(depth, items, when=False):
    """items: (href|None, title, detail, right_hand_text)"""
    out = ['<div class="rows">']
    for it in items:
        href, title, detail = it[0], it[1], it[2]
        right = it[3] if len(it) > 3 else ''
        rcell = '<span class="when">%s</span>' % right if right else '<span></span>'
        inner = ('<span><span class="t">%s</span><span class="d">%s</span></span>%s'
                 % (title, detail, rcell))
        out.append('<a href="%s">%s</a>' % (rel(depth, href), inner) if href
                   else '<div class="row">%s</div>' % inner)
    out.append('</div>')
    return ''.join(out)


def figures(items):
    return ('<div class="figures">%s</div>'
            % ''.join('<div><span class="figure">%s</span><span class="cap">%s</span></div>'
                      % (v, c) for v, c in items))


def note(label, *paras):
    return ('<div class="note"><div class="nl">%s</div>%s</div>'
            % (label, ''.join('<p>%s</p>' % p for p in paras)))


def table(headers, body_rows):
    th = ''.join('<th>%s</th>' % h for h in headers)
    tr = ''.join('<tr>%s</tr>' % ''.join(
        '<td%s>%s</td>' % (' class="n"' if isinstance(c, tuple) else '',
                           c[0] if isinstance(c, tuple) else c) for c in r)
        for r in body_rows)
    return ('<div class="scroll"><table class="grid"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (th, tr))


def mapblock():
    return ('<div class="map"><iframe title="Interactive Google map showing Mill City '
            'Accounting Services at 10 Kearney Square, Lowell, Massachusetts" src="%s" '
            'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen>'
            '</iframe></div><p class="cap">Pan, zoom, or <a href="%s" target="_blank" '
            'rel="noopener">open the map full screen</a> for directions.</p>'
            % (F['mapembed'], F['maps']))

# ==========================================================================
# Calculators. calculators.py is verified DATA plus a runtime keyed on element
# ids — no layout comes from it. The markup and styling here are this site's own.
# Four are included, chosen for the two audiences rather than to pad a list.
# ==========================================================================
import calculators as C

CALC_PICK = ['break-even', 'self-employment-tax', 'loan-payment', 'section-179']
CALCS = [c for s in CALC_PICK for c in C.CALCULATORS if c['slug'] == s]

CALC_WHY = {
    'break-even': ('For a quick-serve owner: the covers or the takings a week has to '
                   'reach before the rent, the wages and the insurance are paid for.'),
    'self-employment-tax': ('For anyone drawing profit rather than a wage &mdash; the '
                            'Social Security and Medicare half of what is owed.'),
    'loan-payment': ('For a landlord: what a mortgage or an acquisition loan actually '
                     'costs per month, and what the interest comes to over the term.'),
    'section-179': ('For a kitchen fit-out or a van: what an immediate deduction is '
                    'worth against a given rate.'),
}
# calculators.py is shared with the template builds, so per-site wording is
# overridden here rather than edited there.
NOTE_OVERRIDES = {
    'section-179': ('Section 179 cannot create a loss, and annual limits and phase-outs '
                    'apply. Ask Scott about the treatment before you sign a purchase '
                    'order, not after.'),
}

CALC_NOTE_MA = {
    'section-179': ('Massachusetts does not follow the federal bonus-depreciation rules '
                    'and has deferred conformity to the increased federal section&nbsp;179 '
                    'limits for the 2025 and 2026 tax years. The state deduction on the '
                    'same purchase may be materially smaller than the federal one.'),
    'self-employment-tax': ('The Social Security portion stops at an annual wage base that '
                            'is adjusted each year; the Medicare portion does not. This '
                            'estimates self-employment tax only &mdash; income tax sits on '
                            'top of it.'),
}


def calc_body(calc, depth=1):
    fields = ''
    for x in calc['inputs']:
        pre = '<span class="pre">$</span>' if x['kind'] == C.MONEY else ''
        suf = ('<span class="suf">%</span>' if x['kind'] == C.PCT else
               '<span class="suf">yrs</span>' if x['kind'] == C.YEARS else '')
        attrs = ' step="%s"' % x['step'] if x.get('step') else ''
        if x.get('min') is not None:
            attrs += ' min="%s"' % x['min']
        if x.get('max') is not None:
            attrs += ' max="%s"' % x['max']
        fields += ('<div class="fieldrow"><label for="f_%s">%s</label>'
                   '<div class="fieldbox">%s<input type="number" inputmode="decimal" '
                   'id="f_%s" value="%s"%s>%s</div>%s</div>'
                   % (x['id'], x['label'], pre, x['id'], x['default'], attrs, suf,
                      ('<p class="hint">%s</p>' % x['hint']) if x.get('hint') else ''))

    primary = next((o for o in calc['outputs'] if o['primary']), calc['outputs'][0])
    outs = ''
    for o in calc['outputs']:
        if o['primary']:
            continue
        outs += ('<div><dt>%s</dt><dd id="o_%s">&mdash;</dd>%s</div>'
                 % (o['label'], o['id'],
                    '<div class="onote">%s</div>' % o['note'] if o.get('note') else ''))

    spec = json.dumps(dict(
        inputs=[dict(id=x['id']) for x in calc['inputs']],
        outputs=[dict(id=o['id'], kind=o['kind']) for o in calc['outputs']],
        js=calc['js']), separators=(',', ':'))

    b = block(
        bh('Work it out', 'Runs in your browser')
        + '<div class="calcwrap" data-calc><div class="calcgrid">' + fields + '</div>'
        '<div class="results" aria-live="polite">'
        '<div class="head">' + primary['label'] + '</div>'
        '<div class="big" id="o_' + primary['id'] + '">&mdash;</div>'
        '<dl>' + outs + '</dl></div></div>'
        '<div class="note"><div class="nl">What this does not cover</div><p>'
        + NOTE_OVERRIDES.get(calc['slug'], calc['note']) + '</p></div>'
        '<script type="application/json" id="calcspec">' + spec + '</script>')

    if calc['slug'] in CALC_NOTE_MA:
        b += block(bh('One Massachusetts note')
                   + '<div class="copy"><p>' + CALC_NOTE_MA[calc['slug']] + '</p></div>')

    others = [(('calculators/%s.html' % o['slug']), o['title'], CALC_WHY[o['slug']])
              for o in CALCS if o['slug'] != calc['slug']]
    b += block(bh('The other calculators') + rows(depth, others), plain=True)
    b += block('<div class="copy"><p>This is an estimating tool, not advice. It uses the '
               'assumptions above and nothing else about your return. Call '
               '<a href="tel:%s">%s</a> or <a href="%s">book a time</a> to talk about what '
               'the figure means for you.</p></div>'
               % (F['tel'], F['ph'], rel(depth, 'contact.html#book')), dark=True)
    return b


def build_calculators():
    d = 1
    out = []
    hub = block(bh('Four calculators, chosen for two kinds of business')
                + '<div class="copy"><p>Not a library of sixteen mortgage variants. These '
                  'four answer the questions a quick-serve owner and a rental property '
                  'owner actually ask, and they run entirely in your browser &mdash; no '
                  'sign-in, no third-party script, nothing you type leaves the page.</p>'
                  '</div>'
                + rows(d, [('calculators/%s.html' % c['slug'], c['title'], CALC_WHY[c['slug']])
                           for c in CALCS]))
    hub += block(bh('Estimates, not advice')
                 + '<div class="copy"><p>Rates, thresholds and contribution limits change '
                   'every year, and none of these account for your filing status, your '
                   'Massachusetts position or anything else on your return. Use one to size '
                   'a question, then <a href="../contact.html">ask about the answer</a>.</p>'
                   '</div>', plain=True)
    out.append(page('calculators/index.html', d, 'calculators',
        'Calculators | Mill City Accounting Services',
        'Break-even, self-employment tax, loan payments and equipment purchases &mdash; four '
        'calculators for restaurant owners and rental property owners. Nothing leaves your browser.',
        'Four calculators.',
        'Break-even for a quick-serve, self-employment tax for an owner drawing profit, loan '
        'payments for a landlord, and what an equipment deduction is actually worth.',
        'Tools', False,
        (('Home', 'index.html'), ('Calculators', None)), hub,
        [page_schema('Calculators', 'calculators/index.html', 'Four native calculators.'),
         crumb_schema([('Home', 'index.html'), ('Calculators', 'calculators/index.html')])]))

    for c in CALCS:
        out.append(page('calculators/%s.html' % c['slug'], d, 'calculators',
            '%s | Mill City Accounting' % c['title'],
            (c['blurb'] + ' Runs entirely in your browser; nothing is sent anywhere.')[:174],
            c['title'] + '.', c['blurb'], 'Calculator', False,
            (('Home', 'index.html'), ('Calculators', 'calculators/index.html'),
             (c['title'], None)),
            calc_body(c, d),
            [page_schema(c['title'], 'calculators/%s.html' % c['slug'], c['blurb']),
             crumb_schema([('Home', 'index.html'),
                           ('Calculators', 'calculators/index.html'),
                           (c['title'], 'calculators/%s.html' % c['slug'])])],
            tail=C.CALC_JS))
    return out


# --------------------------------------------------------------- homepage
def build_home():
    d = 0
    b = ('<div class="doors">'
         '<a class="door-card" href="restaurants.html">'
         '<span class="who">If you run a</span>'
         '<h2>Quick-serve restaurant</h2>'
         '<p>Meals tax every month, tips, the service rate, a payroll that changes every '
         'week, and a food cost that decides whether any of it worked.</p>'
         '<span class="go">What Scott handles for restaurants &rarr;</span></a>'
         '<a class="door-card" href="rentals.html">'
         '<span class="who">If you own</span>'
         '<h2>Rental property</h2>'
         '<p>Schedule E, a depreciation schedule that has to survive twenty-seven years, '
         'passive losses that may not be deductible yet, and a recapture bill at the end.</p>'
         '<span class="go">What Scott handles for landlords &rarr;</span></a>'
         '</div>')

    b += block(bh('Why those two', 'Not a marketing choice')
        + '<div class="copy">'
        '<p>Scott Marchlik spent a decade at an accounting firm in Cambridge before '
        'starting Mill City in 2018, and his primary clientele there were quick-serve '
        'restaurant owners and rental real estate owners. Those are the two businesses he '
        'has done the most of, so they are the two this office is built around.</p>'
        '<p>Everything else &mdash; a contractor, a consultancy, a personal return with a '
        'rental attached &mdash; is welcome and familiar. But if you are one of those two, '
        'you are talking to somebody who has already seen your year.</p>'
        '<p class="after"><a href="about.html">More about Scott &rarr;</a></p></div>')

    b += block(bh('What the office does') + rows(d, SERVICES)
               + '<div class="copy"><p class="after">Business returns cover corporations, '
                 'partnerships, single-member LLCs, non-profits on Form&nbsp;990 and '
                 'fiduciary returns on Form&nbsp;1041 &mdash; the last two being work most '
                 'small offices will not take on. '
                 '<a href="services/index.html">All services &rarr;</a></p></div>')

    b += block(bh('The office', '10 Kearney Square, Lowell')
        + '<div class="copy"><p>One office, on Kearney Square in downtown Lowell. The person '
          'who answers the phone is the person who does the work.</p></div>'
        + hours_table()
        + mapblock())

    b += block(bh('Four calculators')
        + '<div class="copy"><p>Chosen for the two kinds of business above rather than to '
          'pad a list. They run in your browser and nothing you type leaves the page.</p>'
          '</div>'
        + rows(d, [('calculators/%s.html' % c['slug'], c['title'], CALC_WHY[c['slug']])
                   for c in CALCS]), plain=True)

    return page('index.html', d, 'home',
        'Mill City Accounting Services | Lowell, Massachusetts',
        'Accounting, bookkeeping, payroll and tax preparation in Lowell, Massachusetts, for '
        'quick-serve restaurant owners, rental property owners and the people who run them.',
        'An accountant on Kearney Square who has already seen your year.',
        'Mill City Accounting Services is Scott Marchlik, in Lowell, Massachusetts. Tax '
        'preparation, bookkeeping, payroll, new business consulting, tax planning and '
        'notarisation &mdash; with a decade spent on two kinds of business in particular.',
        '', False, (), b,
        [org_schema(), {'@context': 'https://schema.org', '@type': 'WebSite',
                        'name': F['name'], 'url': BASE,
                        'publisher': {'@id': BASE + '#firm'}}])


def hours_table():
    import datetime
    rows_html = ''
    for name, a, bb in HOURS:
        val = a if bb is None else '%s &ndash; %s' % (a, bb)
        rows_html += '<tr><td>%s</td><td>%s</td></tr>' % (name, val)
    return '<table class="hours">%s</table>' % rows_html


# ------------------------------------------------------- agent-written pages
def load(name):
    p = os.path.join(HERE, 'content_millcity', name)
    if not os.path.exists(p):
        raise SystemExit('missing content file: %s — the page workflow has not finished, '
                         'or that agent failed.' % p)
    return open(p, encoding='utf-8').read().strip()


PAGES = [
    dict(file='restaurants.html', path='restaurants.html', depth=0, nav='restaurants',
         title='Accounting for quick-serve restaurants | Mill City Accounting',
         desc='Meals tax, tips, the Massachusetts service rate and the new federal tip '
              'deduction — accounting in Lowell for owners of quick-serve restaurants.',
         h1='Restaurants.', eyebrow='One of two specialisms', hot=True,
         stand='Meals tax every month, tips reported on three different forms, a service '
               'rate with conditions attached, and a new federal deduction Massachusetts '
               'has not adopted. Quick-serve was Scott&rsquo;s primary clientele for '
               'a decade.',
         crumbs=(('Home', 'index.html'), ('Restaurants', None))),
    dict(file='rentals.html', path='rentals.html', depth=0, nav='rentals',
         title='Accounting for rental property owners | Mill City Accounting',
         desc='Schedule E, 27.5-year depreciation, passive loss limits, repairs versus '
              'improvements and recapture on sale — accounting in Lowell for landlords.',
         h1='Rental property.', eyebrow='One of two specialisms', hot=True,
         stand='Schedule E, a depreciation schedule that has to survive twenty-seven and '
               'a half years, losses that may not be deductible in the year you incur '
               'them, and a recapture bill waiting at the sale.',
         crumbs=(('Home', 'index.html'), ('Rental property', None))),
    dict(file='about.html', path='about.html', depth=0, nav='about',
         title='About Scott Marchlik | Mill City Accounting Services',
         desc='Scott Marchlik studied accounting at UMass Lowell, spent a decade at a '
              'Cambridge accounting firm, and started Mill City Accounting in 2018.',
         h1='Scott Marchlik.', eyebrow='Founder',
         stand='a decade at one firm, learning two kinds of business properly, then '
               'eight running his own office on Kearney Square.',
         crumbs=(('Home', 'index.html'), ('About Scott', None))),
    dict(file='contact.html', path='contact.html', depth=0, nav='contact',
         title='Visit or call | Mill City Accounting Services, Lowell MA',
         desc='10 Kearney Square #302, Lowell, Massachusetts. Open Monday to Friday, 9am to '
              '5pm, Saturday by appointment. Call (978) 979-2904 or email the office.',
         h1='Visit or call.', eyebrow='Open weekdays, 9 to 5',
         stand='One office, on Kearney Square in downtown Lowell, with the door open at '
               'stated times and one person behind it.',
         crumbs=(('Home', 'index.html'), ('Visit or call', None)), map_after=True),
    dict(file='services_index.html', path='services/index.html', depth=1, nav='services',
         title='Services | Mill City Accounting Services, Lowell MA',
         desc='Tax preparation, bookkeeping, payroll, new business consulting, tax planning '
              'and notarisation, for businesses and for individuals, in Lowell MA.',
         h1='What the office does.', eyebrow='Six services, two halves',
         stand='Business and personal, and for somebody who owns the business they are '
               'usually the same conversation.',
         crumbs=(('Home', 'index.html'), ('Services', None))),
]

SERVICE_META = {
    'tax-preparation.html': ('Tax preparation | Mill City Accounting Services',
        'Corporation, partnership, single-member LLC, non-profit and fiduciary returns, plus '
        'personal Form 1040s with every state filing they require.',
        'Tax preparation.', 'Business and personal returns &mdash; 1120, 1120-S, 1065, '
        'Schedules C and E, Form 990, Form 1041, and the 1040 they all feed into.'),
    'bookkeeping.html': ('Bookkeeping | Mill City Accounting Services',
        'Monthly, quarterly or annual compilation for small businesses in Lowell, including '
        'accounts payable and accounts receivable.',
        'Bookkeeping.', 'Monthly, quarterly or annual compilation, including accounts '
        'payable and accounts receivable &mdash; the work every other number depends on.'),
    'payroll.html': ('Payroll | Mill City Accounting Services',
        'Weekly or bi-weekly payroll processing with every required federal and state tax '
        'filing, for small employers in Lowell, Massachusetts.',
        'Payroll.', 'Weekly or bi-weekly processing, including all required federal and '
        'state tax filings &mdash; and the deposit deadlines that carry real penalties.'),
    'new-business.html': ('New business consulting | Mill City Accounting Services',
        'Forming the entity, drafting the operating agreement, annual reports and applying '
        'for tax identification numbers, for new businesses in Massachusetts.',
        'New business consulting.', 'Forming the entity, the operating agreement, the annual '
        'report and the tax identification numbers &mdash; and choosing the shape before it '
        'is expensive to change.'),
    'tax-planning.html': ('Tax planning | Mill City Accounting Services',
        'Forecasting future tax liabilities while the decisions that drive them are still '
        'open, for businesses and individuals in Lowell, Massachusetts.',
        'Tax planning.', 'A return records decisions already made. Planning is the part '
        'where they are still open, and almost all of them close on 31 December.'),
    'notary.html': ('Notarization | Mill City Accounting Services',
        'Notary services in Lowell, Massachusetts. Licensed in the Commonwealth, available '
        'during office hours at 10 Kearney Square.',
        'Notarization.', 'Licensed in the Commonwealth of Massachusetts, and available at '
        'the office during opening hours.'),
}


def build_written():
    out = []
    for p in PAGES:
        body = load(p['file'])
        if p.get('map_after'):
            body += block(bh('Finding the office') + mapblock())
        sch = [page_schema(p['h1'].rstrip('.'), p['path'], p['desc']),
               crumb_schema([(n, u or p['path']) for n, u in p['crumbs']])]
        if p['path'] == 'contact.html':
            sch.insert(0, org_schema())
        out.append(page(p['path'], p['depth'], p['nav'], p['title'], p['desc'], p['h1'],
                        p['stand'], p.get('eyebrow', ''), p.get('hot', False),
                        p['crumbs'], body, sch))
    for fn, (title, desc, h1, stand) in SERVICE_META.items():
        body = load(fn)
        name = h1.rstrip('.')
        out.append(page('services/' + fn, 1, 'services', title, desc, h1, stand,
                        'Service', False,
                        (('Home', 'index.html'), ('Services', 'services/index.html'),
                         (name, None)), body,
                        [service_schema(name, desc, 'services/' + fn),
                         crumb_schema([('Home', 'index.html'),
                                       ('Services', 'services/index.html'),
                                       (name, 'services/' + fn)])]))
    return out


def main():
    os.makedirs(os.path.join(OUT, 'css'), exist_ok=True)
    open(os.path.join(OUT, 'css', 'millcity.css'), 'w', encoding='utf-8').write(CSS)
    built = [build_home()]
    built += build_written()
    built += build_calculators()
    print('built %d pages -> %s' % (len(built), OUT))
    return built


if __name__ == '__main__':
    main()
