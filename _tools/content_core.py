# -*- coding: utf-8 -*-
"""Core pages: home, about, peer review, FAQ, contact, two location pages."""
import html
from build import (FIRM, BASE, T, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   org_schema, breadcrumb_schema, faq_schema, service_schema)

def _card(d, href, ic, title, text, num=None):
    return ('<a class="card reveal" href="'+rel(d,href)+'">'
            +('<span class="num">'+num+'</span>' if num else '')
            +'<div class="cic">'+icon(ic)+'</div><h3>'+title+'</h3><p>'+text+'</p>'
            '<span class="more">Read more '+ARROW+'</span></a>')

HOME_FAQS = [
 ("How do I know whether I need an audit, a review, or a compilation?",
  "<p>Usually someone else decides for you. A bank covenant, a bonding company, a grant agreement, a state agency, or your operating agreement will specify a level of service, and that requirement drives the engagement. An audit provides reasonable assurance and involves testing, confirmation with third parties, and an assessment of internal control. A review is substantially narrower — analytical procedures and inquiry, resulting in limited assurance. A compilation presents your figures in financial-statement format with no assurance attached.</p><p>If nobody is requiring anything, the honest answer is often that you need less than you think. We will tell you that.</p>"),
 ("What does working with KPW actually cost?",
  "<p>Fees depend on the engagement. Individual returns are priced by complexity; recurring business work is generally set annually so you can budget for it; audits are scoped once we understand your systems and reporting deadlines. Our stated position on pricing is simple: fair and transparent prices, with no hidden fees or extra charges. Call and describe the situation and we will talk about what the work involves.</p><p>Our <a href=\"guides/cpa-cost-small-business.html\">guide to what a CPA costs a small business</a> walks through what drives the number.</p>"),
 ("Do I work with a partner or get handed to staff I never meet?",
  "<p>A partner owns your relationship. KPW has six professionals, and the partners are the people who sign the work and sit in the meetings. That is a deliberate consequence of staying the size we are.</p>"),
 ("Can you handle both my business and my personal return?",
  "<p>Yes, and for closely held businesses that is the point. Balancing income between the corporation and its owners, timing distributions, planning around a Subchapter S election, and coordinating with your estate plan only work when the same firm sees both returns.</p>"),
 ("Are you taking new clients?",
  "<p>Yes. The most useful first step is a short call describing your situation — entity type, roughly what your year looks like, and what deadline you are working against. If we are not the right firm for the engagement, we will say so.</p>"),
]

def pages():
    P = []

    # ---------------------------------------------------------------- HOME
    svc_cards = ''.join([
      _card(0,'services/tax-planning-preparation.html','calc','Tax Planning &amp; Preparation',
            'Year-round planning for businesses and their owners, with year-end liability forecasts — not a conversation that starts in March.','01'),
      _card(0,'services/audit-assurance.html','shield','Audit &amp; Assurance',
            'Financial statement audits for governmental bodies, non-profits, and privately held companies, planned around risk and your reporting deadlines.','02'),
      _card(0,'services/accounting-compilation.html','ledger','Accounting Services',
            'Financial statement preparation, month-end close support, chart of accounts design, and the reporting discipline behind every other decision.','03'),
      _card(0,'services/business-advisory.html','chart','Business Advisory',
            'Cash flow projections, loan packaging, benefit plan design, internal controls, succession planning, and the operating questions in between.','04'),
      _card(0,'services/business-valuation.html','scale','Business Valuation',
            'Defensible valuations for sales, buy-sell agreements, gift and estate filings, and litigation — performed by a CPA Accredited in Business Valuation by the AICPA.','05'),
      _card(0,'services/litigation-support.html','gavel','Litigation Support',
            'Expert testimony and consulting for law firms: bankruptcy, financial and tax fraud, lost wages and profits, wrongful death, personal injury, and divorce.','06'),
    ])
    team_preview = ''.join([
      '<a class="tcard reveal" href="team/kenneth-j-kolnicki.html"><div class="tava">KK</div><h3>Kenneth J. Kolnicki</h3><div class="cred">CPA · Partner</div><p>Founding partner. Tax planning and the financial questions that come with owning a closely held business. With the firm since 1974.</p></a>',
      '<a class="tcard reveal" href="team/kenneth-w-peterson.html"><div class="tava">KP</div><h3>Kenneth W. Peterson</h3><div class="cred">CPA · Partner</div><p>Governmental and non-profit audits, litigation support and expert witness work, and financing for ongoing and start-up businesses. MBA, University of Chicago.</p></a>',
      '<a class="tcard reveal" href="team/glenn-byers.html"><div class="tava">GB</div><h3>Glenn Byers</h3><div class="cred">CPA, ABV · Partner</div><p>Business valuation — Accredited in Business Valuation by the AICPA — along with audit work and the firm\'s systems. With the firm since 1994.</p></a>',
    ])
    body = (
      '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" aria-hidden="true">'+GLYPH+'</svg>'
      '<div class="wrap"><div class="reveal in">'
      '<span class="eyebrow on-dark">Certified Public Accountants &middot; Downers Grove, Illinois</span>'
      '<h1>Fifty-two years of the same answer: tell the client the truth.</h1>'
      '<p class="sub">Kolnicki, Peterson &amp; Wirth has audited, advised, and filed for privately held businesses, their owners, and public-sector organizations across Illinois since 1974. Partner-led work, at fair and transparent prices.</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:'+FIRM['tel']+'">Call '+FIRM['ph']+'</a>'
      '<a class="btn b-gh" href="services/index.html">See what we do '+ARROW+'</a></div>'
      '<div class="hero-trust"><span><b>Established 1974</b></span><span><b>AICPA</b> peer-reviewed</span>'
      '<span><b>Downers Grove</b>, Illinois</span><span><b>Available</b> day and night</span></div>'
      '</div></div></section>'

      '<section class="strip"><div class="wrap reveal">'
      '<div class="cell"><div class="n">1974</div><div class="l">the year we opened</div></div>'
      '<div class="cell"><div class="n">2,000+</div><div class="l">clients</div></div>'
      '<div class="cell"><div class="n">Peer</div><div class="l">reviewed under AICPA standards</div></div>'
      '<div class="cell"><div class="n">6</div><div class="l">professionals, partner-led</div></div>'
      '</div></section>'

      '<section class="sec" id="services"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">What we do</span><h2>A full-service CPA firm, built around closely held businesses.</h2>'
      '<p class="lead">Most of our clients are companies whose owners are still in the building — and public-sector and non-profit organizations that answer to a board. Both need the same thing from an accountant: work that holds up, and a straight answer about what it means.</p>'
      '</div><div class="cards">'+svc_cards+'</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">All twelve services '+ARROW+'</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split">'
      '<div class="reveal"><span class="eyebrow">Why firms stay with us</span>'
      '<h2>Small enough that a partner knows your file. Old enough to have seen it before.</h2>'
      '<p class="lead">A firm founded in 1974 has filed through the 1986 Tax Reform Act, the S corporation boom, several recessions, the 2017 rewrite of the code, and everything that followed. That history matters less as trivia than as pattern recognition — knowing which problems resolve themselves and which ones become expensive if you wait.</p>'
      '<div class="prose" style="margin-top:26px">'
      '<h3>The partner who takes the call does the work</h3>'
      '<p>KPW is six professionals. There is no layer between you and the person signing the opinion. When your bank moves a covenant deadline or a buyer asks for three years of statements by Friday, you call a partner directly and get an answer the same day.</p>'
      '<h3>Fast, discreet, and reachable</h3>''<p>We guarantee fast and discreet handling of all your accounting needs, and our CPAs can be available day and night. In this profession discretion is not a courtesy, it is the work &mdash; and the deadline that matters is usually not ours.</p>''<h3>The price is the price</h3>'
      '<p>Fair and transparent prices, with no hidden fees or extra charges. That is the commitment, and clients notice when a firm does not keep it.</p>'
      '<h3>Quality that is checked by someone other than us</h3>'
      '<p>Our accounting and auditing practice is enrolled in the AICPA peer review program and undergoes an independent review every three years, conducted under the auspices of the Illinois CPA Society. An outside CPA examines whether our quality control policies are adequate and whether we actually follow them. <a href="peer-review.html">What that involves</a>.</p>'
      '</div></div>'
      '<div class="aside"><div class="acard"><div class="t">Talk to a partner</div>'
      '<p>Describe the situation in five minutes. If we are the right firm, we will tell you what the engagement looks like. If we are not, we will tell you that too.</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a></div>'
      '<div class="acard light"><div class="t">Credentials</div><ul>'
      '<li><a href="peer-review.html"><span class="ck">&#10003;</span> AICPA peer review program</a></li>'
      '<li><span class="ck">&#10003;</span> American Institute of CPAs</li>'
      '<li><span class="ck">&#10003;</span> Illinois CPA Society</li>'
      '<li><a href="team/glenn-byers.html"><span class="ck">&#10003;</span> AICPA Accredited in Business Valuation</a></li>'
      '<li><a href="team/michael-j-kolnicki.html"><span class="ck">&#10003;</span> CERTIFIED FINANCIAL PLANNER™ · IRS Enrolled Agent</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">The people</span><h2>Six professionals. The shortest tenure here is twenty-five years.</h2>'
      '<p class="lead">Every partner here has been with the firm for decades, and several have practiced in Illinois since the 1980s. You are not assigned an account manager — you are assigned a partner.</p>'
      '</div><div class="tgrid">'+team_preview+'</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="team/index.html">Meet the full team '+ARROW+'</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Where we are</span><h2>Downers Grove, and the western suburbs around it.</h2>'
      '<p class="lead">One office, in the DuPage County corridor the firm has worked out of since 1974 &mdash; close to the I-88 and I-355 interchanges, and to the owner-operated companies that make up most of our client base.</p></div>'
      '<div class="split">'
      '<div>'+gmap('1400 Opus Place, Suite 100 &middot; parking on site &middot; Monday to Friday, 9:00 AM to 5:00 PM.')+'</div>'
      '<div class="aside"><div class="acard"><div class="t">Downers Grove</div>'
      '<p>'+FIRM['addr']+'<br>Downers Grove, IL '+FIRM['zip']+'</p>'
      '<p>Telephone '+FIRM['ph']+'<br>Facsimile '+FIRM['fax']+'</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">Call '+FIRM['ph']+'</a></div>'
      '<div class="acard light"><div class="t">Getting here</div><ul>'
      '<li><a href="'+FIRM['maps']+'" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Open in Google Maps</a></li>'
      '<li><a href="locations/downers-grove.html"><span class="ck">&rarr;</span> Office details &amp; service area</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the firm</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Common questions</span><h2>Answers before you call.</h2></div>'
      +faq_html(HOME_FAQS)+
      '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">More questions answered '+ARROW+'</a></p></div></section>'
    )
    P.append(dict(path='index.html', depth=0, nav='home',
      title='Kolnicki, Peterson & Wirth, LLC | CPAs in Downers Grove, Illinois',
      desc='Certified Public Accountants in Downers Grove, Illinois since 1974. Tax planning, audit, valuation, advisory, and litigation support for businesses and their owners.',
      body=body,
      schema=[org_schema(),
              {"@context":"https://schema.org","@type":"WebSite","name":FIRM['name'],"url":BASE,"publisher":{"@id":BASE+'#firm'}},
              ]))

    # ---------------------------------------------------------------- ABOUT
    p = dict(path='about.html', depth=0, nav='about',
      title='About the Firm | Kolnicki, Peterson & Wirth, LLC — CPAs Since 1974',
      desc='Kolnicki, Peterson & Wirth has practiced public accounting in Illinois since 1974, serving privately held businesses, their owners, governmental bodies, and non-profits.',
      eyebrow='About the firm', h1='A CPA firm that has been answering the phone since 1974.',
      sub='Kolnicki, Peterson &amp; Wirth grew by doing careful work for people who came back, and by telling them things they did not always want to hear.')
    p['body'] = phero(p, [('About the firm', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>Kenneth J. Kolnicki opened the practice in 1974. He had earned his accounting degree from the University of Illinois at Chicago Circle in 1970, received his Illinois CPA certificate in 1971, and served as a manager at Wolf and Company from 1970 until founding the firm.</p>'
      '<p>Fifty-two years later the logic has not changed, and neither has the size. Six professionals. One Illinois office. A client base that runs from single-owner S corporations to governmental bodies and non-profits with board-level reporting obligations, and, per the firm\'s own count, more than two thousand clients.</p>'
      '<h2>What steady growth actually bought</h2>'
      '<p>The firm added partners the way it added clients — slowly, and by conviction. Richard D. Wirth joined in 1980 and built the income tax, estate planning, and management consulting side. Kenneth W. Peterson arrived in 1993 from Clifton, Gunderson &amp; Company with a University of Chicago MBA and brought the governmental and non-profit audit practice, plus the litigation support work that law firms still call for. Glenn Byers came in 1994 and earned the AICPA\'s Accredited in Business Valuation credential. Michael J. Kolnicki, also 1994, holds the CERTIFIED FINANCIAL PLANNER™ certification and an IRS Enrolled Agent designation. Michael J. Eckel joined in 2001 after fourteen years in public accounting, nine of them at Mulcahy, Pauritsch, Salvador and Company, adding audit depth and a management information systems MBA from DePaul.</p>'
      '<p>Every one of them is still here. The shortest partner tenure at KPW is a quarter century.</p>'
      '<h2>How we work</h2>'
      '<h3>Quality is the constraint, not the goal</h3>'
      '<p>Everything we do centers on providing services of the highest level of quality, and we do not stop until you are one hundred percent satisfied. That is a guarantee &mdash; and unlike most such promises, ours is checked by somebody outside the firm. We submit the claim to outside verification. Our accounting and auditing practice is enrolled in the AICPA peer review program, which requires an independent review by an outside CPA every three years, conducted under the auspices of the Illinois CPA Society. The reviewer examines whether our quality control policies are suitable and whether we comply with them — including evidence that our professionals meet continuing education requirements and that the firm meets Illinois licensing requirements.</p>'
      '<h3>Efficiency is respect for your money</h3>'
      '<p>Procedures get reviewed and improved because inefficient work is billed work. The point of a firm that has been doing this since 1974 is that we already know where the time goes.</p>'
      '<h3>Fair prices</h3>'
      '<p>Satisfying clients is the priority, which is why we believe in offering fair and transparent prices with no hidden fees or extra charges.</p>'
      '<h3>Proactive, not reactive</h3>'
      '<p>Tax planning that begins when the return is due is not planning. We forecast year-end liabilities while there is still time to do something about them, and we raise issues as they develop rather than explaining them afterward.</p>'
      '<h2>Who we serve</h2>'
      '<p>Both sides of the practice are deliberate. Privately held businesses and their owners get an integrated view — the entity return, the owner return, the benefit plan, the buy-sell agreement, and the estate plan are one problem. Governmental and non-profit organizations get audit partners who have specialized in that reporting environment for decades and understand what a finance committee and a board actually need to hear.</p>'
      '<div class="callout"><p><strong>Memberships.</strong> The firm and its professionals are members of the American Institute of Certified Public Accountants and the Illinois CPA Society. The AICPA sets auditing standards for private-company engagements, upholds the profession\'s code of conduct, administers peer review, and prepares and grades the Uniform CPA Examination.</p></div>'
      '<h2>Where to go next</h2>'
      '<p>The <a href="services/index.html">services section</a> details all twelve practice areas. The <a href="team/index.html">team pages</a> list each professional\'s education, credentials, and areas of special competence. The <a href="peer-review.html">peer review page</a> explains the quality program in full.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Firm at a glance</div>'
      '<p><strong style="color:#fff">Founded</strong><br>1974</p>'
      '<p><strong style="color:#fff">Office</strong><br>Downers Grove, Illinois</p>'
      '<p><strong style="color:#fff">Professionals</strong><br>Six, including five partners</p>'
      '<p><strong style="color:#fff">Memberships</strong><br>AICPA · Illinois CPA Society</p>'
      '<a class="btn b-acc" href="contact.html">Contact the firm</a></div>'
      '<div class="acard light"><div class="t">Firm pages</div><ul>'
      '<li><a href="team/index.html"><span class="ck">&rarr;</span> Our team</a></li>'
      '<li><a href="peer-review.html"><span class="ck">&rarr;</span> Peer review &amp; quality control</a></li>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> All services</a></li>'
      '<li><a href="industries/index.html"><span class="ck">&rarr;</span> Industries served</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('About the firm',BASE+'about.html')])]
    P.append(p)

    # ---------------------------------------------------------------- PEER REVIEW
    pr_faqs = [
      ("How often is a CPA firm peer reviewed?",
       "<p>Every three years for firms enrolled in the AICPA program that perform accounting and auditing work. The cycle is not optional for firms doing audit, review, or attest engagements, and lapsing has licensing consequences.</p>"),
      ("Who performs the review?",
       "<p>An independent licensed CPA from outside the firm, qualified under the program's requirements and with no interest in the firm. Our reviews are conducted under the auspices of the Illinois CPA Society following standards issued by the AICPA.</p>"),
      ("What does the reviewer actually examine?",
       "<p>Whether the firm has suitable quality control policies and procedures, and whether it complies with them. That includes evidence that the firm's auditors meet continuing professional education requirements and that the firm satisfies Illinois licensing requirements. Selected engagements are examined in detail against professional standards.</p>"),
      ("Why should a client care?",
       "<p>Because it is the only routine, independent check on whether a firm's work meets professional standards. A prospective client cannot audit their auditor. Peer review is the mechanism the profession built so that they do not have to.</p>"),
    ]
    p = dict(path='peer-review.html', depth=0, nav='about',
      title='Peer Review & Quality Control | Kolnicki, Peterson & Wirth, LLC',
      desc='KPW is enrolled in the AICPA peer review program: an independent CPA reviews our accounting and auditing practice every three years under Illinois CPA Society auspices.',
      eyebrow='Quality control', h1='Our work is checked by someone who does not work here.',
      sub='Every three years, an independent CPA examines whether our quality control policies are adequate and whether we actually follow them. We have completed that review successfully.')
    p['body'] = phero(p, [('Peer review & quality control', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>Any accounting firm can describe itself as careful. Peer review is how the profession tests the claim.</p>'
      '<p>Kolnicki, Peterson &amp; Wirth has successfully completed a rigorous quality review of its accounting and auditing practice. The reviewer concluded that the firm complies with the stringent quality control standards set by the American Institute of Certified Public Accountants, the national professional organization of CPAs.</p>'
      '<h2>What the program requires</h2>'
      '<p>KPW is enrolled in the AICPA peer review program, one of the AICPA-approved practice-monitoring programs. A firm enrolled in such a program must have an independent review of its accounting and auditing practice every three years. Our review was conducted under the auspices of the Illinois CPA Society, following standards issued by the AICPA.</p>'
      '<p>Peer reviews are performed by an independent licensed CPA who meets the program\'s qualification requirements and has no interest in the firm. They determine whether a public accounting firm has suitable quality control policies and procedures and is complying with them. Among the items examined is evidence that the firm\'s auditors meet the requirements for continuing professional education, and evidence that the firm meets all licensing requirements for the State of Illinois.</p>'
      '<div class="callout"><p><strong>The report is available.</strong> We provide a copy of the report on the results of our most recent review to clients and prospective clients on request. Ask for it — and ask any firm you are considering for theirs.</p></div>'
      '<h2>Why this is the trust signal that matters</h2>'
      '<p>Buyers of professional services usually look for proxies: how long has the firm existed, how many clients, who else uses them. Those are reasonable but indirect. Peer review is direct. It is an outside professional, bound by the same code of conduct, reading real engagement files and judging them against the standards that govern the work.</p>'
      '<p>It is also the reason a firm of six can credibly perform governmental and non-profit audits. Size is not what makes audit work defensible. Documented quality control, current professional education, and independent verification are.</p>'
      '<h2>About the AICPA</h2>'
      '<p>The AICPA is the national professional organization of CPAs in public practice, industry, government, and education. Its members are committed to the highest standards of quality, independence, and ethics. In its continuing efforts to serve the public interest, the organization sets auditing standards for private-company engagements, upholds the profession\'s code of conduct, provides continuing professional education, administers peer review and quality review programs, and prepares and grades the Uniform CPA Examination.</p>'
      '<p>KPW and its professionals are members of the AICPA and of the Illinois CPA Society.</p>'
      '<h2>Questions about peer review</h2>'
      +faq_html(pr_faqs)+
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Request the report</div>'
      '<p>We will send a copy of our most recent peer review report. Email the firm or call the office.</p>'
      '<a class="btn b-acc" href="mailto:'+FIRM['email']+'">'+FIRM['email']+'</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="services/audit-assurance.html"><span class="ck">&rarr;</span> Audit &amp; assurance</a></li>'
      '<li><a href="services/financial-statements.html"><span class="ck">&rarr;</span> Financial statements</a></li>'
      '<li><a href="guides/audit-review-compilation.html"><span class="ck">&rarr;</span> Audit vs. review vs. compilation</a></li>'
      '<li><a href="industries/government-nonprofit.html"><span class="ck">&rarr;</span> Government &amp; non-profit</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Peer review & quality control',BASE+'peer-review.html')]),
                   faq_schema([(q, html.unescape(__import__('re').sub(r'<[^>]+>','',a)).strip()) for q,a in pr_faqs])]
    P.append(p)

    # ---------------------------------------------------------------- FAQ
    FAQS = HOME_FAQS + [
     ("What is the difference between a CPA, an accountant, and an enrolled agent?",
      "<p>Anyone may call themselves an accountant. A Certified Public Accountant has passed the Uniform CPA Examination, met a state's education and experience requirements, and holds an active license — in our case, from the State of Illinois. Only a licensed CPA firm can issue an audit or review report on financial statements. An Enrolled Agent is federally licensed by the IRS and may represent taxpayers before the Service in examinations, collections, and appeals; the EA credential is tax-specific and does not carry attest authority.</p><p>KPW has both. Five CPAs licensed in Illinois, plus an Enrolled Agent who also holds the CERTIFIED FINANCIAL PLANNER™ certification.</p>"),
     ("When should a business owner start tax planning for the year?",
      "<p>Before the year ends, and ideally before the transaction. The decisions that move a tax bill — entity structure, timing of income and deductions, equipment purchases, owner compensation, retirement plan contributions, whether to make an S election — are all decided during the year. By the filing deadline you are recording history.</p><p>We forecast year-end liabilities during the year so there is time to reduce or defer them.</p>"),
     ("Do you work with S corporations?",
      "<p>Extensively. Subchapter S planning is one of the specific areas our tax work covers, including balancing income between the corporation and its owners, reasonable compensation, distributions and basis, and the interaction between the entity return and the shareholders' individual returns.</p>"),
     ("Can you help us get financing or package a loan?",
      "<p>Yes. Loan packaging, capital formation, and cash flow projections are part of our management advisory work, and one of our partners specifically assists clients in obtaining financing for ongoing and start-up businesses. Lenders want statements in a particular format with support behind the projections; we prepare them that way.</p>"),
     ("Do you provide expert witness testimony?",
      "<p>Yes. Law firms retain us for expert testimony and consulting on federal bankruptcy matters including debtor-in-possession representation, financial fraud, tax fraud and evasion, wrongful death, personal injury, and divorce. The work draws on the firm's valuation and audit capability. See <a href=\"services/litigation-support.html\">litigation support</a>.</p>"),
     ("What is a business valuation used for?",
      "<p>Most often: selling or buying a company, funding or updating a buy-sell agreement, gift and estate tax filings, divorce, shareholder disputes, and litigation. The purpose determines the standard of value and the level of report, which is why the first conversation is about why you need it rather than what it costs.</p>"),
     ("Do you handle estate planning?",
      "<p>We handle the accounting and tax side, and we coordinate with your attorney on the legal instruments. That covers minimizing the impact of estate taxes on survivors and structuring the transfer of a business interest to the next generation under the most favorable tax conditions.</p>"),
     ("Do you work with clients outside DuPage County?",
      "<p>Yes. The office is in Downers Grove and much of the client base is in the western suburbs, but we work with clients across the Chicago metropolitan area and, for multi-state matters, well beyond it. Most work does not require anyone to be in the same room.</p>"),
     ("What should I bring to a first meeting?",
      "<p>For a business: the last filed entity return, the most recent financial statements, and anything imposing a deadline on you — a loan agreement, a grant, a board resolution, a letter of intent. For an individual: last year's return and any documents describing what changed. If you do not have all of it, come anyway.</p>"),
     ("Are my documents kept confidential?",
      "<p>Yes. Client information is confidential, and both the AICPA Code of Professional Conduct and the Illinois rules governing our licenses make that an enforceable professional obligation rather than a policy.</p>"),
    ]
    p = dict(path='faq.html', depth=0, nav='about',
      title='Common Questions About Working With a CPA Firm | KPW Illinois',
      desc='Straight answers about CPA fees, audits versus reviews versus compilations, S corporation planning, business valuation, expert witness work, and how KPW engagements work.',
      eyebrow='Answers', h1='Questions we get asked, answered plainly.',
      sub='If your question is not here, call and ask a partner. Nobody will route you to a form.')
    p['body'] = phero(p, [('Common questions', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>About working with the firm</h2><p class="lead">Fees, engagement scope, and what to expect.</p></div>'
      +faq_html(FAQS)+
      '<div class="sec-head reveal" style="margin-top:56px"><h2>Still deciding?</h2>'
      '<p class="lead">Three longer pieces cover the questions that need more than a paragraph: '
      '<a href="guides/cpa-cost-small-business.html">what a CPA costs a small business</a>, '
      '<a href="guides/audit-review-compilation.html">audit versus review versus compilation</a>, and '
      '<a href="guides/choosing-a-cpa-firm.html">how to choose a CPA firm in Illinois</a>.</p></div>'
      '</div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Common questions',BASE+'faq.html')]),
                   faq_schema([(q, html.unescape(__import__('re').sub(r'<[^>]+>','',a)).strip()) for q,a in FAQS])]
    P.append(p)

    # ---------------------------------------------------------------- CONTACT
    p = dict(path='contact.html', depth=0, nav='contact',
      title='Contact KPW | CPAs in Downers Grove, Illinois',
      desc='Reach KPW in Downers Grove at (630) 390-1140. Office open Monday through Friday, 9:00 AM to 5:00 PM. Interactive map and directions.',
      eyebrow='Contact', h1='Call a partner. Not a queue.',
      sub='Tell us what you are working through and we will tell you whether we are the right people for it.')
    p['body'] = phero(p, [('Contact', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Downers Grove, Illinois</h2>'
      '<p class="lead">One office, one set of files, and a partner responsible for your engagement.</p></div>'
      '<div class="split">'
      '<div>'+gmap()+'</div>'
      '<div class="aside"><div class="acard"><div class="t">Office &amp; hours</div>'
      '<p>'+FIRM['addr']+'<br>Downers Grove, IL '+FIRM['zip']+'</p>'
      '<p>Telephone '+FIRM['ph']+'<br>Facsimile '+FIRM['fax']+'<br>'+FIRM['email']+'</p>'
      '<p>Monday&ndash;Friday, 9:00 AM&ndash;5:00 PM</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">Call '+FIRM['ph']+'</a></div>'
      '<div class="acard light"><div class="t">Quick links</div><ul>'
      '<li><a href="'+FIRM['maps']+'" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Directions in Google Maps</a></li>'
      '<li><a href="mailto:'+FIRM['email']+'"><span class="ck">&rarr;</span> '+FIRM['email']+'</a></li>'
      '<li><a href="locations/downers-grove.html"><span class="ck">&rarr;</span> Office &amp; service area</a></li>'
      '</ul></div></div></div></div></section>'
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>What to expect from a first call</h2>'
      '<p>You will speak with a professional, not a screener. The first conversation is usually ten minutes: what kind of entity, what the year looks like, and what deadline is driving the question. From that we can normally tell you whether the engagement is a tax matter, an attest matter, an advisory matter, or some combination — and roughly what it involves.</p>'
      '<p>If the work belongs somewhere else, we will say so and point you in a useful direction. We have been in this market since 1974 and would rather be the firm that gave you a straight answer than the firm that took an engagement it should not have.</p>'
      '<h2>What to have handy</h2>'
      '<ul><li>The most recently filed entity return, if you are calling about a business</li>'
      '<li>Your most recent financial statements, in whatever form they exist</li>'
      '<li>Anything with a date on it — a loan covenant, a grant agreement, a board resolution, a letter of intent, an IRS notice</li>'
      '<li>For individuals, last year\'s return and a short description of what changed</li></ul>'
      '<p>Missing pieces are not a problem. Bring what you have.</p>'
      '<h2>When you can reach us</h2>'
      '<p>The office keeps regular hours, Monday to Friday, 9:00 AM to 5:00 PM. Beyond that, our CPAs can be available day and night &mdash; because if something has gone wrong with a filing, a lender, or an examination, it rarely waits for business hours.</p>'
      '<h2>Confidentiality</h2>'
      '<p>Client information is confidential, including the fact that you called. That obligation runs through both the AICPA Code of Professional Conduct and the Illinois rules governing our licenses.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Prefer email?</div>'
      '<p>Write to the firm and a partner will respond.</p>'
      '<a class="btn b-acc" href="mailto:'+FIRM['email']+'">'+FIRM['email']+'</a>'
      '</div>'
      '<div class="acard light"><div class="t">Direct contacts</div><ul>'
      '<li><a href="team/kenneth-w-peterson.html"><span class="ck">&rarr;</span> Kenneth W. Peterson, CPA — audits, litigation support</a></li>'
      '<li><a href="team/michael-j-eckel.html"><span class="ck">&rarr;</span> Michael J. Eckel, CPA — audits, litigation support</a></li>'
      '<li><a href="team/index.html"><span class="ck">&rarr;</span> Full team directory</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Contact',BASE+'contact.html')]),
      {"@context":"https://schema.org","@type":"ContactPage","name":"Contact Kolnicki, Peterson & Wirth, LLC","url":BASE+'contact.html'}]
    P.append(p)

    # ---------------------------------------------------------------- LOCATIONS
    loc_common_aside = ('<div class="acard light"><div class="t">Also useful</div><ul>'
      '<li><a href="../locations/downers-grove.html"><span class="ck">&rarr;</span> Downers Grove</a></li>'
      '<li><a href="../contact.html"><span class="ck">&rarr;</span> Contact page</a></li>'
      '<li><a href="../services/index.html"><span class="ck">&rarr;</span> All services</a></li></ul></div>')

    p = dict(path='locations/downers-grove.html', depth=1, nav='locations',
      title='CPA in Downers Grove, IL | Kolnicki, Peterson & Wirth, LLC',
      desc='KPW\'s Downers Grove office at 1400 Opus Place serves DuPage County businesses and families. Tax, audit, valuation, and advisory. Call (630) 390-1140.',
      eyebrow='Downers Grove, Illinois', h1='Downers Grove — where the firm has practiced since 1974.',
      sub='1400 Opus Place, Suite 100 — off Butterfield Road at the I-88 corridor, serving DuPage County and the western suburbs.')
    p['body'] = phero(p, [('Locations','locations/downers-grove.html'), ('Downers Grove', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Where we are</h2>'
      '<p><strong>'+FIRM['addr']+', Downers Grove, IL '+FIRM['zip']+'</strong><br>'
      'Telephone <a href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a> &middot; facsimile '+FIRM['fax']+'<br>'
      '<a href="mailto:'+FIRM['email']+'">'+FIRM['email']+'</a><br>Monday&ndash;Friday, 9:00 AM&ndash;5:00 PM</p>'
      '<p>Opus Place sits in the Executive Towers West complex just off Butterfield Road, near the I-88 and I-355 corridors.</p>'
      '<h2>Who this office serves</h2>'
      '<p>DuPage County and the western suburbs are full of owner-operated companies — manufacturers and distributors along the I-88 corridor, professional practices, contractors, and family businesses. That is the client base this office centers on.</p>'
      '<p>We also serve governmental bodies and non-profit organizations throughout the western suburbs, where the audit is not just a compliance exercise but the document a board, a funder, or a taxing body relies on.</p>'
      '<p>The office is convenient to Lisle, Naperville, Woodridge, Westmont, Hinsdale, Oak Brook, Lombard, Glen Ellyn, Wheaton, Darien, Burr Ridge, and Elmhurst — though geography matters less than it used to, and we work with clients across the Chicago metropolitan area.</p>'
      '<h2>What you can handle here</h2>'
      '<ul><li><a href="../services/tax-planning-preparation.html">Tax planning and preparation</a> for businesses, owners, individuals, and fiduciaries</li>'
      '<li><a href="../services/audit-assurance.html">Financial statement audits</a>, reviews, and compilations</li>'
      '<li><a href="../services/business-advisory.html">Management advisory work</a> — cash flow projections, loan packaging, internal controls, benefit plan design, succession planning</li>'
      '<li><a href="../services/business-valuation.html">Business valuations</a> for sales, buy-sell agreements, gift and estate filings, and disputes</li>'
      '<li><a href="../services/estate-trust-planning.html">Estate and trust planning</a> coordinated with your attorney</li></ul>'
      '<h2>Getting here</h2>'
      '<p>Opus Place is reached from the Butterfield Road corridor, close to both the I-88 and I-355 interchanges, with BNSF Metra service into Downers Grove nearby.</p>'
      +gmap('Pan, zoom or open the map full screen for turn-by-turn directions.')+
      '<p><a class="btn b-ln" href="'+FIRM['maps']+'" target="_blank" rel="noopener">Open in Google Maps '+ARROW+'</a></p>'
      '</div><div class="aside"><div class="acard"><div class="t">Downers Grove office</div>'
      '<p>'+FIRM['addr']+'<br>Downers Grove, IL '+FIRM['zip']+'<br>Mon&ndash;Fri 9:00&ndash;5:00</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a></div>'
      +loc_common_aside+'</div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Locations',BASE+'locations/downers-grove.html'),('Downers Grove',BASE+'locations/downers-grove.html')]),
      {"@context":"https://schema.org","@type":"AccountingService","name":FIRM['name']+" — Downers Grove","parentOrganization":{"@id":BASE+'#firm'},
       "url":BASE+'locations/downers-grove.html',"telephone":FIRM['ph'],"email":FIRM['email'],
       "address":{"@type":"PostalAddress","streetAddress":FIRM['addr'],"addressLocality":"Downers Grove","addressRegion":"IL","postalCode":FIRM['zip'],"addressCountry":"US"},
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"}]}]
    P.append(p)

    return P
