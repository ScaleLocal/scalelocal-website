# -*- coding: utf-8 -*-
"""Team hub + 6 professional bio pages. Every fact is sourced from the firm's own sites."""
import html, re
from build import (FIRM, BASE, icon, ARROW, phero, faq_html,
                   org_schema, breadcrumb_schema, person_schema)

def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()

TEAM = [
 dict(slug='kenneth-j-kolnicki', alumni=['University of Illinois at Chicago Circle'], initials='KK', name='Kenneth J. Kolnicki', cred='CPA', role='Partner',
   since='1974', email=None,
   card='Founding partner. Tax planning and the financial questions that come with owning a closely held business.',
   title='Kenneth J. Kolnicki, CPA | Founding Partner | Kolnicki, Peterson & Wirth',
   desc='Kenneth J. Kolnicki, CPA founded Kolnicki, Peterson & Wirth in 1974. He provides expertise to individually owned businesses and leads tax planning engagements.',
   h1='Kenneth J. Kolnicki, CPA',
   sub='Partner &middot; with the firm since 1974',
   education=['Bachelor of Science in Accounting, University of Illinois at Chicago Circle, 1970',
              'CPA Certificate, State of Illinois, 1971',
              'Member — American Institute of Certified Public Accountants and Illinois CPA Society'],
   history=['Kolnicki, Peterson &amp; Wirth, LLC — 1974 to present',
            'Wolf and Company — Manager, 1970 to 1974'],
   competence=['Provide expertise to individually owned businesses.',
               'Tax planning.'],
   body='''
<h2>Practice</h2>
<p>Kenneth Kolnicki founded this firm in 1974. He had earned his accounting degree from the University of Illinois at Chicago Circle in 1970, received his Illinois CPA certificate in 1971, and served as a manager at Wolf and Company from 1970 until the firm opened.</p>
<p>His stated areas of competence have been constant since: providing expertise to individually owned businesses, and tax planning. For an owner-operated company those are two halves of one job — the tax question and the business question are rarely separable.</p>
<h2>What that means for a client</h2>
<p>The questions that reach a partner of this kind are the ones decided before a return exists: whether the building belongs inside the operating company, how to compensate family members working in the business, what an offer to purchase would actually leave after tax, whether an S election still fits where the company has ended up. The value of a practice this long is knowing which of those has a settled answer and which genuinely depends on the facts.</p>
'''),

 dict(slug='kenneth-w-peterson', alumni=['Loyola University', 'University of Chicago'], initials='KP', name='Kenneth W. Peterson', cred='CPA', role='Partner',
   since='1993', email='kpeterson@kpwcpa.com',
   card='Governmental and non-profit audits, litigation support and expert witness work, and financing for ongoing and start-up businesses.',
   title='Kenneth W. Peterson, CPA | Partner | Kolnicki, Peterson & Wirth',
   desc='Kenneth W. Peterson, CPA leads governmental and non-profit audit engagements and litigation support at KPW, including expert witness testimony and valuation.',
   h1='Kenneth W. Peterson, CPA',
   sub='Partner &middot; with the firm since 1993',
   education=['Bachelor of Science in Accounting, Loyola University, 1984',
              'CPA Certificate, State of Illinois, 1984',
              'Master of Business Administration with concentration in Finance and Strategic Planning, University of Chicago, 1988',
              'Member — American Institute of Certified Public Accountants and Illinois CPA Society'],
   history=['Kolnicki, Peterson &amp; Wirth, LLC — 1993 to present',
            'Clifton, Gunderson &amp; Company — 1986 to 1993',
            'Hilisman, Lynch &amp; Company — 1984 to 1986 (merged with above firm)',
            'Board Member, Bank of Commerce, Downers Grove — 1996 to present'],
   competence=['Provide audit services to many governmental and non-profit organizations.',
               'Provide litigation support services to law firms, including expert witness, valuation and calculation of lost wages and profits.',
               'Provide tax planning for individuals and their closely held businesses.',
               'Provide assistance in obtaining financing for ongoing and start-up businesses.'],
   body='''
<h2>Practice</h2>
<p>Kenneth Peterson joined KPW in 1993 from Clifton, Gunderson &amp; Company, bringing a University of Chicago MBA in finance and strategic planning and nine years of public accounting behind him. He carries three distinct lines of work, and they reinforce one another more than the list suggests.</p>
<h3>Governmental and non-profit audits</h3>
<p>He audits governmental bodies and non-profit organizations — a reporting environment with its own model, its own funder requirements, and an audience of board members and finance committees who need to understand the statements well enough to govern by them. See <a href="../industries/government-nonprofit.html">government and non-profit</a>.</p>
<h3>Litigation support and expert testimony</h3>
<p>Law firms retain him for expert witness work, valuation, and the calculation of lost wages and profits. Damages analysis is unforgiving: every assumption behind an earnings base, a growth rate, or a discount rate will be tested by an opposing expert, and the analysis has to be built to be defended rather than merely to be produced. See <a href="../services/litigation-support.html">litigation support</a>.</p>
<h3>Tax planning and financing</h3>
<p>He plans for individuals and their closely held businesses, and assists clients in obtaining financing for both ongoing and start-up companies — work that draws directly on his finance training and on three decades on the board of a Downers Grove bank. Knowing how a credit decision is actually made on the other side of the table changes how a loan package gets built. See <a href="../services/business-advisory.html">business advisory</a>.</p>
'''),

 dict(slug='richard-d-wirth', alumni=['University of Illinois at Chicago Circle'], initials='RW', name='Richard D. Wirth', cred='CPA', role='Partner',
   since='1980', email=None,
   card='Income tax planning, estate planning, and management consulting for privately owned businesses. With the firm since 1980.',
   title='Richard D. Wirth, CPA | Partner | Kolnicki, Peterson & Wirth',
   desc='Richard D. Wirth, CPA has practiced at KPW since 1980, focusing on income tax planning, estate planning, and management consulting for privately owned businesses.',
   h1='Richard D. Wirth, CPA',
   sub='Partner &middot; with the firm since 1980',
   education=['Bachelor of Science in Accounting, University of Illinois at Chicago Circle, 1980',
              'CPA Certificate, State of Illinois, 1982',
              'Member — American Institute of Certified Public Accountants and Illinois CPA Society'],
   history=['Kolnicki, Peterson &amp; Wirth, LLC — 1980 to present'],
   competence=['Income tax planning.',
               'Estate planning.',
               'Management consulting for privately owned businesses.'],
   body='''
<h2>Practice</h2>
<p>Richard Wirth has been with this firm his entire career — joining in 1980, the year he finished his accounting degree at the University of Illinois at Chicago Circle, and receiving his Illinois CPA certificate two years later. Forty-six years at one firm is the kind of tenure that lets an accountant see a closely held business through a full cycle: formation, growth, financing, and eventually transfer.</p>
<h2>Where the three practice areas meet</h2>
<p>Income tax planning, estate planning, and management consulting sound like three services. For an owner-operated business they are one continuous conversation, and the connections are where the planning either works or fails.</p>
<p>How the company is structured determines the annual tax result and also what a transfer to the next generation will cost. How the owner is compensated affects the current return and also the value of the interest that eventually passes. Whether the buy-sell agreement contains a workable valuation mechanism determines what happens when the plan actually gets used. These decisions are made years apart and only produce the intended outcome if someone has been holding all of them in view.</p>
<p>Related: <a href="../services/tax-planning-preparation.html">tax planning and preparation</a>, <a href="../services/estate-trust-planning.html">estate and trust planning</a>, and <a href="../services/business-advisory.html">business advisory</a>.</p>
'''),

 dict(slug='michael-j-eckel', alumni=['Elmhurst College', 'DePaul University'], initials='ME', name='Michael J. Eckel', cred='CPA', role='Partner',
   since='2001', email='meckel@kpwcpa.com',
   card='Audit services for governmental and non-profit organizations, litigation support, and tax planning for closely held businesses.',
   title='Michael J. Eckel, CPA | Partner | Kolnicki, Peterson & Wirth',
   desc='Michael J. Eckel, CPA joined KPW in 2001, providing audits for governmental and non-profit organizations, litigation support, and tax planning for closely held businesses.',
   h1='Michael J. Eckel, CPA',
   sub='Partner &middot; with the firm since 2001',
   education=['Bachelor of Science in Accounting, Elmhurst College, 1983',
              'CPA Certificate, State of Illinois, 1984',
              'Master of Business Administration with concentration in Management Information Systems, DePaul University, 1986',
              'Member — American Institute of Certified Public Accountants and Illinois CPA Society'],
   history=['Kolnicki, Peterson &amp; Wirth, LLC — 2001 to present',
            'Klayman and Korman LLC — 2001',
            'Mulcahy, Pauritsch, Salvador and Company — 1992 to 2001',
            'Berg, DeMarco, Lewis, Sawatski and Company — 1987 to 1992'],
   competence=['Provide audit services to many governmental and non-profit organizations.',
               'Provide litigation support services to law firms, including valuation and calculation of lost wages services.',
               'Provide tax planning for individuals and their closely held businesses.'],
   body='''
<h2>Practice</h2>
<p>Michael Eckel joined KPW in 2001 after fourteen years in public accounting, nine of them at Mulcahy, Pauritsch, Salvador and Company. He audits governmental and non-profit organizations, provides litigation support to law firms including valuation and lost wages calculations, and plans for individuals and their closely held businesses.</p>
<h2>The systems background</h2>
<p>His MBA is in management information systems, which is an unusual pairing with an audit practice and a useful one. Modern audit work is substantially an exercise in understanding how a client's systems produce the numbers — where data originates, what controls sit around it, which reports are generated and which are assembled by hand, and where a well-intentioned workaround has quietly become the process.</p>
<p>Auditing standards require an understanding of internal control sufficient to assess risk. Understanding the system, and not merely its output, is what makes that assessment real rather than documentary. See <a href="../services/audit-assurance.html">audit and assurance</a>.</p>
<h2>Litigation support</h2>
<p>He works with law firms on valuation and the calculation of lost wages — engagements where the analysis has to survive an opposing expert and a cross-examination. See <a href="../services/litigation-support.html">litigation support</a>.</p>
'''),

 dict(slug='glenn-byers', alumni=['Elmhurst College'], initials='GB', name='Glenn Byers', cred='CPA, ABV', role='Partner',
   since='1994', email=None,
   card='Business valuation — Accredited in Business Valuation by the AICPA — along with audit work and the firm\'s systems.',
   title='Glenn Byers, CPA, ABV | Partner | Kolnicki, Peterson & Wirth',
   desc='Glenn Byers, CPA holds the AICPA Accredited in Business Valuation (ABV) credential and leads business valuation engagements at KPW, alongside audit services.',
   h1='Glenn Byers, CPA, ABV',
   sub='Partner &middot; with the firm since 1994',
   education=['Bachelor of Science in Accounting, Elmhurst College',
              'CPA Certificate, State of Illinois, 1984',
              'Accredited in Business Valuation (ABV), American Institute of Certified Public Accountants',
              'Member — American Institute of Certified Public Accountants and Illinois CPA Society'],
   history=['Kolnicki, Peterson &amp; Wirth, LLC — 1994 to present'],
   competence=['Business valuation services.',
               'Audit services.',
               'Systems administration for the firm.'],
   body='''
<h2>Practice</h2>
<p>Glenn Byers holds the AICPA's Accredited in Business Valuation credential and leads the firm's valuation engagements. The ABV is granted to CPAs who meet the AICPA's experience and examination requirements in business valuation — a specific, tested competence rather than a general accounting qualification, and the credential that makes a valuation defensible when it is examined.</p>
<h2>Why valuation belongs inside a CPA firm</h2>
<p>A valuation is only as sound as the financial information underneath it, and closely held financial statements require substantial normalization before they mean anything to a valuation analyst. Owner compensation set by policy rather than by market, discretionary expenses, non-operating assets, related-party arrangements, and non-recurring items all have to be identified and adjusted.</p>
<p>An analyst who also audits closely held companies knows where those adjustments hide, because those are the same accounts that draw the most audit attention. The valuation work and the audit work reinforce each other, which is why he does both.</p>
<h2>What the valuations are used for</h2>
<p>Sales and acquisitions, buy-sell agreements, gift and estate tax filings, divorce, shareholder disputes, and litigation — each invoking a standard of value determined by its purpose. See <a href="../services/business-valuation.html">business valuation</a>, <a href="../services/mergers-acquisitions.html">mergers and acquisitions</a>, and <a href="../services/litigation-support.html">litigation support</a>.</p>
'''),

 dict(slug='michael-j-kolnicki', alumni=['Northern Illinois University'], initials='MK', name='Michael J. Kolnicki', cred='EA, CFP&reg;', role='Tax and Management Advisory',
   since='1994', email=None,
   card='Tax planning and management advisory services. CERTIFIED FINANCIAL PLANNER™ certificant and IRS Enrolled Agent.',
   title='Michael J. Kolnicki, EA, CFP® | Kolnicki, Peterson & Wirth',
   desc='Michael J. Kolnicki holds the CERTIFIED FINANCIAL PLANNER™ certification and IRS Enrolled Agent designation, providing tax planning and advisory at KPW since 1994.',
   h1='Michael J. Kolnicki, EA, CFP&reg;',
   sub='Tax and management advisory &middot; with the firm since 1994',
   education=['Northern Illinois University, 1994',
              'CERTIFIED FINANCIAL PLANNER™ certification, 1999',
              'IRS Enrolled Agent, 2017'],
   history=['Kolnicki, Peterson &amp; Wirth, LLC — 1994 to present'],
   competence=['Tax planning.',
               'Management advisory services.'],
   body='''
<h2>Practice</h2>
<p>Michael Kolnicki has been with the firm since 1994 and holds two credentials that sit on either side of the same problem. The CERTIFIED FINANCIAL PLANNER™ certification, earned in 1999, covers the planning discipline — how the pieces of a household's or an owner's finances fit together. The IRS Enrolled Agent designation, earned in 2017, is a federal license to represent taxpayers before the Internal Revenue Service in examinations, collections, and appeals.</p>
<h2>Why the combination matters</h2>
<p>Planning that ignores tax produces recommendations that do not survive implementation. Tax work that ignores planning optimizes a single year at the expense of the decade around it. Business owners in particular need both at once, because for them retirement funding, benefit plan design, entity structure, and eventual succession are all the same conversation viewed from different angles.</p>
<p>The Enrolled Agent designation also means that when a client receives a notice, the same person who did the planning can handle the representation — no handoff, no re-explanation of the facts.</p>
<h2>Where the work shows up</h2>
<p><a href="../services/tax-planning-preparation.html">Tax planning and preparation</a>, <a href="../services/business-advisory.html">management advisory services</a>, and <a href="../services/employee-benefit-plans.html">employee benefit plans</a>.</p>
'''),
]

def _bio(t):
    url = BASE + 'team/' + t['slug'] + '.html'
    ed = ''.join('<li>'+x+'</li>' for x in t['education'])
    hi = ''.join('<li>'+x+'</li>' for x in t['history'])
    co = ''.join('<li>'+x+'</li>' for x in t['competence'])
    p = dict(path='team/'+t['slug']+'.html', depth=1, nav='team',
             title=t['title'], desc=t['desc'], eyebrow=t['role'], h1=t['h1'], sub=t['sub'])
    others = ''.join('<li><a href="'+o['slug']+'.html"><span class="ck">&rarr;</span> '+o['name']+', '+o['cred']+'</a></li>'
                     for o in TEAM if o['slug'] != t['slug'])
    p['body'] = phero(p, [('Our team','team/index.html'), (t['name'], None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">'+t['body']+
      '<h2>Education and credentials</h2><ul>'+ed+'</ul>'
      '<h2>Professional history</h2><ul>'+hi+'</ul>'
      '<h2>Areas of special competence</h2><ul>'+co+'</ul>'
      +('<div class="callout"><p><strong>Contact.</strong> <a href="mailto:'+t['email']+'">'+t['email']+'</a> &middot; <a href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a></p></div>'
        if t['email'] else
        '<div class="callout"><p><strong>Contact.</strong> <a href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a> &middot; <a href="mailto:'+FIRM['email']+'">'+FIRM['email']+'</a></p></div>')
      + '</div>'
      '<div class="aside"><div class="acard"><div class="t">'+t['name']+'</div>'
      '<p>'+t['cred']+' &middot; '+t['role']+'<br>With the firm since '+t['since']+'</p>'
      + ('<a class="btn b-acc" href="mailto:'+t['email']+'">Email</a>' if t['email'] else '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a>')
      + '</div>'
      '<div class="acard light"><div class="t">The rest of the team</div><ul>'+others+'</ul></div></div>'
      '</div></div></section>')
    p['schema'] = [org_schema(),
      breadcrumb_schema([('Home',BASE),('Our team',BASE+'team/'),(t['name'],url)]),
      person_schema(t['name'], _plain(t['cred']), t['role'], url,
        {"description": _plain(t['card']),
         "alumniOf": [{"@type":"EducationalOrganization","name":n} for n in t.get('alumni', [])],
         **({"email": t['email']} if t['email'] else {})})]
    return p

def pages():
    P = []
    cards = ''
    for t in TEAM:
        cards += ('<a class="tcard reveal" href="'+t['slug']+'.html"><div class="tava">'+t['initials']+'</div>'
                  '<h3>'+t['name']+'</h3><div class="cred">'+t['cred']+' &middot; '+t['role']+'</div>'
                  '<p>'+t['card']+'</p></a>')
    p = dict(path='team/index.html', depth=1, nav='team',
      title='Our Team | Partners & Professionals | Kolnicki, Peterson & Wirth, LLC',
      desc='Meet the six professionals of Kolnicki, Peterson & Wirth — their education, credentials, professional history, and areas of special competence.',
      eyebrow='The people', h1='Six professionals. The shortest tenure here is twenty-five years.',
      sub='Every partner listed below joined this firm and stayed. In a profession where people move constantly, that is the most useful thing we can tell you about how the work gets done.')
    p['body'] = phero(p, [('Our team', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Partners and professionals</h2>'
      '<p class="lead">Education, credentials, professional history, and areas of special competence for each.</p></div>'
      '<div class="tgrid">'+cards+'</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="prose reveal" style="max-width:820px">'
      '<h2>Why a firm this size works</h2>'
      '<p>A six-person firm cannot be all things to everyone, and we do not try. What it can do is guarantee something larger firms structurally cannot: the partner who quotes your work is the partner who does it and signs it.</p>'
      '<p>There is no account manager layer here, no rotating team assignment, and no annual re-education of a new junior on how your business works. When a client calls, they reach someone who already knows the file.</p>'
      '<h2>Credentials in the firm</h2>'
      '<ul>'
      '<li>Five Certified Public Accountants licensed in the State of Illinois</li>'
      '<li>One <a href="glenn-byers.html">Accredited in Business Valuation (ABV)</a> credential from the AICPA</li>'
      '<li>One <a href="michael-j-kolnicki.html">CERTIFIED FINANCIAL PLANNER™ certificant and IRS Enrolled Agent</a></li>'
      '<li>Two MBAs — University of Chicago (finance and strategic planning) and DePaul University (management information systems)</li>'
      '<li>Firm and professional membership in the American Institute of Certified Public Accountants and the Illinois CPA Society</li>'
      '<li>An accounting and auditing practice enrolled in the <a href="../peer-review.html">AICPA peer review program</a></li>'
      '</ul>'
      '<p>Continuing professional education is not optional for any of them — evidence that the firm\'s auditors meet those requirements is one of the items examined during peer review.</p>'
      '<p><a class="btn b-ln" href="../about.html">More about the firm '+ARROW+'</a></p>'
      '</div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Our team',BASE+'team/')]),
      {"@context":"https://schema.org","@type":"ItemList","name":"KPW professionals","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":t['name'],"url":BASE+'team/'+t['slug']+'.html'}
        for i,t in enumerate(TEAM)]}]
    P.append(p)
    for t in TEAM:
        P.append(_bio(t))
    return P
