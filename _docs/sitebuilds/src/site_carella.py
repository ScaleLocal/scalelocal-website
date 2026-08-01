# -*- coding: utf-8 -*-
"""
Charles M. Carella, CPA — North Billerica, Massachusetts
========================================================
A standalone site. It shares NO layout, CSS, component or template with any other
build in this repo. Neither build.py nor site_hickey.py is imported, and neither
must ever be.

THE DESIGN PREMISE
------------------
This firm publishes nothing about itself. No named person, no founding year, no
staff, no history, no office hours, no portal, no payments — the entire "Firm
Profile" on the current site is four sentences of vendor boilerplate. A
conventional marketing site papers over that with stock photography, a team grid
and a card deck. There is nothing to put in them.

So this site is organised around the client's situation rather than the firm's
story, and its whole visual system is typography and space. A person arrives
because something happened — a letter came, a year was never filed, a lender
asked for statements, the first 1099 turned up. The spine of the site is that
list, not a services menu.

Concretely, and deliberately unlike anything else in this repo:
  * a standing left rail — vertical navigation, always visible, with the active
    section's children nested under it. No horizontal bar of any kind.
  * "Start where you are" is the first content block on the homepage. Services
    come third, as running prose, not as cards.
  * six situation pages that are the primary entry points to the site
  * marginal section labels set in the left gutter of the content column
  * ONE typeface at every size. No serif anywhere.
  * no cards, no icons, no numbered badges, no reveal animation, no gradient,
    no hero art, no button pair, no full-bleed reversed CTA band
  * the contact widget is permanent page furniture — part of the rail on desktop,
    a fixed bar on mobile — never a floating pill that opens a panel

Prose is the existing honesty-checked copy, re-laid into the new architecture.
Where new pages needed new copy, every factual claim was verified against irs.gov
and mass.gov on 2026-07-31; see RESEARCH_carellacpa.md.

    python3 site_carella.py
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'carellacpa')
BASE = 'https://www.scalelocal.net/test-builds/carellacpa/'

F = dict(
    name='Charles M. Carella, CPA',
    short='CMC',
    addr='330 Boston Road, Suite 12',
    city='North Billerica', state='MA', state_full='Massachusetts', zip='01862',
    # The extension is dialled after the call connects. It must never appear
    # inside the tel: URI — the firm's current site makes exactly that mistake.
    tel='+19786636419',
    ph='(978) 663-6419',
    ph_disp='(978) 663-6419 ext. 11',
    fax='(978) 663-7260',
    email='CMCCPA@carellacpa.com',
    maps=('https://www.google.com/maps/search/?api=1&query='
          'Charles+M.+Carella+CPA+330+Boston+Road+Suite+12+North+Billerica+MA+01862'),
    mapembed=('https://maps.google.com/maps?q=330+Boston+Road%2C+Suite+12%2C+North+Billerica'
              '%2C+MA+01862&t=&z=15&ie=UTF8&iwloc=&output=embed'),
)

DEMO_BODY = ('Prepared for Charles M. Carella, CPA by ScaleLocal. Not affiliated with, '
             'authorised by, or endorsed by the firm. Reproduction or use of this site '
             'or its contents is prohibited.')
DEMO = 'Demonstration site. ' + DEMO_BODY

# The mark: a squared bracket enclosing a single solid tick. Reads as a C, holds
# at 20px in one flat colour, and is presented to the firm as a proposal — never
# as their existing mark, which does not exist.
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path d="M53 11H11v42h42" fill="none" stroke="currentColor" stroke-width="5.5" '
        'stroke-linecap="square"/>'
        '<rect x="39" y="28" width="9" height="8" fill="currentColor"/></svg>')

FAVICON = (
    "data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2064%2064%27"
    "%3E%3Crect%20width%3D%2764%27%20height%3D%2764%27%20fill%3D%27%231E4437%27/%3E"
    "%3Cpath%20d%3D%27M52%2014H14v36h38%27%20fill%3D%27none%27%20stroke%3D%27%23FCFCFB%27%20stroke-width%3D%276%27/%3E"
    "%3Crect%20x%3D%2738%27%20y%3D%2728%27%20width%3D%279%27%20height%3D%278%27%20fill%3D%27%23FCFCFB%27/%3E%3C/svg%3E")

# --------------------------------------------------------------------------
# Palette. Cool paper, graphite ink, one deep pine accent and nothing else.
# The contrast auditor parses these values straight out of the rendered CSS,
# so this block is the single source of truth.
# --------------------------------------------------------------------------
CSS = r"""
/* Charles M. Carella, CPA — bespoke stylesheet. Shared with no other build. */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --paper:#FCFCFB;
  --panel:#F0F1EC;
  --ink:#131511;
  --soft:#4E5149;
  --faint:#63665D;
  --rule:#DFE0D8;
  --rule2:#C4C7BB;
  /* UI control boundaries need 3:1 against paper (WCAG 1.4.11); --rule2 is 1.67 */
  --field:#8D9087;
  --pine:#1E4437;
  --pinelt:#2C6350;
  --dark:#191B16;
  --sans:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:17px;line-height:1.72;font-weight:400;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  font-feature-settings:"kern","liga";overflow-wrap:break-word}
img{max-width:100%;display:block}
a{color:var(--pine);text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{color:var(--pinelt)}
:focus-visible{outline:2px solid var(--pine);outline-offset:3px;border-radius:1px}
h1,h2,h3,h4{font-weight:700;letter-spacing:-.021em;line-height:1.16;color:var(--ink)}
strong,b{font-weight:700}
.num{font-variant-numeric:tabular-nums lining-nums}
.skip{position:absolute;left:-9999px;top:0;background:var(--pine);color:#fff;
  padding:10px 16px;z-index:99;font-size:14px;font-weight:600}
.skip:focus{left:8px;top:8px}

/* ---------------------------------------------------------- demo notice */
.notice{background:var(--dark);color:#DCDED4;font-size:12.5px;line-height:1.55;
  padding:9px 0;letter-spacing:.005em}
.notice .inner{max-width:1440px;margin:0 auto;padding:0 40px}
.notice b{color:#9EC3B2;font-weight:700}
@media print{.notice{background:#fff;color:#000}.notice b{color:#000}}

/* ------------------------------------------------------------- the shell */
.shell{max-width:1440px;margin:0 auto;padding:0 40px;
  display:grid;grid-template-columns:240px minmax(0,1fr);gap:88px;
  align-items:start}
@media (min-width:1180px){
  .shell{grid-template-columns:216px minmax(0,1fr) 268px;gap:44px}
}
@media (min-width:1400px){
  .shell{grid-template-columns:240px minmax(0,1fr) 292px;gap:60px}
}
.col{padding:52px 0 0;min-width:0}

/* --------------------------------------------------------------- the rail */
.rail{position:sticky;top:0;padding:44px 0 32px;align-self:start;min-width:0;
  max-height:100vh;overflow-y:auto;overscroll-behavior:contain;
  scrollbar-width:thin;scrollbar-color:var(--rule2) transparent}
.rail::-webkit-scrollbar{width:6px}
.rail::-webkit-scrollbar-thumb{background:var(--rule2);border-radius:3px}
.rail::-webkit-scrollbar-track{background:transparent}
.wordmark{display:block;text-decoration:none;color:var(--ink)}
.wordmark .mk{display:block;width:38px;height:38px;color:var(--pine);margin-bottom:14px}
.wordmark .mk svg{width:100%;height:100%;display:block}
.wordmark .nm{font-size:19px;font-weight:700;letter-spacing:-.028em;line-height:1.16;
  display:block}
.wordmark .sb{display:block;margin-top:6px;font-size:10px;font-weight:700;
  letter-spacing:.185em;text-transform:uppercase;color:var(--faint)}
.wordmark:hover .nm{color:var(--pine)}

.railnav{margin-top:28px;border-top:1px solid var(--rule)}
.railnav a{display:block;padding:9px 0;font-size:14.5px;font-weight:600;
  color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule);
  letter-spacing:-.008em}
.railnav a:hover{color:var(--pine)}
.railnav a[aria-current]{color:var(--pine)}
.railnav a[aria-current]::before{content:"";display:inline-block;width:14px;
  height:1.5px;background:var(--pine);vertical-align:middle;margin-right:9px;
  margin-top:-2px}
.railnav .kids{border-bottom:1px solid var(--rule);padding:3px 0 8px}
.railnav .kids a{border:0;padding:4px 0 4px 23px;font-size:13px;font-weight:500;
  line-height:1.45;
  color:var(--soft)}
.railnav .kids a:hover{color:var(--pine)}
.railnav .kids a[aria-current]{color:var(--pine);font-weight:700}
.railnav .kids a[aria-current]::before{display:none}

/* --------------------------------------- reach: permanent contact furniture */
.reach{margin-top:26px;border-top:2px solid var(--ink);padding-top:14px}
.reach .rh{font-size:10px;font-weight:700;letter-spacing:.185em;
  text-transform:uppercase;color:var(--faint);margin-bottom:9px}
.reach .addr{font-size:13.5px;line-height:1.55;color:var(--soft);padding-bottom:10px;
  border-bottom:1px solid var(--rule)}
.reach a{display:block;text-decoration:none;color:var(--ink);padding:8px 0;
  line-height:1.4;
  border-bottom:1px solid var(--rule)}
.reach a:last-of-type{border-bottom:0}
.reach a .t{display:block;font-size:14px;font-weight:700;letter-spacing:-.01em;
  font-variant-numeric:tabular-nums}
.reach a .v{display:block;font-size:13px;color:var(--soft);margin-top:1px;
  font-variant-numeric:tabular-nums}
.reach a:hover .t{color:var(--pine)}
.reach a:hover .v{color:var(--pinelt)}
.reachbar{display:none}

/* ------------------------------------------------ the contact widget itself
   A standing card, always open, never a toggle. It lives in the empty right
   margin the asymmetric column leaves behind, so it covers nothing. Below
   1180px it becomes a fixed bar across the foot of the screen. No script, no
   network call, no third party. */
.deskcard{display:none}
@media (min-width:1180px){
  .deskcard{display:block;position:sticky;top:52px;align-self:start;
    background:var(--paper);border:1px solid var(--rule2);border-top:3px solid var(--pine);
    box-shadow:0 10px 30px rgba(19,21,17,.07)}
  .deskcard .dh{font-size:10px;font-weight:700;letter-spacing:.185em;text-transform:uppercase;
    color:var(--faint);padding:13px 18px 10px}
  .deskcard a{display:block;padding:10px 18px 11px;text-decoration:none;color:var(--ink);
    border-top:1px solid var(--rule)}
  .deskcard a .t{display:block;font-size:14px;font-weight:700;letter-spacing:-.012em;
    line-height:1.35}
  .deskcard a .v{display:block;font-size:12.5px;color:var(--soft);margin-top:1px;
    line-height:1.4}
  .deskcard a:hover{background:var(--panel)}
  .deskcard a:hover .t{color:var(--pine)}
  .deskcard a:hover .v{color:var(--pinelt)}
  .deskcard .dn{padding:10px 18px 12px;font-size:11.5px;line-height:1.5;color:var(--faint);
    border-top:1px solid var(--rule)}
}

/* mobile head: only rendered small, replaces the rail */
.mhead{display:none}

/* ------------------------------------------------------------- page opening */
.open{padding-bottom:8px}
.kicker{font-size:10.5px;font-weight:700;letter-spacing:.185em;text-transform:uppercase;
  color:var(--faint);margin-bottom:22px}
.kicker a{color:var(--faint);text-decoration:none}
.kicker a:hover{color:var(--pine);text-decoration:underline}
.kicker .sep{opacity:.5;padding:0 7px}
h1{font-size:clamp(33px,4.4vw,50px);letter-spacing:-.032em;line-height:1.07;
  max-width:19ch}
.open .stand{margin-top:24px;font-size:20px;line-height:1.58;color:var(--soft);
  max-width:60ch;font-weight:400;letter-spacing:-.008em}
.open.wide h1{max-width:24ch}

/* ------------------------------------------------- band: marginal label + body */
.band{display:grid;grid-template-columns:128px minmax(0,1fr);gap:36px;
  padding:54px 0 0;align-items:start}
.band > .lbl{font-size:10.5px;font-weight:700;letter-spacing:.185em;
  text-transform:uppercase;color:var(--faint);padding-top:7px;line-height:1.6}
.band > .bd{min-width:0}
.band.tight{padding-top:40px}
.band + .band > .bd{border-top:1px solid var(--rule);padding-top:0}
.band + .band{padding-top:0}
.band + .band > .lbl{padding-top:calc(54px + 7px)}
.band + .band > .bd > *:first-child{margin-top:54px}
h2{font-size:27px;letter-spacing:-.028em;line-height:1.2;max-width:27ch}
.bd .lede{margin-top:16px;font-size:18.5px;line-height:1.65;color:var(--soft);
  max-width:64ch}

/* --------------------------------------------------------------------- prose */
.prose{max-width:66ch}
.prose p{margin-top:17px}
.prose h3{font-size:17.5px;margin-top:34px;letter-spacing:-.012em}
.prose h4{font-size:15px;margin-top:26px;letter-spacing:.005em}
.prose h3 + p,.prose h4 + p{margin-top:9px}
.prose ul,.prose ol{margin-top:15px;padding-left:0;list-style:none}
.prose ul li{position:relative;padding-left:20px;margin-top:9px}
.prose ul li::before{content:"";position:absolute;left:0;top:12px;width:9px;
  height:1.5px;background:var(--rule2)}
.prose ol{counter-reset:n}
.prose ol li{position:relative;padding-left:30px;margin-top:9px;counter-increment:n}
.prose ol li::before{content:counter(n) ".";position:absolute;left:0;top:0;
  font-variant-numeric:tabular-nums;color:var(--faint);font-weight:700;font-size:14px}
.prose .after{margin-top:26px;font-size:15px;color:var(--faint);line-height:1.6}

/* a pulled-aside remark. Not a card: two hairlines and indented text. */
.remark{margin:30px 0 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--rule);
  padding:16px 0 17px;max-width:66ch}
.remark .rl{font-size:10.5px;font-weight:700;letter-spacing:.185em;text-transform:uppercase;
  color:var(--pine);margin-bottom:7px}
.remark p{font-size:15.5px;line-height:1.62;color:var(--soft)}
.remark p + p{margin-top:11px}

/* ------------------------------------- index: the situation / page list rows */
.index{margin-top:6px;border-top:1px solid var(--ink);max-width:70ch}
.index a{display:grid;grid-template-columns:minmax(0,1fr) 22px;gap:14px;
  align-items:baseline;padding:19px 0;border-bottom:1px solid var(--rule);
  text-decoration:none;color:var(--ink)}
.index a .t{font-size:18px;font-weight:700;letter-spacing:-.018em;line-height:1.3}
.index a .d{display:block;margin-top:5px;font-size:15px;line-height:1.58;
  color:var(--soft);max-width:58ch;font-weight:400;letter-spacing:0}
.index a .go{justify-self:end;color:var(--rule2);font-size:15px;line-height:1;
  transition:transform .18s ease,color .18s ease}
.index a:hover{background:var(--panel)}
.index a:hover .t{color:var(--pine)}
.index a:hover .go{color:var(--pine);transform:translateX(4px)}
@media (prefers-reduced-motion:reduce){.index a .go{transition:none}}
.index.compact a{padding:14px 0}
.index.compact a .t{font-size:16px}

/* ---------------------------------------------- two-column running services */
.flow{margin-top:8px;columns:2;column-gap:56px}
.flow > div{break-inside:avoid;padding:22px 0;border-top:1px solid var(--rule)}
.flow h3{font-size:16.5px;letter-spacing:-.012em}
.flow p{margin-top:8px;font-size:15px;line-height:1.62;color:var(--soft)}
.flow a{font-weight:600;text-decoration:none}
.flow a:hover{text-decoration:underline}

/* ----------------------------------------------------------- particulars */
.parts{margin-top:8px;border-top:1px solid var(--ink)}
.parts .r{display:grid;grid-template-columns:150px minmax(0,1fr);gap:24px;
  padding:13px 0;border-bottom:1px solid var(--rule)}
.parts .k{font-size:12.5px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  color:var(--faint);padding-top:3px}
.parts .v{font-size:16.5px;font-variant-numeric:tabular-nums;line-height:1.5}
.parts .v a{text-decoration:none;font-weight:600}
.parts .v a:hover{text-decoration:underline}
.parts .v small{display:block;font-size:13px;color:var(--faint);margin-top:3px;
  font-variant-numeric:normal}

/* ------------------------------------------------------------------- map */
.map{margin-top:26px;border:1px solid var(--field);background:var(--panel)}
.map iframe{width:100%;height:340px;border:0;display:block;filter:grayscale(.35)}
.mapnote{margin-top:10px;font-size:13px;color:var(--faint)}

/* ------------------------------------------------------------- questions */
.qa{max-width:68ch}
.qa .q{border-top:1px solid var(--rule);padding:24px 0 4px}
.qa .q:first-child{border-top:1px solid var(--ink)}
.qa h3{font-size:17.5px;letter-spacing:-.014em;max-width:52ch}
.qa p{margin-top:11px;font-size:16px;line-height:1.68;color:var(--soft)}
.qa .q > p:last-child{margin-bottom:20px}
.qa h2.grp{font-size:10.5px;font-weight:700;letter-spacing:.185em;text-transform:uppercase;
  color:var(--pine);margin:44px 0 -4px;line-height:1.6}
.qa h2.grp:first-child{margin-top:0}

/* ------------------------------------------------------------------ table */
.tscroll{margin-top:20px;overflow-x:auto;-webkit-overflow-scrolling:touch}
table.plain{border-collapse:collapse;width:100%;min-width:440px;font-size:15px}
table.plain th,table.plain td{text-align:left;padding:11px 18px 11px 0;
  border-bottom:1px solid var(--rule);vertical-align:top;line-height:1.55}
table.plain th{font-size:11.5px;font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint);border-bottom:1px solid var(--ink)}
table.plain td.n{font-variant-numeric:tabular-nums;white-space:nowrap}

/* ------------------------------------------------------------- calculator */
.calc{margin-top:8px;display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:48px;
  align-items:start}
@media (min-width:1180px) and (max-width:1560px){
  .calc{grid-template-columns:minmax(0,1fr);gap:0}
  .calcout{position:static;margin-top:32px}
}
.calcform{min-width:0;border-top:1px solid var(--ink)}
.calcform .row{padding:15px 0;border-bottom:1px solid var(--rule);
  display:grid;grid-template-columns:minmax(0,1fr) 168px;gap:20px;align-items:center}
.calcform label{font-size:15px;font-weight:600;line-height:1.4}
.calcform .ifield{display:flex;align-items:center;border:1px solid var(--field);
  background:#fff;height:40px}
.calcform .ifield:focus-within{border-color:var(--pine);box-shadow:0 0 0 2px rgba(30,68,55,.13)}
.calcform .pre,.calcform .suf{font-size:13px;color:var(--faint);padding:0 10px;
  font-weight:600;flex:0 0 auto}
.calcform .pre{border-right:1px solid var(--rule)}
.calcform .suf{border-left:1px solid var(--rule)}
.calcform input{width:100%;min-width:0;border:0;background:transparent;height:100%;
  padding:0 10px;font:inherit;font-size:15.5px;font-variant-numeric:tabular-nums;
  color:var(--ink);text-align:right}
.calcform input:focus{outline:0}
.calcform .hint{grid-column:1/-1;font-size:13px;color:var(--faint);margin-top:-2px}
.calcnote{margin-top:18px;font-size:13.5px;line-height:1.6;color:var(--faint);
  max-width:60ch}
.calcout{position:sticky;top:24px;min-width:0}
.calcout .big{border-top:2px solid var(--ink);padding-top:14px}
.calcout .big .l{font-size:10.5px;font-weight:700;letter-spacing:.185em;
  text-transform:uppercase;color:var(--faint)}
.calcout .big .v{font-size:38px;font-weight:700;letter-spacing:-.035em;margin-top:6px;
  font-variant-numeric:tabular-nums lining-nums;line-height:1.1;color:var(--pine)}
.calcout dl{margin-top:22px;border-top:1px solid var(--rule)}
.calcout .orow{display:flex;justify-content:space-between;gap:16px;padding:10px 0;
  border-bottom:1px solid var(--rule);align-items:baseline}
.calcout dt{font-size:14px;color:var(--soft);line-height:1.45}
.calcout dd{font-size:15.5px;font-weight:700;font-variant-numeric:tabular-nums;
  white-space:nowrap}
.calcout .onote{font-size:12.5px;color:var(--faint);line-height:1.55;padding:8px 0 2px}

/* ------------------------------------------------------------------ footer */
.foot{margin-top:76px;border-top:1px solid var(--rule);padding:34px 0 0}
.foot .fn{font-size:15px;font-weight:700;letter-spacing:-.015em}
.foot .fa{margin-top:6px;font-size:14.5px;color:var(--soft);line-height:1.65;
  font-variant-numeric:tabular-nums}
.foot .fa a{color:var(--soft);text-decoration:none}
.foot .fa a:hover{color:var(--pine);text-decoration:underline}
.foot .flinks{margin-top:20px;font-size:14px;line-height:2}
.foot .flinks a{color:var(--ink);text-decoration:none;font-weight:500}
.foot .flinks a:hover{color:var(--pine);text-decoration:underline}
.foot .flinks .sep{color:var(--rule2);padding:0 9px}
.foot .fine{margin-top:24px;padding:16px 0 40px;border-top:1px solid var(--rule);
  font-size:12.5px;line-height:1.65;color:var(--faint);max-width:78ch}

/* ============================================================== responsive */
@media (max-width:1080px){
  .shell{grid-template-columns:210px minmax(0,1fr);gap:56px;padding:0 30px}
  .calc{grid-template-columns:minmax(0,1fr) 260px;gap:36px}
  .band{grid-template-columns:110px minmax(0,1fr);gap:26px}
}
@media (max-width:900px){
  .notice .inner{padding:0 22px}
  .shell{display:block;padding:0 22px;max-width:720px}
  .rail{position:static;padding:26px 0 0}
  .col{padding-top:30px}
  .rail .railnav,.rail .reach{display:none}
  .mhead{display:block;border-top:1px solid var(--rule);margin-top:22px}
  .mhead summary{list-style:none;cursor:pointer;padding:13px 0;font-size:13px;
    font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);
    display:flex;justify-content:space-between;align-items:center;
    border-bottom:1px solid var(--rule)}
  .mhead summary::-webkit-details-marker{display:none}
  .mhead summary .x{font-weight:400;color:var(--faint);font-size:17px;line-height:1}
  .mhead[open] summary .x{transform:rotate(45deg)}
  .mhead nav a{display:block;padding:11px 0;font-size:15.5px;font-weight:600;
    color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}
  .mhead nav .kids a{padding-left:20px;font-size:14px;font-weight:500;color:var(--soft)}
  .wordmark .mk{width:30px;height:30px;margin-bottom:12px}
  .band{display:block;padding-top:40px}
  .band > .lbl{padding:0 0 12px}
  .band + .band > .lbl{padding-top:40px}
  .band + .band > .bd > *:first-child{margin-top:0}
  .band + .band > .bd{border-top:0}
  .band + .band{padding-top:0;border-top:1px solid var(--rule)}
  .flow{columns:1}
  .calc{display:block}
  .calcout{position:static;margin-top:34px}
  .parts .r{grid-template-columns:120px minmax(0,1fr);gap:16px}
  .foot{margin-top:56px}
}
@media (max-width:1179px){
  .reachbar{display:grid;position:fixed;left:0;right:0;bottom:0;z-index:50;
    grid-template-columns:repeat(3,1fr);background:var(--paper);
    border-top:3px solid var(--pine);box-shadow:0 -8px 22px rgba(19,21,17,.10);
    max-width:680px;margin:0 auto;border-left:1px solid var(--rule2);
    border-right:1px solid var(--rule2)}
  .reachbar a{display:block;padding:11px 6px 12px;text-align:center;
    text-decoration:none;color:var(--ink);border-left:1px solid var(--rule)}
  .reachbar a:first-child{border-left:0}
  .reachbar a:hover{background:var(--panel)}
  .reachbar .t{display:block;font-size:13px;font-weight:700;letter-spacing:-.01em}
  .reachbar .v{display:block;font-size:11px;color:var(--faint);margin-top:2px;
    font-variant-numeric:tabular-nums;line-height:1.3}
  .foot .fine{padding-bottom:104px}
}
@media (max-width:520px){
  .calcform .row{grid-template-columns:minmax(0,1fr);gap:8px}
  .calcform .ifield{max-width:200px}
  .parts .r{display:block}
  .parts .k{padding-bottom:2px}
  .index a{grid-template-columns:minmax(0,1fr)}
  .index a .go{display:none}
  h1{font-size:clamp(29px,8vw,36px)}
}
@media print{
  .rail,.mhead,.reachbar,.map{display:none}
  .shell{display:block;max-width:none;padding:0}
  body{font-size:12pt}
}
"""

# ==========================================================================
# Navigation. A standing vertical rail; the active section's children nest
# under it. Seven top-level entries — which is precisely why this site can
# have a situations spine and a horizontal bar could not.
# ==========================================================================
NAV = [
    ('situations/index.html', 'Start where you are', 'situations'),
    ('services/index.html',   'What the office does', 'services'),
    ('calculators/index.html', 'Calculators',        'calculators'),
    ('what-to-bring.html',    'What to bring',       'bring'),
    ('questions.html',        'Common questions',    'questions'),
    ('about.html',            'About the office',    'about'),
    ('contact.html',          'Contact',             'contact'),
]

SITUATIONS = [
    ('situations/irs-notice.html', 'A letter arrived from the IRS or DOR',
     'Most notices are automated and many are simply wrong. The part that matters is '
     'the date printed on it.'),
    ('situations/unfiled-years.html', 'There are years that were never filed',
     'More common than people assume, and the only version of it that gets worse is '
     'the one left alone.'),
    ('situations/self-employed.html', 'Income is arriving with no tax withheld',
     'A first 1099, a side business, a K-1. Nobody is withholding, so the quarterly '
     'obligation is now yours.'),
    ('situations/new-business.html', 'A business is starting, or changing shape',
     'How it is organised decides which return it files, when it is due, and how the '
     'profit reaches you.'),
    ('situations/financial-statements.html', 'Someone has asked for financial statements',
     'A lender, a landlord or a bonding company. Which level of service they actually '
     'need is worth establishing first.'),
    ('situations/two-states.html', 'A move into or out of Massachusetts',
     'Part-year and non-resident apportionment is one of the more common reasons a '
     'return has to be amended.'),
]

SERVICES = [
    ('services/tax.html', 'Tax preparation and planning',
     'Federal and Massachusetts returns for individuals and small businesses, and the '
     'decisions that have to be made before the year closes.'),
    ('services/bookkeeping.html', 'Accounting and bookkeeping',
     'The monthly discipline underneath everything else: a chart of accounts that fits '
     'the business, and accounts that reconcile.'),
    ('services/financial-statements.html', 'Financial statement preparation',
     'Statements a lender, a landlord or an owner can read, and a straight answer about '
     'which level of service the request requires.'),
    ('services/consulting.html', 'Business consulting',
     'The questions that arrive between filings: how to organise, what a hire costs, '
     'whether to buy the equipment.'),
]

# Children shown in the rail when their section is the active one.
KIDS = {
    'situations': [(p, t) for p, t, _ in SITUATIONS],
    'services': [(p, t) for p, t, _ in SERVICES],
}


def rel(depth, target):
    """Resolve a root-relative path for a page that sits `depth` directories down."""
    if target.startswith(('http', 'mailto:', 'tel:', '#')):
        return target
    return ('../' * depth) + target


def esc(s):
    return H.escape(s, quote=True)


def railnav(depth, active, calc_kids):
    kids = dict(KIDS)
    kids['calculators'] = calc_kids
    out = ['<nav class="railnav" aria-label="Sections">']
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        out.append('<a href="%s"%s>%s</a>' % (rel(depth, href), cur, label))
        if key == active and key in kids:
            out.append('<div class="kids">')
            for kh, kt in kids[key]:
                out.append('<a href="%s">%s</a>' % (rel(depth, kh), kt))
            out.append('</div>')
    out.append('</nav>')
    return ''.join(out)


def mobilenav(depth, active, calc_kids):
    kids = dict(KIDS)
    kids['calculators'] = calc_kids
    out = ['<details class="mhead"><summary>Sections<span class="x">&#43;</span></summary>'
           '<nav aria-label="Sections">']
    for href, label, key in NAV:
        out.append('<a href="%s">%s</a>' % (rel(depth, href), label))
        if key == active and key in kids:
            out.append('<div class="kids">')
            for kh, kt in kids[key]:
                out.append('<a href="%s">%s</a>' % (rel(depth, kh), kt))
            out.append('</div>')
    out.append('</nav></details>')
    return ''.join(out)


def reach(depth):
    """The office's particulars in the rail. NOT the contact widget — that is
    `deskcard` on wide viewports and `reachbar` below them, and it owns the
    actions. This is here so the address and number are on screen while reading."""
    return (
        '<div class="reach">'
        '<div class="rh">The office</div>'
        '<p class="addr">%s<br>%s, %s %s</p>'
        '<a href="tel:%s"><span class="t">%s</span>'
        '<span class="v">Telephone</span></a>'
        '<a href="mailto:%s"><span class="t">Email the office</span>'
        '<span class="v">%s</span></a>'
        '</div>'
    ) % (F['addr'], F['city'], F['state'], F['zip'], F['tel'], F['ph_disp'],
         F['email'], F['email'])


def deskcard(depth):
    """The contact widget on wide viewports. Always open — there is nothing to
    click before you can use it — and parked in the empty right margin, so it
    never covers a line of text."""
    return (
        '<aside class="deskcard" data-contact-widget aria-label="Contact the office">'
        '<div class="dh">Speak to the office</div>'
        '<a href="tel:%s"><span class="t">Call</span>'
        '<span class="v num">%s</span></a>'
        '<a href="mailto:%s"><span class="t">Email</span>'
        '<span class="v">%s</span></a>'
        '<a href="%s"><span class="t">Request an appointment</span>'
        '<span class="v">What a first call covers</span></a>'
        '<p class="dn">Dial the extension once the call connects.</p>'
        '</aside>'
    ) % (F['tel'], F['ph_disp'], F['email'], F['email'],
         rel(depth, 'contact.html#appointment'))


def reachbar(depth):
    return (
        '<div class="reachbar" data-contact-widget role="group" aria-label="Contact the office">'
        '<a href="tel:%s"><span class="t">Call</span><span class="v num">%s</span></a>'
        '<a href="mailto:%s"><span class="t">Email</span><span class="v">Write to the office</span></a>'
        '<a href="%s"><span class="t">Appointment</span><span class="v">Arrange a time</span></a>'
        '</div>'
    ) % (F['tel'], F['ph'], F['email'], rel(depth, 'contact.html#appointment'))


def footer(depth):
    links = [('situations/index.html', 'Start where you are'),
             ('services/index.html', 'What the office does'),
             ('calculators/index.html', 'Calculators'),
             ('what-to-bring.html', 'What to bring'),
             ('questions.html', 'Common questions'),
             ('about.html', 'About the office'),
             ('contact.html', 'Contact')]
    row = ('<span class="sep">&middot;</span>'.join(
        '<a href="%s">%s</a>' % (rel(depth, h), t) for h, t in links))
    return (
        '<footer class="foot">'
        '<div class="fn">%s</div>'
        '<div class="fa">%s, %s, %s %s<br>'
        '<a href="tel:%s" class="num">%s</a> &middot; facsimile <span class="num">%s</span><br>'
        '<a href="mailto:%s">%s</a></div>'
        '<div class="flinks">%s</div>'
        '<p class="fine">%s</p>'
        '</footer>'
    ) % (F['name'], F['addr'], F['city'], F['state'], F['zip'],
         F['tel'], F['ph_disp'], F['fax'], F['email'], F['email'], row, DEMO)


def kicker(depth, crumbs):
    if not crumbs:
        return ''
    parts = []
    for label, href in crumbs:
        if href:
            parts.append('<a href="%s">%s</a>' % (rel(depth, href), label))
        else:
            parts.append('<span>%s</span>' % label)
    return '<div class="kicker">%s</div>' % '<span class="sep">/</span>'.join(parts)


def page(path, depth, nav, title, desc, h1, stand='', crumbs=(), body='',
         schema=(), wide=False, tail='', calc_kids=()):
    """Render one page to OUT/<path>."""
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
        '<meta name="theme-color" content="#1E4437">'
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="%(name)s">'
        '<meta property="og:title" content="%(title)s">'
        '<meta property="og:description" content="%(desc)s">'
        '<meta property="og:url" content="%(url)s">'
        '<meta property="og:image" content="%(base)sog.png">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Charles M. Carella, CPA &mdash; North Billerica, Massachusetts">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="%(title)s">'
        '<meta name="twitter:description" content="%(desc)s">'
        '<meta name="twitter:image" content="%(base)sog.png">'
        '<link rel="apple-touch-icon" href="%(atouch)s">'
        '<link rel="icon" type="image/svg+xml" href="%(fav)s">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="%(css)s">'
        '%(ld)s</head>'
    ) % dict(title=esc(title), desc=esc(desc), url=url, name=esc(F['name']),
             base=BASE, css=rel(depth, 'css/carella.css'), fav=FAVICON,
             atouch=rel(depth, 'apple-touch-icon.png'), ld=ld)

    doc = (
        head +
        '<body>'
        '<a class="skip" href="#main">Skip to content</a>'
        '<div class="notice" role="note"><div class="inner"><b>Demonstration site.</b> '
        + DEMO_BODY + '</div></div>'
        '<div class="shell">'
        '<div class="rail">'
        '<a class="wordmark" href="' + rel(depth, 'index.html') + '">'
        '<span class="mk">' + MARK + '</span>'
        '<span class="nm">Charles M.<br>Carella, CPA</span>'
        '<span class="sb">Certified Public Accountant</span></a>'
        + railnav(depth, nav, calc_kids)
        + reach(depth)
        + mobilenav(depth, nav, calc_kids) +
        '</div>'
        '<main class="col" id="main">'
        '<div class="open' + (' wide' if wide else '') + '">'
        + kicker(depth, crumbs) +
        '<h1>' + h1 + '</h1>'
        + ('<p class="stand">' + stand + '</p>' if stand else '') +
        '</div>'
        + body
        + footer(depth) +
        '</main>'
        + deskcard(depth) +
        '</div>'
        + reachbar(depth)
        + tail +
        '</body></html>'
    )
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(doc)
    return path


# --------------------------------------------------------------- schema bits
def org_schema():
    return {
        '@context': 'https://schema.org', '@type': 'AccountingService',
        '@id': BASE + '#firm', 'name': F['name'], 'url': BASE,
        'email': F['email'], 'telephone': F['ph_disp'], 'faxNumber': F['fax'],
        'address': {'@type': 'PostalAddress', 'streetAddress': F['addr'],
                    'addressLocality': F['city'], 'addressRegion': F['state'],
                    'postalCode': F['zip'], 'addressCountry': 'US'},
        'hasMap': F['maps'],
    }


def crumb_schema(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': i + 1, 'name': n,
                 'item': BASE + (u if u != 'index.html' else '')}
                for i, (n, u) in enumerate(items)]}


def page_schema(name, path, desc):
    return {'@context': 'https://schema.org', '@type': 'WebPage', 'name': name,
            'description': desc,
            'url': BASE + ('' if path == 'index.html' else path),
            'isPartOf': {'@id': BASE + '#firm'}}


def faq_schema(pairs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                           for q, a in pairs]}


def service_schema(name, desc, path):
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': name,
            'description': desc, 'url': BASE + path,
            'provider': {'@id': BASE + '#firm'},
            'areaServed': {'@type': 'State', 'name': 'Massachusetts'}}


# ------------------------------------------------------------ small builders
def band(label, body_html, tight=False):
    return ('<section class="band%s"><div class="lbl">%s</div><div class="bd">%s</div></section>'
            % (' tight' if tight else '', label, body_html))


def index_rows(depth, rows, compact=False):
    out = ['<div class="index%s">' % (' compact' if compact else '')]
    for href, title, desc in rows:
        out.append('<a href="%s"><span><span class="t">%s</span>'
                   '<span class="d">%s</span></span>'
                   '<span class="go" aria-hidden="true">&rarr;</span></a>'
                   % (rel(depth, href), title, desc))
    out.append('</div>')
    return ''.join(out)


def parts_rows(rows):
    out = ['<div class="parts">']
    for k, v in rows:
        out.append('<div class="r"><div class="k">%s</div><div class="v">%s</div></div>' % (k, v))
    out.append('</div>')
    return ''.join(out)


def remark(label, *paras):
    return ('<div class="remark"><div class="rl">%s</div>%s</div>'
            % (label, ''.join('<p>%s</p>' % p for p in paras)))


def mapblock():
    return ('<div class="map"><iframe title="Interactive Google map showing the office at '
            '330 Boston Road, Suite 12, North Billerica, Massachusetts" src="%s" '
            'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>'
            '<p class="mapnote">Pan, zoom, or <a href="%s" target="_blank" rel="noopener">'
            'open the map full screen</a> for turn-by-turn directions.</p>'
            % (F['mapembed'], F['maps']))


def qa_block(groups):
    """groups: list of (group_label_or_None, [(q, a_html), ...])"""
    out = ['<div class="qa">']
    for label, items in groups:
        if label:
            out.append('<h2 class="grp">%s</h2>' % label)
        for q, a in items:
            out.append('<div class="q"><h3>%s</h3>%s</div>' % (q, a))
    out.append('</div>')
    return ''.join(out)

# ==========================================================================
# CONTENT
# Prose below is the firm's honesty-checked copy from the previous build,
# re-laid into this architecture, plus new copy for the situation pages whose
# every factual claim was verified against irs.gov and mass.gov on 2026-07-31.
# Nothing here asserts a person, a founding year, a headcount, office hours,
# a credential beyond "CPA", a membership, a specialism or a client facility
# the firm does not publish.
# ==========================================================================

def build_home():
    d = 0
    calc_kids = [('calculators/' + c['slug'] + '.html', c['title']) for c in CALCS]

    b = band('Where to start',
        '<h2>Most people arrive because something happened.</h2>'
        '<p class="lede">A letter came. A year was never filed. A lender asked for '
        'statements. The first 1099 turned up and nobody withheld anything. Start with '
        'whichever of these is closest to your situation &mdash; each one sets out what '
        'is actually involved before you pick up the phone.</p>'
        + index_rows(d, SITUATIONS))

    flow = '<div class="flow">'
    for href, title, desc in SERVICES:
        flow += ('<div><h3>%s</h3><p>%s</p><p><a href="%s">Read more &rarr;</a></p></div>'
                 % (title, desc, rel(d, href)))
    flow += '</div>'

    b += band('The work',
        '<h2>Four services, and they are the same conversation.</h2>'
        '<p class="lede">For somebody who owns a small business, the return, the books, '
        'the statements a lender asks for and the decision about next year are not '
        'separate problems. They are one problem looked at from four directions, which '
        'is the argument for handling them in one place.</p>' + flow)

    b += band('The office',
        '<h2>330 Boston Road, North Billerica.</h2>'
        + parts_rows([
            ('Address', '%s<br>%s, %s %s' % (F['addr'], F['city'], F['state'], F['zip'])),
            ('Telephone', '<a href="tel:%s" class="num">%s</a>'
                          '<small>The extension is dialled after the call connects.</small>'
                          % (F['tel'], F['ph_disp'])),
            ('Facsimile', '<span class="num">%s</span>' % F['fax']),
            ('Email', '<a href="mailto:%s">%s</a>' % (F['email'], F['email'])),
            ('Appointments', 'Call or email to arrange a time'),
        ])
        + mapblock())

    b += band('Tools',
        '<h2>Eight calculators that run on this page.</h2>'
        '<p class="lede">Mortgage and refinance, loans, retirement and college saving, '
        'self-employment tax, equipment purchases and break-even. No third-party script, '
        'no sign-in, nothing stored &mdash; the arithmetic happens in your browser and stops '
        'there.</p>'
        + index_rows(d, [('calculators/%s.html' % c['slug'], c['title'], c['blurb'])
                         for c in CALCS], compact=True))

    b += band('Before you call',
        '<h2>Worth reading first.</h2>'
        + index_rows(d, [
            ('what-to-bring.html', 'What to bring',
             'The full list, by category, of what to gather before an appointment.'),
            ('questions.html', 'Common questions',
             'Deadlines, notices, records, extensions, and what a CPA licence actually means.'),
            ('about.html', 'About the office',
             'What the credential is, how an engagement runs, and what confidentiality covers.'),
            ('contact.html', 'Contact the office',
             'What a first call covers and what to have in front of you when you make it.'),
        ], compact=True))

    return page('index.html', d, 'home',
        'Charles M. Carella, CPA | North Billerica, Massachusetts',
        'Certified Public Accountant at 330 Boston Road in North Billerica, Massachusetts. '
        'Tax preparation and planning, bookkeeping, financial statements and business consulting.',
        'Tax and accounting for people and the businesses they run.',
        'A Certified Public Accountant&rsquo;s office at 330 Boston Road in North Billerica. '
        'Tax preparation and planning, accounting and bookkeeping, financial statement '
        'preparation, and business consulting &mdash; for individuals and for small businesses.',
        (), b, [org_schema(), {'@context': 'https://schema.org', '@type': 'WebSite',
                               'name': F['name'], 'url': BASE,
                               'publisher': {'@id': BASE + '#firm'}}],
        wide=True, calc_kids=calc_kids)


def build_about():
    d = 0
    b = band('The credential',
        '<div class="prose">'
        '<h2>What a CPA licence is.</h2>'
        '<p>Anybody may prepare a tax return for payment provided they hold a preparer tax '
        'identification number. The bar for calling yourself an accountant is lower still: '
        'there is not one.</p>'
        '<p>A Certified Public Accountant is licensed by a state board. The licence requires '
        'passing the Uniform CPA Examination, meeting education and experience requirements, '
        'and then continuing to meet professional education requirements to keep it. '
        'It carries a code of professional conduct with a disciplinary process attached, and '
        'it can be revoked.</p>'
        '<p>Two consequences matter to a client. A CPA has unlimited rights to represent a '
        'taxpayer before the IRS &mdash; in an examination, in collection, on appeal &mdash; '
        'which most paid preparers do not. And the same licence covers the work either side '
        'of the return: the books it is built from, the statements a lender asks for, and the '
        'structural questions that decide what next year&rsquo;s return will look like.</p>'
        '</div>')

    b += band('The engagement',
        '<div class="prose" id="engagement">'
        '<h2>How the work runs, in the order it runs.</h2>'
        '<p>Accounting work has a shape, and it is worth knowing before you start.</p>'
        '<h3>The first conversation</h3>'
        '<p>Short, and mostly diagnostic: what kind of return or engagement this is, roughly '
        'what the year looked like, whether there is a business and how it is organised, and '
        'what deadline is driving the question. That is normally enough to establish whether the '
        'work is a tax matter, an accounting matter, or both, and what it involves.</p>'
        '<p>The most useful thing you can do in that conversation is describe the awkward '
        'part. Unfiled years, a notice sitting on the desk, books that stopped reconciling in '
        'June, a business partner who left &mdash; none of those are unusual, and all of them '
        'change the order of the work. Discovered at the start they are a plan. Discovered at '
        'the end they are a problem.</p>'
        '<h3>Gathering</h3>'
        '<p>Then the records. Completeness here decides most of what follows: a complete file '
        'produces fewer questions, a shorter engagement and a lower chance of an amended '
        'return later. <a href="what-to-bring.html">The list is here.</a></p>'
        '<h3>The work</h3>'
        '<p>Preparation, and then the questions that come out of it. Anything unusual in your '
        'year is a reason to ask rather than to assume, and the questions are better delivered '
        'in one batch than as a trickle over three weeks.</p>'
        '<h3>Review and filing</h3>'
        '<p>Nothing goes anywhere before you have signed for it, and that is a rule rather '
        'than a courtesy: IRS e-file rules require the taxpayer to sign the authorisation '
        'before an electronic return originator may transmit the return. A paid preparer must also sign '
        'the return and furnish you with a complete copy of it. Keep the copy. It is the '
        'starting point for next year, for a lender, and for anything that surfaces '
        'afterwards.</p>'
        '<h3>The year that is still open</h3>'
        '<p>Filing closes a year that has already happened. Almost every decision that changes '
        'a tax bill belongs to the year that has not finished yet &mdash; how the business is '
        'organised, what the owner takes as wages against distributions, when equipment is '
        'bought, whether a retirement plan contribution gets made, how a sale is structured. '
        'Which is why an autumn conversation is generally worth more than an April one.</p>'
        '</div>'
        + remark('On scope and fees',
                 'This site describes the services offered and what the work generally '
                 'involves. What your own engagement covers, how long it takes and what it '
                 'costs are settled in conversation with the office &mdash; there is no '
                 'published fee schedule, because the work is not uniform.'))

    b += band('Confidentiality',
        '<div class="prose">'
        '<h2>What confidentiality covers.</h2>'
        '<p>Client information is confidential. For a CPA that is a professional obligation '
        'with enforcement behind it rather than an internal policy, and it covers the fact of '
        'the engagement as well as its contents.</p>'
        '<p>Federal law adds a further restriction specific to tax work: information supplied '
        'for the preparation of a return may not be used for another purpose, or disclosed to '
        'anybody else, without the taxpayer&rsquo;s written consent.</p>'
        '</div>')

    b += band('Next',
        index_rows(d, [
            ('services/index.html', 'What the office does',
             'The four practice areas, each in detail.'),
            ('what-to-bring.html', 'What to bring',
             'What to gather before an appointment, by category.'),
            ('questions.html', 'Common questions',
             'The things people ask before they call.'),
        ], compact=True))

    return page('about.html', d, 'about',
        'About the office | Charles M. Carella, CPA',
        'What a CPA licence means, how an accounting engagement runs from first call to '
        'filing, and what professional confidentiality covers in practice.',
        'About the work.',
        'A short account of what this office does, what the licence behind it means, and how '
        'an engagement actually runs.',
        (('Home', 'index.html'), ('About the office', None)), b,
        [page_schema('About the office', 'about.html',
                     'What a CPA licence means and how an engagement runs.'),
         crumb_schema([('Home', 'index.html'), ('About the office', 'about.html')])])


def build_bring():
    d = 0
    b = band('Everyone',
        '<div class="prose">'
        '<h2>Whatever else is true, bring these.</h2>'
        '<ul>'
        '<li>Last year&rsquo;s federal and state returns, complete, including the schedules</li>'
        '<li>Names, dates of birth and Social Security numbers for everyone on the return</li>'
        '<li>Bank details if a refund is to be deposited directly</li>'
        '<li>Any notice received from the IRS or the Massachusetts Department of Revenue, '
        'with its envelope</li>'
        '</ul></div>')

    b += band('Income',
        '<div class="prose">'
        '<h2>Everything that paid you.</h2>'
        '<ul>'
        '<li>W-2 forms, and the 1099 forms &mdash; interest, dividends, retirement '
        'distributions, brokerage proceeds, contract income, state refunds</li>'
        '<li>Brokerage statements showing cost basis for anything sold, not just the '
        'proceeds</li>'
        '<li>K-1 forms from a partnership, an S corporation, a trust or an estate</li>'
        '<li>Rental income and the expenses against it</li>'
        '<li>Records of any income that arrived without a form attached to it</li>'
        '</ul></div>')

    b += band('Deductions',
        '<div class="prose">'
        '<h2>Deductions, credits and payments.</h2>'
        '<ul>'
        '<li>Mortgage interest and property tax statements</li>'
        '<li>Tuition statements, student loan interest, and childcare paid, with the '
        'provider&rsquo;s identification number</li>'
        '<li>Retirement and health savings account contributions made outside payroll</li>'
        '<li>Charitable receipts, and written acknowledgement for anything substantial</li>'
        '<li>Health coverage forms</li>'
        '<li>Estimated tax payments made during the year, with the dates and amounts</li>'
        '</ul></div>')

    b += band('If there is a business',
        '<div class="prose">'
        '<h2>The business file.</h2>'
        '<ul>'
        '<li>The books for the year, or the bank and card statements if there are no books</li>'
        '<li>A depreciation schedule, and details of anything bought or sold during the year</li>'
        '<li>Payroll reports and any 1099 forms issued to contractors</li>'
        '<li>Loan statements showing the year-end balance and the interest paid</li>'
        '<li>The formation documents and any election filed &mdash; especially an S election '
        '&mdash; if this is a first engagement</li>'
        '</ul></div>')

    b += band('Anything that changed',
        '<div class="prose">'
        '<h2>The year&rsquo;s events, not just its paperwork.</h2>'
        '<p>A marriage or a divorce, a birth, a death, a house bought or sold, a move to or '
        'from another state, a business started or closed, a large gift given or received, an '
        'inheritance, a retirement, a first year of self-employment.</p>'
        '<p>Each of these changes the return, and each is easier to handle when it is '
        'mentioned at the start.</p>'
        '</div>'
        + remark('If something is missing',
                 'Say so at the start rather than working around it. A gap usually changes '
                 'the order of the work rather than whether it can be done &mdash; and it is '
                 'far cheaper to plan around at the beginning than to discover with a deadline '
                 'running.'))

    return page('what-to-bring.html', d, 'bring',
        'What to bring | Charles M. Carella, CPA',
        'What to gather before a tax appointment, by category: prior returns, income forms, '
        'deductions, the business file, and the events that changed your year.',
        'What to bring.',
        'More is better than less, and a gap is worth mentioning rather than working around. '
        'The list below covers the ordinary case.',
        (('Home', 'index.html'), ('What to bring', None)), b,
        [page_schema('What to bring', 'what-to-bring.html',
                     'What to gather before a tax appointment.'),
         crumb_schema([('Home', 'index.html'), ('What to bring', 'what-to-bring.html')])])


FAQS = [
 ('Working with a CPA', [
  ('What does a CPA do that other tax preparers do not?',
   '<p>Anyone with a preparer tax identification number may prepare a return for a fee. A '
   'Certified Public Accountant has passed the Uniform CPA Examination and holds an active '
   'state licence, which carries continuing education requirements and a professional code of '
   'conduct with enforcement behind it.</p>'
   '<p>The practical difference shows up in two places. A CPA has unlimited rights to '
   'represent a taxpayer before the IRS &mdash; in an examination, in collection, on appeal '
   '&mdash; which most preparers do not. And a CPA can work across the whole picture rather '
   'than the return alone: the books that feed it, the statements a lender wants, and the '
   'structural questions that decide next year&rsquo;s number.</p>'),
  ('Do you work with businesses as well as individuals?',
   '<p>Both. This office prepares returns and plans for individuals and for small businesses, '
   'and does the accounting and bookkeeping, financial statement preparation and business '
   'consulting behind them. For an owner-operated business that combination is the point: the '
   'entity return, the owner&rsquo;s return and the books are one problem seen from three '
   'sides.</p>'),
  ('What does it cost?',
   '<p>There is no published fee schedule, because the work is not uniform. What a return or '
   'an engagement takes depends on how many moving parts there are and on the condition of the '
   'records it is built from &mdash; which is why the useful first step is a short call '
   'describing the situation rather than a price list. Call <a href="tel:+19786636419" '
   'class="num">(978) 663-6419 ext. 11</a> and describe what you have.</p>'),
  ('What should I bring to the first appointment?',
   '<p>Last year&rsquo;s return, this year&rsquo;s income documents, and anything that '
   'changed. The <a href="what-to-bring.html">full list is here</a>, but the general rule is '
   'that more is better and gaps are worth mentioning rather than working around. If something '
   'is missing, say so at the start &mdash; it usually changes the order of the work rather '
   'than whether it can be done.</p>'),
  ('How do I get my documents to the office?',
   '<p>Call the office and ask. Which route makes sense depends on what you have and what form '
   'it is in, and it is a two-minute conversation rather than something worth guessing at. The '
   'office is at 330 Boston Road, Suite 12, in North Billerica.</p>'),
 ]),
 ('Deadlines, notices and records', [
  ('Is it too late to do anything about this year?',
   '<p>It depends what month it is. Before 31 December, most things are still open &mdash; the '
   'timing of income and purchases, retirement plan contributions, how a transaction is '
   'structured, whether an entity election makes sense. After 31 December the list shortens to '
   'a handful of items: certain self-employed retirement contributions, an IRA, and a few '
   'accounting method questions. That is the argument for an autumn conversation.</p>'),
  ('I have not filed for a few years. What happens now?',
   '<p>It is a more common situation than people assume, and it does not improve while it is '
   'left. There is no time limit on assessing a year for which no return was filed, and the '
   'penalty for failing to file runs at ten times the rate of the penalty for failing to pay. '
   'Say it plainly on the first call. <a href="situations/unfiled-years.html">What that work '
   'looks like is set out here.</a></p>'),
  ('I got a letter from the IRS. Do I need to panic?',
   '<p>No, but you do need to read the date on it. Most notices are automated, some are simply '
   'wrong, and many are resolved with one letter and a document. What turns a notice into a '
   'real problem is letting the response window close, because an unanswered proposal becomes '
   'an assessment. <a href="situations/irs-notice.html">There is more on notices here.</a></p>'
   '<p>CPAs hold unlimited representation rights before the IRS. Whether representation forms '
   'part of your engagement is something to agree with the office.</p>'),
  ('I moved into or out of Massachusetts this year. Which return do I file?',
   '<p>A part-year resident files Massachusetts Form 1-NR/PY and reports income earned while '
   'resident, plus Massachusetts-source income from the rest of the year. If you also worked in '
   'another state, both states may tax the same income, and a credit mechanism is meant to '
   'prevent that being paid twice. It is worth getting right; it is one of the more common '
   'sources of an amended return.</p>'),
  ('Does an extension give me more time to pay?',
   '<p>No. A federal extension moves the filing deadline to 15 October and does nothing about '
   'the balance &mdash; interest and penalties run from the original due date. Massachusetts is '
   'stricter still: its six-month extension is automatic only if at least 80% of the '
   'year&rsquo;s total tax has already been paid by the original due date. Miss that and the '
   'extension is void, which means a late-filing penalty on top of the late-payment one.</p>'),
  ('Do I have to sign anything before my return is filed?',
   '<p>Yes. Under IRS e-file rules the taxpayer must sign the authorisation before an '
   'electronic return originator may transmit the return &mdash; that is a rule, not a '
   'courtesy, and it exists so that nothing goes anywhere before you have seen it. A paid '
   'preparer must also sign the return and furnish you with a complete copy of it. Keep that '
   'copy; it is the starting point for next year and for anything that arises later.</p>'),
  ('How long should I keep my records?',
   '<p>Three years from filing covers the ordinary examination window. Six years applies where '
   'a return omits gross income exceeding 25% of the gross income it states, and there is no '
   'limit at all on a year for which no return was filed. Some records outlive all of that: '
   'anything establishing the cost basis of an asset should be kept until the asset is sold and '
   'the gain reported, which for a house or a business interest can mean decades.</p>'),
  ('Can I do my own bookkeeping and have you handle the return?',
   '<p>Yes, and many small businesses do exactly that. What determines whether it works is the '
   'state of the books rather than who keeps them: accounts that reconcile to outside '
   'statements, a chart of accounts that reflects the business, and nothing significant parked '
   'in a suspense account. A review of the books at the start of the engagement is usually '
   'cheaper than the alternative, which is discovering the problems while a deadline is '
   'running.</p>'),
  ('Are my records confidential?',
   '<p>Yes. Confidentiality is a professional obligation for a CPA rather than an internal '
   'policy, and it is enforceable as one. Separately, federal law restricts what a tax preparer '
   'may do with information supplied for the preparation of a return, including disclosing it '
   'to anyone else, without the taxpayer&rsquo;s written consent.</p>'),
  ('Are the calculators on this site giving me tax advice?',
   '<p>No. They are estimating tools that run entirely in your browser, using assumptions you '
   'can see and change. Rates, thresholds and contribution limits change every year, and none '
   'of them account for your filing status, your state position or anything else on your '
   'return. Use them to size a question and then call about the answer.</p>'),
 ]),
]


def build_questions():
    d = 0
    b = band('Answers', qa_block(FAQS))
    b += band('Still deciding',
        index_rows(d, [
            ('situations/index.html', 'Start where you are',
             'Six situations, each with what is actually involved.'),
            ('about.html#engagement', 'How an engagement runs',
             'From the first call to filing, in the order it happens.'),
            ('what-to-bring.html', 'What to bring',
             'What to gather before an appointment.'),
        ], compact=True))
    flat = [(q, re.sub(r'<[^>]+>', '', a)) for _, items in FAQS for q, a in items]
    return page('questions.html', d, 'questions',
        'Common questions | Charles M. Carella, CPA',
        'Answers on CPA licensing, engagement costs, IRS notices, unfiled years, extensions, '
        'record retention and Massachusetts part-year returns.',
        'Questions worth asking before you call.',
        'If yours is not here, the answer is a short phone call rather than a form.',
        (('Home', 'index.html'), ('Common questions', None)), b,
        [faq_schema(flat),
         crumb_schema([('Home', 'index.html'), ('Common questions', 'questions.html')])])


def build_contact():
    d = 0
    b = band('The office',
        parts_rows([
            ('Address', '%s<br>%s, %s %s' % (F['addr'], F['city'], F['state'], F['zip'])),
            ('Telephone', '<a href="tel:%s" class="num">%s</a>'
                          '<small>Dial the extension after the call connects.</small>'
                          % (F['tel'], F['ph_disp'])),
            ('Facsimile', '<span class="num">%s</span>' % F['fax']),
            ('Email', '<a href="mailto:%s">%s</a>' % (F['email'], F['email'])),
            ('Appointments', 'Call or email to arrange a time'),
        ])
        + mapblock())

    b += band('The first call',
        '<div class="prose" id="appointment">'
        '<h2>What a first call covers.</h2>'
        '<p>Three things, and none of them takes long: what kind of return or '
        'engagement this is, roughly what the year looked like, and what deadline is driving '
        'the question. If there is a business, how it is organised matters as well &mdash; sole '
        'proprietorship, partnership, LLC, S corporation, corporation &mdash; because that '
        'decides which return is involved and when it is due.</p>'
        '<p>The most useful thing to raise early is whatever is awkward. Years that were never '
        'filed, a notice with a date on it, books that stopped reconciling, a business that '
        'closed mid-year. None of those are unusual. All of them change the order in which the '
        'work is done.</p>'
        '<h3>What to have in front of you</h3>'
        '<ul>'
        '<li>Last year&rsquo;s return, if you can find it &mdash; not essential for a first '
        'call, but useful</li>'
        '<li>Any notice you have received, so the date on it can be read out</li>'
        '<li>For a business: how it is organised, and roughly what revenue looks like</li>'
        '<li>The deadline you are working against, if there is one</li>'
        '</ul>'
        '<p class="after">The <a href="what-to-bring.html">full list of what to gather</a> is '
        'for the appointment rather than the call. Missing pieces are not a reason to wait.</p>'
        '</div>')

    b += band('Sending documents',
        '<div class="prose">'
        '<h2>Ask before you send anything sensitive.</h2>'
        '<p>Which route makes sense depends on what you have and what form it is in, and it is '
        'a two-minute question on the call rather than something worth guessing at. The office '
        'is at 330 Boston Road, Suite 12, North Billerica, MA 01862, and the fax line is '
        'above.</p>'
        '<p>Never send Social Security numbers or account details in an unencrypted email.</p>'
        '</div>'
        + remark('Confidentiality',
                 'Client information is confidential. For a CPA that is a professional '
                 'obligation with enforcement behind it rather than an internal policy, and '
                 'federal law separately restricts what a preparer may do with information '
                 'supplied for the preparation of a return.'))

    return page('contact.html', d, 'contact',
        'Contact the office | Charles M. Carella, CPA',
        'Telephone, fax, email and address for the CPA office at 330 Boston Road, Suite 12, '
        'North Billerica, Massachusetts, and what a first call covers.',
        'Call the office.',
        'Describe the situation in a couple of minutes and ask what the work involves. There '
        'is no published fee schedule, because the work is not uniform.',
        (('Home', 'index.html'), ('Contact', None)), b,
        [org_schema(),
         crumb_schema([('Home', 'index.html'), ('Contact', 'contact.html')])])


def sit_page(slug, nav_title, title, desc, h1, stand, bands, related):
    d = 1
    b = ''.join(bands)
    b += band('Talk it through',
        '<div class="prose"><p>Describe what you are dealing with, and ask what the work '
        'involves. Call <a href="tel:%s" class="num">%s</a> or write to '
        '<a href="mailto:%s">%s</a>.</p></div>' % (F['tel'], F['ph_disp'], F['email'], F['email']))
    b += band('Related', index_rows(d, related, compact=True))
    return page('situations/%s.html' % slug, d, 'situations', title, desc, h1, stand,
                (('Home', 'index.html'), ('Start where you are', 'situations/index.html'),
                 (nav_title, None)), b,
                [page_schema(nav_title, 'situations/%s.html' % slug, desc),
                 crumb_schema([('Home', 'index.html'),
                               ('Start where you are', 'situations/index.html'),
                               (nav_title, 'situations/%s.html' % slug)])])


def build_situations():
    d = 1
    out = []

    # ---- hub -------------------------------------------------------------
    b = band('The list', index_rows(d, SITUATIONS))
    b += band('Or by service',
        '<p class="lede">If you already know what you need rather than what happened, the four '
        'practice areas are described in full.</p>'
        + index_rows(d, SERVICES, compact=True))
    out.append(page('situations/index.html', d, 'situations',
        'Start where you are | Charles M. Carella, CPA',
        'Six common situations: an IRS notice, unfiled years, untaxed income, a new business, '
        'a lender asking for statements, a move between states, and what each involves.',
        'Start where you are.',
        'Most people call an accountant because something specific happened. Whichever of '
        'these is closest, the page sets out what is actually involved &mdash; the deadlines '
        'that matter, the order the work runs in, and what to have ready.',
        (('Home', 'index.html'), ('Start where you are', None)), b,
        [page_schema('Start where you are', 'situations/index.html',
                     'Six common situations and what each involves.'),
         crumb_schema([('Home', 'index.html'),
                       ('Start where you are', 'situations/index.html')])]))

    # ---- notice ----------------------------------------------------------
    out.append(sit_page('irs-notice', 'A letter arrived',
        'A letter from the IRS or DOR | Charles M. Carella, CPA',
        'What an IRS or Massachusetts Department of Revenue notice means, why the response '
        'date on it is the part that matters, and what to do before you reply.',
        'A letter arrived from the IRS or the Department of Revenue.',
        'Read the date before you read anything else. A notice is a starting point, not a '
        'verdict &mdash; but an unanswered proposal becomes an assessment.',
        [band('First',
          '<div class="prose">'
          '<h2>The date is the only urgent part.</h2>'
          '<p>Most notices are generated automatically by a matching program rather than by a '
          'person who has looked at your return. Some are simply wrong. Many are resolved with '
          'one letter and a document. None of that helps if the response window closes, '
          'because a proposed adjustment that goes unanswered is eventually assessed &mdash; '
          'and once it is assessed the argument becomes considerably more expensive to have.</p>'
          '<p>So the first thing to establish is what kind of notice it is and how long you '
          'have. That is usually printed on the first page.</p>'
          '</div>'
          + remark('Before you reply',
                   'Send the notice on before responding to it, and keep the envelope. The '
                   'postmark occasionally matters, and the notice number in the corner '
                   'determines which procedure applies.')),
         band('What it usually is',
          '<div class="prose">'
          '<h2>Four things it is likely to be.</h2>'
          '<h3>A matching notice</h3>'
          '<p>The agency has a form &mdash; a 1099, a W-2, a K-1, a broker&rsquo;s report of '
          'proceeds &mdash; that it cannot find on your return. The commonest version is a sale '
          'of securities reported at its gross proceeds, with no cost basis, so the proposed '
          'tax is calculated as though the whole sale were profit. It is frequently wrong by a '
          'very large margin and it is answered with the basis records.</p>'
          '<h3>A maths or processing adjustment</h3>'
          '<p>A figure was transcribed differently, a credit was recalculated, an estimated '
          'payment was posted to the wrong year. These are often correct and occasionally not, '
          'and the way to tell is to compare the notice against the return and the payment '
          'record rather than against your memory.</p>'
          '<h3>A balance due</h3>'
          '<p>A statement of what the agency believes is outstanding, with interest and '
          'penalties calculated to a date. Worth checking rather than paying on sight, '
          'particularly if a payment was made close to the deadline or applied to a different '
          'period.</p>'
          '<h3>A request for information</h3>'
          '<p>A specific document, or verification of identity. Narrow, and usually answered '
          'exactly as asked and no more.</p>'
          '</div>'),
         band('Massachusetts',
          '<div class="prose">'
          '<h2>A DOR letter is not the same letter.</h2>'
          '<p>The Massachusetts Department of Revenue runs its own notice cycle with its own '
          'response periods, and a federal adjustment frequently produces a state one some '
          'months later because the agencies exchange data. If you have settled something '
          'federally, expect the state to catch up, and keep the federal correspondence: it is '
          'usually the whole answer to the state notice.</p>'
          '<p>The reverse also holds. A Massachusetts adjustment that changes your federal '
          'position may require an amended federal return.</p>'
          '</div>'),
         band('Penalties',
          '<div class="prose">'
          '<h2>What is actually accruing.</h2>'
          '<p>It is worth knowing which clock is running, because the two federal penalties are '
          'very different in size.</p>'
          '<div class="tscroll"><table class="plain">'
          '<thead><tr><th>Penalty</th><th>Rate</th><th>Ceiling</th></tr></thead>'
          '<tbody>'
          '<tr><td>Failure to file</td><td class="n">5% of the unpaid tax per month or part '
          'month</td><td class="n">25%</td></tr>'
          '<tr><td>Failure to pay</td><td class="n">0.5% of the unpaid tax per month or part '
          'month</td><td class="n">25%</td></tr>'
          '</tbody></table></div>'
          '<p class="after">In a month where both apply the failure-to-file penalty is reduced '
          'by the failure-to-pay amount, so the combined charge is 5% rather than 5.5%. '
          'Interest runs separately from the original due date and is not a penalty. The '
          'practical consequence is the one worth remembering: filing late costs ten times what '
          'paying late costs, so a return filed on time with a partial payment is far cheaper '
          'than a return held back until the money is there.</p>'
          '</div>'),
         band('Representation',
          '<div class="prose">'
          '<p>A Certified Public Accountant holds unlimited rights to represent a taxpayer '
          'before the IRS &mdash; in an examination, in collection and on appeal. Whether '
          'representation forms part of your engagement is something to agree with the office '
          'rather than something to assume; the point is that the licence permits it.</p>'
          '</div>')],
        [('situations/unfiled-years.html', 'Years that were never filed',
          'Where a notice turns out to be the smaller half of the problem.'),
         ('questions.html', 'Common questions',
          'Deadlines, records, extensions and what a CPA licence covers.'),
         ('services/tax.html', 'Tax preparation and planning',
          'The service behind this work.')]))

    # ---- unfiled ---------------------------------------------------------
    out.append(sit_page('unfiled-years', 'Unfiled years',
        'Years that were never filed | Charles M. Carella, CPA',
        'What happens when tax returns were never filed: the assessment period, how the work '
        'is sequenced using transcripts, and why the failure-to-file penalty is the expensive one.',
        'There are years that were never filed.',
        'More common than people assume, and the only version of this that gets worse is the '
        'one left alone. It changes what the work looks like, not whether it can be done.',
        [band('The clock',
          '<div class="prose">'
          '<h2>A year that was never filed never closes.</h2>'
          '<p>The ordinary period in which the IRS may assess additional tax is three years '
          'from the date a return was filed. It stretches to six where a return omits gross '
          'income exceeding 25% of the gross income it states. Where no return was filed at '
          'all, there is no limit &mdash; the year stays open indefinitely, and so does the '
          'ability to assess it.</p>'
          '<p>That asymmetry is the entire argument for dealing with it. Every filed year is a '
          'year that starts running down. Every unfiled year sits there.</p>'
          '</div>'
          + remark('Refunds do expire',
                   'The limit that does run against you is the one on claiming money back. A '
                   'refund for a year filed too late is generally lost, which means an unfiled '
                   'year that would have produced a refund can quietly turn into nothing at '
                   'all.')),
         band('Sequence',
          '<div class="prose">'
          '<h2>How the work actually runs.</h2>'
          '<ol>'
          '<li><b>Establish what the agencies already hold.</b> Wage and income transcripts '
          'show what was reported under your number for each year &mdash; W-2s, 1099s, K-1s, '
          'broker proceeds. That is the skeleton of each return and it does not depend on your '
          'records surviving.</li>'
          '<li><b>Find what the transcripts cannot see.</b> Business income with no form behind '
          'it, expenses, cost basis, dependants, state residency. This is the part that '
          'determines whether the reconstructed return resembles what you actually owed.</li>'
          '<li><b>Work oldest first.</b> Carry-forwards, basis and net operating losses run '
          'downhill through the years, so a later year cannot be finished properly until the '
          'earlier one is.</li>'
          '<li><b>File, then deal with the balance.</b> Filing stops the expensive penalty '
          'first. What is owed is a separate conversation with its own arrangements.</li>'
          '</ol>'
          '</div>'),
         band('Substitutes',
          '<div class="prose">'
          '<h2>If the agency has already filed for you.</h2>'
          '<p>Where a return is not filed, the IRS may eventually prepare one from the forms it '
          'holds. It is not a sympathetic document: it allows no business expenses, no cost '
          'basis, and usually the least favourable filing status. A stock sale appears as pure '
          'profit. A contractor&rsquo;s gross receipts appear with nothing deducted.</p>'
          '<p>The number produced that way is almost always far higher than the real one, and '
          'the answer is to file an actual return for the year rather than to argue with the '
          'assessment.</p>'
          '</div>'),
         band('Cost',
          '<div class="prose">'
          '<h2>Which penalty is doing the damage.</h2>'
          '<p>Failing to file is charged at 5% of the unpaid tax for each month or part month, '
          'to a maximum of 25%. Failing to pay is charged at 0.5% on the same basis, to the '
          'same maximum. Ten to one. A return more than 60 days late also carries a minimum '
          'penalty &mdash; the lesser of the tax due or a fixed amount that is adjusted '
          'annually.</p>'
          '<p>None of that changes the sequence, but it does explain it: file first, arrange '
          'the balance second.</p>'
          '</div>'),
         band('Massachusetts',
          '<div class="prose">'
          '<p>Massachusetts runs its own assessment periods and its own penalties, and a '
          'federal filing generally produces state correspondence in due course. Unfiled '
          'Massachusetts years are worked the same way and usually alongside &mdash; the state '
          'return is largely built from the federal one, so doing them together is cheaper than '
          'doing them twice.</p>'
          '</div>')],
        [('situations/irs-notice.html', 'A letter arrived',
          'Frequently the thing that starts this conversation.'),
         ('what-to-bring.html', 'What to bring',
          'What to gather, and what to do about the gaps.'),
         ('services/tax.html', 'Tax preparation and planning',
          'The service behind this work.')]))
    # ---- self-employed ---------------------------------------------------
    out.append(sit_page('self-employed', 'Income with no withholding',
        'Income with no tax withheld | Charles M. Carella, CPA',
        'A first 1099, a side business or K-1 income: how quarterly estimated tax works, what '
        'the safe harbour is, and how self-employment tax is calculated.',
        'Income is arriving and nobody is withholding tax.',
        'A first 1099, a side business, a K-1, a large capital gain. The obligation to pay in '
        'during the year has moved from an employer to you, and it has four dates on it.',
        [band('The shift',
          '<div class="prose">'
          '<h2>Two taxes, not one.</h2>'
          '<p>A wage earner has income tax withheld every payday and has half of Social '
          'Security and Medicare paid by an employer. Both of those disappear at once when '
          'income starts arriving without withholding, and they are separate problems.</p>'
          '<p><b>Income tax</b> is charged on the profit at your ordinary rates, on top of '
          'everything else on the return. <b>Self-employment tax</b> is the Social Security and '
          'Medicare contribution, and because there is no employer, both halves are yours: '
          '15.3% in total &mdash; 12.4% for Social Security and 2.9% for Medicare.</p>'
          '<p>Three details soften it. Only 92.35% of net profit is subject to the tax. The '
          'Social Security portion stops at an annual wage base, while the Medicare portion '
          'does not. And one half of the self-employment tax is deductible against income tax.</p>'
          '<p class="after">The <a href="../calculators/self-employment-tax.html">self-employment '
          'tax calculator</a> works through that arithmetic. Income tax sits on top of the '
          'figure it produces.</p>'
          '</div>'),
         band('The dates',
          '<div class="prose">'
          '<h2>Four instalments, federal and state.</h2>'
          '<p>Estimated tax is paid quarterly, and Massachusetts uses the same calendar as the '
          'federal system, on Form 1-ES.</p>'
          '<div class="tscroll"><table class="plain">'
          '<thead><tr><th>Instalment</th><th>Covers</th><th>Due</th></tr></thead><tbody>'
          '<tr><td class="n">First</td><td>1 January &ndash; 31 March</td><td class="n">15 April</td></tr>'
          '<tr><td class="n">Second</td><td>1 April &ndash; 31 May</td><td class="n">15 June</td></tr>'
          '<tr><td class="n">Third</td><td>1 June &ndash; 31 August</td><td class="n">15 September</td></tr>'
          '<tr><td class="n">Fourth</td><td>1 September &ndash; 31 December</td><td class="n">15 January following</td></tr>'
          '</tbody></table></div>'
          '<p class="after">Note that the quarters are not equal &mdash; the second covers two '
          'months and the third covers three. A due date falling on a weekend or holiday moves '
          'to the next business day.</p>'
          '</div>'),
         band('The safe harbour',
          '<div class="prose">'
          '<h2>The single most useful rule here.</h2>'
          '<p>The underpayment penalty is not a fine for owing money at filing. It is interest '
          'charged for paying too little too late in the year, and it can be avoided even in a '
          'year of completely unexpected income.</p>'
          '<p>Paying in at least the total tax shown on last year&rsquo;s return &mdash; 110% '
          'of it if last year&rsquo;s adjusted gross income was above $150,000, or $75,000 '
          'filing separately &mdash; protects you regardless of what this year turns out to be. '
          'Paying 90% of the current year&rsquo;s eventual tax also works, but you have to know '
          'what that is, and in a volatile year you do not.</p>'
          '<p>Which is why the useful moment to check this is the autumn, when there is still a '
          'January instalment left to adjust, rather than the following April when there is not.</p>'
          '</div>'
          + remark('If you also have a job',
                   'Withholding is treated as paid evenly across the year no matter when it '
                   'actually happened. Increasing withholding on a salary late in the year can '
                   'therefore repair an estimated tax shortfall in a way that a late estimated '
                   'payment cannot. It is a genuinely useful piece of arithmetic and it is '
                   'available only until 31 December.')),
         band('Massachusetts',
          '<div class="prose">'
          '<h2>The state runs alongside.</h2>'
          '<p>Massachusetts taxes most income at a flat 5%, which makes the state estimate '
          'easier to size than the federal one. Short-term capital gains are taxed at a higher '
          'rate of their own, and an additional 4% surtax applies to taxable income above a '
          'threshold a little over one million dollars that is adjusted annually &mdash; which '
          'matters in the year of a business sale or a property sale rather than in an ordinary '
          'year.</p>'
          '<p>Massachusetts has no state standard deduction; it uses personal exemptions and '
          'its own list of deductions instead, so federal and state taxable income rarely '
          'match.</p>'
          '</div>')],
        [('calculators/self-employment-tax.html', 'Self-employment tax calculator',
          'The Social Security and Medicare half of the estimate, and the deductible portion.'),
         ('situations/new-business.html', 'A business is starting, or changing shape',
          'At some level of profit the way the business is organised starts to matter.'),
         ('services/tax.html', 'Tax preparation and planning',
          'The service behind this work.')]))

    # ---- new business ----------------------------------------------------
    out.append(sit_page('new-business', 'A new or changing business',
        'Starting or restructuring a business | Charles M. Carella, CPA',
        'How a business is organised decides which return it files, when it is due and how the '
        'profit reaches the owner: sole proprietorship, partnership, LLC, S corporation.',
        'A business is starting, or changing shape.',
        'How it is organised decides which return it files, when that return is due, how the '
        'profit reaches your personal return, and what the payroll obligations are.',
        [band('The choice',
          '<div class="prose">'
          '<h2>Four shapes, and they behave differently.</h2>'
          '<p>An LLC is a state-law entity, not a tax classification. For tax purposes it is '
          'treated as one of the shapes below, which is the source of most of the confusion '
          'about it.</p>'
          '<div class="tscroll"><table class="plain">'
          '<thead><tr><th>Organised as</th><th>Files</th><th>Profit reaches you via</th><th>Return due</th></tr></thead>'
          '<tbody>'
          '<tr><td>Sole proprietorship or single-member LLC</td><td class="n">Schedule C inside Form 1040</td>'
          '<td>Directly</td><td class="n">15 April</td></tr>'
          '<tr><td>Partnership or multi-member LLC</td><td class="n">Form 1065</td>'
          '<td>Schedule K-1</td><td class="n">15 March</td></tr>'
          '<tr><td>S corporation</td><td class="n">Form 1120-S</td>'
          '<td>Schedule K-1, plus wages</td><td class="n">15 March</td></tr>'
          '<tr><td>C corporation</td><td class="n">Form 1120</td>'
          '<td>Salary or dividends</td><td class="n">15 April</td></tr>'
          '</tbody></table></div>'
          '<p class="after">Dates shown are for a calendar-year business and move to the next '
          'business day when they fall on a weekend or holiday. The entity return has to be '
          'finished before the owner&rsquo;s personal return can be, because it produces the '
          'K-1 the personal return depends on.</p>'
          '</div>'),
         band('The penalty',
          '<div class="prose">'
          '<h2>A late business return is expensive in a way a personal one is not.</h2>'
          '<p>The failure-to-file penalty on a partnership or S corporation return is charged '
          'per owner, per month, for up to twelve months &mdash; not as a percentage of tax '
          'owed. The per-owner monthly amount is adjusted annually and stood at $255 for '
          'returns required to be filed in 2026.</p>'
          '<p>A four-owner partnership that files six months late is therefore looking at '
          'roughly six thousand dollars of penalty on a return that may show no tax at all. '
          'This is the single strongest argument for extending an entity return you cannot '
          'finish on time.</p>'
          '</div>'),
         band('S corporations',
          '<div class="prose">'
          '<h2>The reasonable compensation question.</h2>'
          '<p>An S election is often made to reduce self-employment tax: profit distributed to '
          'an owner is not subject to it, whereas the profit of a sole proprietorship is. The '
          'condition attached is that an owner who works in the business must be paid '
          'reasonable compensation as wages, with payroll, withholding and the employer&rsquo;s '
          'share of Social Security and Medicare that go with it.</p>'
          '<p>What follows is that the election only makes sense above a certain level of '
          'profit, because it brings real costs with it: a separate return, a payroll '
          'obligation, and a wage figure that has to be defensible. Below that level it costs '
          'more than it saves. Establishing where that line falls for a particular business is '
          'an arithmetic question rather than an opinion, and it is worth asking before the '
          'election rather than after.</p>'
          '</div>'
          + remark('Elections have deadlines',
                   'An S election is due within a defined window from the beginning of the tax '
                   'year it is to apply to, or from the entity being formed. Late relief exists '
                   'and is frequently granted, but it is relief from a missed deadline rather '
                   'than an alternative to meeting it.')),
         band('Massachusetts',
          '<div class="prose">'
          '<h2>Two state-level points to know before you choose.</h2>'
          '<p>A Massachusetts corporation owes a minimum corporate excise in every year, '
          'including a year in which it loses money. The minimum stood at $456 for the 2025 tax '
          'year. It is small, but it is not zero, and it surprises people who assumed a loss '
          'year costs nothing.</p>'
          '<p>Massachusetts also does not follow the federal depreciation rules. Bonus '
          'depreciation is disallowed outright for state purposes, and while the state does '
          'allow section 179 expensing, Massachusetts has deferred conformity to the increased '
          'federal limits enacted in 2025 &mdash; for the 2025 and 2026 tax years the state '
          'deduction has to be recomputed without those amendments. A purchase that produces a '
          'large federal deduction may produce a much smaller state one, and the two sets of '
          'figures diverge from that point onward.</p>'
          '</div>')],
        [('calculators/section-179.html', 'Equipment purchase calculator',
          'What a deduction for an equipment purchase is worth at your rate.'),
         ('calculators/break-even.html', 'Break-even calculator',
          'The volume at which the business covers its fixed costs.'),
         ('services/consulting.html', 'Business consulting',
          'The service behind this work.')]))

    # ---- financial statements -------------------------------------------
    out.append(sit_page('financial-statements', 'Someone wants statements',
        'A lender has asked for financial statements | Charles M. Carella, CPA',
        'Preparation, compilation, review and audit are four different levels of service at '
        'four different costs. Establishing which one is required is the first step.',
        'Someone has asked for financial statements.',
        'A lender, a landlord, a bonding company or a prospective buyer. The first question is '
        'not how fast &mdash; it is which level of service they actually require.',
        [band('Four levels',
          '<div class="prose">'
          '<h2>The word &ldquo;statements&rdquo; covers four different jobs.</h2>'
          '<p>They differ in how much work stands behind them, and therefore in what they cost '
          'and how long they take. Requests routinely arrive without specifying which is meant, '
          'and the gap between the cheapest and the dearest is very wide.</p>'
          '<div class="tscroll"><table class="plain">'
          '<thead><tr><th>Level</th><th>What the accountant does</th><th>What it gives the reader</th></tr></thead>'
          '<tbody>'
          '<tr><td>Preparation</td><td>Assembles the statements from your records</td>'
          '<td>No report, and no assurance</td></tr>'
          '<tr><td>Compilation</td><td>The same assembly, plus a reading for obvious problems, '
          'plus a signed report</td><td>A report, but still no assurance</td></tr>'
          '<tr><td>Review</td><td>Analytical procedures and enquiry</td><td>Limited assurance</td></tr>'
          '<tr><td>Audit</td><td>Testing, confirmation and evidence gathering</td>'
          '<td>An opinion</td></tr>'
          '</tbody></table></div>'
          '<p class="after">A great many requests that arrive asking for &ldquo;audited '
          'accounts&rdquo; are satisfied by a compilation once somebody asks the question. Establishing that first '
          'is usually the largest single saving available in this whole exercise.</p>'
          '</div>'
          + remark('Ask what they will accept',
                   'The person who asked can nearly always tell you which level their credit '
                   'policy requires, and the answer is frequently less than the phrasing of '
                   'the request implied. It is a two-minute question that occasionally saves '
                   'a great deal.')),
         band('What is needed',
          '<div class="prose">'
          '<h2>Statements are built out of the books.</h2>'
          '<p>Which means the condition of the books decides the timetable. What has to be in '
          'place first:</p>'
          '<ul>'
          '<li>Bank and credit card accounts reconciled through the period end</li>'
          '<li>A chart of accounts that reflects how the business actually works, rather than '
          'whatever the software proposed on installation</li>'
          '<li>Loans stated at their real balances, with the interest split out</li>'
          '<li>A current depreciation schedule</li>'
          '<li>Nothing significant sitting in a suspense or uncategorised account</li>'
          '<li>Accounts receivable and payable that agree to something</li>'
          '</ul>'
          '<p class="after">Where the books are behind, the honest sequence is to bring them '
          'current first. Statements produced from unreconciled records are worth very little '
          'and a lender&rsquo;s analyst tends to notice.</p>'
          '</div>'),
         band('Timing',
          '<div class="prose">'
          '<h2>Deadlines that arrive with the request.</h2>'
          '<p>Requests of this kind usually carry a date, and the date is usually somebody '
          'else&rsquo;s: a credit committee, a closing, a bonding renewal, a lease signature. '
          'The useful thing to establish on the first call is what the date actually is and '
          'what happens if it moves, because that determines whether the books can be brought '
          'current properly or whether the work has to be sequenced around a fixed point.</p>'
          '<p>If a covenant in an existing loan agreement is what is driving the request, the '
          'agreement itself usually specifies the level of service and the deadline. It is '
          'worth reading before the work is scoped rather than after.</p>'
          '</div>')],
        [('services/financial-statements.html', 'Financial statement preparation',
          'The service behind this work.'),
         ('services/bookkeeping.html', 'Accounting and bookkeeping',
          'What has to be true before statements can be prepared.'),
         ('questions.html', 'Common questions',
          'Including whether you can keep your own books.')]))

    # ---- two states ------------------------------------------------------
    out.append(sit_page('two-states', 'Two states in one year',
        'Moving into or out of Massachusetts | Charles M. Carella, CPA',
        'Part-year and non-resident Massachusetts returns, Form 1-NR/PY, apportionment, and '
        'the credit that stops the same income being taxed twice.',
        'A move into or out of Massachusetts.',
        'Two states in one year, or living in one and working in another. Apportionment is the '
        'whole exercise, and it is one of the more common reasons a return has to be amended.',
        [band('Which return',
          '<div class="prose">'
          '<h2>Residency for the year decides the form.</h2>'
          '<p>A full-year Massachusetts resident files Form 1. A part-year resident or a '
          'non-resident files Form 1-NR/PY.</p>'
          '<p>A part-year resident reports income earned while resident in Massachusetts, plus '
          'Massachusetts-source income from the remainder of the year. A non-resident reports '
          'Massachusetts-source income only. Both require the year to be split, and the split '
          'is where the work is.</p>'
          '</div>'),
         band('Apportionment',
          '<div class="prose">'
          '<h2>Splitting the year.</h2>'
          '<p>Wages are generally apportioned by where the work was performed rather than by '
          'where the employer sits or where the payslip was issued. Investment income usually '
          'follows residence at the time it was received. A capital gain follows residence at '
          'the date of sale, which means the timing of a large sale relative to a move can '
          'change which state taxes it &mdash; a fact worth knowing before the move rather '
          'than after.</p>'
          '<p>Deductions and exemptions are generally prorated to the Massachusetts portion of '
          'the year, so the state figure is not simply a fraction of the federal one.</p>'
          '</div>'
          + remark('Keep the dates',
                   'The single most useful record here is a clear note of when the move '
                   'happened and, where the work was performed in more than one state, how '
                   'many days were worked where. Reconstructing that a year later from '
                   'memory is the part that goes wrong.')),
         band('Taxed twice',
          '<div class="prose">'
          '<h2>The credit is meant to prevent it, and it usually does.</h2>'
          '<p>Where two states tax the same income, the state of residence generally allows a '
          'credit for tax paid to the other state. It is a credit rather than an exemption, so '
          'it is limited to what the residence state would itself have charged on that income '
          '&mdash; if the other state charges more, the excess is not recovered.</p>'
          '<p>Both returns have to be prepared in the right order for the credit to compute '
          'correctly, and the non-resident return generally has to be done first. Getting the '
          'order wrong is a common cause of an amended return.</p>'
          '</div>'),
         band('Massachusetts rates',
          '<div class="prose">'
          '<p>Massachusetts taxes most income &mdash; wages, interest, dividends and long-term '
          'capital gains &mdash; at a flat 5%. Short-term capital gains are taxed at a higher '
          'rate of their own. An additional 4% surtax applies to taxable income above a '
          'threshold a little over one million dollars, adjusted annually, and it reaches '
          'one-off events, so the year of a business sale or a property sale is the year to '
          'check it. There is no state standard deduction.</p>'
          '</div>')],
        [('services/tax.html', 'Tax preparation and planning',
          'The service behind this work.'),
         ('what-to-bring.html', 'What to bring',
          'Including the events that changed your year.'),
         ('questions.html', 'Common questions',
          'Including which return a part-year resident files.')]))

    return out


def svc_page(slug, nav_title, title, desc, h1, stand, bands, questions, related):
    d = 1
    b = ''.join(bands)
    if questions:
        b += band('Questions', qa_block([(None, questions)]))
    b += band('Talk it through',
        '<div class="prose"><p>Describe what you are dealing with, and ask what the work '
        'involves. Call <a href="tel:%s" class="num">%s</a> or write to '
        '<a href="mailto:%s">%s</a>.</p></div>' % (F['tel'], F['ph_disp'], F['email'], F['email']))
    b += band('Related', index_rows(d, related, compact=True))
    sch = [service_schema(nav_title, desc, 'services/%s.html' % slug),
           crumb_schema([('Home', 'index.html'), ('What the office does', 'services/index.html'),
                         (nav_title, 'services/%s.html' % slug)])]
    if questions:
        sch.append(faq_schema([(q, re.sub(r'<[^>]+>', '', a)) for q, a in questions]))
    return page('services/%s.html' % slug, d, 'services', title, desc, h1, stand,
                (('Home', 'index.html'), ('What the office does', 'services/index.html'),
                 (nav_title, None)), b, sch)


def build_services():
    d = 1
    out = []

    b = band('The four', index_rows(d, SERVICES))
    b += band('Why one office',
        '<div class="prose">'
        '<p>For somebody who owns a small business these are not four separate problems. The '
        'entity return depends on the books; the statements a lender asks for are built from '
        'the same books; and the structural questions decide what next year&rsquo;s return will '
        'look like. Handled in one place, each piece of work informs the next. Handled '
        'separately, the same facts get established four times.</p>'
        '</div>')
    b += band('Or by situation',
        '<p class="lede">If what you have is a problem rather than a service, start here '
        'instead.</p>' + index_rows(d, SITUATIONS, compact=True))
    out.append(page('services/index.html', d, 'services',
        'What the office does | Charles M. Carella, CPA',
        'Tax preparation and planning, accounting and bookkeeping, financial statement '
        'preparation and business consulting, for individuals and small businesses.',
        'Four services, and they are the same conversation.',
        'Tax preparation and planning, accounting and bookkeeping, financial statement '
        'preparation, and business consulting &mdash; for individuals and for the small '
        'businesses they run.',
        (('Home', 'index.html'), ('What the office does', None)), b,
        [page_schema('What the office does', 'services/index.html',
                     'The four practice areas of the office.'),
         crumb_schema([('Home', 'index.html'),
                       ('What the office does', 'services/index.html')])]))

    # ---------------------------------------------------------------- tax
    out.append(svc_page('tax', 'Tax preparation and planning',
        'Tax preparation and planning | Charles M. Carella, CPA',
        'Federal and Massachusetts income tax returns for individuals and small businesses, '
        'and the planning that has to happen before the year closes.',
        'A return is a record. The planning happens earlier.',
        'Income tax preparation and planning for individuals and for the small businesses they '
        'own, federal and Massachusetts.',
        [band('The two halves',
          '<div class="prose">'
          '<h2>Preparation and planning are not one job.</h2>'
          '<p>Preparation of federal and Massachusetts income tax returns for individuals and '
          'small businesses, and the planning work that sits in front of them. Those two halves '
          'are usually sold as one service and treated as one job. They are not. Preparation '
          'records decisions that have already been made. Planning is the part where the '
          'decisions are still open.</p>'
          '<h3>Why the calendar decides most of it</h3>'
          '<p>By the time a return is being prepared, the year is closed and the arithmetic is '
          'fixed. Nearly everything that moves the number happened months earlier: how the '
          'business is organised, what the owner took as wages against distributions, when '
          'equipment was bought and how it was paid for, whether a retirement plan contribution '
          'was made, how a property sale was structured, which state the work was performed '
          'in.</p>'
          '<p>Some of it can still be adjusted after year end &mdash; a self-employed '
          'retirement plan contribution, an IRA, an accounting method question. Most of it '
          'cannot. That is the argument for a conversation in the autumn rather than a scramble '
          'in April.</p>'
          '</div>'),
         band('Individuals',
          '<div class="prose">'
          '<h2>Where a return stops being straightforward.</h2>'
          '<p>A straightforward wage return is straightforward. Returns stop being '
          'straightforward at fairly predictable points: a first year of self-employment or '
          '1099 income, a house bought or sold, equity compensation, a rental unit, an '
          'inheritance, a move across a state line, a year with two states in it, marriage, '
          'divorce, a child in college, retirement account withdrawals starting.</p>'
          '<p>Each of those changes what has to be reported and what can be claimed, and each '
          'of them is a reason to raise the question before the year ends rather than after.</p>'
          '</div>'),
         band('Massachusetts',
          '<div class="prose">'
          '<h2>The state return is not a copy of the federal one.</h2>'
          '<ul>'
          '<li>Massachusetts taxes most income &mdash; wages, interest, dividends, long-term '
          'capital gains &mdash; at a flat 5%. Short-term capital gains are taxed at a higher '
          'rate of their own.</li>'
          '<li>A 4% surtax applies to taxable income above a threshold a little over one '
          'million dollars, adjusted annually. It reaches one-off events, so the year you sell '
          'a business or a building is the year to check it.</li>'
          '<li>There is no state standard deduction. Massachusetts uses personal exemptions and '
          'its own list of deductions instead, which is why federal and state taxable income '
          'rarely match.</li>'
          '<li>Residents file Form 1; part-year residents and non-residents file Form 1-NR/PY. '
          '<a href="../situations/two-states.html">If you moved during the year</a>, or you '
          'live in one state and work in another, the apportionment is the whole exercise.</li>'
          '<li>Massachusetts does not follow the federal bonus-depreciation rules, and it has '
          'deferred conformity to the increased section 179 limits enacted in 2025 for the 2025 '
          'and 2026 tax years. A purchase that produces a large federal deduction may produce a '
          'much smaller state one, and the two sets of figures diverge from that point on.</li>'
          '</ul></div>'),
         band('Businesses',
          '<div class="prose">'
          '<h2>The entity decides the return.</h2>'
          '<p>How a business is organised decides which return it files, when it is due, and '
          'how the profit reaches the owner&rsquo;s personal return. A sole proprietorship or '
          'single-member LLC reports on Schedule C inside the owner&rsquo;s Form 1040. A '
          'partnership or multi-member LLC files its own return and issues a Schedule K-1 to '
          'each owner. An S corporation files its own return, issues K-1s, and adds the '
          'question of reasonable compensation for any owner who works in the business. A C '
          'corporation is taxed in its own right and owes a Massachusetts corporate excise even '
          'in a year it loses money.</p>'
          '<p>Those returns are due on different dates, and the entity return has to be '
          'finished before the owner&rsquo;s personal return can be. A business return filed '
          'late is expensive in a way an individual return is not: the penalty is charged per '
          'owner, per month. <a href="../situations/new-business.html">The comparison is set '
          'out here.</a></p>'
          '</div>'),
         band('Estimates',
          '<div class="prose">'
          '<h2>Income that arrives without withholding.</h2>'
          '<p>Self-employment profit, K-1 income, investment income, a large capital gain '
          '&mdash; all of it carries an obligation to pay in quarterly. The federal instalments '
          'are due in April, June, September and January; Massachusetts uses the same schedule '
          'on Form 1-ES.</p>'
          '<p>The underpayment penalty is not a fine for owing money at filing. It is interest '
          'charged for paying late in the year, and it can be avoided even in a year of '
          'unexpected income by paying in at least what last year&rsquo;s tax was &mdash; a '
          'higher percentage of it if your income is above the threshold in the rule. That safe '
          'harbour is the single most useful thing to know about estimates, and it is worth '
          'checking in the autumn rather than in January.</p>'
          '</div>'
          + remark('An extension buys time to file, not time to pay',
                   'The federal extension moves the filing deadline to 15 October and nothing '
                   'else; interest and penalties run on any unpaid balance from the original '
                   'due date. Massachusetts grants an automatic six-month extension only if at '
                   'least 80% of the year&rsquo;s total tax has already been paid &mdash; miss '
                   'that and the extension is void, with a late-filing penalty on top.')),
         band('Prior years',
          '<div class="prose">'
          '<h2>Notices and years that got away.</h2>'
          '<p>A letter from the IRS or the Massachusetts Department of Revenue is a starting '
          'point, not a verdict. Some are wrong. Many are answered with a single letter and a '
          'document. Almost all of them have a deadline printed on them, and the deadline is '
          'the part that matters &mdash; a notice that is ignored becomes an assessment.</p>'
          '<p>Unfiled years work the same way. They are more common than most people assume, '
          'and the situation only compounds while it is left alone. Say so plainly on the first '
          'call; it changes what the work looks like but not whether it can be done.</p>'
          '</div>'),
         band('Your side',
          '<div class="prose">'
          '<p>The quality of a return is mostly decided by the completeness of what it is built '
          'from. Complete records shorten the work, reduce the questions, and lower the chance '
          'of an amendment later. The <a href="../what-to-bring.html">list of what to gather</a> '
          'covers the usual case; anything unusual about your year is worth mentioning at the '
          'start rather than being discovered at the end.</p>'
          '</div>')],
        [('When should I call about planning rather than preparation?',
          '<p>Before the year closes, and before the transaction if there is one. Selling a '
          'property, buying equipment, changing how the business is organised, taking a large '
          'distribution, exercising options &mdash; all of those have a better and a worse '
          'version, and the choice closes on 31 December. Planning after year end is limited to '
          'a short list: certain retirement contributions, an IRA, and a few accounting method '
          'questions.</p>'),
         ('Do you prepare both the business return and the owner&rsquo;s personal return?',
          '<p>Tax preparation and planning for individuals and small businesses is what this '
          'office does, and for an owner-operated business the two returns are one problem. The '
          'entity return produces the K-1 or the Schedule C figure that the personal return '
          'depends on, so the entity return has to be finished first.</p>'),
         ('I have income with no tax withheld. How much should I be paying in?',
          '<p>Enough to land inside the safe harbour. Paying in at least the amount of last '
          'year&rsquo;s total tax &mdash; a higher percentage of it above an income threshold '
          '&mdash; avoids the underpayment penalty regardless of what this year turns out to '
          'be. The <a href="../calculators/self-employment-tax.html">self-employment tax '
          'calculator</a> gives you the Social Security and Medicare half of the estimate; '
          'income tax sits on top of it.</p>'),
         ('What happens if I cannot pay what I owe?',
          '<p>File anyway. The penalty for filing late is ten times the penalty for paying '
          'late, so a return filed on time with a partial payment costs far less than a return '
          'held back until the money is there. Both the IRS and the Massachusetts Department of '
          'Revenue have instalment arrangements; both are easier to arrange before the balance '
          'is in collection.</p>')],
        [('situations/self-employed.html', 'Income with no tax withheld',
          'Quarterly estimates, the safe harbour, and self-employment tax.'),
         ('services/bookkeeping.html', 'Accounting and bookkeeping',
          'What the return is built from.'),
         ('calculators/self-employment-tax.html', 'Self-employment tax calculator',
          'Size the quarterly obligation before you call.')]))

    # -------------------------------------------------------- bookkeeping
    out.append(svc_page('bookkeeping', 'Accounting and bookkeeping',
        'Accounting and bookkeeping | Charles M. Carella, CPA',
        'Chart of accounts design, monthly reconciliation and period-end accounting for small '
        'businesses: the work every other number depends on.',
        'The monthly work everything else depends on.',
        'Setting up or repairing a chart of accounts, recording activity, reconciling accounts, '
        'and producing figures at the end of each period that mean what they say.',
        [band('What it buys',
          '<div class="prose">'
          '<h2>Bookkeeping is not a compliance chore.</h2>'
          '<p>It is usually described as one &mdash; something done because the tax return '
          'needs it. That is the least valuable thing it does.</p>'
          '<p>A set of books that reconciles every month tells you which jobs make money and '
          'which ones only look busy, whether the business is generating cash or borrowing '
          'against next month, when receivables are drifting, and what a slow quarter actually '
          'costs. None of that is visible from a bank balance. A bank balance tells you what '
          'has already happened to the cash; the books tell you what is about to.</p>'
          '<p>The other thing it buys is optionality. A business with three years of clean '
          'books can apply for a loan, take on an investor, price itself for sale, or answer a '
          'state notice. A business without them can do none of those quickly, and the cost of '
          'reconstructing the history always exceeds the cost of having kept it.</p>'
          '</div>'),
         band('The chart',
          '<div class="prose">'
          '<h2>The chart of accounts is the whole design.</h2>'
          '<p>Most bookkeeping problems are really chart-of-accounts problems. The default '
          'chart that comes with accounting software is designed to suit everyone, which means '
          'it suits nobody: too many accounts in places that do not matter, one undifferentiated '
          'bucket where the business actually makes its decisions.</p>'
          '<p>A chart that fits the business separates the things you would want to compare and '
          'combines the things you would not. It puts direct costs where they can be read '
          'against revenue instead of scattering them through overhead. It gives the two or '
          'three lines you actually manage their own place. Getting it right early is cheap; '
          'changing it after four years of history is not, because every comparison to an '
          'earlier period has to be restated with it.</p>'
          '</div>'),
         band('The cycle',
          '<div class="prose">'
          '<h2>Not complicated, but unforgiving about being skipped.</h2>'
          '<ol>'
          '<li><b>Reconcile every account against an outside statement.</b> Bank accounts, '
          'credit cards, loans, merchant processors, payroll clearing. An account that has not '
          'been reconciled is not evidence of anything.</li>'
          '<li><b>Code the activity properly rather than plausibly.</b> Software will suggest a '
          'category from the vendor name. It is right often enough to be dangerous.</li>'
          '<li><b>Deal with the awkward items rather than parking them.</b> The transaction '
          'nobody could identify in March is considerably harder to identify in December.</li>'
          '<li><b>Close the period and leave it closed.</b> Entries posted into a closed month '
          'silently change figures somebody has already relied on.</li>'
          '</ol></div>'),
         band('Failures',
          '<div class="prose">'
          '<h2>The five that come up again and again.</h2>'
          '<h3>Personal and business money in one account</h3>'
          '<p>It makes every subsequent step harder, it obscures what the business actually '
          'earns, and for a company or LLC it weakens the separation the entity exists to '
          'provide in the first place. A separate account and a separate card cost nothing and '
          'solve it permanently.</p>'
          '<h3>Owner draws recorded as expenses</h3>'
          '<p>Money an owner takes out of a sole proprietorship or a partnership is a draw '
          'against equity, not a deductible cost. Recorded as an expense it understates profit, '
          'which is pleasant right up to the point a lender, a buyer or an examiner reads the '
          'statements.</p>'
          '<h3>Sales tax treated as revenue</h3>'
          '<p>Massachusetts sales tax collected from a customer never belonged to the business. '
          'It is money held on the state&rsquo;s behalf until it is remitted. Booked as income '
          'it inflates revenue and hides a liability that is already accruing.</p>'
          '<h3>Payroll recorded from the net</h3>'
          '<p>Recording only the amount that left the bank omits the withholding and the '
          'employer&rsquo;s own share. The wage deduction ends up understated and the payroll '
          'liability accounts never clear.</p>'
          '<h3>Reconciliations that are forced</h3>'
          '<p>An adjustment entered to make a reconciliation balance does not fix anything; it '
          'moves the discrepancy somewhere it will be harder to find. Forced entries are '
          'usually what makes a year of books take three days to unpick instead of three '
          'hours.</p>'
          '</div>'
          + remark('Books and the return are one job in two parts',
                   'Every hour spent reconstructing a year at filing time is an hour billed at '
                   'filing time, under a deadline, with worse information. It is the most '
                   'expensive way to buy bookkeeping.')),
         band('Records',
          '<div class="prose">'
          '<h2>How long to keep them.</h2>'
          '<p>The general rule is three years from filing, because that is the ordinary window '
          'in which a return can be examined. It stretches to six years where a return omits '
          'gross income exceeding 25% of the gross income it states, and there is no limit at '
          'all on a year for which no return was filed.</p>'
          '<p>Employment tax records, property and improvement records, and anything '
          'establishing the cost basis of an asset should outlive that schedule &mdash; basis '
          'records matter until the asset is sold and the gain is reported, which for a '
          'building or a business interest can mean decades.</p>'
          '</div>')],
        [('Do I need a bookkeeper?',
          '<p>Not in itself. Plenty of small businesses keep their own books perfectly well. '
          'What matters is whether the accounts reconcile to outside statements every month, '
          'whether the chart of accounts reflects how the business actually works, and whether '
          'anything unresolved has been parked rather than answered. Those three things are '
          'worth a review even if nothing else changes.</p>'),
         ('My books are two years behind. Is it too late?',
          '<p>There is no point at which it becomes impossible, only points at which it '
          'becomes more expensive. Bank and card statements can be obtained, and a year can be '
          'rebuilt from them. What cannot be recovered is the memory of what an unexplained '
          'transaction was for, which is why the cost rises with age rather than with '
          'volume.</p>'),
         ('Which software should I use?',
          '<p>Almost any of the mainstream small-business packages will do the job. The choice '
          'matters far less than the chart of accounts inside it and the discipline of '
          'reconciling monthly. Software does not produce good books; it produces fast books, '
          'in whatever condition the inputs put them.</p>'),
         ('What is the difference between bookkeeping and accounting?',
          '<p>Bookkeeping is the recording: capturing transactions, coding them, reconciling '
          'the accounts. Accounting is what is done with the result &mdash; period-end '
          'adjustments, depreciation, accruals, and presenting the figures so they can be read '
          'and relied on. The same records support both, which is why the recording standard '
          'determines everything above it.</p>')],
        [('services/financial-statements.html', 'Financial statement preparation',
          'What reconciled books make possible.'),
         ('situations/financial-statements.html', 'Someone has asked for statements',
          'What has to be true before that request can be answered.'),
         ('calculators/break-even.html', 'Break-even calculator',
          'What the books should be able to tell you.')]))

    # ------------------------------------------------ financial statements
    out.append(svc_page('financial-statements', 'Financial statement preparation',
        'Financial statement preparation | Charles M. Carella, CPA',
        'Balance sheet, income statement and supporting detail for small businesses, and the '
        'conversation about which level of service a request actually requires.',
        'Statements somebody outside the business can read.',
        'A balance sheet, an income statement and the supporting detail, built from the books '
        'and presented so that a lender, a landlord or an owner can rely on them.',
        [band('Four levels',
          '<div class="prose">'
          '<h2>Four different things share one name.</h2>'
          '<p>When a lender, a landlord, a bonding company or a buyer asks for &ldquo;financial '
          'statements&rdquo;, they may mean any of four levels of service. They differ '
          'enormously in what the accountant does and in what the recipient is entitled to rely '
          'on, and it is worth knowing which one is being asked for before agreeing to produce '
          'it.</p>'
          '<div class="tscroll"><table class="plain">'
          '<thead><tr><th>Level</th><th>What the accountant does</th><th>What the reader gets</th></tr></thead>'
          '<tbody>'
          '<tr><td>Preparation</td><td>Assembles statements from the client&rsquo;s records '
          'under professional standards</td><td>Statements with no report attached and no '
          'assurance offered. Each page says so.</td></tr>'
          '<tr><td>Compilation</td><td>The same assembly, plus a reading of the statements for '
          'obvious problems, plus a signed report</td><td>A report from the accountant. Still '
          'no assurance.</td></tr>'
          '<tr><td>Review</td><td>Analytical procedures and enquiry of management</td>'
          '<td>Limited assurance &mdash; nothing came to the accountant&rsquo;s attention.</td></tr>'
          '<tr><td>Audit</td><td>Testing, confirmation and evidence gathering</td>'
          '<td>An opinion on whether the statements are fairly stated.</td></tr>'
          '</tbody></table></div>'
          '<p class="after">The cost difference between the top and the bottom of that table is '
          'large &mdash; a multiple, not a percentage. So is the difference in what is required '
          'from you.</p>'
          '</div>'),
         band('Who decides',
          '<div class="prose">'
          '<h2>Almost always somebody else.</h2>'
          '<p>A loan agreement, a line-of-credit covenant, a bonding requirement, a franchise '
          'agreement, a lease, a grant, a state licensing body, or a company&rsquo;s own '
          'operating agreement will name a level of service, and that requirement drives the '
          'engagement.</p>'
          '<p>Two things are worth doing about that. First, read the clause before signing it: '
          'the difference between &ldquo;reviewed&rdquo; and &ldquo;audited&rdquo; in a '
          'covenant is a real annual cost for as long as the agreement runs, and it is '
          'frequently negotiable at the outset and never afterwards. Second, if the request '
          'came verbally, ask which level is meant. Requests for &ldquo;audited '
          'statements&rdquo; are often satisfied by something considerably cheaper.</p>'
          '<p>If nothing external requires anything, the honest answer is usually that you need '
          'less than you have been told.</p>'
          '</div>'
          + remark('Independence',
                   'Assurance work &mdash; a review or an audit &mdash; must be performed by an '
                   'accountant who is independent of the business. An accountant who keeps the '
                   'books ordinarily cannot also provide assurance on them. That constraint '
                   'sometimes decides who does what, and it is better understood at the start '
                   'than discovered at the deadline.')),
         band('What they say',
          '<div class="prose">'
          '<h2>Reading the statements themselves.</h2>'
          '<h3>The balance sheet</h3>'
          '<p>A position at one instant: what the business owns, what it owes, and what is '
          'left. Read it for the relationship between current assets and current liabilities, '
          'for how much of the business is financed by debt, and for the two accounts that hide '
          'the most trouble &mdash; receivables that are ageing and inventory that is not '
          'moving.</p>'
          '<h3>The income statement</h3>'
          '<p>Performance across a period. The useful reading is never the bottom line on its '
          'own but the shape above it: gross margin, and whether it is holding; which costs '
          'move with revenue and which do not; and the comparison against the same period last '
          'year rather than against the month before.</p>'
          '<h3>Cash flow</h3>'
          '<p>Profit is an opinion about timing. Cash is a fact. A growing business is '
          'perfectly capable of being profitable and insolvent at the same time, because growth '
          'consumes cash before it produces any &mdash; inventory bought, wages paid, invoices '
          'outstanding. The statement that reconciles profit to cash movement is the one that '
          'explains where the money went.</p>'
          '</div>'),
         band('Lenders',
          '<div class="prose">'
          '<h2>What a lender actually looks at.</h2>'
          '<p>Not the statements alone. A lender reads them against the debt service they are '
          'being asked to support, checks the covenants they intend to impose, compares the '
          'figures to the tax returns, and looks at whether the equity account moves in a way '
          'the drawings explain. Statements that agree with the returns, and drawings that are '
          'recorded as drawings, remove most of the friction from that process before it '
          'starts.</p>'
          '<p>Statements are only as good as the records under them. Reconciled accounts, a '
          'chart of accounts that separates what matters, and no unresolved items are the '
          'precondition &mdash; see <a href="bookkeeping.html">accounting and bookkeeping</a>. '
          'Statements produced from books that do not reconcile are an expensive way of '
          'formatting a guess.</p>'
          '</div>')],
        [('A lender asked for &ldquo;financial statements&rdquo;. Which do I need?',
          '<p>Ask them. The word covers four different levels of service with very different '
          'costs, and lenders frequently ask for more than their own policy requires. Get the '
          'requirement in writing, ideally from the loan document rather than from the '
          'conversation, before anyone starts work.</p>'),
         ('Can my tax return serve instead?',
          '<p>Sometimes, and it is always worth asking. A tax return is prepared under tax '
          'rules rather than accounting rules, so the figures legitimately differ &mdash; '
          'depreciation is the usual culprit. Many small-business lending decisions are made on '
          'returns alone. Where statements are genuinely required, the two should still agree '
          'with each other in every place they can.</p>'),
         ('How often should statements be produced?',
          '<p>For internal use, monthly, because that is the frequency at which a problem is '
          'still small. For outside recipients, whatever the agreement requires &mdash; '
          'typically annually, sometimes quarterly for a business under covenants.</p>'),
         ('What does &ldquo;no assurance is provided&rdquo; mean?',
          '<p>That the accountant assembled the statements from records supplied by the '
          'business and did not verify them. It is a statement of scope, not a warning about '
          'the figures. Statements at that level are entirely appropriate for internal '
          'management and for many outside purposes; they are not the same thing as an audited '
          'statement and are not priced like one.</p>')],
        [('situations/financial-statements.html', 'Someone has asked for statements',
          'What to establish before the work is scoped.'),
         ('services/bookkeeping.html', 'Accounting and bookkeeping',
          'The records statements are built from.'),
         ('calculators/loan-payment.html', 'Loan payment calculator',
          'What the debt service actually is.')]))

    # --------------------------------------------------------- consulting
    out.append(svc_page('consulting', 'Business consulting',
        'Business consulting | Charles M. Carella, CPA',
        'Entity choice, pricing and break-even, working capital, what a hire really costs, and '
        'the equipment purchases that look like tax savings.',
        'The questions that arrive between filings.',
        'The operating and structural questions that come up during the year and do not wait '
        'for a deadline.',
        [band('Organisation',
          '<div class="prose">'
          '<h2>Entity choice is arithmetic, not preference.</h2>'
          '<p>It gets treated as a one-off decision made at the start and never revisited. It '
          'should be revisited, because the answer changes as the business does.</p>'
          '<p>A sole proprietorship is the default and costs nothing to maintain, but every '
          'dollar of profit carries self-employment tax and there is no separation between the '
          'business and the person. An LLC adds that separation and, in Massachusetts, an '
          'annual filing fee that is not trivial for a very small business. Electing S '
          'corporation treatment can reduce self-employment tax on the portion of profit taken '
          'as distribution rather than wages, at the cost of payroll, a separate return and a '
          'reasonable compensation figure that has to be defensible.</p>'
          '<p>The right answer depends on profit, on how many owners there are, on whether '
          'outside investment or a sale is plausible, and on how much administration the '
          'business can absorb. It is worth redoing when profit changes materially.</p>'
          '</div>'),
         band('Pricing',
          '<div class="prose">'
          '<h2>Most small businesses under-price.</h2>'
          '<p>And most of them discover it by working harder without earning more.</p>'
          '<p>The number that matters is contribution margin: what is left from a sale after '
          'the costs that only exist because the sale happened. Fixed costs are then paid out '
          'of accumulated contribution, and the point at which they are covered is break-even. '
          'Two consequences follow, and they are not intuitive. A modest price increase moves '
          'break-even far more than the same percentage cut in costs, because the increase '
          'lands entirely in the margin. And the volume you can afford to lose at a higher '
          'price is usually much larger than it feels.</p>'
          '<p class="after">The <a href="../calculators/break-even.html">break-even '
          'calculator</a> does the arithmetic for a single line of business.</p>'
          '</div>'),
         band('Cash',
          '<div class="prose">'
          '<h2>Why profitable businesses run out of it.</h2>'
          '<p>Growth consumes cash. Inventory is bought before it is sold, wages are paid '
          'before the work is invoiced, and invoices are paid on the customer&rsquo;s schedule '
          'rather than yours. The gap between paying and being paid is a working capital '
          'requirement, and it grows in proportion to sales &mdash; so the faster a business '
          'grows, the more of it needs funding.</p>'
          '<p>The practical levers are deposits and progress billing, invoicing on the day work '
          'is finished instead of at month end, terms that are actually enforced, and inventory '
          'bought against demand rather than against a discount. A short cash projection '
          '&mdash; thirteen weeks is the conventional horizon &mdash; converts all of that from '
          'an anxiety into a schedule.</p>'
          '</div>'),
         band('Hiring',
          '<div class="prose">'
          '<h2>What a hire really costs.</h2>'
          '<p>The wage is roughly two thirds of it. On top sits the employer&rsquo;s share of '
          'Social Security and Medicare, federal and Massachusetts unemployment insurance, '
          'workers&rsquo; compensation, the Massachusetts paid family and medical leave '
          'contribution, any benefits, and the payroll administration itself. Then there is the '
          'part that never appears in a budget: the time spent training somebody, and the '
          'productivity that is not there in the first months.</p>'
          '<p>The other question is whether the role is an employee at all. The distinction '
          'between an employee and an independent contractor is not a matter of what the '
          'parties agree; Massachusetts applies a strict test of its own, stricter than the '
          'federal one, and getting it wrong is expensive in back taxes, penalties and unpaid '
          'wage claims. It is worth settling before the first payment, not after.</p>'
          '</div>'),
         band('Purchases',
          '<div class="prose">'
          '<h2>The purchases that look like tax savings.</h2>'
          '<p>A deduction is not a rebate. Spending a dollar to save thirty cents of tax leaves '
          'you seventy cents down, which is fine if the asset earns its keep and a poor '
          'decision if it was bought for the deduction. The order of the questions is: does the '
          'business need it, can the cash or the financing be carried, and only then, how is it '
          'treated for tax.</p>'
          '<p>The treatment itself is worth modelling rather than assuming. Immediate expensing '
          'and bonus depreciation are limited by rules that change, a deduction is worth only '
          'your marginal rate, an immediate deduction cannot create a loss in some cases, and '
          'Massachusetts does not follow the federal bonus-depreciation rules at all. The '
          '<a href="../calculators/section-179.html">equipment purchase calculator</a> shows '
          'what a deduction is worth against a given rate.</p>'
          '</div>'
          + remark('The cheapest advice is early advice',
                   'Almost every expensive problem in a small business was cheap at the point '
                   'it was still a question &mdash; the lease that was signed, the contractor '
                   'who should have been an employee, the covenant nobody read, the equipment '
                   'bought in December. None of those are fixable afterwards at anything like '
                   'the cost of asking first.')),
         band('Reading it',
          '<div class="prose">'
          '<h2>Three or four figures, on a schedule.</h2>'
          '<p>A small business does not need a dashboard. It needs a handful of figures looked '
          'at regularly: gross margin against last year, cash and the thirteen-week projection, '
          'receivables over sixty days, and whatever the single operational number is that '
          'drives the business &mdash; utilisation, occupancy, jobs closed, average ticket. '
          'Everything else is commentary.</p>'
          '</div>')],
        [('Should I elect S corporation treatment?',
          '<p>It depends on profit, on what reasonable compensation for the owner&rsquo;s role '
          'would be, and on whether the business can carry payroll, a separate return and '
          'tighter bookkeeping. Below a certain level of profit the added cost exceeds the '
          'saving. Above it the saving can be substantial. It is worth calculating rather than '
          'assuming, and worth recalculating when profit changes materially.</p>'),
         ('Should I buy equipment before year end to reduce tax?',
          '<p>Only if the equipment is needed. A deduction returns your marginal rate, so the '
          'purchase still costs most of its price in cash. Buying an asset you would have '
          'bought anyway, slightly earlier, is sound. Buying one you would not have bought is '
          'spending a dollar to save a fraction of it.</p>'),
         ('How should I set prices?',
          '<p>Start from contribution margin rather than from what competitors charge. A price '
          'rise lands entirely in the margin, so a small one moves break-even further than a '
          'large cost saving. The real question is usually how much volume you can afford to '
          'lose at the new price &mdash; and the answer is often more than expected.</p>'),
         ('Can I treat this worker as a contractor?',
          '<p>Massachusetts applies its own test and it is strict &mdash; stricter than the '
          'federal rules, and it does not care what the written agreement says. '
          'Misclassification is corrected with back employment taxes, penalties and potential '
          'wage claims. Settle the question before the first payment.</p>')],
        [('situations/new-business.html', 'A business is starting, or changing shape',
          'Entity choice, due dates and the reasonable compensation question.'),
         ('calculators/break-even.html', 'Break-even calculator',
          'Fixed costs, contribution margin and the volume that covers them.'),
         ('services/bookkeeping.html', 'Accounting and bookkeeping',
          'The figures any of this depends on.')]))

    return out


# ==========================================================================
# Calculators. calculators.py is DATA (verified formulas) and a runtime keyed on
# element ids — no layout comes from it. The markup and styling below are this
# site's own.
# ==========================================================================
import calculators as C
CALCS = C.CALCULATORS

# calculators.py is shared with the five remaining template builds, so per-site
# wording is overridden here rather than edited there.
NOTE_OVERRIDES = {
    'section-179': ('Section 179 cannot create a loss, and annual limits and phase-outs '
                    'apply. Ask about the treatment before signing a purchase order, not '
                    'after.'),
}

CALC_NOTES = {
    'section-179': ('Massachusetts does not follow the federal bonus-depreciation rules, and '
                    'it has deferred conformity to the increased federal section 179 limits '
                    'for the 2025 and 2026 tax years. The state deduction on the same purchase '
                    'may be materially smaller than the federal one.'),
    'self-employment-tax': ('The Social Security portion stops at an annual wage base that is '
                            'adjusted each year; the Medicare portion does not. This estimates '
                            'self-employment tax only &mdash; income tax sits on top of it.'),
}


def _clip(t, lo=70, hi=175):
    """Meta descriptions must land inside the QA window without breaking a word."""
    if len(t) <= hi:
        return t
    cut = t[:hi]
    return cut[:cut.rfind(' ')].rstrip(' ,;&') + '.'


def calc_body(calc):
    rows = ''
    for x in calc['inputs']:
        pre = '<span class="pre">$</span>' if x['kind'] == C.MONEY else ''
        suf = ('<span class="suf">%</span>' if x['kind'] == C.PCT else
               '<span class="suf">yrs</span>' if x['kind'] == C.YEARS else '')
        attrs = ' step="%s"' % x['step'] if x.get('step') else ''
        if x.get('min') is not None:
            attrs += ' min="%s"' % x['min']
        if x.get('max') is not None:
            attrs += ' max="%s"' % x['max']
        rows += ('<div class="row"><label for="f_%s">%s</label>'
                 '<div class="ifield">%s<input type="number" inputmode="decimal" id="f_%s" '
                 'value="%s"%s>%s</div>%s</div>'
                 % (x['id'], x['label'], pre, x['id'], x['default'], attrs, suf,
                    ('<p class="hint">%s</p>' % x['hint']) if x.get('hint') else ''))

    primary = next((o for o in calc['outputs'] if o['primary']), calc['outputs'][0])
    srows = ''
    for o in calc['outputs']:
        if o['primary']:
            continue
        srows += ('<div><div class="orow"><dt>%s</dt><dd id="o_%s">&mdash;</dd></div>%s</div>'
                  % (o['label'], o['id'],
                     ('<div class="onote">%s</div>' % o['note']) if o.get('note') else ''))

    spec = json.dumps(dict(
        inputs=[dict(id=x['id']) for x in calc['inputs']],
        outputs=[dict(id=o['id'], kind=o['kind']) for o in calc['outputs']],
        js=calc['js']), separators=(',', ':'))

    b = band('Work it out',
        '<div class="calc" data-calc>'
        '<div class="calcform">' + rows + '</div>'
        '<div class="calcout" aria-live="polite">'
        '<div class="big"><div class="l">' + primary['label'] + '</div>'
        '<div class="v" id="o_' + primary['id'] + '">&mdash;</div></div>'
        '<dl>' + srows + '</dl></div>'
        '</div>'
        '<p class="calcnote">' + NOTE_OVERRIDES.get(calc['slug'], calc['note']) + '</p>'
        '<script type="application/json" id="calcspec">' + spec + '</script>')

    extra = CALC_NOTES.get(calc['slug'])
    if extra:
        b += band('Massachusetts' if calc['slug'] == 'section-179' else 'Note',
                  remark('Worth knowing', extra), tight=True)
    return b


def build_calculators():
    d = 1
    out = []
    calc_kids = [('calculators/%s.html' % c['slug'], c['title']) for c in CALCS]

    cats = []
    for c in CALCS:
        if c['cat'] not in [x[0] for x in cats]:
            cats.append((c['cat'], []))
        dict(cats)[c['cat']].append(c)
    body = ''
    for cat, items in cats:
        body += band(cat, index_rows(d, [('calculators/%s.html' % c['slug'], c['title'],
                                          c['blurb']) for c in items]))
    hub = band('Why these',
        '<div class="prose">'
        '<p>Eight calculators, chosen to cover the questions that actually come up rather '
        'than to pad a list. Each one runs entirely in your browser: no third-party calculator '
        'script, no sign-in, no cookie, and nothing you enter leaves the page or is stored '
        'anywhere. They work with the network off.</p>'
        '<p>They are estimating tools, not advice. Rates, thresholds and contribution limits '
        'change every year, and none of them account for your filing status, your Massachusetts '
        'position or anything else on your return. Use one to size a question, then '
        '<a href="../contact.html">call about the answer</a>.</p>'
        '</div>') + body
    out.append(page('calculators/index.html', d, 'calculators',
        'Financial calculators | Charles M. Carella, CPA',
        'Eight calculators covering mortgages, refinancing, loans, retirement, college saving, '
        'self-employment tax, equipment purchases and break-even. Nothing leaves your browser.',
        'Eight calculators that run on the page.',
        'Mortgage and refinance, loans, retirement and college saving, self-employment tax, '
        'equipment purchases and break-even. The arithmetic happens in your browser and stops '
        'there.',
        (('Home', 'index.html'), ('Calculators', None)), hub,
        [page_schema('Financial calculators', 'calculators/index.html',
                     'Eight native financial calculators.'),
         crumb_schema([('Home', 'index.html'), ('Calculators', 'calculators/index.html')])],
        calc_kids=calc_kids))

    for c in CALCS:
        others = [('calculators/%s.html' % o['slug'], o['title'], o['blurb'])
                  for o in CALCS if o['slug'] != c['slug']][:3]
        b = calc_body(c)
        b += band('Other calculators', index_rows(d, others, compact=True))
        b += band('Not advice',
            '<div class="prose"><p>This is an estimating tool. It uses the assumptions you can '
            'see and change above, and it does not account for your filing status, your '
            'Massachusetts position, or anything else on your return. Call '
            '<a href="tel:%s" class="num">%s</a> to talk about what the figure means for '
            'you.</p></div>' % (F['tel'], F['ph_disp']))
        out.append(page('calculators/%s.html' % c['slug'], d, 'calculators',
            '%s | Charles M. Carella, CPA' % c['title'],
            _clip(c['blurb'] + ' Runs entirely in your browser; nothing is sent anywhere.'),
            c['title'] + '.',
            c['blurb'],
            (('Home', 'index.html'), ('Calculators', 'calculators/index.html'),
             (c['title'], None)), b,
            [page_schema(c['title'], 'calculators/%s.html' % c['slug'], c['blurb']),
             crumb_schema([('Home', 'index.html'), ('Calculators', 'calculators/index.html'),
                           (c['title'], 'calculators/%s.html' % c['slug'])])],
            tail=C.CALC_JS, calc_kids=calc_kids))
    return out


# ==========================================================================
def main():
    os.makedirs(os.path.join(OUT, 'css'), exist_ok=True)
    open(os.path.join(OUT, 'css', 'carella.css'), 'w', encoding='utf-8').write(CSS)
    built = []
    built.append(build_home())
    built.append(build_about())
    built.append(build_bring())
    built.append(build_questions())
    built.append(build_contact())
    built += build_situations()
    built += build_services()
    built += build_calculators()
    print('built %d pages -> %s' % (len(built), OUT))
    return built


if __name__ == '__main__':
    main()
