# -*- coding: utf-8 -*-
"""
Fitzpatrick & Goguen CPAs P.C. — Billerica, Massachusetts
=========================================================
A standalone site. It shares NO layout, CSS, component or template with any other
build in this repo. build.py, site_hickey.py, site_carella.py and site_millcity.py
are not imported and must never be.

THE DESIGN PREMISE — "Who you will actually work with"
------------------------------------------------------
This is the only firm in the batch with a real team. Five named people, four of
them with printed credentials, two of them also Investment Advisor
Representatives, and a stated set of principles. Hickey names one person, Carella
names nobody, Mill City is one man at a counter. Every one of those sites had to
work around an absence. This one has the opposite problem: it has more to show
than it currently shows.

So the roster is the front door. The people come first on the homepage, services
are tagged with who leads them, and the credential line is treated as content
rather than decoration — because for a prospect choosing an accountant, "MBA, EA,
CPA" and "CPA since 1981" is the single most persuasive thing on the page.

Concretely, and deliberately unlike anything else in this repo:
  * the team roster is the first content block, not a page buried in the nav
  * a SOFT surface logic — layered cards, 10px radii, real shadows. Hickey,
    Carella and Mill City are all flat, square and ruled.
  * Fraunces for display and Figtree for text; no Plex, no Public Sans, no Archivo
  * indigo and sand on warm paper — no claret, no pine, no vermilion, no navy/gold
  * navigation is a row of filled tabs, not a ruled band, a left rail or a
    sentence-case link row
  * the contact widget is a standing vertical rail down the LEFT edge of the
    viewport, always open, carrying the firm's real TaxDome portal link

THE HARD CONSTRAINT
-------------------
www.bgoguen.com is a CNAME to briangoguenpc.cd.taxdome.com. The firm's marketing
site and its client portal are the SAME hostname. Nothing in this build may imply
that the site can simply be swapped over, and the portal link must point at their
existing live login. Their cheaper real problem — which this build fixes — is that
the portal is not linked from anywhere on the public site.

    python3 site_goguen.py
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'bgoguen')
BASE = 'https://www.scalelocal.net/test-builds/bgoguen/'

F = dict(
    name='Fitzpatrick &amp; Goguen CPAs P.C.',
    name_plain='Fitzpatrick & Goguen CPAs P.C.',
    short='F&amp;G',
    addr='164 Concord Road',
    city='Billerica', state='MA', state_full='Massachusetts', zip='01821',
    tel='+19786674595', ph='(978) 667-4595',
    fax='(978) 667-4597',
    email='office@bgoguen.com',
    portal='https://www.bgoguen.com/login',
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Fitzpatrick+Goguen+CPAs+164+Concord+Road+Billerica+MA+01821'),
    mapembed=('https://maps.google.com/maps?q=164+Concord+Road%2C+Billerica%2C+MA+01821'
              '&t=&z=15&ie=UTF8&iwloc=&output=embed'),
)

DEMO_LEAD = 'Demonstration site.'
DEMO_BODY = ('Prepared for Fitzpatrick &amp; Goguen CPAs P.C. by ScaleLocal. Not affiliated '
             'with, authorised by, or endorsed by the firm. Reproduction or use of this site '
             'or its contents is prohibited.')

# The mark: two overlapping rounded forms — two names on one practice. Presented as
# a proposal; the firm has no existing mark.
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="6" y="14" width="30" height="36" rx="9" fill="currentColor" opacity=".38"/>'
        '<rect x="28" y="14" width="30" height="36" rx="9" fill="currentColor"/>'
        '</svg>')

FAVICON = (
    "data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2064%2064%27"
    "%3E%3Crect%20width%3D%2764%27%20height%3D%2764%27%20rx%3D%2714%27%20fill%3D%27%23443A8E%27/%3E"
    "%3Crect%20x%3D%2710%27%20y%3D%2716%27%20width%3D%2726%27%20height%3D%2732%27%20rx%3D%278%27%20fill%3D%27%23FFFFFF%27%20opacity%3D%27.45%27/%3E"
    "%3Crect%20x%3D%2728%27%20y%3D%2716%27%20width%3D%2726%27%20height%3D%2732%27%20rx%3D%278%27%20fill%3D%27%23FFFFFF%27/%3E%3C/svg%3E")

CSS = r"""
/* Fitzpatrick & Goguen CPAs P.C. — bespoke stylesheet. Shared with no other build. */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --paper:#F7F5F2;
  --card:#FFFFFF;
  --sand:#EDE7DC;
  --sand-2:#E1D8C8;
  --ink:#1E1B2E;
  --body:#454057;
  --muted:#666076;
  --line:#DCD6CC;
  --indigo:#443A8E;
  --indigo-dk:#332B6E;
  --indigo-lt:#6A5FC0;
  --deep:#25203C;
  --field:#8B8598;
  --disp:"Fraunces",Georgia,"Times New Roman",serif;
  --text:"Figtree",-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
  --rad:10px;
  --shadow:0 1px 2px rgba(30,27,46,.05),0 10px 26px rgba(30,27,46,.07);
  --shadow-lift:0 2px 6px rgba(30,27,46,.07),0 18px 42px rgba(30,27,46,.11);
}
html{-webkit-text-size-adjust:100%}
body{background:var(--paper);color:var(--body);font-family:var(--text);
  font-size:16.5px;line-height:1.7;-webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;overflow-wrap:break-word}
img{max-width:100%;display:block}
a{color:var(--indigo-dk)}
a:hover{color:var(--indigo)}
:focus-visible{outline:3px solid var(--indigo);outline-offset:3px;border-radius:4px}
h1,h2,h3{font-family:var(--disp);font-weight:600;color:var(--ink);line-height:1.13;
  font-variation-settings:"SOFT" 0,"WONK" 0,"opsz" 40}
h4{font-family:var(--text);font-weight:700;color:var(--ink)}
strong,b{font-weight:700;color:var(--ink)}
.skip{position:absolute;left:-9999px;background:var(--indigo);color:#fff;padding:11px 18px;
  z-index:99;font-weight:600;border-radius:var(--rad)}
.skip:focus{left:12px;top:12px}
.wrapper{max-width:1180px;margin:0 auto;padding:0 34px}

/* ------------------------------------------------------------ demo notice */
.demo{background:var(--deep);color:#CFCBDD;font-size:12.5px;line-height:1.5;padding:9px 0}
.demo b{color:#B9AFEA;font-weight:700}
@media print{.demo{background:#fff;color:#000}}

/* ---------------------------------------------------------------- masthead */
.top{padding:24px 0 0}
.top .wrapper{display:flex;align-items:center;justify-content:space-between;gap:26px;
  flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:13px;text-decoration:none;color:var(--ink)}
.logo .mk{display:block;width:40px;height:40px;flex:0 0 40px;color:var(--indigo)}
.logo .mk svg{width:100%;height:100%;display:block}
.logo .wm{font-family:var(--disp);font-size:20.5px;font-weight:600;line-height:1.12;
  letter-spacing:-.01em}
.logo .wm span{display:block;font-family:var(--text);font-size:11.5px;font-weight:600;
  color:var(--muted);margin-top:4px;letter-spacing:.04em;text-transform:uppercase}
.logo:hover .wm{color:var(--indigo-dk)}
.topcall{font-size:14.5px;color:var(--muted);text-align:right;line-height:1.5}
.topcall a{font-family:var(--disp);font-size:20px;font-weight:600;color:var(--ink);
  text-decoration:none;display:block}
.topcall a:hover{color:var(--indigo-dk)}

/* nav: filled tabs. Not a ruled band, not a rail, not a sentence-case row. */
.tabs{padding:20px 0 4px}
.tabs .wrapper{display:flex;gap:9px;flex-wrap:wrap}
.tabs a{font-size:14.5px;font-weight:600;color:var(--body);text-decoration:none;
  padding:9px 16px;border-radius:999px;background:transparent;line-height:1.2}
.tabs a:hover{background:var(--sand);color:var(--ink)}
.tabs a[aria-current]{background:var(--indigo);color:#fff}
.tabs a.portal{color:var(--indigo-dk);border:1.5px solid var(--indigo-lt)}
.tabs a.portal:hover{background:var(--indigo);color:#fff;border-color:var(--indigo)}

/* ================================================== THE CONTACT WIDGET
   A standing rail down the LEFT edge of the viewport. Always open — nothing to
   click before it can be used. It carries the firm's real TaxDome portal login,
   which their current public site links from nowhere. Static: no script, no
   network call, no third party. Below 1180px it becomes a sticky action row
   under the header rather than a bottom bar. */
.reachrail{display:none}
@media (min-width:1180px){
  body{padding-left:96px}
  .demo .wrapper,.top .wrapper,.tabs .wrapper,main .wrapper,.foot .wrapper{
    max-width:1120px}
  .reachrail{display:flex;position:fixed;left:0;top:0;bottom:0;width:96px;z-index:60;
    flex-direction:column;align-items:stretch;justify-content:center;gap:6px;
    background:var(--card);border-right:1px solid var(--line);padding:14px 10px}
  .reachrail .rl{font-family:var(--text);font-size:9.5px;font-weight:700;
    letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:center;
    padding-bottom:8px}
  .reachrail a{display:block;text-align:center;text-decoration:none;color:var(--body);
    padding:11px 5px;border-radius:8px;line-height:1.25}
  .reachrail a .ic{display:block;width:22px;height:22px;margin:0 auto 6px;color:var(--indigo)}
  .reachrail a .ic svg{width:100%;height:100%;display:block}
  .reachrail a .lb{display:block;font-size:11.5px;font-weight:700;color:var(--ink)}
  .reachrail a:hover{background:var(--sand)}
  .reachrail a:hover .lb{color:var(--indigo-dk)}
  .reachrail a.key{background:var(--indigo)}
  .reachrail a.key .lb{color:#fff}
  .reachrail a.key .ic{color:#fff}
  .reachrail a.key:hover{background:var(--indigo-dk)}
}
.reachrow{position:sticky;top:0;z-index:55;background:var(--paper);
  border-bottom:1px solid var(--line);padding:10px 0}
.reachrow .wrapper{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.reachrow a{display:block;text-align:center;text-decoration:none;padding:9px 6px;
  border:1.5px solid var(--line);border-radius:8px;background:var(--card);line-height:1.3}
.reachrow a .lb{display:block;font-size:13px;font-weight:700;color:var(--ink)}
.reachrow a .sb{display:block;font-size:11px;color:var(--muted);margin-top:1px}
.reachrow a.key{background:var(--indigo);border-color:var(--indigo)}
.reachrow a.key .lb{color:#fff}
.reachrow a.key .sb{color:#D5CFF2}
@media (min-width:1180px){.reachrow{display:none}}

/* ------------------------------------------------------------------- page */
main{padding:36px 0 0}
.head{max-width:760px}
.pill{display:inline-block;background:var(--sand);color:var(--ink);font-size:12.5px;
  font-weight:700;padding:5px 13px;border-radius:999px;margin-bottom:16px}
.pill.ind{background:var(--indigo);color:#fff}
h1{font-size:clamp(31px,4.3vw,48px);letter-spacing:-.018em}
.sub{margin-top:15px;font-size:19px;line-height:1.6;color:var(--body);max-width:58ch}
.trail{font-size:13.5px;color:var(--muted);margin-bottom:13px}
.trail a{color:var(--muted);text-decoration:none}
.trail a:hover{color:var(--indigo-dk);text-decoration:underline}
.trail em{font-style:normal;padding:0 7px;color:var(--line)}

/* card: the site's structural unit. Soft, layered, shadowed. */
.card{margin-top:30px;background:var(--card);border-radius:var(--rad);padding:30px 32px;
  box-shadow:var(--shadow)}
.card.sand{background:var(--sand)}
.card.deep{background:var(--deep);color:#CFCBDD}
.card.deep h2,.card.deep h3{color:#fff}
.card.deep a{color:#BCB2F0}
.card.deep a:hover{color:#fff}
.card.bare{background:transparent;box-shadow:none;padding:0}
h2{font-size:27px;letter-spacing:-.012em}
h3{font-size:19px;letter-spacing:-.006em}
.card > h2:first-child,.card > .ch:first-child{margin-top:0}
.ch{display:flex;align-items:baseline;justify-content:space-between;gap:18px;flex-wrap:wrap}
.ch .lbl{font-size:12.5px;font-weight:700;color:var(--muted)}
.text p{margin-top:14px;max-width:70ch}
.text h3{margin-top:26px}
.text h3 + p{margin-top:8px}
.text h4{margin-top:20px;font-size:15px}
.text ul,.text ol{margin-top:13px;padding-left:0;list-style:none;max-width:70ch}
.text li{position:relative;padding-left:25px;margin-top:9px}
.text ul li::before{content:"";position:absolute;left:2px;top:11px;width:8px;height:8px;
  border-radius:50%;background:var(--indigo-lt)}
.text ol{counter-reset:c}
.text ol li{counter-increment:c}
.text ol li::before{content:counter(c);position:absolute;left:0;top:2px;width:18px;height:18px;
  border-radius:50%;background:var(--indigo);color:#fff;font-size:11px;font-weight:700;
  display:flex;align-items:center;justify-content:center;font-family:var(--text)}
.text .close{margin-top:20px;font-size:14.5px;color:var(--muted)}

/* the roster — the site's signature block */
.roster{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
  gap:16px}
.person{display:block;text-decoration:none;background:var(--card);border-radius:var(--rad);
  padding:22px 22px 20px;box-shadow:var(--shadow);color:var(--body)}
.person:hover{box-shadow:var(--shadow-lift);transform:translateY(-2px)}
.person{transition:box-shadow .18s ease,transform .18s ease}
@media (prefers-reduced-motion:reduce){.person{transition:none}.person:hover{transform:none}}
.person .face{width:96px;height:96px;border-radius:50%;object-fit:cover;
  display:block;margin-bottom:14px;background:var(--sand-2);
  box-shadow:0 0 0 3px var(--card),0 0 0 5px var(--sand-2)}
.person:hover .face{box-shadow:0 0 0 3px var(--card),0 0 0 5px var(--indigo)}
.mem{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
  gap:14px;margin-top:18px}
.mem li{background:var(--sand);border-radius:var(--rad);padding:14px 16px}
.mem b{display:block;font-family:var(--disp);font-size:17px;font-weight:600;color:var(--indigo)}
.mem span{display:block;margin-top:3px;font-size:13.5px;color:var(--muted);line-height:1.45}
.person .nm{font-family:var(--disp);font-size:19px;font-weight:600;color:var(--ink);
  line-height:1.2}
.person .cr{display:block;margin-top:5px;font-size:12.5px;font-weight:700;
  color:var(--indigo-dk);letter-spacing:.02em}
.person .ro{display:block;margin-top:7px;font-size:14px;color:var(--muted);line-height:1.45}
.person .more{display:block;margin-top:13px;font-size:13.5px;font-weight:700;
  color:var(--indigo-dk)}
.person:hover .more{color:var(--indigo)}

/* principles — three tinted panels */
.trio{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
  gap:16px}
.trio div{background:var(--sand);border-radius:var(--rad);padding:22px 22px}
.trio h3{font-size:17.5px}
.trio p{margin-top:8px;font-size:14.5px;line-height:1.6;color:var(--body)}

/* link rows */
.list{margin-top:20px;display:grid;gap:10px}
.list a,.list .li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;
  align-items:center;background:var(--card);border-radius:var(--rad);padding:17px 20px;
  text-decoration:none;color:var(--body);box-shadow:0 1px 2px rgba(30,27,46,.05)}
.list a:hover{box-shadow:var(--shadow)}
.list .t{font-family:var(--disp);font-size:18px;font-weight:600;color:var(--ink);line-height:1.25}
.list .d{display:block;margin-top:4px;font-size:14.5px;color:var(--body);line-height:1.55;
  max-width:62ch}
.list .by{font-size:12.5px;font-weight:700;color:var(--indigo-dk);white-space:nowrap;
  text-align:right}
.list a:hover .t{color:var(--indigo-dk)}

/* facts */
.facts{margin-top:22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));
  gap:14px}
.facts div{background:var(--sand);border-radius:var(--rad);padding:18px 20px}
.card.deep .facts div{background:#312A4F}
.facts .fg{display:block;font-family:var(--disp);font-size:31px;font-weight:600;
  color:var(--indigo-dk);line-height:1.08}
.card.deep .facts .fg{color:#BCB2F0}
.facts .fc{display:block;margin-top:5px;font-size:13px;color:var(--muted);line-height:1.45}
.card.deep .facts .fc{color:#A9A3C0}

/* aside */
.aside{margin-top:24px;border-left:4px solid var(--indigo);background:var(--card);
  border-radius:0 var(--rad) var(--rad) 0;padding:18px 22px;box-shadow:var(--shadow)}
.aside .al{font-size:12.5px;font-weight:700;color:var(--indigo-dk);margin-bottom:6px}
.aside p{font-size:15px;line-height:1.62}
.aside p + p{margin-top:10px}

/* tables */
.tbl{margin-top:18px;overflow-x:auto;-webkit-overflow-scrolling:touch}
table.data{border-collapse:separate;border-spacing:0;width:100%;min-width:460px;font-size:15px}
table.data th{background:var(--sand);color:var(--ink);font-size:12.5px;font-weight:700;
  text-align:left;padding:11px 16px}
table.data th:first-child{border-radius:var(--rad) 0 0 0}
table.data th:last-child{border-radius:0 var(--rad) 0 0}
table.data td{padding:11px 16px;border-bottom:1px solid var(--line);vertical-align:top;
  line-height:1.5}
table.data tr:last-child td{border-bottom:0}
table.data td.v{font-weight:700;color:var(--ink);white-space:nowrap}

/* map */
.map{margin-top:20px;border-radius:var(--rad);overflow:hidden;box-shadow:var(--shadow)}
.map iframe{width:100%;height:320px;border:0;display:block}
.map + .mc{margin-top:10px;font-size:13px;color:var(--muted)}

/* footer */
.foot{margin-top:56px;background:var(--deep);color:#B3AEC6;padding:40px 0 30px}
.foot a{color:#D2CEE4;text-decoration:none}
.foot a:hover{color:#fff;text-decoration:underline}
.foot .fg{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:34px}
.foot .fh{color:#fff;font-size:13px;font-weight:700;margin-bottom:11px}
.foot .fw{font-family:var(--disp);font-size:18px;color:#fff;font-weight:600;margin-bottom:9px}
.foot ul{list-style:none;font-size:14.5px;line-height:2}
.foot .fine{margin-top:30px;padding-top:20px;border-top:1px solid #3B3458;font-size:12.5px;
  line-height:1.6;color:#8D87A5}

/* ========================================================== responsive */
@media (max-width:900px){
  .wrapper{padding:0 20px}
  .foot .fg{grid-template-columns:minmax(0,1fr);gap:24px}
  .card{padding:24px 22px}
  .top .wrapper{gap:14px}
  .topcall{text-align:left}
  .reachrow .wrapper{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:520px){
  .out .ov{font-size:35px}
  .list a,.list .li{grid-template-columns:minmax(0,1fr)}
  .list .by{text-align:left}
}
@media print{.demo,.tabs,.reachrail,.reachrow,.map{display:none}body{padding-left:0}}
"""

# ==========================================================================
NAV = [
    ('team/index.html',     'The team',   'team'),
    ('services/index.html', 'Services',   'services'),
    ('guides/index.html',   'Guides',     'guides'),
    ('about.html',          'The firm',   'about'),
    ('contact.html',        'Contact',    'contact'),
]

# Every credential below is printed on the firm's own team page. Dana, Sean and
# Monirina carry none, and none is added.
TEAM = [
    dict(slug='thomas-l-fitzpatrick', name='Thomas L. Fitzpatrick IV', initials='TF',
         cred='MBA, EA, CPA', role='President &amp; Shareholder', key=True,
         alt='Thomas L. Fitzpatrick IV, President and Shareholder'),
    dict(slug='brian-d-goguen', name='Brian D. Goguen', initials='BG',
         cred='MST, CPA', role='Certified Public Accountant &mdash; licensed since 1981',
         key=True, alt='Brian D. Goguen, Certified Public Accountant'),
    dict(slug='dana-reardon', name='Dana Reardon', initials='DR', cred='',
         role='Accountant &mdash; joined the firm in 2000', key=False,
         alt='Dana Reardon, Accountant'),
    dict(slug='sean-malone', name='Sean Malone', initials='SM', cred='',
         role='Accountant &mdash; joined the firm in 2000', key=False,
         alt='Sean Malone, Accountant'),
    dict(slug='monirina-kim', name='Monirina Kim', initials='MK', cred='',
         role='Firm administration &mdash; joined the firm in 2022', key=False,
         alt='Monirina Kim, firm administration'),
]

# Exactly the three headings the firm publishes, including the non-profit scope the
# research file dropped. Nothing is added.
SERVICES = [
    ('services/personal-tax.html', 'Personal income tax planning and preparation',
     'Individual returns, and the conversations that decide the number before the year '
     'closes rather than after.'),
    ('services/business-tax.html', 'Small business and non-profit tax',
     'Entity returns for small businesses and for non-profits, and the owner&rsquo;s '
     'return that depends on them.'),
    ('services/bookkeeping.html', 'Bookkeeping',
     'The monthly discipline underneath every other number the firm produces.'),
]

# Stated on every page of the firm's own site under "Proud Members of:".
# Stated on every page of the firm's own site under "Proud Members of:". All three
# are firm-level and printed, so all three are carried; nothing else is added.
MEMBERSHIPS = [('American Institute of Certified Public Accountants', 'AICPA'),
               ('National Association of Enrolled Agents', 'NAEA'),
               ('Massachusetts Association of Accountants', 'MAA')]

ICONS = dict(
    call='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    mail='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    portal='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
    book='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
)


def rel(depth, target):
    if target.startswith(('http', 'mailto:', 'tel:', '#')):
        return target
    return ('../' * depth) + target


def esc(s):
    return H.escape(s, quote=True)


def tabs_html(depth, active):
    out = ['<div class="tabs"><div class="wrapper">']
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        out.append('<a href="%s"%s>%s</a>' % (rel(depth, href), cur, label))
    out.append('<a class="portal" href="%s" target="_blank" rel="noopener">Client portal</a>'
               % F['portal'])
    out.append('</div></div>')
    return ''.join(out)


def reach(depth):
    """THE CONTACT WIDGET. A standing rail down the left edge on wide viewports,
    a sticky action row under the header below that. Always open. Carries the
    firm's real TaxDome portal login — which their current public site links from
    nowhere at all. No script, no network call, no third party."""
    acts = [
        ('tel:' + F['tel'], 'call', 'Call', F['ph'], False),
        ('mailto:' + F['email'], 'mail', 'Email', 'Write to the firm', False),
        (F['portal'], 'portal', 'Client portal', 'Existing clients', True),
        (rel(depth, 'contact.html#appointment'), 'book', 'Book a time', 'Arrange a meeting', False),
    ]
    rail = ['<aside class="reachrail" data-contact-widget aria-label="Contact the firm">'
            '<div class="rl">Reach us</div>']
    row = ['<div class="reachrow" data-contact-widget role="group" aria-label="Contact the firm">'
           '<div class="wrapper">']
    for href, ic, lab, sub, ext in acts:
        e = ' target="_blank" rel="noopener"' if ext else ''
        k = ' key' if ic == 'portal' else ''
        rail.append('<a class="%s" href="%s"%s><span class="ic">%s</span>'
                    '<span class="lb">%s</span></a>' % (k.strip(), href, e, ICONS[ic], lab))
        row.append('<a class="%s" href="%s"%s><span class="lb">%s</span>'
                   '<span class="sb">%s</span></a>' % (k.strip(), href, e, lab, sub))
    rail.append('</aside>')
    row.append('</div></div>')
    return ''.join(rail), ''.join(row)


def footer(depth):
    svc = ''.join('<li><a href="%s">%s</a></li>' % (rel(depth, h), t) for h, t, _ in SERVICES)
    ppl = ''.join('<li><a href="team/%s.html">%s</a></li>' % (p['slug'], p['name'])
                  for p in TEAM)
    ppl = ppl.replace('href="team/', 'href="' + rel(depth, 'team/'))
    return (
        '<footer class="foot"><div class="wrapper"><div class="fg">'
        '<div><div class="fw">%s</div>'
        '<p>%s<br>%s, %s %s<br><a href="tel:%s">%s</a><br>'
        '<a href="mailto:%s">%s</a></p></div>'
        '<div><div class="fh">Services</div><ul>%s</ul></div>'
        '<div><div class="fh">The team</div><ul>%s</ul></div>'
        '</div><p class="fine">%s %s</p></div></footer>'
    ) % (F['name'], F['addr'], F['city'], F['state'], F['zip'], F['tel'], F['ph'],
         F['email'], F['email'], svc, ppl, DEMO_LEAD, DEMO_BODY)


def trail_html(depth, crumbs):
    if not crumbs:
        return ''
    b = []
    for label, href in crumbs:
        b.append('<a href="%s">%s</a>' % (rel(depth, href), label) if href
                 else '<span>%s</span>' % label)
    return '<div class="trail">%s</div>' % '<em>/</em>'.join(b)


def page(path, depth, nav, title, desc, h1, sub='', pill='', pill_ind=False,
         crumbs=(), body='', schema=(), tail=''):
    url = BASE + ('' if path == 'index.html' else path)
    ld = ''.join('<script type="application/ld+json">%s</script>'
                 % json.dumps(s, separators=(',', ':')) for s in schema)
    rail, row = reach(depth)
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<title>%(t)s</title><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="description" content="%(d)s">'
        '<meta name="robots" content="noindex, nofollow">'
        '<meta name="googlebot" content="noindex, nofollow">'
        '<link rel="canonical" href="%(u)s"><meta name="theme-color" content="#443A8E">'
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="%(n)s">'
        '<meta property="og:title" content="%(t)s">'
        '<meta property="og:description" content="%(d)s">'
        '<meta property="og:url" content="%(u)s">'
        '<meta property="og:image" content="%(b)sog.png">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Fitzpatrick &amp; Goguen CPAs P.C., Billerica, Massachusetts">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="%(t)s">'
        '<meta name="twitter:description" content="%(d)s">'
        '<meta name="twitter:image" content="%(b)sog.png">'
        '<link rel="apple-touch-icon" href="%(a)s">'
        '<link rel="icon" type="image/svg+xml" href="%(f)s">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="%(c)s">%(ld)s</head>'
    ) % dict(t=esc(title), d=esc(desc), u=url, n=esc(F['name_plain']), b=BASE,
             c=rel(depth, 'css/fg.css'), f=FAVICON,
             a=rel(depth, 'apple-touch-icon.png'), ld=ld)
    doc = (
        head + '<body>'
        '<a class="skip" href="#main">Skip to content</a>'
        + rail +
        '<div class="demo"><div class="wrapper"><b>' + DEMO_LEAD + '</b> ' + DEMO_BODY + '</div></div>'
        '<header class="top"><div class="wrapper">'
        '<a class="logo" href="' + rel(depth, 'index.html') + '">'
        '<span class="mk">' + MARK + '</span>'
        '<span class="wm">Fitzpatrick &amp; Goguen<span>CPAs P.C. &middot; Billerica, MA</span></span></a>'
        '<div class="topcall">Speak to the firm<a href="tel:' + F['tel'] + '">' + F['ph'] + '</a></div>'
        '</div></header>'
        + tabs_html(depth, nav) + row +
        '<main id="main"><div class="wrapper">'
        '<div class="head">' + trail_html(depth, crumbs)
        + ('<span class="pill%s">%s</span>' % (' ind' if pill_ind else '', pill) if pill else '')
        + '<h1>' + h1 + '</h1>'
        + ('<p class="sub">' + sub + '</p>' if sub else '') + '</div>'
        + body + '</div></main>'
        + footer(depth) + tail + '</body></html>'
    )
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(doc)
    return path


# ------------------------------------------------------------------ schema
def org_schema():
    return {'@context': 'https://schema.org', '@type': 'AccountingService',
            '@id': BASE + '#firm', 'name': F['name_plain'], 'url': BASE,
            'email': F['email'], 'telephone': F['ph'],
            'address': {'@type': 'PostalAddress', 'streetAddress': F['addr'],
                        'addressLocality': F['city'], 'addressRegion': F['state'],
                        'postalCode': F['zip'], 'addressCountry': 'US'},
            'employee': [{'@type': 'Person', 'name': p['name'],
                          'jobTitle': re.sub(r'<[^>]+>|&[a-z]+;', ' ', p['role']).strip()}
                         for p in TEAM],
            'hasMap': F['maps']}


def crumb_schema(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n,
                                 'item': BASE + (u if u != 'index.html' else '')}
                                for i, (n, u) in enumerate(items)]}


def page_schema(name, path, desc):
    return {'@context': 'https://schema.org', '@type': 'WebPage', 'name': name,
            'description': desc, 'url': BASE + ('' if path == 'index.html' else path),
            'isPartOf': {'@id': BASE + '#firm'}}


def person_schema(p):
    return {'@context': 'https://schema.org', '@type': 'Person', 'name': p['name'],
            'jobTitle': re.sub(r'<[^>]+>|&[a-z]+;', ' ', p['role']).strip(),
            'worksFor': {'@id': BASE + '#firm'},
            'url': BASE + 'team/' + p['slug'] + '.html'}


def service_schema(name, desc, path):
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': name,
            'description': desc, 'url': BASE + path, 'provider': {'@id': BASE + '#firm'},
            'areaServed': {'@type': 'State', 'name': 'Massachusetts'}}


def faq_schema(pairs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                           for q, a in pairs]}


# --------------------------------------------------------------- components
def card(inner, kind=''):
    return '<section class="card%s">%s</section>' % ((' ' + kind) if kind else '', inner)


def ch(title, lbl=''):
    return ('<div class="ch"><h2>%s</h2>%s</div>'
            % (title, '<span class="lbl">%s</span>' % lbl if lbl else ''))


def roster(depth, people=None):
    """Photographs supplied by the firm. Where a site has real faces, use them —
    initials were a placeholder for the absence of any."""
    out = ['<div class="roster">']
    for p in (people or TEAM):
        out.append('<a class="person" href="%s">'
                   '<img class="face" src="%s" srcset="%s 1x, %s 2x" width="640" height="640" '
                   'alt="%s" loading="lazy" decoding="async">'
                   '<span class="nm">%s</span>%s<span class="ro">%s</span>'
                   '<span class="more">Read more &rarr;</span></a>'
                   % (rel(depth, 'team/%s.html' % p['slug']),
                      rel(depth, 'img/team/%s.jpg' % p['slug']),
                      rel(depth, 'img/team/%s.jpg' % p['slug']),
                      rel(depth, 'img/team/%s@2x.jpg' % p['slug']),
                      p['alt'], p['name'],
                      '<span class="cr">%s</span>' % p['cred'] if p['cred'] else '',
                      p['role']))
    out.append('</div>')
    return ''.join(out)


def memberships_html():
    return ('<ul class="mem">%s</ul>'
            % ''.join('<li><b>%s</b><span>%s</span></li>' % (ab, full)
                      for full, ab in MEMBERSHIPS))


def lst(depth, items):
    """items: (href|None, title, detail, right)"""
    out = ['<div class="list">']
    for it in items:
        href, t, d = it[0], it[1], it[2]
        r = it[3] if len(it) > 3 else ''
        inner = ('<span><span class="t">%s</span><span class="d">%s</span></span>%s'
                 % (t, d, '<span class="by">%s</span>' % r if r else '<span></span>'))
        out.append('<a href="%s">%s</a>' % (rel(depth, href), inner) if href
                   else '<div class="li">%s</div>' % inner)
    out.append('</div>')
    return ''.join(out)


def facts(items):
    return ('<div class="facts">%s</div>'
            % ''.join('<div><span class="fg">%s</span><span class="fc">%s</span></div>'
                      % (a, b) for a, b in items))


def aside(label, *paras):
    return ('<div class="aside"><div class="al">%s</div>%s</div>'
            % (label, ''.join('<p>%s</p>' % p for p in paras)))


def table(headers, rows_):
    th = ''.join('<th>%s</th>' % h for h in headers)
    tr = ''.join('<tr>%s</tr>' % ''.join(
        '<td%s>%s</td>' % (' class="v"' if isinstance(c, tuple) else '',
                           c[0] if isinstance(c, tuple) else c) for c in r) for r in rows_)
    return ('<div class="tbl"><table class="data"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (th, tr))


def mapblock():
    return ('<div class="map"><iframe title="Interactive Google map showing Fitzpatrick '
            '&amp; Goguen CPAs at 164 Concord Road, Billerica, Massachusetts" src="%s" '
            'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen>'
            '</iframe></div><p class="mc">Pan, zoom, or <a href="%s" target="_blank" '
            'rel="noopener">open the map full screen</a> for directions.</p>'
            % (F['mapembed'], F['maps']))


def trio(items):
    return ('<div class="trio">%s</div>'
            % ''.join('<div><h3>%s</h3><p>%s</p></div>' % (a, b) for a, b in items))


def load(name):
    p = os.path.join(HERE, 'content_goguen', name)
    if not os.path.exists(p):
        raise SystemExit('missing content file: %s' % p)
    return open(p, encoding='utf-8').read().strip()

# ==========================================================================


def build_home():
    d = 0
    b = card(ch('The people who will do your work', 'Billerica, since 1981')
             + '<div class="text"><p>A Certified Public Accountant licensed since 1981, with '
               'a master&rsquo;s degree in taxation. A president who holds an MBA, an Enrolled '
               'Agent licence and a CPA licence at the same time. Two accountants who have '
               'been at this firm since 2000. Most accounting websites tell you what a firm '
               'does; this one starts with who does it, because that is the question a client '
               'is actually asking.</p></div>'
             + roster(d)
             + '<div class="text"><p class="close">The firm is a member of the American '
               'Institute of CPAs, the National Association of Enrolled Agents and the '
               'Massachusetts Association of Accountants. '
               '<a href="team/index.html">Meet the team &rarr;</a></p></div>')
    b += card(ch('What we do')
              + lst(d, [(h, t, x, 'Thomas &amp; Brian' if 'tax' in h else 'The firm')
                        for h, t, x in SERVICES])
              + '<div class="text"><p class="close">Non-profit returns are part of the second '
                'one &mdash; work a good many firms this size will not take on. '
                '<a href="services/index.html">All three services &rarr;</a></p></div>')
    b += card(ch('What the firm says it stands for')
              + trio([('Trust', 'The firm&rsquo;s own heading is &ldquo;Partners You Can '
                                'Trust&rdquo;. In practice that means the person you meet is '
                                'the person who does the work.'),
                      ('Independence', 'Independence is a professional requirement before it '
                                       'is a value. It is what makes an opinion worth '
                                       'anything.'),
                      ('Confidentiality', 'For a CPA this is an enforceable professional '
                                          'obligation rather than an internal policy, and it '
                                          'covers the fact of the engagement as well as its '
                                          'contents.')]),
              'bare')
    b += card(ch('Already a client?')
              + '<div class="text"><p>The firm runs a secure client portal for documents, '
                'signatures, messages and paying an invoice. It is the right way to send '
                'anything with a Social Security number or an account number on it.</p>'
                '<p><a href="%s" target="_blank" rel="noopener">Open the client portal '
                '&rarr;</a> &nbsp;&middot;&nbsp; <a href="client-portal.html">What the portal '
                'is for</a></p></div>' % F['portal'], 'deep')
    b += card(ch('Where the firm is', 'Billerica, Massachusetts') + mapblock())
    b += card(ch('Worth reading first')
              + lst(d, [('guides/what-to-bring.html', 'What to bring',
                         'What to gather before an appointment, by category.'),
                        ('guides/cpa-and-ea.html', 'What the letters actually mean',
                         'CPA, EA and MST &mdash; and the one thing most people get wrong '
                         'about representation rights.'),
                        ('client-portal.html', 'The client portal',
                         'The TaxDome portal the firm already runs &mdash; and how to '
                         'sign in to it.')]), 'bare')
    return page('index.html', d, 'home',
        'Fitzpatrick &amp; Goguen CPAs P.C. | Billerica, Massachusetts',
        'A Billerica accounting firm: two CPAs, an Enrolled Agent and a team that stays. '
        'Bookkeeping, personal income tax, and small business and non-profit tax.',
        'You can see who will do your work.',
        'Fitzpatrick &amp; Goguen CPAs P.C. is a family business in Billerica providing '
        'personalized accounting, tax and bookkeeping services to clients across the '
        'Merrimack Valley and beyond.',
        'Helping you achieve your ideal life', True, (), b,
        [org_schema(), {'@context': 'https://schema.org', '@type': 'WebSite',
                        'name': F['name_plain'], 'url': BASE,
                        'publisher': {'@id': BASE + '#firm'}}])


PAGES = [
    dict(file='team_index.html', path='team/index.html', depth=1, nav='team',
         title='The team | Fitzpatrick &amp; Goguen CPAs P.C.',
         desc='Thomas L. Fitzpatrick IV MBA EA CPA, Brian D. Goguen MST CPA, Dana Reardon, '
              'Sean Malone and Monirina Kim &mdash; the team at Billerica.',
         h1='Serious credentials, and the same faces every year.', pill='The team',
         sub='A CPA licensed since 1981 with a master&rsquo;s in taxation. A president who '
             'holds an MBA, an Enrolled Agent licence and a CPA licence together &mdash; a '
             'combination you rarely find in one person, let alone in a firm this size. And '
             'two accountants who have stayed since 2000. You will know exactly who is doing '
             'your work before you hand anything over.',
         crumbs=(('Home', 'index.html'), ('The team', None)), roster_after=True),
    dict(file='services_index.html', path='services/index.html', depth=1, nav='services',
         title='Services | Fitzpatrick &amp; Goguen CPAs P.C.',
         desc='Bookkeeping, personal income tax planning and preparation, and small business '
              'and non-profit tax planning and preparation, in Billerica, Massachusetts.',
         h1='Three things, done properly.', pill='What we do',
         sub='Bookkeeping, personal tax, and tax for small businesses and non-profits '
             '&mdash; and for somebody who owns a business, the last two are one problem.',
         crumbs=(('Home', 'index.html'), ('Services', None))),
    dict(file='guides_index.html', path='guides/index.html', depth=1, nav='guides',
         title='Guides | Fitzpatrick &amp; Goguen CPAs P.C.',
         desc='Two plain guides: what to gather before a tax appointment, and what the '
              'letters after an accountant&rsquo;s name actually mean.',
         h1='Two guides.', pill='Before you engage anyone',
         sub='The two things people ask before they choose an accountant.',
         crumbs=(('Home', 'index.html'), ('Guides', None))),
    dict(file='about.html', path='about.html', depth=0, nav='about',
         title='The firm | Fitzpatrick &amp; Goguen CPAs P.C.',
         desc='A family business in Billerica providing personalized accounting, tax and '
              'bookkeeping services across the Merrimack Valley and beyond.',
         h1='Partners you can trust.', pill='The firm',
         sub='A family business providing personalized accounting, tax, bookkeeping and '
             'other services to a broad range of clients across the Merrimack Valley '
             'and beyond.',
         crumbs=(('Home', 'index.html'), ('The firm', None))),
    dict(file='contact.html', path='contact.html', depth=0, nav='contact',
         title='Contact | Fitzpatrick &amp; Goguen CPAs P.C., Billerica MA',
         desc='164 Concord Road, Billerica, Massachusetts. Telephone (978) 667-4595, or '
              'write to the office. Existing clients can use the secure client portal.',
         h1='Speak to the firm.', pill='Contact',
         sub='One office, on Concord Road in Billerica. A call or an email &mdash; and the '
             'portal for anything with a number on it that matters.',
         crumbs=(('Home', 'index.html'), ('Contact', None)), map_after=True),
    dict(file='client-portal.html', path='client-portal.html', depth=0, nav='contact',
         title='The client portal | Fitzpatrick &amp; Goguen CPAs P.C.',
         desc='How existing clients send documents, sign returns, message the firm and pay '
              'an invoice through the secure client portal.',
         h1='The client portal.', pill='For existing clients',
         sub='Documents, signatures, messages and invoices, in one place that is safe to '
             'send a Social Security number through.',
         crumbs=(('Home', 'index.html'), ('The client portal', None))),
]

PERSON_META = {
    'thomas-l-fitzpatrick.html': ('Thomas L. Fitzpatrick IV, MBA, EA, CPA'),
    'brian-d-goguen.html': ('Brian D. Goguen, MST, CPA'),
    'dana-reardon.html': ('Dana Reardon'),
    'sean-malone.html': ('Sean Malone'),
    'monirina-kim.html': ('Monirina Kim'),
}

SERVICE_META = {
    'personal-tax.html': ('Personal income tax | Fitzpatrick &amp; Goguen CPAs P.C.',
        'Personal income tax planning and preparation for individuals in Billerica and '
        'across the Merrimack Valley, federal and Massachusetts.',
        'Personal income tax.', 'Planning and preparation. One of them records decisions '
        'already made; the other happens while they are still open.'),
    'business-tax.html': ('Small business and non-profit tax | Fitzpatrick &amp; Goguen',
        'Tax planning and preparation for small businesses and for non-profit '
        'organisations in Billerica, Massachusetts.',
        'Small business and non-profit tax.', 'How a business is organised decides which '
        'return it files and when &mdash; and a non-profit return is a public document, '
        'which changes how the year should be kept.'),
    'bookkeeping.html': ('Bookkeeping | Fitzpatrick &amp; Goguen CPAs P.C.',
        'Monthly bookkeeping for small businesses in Billerica, Massachusetts &mdash; the '
        'work every other number the firm produces depends on.',
        'Bookkeeping.', 'The monthly discipline underneath everything else, and the thing '
        'that decides whether a return takes three hours or three days.'),
}

GUIDE_META = {
    'what-to-bring.html': ('What to bring | Fitzpatrick &amp; Goguen CPAs P.C.',
        'What to gather before a tax appointment, by category: prior returns, income forms, '
        'deductions, the business file, and what changed during the year.',
        'What to bring.', 'More is better than less, and a gap is worth mentioning at the '
        'start rather than working around.'),
    'cpa-and-ea.html': ('CPA, EA and MST | Fitzpatrick &amp; Goguen CPAs P.C.',
        'What the letters after an accountant&rsquo;s name mean, and the one thing most '
        'people get wrong about who may represent you before the IRS.',
        'What the letters mean.', 'CPA, EA, MST &mdash; three different things, and the '
        'difference is worth ten minutes before you choose anyone.'),
}


def build_written():
    out = []
    for p in PAGES:
        body = load(p['file'])
        if p.get('roster_after'):
            body = (card(ch('Who you would be working with') + roster(p['depth']), 'bare')
                    + card(ch('The firm belongs to', 'All three, firm-level')
                           + memberships_html()
                           + '<div class="text"><p class="close">Membership means continuing '
                             'education requirements and a code of conduct with a '
                             'disciplinary process attached &mdash; not a badge bought for '
                             'a website.</p></div>')
                    + body)
        if p.get('map_after'):
            body += card(ch('Finding the office') + mapblock())
        sch = [page_schema(re.sub(r'<[^>]+>', '', p['h1']).rstrip('.'), p['path'], p['desc']),
               crumb_schema([(n, u or p['path']) for n, u in p['crumbs']])]
        if p['path'] == 'contact.html':
            sch.insert(0, org_schema())
        out.append(page(p['path'], p['depth'], p['nav'], p['title'], p['desc'], p['h1'],
                        p['sub'], p.get('pill', ''), p.get('pill_ind', False),
                        p['crumbs'], body, sch))
    for pr in TEAM:
        fn = pr['slug'] + '.html'
        body = load(fn)
        full = PERSON_META[fn]
        title = '%s | Fitzpatrick &amp; Goguen CPAs P.C.' % pr['name']
        desc = ('%s at Fitzpatrick &amp; Goguen CPAs P.C. in Billerica, Massachusetts. '
                '%s' % (full, re.sub(r'&[a-z]+;', '', pr['role'])))[:174]
        if len(desc) < 72:
            desc = (desc + ' Part of a five-person firm serving the Merrimack Valley.')[:174]
        out.append(page('team/%s.html' % pr['slug'], 1, 'team', title, desc,
                        pr['name'] + '.', re.sub(r'&mdash;', '&mdash;', pr['role']),
                        pr['cred'] or 'The team', bool(pr['cred']),
                        (('Home', 'index.html'), ('The team', 'team/index.html'),
                         (pr['name'], None)), body,
                        [person_schema(pr),
                         crumb_schema([('Home', 'index.html'), ('The team', 'team/index.html'),
                                       (pr['name'], 'team/%s.html' % pr['slug'])])]))
    for fn, (title, desc, h1, sub) in SERVICE_META.items():
        name = h1.rstrip('.')
        out.append(page('services/' + fn, 1, 'services', title, desc, h1, sub,
                        'Service', False,
                        (('Home', 'index.html'), ('Services', 'services/index.html'),
                         (name, None)), load(fn),
                        [service_schema(name, desc, 'services/' + fn),
                         crumb_schema([('Home', 'index.html'),
                                       ('Services', 'services/index.html'),
                                       (name, 'services/' + fn)])]))
    for fn, (title, desc, h1, sub) in GUIDE_META.items():
        name = h1.rstrip('.')
        out.append(page('guides/' + fn, 1, 'guides', title, desc, h1, sub, 'Guide', False,
                        (('Home', 'index.html'), ('Guides', 'guides/index.html'),
                         (name, None)), load(fn),
                        [page_schema(name, 'guides/' + fn, desc),
                         crumb_schema([('Home', 'index.html'), ('Guides', 'guides/index.html'),
                                       (name, 'guides/' + fn)])]))
    return out


def main():
    os.makedirs(os.path.join(OUT, 'css'), exist_ok=True)
    open(os.path.join(OUT, 'css', 'fg.css'), 'w', encoding='utf-8').write(CSS)
    built = [build_home()] + build_written()
    print('built %d pages -> %s' % (len(built), OUT))
    return built


if __name__ == '__main__':
    main()
