# -*- coding: utf-8 -*-
"""
ScaleLocal multi-page build engine — firm-agnostic.
Firm facts, theme, nav, logo and content live in firms/<slug>.py; this file is the engine.
Select a firm with the BUILD_FIRM env var (defaults to kpw-cpa).
Separate multi-page engine (HANDOFF v2.2 §13 P0 engine-split). Inherits the
gen_sites.py design system (typography, tokens, components); does NOT touch gen_sites.py.
Staging posture: every page noindex,nofollow (§10.1 layer 1).
"""
import json, os, html, re, importlib

SLUG = os.environ.get('BUILD_FIRM', 'kpw-cpa')
_F = importlib.import_module('firms.' + SLUG.replace('-', '_'))

OUT = os.path.join(os.path.dirname(__file__), 'out', SLUG)
BASE = 'https://www.scalelocal.net/test-builds/' + SLUG + '/'

FIRM = _F.FIRM          # firm facts, sourced only (see the firm's RESEARCH notes)
T = _F.T                # theme tokens
NAV = _F.NAV            # nav model
LOGO = _F.LOGO          # inline SVG lettermark, designed per firm
PRESERVED = getattr(_F, 'PRESERVED', {})   # portals / payment links carried over verbatim
FIRM['name_html'] = html.escape(FIRM['name'])   # firm names contain '&'; never emit it raw

import design as _design
D = _design.resolve(getattr(_F, 'DESIGN', 'ledger'))   # typography + composition, per firm

CSS = r"""
:root{--ink:__INK__;--ink2:__INK2__;--acc:__ACC__;--accd:__ACCD__;--accrgb:__ACCRGB__;--cream:__CREAM__;
--paper:#fffdf8;--line:#e7e2d7;--muted:#5d5f58;--gold:#E8B33F;--goldl:#F5C453;
--serif:__SERIF__;--sans:__SANS__;
--sh1:__SH1__;--sh2:__SH2__;--r:__RADIUS__;--rs:__RADIUS_SM__;--bw:__BORDER__;}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:78px}
body{font-family:var(--sans);color:var(--ink);background:var(--paper);line-height:__LH__;font-size:__BODY__;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
img{display:block;max-width:100%}
a{color:var(--accd)}
::selection{background:var(--acc);color:#15130e}
:focus-visible{outline:2.5px solid var(--acc);outline-offset:3px;border-radius:3px}
.wrap{max-width:1160px;margin:0 auto;padding:0 26px}
section[id]{scroll-margin-top:78px}
h1,h2,h3,h4{font-family:var(--serif);font-weight:__HWEIGHT__;line-height:1.16;letter-spacing:__HTRACK__}
h1{font-size:__H1__}
h2{font-size:__H2__}
h3{font-size:1.35rem}
.eyebrow{display:inline-flex;align-items:center;gap:11px;font-size:.73rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:var(--accd);margin-bottom:18px}
.eyebrow::before{content:"";width:28px;height:2px;background:var(--acc)}
.eyebrow.on-dark{color:#e8d3a8}.eyebrow.on-dark::before{background:var(--acc)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 30px;border-radius:var(--rs);font-weight:600;font-size:1rem;text-decoration:none;border:1.5px solid transparent;cursor:pointer;transition:transform .18s ease,background .2s,box-shadow .2s}
.btn .arr{width:18px;height:18px;transition:transform .2s ease}
.btn:hover .arr{transform:translateX(3px)}
.b-acc{background:var(--acc);color:#15130e;box-shadow:0 10px 26px rgba(var(--accrgb),.36)}
.b-acc:hover{background:var(--accd);color:#fff;transform:translateY(-2px)}
.b-gh{border-color:rgba(255,255,255,.5);color:#fff}.b-gh:hover{background:rgba(255,255,255,.12);transform:translateY(-2px)}
.b-dk{background:var(--ink);color:#fff}.b-dk:hover{background:var(--ink2);transform:translateY(-2px)}
.b-ln{border-color:var(--ink);color:var(--ink)}.b-ln:hover{background:var(--ink);color:#fff}
.demostrip{background:#23211d;color:#e8e3d8;font-size:.72rem;line-height:1.5;letter-spacing:.015em;padding:9px 0;border-bottom:1px solid rgba(var(--accrgb),.55)}
.demostrip.bottom{border-bottom:none;border-top:1px solid rgba(var(--accrgb),.55)}
.demostrip .wrap{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;justify-content:center;text-align:center}
.demostrip b{color:var(--gold);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.66rem;white-space:nowrap}
@media print{.demostrip{background:#fff;color:#000;border-color:#000}.demostrip b{color:#000}}
.topbar{background:var(--ink);color:#cfcbc1;font-size:.82rem;padding:9px 0}
.topbar .wrap{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:center}
.topbar a{color:#fff;text-decoration:none;font-weight:600}
.hdr{background:rgba(255,253,248,.88);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:60;transition:box-shadow .25s}
.hdr .wrap{display:flex;align-items:center;justify-content:space-between;padding:13px 26px;gap:16px}
.hdr.small{box-shadow:0 6px 20px rgba(20,18,12,.08)}
.brand{display:flex;align-items:center;gap:13px;text-decoration:none}
.mark{width:50px;height:50px;flex:0 0 50px;color:var(--ink);display:block}
.mark svg{width:100%;height:100%;display:block}
.mark svg text{font-family:var(--serif);font-weight:600}
.brand:hover .mark{color:var(--accd)}
.mark,.brand:hover .mark{transition:color .2s}
.bt{font-family:var(--serif);font-size:1.18rem;color:var(--ink);line-height:1.05}
.bt small{display:block;font-family:var(--sans);font-size:.58rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accd);margin-top:3px;font-weight:600}
nav{display:flex;align-items:center;gap:24px}
nav a{text-decoration:none;color:var(--ink);opacity:.78;font-size:.94rem;font-weight:500;transition:.2s;white-space:nowrap}
nav a:hover,nav a[aria-current]{opacity:1;color:var(--accd)}
.ncta{background:var(--ink);color:#fff !important;opacity:1 !important;padding:11px 20px !important;border-radius:var(--rs);font-weight:600}
.ncta:hover{background:var(--accd)}
.toggle{display:none;background:none;border:var(--bw) solid var(--line);border-radius:var(--rs);padding:9px 12px;font-size:1.1rem;cursor:pointer;color:var(--ink)}
.hero{position:relative;color:#fff;min-height:72vh;display:flex;align-items:center;overflow:hidden;background:radial-gradient(1100px 560px at 80% 15%,rgba(var(--accrgb),.30),transparent 60%),linear-gradient(155deg,var(--ink),var(--ink2))}
.hero::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.055) 1px,transparent 1px);background-size:24px 24px;opacity:.6}
.hero-art{position:absolute;right:-30px;top:50%;transform:translateY(-50%);width:min(46vw,560px);opacity:.09;stroke:#fff;stroke-width:2;fill:none;pointer-events:none}
.hero .wrap{position:relative;z-index:2;padding:96px 26px;width:100%}
.hero h1{color:#fff;max-width:21ch}
.hero .sub{max-width:56ch;margin-top:20px;font-size:1.16rem;color:#ece7dc}
.acts{margin-top:32px;display:flex;gap:14px;flex-wrap:wrap}
.hero-trust{margin-top:26px;display:flex;gap:20px;flex-wrap:wrap;font-size:.86rem;color:#d7d3c9;align-items:center}
.hero-trust b{color:#fff;font-weight:600}
.phero{position:relative;color:#fff;background:radial-gradient(900px 420px at 85% 0%,rgba(var(--accrgb),.28),transparent 60%),linear-gradient(155deg,var(--ink),var(--ink2));overflow:hidden}
.phero::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:24px 24px;opacity:.55}
.phero .wrap{position:relative;z-index:2;padding:72px 26px 64px}
.phero h1{color:#fff;max-width:25ch}
.phero .sub{max-width:62ch;margin-top:16px;font-size:1.1rem;color:#e6e1d5}
.crumbs{position:relative;z-index:2;font-size:.8rem;color:#c9c4b8;margin-bottom:22px}
.crumbs a{color:#e8d3a8;text-decoration:none}.crumbs a:hover{text-decoration:underline}
.crumbs span{margin:0 7px;opacity:.6}
.strip{background:var(--ink);color:#fff;border-top:1px solid rgba(255,255,255,.08)}
.strip .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:34px 26px}
.strip .cell{text-align:center;padding:6px 10px;border-right:1px solid rgba(255,255,255,.1)}
.strip .cell:last-child{border-right:none}
.strip .n{font-family:var(--serif);font-size:1.95rem;line-height:1;color:#fff}
.strip .l{font-size:.82rem;color:#b9b5ab;margin-top:9px}
.sec{padding:__SECPAD__ 0}
.sec.tint{background:var(--cream)}
.sec.dark{background:var(--ink);color:#e9e5db}
.sec.dark h2{color:#fff}.sec.dark .lead{color:#c4c0b6}
.sec.accent{background:linear-gradient(150deg,var(--ink),var(--ink2));color:#fff;position:relative;overflow:hidden}
.sec.accent::before{content:"";position:absolute;right:-120px;top:-120px;width:440px;height:440px;border-radius:50%;background:radial-gradient(circle,rgba(var(--accrgb),.32),transparent 66%)}
.sec-head{max-width:680px;margin-bottom:48px}
.lead{font-size:1.1rem;color:var(--muted);margin-top:14px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.cards.two{grid-template-columns:repeat(2,1fr)}
.card{position:relative;background:var(--paper);border:var(--bw) solid var(--line);border-radius:var(--r);padding:30px 28px;transition:transform .25s,box-shadow .25s,border-color .25s;box-shadow:var(--sh1);display:block;text-decoration:none;color:var(--ink)}
a.card:hover{transform:translateY(-6px);box-shadow:var(--sh2);border-color:rgba(var(--accrgb),.55)}
.card .num{position:absolute;top:26px;right:28px;font-family:var(--serif);font-size:.9rem;color:var(--acc);opacity:.6}
.cic{width:52px;height:52px;border-radius:14px;background:rgba(var(--accrgb),.12);display:flex;align-items:center;justify-content:center;color:var(--accd);margin-bottom:20px}
.cic svg{width:26px;height:26px}
.card h3{font-size:1.2rem;margin-bottom:9px}
.card p{font-size:.94rem;color:var(--muted)}
.card .more{display:inline-flex;align-items:center;gap:7px;margin-top:16px;font-size:.88rem;font-weight:600;color:var(--accd);white-space:nowrap}
.card .more .arr{width:16px;height:16px;flex:0 0 16px}
.prose{max-width:760px}
.prose h2{margin:44px 0 16px;font-size:clamp(1.5rem,2.6vw,2rem)}
.prose h3{margin:30px 0 12px}
.prose p{margin-bottom:16px;color:#3c4038}
.prose ul,.prose ol{margin:0 0 18px 22px;color:#3c4038}
.prose li{margin-bottom:8px}
.prose li::marker{color:var(--accd)}
.prose strong{color:var(--ink)}
.prose .callout{background:var(--cream);border-left:3px solid var(--acc);border-radius:0 12px 12px 0;padding:20px 24px;margin:26px 0}
.prose .callout p:last-child{margin-bottom:0}
.split{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:56px;align-items:start}
.split>*{min-width:0}
.prose{min-width:0}
.aside{position:sticky;top:96px;display:grid;gap:18px}
.acard{background:var(--ink);border-radius:var(--r);padding:30px;color:#e9e5db;box-shadow:var(--sh2)}
.acard .t{font-family:var(--serif);font-size:1.2rem;color:#fff;margin-bottom:14px}
.acard p{font-size:.9rem;color:#c4c0b6;margin-bottom:16px}
.acard .btn{width:100%}
.acard.light{background:var(--cream);color:var(--ink);box-shadow:var(--sh1);border:var(--bw) solid var(--line)}
.acard.light .t{color:var(--ink)}
.acard.light ul{list-style:none;display:grid;gap:10px;font-size:.92rem}
.acard.light li a{text-decoration:none;color:var(--ink);display:flex;gap:9px;align-items:baseline}
.acard.light li a:hover{color:var(--accd)}
.acard.light li::before{display:none}
.acard.light .ck{color:var(--accd);font-weight:700}
.faq{max-width:820px;display:grid;gap:14px}
.faq details{background:var(--paper);border:var(--bw) solid var(--line);border-radius:14px;box-shadow:var(--sh1);overflow:hidden}
.faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px 24px;font-family:var(--serif);font-size:1.08rem;font-weight:600}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:1.4rem;color:var(--accd);transition:transform .2s;line-height:1}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq .fa{padding:0 24px 22px;color:#3c4038;font-size:.97rem}
.faq .fa p{margin-bottom:12px}.faq .fa p:last-child{margin-bottom:0}
.faq .fa ul{margin:0 0 12px 20px}
.tgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.tcard{background:var(--paper);border:var(--bw) solid var(--line);border-radius:var(--r);padding:30px 28px;box-shadow:var(--sh1);text-decoration:none;color:var(--ink);transition:transform .25s,box-shadow .25s,border-color .25s;display:block}
a.tcard:hover{transform:translateY(-6px);box-shadow:var(--sh2);border-color:rgba(var(--accrgb),.55)}
.tava{width:64px;height:64px;border-radius:50%;background:linear-gradient(145deg,var(--ink),var(--ink2));color:#fff;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:1.3rem;margin-bottom:18px}
.tcard h3{font-size:1.22rem}
.tcard .cred{color:var(--accd);font-weight:600;font-size:.85rem;letter-spacing:.06em;margin:4px 0 10px}
.tcard p{font-size:.92rem;color:var(--muted)}
.offices{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.office{background:var(--paper);border:var(--bw) solid var(--line);border-radius:var(--r);padding:34px;box-shadow:var(--sh1)}
.office h3{margin-bottom:6px}
.office .oloc{color:var(--accd);font-weight:600;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:16px}
.office ul{list-style:none;display:grid;gap:9px;font-size:.96rem;color:#3c4038}
.office a{color:var(--ink);text-decoration:none;font-weight:500}.office a:hover{color:var(--accd)}
.office .acts{margin-top:22px}
.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:20px 0;max-width:100%}
.tscroll table.plain{margin:0;min-width:520px}
table.plain{width:100%;border-collapse:collapse;margin:20px 0;font-size:.95rem}
table.plain th{text-align:left;font-family:var(--serif);font-weight:600;padding:12px 14px;background:var(--cream);border:var(--bw) solid var(--line)}
table.plain td{padding:12px 14px;border:var(--bw) solid var(--line);color:#3c4038;vertical-align:top}
.mapwrap{position:relative;border-radius:var(--r);overflow:hidden;border:var(--bw) solid var(--line);box-shadow:var(--sh1);aspect-ratio:16/9;background:var(--cream)}
.mapwrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
.mapcap{font-size:.86rem;color:var(--muted);margin-top:12px}
@media(max-width:560px){.mapwrap{aspect-ratio:4/3}}
.cta{background:linear-gradient(150deg,var(--ink),var(--ink2));color:#fff;text-align:center;padding:84px 0;position:relative;overflow:hidden}
.cta::before{content:"";position:absolute;left:50%;top:-150px;transform:translateX(-50%);width:560px;height:360px;background:radial-gradient(circle,rgba(var(--accrgb),.3),transparent 66%)}
.cta .wrap{position:relative;z-index:2}
.cta h2{color:#fff}
.cta p{max-width:56ch;margin:14px auto 0;color:#d7d3c9;font-size:1.1rem}
.cta .acts{justify-content:center;margin-top:30px}
.foot{background:#0e1826;color:#a7a39a;padding:60px 0 30px;font-size:.92rem}
.foot .fh{font-family:var(--serif);color:#fff;font-weight:500;margin-bottom:14px;font-size:1.12rem;line-height:1.2}
.foot a{color:#cfcbc1;text-decoration:none;transition:.2s}.foot a:hover{color:#fff}
.fgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1.3fr;gap:40px;margin-bottom:42px}
.fgrid ul{list-style:none;display:grid;gap:9px}
.fbot{border-top:1px solid rgba(255,255,255,.12);padding-top:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:.8rem;color:#918d84}
.launch{position:fixed;right:20px;bottom:20px;z-index:90}
.lbtn{display:flex;align-items:center;gap:10px;background:var(--gold);color:var(--ink);border:none;border-radius:999px;padding:16px 27px;font-size:.98rem;font-weight:700;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.28),0 14px 34px rgba(232,179,63,.30);transition:transform .2s,box-shadow .2s,background .2s}
.lbtn:hover{transform:translateY(-2px);background:var(--goldl);box-shadow:0 8px 22px rgba(0,0,0,.32),0 18px 42px rgba(232,179,63,.42)}
.lbtn svg{stroke:var(--ink)}
.lbtn svg{width:22px;height:22px}
.lpanel{position:absolute;right:0;bottom:74px;width:300px;background:var(--paper);border:2px solid var(--gold);border-radius:var(--r);box-shadow:0 22px 54px rgba(0,0,0,.26);padding:15px;display:none;transform-origin:bottom right;animation:pop .18s ease}
@keyframes pop{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:scale(1)}}
.launch.open .lpanel{display:block}
.lhead{font-family:var(--serif);font-size:1.12rem;padding:5px 9px 13px}
.lact{display:flex;align-items:center;gap:13px;padding:12px 10px;border-radius:11px;text-decoration:none;color:var(--ink);font-weight:500;transition:.15s}
.lact:hover{background:var(--cream)}
.lact .ic{width:37px;height:37px;flex:0 0 37px;border-radius:10px;background:rgba(var(--accrgb),.13);display:flex;align-items:center;justify-content:center;color:var(--accd)}
.lact .ic svg{width:17px;height:17px}
.lact small{display:block;font-weight:400;color:var(--muted);font-size:.78rem}
.lnote{font-size:.76rem;color:var(--muted);padding:10px;border-top:1px solid var(--line);margin-top:6px}
.reveal{opacity:0;transform:translateY(20px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.75,.25,1)}
.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}*{scroll-behavior:auto}}
@media(max-width:980px){.split{grid-template-columns:minmax(0,1fr)}.aside{position:static}.fgrid{grid-template-columns:1fr 1fr}}
@media(max-width:920px){.strip .wrap{grid-template-columns:repeat(2,1fr);gap:24px 10px}.strip .cell:nth-child(2){border-right:none}.tgrid,.cards{grid-template-columns:repeat(2,1fr)}.offices{grid-template-columns:1fr}}
@media(max-width:860px){
 nav{display:none;position:absolute;top:100%;left:0;right:0;background:var(--paper);border-bottom:1px solid var(--line);flex-direction:column;gap:2px;padding:14px 26px 20px;box-shadow:0 16px 26px rgba(0,0,0,.1);align-items:stretch}
 nav.open{display:flex}nav a{padding:13px 10px;width:100%;border-radius:var(--rs)}
 .ncta{text-align:center;margin-top:8px}.toggle{display:block}
 .cards,.tgrid{grid-template-columns:1fr}.hero-art{opacity:.05}}
@media(max-width:560px){
 body{font-size:16px}.sec{padding:60px 0}.wrap{padding:0 20px}
 .hero .wrap{padding:72px 20px}.hero{min-height:74vh}
 .phero .wrap{padding:56px 20px 48px}
 .acts{flex-direction:column}.acts .btn{width:100%}
 .strip .wrap{grid-template-columns:1fr 1fr;padding:28px 20px}.strip .n{font-size:1.5rem}
 .office{padding:26px}.fgrid{grid-template-columns:1fr;gap:30px}
 .topbar .tb-l{display:none}.topbar .wrap{justify-content:center}
 .lbtn .lbl{display:none}.lbtn{padding:16px;border-radius:50%}.cta{padding:60px 0}
 .bt small{display:none}}
"""
def _design_css(D):
    """Composition overrides. These are structural, not decorative — they change how
    the hero is built, how a card is expressed, where the nav sits and how an eyebrow
    is drawn. Without them every firm gets the same page in a different colour."""
    css = []

    # ---------------------------------------------------------------- hero
    if D['hero'] == 'rule':
        css.append("""
.hero{min-height:auto;background:linear-gradient(150deg,var(--ink),var(--ink2))}
.hero .wrap{padding:104px 26px 96px;border-left:4px solid var(--acc);margin-left:26px}
.hero h1{max-width:19ch}
.hero-art{display:none}
.hero .sub{max-width:52ch}""")
    elif D['hero'] == 'statement':
        css.append("""
.hero{min-height:auto;background:var(--cream);color:var(--ink)}
.hero::after{display:none}
.hero .wrap{padding:112px 26px 100px;text-align:center;max-width:900px}
.hero h1{color:var(--ink);max-width:none;margin:0 auto}
.hero .sub{color:#43463e;margin:22px auto 0;max-width:58ch}
.hero .acts,.hero-trust{justify-content:center}
.hero-trust{color:#5d5f58}.hero-trust b{color:var(--ink)}
.hero .eyebrow.on-dark{color:var(--accd)}
.hero-art{display:none}
.hero .b-gh{border-color:var(--ink);color:var(--ink)}
.hero .b-gh:hover{background:var(--ink);color:#fff}""")
    elif D['hero'] == 'panel':
        css.append("""
.hero{min-height:auto;background:var(--ink)}
.hero::after{display:none}
.hero .wrap{padding:0 26px;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:0;align-items:stretch}
.hero .wrap>div:first-child{padding:96px 56px 96px 0}
.hero-art{display:none}
.hero h1{max-width:16ch}
@media(max-width:900px){.hero .wrap{grid-template-columns:minmax(0,1fr)}.hero .wrap>div:first-child{padding:80px 0}}""")
    elif D['hero'] == 'rail':
        # Asymmetric left rail. Drawn as a decoration, NOT a grid column — the hero
        # markup has a single child, so a two-column grid crushes the h1 into 200px.
        css.append("""
.hero{min-height:auto;background:var(--paper);color:var(--ink)}
.hero::after{display:none}
.hero .wrap{padding:92px 26px 84px 96px;position:relative}
.hero .wrap::before{content:"";position:absolute;left:34px;top:98px;bottom:90px;width:1px;background:var(--line)}
.hero .wrap::after{content:"";position:absolute;left:26px;top:98px;width:18px;height:3px;background:var(--acc)}
.hero h1{color:var(--ink);max-width:22ch}
.hero .sub{color:#43463e}
.hero-trust{color:#5d5f58}.hero-trust b{color:var(--ink)}
.hero .eyebrow.on-dark{color:var(--accd)}
.hero-art{display:none}
.hero .b-gh{border-color:var(--ink);color:var(--ink)}
.hero .b-gh:hover{background:var(--ink);color:#fff}
@media(max-width:860px){.hero .wrap{padding-left:26px}.hero .wrap::before,.hero .wrap::after{display:none}}""")
    elif D['hero'] == 'split':
        css.append("""
.hero{min-height:auto}
.hero .wrap{padding:104px 26px}
.hero h1{max-width:18ch}
.hero-art{width:min(38vw,440px);opacity:.13}""")

    # ---------------------------------------------------------------- cards
    if D['cards'] == 'flat':
        css.append("""
.card{box-shadow:none;background:transparent;border:0;border-top:2px solid var(--line);border-radius:0;padding:26px 0 0}
.card:hover{transform:none;box-shadow:none;border-top-color:var(--acc)}
.cic{display:none}
.card h3{margin-bottom:10px}""")
    elif D['cards'] == 'ruled':
        css.append("""
.card{box-shadow:none;background:transparent;border:0;border-left:2px solid var(--line);border-radius:0;padding:4px 0 4px 24px}
.card:hover{transform:none;box-shadow:none;border-left-color:var(--acc)}
.cic{width:38px;height:38px;border-radius:0;background:transparent;color:var(--accd);margin-bottom:14px}
.card .num{display:none}""")
    elif D['cards'] == 'numbered':
        css.append("""
.card{box-shadow:none;background:var(--cream);border:0;border-top:3px solid var(--ink);border-radius:0;padding:28px 24px}
.card:hover{transform:translateY(-3px);box-shadow:var(--sh2);border-top-color:var(--acc)}
.cic{display:none}
.card .num{position:static;display:block;font-family:var(--serif);font-size:2rem;line-height:1;
  color:var(--accd);opacity:1;margin-bottom:14px;font-weight:700}""")

    # ---------------------------------------------------------------- nav
    if D['nav'] == 'center':
        css.append("""
.hdr .wrap{flex-direction:column;gap:14px;padding:20px 26px 16px}
.brand{justify-content:center}
nav{gap:20px;flex-wrap:wrap;justify-content:center}
.ncta{order:99}
@media(max-width:860px){.hdr .wrap{flex-direction:row}}""")
    elif D['nav'] == 'stacked':
        css.append("""
.hdr .wrap{flex-wrap:wrap;padding:14px 26px 0}
.brand{flex:1 1 auto}
nav{flex:1 0 100%;order:9;gap:22px;border-top:1px solid var(--line);margin-top:12px;padding:10px 0}
.ncta{margin-left:auto}
@media(max-width:860px){nav{border-top:0}}""")

    # ---------------------------------------------------------------- eyebrow
    if D['eyebrow'] == 'caps':
        css.append("""
.eyebrow::before{display:none}
.eyebrow{letter-spacing:.3em;gap:0}""")
    elif D['eyebrow'] == 'bracket':
        css.append("""
.eyebrow{gap:8px;flex-wrap:nowrap;align-items:flex-start}
.eyebrow::before{content:"[";width:auto;height:auto;background:none;color:var(--acc);font-size:1.15em;line-height:1.1;flex:0 0 auto}
.eyebrow::after{content:"]";color:var(--acc);font-size:1.15em;line-height:1.1;flex:0 0 auto}""")

    # ---------------------------------------------------------------- texture
    if not D['dots']:
        css.append("""
.hero::after,.phero::after{display:none}""")

    return '\n'.join(css)


CSS = (CSS.replace('__INK__', T['ink']).replace('__INK2__', T['ink2']).replace('__ACCD__', T['accd'])
          .replace('__ACCRGB__', T['accrgb']).replace('__ACC__', T['acc']).replace('__CREAM__', T['cream']))
for _k, _v in (('__SERIF__', D['serif']), ('__SANS__', D['sans']), ('__SH1__', D['sh1']),
               ('__SH2__', D['sh2']), ('__RADIUS_SM__', D['radius_sm']), ('__RADIUS__', D['radius']),
               ('__BORDER__', D['border']), ('__H1__', D['h1']), ('__H2__', D['h2']),
               ('__HWEIGHT__', D['hweight']), ('__HTRACK__', D['htrack']), ('__BODY__', D['body']),
               ('__LH__', D['lh']), ('__SECPAD__', D['sec_pad'])):
    CSS = CSS.replace(_k, _v)
CSS += _design_css(D)

ARROW = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

ICONS = {
 'ledger':'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h4"/>',
 'shield':'<path d="M12 3 5 6v5c0 4.2 3 7.4 7 9 4-1.6 7-4.8 7-9V6z"/><path d="M9.5 12l2 2 3.5-3.5"/>',
 'scale':'<path d="M12 4v16M7 20h10M12 6l-5 2 0 0a5 5 0 0 0 10 0l-5-2z" transform="translate(0,0)"/><path d="M5 8h14"/>',
 'chart':'<path d="M4 20h16M7 16v-5M12 16V7M17 16v-8"/>',
 'calc':'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"/>',
 'handshake':'<path d="M4 12l4-4 4 3 4-3 4 4M8 8v8M16 8v8M4 12v4h4M20 12v4h-4"/>',
 'gavel':'<path d="M13 5l6 6M11 7l6 6M9 9l6 6M3 21l7-7M14 4l-4 4 6 6 4-4z"/>',
 'estate':'<path d="M4 11 12 5l8 6M6 10v9h12v-9"/><path d="M10 19v-5h4v5"/>',
 'merge':'<circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="12" r="2.5"/><path d="M8 7c4 1 4 4 7.5 4.6M8 17c4-1 4-4 7.5-4.6"/>',
 'vault':'<rect x="4" y="4" width="16" height="16" rx="2"/><circle cx="12" cy="12" r="4"/><path d="M12 8v2M12 14v2M8 12h2M14 12h2"/>',
 'star':'<path d="M12 3l2.5 5.4 5.5.7-4 4 1 5.9-5-3-5 3 1-5.9-4-4 5.5-.7z"/>',
 'plan':'<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M16 2v4M8 2v4M3 9h18M8 14h3M8 17h6"/>',
 'building':'<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 'gov':'<path d="M4 21h16M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 10h18L12 4z"/>',
 'mic':'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/>',
 'crane':'<path d="M3 21h18M6 21V8l9-4v17M15 8h5v4h-5M9 12h2M9 16h2"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'people':'<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="9" r="2.6"/><path d="M15.5 14.6A4.8 4.8 0 0 1 21 19.5"/>',
 'doc':'<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
 'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 'pin':'<path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
}
def icon(k):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS.get(k, ICONS['ledger'])+'</svg>'

_GLYPHS = {
  # rising columns (the original)
  'columns': '<path d="M34 96V54l16-10v52M58 96V40l16-10v66M82 96V64l16-10v42M24 96h84"/>',
  # concentric seal — weight and permanence, for a long-established practice
  'seal':    '<circle cx="64" cy="64" r="40"/><circle cx="64" cy="64" r="29"/><path d="M64 24v80M24 64h80"/>',
  # plain weave — the Lowell mills
  'weave':   ('<path d="M30 30h68M30 52h68M30 74h68M30 96h68"/>'
              '<path d="M30 30v68M52 30v68M74 30v68M96 30v68"/>'),
  # open arc — the least corporate of the set
  'arc':     '<path d="M20 100a44 44 0 0 1 88 0"/><path d="M40 100a24 24 0 0 1 48 0"/><path d="M64 100V28"/>',
  # ruled column — an examiner's tick sheet
  'rule':    ('<path d="M28 26h72M28 50h72M28 74h72M28 98h72"/>'
              '<path d="M44 18v88"/>'),
  # modular grid — a brand system rather than a ledger
  'grid':    ('<path d="M26 26h32v32H26zM70 26h32v32H70zM26 70h32v32H26zM70 70h32v32H70z"/>'),
  'none':    '',
}
GLYPH = _GLYPHS.get(D.get('glyph', 'columns'), _GLYPHS['columns'])

def favicon():
    """Favicon uses the simplified single-letter variant of the ruled lettermark —
    A multi-letter mark turns to mush below 24px; a single letter stays legible at 16px."""
    from urllib.parse import quote
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
           "<rect width='64' height='64' rx='11' fill='" + T['ink'] + "'/>"
           "<rect x='14' y='16' width='36' height='2.6' fill='#ffffff'/>"
           "<rect x='14' y='46' width='36' height='2.6' fill='#ffffff'/>"
           "<text x='32' y='40.5' text-anchor='middle' fill='#ffffff' "
           "font-family='Georgia,serif' font-weight='700' font-size='25'>" + FIRM['favicon_letter'] + "</text></svg>")
    return 'data:image/svg+xml,' + quote(svg)


def gmap(caption=None):
    """Interactive Google Map of the office. Keyless embed, lazy-loaded."""
    from urllib.parse import quote_plus
    q = quote_plus(FIRM['addr'] + ', ' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'])
    return ('<div class="mapwrap reveal">'
      '<iframe title="Interactive Google map showing ' + html.escape(FIRM['name']) + ' at '
      + html.escape(FIRM['addr'] + ', ' + FIRM['city'] + ', ' + FIRM['state']) + '" '
      'src="https://maps.google.com/maps?q='+q+'&amp;t=&amp;z=15&amp;ie=UTF8&amp;iwloc=&amp;output=embed" '
      'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>'
      + ('<p class="mapcap">'+caption+'</p>' if caption else ''))

# ---------------- nav model comes from the firm profile (see top of file) ----------------

def rel(depth, path):
    return ('../'*depth)+path

def head(p):
    url = BASE + p['path'].replace('index.html','') if p['path'].endswith('index.html') else BASE + p['path']
    d = p['depth']
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
      '<title>'+html.escape(p['title'])+'</title>'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
      '<meta name="description" content="'+html.escape(p['desc'])+'">'
      '<meta name="robots" content="noindex, nofollow"><meta name="googlebot" content="noindex, nofollow">'
      '<link rel="canonical" href="'+url+'">'
      '<meta name="theme-color" content="'+T['ink']+'">'
      '<meta property="og:type" content="website"><meta property="og:site_name" content="'+html.escape(FIRM['name'])+'">'
      '<meta property="og:title" content="'+html.escape(p['title'])+'"><meta property="og:description" content="'+html.escape(p['desc'])+'">'
      '<meta property="og:url" content="'+url+'"><meta property="og:image" content="'+BASE+'og.png">'
      '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
      '<meta property="og:image:alt" content="'+html.escape(FIRM['name'])+' — '+html.escape(re.sub(r'&amp;','&',FIRM['brand_sub']))+'">'
      '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+html.escape(p['title'])+'">'
      '<meta name="twitter:description" content="'+html.escape(p['desc'])+'"><meta name="twitter:image" content="'+BASE+'og.png">'
      '<link rel="apple-touch-icon" href="'+rel(d,'apple-touch-icon.png')+'">'
      '<link rel="icon" type="image/svg+xml" href="'+favicon()+'">'
      '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family='+D['gfont']+'&display=swap" rel="stylesheet">'
      '<link rel="stylesheet" href="'+rel(d,'css/site.css')+'">'
      + ''.join('<script type="application/ld+json">'+json.dumps(s, separators=(',',':'))+'</script>' for s in p.get('schema',[]))
      + '</head><body>')

DEMO_NOTICE = ('Prepared for ' + FIRM['name_html'] + ' by ScaleLocal. '
    'Not affiliated with, authorized by, or endorsed by the firm. '
    'Reproduction or use of this site or its contents is prohibited.')

def demostrip(bottom=False):
    """Thin non-affiliation notice, top and bottom of every page (ScaleLocal house rule).
    Legally load-bearing part is the non-affiliation sentence - it is what keeps the
    build inside nominative fair use while the firm's name is on it."""
    return ('<div class="demostrip' + (' bottom' if bottom else '') + '" role="note">'
            '<div class="wrap"><b>Demonstration site</b><span>' + DEMO_NOTICE + '</span></div></div>')

def header(p):
    d = p['depth']
    links = ''
    for href, label, key in NAV:
        cur = ' aria-current="page"' if p.get('nav')==key else ''
        links += '<a href="'+rel(d,href)+'"'+cur+'>'+label+'</a>'
    return ('<div class="topbar"><div class="wrap"><span class="tb-l">'+FIRM['topbar']+'</span>'
      '<span class="tb-r"><a href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a></span></div></div>'
      '<header class="hdr"><div class="wrap"><a class="brand" href="'+rel(d,'index.html')+'">'
      '<span class="mark">'+LOGO+'</span>'
      '<span class="bt">'+FIRM['brand_line']+'<small>'+FIRM['brand_sub']+'</small></span></a>'
      '<button class="toggle" aria-label="Menu" aria-expanded="false">&#9776;</button>'
      '<nav>'+links+'<a href="'+rel(d,'contact.html')+'" class="ncta">'+FIRM['nav_cta']+'</a></nav></div></header>')

def phero(p, crumbs):
    d = p['depth']
    cr = '<div class="crumbs"><a href="'+rel(d,'index.html')+'">Home</a>'
    for label, href in crumbs[:-1]:
        cr += '<span>/</span><a href="'+rel(d,href)+'">'+html.escape(label)+'</a>'
    cr += '<span>/</span>'+html.escape(crumbs[-1][0])+'</div>' if crumbs else '</div>'
    return ('<div class="phero"><div class="wrap">'+cr+
      '<span class="eyebrow on-dark">'+html.escape(p.get('eyebrow',''))+'</span>'
      '<h1>'+p['h1']+'</h1>'+
      ('<p class="sub">'+p['sub']+'</p>' if p.get('sub') else '')+
      '</div></div>')

def cta(d, title='Start the conversation.', text=None):
    text = text or ('Call the office or send a note to '+FIRM['email']+' — tell us what you’re working through, and a partner will follow up directly. No obligation, and your inquiry stays confidential.')
    return ('<section class="cta" id="contact-cta"><div class="wrap"><span class="eyebrow on-dark" style="justify-content:center">Get in touch</span>'
      '<h2>'+html.escape(title)+'</h2><p>'+html.escape(text)+'</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:'+FIRM['tel']+'">Call '+FIRM['ph']+' '+ARROW+'</a>'
      '<a class="btn b-gh" href="mailto:'+FIRM['email']+'">Email the firm</a></div></div></section>')

def footer(d):
    def col(title, items):
        return ('<div><div class="fh">'+title+'</div><ul>'
                + ''.join('<li><a href="'+rel(d,h)+'">'+l+'</a></li>' for h, l in items)
                + '</ul></div>')
    loc = FIRM['city'] + ', ' + FIRM['state_full']
    return ('<footer class="foot"><div class="wrap"><div class="fgrid">'
      '<div><div class="fh">'+FIRM['name_html']+'</div><p style="max-width:36ch">'+FIRM['footer_blurb']+'</p>'
      + ('<p style="margin-top:12px;font-size:.85rem">'+FIRM['footer_note']+'</p>' if FIRM.get('footer_note') else '')
      + '</div>'
      + col('Services', FIRM['footer_services'])
      + col('Firm', FIRM['footer_firm'])
      + '<div><div class="fh">Office</div><ul>'
        '<li>'+(('<a href="'+rel(d,FIRM['office_page'])+'"><strong>'+FIRM['city']+'</strong></a><br>')
                 if FIRM.get('office_page') else '')+FIRM['addr']+'<br>'+FIRM['city']+', '+FIRM['state']+' '+FIRM['zip']+
        '<br><a href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a></li>'
        '<li style="margin-top:10px"><a href="mailto:'+FIRM['email']+'">'+FIRM['email']+'</a></li>'
        '<li>'+FIRM['hours']+'</li></ul></div>'
      '</div><div class="fbot"><span>&copy; <span id="yr"></span> '+FIRM['name_html']+' &middot; '+FIRM['brand_sub']+'</span>'
      '<span>'+loc+'</span></div></div></footer>')

def widget():
    return ('<div class="launch"><button class="lbtn" aria-expanded="false">'
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 8.7 8.7 0 0 1-3.9-.9L3 20l1.1-5.2a8.1 8.1 0 0 1-.9-3.7A8.4 8.4 0 0 1 11.7 3a8.4 8.4 0 0 1 9.3 8.5z"/></svg><span class="lbl">Let’s talk</span></button>'
      '<div class="lpanel"><div class="lhead">Reach '+FIRM['short']+'</div>'
      '<a class="lact" href="tel:'+FIRM['tel']+'"><span class="ic">'+icon('phone')+'</span><span>Call us<small>'+FIRM['ph']+'</small></span></a>'
      '<a class="lact" href="mailto:'+FIRM['email']+'"><span class="ic">'+icon('mail')+'</span><span>Email us<small>'+FIRM['email']+'</small></span></a>'
      '<a class="lact" href="#book"><span class="ic">'+icon('plan')+'</span><span>Book an appointment<small>Call or email to arrange one</small></span></a>'
      '<div class="lnote">'+FIRM['city']+', '+FIRM['state']+' &middot; '+FIRM['hours']+'</div></div></div>')

SCRIPT = ('<script>(function(){var t=document.querySelector(".toggle"),n=document.querySelector("nav");'
  'if(t)t.addEventListener("click",function(){var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o?"true":"false");});'
  'n&&n.querySelectorAll("a").forEach(function(a){a.addEventListener("click",function(){n.classList.remove("open");});});'
  'var hd=document.querySelector(".hdr");window.addEventListener("scroll",function(){hd.classList.toggle("small",window.scrollY>24);},{passive:true});'
  'var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{threshold:.12,rootMargin:"0px 0px -40px 0px"});'
  'document.querySelectorAll(".reveal").forEach(function(el,i){el.style.transitionDelay=((i%6)*0.05)+"s";io.observe(el);});'
  'var L=document.querySelector(".launch"),b=L.querySelector(".lbtn");'
  'b.addEventListener("click",function(e){e.stopPropagation();var o=L.classList.toggle("open");b.setAttribute("aria-expanded",o?"true":"false");});'
  'document.addEventListener("click",function(e){if(!L.contains(e.target))L.classList.remove("open");});'
  'var bk=L.querySelector(\'[href="#book"]\');if(bk)bk.addEventListener("click",function(e){e.preventDefault();L.querySelector(".lnote").textContent="Call or email and we\\u2019ll arrange a consultation.";});'
  'var y=document.getElementById("yr");if(y)y.textContent=new Date().getFullYear();})();</script>')

# ---------------- schema builders ----------------
ORG_ID = BASE + '#firm'
def org_schema():
    """AccountingService node. Everything that varies by firm comes from the profile;
    anything the firm does not publish is OMITTED rather than defaulted. Memberships,
    hours, founding date and geo were previously hardcoded to one firm and would have
    asserted false facts about every other build."""
    d = {"@context": "https://schema.org", "@type": "AccountingService", "@id": ORG_ID,
         "name": FIRM['name'], "legalName": FIRM['name'], "url": BASE,
         "email": FIRM['email'], "telephone": FIRM['ph'], "priceRange": "$$",
         "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                     "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                     "postalCode": FIRM['zip'], "addressCountry": "US"},
         "hasMap": FIRM['maps']}
    if FIRM.get('founded'):
        d['foundingDate'] = str(FIRM['founded'])
    if FIRM.get('opens') and FIRM.get('closes'):
        d['openingHoursSpecification'] = [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": FIRM['opens'], "closes": FIRM['closes']}]
    if FIRM.get('member_of'):
        d['memberOf'] = [{"@type": "Organization", "name": n} for n in FIRM['member_of']]
    if FIRM.get('area_served'):
        d['areaServed'] = [{"@type": "AdministrativeArea", "name": n} for n in FIRM['area_served']]
    if FIRM.get('geo'):
        d['geo'] = {"@type": "GeoCoordinates", "latitude": FIRM['geo'][0], "longitude": FIRM['geo'][1]}
    return d

def breadcrumb_schema(items):
    # items: [(name, absolute_url)]
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

def service_schema(name, desc, url):
    return {"@context":"https://schema.org","@type":"Service","name":name,"description":desc,
      "url":url,"serviceType":name,"provider":{"@id":ORG_ID},
      "areaServed":{"@type":"AdministrativeArea","name":"Chicagoland, Illinois"}}

def faq_schema(qas):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}

def person_schema(name, cred, role, url, extra=None):
    p = {"@context":"https://schema.org","@type":"Person","name":name,"jobTitle":role,
         "honorificSuffix":cred,"url":url,"worksFor":{"@id":ORG_ID}}
    if extra: p.update(extra)
    return p

def article_schema(title, desc, url):
    return {"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,
      "url":url,"author":{"@type":"Organization","name":FIRM['name']},"publisher":{"@id":ORG_ID}}

# ---------------- FAQ block helper ----------------
def faq_html(qas):
    out = '<div class="faq">'
    for q, a in qas:
        out += '<details><summary>'+html.escape(q)+'</summary><div class="fa">'+a+'</div></details>'
    return out+'</div>'

def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s).replace('  ',' ').strip()

# ---------------- render ----------------
def render(p):
    d = p['depth']
    doc = head(p)+demostrip()+header(p)+p['body']+cta(d, *p.get('cta_args', ()))+footer(d)+demostrip(bottom=True)+widget()+SCRIPT+'</body></html>'
    # Wide comparison tables cannot shrink below their content on narrow
    # viewports and would push the whole document sideways. Give every data
    # table its own scroll container so overflow stays inside the table.
    doc = re.sub(r'<table class="plain">', '<div class="tscroll"><table class="plain">', doc)
    doc = doc.replace('</table>', '</table></div>')
    fp = os.path.join(OUT, p['path'])
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp,'w',encoding='utf-8').write(doc)
    return p['path']

def main():
    os.makedirs(os.path.join(OUT,'css'), exist_ok=True)
    open(os.path.join(OUT,'css','site.css'),'w',encoding='utf-8').write(CSS)
    pages = _F.pages()
    seen = set()
    for p in pages:
        assert p['path'] not in seen, 'dup '+p['path']
        seen.add(p['path'])
        render(p)
    print('BUILT', len(pages), 'pages ->', OUT)

if __name__ == '__main__':
    main()
