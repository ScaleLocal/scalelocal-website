# -*- coding: utf-8 -*-
"""Industries hub + 4 industry pages."""
import html, re
from build import (FIRM, BASE, icon, ARROW, phero, faq_html,
                   org_schema, breadcrumb_schema, faq_schema, service_schema)

def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()

INDUSTRIES = [
 dict(slug='privately-held-businesses', ic='building', nav_title='Privately Held Businesses',
   short='The core of the practice since 1974 — owner-operated companies where the entity return, the owner return, and the exit plan are one problem.',
   title='CPA for Privately Held & Family Businesses | Illinois | KPW',
   desc='KPW specializes in privately owned businesses and their owners: integrated entity and owner tax planning, reporting, benefit plans, buy-sell agreements, and succession.',
   eyebrow='Privately held businesses', h1='Companies whose owners are still in the building.',
   sub='KPW specializes in the needs of privately owned businesses and their owners. It is the reason the firm exists and it is still most of what we do.',
   body='''
<h2>The short answer</h2>
<p>We have decades of experience with the specific financial and reporting requirements of privately owned businesses, and we handle the entity and the owner as a single engagement — because for a closely held company they are a single financial problem.</p>

<h2>What makes closely held companies different</h2>
<p>Public-company accounting exists to inform strangers. Closely held accounting exists to inform a handful of people who already know the business intimately and who are personally exposed to what it does. That changes what good work looks like.</p>
<ul>
<li><strong>The entity and the owner are one calculation.</strong> Reasonable compensation, distributions, basis, loans between owner and company, and personally guaranteed debt all cross the line between the two returns. Firms that see only one side optimize one side.</li>
<li><strong>The owner is the enterprise risk.</strong> Customer relationships, pricing judgment, and institutional knowledge frequently sit with one or two people. That concentration affects valuation, financing, insurance needs, and every succession conversation.</li>
<li><strong>Compensation is a policy decision, not a market outcome.</strong> Owner pay is set by owners, which makes it the single largest normalizing adjustment in almost every valuation and quality-of-earnings analysis.</li>
<li><strong>Records are built for the tax return.</strong> Which is why so many owners cannot answer basic questions from their own statements. Fixing the chart of accounts is usually a one-time project with permanent returns. See <a href="../services/accounting-compilation.html">accounting services</a>.</li>
</ul>

<h2>Where we spend our time</h2>
<h3>Year-round tax planning</h3>
<p>Balancing income between the corporation and its owners, Subchapter S planning, special planning for businesses that own their facilities, leasing decisions, and year-end liability forecasts issued while there is still time to act. See <a href="../services/tax-planning-preparation.html">tax planning and preparation</a>.</p>
<h3>Financial reporting at the right level</h3>
<p>Audit, review, or compilation depending on what a lender, bonding company, or agreement actually requires — plus internal, forecasted, projected, and pro forma statements. See <a href="../services/financial-statements.html">financial statements</a>.</p>
<h3>Financing and cash flow</h3>
<p>Cash flow projections, loan packaging, and capital formation — the documents a lender expects before a credit conversation becomes serious. See <a href="../services/business-advisory.html">business advisory</a>.</p>
<h3>Benefit plans and owner compensation</h3>
<p>Profit sharing, 401(k), pension, Section 125, and deferred compensation arrangements chosen against a stated objective. See <a href="../services/employee-benefit-plans.html">employee benefit plans</a>.</p>
<h3>Buy-sell agreements, valuation, and succession</h3>
<p>Buy-sell agreements are usually drafted at formation and rarely revisited, which means the pricing mechanism inside reflects a much smaller company. We model what it would produce today, and we start succession work years ahead, because that is when the efficient options are still available. See <a href="../services/business-valuation.html">business valuation</a>.</p>
<h3>Eventually, the exit</h3>
<p>Whether that is a sale, a transfer to family, or a management buyout, structure determines what the owner keeps. See <a href="../services/mergers-acquisitions.html">mergers and acquisitions</a>.</p>

<div class="callout"><p><strong>The firm counts more than two thousand clients</strong> — the large majority of them privately held companies and the families who own them.</p></div>

<h2>Transaction experience by industry</h2>
<p>The firm's <a href="../services/mergers-acquisitions.html">mergers and acquisitions</a> work records the widest industry range: entertainment, real estate, distribution and cartage, biotech and pharmaceuticals, food and beverage, software, media and publishing, iron and steel processing, consumer products, personal care and beauty, computer resellers, financial services, health care, construction, hospitality and leisure, and design and engineering.</p>
''',
   faqs=[("We are small. Are we too small for your firm?",
          "<p>Almost certainly not. The firm was built around owner-operated companies, and single-owner S corporations are ordinary clients here. The useful question is what you need done, not what you gross.</p>"),
         ("Can you handle the business and the owners' personal returns?",
          "<p>Yes, and we prefer to. Balancing income between the corporation and its owners only works when one firm prepares both.</p>"),
         ("Do we need audited statements?",
          "<p>Only if something requires them — a lender, a bonding company, a grant, or your own operating agreement. Read the actual language before you buy the audit. See our <a href=\"../guides/audit-review-compilation.html\">comparison guide</a>.</p>")]),

 dict(slug='government-nonprofit', ic='gov', nav_title='Government &amp; Non-Profit',
   short='Audits for governmental bodies and non-profit organizations, led by partners who have specialized in this reporting environment for decades.',
   title='Governmental & Non-Profit Audit Services | Illinois CPA Firm | KPW',
   desc='KPW audits governmental and non-profit organizations across Illinois. Peer-reviewed practice, risk-based planning, management letters, and board presentations.',
   eyebrow='Government & non-profit', h1='Audits for organizations that answer to a board and to the public.',
   sub='Two of our partners have specialized in governmental and non-profit audit work for decades. It is a distinct discipline, and it is a substantial part of this firm.',
   body='''
<h2>The short answer</h2>
<p>We provide audit services to governmental organizations and non-profits, with partners who have concentrated in this area for most of their careers. The firm's accounting and auditing practice is enrolled in the AICPA peer review program and independently reviewed every three years under the auspices of the Illinois CPA Society.</p>

<h2>Why this work is its own discipline</h2>
<p>A commercial audit answers to owners and lenders. A governmental or non-profit audit answers to a board, to funders, to taxing bodies, and ultimately to the public — none of whom accept "it balanced" as an answer.</p>
<p>The reporting model itself differs. Fund accounting, restrictions on the use of resources, grant compliance requirements that carry their own testing obligations, and governance structures where the people responsible for oversight are volunteers with day jobs. An auditor who does this occasionally will produce a defensible opinion and miss most of what the board needed to hear.</p>

<h2>What our engagements involve</h2>
<h3>Risk-based planning</h3>
<p>Planning begins with an assessment of the organization's general risks — comparison to similar entities, national and local economic conditions, and independent ratio analysis — which drives the audit plan rather than the other way around. Full detail on our <a href="../services/audit-assurance.html">audit approach</a>.</p>
<h3>Internal control in a small-staff environment</h3>
<p>Most non-profits and smaller governmental units cannot achieve textbook segregation of duties, and pretending otherwise helps nobody. The productive question is which compensating controls are realistic — board treasurer review of bank statements, dual authorization thresholds, independent reconciliation — and we make specific, sized recommendations.</p>
<h3>Restricted resources and grant compliance</h3>
<p>Tracking donor restrictions and grant terms correctly is where these organizations most often get into trouble, usually through drift rather than intent. Grant agreements frequently impose testing and reporting obligations beyond the financial statement audit.</p>
<h3>Communication with those charged with governance</h3>
<p>We stay in constant communication with management throughout fieldwork so nothing material is a surprise, and after the statements are finalized we are available to meet with the finance committee or the board of directors to review the audit. For volunteer boards, that meeting is often where the audit actually delivers its value.</p>
<h3>The management letter</h3>
<p>Written observations on controls, procedures, and conditions affecting the organization — the document a board can act on, as distinct from the opinion, which they mostly file.</p>

<div class="callout"><p><strong>Independent verification of our own work.</strong> Our reviewer examines whether our quality control policies are suitable and whether we comply with them, including evidence of continuing professional education and Illinois licensing compliance. <a href="../peer-review.html">More on peer review</a> — and ask any firm you are considering for their most recent report.</p></div>

<h2>Also relevant to non-profits</h2>
<p>Employee benefit plans reach an audit requirement based on participant count, which affects growing organizations. See <a href="../services/employee-benefit-plans.html">employee benefit plans</a>. Organizations facing a dispute or an investigation may also need <a href="../services/litigation-support.html">forensic support</a>.</p>
''',
   faqs=[("Do you audit Illinois governmental units?",
          "<p>Yes. Governmental audit work has been a partner specialization at this firm for decades, alongside non-profit engagements.</p>"),
         ("Will you present to our board or finance committee?",
          "<p>Yes. After the statements are finalized we make ourselves available to review the audit with the finance committee or the board.</p>"),
         ("Our organization is small and our staff wear several hats. Is that a finding?",
          "<p>Limited segregation of duties is common and frequently unavoidable at this size. What matters is whether realistic compensating controls exist. We recommend controls sized to your actual staffing rather than to an ideal organization chart.</p>"),
         ("How do we compare audit proposals?",
          "<p>Ask each firm for its most recent peer review report, ask who will actually be on site and how experienced they are in this reporting environment, and ask what the management letter will contain. Fee is the easiest variable to compare and the least informative.</p>")]),

 dict(slug='entertainment-sports', ic='mic', nav_title='Entertainment &amp; Sports',
   short='Business management for musicians, actors, and professional athletes — bank accounts, bill payment, reporting, multi-jurisdiction tax, and contract review.',
   title='CPA for Musicians, Actors & Professional Athletes | Chicago | KPW',
   desc='KPW acts as financial and tax agency for entertainment and sports clients: cash management, bill payment, monthly reporting, multi-state tax, and contract review.',
   eyebrow='Entertainment & sports', h1='Careers that earn a lifetime\'s income in a handful of years.',
   sub='KPW is a financial and tax agency for the entertainment industry, geared toward musicians, actors, and professional athletes.',
   body='''
<h2>The short answer</h2>
<p>We provide full business management to entertainment and sports clients: establishing bank accounts, processing monthly bills, monthly bookkeeping, compiled financial statements, income tax planning, preparation and representation, contract review and negotiation, asset sourcing and procurement including luxury real estate and automobiles, estate planning, and litigation support.</p>

<h2>Why the ordinary playbook fails</h2>
<p>Conventional financial planning assumes level income and a long career. Entertainment and athletic careers break both assumptions: income is lumpy, arrives late, comes from many payers in many jurisdictions, and stops far earlier than anyone plans for.</p>
<p>Three consequences follow, and they drive everything we do for these clients.</p>
<h3>The high-earning years fund everything after them</h3>
<p>A career that peaks in a five-year window has to fund the decades on either side. Spending calibrated to peak income is the failure mode this industry is famous for, and it is not usually caused by extravagance — it is caused by nobody producing a monthly statement that showed what was happening.</p>
<h3>Income is taxed where the work happens</h3>
<p>Athletes owe tax in states where they compete; touring performers face allocation across every jurisdiction they play. Multi-state and, for many clients, international filing is the normal case, along with credit calculations that prevent the same dollar being taxed twice. See <a href="../services/tax-planning-preparation.html">tax planning</a>.</p>
<h3>Money arrives after the work, through other people\'s hands</h3>
<p>Royalties, residuals, licensing, endorsements, and performance income flow through payers, agents, labels, and teams, often with deductions taken before anything reaches the client. Knowing what should have arrived — and when — requires someone tracking it independently.</p>

<h2>What we do about it</h2>
<ul>
<li>Someone independent tracking what should have arrived against what did</li>
<li>Spending made visible monthly, while it can still be adjusted</li>
<li>Filings and estimates handled in every jurisdiction the work touched</li>
<li>Financial terms of agreements reviewed before they are signed</li>
<li>Significant purchases structured and titled deliberately rather than quickly</li>
<li>An <a href="../services/estate-trust-planning.html">estate plan</a> that accounts for a compressed earning window, and <a href="../services/litigation-support.html">litigation support</a> if a dispute arises</li>
</ul>
<p>The full service description — accounts, bill processing, bookkeeping, reporting, tax, contract review, and asset procurement — is on the <a href="../services/entertainment-sports-management.html">business management page</a>.</p>

<div class="callout"><p><strong>This service exists because of the firm\'s breadth.</strong> No single discipline covers it — it draws on the accounting, tax, and finance practices at once. For the mechanics of how an engagement runs, see <a href="../services/entertainment-sports-management.html">business management</a>.</p></div>

<h2>More detail</h2>
<p>Full detail on how the service runs: <a href="../services/entertainment-sports-management.html">business management</a>.</p>
''',
   faqs=[("Do you work with clients based outside Illinois?",
          "<p>This practice is inherently multi-jurisdictional — the work travels regardless of where the client lives. What matters is that the filing obligations in every jurisdiction the income touches are handled.</p>"),
         ("Can you work alongside my agent and attorney?",
          "<p>Yes, and that is the normal arrangement. Our role is the financial and tax side; agents and attorneys handle representation and legal terms. Clear separation of roles is part of what keeps the arrangement safe.</p>"),
         ("What reporting will I actually receive?",
          "<p>Compiled financial statements on a monthly cycle, showing what came in, what went out, and what remains. You receive them as a matter of course rather than on request.</p>")]),

 dict(slug='real-estate-construction', ic='crane', nav_title='Real Estate &amp; Construction',
   short='Ownership entities, contractors, and developers — where entity structure, method of accounting, and bonding requirements decide the outcome.',
   title='CPA for Real Estate & Construction Companies | Illinois | KPW',
   desc='Tax, accounting, and advisory considerations for Illinois real estate owners and construction contractors — entity structure, facilities taxation, leasing, and reporting.',
   eyebrow='Real estate & construction', h1='Two industries where structure decides the outcome.',
   sub='Real estate ownership and construction contracting share a trait: the accounting decisions made at the start determine what the tax and financing look like for years afterward.',
   body='''
<h2>The short answer</h2>
<p>Real estate and construction are two of the sixteen industries in which the firm has handled transactions, and property-owning businesses are a long-standing part of the tax practice — special taxation planning for businesses that own their facilities, and lease-versus-buy analysis, are specific areas our planners work in. This page covers what we see in both industries and where our services apply.</p>

<h2>Real estate</h2>
<h3>Entity structure is the first and largest decision</h3>
<p>Whether property is held inside an operating company or in a separate ownership entity changes the tax result on operations, on refinancing, and eventually on sale. Special taxation planning for businesses that own their facilities is a specific part of our <a href="../services/tax-planning-preparation.html">tax practice</a>, and it is a decision that is expensive to reverse once made.</p>
<h3>Depreciation and the cost of getting it wrong slowly</h3>
<p>Placing property in service starts a depreciation schedule that runs for decades. Component classification, improvements versus repairs, and the treatment of tenant improvements each affect current deductions and eventual gain character. Cost segregation studies can accelerate deductions substantially on qualifying properties, and the analysis is worth running before assuming the answer.</p>
<h3>The exit</h3>
<p>Depreciation recapture, installment treatment, like-kind exchange requirements, and how the ownership entity is structured all determine what an owner keeps from a sale. These are planning decisions made years ahead, not filing decisions.</p>
<h3>Leasing</h3>
<p>Lease-versus-buy analysis sits at the intersection of tax, cash flow, and the balance sheet — and lender covenants frequently react to how leases are presented. It is one of the specific areas our tax planners work in.</p>

<h2>Construction</h2>
<h3>Method of accounting</h3>
<p>Long-term contract accounting drives both taxable income timing and what the financial statements show. The available methods, and the eligibility thresholds that govern them, materially affect a contractor's tax picture — and the method that minimizes tax is not always the method that presents best to a surety.</p>
<h3>Bonding and the surety relationship</h3>
<p>For contractors that bond work, the surety is effectively a second lender with its own reporting expectations, its own view of working capital and equity, and a limit that constrains how much work you can take. Statements prepared without regard to how a surety reads them can cost a contractor capacity — which costs revenue. Whatever level of service is required, it is worth preparing with that reader in mind. See <a href="../services/financial-statements.html">financial statements</a>.</p>
<h3>Job costing and the numbers behind the bid</h3>
<p>Contractors who cannot see accurate cost by job are bidding on averages. Getting the cost structure right — direct cost, allocated overhead, equipment cost, and work in process — is what turns bidding from optimism into arithmetic, and it is a chart-of-accounts problem before it is anything else. See <a href="../services/accounting-compilation.html">accounting services</a>.</p>
<h3>Cash flow and retainage</h3>
<p>Retainage, progress billing cycles, and the gap between paying labor weekly and collecting in sixty days make construction a working-capital business regardless of margin. Cash flow projections are not optional here. See <a href="../services/business-advisory.html">business advisory</a>.</p>

<div class="callout"><p><strong>Both industries are cyclical, and both are capital intensive.</strong> That combination is exactly why the financing relationship — lender, surety, or both — deserves as much attention as the tax return.</p></div>

<h2>Also relevant</h2>
<p>Owners in both industries typically hold significant value in a single illiquid asset class, which makes <a href="../services/estate-trust-planning.html">estate planning</a>, <a href="../services/asset-protection.html">asset protection</a>, and <a href="../services/business-valuation.html">valuation</a> more pressing than they are for the average business.</p>
''',
   faqs=[("Should the building be in the operating company?",
          "<p>Usually not, though the analysis depends on entity type, financing, and exit plans. Separating real estate from operations affects liability exposure, the tax result on refinancing and sale, and flexibility if the business is later sold without the property.</p>"),
         ("Do you prepare statements for a surety?",
          "<p>Yes. Sureties have specific expectations about level of service, presentation, and working capital. Statements prepared without that reader in mind can reduce bonding capacity.</p>"),
         ("Is a cost segregation study worth it?",
          "<p>It depends on the property, its cost basis, and how long you intend to hold it. It is worth evaluating rather than assuming — the analysis is straightforward and the acceleration can be substantial on qualifying properties.</p>")]),
]

def _ind_page(s):
    url = BASE + 'industries/' + s['slug'] + '.html'
    p = dict(path='industries/'+s['slug']+'.html', depth=1, nav='industries',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'])
    p['body'] = phero(p, [('Industries','industries/index.html'), (_plain(s['nav_title']), None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">'+s['body']+
      '<h2>Common questions</h2>'+faq_html(s['faqs'])+
      '</div>'
      '<div class="aside">'
      '<div class="acard"><div class="t">Talk to a partner</div>'
      '<p>Ten minutes on the phone is usually enough to work out what the engagement involves.</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a>'
      '</div>'
      '<div class="acard light"><div class="t">Other industries</div><ul>'
      + ''.join('<li><a href="'+o['slug']+'.html"><span class="ck">&rarr;</span> '+o['nav_title']+'</a></li>'
                for o in INDUSTRIES if o['slug'] != s['slug'])
      + '<li><a href="../services/index.html"><span class="ck">&rarr;</span> All services</a></li></ul></div></div>'
      '</div></div></section>')
    p['schema'] = [org_schema(),
      breadcrumb_schema([('Home',BASE),('Industries',BASE+'industries/'),(_plain(s['nav_title']),url)]),
      faq_schema([(q, _plain(a)) for q, a in s['faqs']])]
    return p

def pages():
    P = []
    cards = ''
    for i, s in enumerate(INDUSTRIES):
        cards += ('<a class="card reveal" href="'+s['slug']+'.html"><span class="num">'+('0'+str(i+1))[-2:]+'</span>'
                  '<div class="cic">'+icon(s['ic'])+'</div><h3>'+s['nav_title']+'</h3><p>'+s['short']+'</p>'
                  '<span class="more">Read more '+ARROW+'</span></a>')
    p = dict(path='industries/index.html', depth=1, nav='industries',
      title='Industries We Serve | KPW CPAs — Downers Grove, Illinois',
      desc='KPW serves privately held businesses, governmental and non-profit organizations, entertainment and sports clients, and real estate and construction companies across Illinois.',
      eyebrow='Industries', h1='Where fifty-two years of pattern recognition pays off.',
      sub='Both halves of this practice are deliberate: the private sector and the public sector, each with partners who have specialized in it for decades.')
    p['body'] = phero(p, [('Industries', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Who we work with</h2>'
      '<p class="lead">The firm has grown steadily since 1974 by providing audit, tax, and business advisory services to the private sector as well as to public sector organizations.</p></div>'
      '<div class="cards two">'+cards+'</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="prose reveal" style="max-width:820px">'
      '<h2>Transaction experience across industries</h2>'
      '<p>Our <a href="../services/mergers-acquisitions.html">mergers and acquisitions</a> work has covered a wider range still: entertainment, real estate, distribution and cartage, biotech and pharmaceuticals, food and beverage, software, media and publishing, iron and steel processing, consumer products, personal care and beauty, computer resellers (VAR), financial services, health care, construction, hospitality and leisure, and design and engineering. By the firm\'s own count, total transaction value across all industries exceeds one billion dollars.</p>'
      '<h2>What carries across all of them</h2>'
      '<p>Industry knowledge matters, but it is not what most clients are missing. What they are missing is a firm where the person who understands their situation is the same person who signs the work, and where nobody has to re-explain the business every year. That is a function of firm size and partner tenure rather than of industry specialization — and it is the part of this practice we protect most carefully.</p>'
      '<p><a class="btn b-ln" href="../services/index.html">See all twelve services '+ARROW+'</a></p>'
      '</div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Industries',BASE+'industries/')]),
      {"@context":"https://schema.org","@type":"ItemList","name":"Industries served","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":_plain(s['nav_title']),"url":BASE+'industries/'+s['slug']+'.html'}
        for i,s in enumerate(INDUSTRIES)]}]
    P.append(p)
    for s in INDUSTRIES:
        P.append(_ind_page(s))
    return P
