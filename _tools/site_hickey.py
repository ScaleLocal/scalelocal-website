# -*- coding: utf-8 -*-
"""
James L. Hickey, CPA PC — Tewksbury, Massachusetts
==================================================
A standalone site. It shares NO layout, CSS, component or template with any other
build in this repo. build.py is not imported and must never be.

The design premise is a working document rather than a marketing page. A CPA firm's
own artefacts — the letterhead, the engagement letter, the ruled index, the notice
that arrives in a window envelope — are the visual language clients already associate
with this profession, and none of them look like a card grid.

Concretely, and deliberately unlike anything else here:
  * a static letterhead masthead, not a sticky glass bar
  * a hero that is a statement plus a bordered particulars panel, on paper — no
    gradient block, no hero art, no pair of buttons
  * services set as a ruled index with dot leaders, like a contents page
  * the IRS practice as a numbered procedure, because that is what it is
  * body pages in a single measured column with a marginal note gutter
  * figures, phone numbers and money set in a monospace face throughout
  * no floating chat pill

Content is the existing honesty-checked prose, extracted block by block from the
previous build so nothing verified is lost. Layout is entirely new.

    python3 site_hickey.py
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'hickeycpa')
BASE = 'https://www.scalelocal.net/test-builds/hickeycpa/'
# Extracted prose. Ships alongside this file so the build is reproducible in a fresh
# sandbox; regenerate with extract_prose.py if the source pages change.
_BLOCKS_PATH = os.path.join(HERE, 'content_blocks_hickeycpa.json')
if not os.path.exists(_BLOCKS_PATH):
    _BLOCKS_PATH = '/tmp/hickey_blocks.json'
BLOCKS = json.load(open(_BLOCKS_PATH, encoding='utf-8'))

F = dict(
    name='James L. Hickey, CPA PC',
    short='Hickey',
    person='James L. Hickey, CPA',
    addr='170 Main Street, Suite 110',
    city='Tewksbury', state='MA', state_full='Massachusetts', zip='01876',
    tel='+19788518945', ph='(978) 851-8945', fax='(978) 851-9314',
    email='info@hickeycpa.com',
    portal='https://www.securefirmportal.com/Account/Login/4700',
    maps='https://www.google.com/maps/search/?api=1&query=170+Main+Street+Suite+110+Tewksbury+MA+01876',
)

# ---------------------------------------------------------------- palette
# Near-black ink on warm paper, one claret accent, one brass rule. Restrained on
# purpose: the colour does no work here, the typography and the rules do.
INK = '#16171A'
INK_SOFT = '#4A4C51'
PAPER = '#FCFBF8'
PAPER_2 = '#F4F1EA'
RULE = '#DCD6C9'
CLARET = '#6E1F2A'
CLARET_LT = '#8E3542'
BRASS = '#A8842F'

CSS = """
/* James L. Hickey, CPA PC — bespoke. Not shared with any other build. */
@font-face{font-family:x;src:local(x)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --ink:%(INK)s; --soft:%(INK_SOFT)s; --paper:%(PAPER)s; --paper2:%(PAPER_2)s;
  --rule:%(RULE)s; --claret:%(CLARET)s; --claretlt:%(CLARET_LT)s; --brass:%(BRASS)s;
  --serif:"IBM Plex Serif",Georgia,"Times New Roman",serif;
  --sans:"IBM Plex Sans",-apple-system,"Segoe UI",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  --measure:66ch;
}
html{-webkit-text-size-adjust:100%%}
body{background:var(--paper);color:var(--ink);font-family:var(--serif);
  font-size:17px;line-height:1.66;font-feature-settings:"kern","liga";
  -webkit-font-smoothing:antialiased}
img{max-width:100%%;display:block}
a{color:var(--claret);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{color:var(--claretlt)}
:focus-visible{outline:2px solid var(--claret);outline-offset:2px}
.sheet{max-width:1180px;margin:0 auto;padding:0 32px}
.mono{font-family:var(--mono);font-size:.92em;font-variant-numeric:tabular-nums}

/* ---------------------------------------------------------- demo notice */
.notice{background:#1B1A17;color:#E7E2D6;font-family:var(--sans);font-size:12px;
  line-height:1.5;padding:8px 0;letter-spacing:.01em}
.notice .sheet{display:flex;gap:10px;justify-content:center;text-align:center;flex-wrap:wrap}
.notice b{color:var(--brass);text-transform:uppercase;letter-spacing:.14em;font-size:11px;
  font-weight:700;white-space:nowrap}
@media print{.notice{background:#fff;color:#000}.notice b{color:#000}}

/* ------------------------------------------------------------ letterhead */
.masthead{background:var(--paper);border-bottom:1px solid var(--rule)}
.masthead .sheet{display:flex;align-items:flex-end;justify-content:space-between;
  gap:36px;padding-top:30px;padding-bottom:20px;flex-wrap:wrap}
.wordmark{display:flex;align-items:center;gap:16px;text-decoration:none;color:inherit}
.wordmark .mk{width:52px;height:52px;flex:0 0 52px;color:var(--claret)}
.wordmark .mk svg{width:100%%;height:100%%;display:block}
.wordmark .nm{font-family:var(--serif);font-size:25px;font-weight:600;letter-spacing:-.015em;line-height:1.06}
.wordmark .nm span{display:block;font-family:var(--sans);font-size:10.5px;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;color:var(--soft);margin-top:6px}
.headcontact{font-family:var(--sans);font-size:13px;color:var(--soft);text-align:right;line-height:1.75}
.headcontact a{color:var(--ink);text-decoration:none;font-weight:600}
.headcontact .tel{font-family:var(--mono);font-size:15px;letter-spacing:-.02em}
/* nav is a ruled band under the letterhead, not a floating bar */
.navband{border-bottom:2px solid var(--ink);background:var(--paper)}
.navband .sheet{display:flex;gap:30px;flex-wrap:wrap;align-items:center;padding-top:11px;padding-bottom:11px}
.navband a{font-family:var(--sans);font-size:12.5px;font-weight:600;letter-spacing:.13em;
  text-transform:uppercase;color:var(--ink);text-decoration:none;padding-bottom:2px;
  border-bottom:2px solid transparent;margin-bottom:-2px}
.navband a:hover,.navband a[aria-current]{color:var(--claret);border-bottom-color:var(--claret)}
.navband .spacer{flex:1}
.navband .portal{color:var(--claret)}

/* ------------------------------------------------------------------ hero */
.opening{padding:74px 0 0}
.opening .grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:64px;align-items:start}
.kicker{font-family:var(--sans);font-size:11.5px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--claret);margin-bottom:20px}
.opening h1{font-size:clamp(2.3rem,4.4vw,3.35rem);line-height:1.1;font-weight:500;
  letter-spacing:-.022em;max-width:20ch}
.opening .stand{margin-top:22px;font-size:1.14rem;color:var(--soft);max-width:52ch;line-height:1.62}
.opening .after{margin-top:30px;font-family:var(--sans);font-size:14px}
.opening .after a{font-weight:600;text-decoration:none;border-bottom:1px solid var(--rule);padding-bottom:2px}
.opening .after a:hover{border-bottom-color:var(--claret)}
@media(max-width:900px){.opening{padding-top:48px}
  .opening .grid{grid-template-columns:minmax(0,1fr);gap:38px}
  .opening h1{max-width:none}}
@media(max-width:560px){.sheet{padding:0 20px}
  .particulars dl{grid-template-columns:minmax(0,1fr)}
  .particulars dt{border-bottom:0;padding-bottom:0}
  .particulars dd{padding-left:18px}
  .headcontact{text-align:left}
  .masthead .sheet{align-items:flex-start}}

/* the particulars panel — a form, not a card */
.particulars{border:1px solid var(--ink);background:var(--paper2)}
.particulars .cap{background:var(--ink);color:var(--paper);font-family:var(--sans);font-size:10.5px;
  font-weight:700;letter-spacing:.2em;text-transform:uppercase;padding:9px 18px}
.particulars dl{display:grid;grid-template-columns:auto 1fr}
.particulars dt{font-family:var(--sans);font-size:10.5px;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;color:var(--soft);padding:13px 14px 13px 18px;border-bottom:1px solid var(--rule);
  white-space:nowrap}
.particulars dd{padding:13px 18px 13px 0;border-bottom:1px solid var(--rule);font-size:14.5px;line-height:1.5}
.particulars dl>:nth-last-child(1),.particulars dl>:nth-last-child(2){border-bottom:0}
.particulars dd a{text-decoration:none;font-weight:600}
.particulars .act{border-top:1px solid var(--ink);display:block;padding:14px 18px;background:var(--claret);
  color:#fff;font-family:var(--sans);font-size:13px;font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;text-align:center;text-decoration:none}
.particulars .act:hover{background:var(--claretlt);color:#fff}

/* practice areas as a running line of links, not cards */
.areas{margin-top:66px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:20px 0}
.areas .lbl{font-family:var(--sans);font-size:10.5px;font-weight:700;letter-spacing:.2em;
  text-transform:uppercase;color:var(--soft);margin-bottom:10px}
.areas .run{font-size:16px;line-height:2}
.areas .run a{text-decoration:none;color:var(--ink);border-bottom:1px solid var(--rule)}
.areas .run a:hover{color:var(--claret);border-bottom-color:var(--claret)}
.areas .run i{color:var(--brass);font-style:normal;margin:0 12px}

/* ------------------------------------------------- IRS practice, numbered */
.procedure{background:var(--ink);color:#E9E5DC;margin-top:76px;padding:70px 0}
.procedure h2{font-size:clamp(1.7rem,3vw,2.3rem);font-weight:500;line-height:1.14;color:#fff;letter-spacing:-.018em;max-width:24ch}
.procedure .intro{margin-top:16px;color:#B9B4A8;max-width:62ch;font-size:1.02rem;line-height:1.6}
.procedure ol{list-style:none;margin-top:44px;border-top:1px solid #34322D}
.procedure li{display:grid;grid-template-columns:78px minmax(0,1fr) auto;gap:26px;align-items:baseline;
  padding:22px 0;border-bottom:1px solid #34322D}
.procedure .n{font-family:var(--mono);font-size:13px;color:var(--brass);letter-spacing:.08em}
.procedure .t{font-size:1.12rem;color:#fff}
.procedure .t small{display:block;font-family:var(--sans);font-size:13.5px;color:#A9A498;margin-top:5px;line-height:1.55}
.procedure .go{font-family:var(--sans);font-size:12px;font-weight:600;letter-spacing:.12em;
  text-transform:uppercase;color:var(--brass);text-decoration:none;white-space:nowrap}
.procedure .go:hover{color:#fff}
@media(max-width:720px){.procedure li{grid-template-columns:52px minmax(0,1fr)}.procedure .go{grid-column:2}}

/* ------------------------------------------------- services as a ruled index */
.index{padding:76px 0}
.index h2{font-size:clamp(1.7rem,3vw,2.3rem);font-weight:500;line-height:1.14;letter-spacing:-.018em}
.index .note{margin-top:14px;color:var(--soft);max-width:60ch;line-height:1.6}
.contents{margin-top:38px;column-count:2;column-gap:64px}
@media(max-width:820px){.contents{column-count:1}}
.contents a{display:flex;align-items:baseline;gap:10px;text-decoration:none;color:var(--ink);
  padding:11px 0;border-bottom:1px solid var(--rule);break-inside:avoid}
.contents a:hover{color:var(--claret)}
.contents .ttl{font-size:16.5px}
.contents .dots{flex:1;border-bottom:1px dotted var(--rule);transform:translateY(-4px)}
.contents .pg{font-family:var(--mono);font-size:12px;color:var(--soft)}
.contents a:hover .pg{color:var(--claret)}

/* ------------------------------------------------------------ body pages */
.page{padding:56px 0 0}
.trail{font-family:var(--sans);font-size:12px;color:var(--soft);margin-bottom:26px}
.trail a{color:var(--soft);text-decoration:none}
.trail a:hover{color:var(--claret)}
.trail span{margin:0 8px;color:var(--rule)}
.page h1{font-size:clamp(1.95rem,3.7vw,2.75rem);font-weight:500;line-height:1.11;letter-spacing:-.02em;max-width:22ch}
.page .stand{margin-top:18px;font-size:1.1rem;line-height:1.55;color:var(--soft);max-width:56ch}
.page .rule{margin:38px 0 0;border-top:2px solid var(--ink)}
.body{display:grid;grid-template-columns:172px minmax(0,1fr);gap:48px;padding:40px 0 84px}
@media(max-width:880px){.body{grid-template-columns:minmax(0,1fr);gap:0}.marginal{display:none}}
.marginal{font-family:var(--sans);font-size:12.5px;color:var(--soft);line-height:1.6;
  position:sticky;top:26px;border-right:1px solid var(--rule);padding-right:20px}
.marginal b{display:block;color:var(--ink);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:8px}
.marginal a{display:block;color:var(--soft);text-decoration:none;padding:3px 0}
.marginal a:hover{color:var(--claret)}
.copy{max-width:var(--measure)}
.copy h2{font-size:1.5rem;font-weight:600;margin:44px 0 14px;letter-spacing:-.012em}
.copy h2:first-child{margin-top:0}
.copy h3{font-size:1.16rem;font-weight:600;margin:32px 0 10px;font-family:var(--sans)}
.copy p{margin-bottom:17px}
.copy ul,.copy ol{margin:0 0 20px 20px}
.copy li{margin-bottom:8px}
.copy li::marker{color:var(--brass)}
.copy table{width:100%%;border-collapse:collapse;margin:24px 0;font-size:15px;font-family:var(--sans)}
.copy th{text-align:left;font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  padding:10px 12px;border-bottom:2px solid var(--ink);color:var(--soft)}
.copy td{padding:11px 12px;border-bottom:1px solid var(--rule);vertical-align:top}
.tblwrap{overflow-x:auto}
.tblwrap table{min-width:480px}
.pull{border-left:3px solid var(--claret);background:var(--paper2);padding:18px 22px;margin:26px 0;font-size:16px}

/* ------------------------------------------------------------ calculators */
.calc{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:48px;align-items:start;padding:8px 0 84px}
@media(max-width:900px){.calc{grid-template-columns:minmax(0,1fr)}}
.fields .fld{display:grid;grid-template-columns:1fr 190px;gap:18px;align-items:center;
  padding:13px 0;border-bottom:1px solid var(--rule)}
.fields label{font-size:15.5px}
.fields .hint{grid-column:1/-1;font-family:var(--sans);font-size:12px;color:var(--soft);margin-top:-6px}
.fields .inp{display:flex;align-items:center;border:1px solid var(--ink);background:#fff}
.fields .inp span{font-family:var(--sans);font-size:12px;color:var(--soft);padding:0 9px}
.fields input{width:100%%;min-width:0;border:0;padding:9px 8px;font-family:var(--mono);font-size:15px;
  color:var(--ink);background:transparent;text-align:right;-moz-appearance:textfield}
.fields input:focus{outline:none;background:var(--paper2)}
.fields input::-webkit-outer-spin-button,.fields input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.result{border:1px solid var(--ink);position:sticky;top:24px}
.result .cap{background:var(--ink);color:var(--paper);font-family:var(--sans);font-size:10.5px;
  font-weight:700;letter-spacing:.2em;text-transform:uppercase;padding:9px 18px}
.result .head{padding:22px 18px;border-bottom:1px solid var(--ink);background:var(--paper2)}
.result .head .l{font-family:var(--sans);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--soft)}
.result .head .v{font-family:var(--mono);font-size:2rem;margin-top:7px;letter-spacing:-.03em;word-break:break-word}
.result .row{display:flex;justify-content:space-between;gap:14px;padding:11px 18px;border-bottom:1px solid var(--rule);
  font-size:14px;align-items:baseline}
.result .row:last-child{border-bottom:0}
.result .row dt{font-family:var(--sans);color:var(--soft);font-size:13px}
.result .row dd{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.result .onote{padding:0 18px 11px;font-family:var(--sans);font-size:11.5px;color:var(--soft);
  border-bottom:1px solid var(--rule);margin-top:-6px;line-height:1.5}
.calcnote{font-family:var(--sans);font-size:13px;color:var(--soft);margin-top:26px;padding-top:18px;
  border-top:1px solid var(--rule);line-height:1.6}

/* ------------------------------------------------------------------- map */
.mapblock{border:1px solid var(--ink);margin-top:8px}
.mapblock iframe{display:block;width:100%%;height:340px;border:0}
.mapcap{font-family:var(--sans);font-size:12px;color:var(--soft);margin-top:9px}

/* ------------------------------------------------------- closing + colophon */
.closing{border-top:2px solid var(--ink);background:var(--paper2);padding:58px 0}
.closing .grid{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:44px;align-items:center}
@media(max-width:760px){.closing .grid{grid-template-columns:minmax(0,1fr)}}
.closing h2{font-size:1.7rem;font-weight:500;line-height:1.16;letter-spacing:-.018em;max-width:22ch}
.closing p{margin-top:12px;color:var(--soft);max-width:52ch}
.closing .acts{display:flex;gap:14px;flex-wrap:wrap}
.closing .btn{font-family:var(--sans);font-size:13px;font-weight:600;letter-spacing:.08em;
  text-transform:uppercase;padding:14px 24px;text-decoration:none;border:1px solid var(--ink)}
.closing .btn.solid{background:var(--ink);color:var(--paper)}
.closing .btn.solid:hover{background:var(--claret);border-color:var(--claret);color:#fff}
.closing .btn.ghost{color:var(--ink)}
.closing .btn.ghost:hover{background:var(--ink);color:var(--paper)}

.colophon{border-top:1px solid var(--rule);padding:46px 0 34px;font-family:var(--sans);font-size:13.5px;color:var(--soft)}
.colophon .cols{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:44px}
@media(max-width:780px){.colophon .cols{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.colophon .cols{grid-template-columns:1fr}}
.colophon .lbl{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink);
  margin-bottom:13px;font-family:var(--sans);font-weight:700;display:block}
.colophon ul{list-style:none}
.colophon li{margin-bottom:7px}
.colophon a{color:var(--soft);text-decoration:none}
.colophon a:hover{color:var(--claret)}
/* ------------------------------------------------------- contact widget */
/* Same job as the widget on every other site, drawn in this one's language:
   a filing tab clipped to the edge of the sheet, opening a panel built exactly
   like the particulars block in the hero. No bubble, no pill, no AI, no CRM —
   three plain links to a telephone, an inbox and the office. */
.helpdesk{position:fixed;right:26px;bottom:0;z-index:80;font-family:var(--sans)}
.hd-tab{display:flex;align-items:center;gap:9px;background:var(--claret);color:#fff;border:0;
  border-radius:3px 3px 0 0;padding:12px 20px;font:inherit;font-size:12.5px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;cursor:pointer;
  box-shadow:0 -2px 14px rgba(22,23,26,.22)}
.hd-tab:hover{background:var(--claretlt)}
.hd-tab svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:2}
.hd-tab .chev{transition:transform .18s ease}
.helpdesk.open .hd-tab .chev{transform:rotate(180deg)}
.hd-panel{display:none;width:310px;border:1px solid var(--ink);border-bottom:0;background:var(--paper);
  box-shadow:0 -8px 30px rgba(22,23,26,.2)}
.helpdesk.open .hd-panel{display:block}
.hd-panel .cap{background:var(--ink);color:var(--paper);font-size:10.5px;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;padding:9px 16px}
.hd-panel a{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:center;
  padding:13px 16px;border-bottom:1px solid var(--rule);text-decoration:none;color:var(--ink)}
.hd-panel a:last-of-type{border-bottom:0}
.hd-panel a:hover{background:var(--paper2)}
.hd-panel .ic{width:20px;height:20px;stroke:var(--claret);fill:none;stroke-width:1.8}
.hd-panel .t{font-size:14px;font-weight:600;line-height:1.3}
.hd-panel .t small{display:block;font-weight:400;color:var(--soft);font-size:12.5px;margin-top:2px;
  font-family:var(--mono);letter-spacing:-.02em}
.hd-panel .foot{padding:11px 16px;border-top:1px solid var(--rule);background:var(--paper2);
  font-size:11.5px;color:var(--soft);line-height:1.5}
@media(max-width:560px){.helpdesk{right:12px;left:12px}.hd-panel{width:auto}}
@media print{.helpdesk{display:none}}

.colophon .fine{margin-top:38px;padding-top:18px;border-top:1px solid var(--rule);
  display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;font-size:12px}
""" % dict(INK=INK, INK_SOFT=INK_SOFT, PAPER=PAPER, PAPER_2=PAPER_2, RULE=RULE,
           CLARET=CLARET, CLARET_LT=CLARET_LT, BRASS=BRASS)


# ---------------------------------------------------------------- the mark
# A window envelope: the rectangle an IRS notice arrives in, with the aperture
# offset the way a real one is. Reads at 20px, and it is specific to this practice
# rather than a generic ledger or column motif.
MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" '
        'fill="none" stroke="currentColor" stroke-width="2.6">'
        '<rect x="6" y="14" width="52" height="36"/>'
        '<rect x="13" y="34" width="22" height="9" stroke-width="2"/>'
        '<path d="M6 14l26 18 26-18" stroke-width="2"/></svg>')

NAV = [('services/index.html', 'Practice'), ('irs.html', 'IRS Problems'),
       ('calculators/index.html', 'Calculators'), ('about.html', 'The Firm'),
       ('contact.html', 'Contact')]


def rel(depth, path):
    return ('../' * depth) + path


def notice():
    return ('<div class="notice"><div class="sheet"><b>Demonstration site</b>'
            '<span>Prepared for ' + H.escape(F['name']) + ' by ScaleLocal. Not affiliated with, '
            'authorized by, or endorsed by the firm. Reproduction or use of this site or its '
            'contents is prohibited.</span></div></div>')


def masthead(d, current=None):
    links = ''
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        cls = ' class="portal"' if href == 'irs.html' else ''
        links += '<a href="' + rel(d, href) + '"' + cur + cls + '>' + label + '</a>'
    return (
        '<div class="masthead"><div class="sheet">'
        '<a class="wordmark" href="' + rel(d, 'index.html') + '">'
        '<span class="mk">' + MARK + '</span>'
        '<span class="nm">James L. Hickey, CPA<span>Tax &middot; Accounting &middot; Business Consulting</span></span></a>'
        '<div class="headcontact">' + F['addr'] + ', ' + F['city'] + ', ' + F['state'] + ' ' + F['zip'] + '<br>'
        '<a class="tel mono" href="tel:' + F['tel'] + '">' + F['ph'] + '</a></div>'
        '</div></div>'
        '<div class="navband"><div class="sheet">' + links +
        '<span class="spacer"></span>'
        '<a href="' + F['portal'] + '" rel="noopener">Client Portal &rarr;</a>'
        '</div></div>')


def closing(d, title=None, text=None):
    title = title or 'Tell us what the notice says.'
    text = text or ('Telephone the office, or write to ' + F['email'] + '. You will speak with a '
                    'CPA about what the letter actually asks for and what happens next.')
    return ('<section class="closing"><div class="sheet"><div class="grid"><div>'
            '<h2>' + H.escape(title) + '</h2><p>' + H.escape(text) + '</p></div>'
            '<div class="acts"><a class="btn solid" href="tel:' + F['tel'] + '">Call ' + F['ph'] + '</a>'
            '<a class="btn ghost" href="mailto:' + F['email'] + '">Write to the office</a></div>'
            '</div></div></section>')


def colophon(d):
    def col(h, items):
        return ('<div><span class="lbl">' + h + '</span><ul>' +
                ''.join('<li><a href="' + (i[0] if i[0].startswith('http') else rel(d, i[0])) + '">' + i[1] + '</a></li>'
                        for i in items) + '</ul></div>')
    return ('<footer class="colophon"><div class="sheet"><div class="cols">'
            '<div><span class="lbl">' + H.escape(F['name']) + '</span>'
            '<p style="max-width:34ch;line-height:1.7">A full service tax, accounting and business '
            'consulting practice on Main Street in Tewksbury, working with individuals, small '
            'businesses and non-profit organizations across the Merrimack Valley.</p>'
            '<p style="margin-top:14px"><span class="mono">' + F['addr'] + '<br>' + F['city'] + ', '
            + F['state'] + ' ' + F['zip'] + '</span></p></div>'
            + col('Practice', [('services/tax-preparation.html', 'Tax preparation'),
                               ('services/tax-planning.html', 'Tax planning'),
                               ('irs.html', 'IRS problem resolution'),
                               ('services/small-business-services.html', 'Small business services'),
                               ('services/quickbooks.html', 'QuickBooks'),
                               ('services/index.html', 'Full index')])
            + col('Office', [('contact.html', 'Contact and directions'),
                             ('about.html', 'About the firm'),
                             ('calculators/index.html', 'Calculators'),
                             ('faq.html', 'Common questions'),
                             (F['portal'], 'Client portal'),
                             ('pay.html', 'Paying an invoice')])
            + '</div><div class="fine"><span>&copy; <span id="yr"></span> ' + H.escape(F['name'])
            + '</span><span class="mono">' + F['ph'] + ' &middot; ' + F['email'] + '</span></div>'
            '</div></footer>')



def helpdesk(d):
    """Static contact widget. No CRM, no chatbot, no third-party script — three links
    and a note. Present on every page, same as every other site in the portfolio."""
    def row(href, ic, title, sub, ext=False):
        return ('<a href="' + href + '"' + (' rel="noopener"' if ext else '') + '>'
                '<span class="ic">' + ic + '</span>'
                '<span class="t">' + title + '<small>' + sub + '</small></span></a>')
    phone = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11 11 0 0 0 3.5.56 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11 11 0 0 0 .56 3.5 1 1 0 0 1-.25 1z"/></svg>')
    mail = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 6l9 7 9-7"/></svg>')
    cal = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>')
    lock = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="10" rx="1"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>')
    return ('<div class="helpdesk">'
            '<div class="hd-panel" id="hd-panel" hidden><div class="cap">Reach the office</div>'
            + row('tel:' + F['tel'], phone, 'Telephone', F['ph'])
            + row('mailto:' + F['email'], mail, 'Email', F['email'])
            + row(rel(d, 'contact.html'), cal, 'Request an appointment', 'Call or write to arrange one')
            + row(F['portal'], lock, 'Client portal', 'Secure document exchange', ext=True)
            + '<div class="foot">Documents containing a Social Security number should go through '
              'the portal rather than email.</div></div>'
            '<button class="hd-tab" aria-expanded="false" aria-controls="hd-panel">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H8l-4 4z"/></svg>'
            '<span>Contact</span>'
            '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>'
            '</button></div>')


SCRIPT = ('<script>(function(){'
          'var y=document.getElementById("yr");if(y)y.textContent=new Date().getFullYear();'
          'var hd=document.querySelector(".helpdesk");if(!hd)return;'
          'var btn=hd.querySelector(".hd-tab"),pan=hd.querySelector(".hd-panel");'
          'function set(o){hd.classList.toggle("open",o);btn.setAttribute("aria-expanded",o?"true":"false");'
          'if(o){pan.removeAttribute("hidden");}else{pan.setAttribute("hidden","");}}'
          'btn.addEventListener("click",function(e){e.stopPropagation();set(!hd.classList.contains("open"));});'
          'document.addEventListener("click",function(e){if(!hd.contains(e.target))set(false);});'
          'document.addEventListener("keydown",function(e){if(e.key==="Escape")set(false);});'
          '})();</script>')


def shell(p, body):
    d = p['depth']
    url = BASE + (p['path'][:-len('index.html')] if p['path'].endswith('index.html') else p['path'])
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<title>' + H.escape(p['title']) + '</title>'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="description" content="' + H.escape(p['desc']) + '">'
            '<meta name="robots" content="noindex, nofollow">'
            '<meta name="googlebot" content="noindex, nofollow">'
            '<link rel="canonical" href="' + url + '">'
            '<link rel="apple-touch-icon" href="' + rel(d, 'apple-touch-icon.png') + '">'
            '<meta property="og:type" content="website"><meta property="og:url" content="' + url + '">'
            '<meta property="og:title" content="' + H.escape(p['title']) + '">'
            '<meta property="og:description" content="' + H.escape(p['desc']) + '">'
            '<meta property="og:image" content="' + BASE + 'og.png">'
            '<meta property="og:image:width" content="1200">'
            '<meta property="og:image:height" content="630">'
            '<meta property="og:site_name" content="' + H.escape(F['name']) + '">'
            '<meta property="og:image:alt" content="' + H.escape(F['name']) + ' — Tax, Accounting and Business Consulting">'
            '<meta name="twitter:card" content="summary_large_image">'
            '<meta name="twitter:title" content="' + H.escape(p['title']) + '">'
            '<meta name="twitter:description" content="' + H.escape(p['desc']) + '">'
            '<meta name="twitter:image" content="' + BASE + 'og.png">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@400;500;600&'
            'family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="' + rel(d, 'css/hickey.css') + '">'
            + ''.join('<script type="application/ld+json">' + json.dumps(s) + '</script>' for s in p.get('schema', []))
            + '</head><body>'
            + notice() + masthead(d, p.get('nav')) + body
            + closing(d, *p.get('closing', ()))
            + colophon(d) + notice() + helpdesk(d)
            + SCRIPT + '</body></html>')


def write(p, body):
    fp = os.path.join(OUT, p['path'])
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(shell(p, body))
    return p['path']
