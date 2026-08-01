# -*- coding: utf-8 -*-
"""
Dorfman & Dorfman, CPAs — Wilmington, Massachusetts
===================================================
A standalone site. Shares NO layout, CSS, component or template with any other
build in this repo. build.py, site_hickey.py, site_carella.py, site_millcity.py
and site_goguen.py are not imported and must never be.

THE DESIGN PREMISE — "The examiner's eye"
-----------------------------------------
Two names on the door, and one of them examined firms for a living. Estee C.
Dorfman was previously employed by the Financial Industry Regulatory Authority
as a Principal Examiner. For a two-person small-town CPA firm that is a genuinely
unusual background, it is on their own About page, and it is the single most
interesting fact available about this practice.

So the site is built as an examiner would build it: everything stated precisely,
every claim sourced, nothing decorative. The visual language is evidential —
outlined boxes with a filed label tab, a strict measure, centred composition,
and figures set plainly. Where the other four builds in this batch each solve an
absence, this one has a specific professional perspective to sell.

Concretely, and deliberately unlike anything else in this repo:
  * a CENTRED masthead and centred navigation — the other four are all left-aligned
  * outlined "filed" boxes with a label tab in the top-left corner, no shadows and
    no radius; Goguen is soft and shadowed, Mill City is filled, Hickey and
    Carella are hairline-ruled
  * Spectral for text and Barlow Semi Condensed for labels and figures
  * cool grey-white and slate blue — no claret, no pine, no vermilion, no indigo
  * the contact widget is a sticky, centred, outlined bar of four cells

VERIFIED 2026-07-31. The research file for this firm was substantially wrong: it
invented the wording of all six services, wrongly said the firm advertises no
attest work (review and compilation are both on their site), missed that their
HTTPS certificate is self-signed and expired 19 June 2025, and recorded titles
for the two owners that their site does not print.

    python3 site_dorfman.py
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'dorfmancpas')
BASE = 'https://www.scalelocal.net/test-builds/dorfmancpas/'

F = dict(
    name='Dorfman &amp; Dorfman, CPAs',
    name_plain='Dorfman & Dorfman, CPAs',
    addr='402 Main Street, Suite #2',
    city='Wilmington', state='MA', state_full='Massachusetts', zip='01887',
    tel='+17817807069', ph='(781) 780-7069', ph_disp='(781) 780-7069 ext. 11',
    fax='(781) 780-7062',
    email='estee@dorfman-cpas.com',
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Dorfman+and+Dorfman+CPAs+402+Main+Street+Wilmington+MA+01887'),
    mapembed=('https://maps.google.com/maps?q=402+Main+Street%2C+Suite+2%2C+Wilmington%2C+MA'
              '+01887&t=&z=15&ie=UTF8&iwloc=&output=embed'),
)

DEMO_LEAD = 'Demonstration site.'
DEMO_BODY = ('Prepared for Dorfman &amp; Dorfman, CPAs by ScaleLocal. Not affiliated with, '
             'authorised by, or endorsed by the firm. Reproduction or use of this site or '
             'its contents is prohibited.')

# The mark: two squares sharing an edge — two names, one practice. A proposal; the
# firm has no existing mark.
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="7" y="17" width="24" height="30" fill="none" stroke="currentColor" '
        'stroke-width="4"/>'
        '<rect x="33" y="17" width="24" height="30" fill="currentColor"/></svg>')

FAVICON = (
    "data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2064%2064%27"
    "%3E%3Crect%20width%3D%2764%27%20height%3D%2764%27%20fill%3D%27%232F4E6E%27/%3E"
    "%3Crect%20x%3D%2710%27%20y%3D%2718%27%20width%3D%2720%27%20height%3D%2728%27%20fill%3D%27none%27%20stroke%3D%27%23FFFFFF%27%20stroke-width%3D%274%27/%3E"
    "%3Crect%20x%3D%2734%27%20y%3D%2718%27%20width%3D%2720%27%20height%3D%2728%27%20fill%3D%27%23FFFFFF%27/%3E%3C/svg%3E")

CSS = r"""
/* Dorfman & Dorfman, CPAs — bespoke stylesheet. Shared with no other build. */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --page:#FBFAF8;
  --sheet:#FFFFFF;
  --tint:#EEF1F3;
  --warm:#F4EFE7;
  --ink:#15181B;
  --body:#3A4147;
  --note:#5B646B;
  --rule:#DDE1E4;
  --rule2:#C3CACF;
  --slate:#2F4E6E;
  --slate-dk:#233B54;
  --slate-lt:#4E7398;
  --dark:#1B2530;
  --field:#87909A;
  --serif:"Spectral",Georgia,"Times New Roman",serif;
  --label:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;
}
html{-webkit-text-size-adjust:100%}
body{background:var(--page);color:var(--body);font-family:var(--serif);font-size:17px;
  line-height:1.72;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  overflow-wrap:break-word}
img{max-width:100%;display:block}
a{color:var(--slate-dk)}
a:hover{color:var(--slate)}
:focus-visible{outline:2px solid var(--slate);outline-offset:3px}
h1,h2,h3{font-family:var(--serif);font-weight:600;color:var(--ink);line-height:1.2}
h4{font-family:var(--label);font-weight:600;color:var(--ink);letter-spacing:.02em}
strong,b{font-weight:600;color:var(--ink)}
.skip{position:absolute;left:-9999px;background:var(--slate);color:#fff;padding:10px 16px;
  z-index:99;font-family:var(--label);font-weight:600}
.skip:focus{left:10px;top:10px}
.gut{max-width:1160px;margin:0 auto;padding:0 32px}

.demo{background:var(--dark);color:#C6CCD2;font-family:var(--label);font-size:14px;
  line-height:1.5;padding:8px 0;text-align:center}
.demo b{color:#9CC0DE;font-weight:600}
@media print{.demo{background:#fff;color:#000}}

/* ============================== THE CONTACT WIDGET =========================
   A utility bar above the navigation — the convention on professional-services
   sites, and it satisfies the requirement without inventing a new paradigm.
   Call, email and request an appointment, always visible, no script, no
   network call, no third party. */
.util{background:var(--tint);border-bottom:1px solid var(--rule)}
.util .gut{display:flex;justify-content:flex-end;gap:0;flex-wrap:wrap}
.util a{display:flex;align-items:baseline;gap:8px;padding:9px 18px;text-decoration:none;
  color:var(--body);font-family:var(--label);font-size:16px;letter-spacing:.02em;
  border-left:1px solid var(--rule)}
.util a:first-child{border-left:0}
.util a b{font-weight:600;color:var(--ink)}
.util a:hover{background:var(--sheet);color:var(--slate-dk)}
.util a:hover b{color:var(--slate-dk)}

/* ---------------------------------------------- conventional top navigation */
.bar{background:var(--page);border-bottom:1px solid var(--rule);position:sticky;top:0;
  z-index:60}
.bar .gut{display:flex;align-items:center;justify-content:space-between;gap:20px;
  padding-top:14px;padding-bottom:14px;flex-wrap:nowrap}
.mark{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}
.mark .mk{display:block;width:32px;height:32px;flex:0 0 32px;color:var(--slate)}
.mark .mk svg{width:100%;height:100%;display:block}
.mark .nm{font-family:var(--serif);font-size:20px;font-weight:600;line-height:1.14;
  white-space:nowrap}
.mark .nm span{display:block;font-family:var(--label);font-size:12.5px;font-weight:500;
  letter-spacing:.09em;text-transform:uppercase;color:var(--note);margin-top:2px;
  white-space:nowrap}
.mark:hover .nm{color:var(--slate-dk)}
.links{display:flex;align-items:center;gap:2px;flex-wrap:wrap;justify-content:flex-end}
.links a{font-family:var(--label);font-size:16px;font-weight:500;letter-spacing:.02em;
  color:var(--body);text-decoration:none;padding:7px 10px;white-space:nowrap}
.links a:hover{color:var(--ink)}
.links a[aria-current]{color:var(--slate-dk);font-weight:600}
.links a.cta{background:var(--slate);color:#fff;font-weight:600;padding:9px 16px;
  margin-left:6px}
.links a.cta:hover{background:var(--slate-dk);color:#fff}

/* ============================== THE HERO ==================================
   A plain promise, room to breathe, and one obvious thing to do next. */
.hero{background:var(--warm);border-bottom:1px solid var(--rule)}
.hero .gut{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:56px;
  align-items:center;padding-top:66px;padding-bottom:66px}
.hero .eyebrow{font-family:var(--label);font-size:15.5px;font-weight:600;letter-spacing:.12em;
  text-transform:uppercase;color:var(--slate-dk);margin-bottom:18px}
.hero h1{font-size:clamp(33px,4.6vw,52px);letter-spacing:-.015em;line-height:1.1;
  max-width:15ch}
.hero p{margin-top:20px;font-size:20px;line-height:1.58;color:var(--body);max-width:46ch}
.hero .acts{margin-top:30px;display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-block;font-family:var(--label);font-size:17px;font-weight:600;
  letter-spacing:.03em;padding:13px 26px;text-decoration:none;line-height:1.2}
.btn.solid{background:var(--slate);color:#fff}
.btn.solid:hover{background:var(--slate-dk);color:#fff}
.btn.ghost{background:transparent;color:var(--slate-dk);border:2px solid var(--slate-lt)}
.btn.ghost:hover{border-color:var(--slate);color:var(--slate-dk)}
.hero .art{width:100%}
.hero .art img{width:100%;height:auto;display:block}
.hero.plain .gut{grid-template-columns:minmax(0,1fr);max-width:900px}
.hero.plain p{max-width:56ch}

/* page heads on inner pages */
.phead{background:var(--warm);border-bottom:1px solid var(--rule)}
.phead .gut{padding-top:42px;padding-bottom:42px;max-width:1160px}
.phead .inner{max-width:64ch}
.path{font-family:var(--label);font-size:15px;color:var(--note);margin-bottom:12px}
.path a{color:var(--note);text-decoration:none}
.path a:hover{color:var(--slate-dk);text-decoration:underline}
.path s{text-decoration:none;padding:0 8px;color:var(--rule2)}
.tagline{font-family:var(--label);font-size:15px;font-weight:600;letter-spacing:.11em;
  text-transform:uppercase;color:var(--slate-dk);margin-bottom:12px}
.phead h1{font-size:clamp(29px,4vw,42px);letter-spacing:-.012em;line-height:1.14}
.phead .stand{margin-top:13px;font-size:19px;line-height:1.6;color:var(--body);max-width:58ch}

main{padding:44px 0 0}

/* the filed box */
.filed{margin-top:30px;background:var(--sheet);border:1px solid var(--rule);
  position:relative;padding:30px 32px 28px}
.filed > .tab{display:inline-block;background:var(--slate);color:#fff;
  font-family:var(--label);font-size:14px;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 12px 4px;margin-bottom:16px}
.filed.blue{border-color:var(--slate-lt)}
.filed.tint{background:var(--tint);border-color:var(--rule2)}
.filed.dark{background:var(--dark);border-color:var(--dark);color:#C6CCD2}
.filed.dark > .tab{background:var(--slate);color:#fff}
.filed.dark h2,.filed.dark h3{color:#fff}
.filed.dark a{color:#9CC0DE}
.filed.dark a:hover{color:#fff}
.filed.plain{border:0;background:transparent;padding:0}
h2{font-size:27px}
h3{font-size:19px}
.prose p{margin-top:14px;max-width:68ch}
.prose h3{margin-top:26px}
.prose h3 + p{margin-top:8px}
.prose h4{margin-top:20px;font-size:16px;text-transform:uppercase;letter-spacing:.06em}
.prose ul,.prose ol{margin-top:13px;padding-left:0;list-style:none;max-width:68ch}
.prose li{position:relative;padding-left:24px;margin-top:9px}
.prose ul li::before{content:"";position:absolute;left:1px;top:12px;width:11px;height:2px;
  background:var(--slate-lt)}
.prose ol{counter-reset:d}
.prose ol li{counter-increment:d}
.prose ol li::before{content:counter(d) ".";position:absolute;left:0;top:0;
  font-family:var(--label);font-weight:600;color:var(--slate-dk);font-size:16px}
.prose .end{margin-top:20px;font-size:15.5px;color:var(--note)}

/* services as scannable tiles — what a visitor looks for first */
.tiles{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:18px}
.tiles a{display:block;background:var(--sheet);border:1px solid var(--rule);padding:24px 24px 22px;
  text-decoration:none;color:var(--body)}
.tiles a:hover{border-color:var(--slate);background:var(--sheet)}
.tiles .t{font-family:var(--serif);font-size:20px;font-weight:600;color:var(--ink);
  line-height:1.25;display:block}
.tiles .d{display:block;margin-top:9px;font-size:16px;line-height:1.6}
.tiles .go{display:block;margin-top:14px;font-family:var(--label);font-size:15.5px;
  font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--slate-dk)}

/* section heading used between bands */
.band{padding:52px 0 0}
.band.warm{background:var(--warm);padding:52px 0 56px;margin-top:52px;
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.band .lead{max-width:62ch}
.band .lead h2{font-size:31px;letter-spacing:-.01em}
.band .lead p{margin-top:13px;font-size:18.5px;line-height:1.6}
.band.warm + .band{padding-top:52px}

.reg{margin-top:18px;border-top:1px solid var(--rule2)}
.reg a,.reg .r{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:16px;
  align-items:baseline;padding:15px 0;border-bottom:1px solid var(--rule);
  text-decoration:none;color:var(--body)}
.reg .n{font-family:var(--label);font-size:15px;font-weight:600;color:var(--slate-dk)}
.reg .t{font-family:var(--serif);font-size:18.5px;font-weight:600;color:var(--ink);
  line-height:1.3}
.reg .d{display:block;margin-top:4px;font-size:15.5px;line-height:1.55;max-width:60ch}
.reg .x{font-family:var(--label);font-size:14.5px;font-weight:600;color:var(--note);
  white-space:nowrap;text-transform:uppercase}
.reg a:hover .t{color:var(--slate-dk)}

.pair{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));
  gap:20px}
.pair a{display:block;background:var(--sheet);border:1px solid var(--rule);padding:24px;
  text-decoration:none;color:var(--body)}
.pair a:hover{border-color:var(--slate)}
.pair .who{font-family:var(--serif);font-size:22px;font-weight:600;color:var(--ink);
  line-height:1.2}
.pair .cred{display:block;margin-top:5px;font-family:var(--label);font-size:15.5px;
  font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--slate-dk)}
.pair .line{display:block;margin-top:11px;font-size:16px;line-height:1.58}
.pair .go{display:block;margin-top:13px;font-family:var(--label);font-size:15.5px;
  font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--slate-dk)}

.fig{margin-top:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  gap:0;border-top:1px solid var(--rule2);border-left:1px solid var(--rule)}
.fig div{padding:18px 20px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.filed.dark .fig{border-top-color:var(--slate-lt);border-left-color:#33414F}
.filed.dark .fig div{border-right-color:#33414F;border-bottom-color:#33414F}
.fig .n{display:block;font-family:var(--label);font-size:31px;font-weight:600;
  color:var(--slate-dk);line-height:1.08;letter-spacing:-.005em}
.filed.dark .fig .n{color:#9CC0DE}
.fig .c{display:block;margin-top:5px;font-size:14.5px;line-height:1.45;color:var(--note)}
.filed.dark .fig .c{color:#9AA6B2}

.mnote{margin-top:22px;border-left:3px solid var(--slate);padding:2px 0 2px 18px}
.mnote .ml{font-family:var(--label);font-size:14.5px;font-weight:600;letter-spacing:.09em;
  text-transform:uppercase;color:var(--slate-dk);margin-bottom:5px}
.mnote p{font-size:16px;line-height:1.6;max-width:64ch}
.mnote p + p{margin-top:10px}

.sc{margin-top:18px;overflow-x:auto;-webkit-overflow-scrolling:touch}
table.reg2{border-collapse:collapse;width:100%;min-width:440px;font-size:16px}
table.reg2 th{font-family:var(--label);font-size:14.5px;font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;text-align:left;padding:10px 16px 10px 0;color:var(--ink);
  border-bottom:2px solid var(--rule2)}
table.reg2 td{padding:11px 16px 11px 0;border-bottom:1px solid var(--rule);vertical-align:top;
  line-height:1.5}
table.reg2 td.q{font-family:var(--label);font-weight:600;color:var(--ink);white-space:nowrap}

.map{margin-top:20px;border:1px solid var(--rule)}
.map iframe{width:100%;height:310px;border:0;display:block;filter:grayscale(.35)}
.map + .mc{margin-top:9px;font-size:14.5px;color:var(--note)}

.cwrap{margin-top:20px}
.cf{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:16px}
.cf .fl{display:block;font-family:var(--label);font-size:15.5px;font-weight:600;
  color:var(--ink);margin-bottom:5px}
.fbx{display:flex;align-items:center;border:2px solid var(--field);background:var(--sheet);
  height:42px}
.fbx:focus-within{border-color:var(--slate)}
.fbx .pf,.fbx .sf{font-family:var(--label);font-size:14.5px;font-weight:600;color:var(--note);
  padding:0 10px}
.fbx input{width:100%;min-width:0;border:0;background:transparent;height:100%;padding:0 8px;
  font:inherit;font-family:var(--label);font-size:17px;font-weight:600;color:var(--ink);
  text-align:right}
.fbx input:focus{outline:0}
.hint{margin-top:5px;font-size:14.5px;color:var(--note);line-height:1.45}
.res{margin-top:24px;border:1px solid var(--slate);background:var(--sheet)}
.res .rh{font-family:var(--label);font-size:14.5px;font-weight:600;letter-spacing:.09em;
  text-transform:uppercase;color:#fff;background:var(--slate);padding:7px 16px}
.res .rv{font-family:var(--label);font-size:46px;font-weight:600;color:var(--slate-dk);
  line-height:1.05;padding:18px 16px 6px}
.res dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  border-top:1px solid var(--rule)}
.res dl > div{padding:12px 16px;border-right:1px solid var(--rule);
  border-bottom:1px solid var(--rule)}
.res dt{font-family:var(--label);font-size:14.5px;color:var(--note)}
.res dd{font-family:var(--label);font-size:21px;font-weight:600;color:var(--ink);margin-top:2px}
.res .rn{grid-column:1/-1;padding:11px 16px;font-size:14.5px;color:var(--note);
  line-height:1.5;border-right:0}

/* closing call to action */
.close-cta{margin-top:56px;background:var(--dark);color:#C6CCD2;padding:46px 0}
.close-cta h2{color:#fff;font-size:30px;max-width:20ch}
.close-cta p{margin-top:13px;font-size:18px;line-height:1.6;max-width:54ch}
.close-cta .acts{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}
.close-cta .btn.solid{background:#fff;color:var(--dark)}
.close-cta .btn.solid:hover{background:#DCE4EA;color:var(--dark)}
.close-cta .btn.ghost{color:#fff;border-color:#42505E}
.close-cta .btn.ghost:hover{border-color:#fff;color:#fff}

.foot{background:var(--page);border-top:1px solid var(--rule);padding:34px 0 34px}
.foot .fg{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:34px}
.foot .fn{font-family:var(--serif);font-size:19px;font-weight:600;color:var(--ink)}
.foot .fa{margin-top:8px;font-size:16px;line-height:1.7;color:var(--body)}
.foot .fa a{color:var(--body);text-decoration:none}
.foot .fa a:hover{color:var(--slate-dk);text-decoration:underline}
.foot .fh{font-family:var(--label);font-size:14.5px;font-weight:600;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink);margin-bottom:10px}
.foot ul{list-style:none;font-size:16px;line-height:1.95}
.foot ul a{color:var(--body);text-decoration:none}
.foot ul a:hover{color:var(--slate-dk);text-decoration:underline}
.foot .fine{margin-top:28px;padding-top:18px;border-top:1px solid var(--rule);font-size:14.5px;
  line-height:1.6;color:var(--note)}

@media (max-width:1080px){
  .links a{font-size:15px;padding:7px 8px}
  .mark .nm{font-size:18px}
}
@media (max-width:900px){
  .gut{padding:0 20px}
  .bar .gut{flex-wrap:wrap}
  .hero .gut{grid-template-columns:minmax(0,1fr);gap:32px;padding-top:44px;padding-bottom:46px}
  .hero .art{order:-1;max-width:420px}
  .foot .fg{grid-template-columns:minmax(0,1fr);gap:24px}
  .filed{padding:24px 20px 22px}
  .bar .gut{flex-wrap:wrap;gap:12px}
  .links{gap:0}
  .links a{padding:7px 9px;font-size:16px}
  .util .gut{justify-content:center}
  .util a{padding:8px 12px;font-size:15px}
}
@media (max-width:520px){
  .reg a,.reg .r{grid-template-columns:26px minmax(0,1fr)}
  .reg .x{grid-column:2;text-align:left}
  .res .rv{font-size:36px}
  .util a b{display:none}
}
@media print{.demo,.bar,.util,.map,.close-cta{display:none}}
"""

# ==========================================================================
NAV = [('services/index.html', 'Services', 'services'),
       ('regulatory-background.html', 'Background', 'reg'),
       ('about.html', 'The firm', 'about'),
       ('calculators/index.html', 'Calculators', 'calculators'),
       ('faq.html', 'Questions', 'faq'),
       ('contact.html', 'Contact', 'contact')]

# Both credential strings are printed exactly once on the firm's own site, in the
# ownership sentence. Neither person is given a title anywhere — not "owner", not
# "partner", not "founder" — so none is invented here.
PEOPLE = [
    dict(slug='marvin-h-dorfman', name='Marvin H. Dorfman', cred='CPA',
         line='Formed the firm in 2008. Senior partner at Dorfman &amp; Goldstein, CPAs '
              'until 2004, then a sole practitioner until the two practices became one.'),
    dict(slug='estee-c-dorfman', name='Estee C. Dorfman', cred='CPA, MSA',
         line='Co-founded the firm in 2008. Previously employed by the Financial Industry '
              'Regulatory Authority as a Principal Examiner.'),
]

# The six services, in the firm's own words, from their Accounting & Tax Services
# page. Grouped into four pages; not a word of the wording is invented.
SERVICES = [
    ('services/review-compilation.html', 'Review and compilation',
     'Review and compilation of small business financial statements &mdash; two different '
     'levels of service, at two very different costs.'),
    ('services/tax-returns.html', 'Tax returns',
     'Returns for individuals and trusts, corporate returns, and returns for partnerships '
     'and limited liability companies.'),
    ('services/bookkeeping.html', 'Bookkeeping to trial balance',
     'The monthly discipline that every statement and every return above it depends on.'),
    ('services/payroll-tax.html', 'Payroll tax returns',
     'Federal and state payroll tax returns, and the deposit deadlines that carry the '
     'real penalties.'),
]


def rel(depth, target):
    if target.startswith(('http', 'mailto:', 'tel:', '#')):
        return target
    return ('../' * depth) + target


def esc(s):
    return H.escape(s, quote=True)


def nav_html(depth, active):
    out = ['<div class="bar"><div class="gut">',
           '<a class="mark" href="%s"><span class="mk">%s</span>'
           '<span class="nm">Dorfman &amp; Dorfman<span>CPAs &middot; Wilmington</span></span></a>'
           % (rel(depth, 'index.html'), MARK),
           '<nav class="links" aria-label="Main">']
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        out.append('<a href="%s"%s>%s</a>' % (rel(depth, href), cur, label))
    out.append('<a class="cta" href="%s">Request an appointment</a>'
               % rel(depth, 'contact.html#appointment'))
    out.append('</nav></div></div>')
    return ''.join(out)


def utility(depth):
    """THE CONTACT WIDGET. A utility bar above the navigation — the convention on
    professional-services sites, and it meets the requirement without inventing a
    paradigm. Call, email, appointment. Always visible, no interaction needed, no
    script, no network call, no third party."""
    return (
        '<div class="util" data-contact-widget role="group" aria-label="Contact the firm">'
        '<div class="gut">'
        '<a href="tel:%s">Call <b>%s</b></a>'
        '<a href="mailto:%s">Email <b>%s</b></a>'
        '<a href="%s"><b>Request an appointment</b></a>'
        '</div></div>'
    ) % (F['tel'], F['ph_disp'], F['email'], F['email'],
         rel(depth, 'contact.html#appointment'))


def closing_cta(depth):
    return (
        '<section class="close-cta"><div class="gut">'
        '<h2>Two CPAs, and one of them will be the one who does the work.</h2>'
        '<p>Describe what you have and ask what the work involves. There is no fee '
        'schedule to quote from, because no two engagements are the same.</p>'
        '<div class="acts"><a class="btn solid" href="tel:%s">Call %s</a>'
        '<a class="btn ghost" href="%s">Request an appointment</a></div>'
        '</div></section>'
    ) % (F['tel'], F['ph_disp'], rel(depth, 'contact.html#appointment'))


def footer(depth):
    svc = ''.join('<li><a href="%s">%s</a></li>' % (rel(depth, h), t)
                  for h, t, _ in SERVICES)
    firm = ''.join('<li><a href="%s">%s</a></li>' % (rel(depth, h), t)
                   for h, t in [('about.html', 'The firm'),
                                ('regulatory-background.html', 'Regulatory background'),
                                ('team/marvin-h-dorfman.html', 'Marvin H. Dorfman, CPA'),
                                ('team/estee-c-dorfman.html', 'Estee C. Dorfman, CPA, MSA'),
                                ('faq.html', 'Questions'),
                                ('calculators/index.html', 'Calculators'),
                                ('contact.html', 'Contact')])
    return (
        '<footer class="foot"><div class="gut"><div class="fg">'
        '<div><div class="fn">%s</div><div class="fa">%s<br>%s, %s %s<br>'
        '<a href="tel:%s">%s</a> &nbsp;&middot;&nbsp; facsimile %s<br>'
        '<a href="mailto:%s">%s</a></div></div>'
        '<div><div class="fh">Services</div><ul>%s</ul></div>'
        '<div><div class="fh">The firm</div><ul>%s</ul></div>'
        '</div><p class="fine">%s %s</p></div></footer>'
    ) % (F['name'], F['addr'], F['city'], F['state'], F['zip'], F['tel'], F['ph_disp'],
         F['fax'], F['email'], F['email'], svc, firm, DEMO_LEAD, DEMO_BODY)


def path_html(depth, crumbs):
    if not crumbs:
        return ''
    b = []
    for label, href in crumbs:
        b.append('<a href="%s">%s</a>' % (rel(depth, href), label) if href
                 else '<span>%s</span>' % label)
    return '<div class="path">%s</div>' % '<s>/</s>'.join(b)


def shell(depth, nav, title, desc, head_html, body, schema, tail=''):
    url = BASE + ('' if head_html is None else '')
    return None


def page(path, depth, nav, title, desc, h1, stand='', tagline='', crumbs=(), body='',
         schema=(), tail='', hero=None):
    """hero: None renders the standard page head. A dict renders the homepage hero."""
    url = BASE + ('' if path == 'index.html' else path)
    ld = ''.join('<script type="application/ld+json">%s</script>'
                 % json.dumps(s, separators=(',', ':')) for s in schema)
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<title>%(t)s</title><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="description" content="%(d)s">'
        '<meta name="robots" content="noindex, nofollow">'
        '<meta name="googlebot" content="noindex, nofollow">'
        '<link rel="canonical" href="%(u)s"><meta name="theme-color" content="#2F4E6E">'
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="%(n)s">'
        '<meta property="og:title" content="%(t)s">'
        '<meta property="og:description" content="%(d)s">'
        '<meta property="og:url" content="%(u)s">'
        '<meta property="og:image" content="%(b)sog.png">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Dorfman &amp; Dorfman, CPAs, Wilmington, Massachusetts">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="%(t)s">'
        '<meta name="twitter:description" content="%(d)s">'
        '<meta name="twitter:image" content="%(b)sog.png">'
        '<link rel="apple-touch-icon" href="%(a)s">'
        '<link rel="icon" type="image/svg+xml" href="%(f)s">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;500;600&family=Barlow+Semi+Condensed:wght@400;500;600&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="%(c)s">%(ld)s</head>'
    ) % dict(t=esc(title), d=esc(desc), u=url, n=esc(F['name_plain']), b=BASE,
             c=rel(depth, 'css/dd.css'), f=FAVICON,
             a=rel(depth, 'apple-touch-icon.png'), ld=ld)

    if hero:
        art = ('<div class="art"><img src="%s" alt="%s" width="960" height="720"></div>'
               % (rel(depth, hero['art']), hero['alt'])) if hero.get('art') else ''
        opening = (
            '<section class="hero%s"><div class="gut"><div>'
            '<div class="eyebrow">%s</div><h1>%s</h1><p>%s</p>'
            '<div class="acts"><a class="btn solid" href="%s">%s</a>'
            '<a class="btn ghost" href="%s">%s</a></div></div>%s</div></section>'
        ) % ('' if art else ' plain', hero['eyebrow'], h1, stand,
             rel(depth, hero['cta1'][1]), hero['cta1'][0],
             rel(depth, hero['cta2'][1]), hero['cta2'][0], art)
    else:
        opening = (
            '<section class="phead"><div class="gut"><div class="inner">%s%s<h1>%s</h1>%s'
            '</div></div></section>'
        ) % (path_html(depth, crumbs),
             '<div class="tagline">%s</div>' % tagline if tagline else '',
             h1, '<p class="stand">%s</p>' % stand if stand else '')

    doc = (head + '<body><a class="skip" href="#main">Skip to content</a>'
           '<div class="demo"><div class="gut"><b>' + DEMO_LEAD + '</b> ' + DEMO_BODY + '</div></div>'
           + utility(depth) + nav_html(depth, nav) + opening +
           '<main id="main"><div class="gut">' + body + '</div></main>'
           + closing_cta(depth) + footer(depth) + tail + '</body></html>')
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(doc)
    return path


def org_schema():
    return {'@context': 'https://schema.org', '@type': 'AccountingService',
            '@id': BASE + '#firm', 'name': F['name_plain'], 'url': BASE,
            'email': F['email'], 'telephone': F['ph'], 'faxNumber': F['fax'],
            'foundingDate': '2008',
            'address': {'@type': 'PostalAddress', 'streetAddress': F['addr'],
                        'addressLocality': F['city'], 'addressRegion': F['state'],
                        'postalCode': F['zip'], 'addressCountry': 'US'},
            'employee': [{'@type': 'Person', 'name': p['name']} for p in PEOPLE],
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
def filed(tab, inner, kind=''):
    return ('<section class="filed%s"><span class="tab">%s</span>%s</section>'
            % ((' ' + kind) if kind else '', tab, inner))


def reg(depth, items, numbered=True):
    """items: (href|None, title, detail, right)"""
    out = ['<div class="reg">']
    for i, it in enumerate(items, 1):
        href, t, d = it[0], it[1], it[2]
        r = it[3] if len(it) > 3 else ''
        n = '<span class="n">%02d</span>' % i if numbered else '<span class="n"></span>'
        inner = ('%s<span><span class="t">%s</span><span class="d">%s</span></span>'
                 '<span class="x">%s</span>' % (n, t, d, r))
        out.append('<a href="%s">%s</a>' % (rel(depth, href), inner) if href
                   else '<div class="r">%s</div>' % inner)
    out.append('</div>')
    return ''.join(out)


def pair(depth):
    out = ['<div class="pair">']
    for p in PEOPLE:
        out.append('<a href="%s"><span class="who">%s</span>'
                   '<span class="cred">%s</span><span class="line">%s</span>'
                   '<span class="go">Read more &rarr;</span></a>'
                   % (rel(depth, 'team/%s.html' % p['slug']), p['name'], p['cred'], p['line']))
    out.append('</div>')
    return ''.join(out)


def fig(items):
    return ('<div class="fig">%s</div>'
            % ''.join('<div><span class="n">%s</span><span class="c">%s</span></div>'
                      % (a, b) for a, b in items))


def mnote(label, *paras):
    return ('<div class="mnote"><div class="ml">%s</div>%s</div>'
            % (label, ''.join('<p>%s</p>' % p for p in paras)))


def table(headers, rows_):
    th = ''.join('<th>%s</th>' % h for h in headers)
    tr = ''.join('<tr>%s</tr>' % ''.join(
        '<td%s>%s</td>' % (' class="q"' if isinstance(c, tuple) else '',
                           c[0] if isinstance(c, tuple) else c) for c in r) for r in rows_)
    return ('<div class="sc"><table class="reg2"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (th, tr))


def mapblock():
    return ('<div class="map"><iframe title="Interactive Google map showing Dorfman '
            '&amp; Dorfman, CPAs at 402 Main Street, Wilmington, Massachusetts" src="%s" '
            'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen>'
            '</iframe></div><p class="mc">Pan, zoom, or <a href="%s" target="_blank" '
            'rel="noopener">open the map full screen</a> for directions.</p>'
            % (F['mapembed'], F['maps']))


def load(name):
    p = os.path.join(HERE, 'content_dorfman', name)
    if not os.path.exists(p):
        raise SystemExit('missing content file: %s' % p)
    return open(p, encoding='utf-8').read().strip()

# ==========================================================================
import calculators as C
CALC_PICK = ['self-employment-tax', 'break-even', 'loan-payment', 'section-179']
CALCS = [c for s in CALC_PICK for c in C.CALCULATORS if c['slug'] == s]
MA_NOTE = {
    'section-179': ('Massachusetts disallows federal bonus depreciation and has deferred '
                    'conformity to the increased federal section&nbsp;179 limits for the '
                    '2025 and 2026 tax years. The state deduction on the same purchase may '
                    'be materially smaller than the federal one.'),
    'self-employment-tax': ('The Social Security portion stops at an annual wage base that '
                            'is adjusted each year; the Medicare portion does not. This '
                            'estimates self-employment tax only.'),
}
NOTE_OVER = {'section-179': ('Section 179 cannot create a loss, and annual limits and '
                             'phase-outs apply. Ask before the purchase order is signed, '
                             'not after.')}


def calc_body(c, depth=1):
    fields = ''
    for x in c['inputs']:
        pre = '<span class="pf">$</span>' if x['kind'] == C.MONEY else ''
        suf = ('<span class="sf">%</span>' if x['kind'] == C.PCT else
               '<span class="sf">yrs</span>' if x['kind'] == C.YEARS else '')
        at = ' step="%s"' % x['step'] if x.get('step') else ''
        if x.get('min') is not None:
            at += ' min="%s"' % x['min']
        if x.get('max') is not None:
            at += ' max="%s"' % x['max']
        fields += ('<div><label class="fl" for="f_%s">%s</label><div class="fbx">%s'
                   '<input type="number" inputmode="decimal" id="f_%s" value="%s"%s>%s</div>%s</div>'
                   % (x['id'], x['label'], pre, x['id'], x['default'], at, suf,
                      '<p class="hint">%s</p>' % x['hint'] if x.get('hint') else ''))
    primary = next((o for o in c['outputs'] if o['primary']), c['outputs'][0])
    outs = ''
    for o in c['outputs']:
        if o['primary']:
            continue
        outs += '<div><dt>%s</dt><dd id="o_%s">&mdash;</dd></div>' % (o['label'], o['id'])
        if o.get('note'):
            outs += '<div class="rn">%s</div>' % o['note']
    spec = json.dumps(dict(inputs=[dict(id=x['id']) for x in c['inputs']],
                           outputs=[dict(id=o['id'], kind=o['kind']) for o in c['outputs']],
                           js=c['js']), separators=(',', ':'))
    b = filed('Work it out',
              '<div class="cwrap" data-calc><div class="cf">' + fields + '</div>'
              '<div class="res" aria-live="polite"><div class="rh">' + primary['label'] + '</div>'
              '<div class="rv" id="o_' + primary['id'] + '">&mdash;</div><dl>' + outs + '</dl></div></div>'
              + mnote('What this does not cover', NOTE_OVER.get(c['slug'], c['note']))
              + '<script type="application/json" id="calcspec">' + spec + '</script>', 'blue')
    if c['slug'] in MA_NOTE:
        b += filed('Massachusetts', '<div class="prose"><p>' + MA_NOTE[c['slug']] + '</p></div>', 'tint')
    others = [('calculators/%s.html' % o['slug'], o['title'], o['blurb'])
              for o in CALCS if o['slug'] != c['slug']]
    b += filed('Other calculators', reg(depth, others), 'plain')
    b += filed('Not advice',
               '<div class="prose"><p>An estimating tool. It uses the assumptions above and '
               'nothing else about your return. Call <a href="tel:%s">%s</a> or '
               '<a href="%s">arrange a time</a> to talk about what the figure means.</p></div>'
               % (F['tel'], F['ph_disp'], rel(depth, 'contact.html#appointment')), 'dark')
    return b


def build_calculators():
    d = 1
    out = [page('calculators/index.html', d, 'calculators',
        'Calculators | Dorfman &amp; Dorfman, CPAs',
        'Self-employment tax, break-even, loan payments and equipment purchases &mdash; four '
        'calculators that run entirely in your browser. Nothing is sent anywhere.',
        'Four calculators.',
        'Enough to size a question before you raise it. They run in your browser, and '
        'nothing you enter leaves the page.', 'Tools',
        (('Home', 'index.html'), ('Calculators', None)),
        filed('The four', reg(d, [('calculators/%s.html' % c['slug'], c['title'], c['blurb'])
                                  for c in CALCS]))
        + filed('Estimates, not advice',
                '<div class="prose"><p>Rates, thresholds and contribution limits change every '
                'year, and none of these account for your filing status, your Massachusetts '
                'position or anything else on your return. Use one to size a question, then '
                '<a href="../contact.html">ask about the answer</a>.</p></div>', 'tint'),
        [page_schema('Calculators', 'calculators/index.html', 'Four native calculators.'),
         crumb_schema([('Home', 'index.html'), ('Calculators', 'calculators/index.html')])])]
    for c in CALCS:
        out.append(page('calculators/%s.html' % c['slug'], d, 'calculators',
            '%s | Dorfman &amp; Dorfman, CPAs' % c['title'],
            (c['blurb'] + ' Runs entirely in your browser; nothing is sent anywhere.')[:174],
            c['title'] + '.', c['blurb'], 'Calculator',
            (('Home', 'index.html'), ('Calculators', 'calculators/index.html'),
             (c['title'], None)), calc_body(c, d),
            [page_schema(c['title'], 'calculators/%s.html' % c['slug'], c['blurb']),
             crumb_schema([('Home', 'index.html'), ('Calculators', 'calculators/index.html'),
                           (c['title'], 'calculators/%s.html' % c['slug'])])],
            tail=C.CALC_JS))
    return out


def tiles(depth, items):
    out = ['<div class="tiles">']
    for href, t, d in items:
        out.append('<a href="%s"><span class="t">%s</span><span class="d">%s</span>'
                   '<span class="go">Read more &rarr;</span></a>' % (rel(depth, href), t, d))
    out.append('</div>')
    return ''.join(out)


def band(inner, warm=False):
    return '<section class="band%s">%s</section>' % (' warm' if warm else '', inner)


def build_home():
    """Conventional order, on purpose: a promise, then what we do, then why us,
    then who we are, then the differentiated content, then a way to start."""
    d = 0
    b = band(
        '<div class="lead"><h2>What the firm does</h2>'
        '<p>Six services, in the firm&rsquo;s own words, grouped into four pages. Review '
        'and compilation are both offered. Audits are not, and it is more useful to say '
        'so than to leave you guessing.</p></div>'
        + tiles(d, [(h, t, x) for h, t, x in SERVICES]))

    b += band(
        '<div class="lead"><h2>Why a firm of two</h2>'
        '<p>There is no bench to hand your file to. The person who takes the call is the '
        'person who does the work, and both of them are Certified Public Accountants.</p>'
        '</div>'
        + fig([('2008', 'the year the firm was formed'),
               ('2', 'Certified Public Accountants, and no one else'),
               ('Form 1041', 'trusts and estates are in scope'),
               ('4', 'levels of financial statement service explained plainly')]),
        warm=True)

    b += band(
        '<div class="lead"><h2>Who you would be working with</h2>'
        '<p>Marvin formed the firm in 2008 after a decade as a sole practitioner and, '
        'before that, as senior partner of another practice. Estee co-founded it the same '
        'year, having previously been employed by the Financial Industry Regulatory '
        'Authority as a Principal Examiner.</p></div>' + pair(d))

    b += band(
        '<div class="lead"><h2>What a regulator&rsquo;s eye is worth</h2>'
        '<p>An examiner&rsquo;s job is to decide whether records support what has been '
        'asserted. That is the same question a lender, a buyer or an examination asks of a '
        'small business years after the fact &mdash; and the answer is settled long before '
        'anyone asks it.</p><p><a href="regulatory-background.html">Read the longer '
        'piece &rarr;</a></p></div>')

    b += band(
        '<div class="lead"><h2>Before you call</h2></div>'
        + reg(d, [('faq.html', 'Common questions',
                   'Compilation against review, what a lender is actually asking for, and '
                   'how long to keep records.'),
                  ('about.html', 'About the firm',
                   'How two practices became one, and how an engagement runs.'),
                  ('calculators/index.html', 'Calculators',
                   'Four estimating tools that run in your browser.')], numbered=False))

    return page('index.html', d, 'home',
        'Dorfman &amp; Dorfman, CPAs | Wilmington, Massachusetts',
        'A family-owned firm of two CPAs in Wilmington, Massachusetts. Review and '
        'compilation, tax returns, bookkeeping to trial balance and payroll tax returns.',
        'Accounting that holds up when somebody checks.',
        'A family-owned firm of two Certified Public Accountants in Wilmington. One of them '
        'spent part of her career deciding whether other people&rsquo;s records supported '
        'what they claimed.',
        '', (), b,
        [org_schema(), {'@context': 'https://schema.org', '@type': 'WebSite',
                        'name': F['name_plain'], 'url': BASE,
                        'publisher': {'@id': BASE + '#firm'}}],
        hero=dict(eyebrow='Wilmington, Massachusetts &middot; since 2008',
                  cta1=('Request an appointment', 'contact.html#appointment'),
                  cta2=('What the firm does', 'services/index.html'),
                  art='img/hero.png',
                  alt='An original illustration of a set of financial records under review, '
                      'drawn in the firm&rsquo;s colours'))



PAGES = [
    dict(file='regulatory-background.html', path='regulatory-background.html', depth=0,
         nav='reg', title='Regulatory background | Dorfman &amp; Dorfman, CPAs',
         desc='What a former Principal Examiner brings to a small business&rsquo;s books, '
              'and the honest limits of what that means.',
         h1='What a regulator&rsquo;s eye is worth.', tag='The differentiator',
         stand='Estee C. Dorfman was previously employed by the Financial Industry '
               'Regulatory Authority as a Principal Examiner. An examiner&rsquo;s job is to '
               'decide whether records support what has been asserted.',
         crumbs=(('Home', 'index.html'), ('Regulatory background', None))),
    dict(file='services_index.html', path='services/index.html', depth=1, nav='services',
         title='Services | Dorfman &amp; Dorfman, CPAs, Wilmington MA',
         desc='Review and compilation of small business financial statements, tax returns, '
              'bookkeeping to trial balance, and federal and state payroll tax returns.',
         h1='Six services, four pages.', tag='What the firm does',
         stand='Stated in the firm&rsquo;s own words, with the scope left exactly as the '
               'firm scopes it.',
         crumbs=(('Home', 'index.html'), ('Services', None))),
    dict(file='about.html', path='about.html', depth=0, nav='about',
         title='The firm | Dorfman &amp; Dorfman, CPAs',
         desc='A family-owned firm formed in 2008 by two Certified Public Accountants, in '
              'Wilmington, Massachusetts.',
         h1='How two practices became one.', tag='The firm',
         stand='Formed in 2008. A family-owned firm of two Certified Public Accountants, '
               'and no one else.',
         crumbs=(('Home', 'index.html'), ('The firm', None))),
    dict(file='faq.html', path='faq.html', depth=0, nav='faq',
         title='Questions | Dorfman &amp; Dorfman, CPAs',
         desc='Compilation against review, what a lender is actually asking for, trusts and '
              'Form 1041, extensions, records retention, and what a CPA licence means.',
         h1='Questions worth asking first.', tag='Common questions',
         stand='If yours is not here, it is a short phone call rather than a form.',
         crumbs=(('Home', 'index.html'), ('Questions', None))),
    dict(file='contact.html', path='contact.html', depth=0, nav='contact',
         title='Contact | Dorfman &amp; Dorfman, CPAs, Wilmington MA',
         desc='402 Main Street, Suite #2, Wilmington, Massachusetts. Telephone (781) '
              '780-7069 extension 11, or write to the firm.',
         h1='Speak to a CPA.', tag='Contact',
         stand='One office, on Main Street in Wilmington. Two people, and one of them will '
               'be the one who does the work.',
         crumbs=(('Home', 'index.html'), ('Contact', None)), map_after=True),
]

SVC_META = {
    'review-compilation.html': ('Review and compilation | Dorfman &amp; Dorfman, CPAs',
        'Review and compilation of small business financial statements, and a straight '
        'answer about which level of service a lender is actually asking for.',
        'Review and compilation.', 'Four levels of service share one name, and the gap '
        'between the cheapest and the dearest is a multiple rather than a percentage.'),
    'tax-returns.html': ('Tax returns | Dorfman &amp; Dorfman, CPAs',
        'Returns for individuals and trusts, corporate returns, and returns for '
        'partnerships and limited liability companies, federal and Massachusetts.',
        'Tax returns.', 'Individuals and trusts, corporations, partnerships and limited '
        'liability companies &mdash; and the order in which they have to be done.'),
    'bookkeeping.html': ('Bookkeeping to trial balance | Dorfman &amp; Dorfman, CPAs',
        'Monthly bookkeeping to trial balance for small businesses in Wilmington, '
        'Massachusetts &mdash; the work every statement and every return depends on.',
        'Bookkeeping to trial balance.', 'The scope is stated plainly, and so is what it '
        'buys: books that reconcile to something outside themselves.'),
    'payroll-tax.html': ('Payroll tax returns | Dorfman &amp; Dorfman, CPAs',
        'Federal and state payroll tax returns for small employers in Wilmington, '
        'Massachusetts, and the deadlines that carry the real penalties.',
        'Payroll tax returns.', 'Federal and state. The most dangerous liability a small '
        'business carries, because it is money withheld on somebody else&rsquo;s behalf.'),
}


def build_written():
    out = []
    for p in PAGES:
        body = load(p['file'])
        if p.get('map_after'):
            body += filed('Finding the office', mapblock())
        sch = [page_schema(re.sub(r'<[^>]+>|&[a-z]+;', '', p['h1']).rstrip('.'),
                           p['path'], p['desc']),
               crumb_schema([(n, u or p['path']) for n, u in p['crumbs']])]
        if p['path'] == 'contact.html':
            sch.insert(0, org_schema())
        out.append(page(p['path'], p['depth'], p['nav'], p['title'], p['desc'], p['h1'],
                        p['stand'], p.get('tag', ''), p['crumbs'], body, sch))
    for pr in PEOPLE:
        fn = pr['slug'] + '.html'
        title = '%s, %s | Dorfman &amp; Dorfman, CPAs' % (pr['name'], pr['cred'])
        desc = ('%s, %s, of Dorfman &amp; Dorfman, CPAs in Wilmington, Massachusetts. %s'
                % (pr['name'], pr['cred'], re.sub(r'&[a-z]+;', '', pr['line'])))[:174]
        out.append(page('team/%s.html' % pr['slug'], 1, 'about', title, desc,
                        pr['name'] + '.', pr['line'], pr['cred'],
                        (('Home', 'index.html'), ('The firm', 'about.html'),
                         (pr['name'], None)), load(fn),
                        [person_schema(pr),
                         crumb_schema([('Home', 'index.html'), ('The firm', 'about.html'),
                                       (pr['name'], 'team/%s.html' % pr['slug'])])]))
    for fn, (title, desc, h1, stand) in SVC_META.items():
        name = re.sub(r'&[a-z]+;', '', h1).rstrip('.')
        out.append(page('services/' + fn, 1, 'services', title, desc, h1, stand, 'Service',
                        (('Home', 'index.html'), ('Services', 'services/index.html'),
                         (name, None)), load(fn),
                        [service_schema(name, desc, 'services/' + fn),
                         crumb_schema([('Home', 'index.html'),
                                       ('Services', 'services/index.html'),
                                       (name, 'services/' + fn)])]))
    return out


def main():
    os.makedirs(os.path.join(OUT, 'css'), exist_ok=True)
    open(os.path.join(OUT, 'css', 'dd.css'), 'w', encoding='utf-8').write(CSS)
    built = [build_home()] + build_written() + build_calculators()
    print('built %d pages -> %s' % (len(built), OUT))
    return built


if __name__ == '__main__':
    main()
