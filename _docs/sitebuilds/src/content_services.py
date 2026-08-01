# -*- coding: utf-8 -*-
"""Services hub + 12 service pages."""
import html, re
from build import (FIRM, BASE, icon, ARROW, phero, faq_html, rel,
                   org_schema, breadcrumb_schema, faq_schema, service_schema)

def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()

SERVICES = [
 dict(slug='tax-planning-preparation', ic='calc', nav_title='Tax Planning &amp; Preparation',
   short='Year-round planning for businesses and their owners, with year-end liability forecasts — not a conversation that starts in March.',
   title='Tax Planning & Preparation | CPA in Downers Grove, IL | KPW',
   desc='Year-round tax planning and return preparation for Illinois businesses, owners, and fiduciaries — year-end liability forecasts and S corporation planning.',
   eyebrow='Tax', h1='Tax planning that starts before the year ends.',
   sub='Maximizing after-tax earnings is the objective. That requires planning throughout the year — not a few meetings when it is time to file.',
   body='''
<h2>The short answer</h2>
<p>We provide year-round tax planning and return preparation for privately held businesses, their owners, individuals, trusts, and estates. You receive forecasts of year-end tax liabilities with enough time to reduce or defer them, and you address tax concerns as they develop rather than discovering them at filing.</p>

<h2>Why timing is the whole game</h2>
<p>By the time a return is due, nearly every decision that moves the number has already been made. Entity structure, owner compensation, the timing of income and deductions, equipment purchases and how they are financed, retirement plan contributions, whether to make or revoke a Subchapter S election, how a property sale is structured — all of it is decided during the year, often in a meeting where taxes were not on the agenda.</p>
<p>Preparation without planning is transcription. We do both, and we treat the planning half as the part you are actually paying for.</p>

<h2>What our tax work covers</h2>
<h3>Business taxation</h3>
<p>Our planners work in federal, state, and local law across a wide range of issues, including:</p>
<ul>
<li><strong>Balancing taxes between the corporation and its owners.</strong> For a closely held company, the entity return and the shareholder returns are one calculation. Reasonable compensation, distributions, basis, and loss limitations all interact.</li>
<li><strong>Subchapter S corporation planning.</strong> Election timing, eligibility maintenance, shareholder basis tracking, distribution planning, and the built-in gains exposure that follows a C-to-S conversion.</li>
<li><strong>Special taxation planning for businesses that own their facilities.</strong> Whether the real estate belongs inside the operating entity or in a separate ownership structure changes the tax outcome on operations, on refinancing, and eventually on sale.</li>
<li><strong>Leasing considerations.</strong> The lease-versus-buy analysis is a tax question, a cash flow question, and a balance-sheet question at once, and the right answer depends on all three.</li>
</ul>

<h3>Individual, trust, and estate returns</h3>
<p>We prepare income tax returns for individuals and businesses, and for the fiduciaries who administer trusts and estates. For business owners, these are prepared alongside the entity return by the same people, which is the only way the planning holds together.</p>

<h3>Illinois and multi-state issues</h3>
<p>Illinois clients face a set of questions that do not appear in a generic tax guide: the pass-through entity tax election and whether it helps a given owner, the replacement tax on entities, allocation and apportionment when a company sells or delivers across state lines, and Cook County and municipal impositions that vary by a few blocks. Nexus problems in particular tend to surface years late, in the form of a notice.</p>

<h2>Staying current</h2>
<p>Tax law moves, and the useful version of "staying current" is not a newsletter — it is a firm that notices which change affects <em>your</em> facts and calls you about it. Clients hear about developments that matter to them before the development is a problem.</p>

<div class="callout"><p><strong>Estate tax coordination.</strong> Our estate planning consultants work with you to minimize the impact of estate taxes on your survivors, and to transfer a business interest to the next generation under the most favorable tax conditions available. See <a href="estate-trust-planning.html">estate and trust planning</a>.</p></div>

<h2>How an engagement runs</h2>
<p>Most business clients settle into a rhythm: a planning conversation before year-end while there is still room to act, a preparation cycle after the books close, and calls in between whenever something material happens — a large purchase, a new state, a change in ownership, an offer to buy. The planning conversation is the one that pays for itself.</p>
''',
   faqs=[("When should tax planning happen?",
          "<p>Before the transaction, and at minimum before December 31. The decisions that change a tax bill are made during the year; the return records them. We forecast year-end liabilities while there is still time to act.</p>"),
         ("Do you prepare both the business and the owner's return?",
          "<p>Yes, and for closely held companies that is the point. Balancing income between the corporation and its owners only works when one firm sees both returns.</p>"),
         ("Can you help with an IRS or Illinois Department of Revenue notice?",
          "<p>Yes. The firm handles examination and notice matters, including representation before the IRS. Send the notice before responding to it — many are resolved with a letter, and some are simply wrong.</p>"),
         ("Do you handle multi-state filings?",
          "<p>Yes. Nexus, allocation, and apportionment questions come up constantly for Illinois companies selling or delivering across state lines, and they are far cheaper to address prospectively than after a state finds you.</p>")],
   related=[('audit-assurance','Audit &amp; assurance'),('business-advisory','Business advisory'),
            ('estate-trust-planning','Estate &amp; trust planning'),('../guides/cpa-cost-small-business.html','What a CPA costs')]),

 dict(slug='audit-assurance', ic='shield', nav_title='Audit &amp; Assurance',
   short='Financial statement audits for governmental bodies, non-profits, and privately held companies, planned around risk and your reporting deadlines.',
   title='Audit & Assurance Services | Illinois CPA Firm | KPW',
   desc='Financial statement audits by an AICPA peer-reviewed Illinois CPA firm. Risk-based planning, tests of controls, substantive testing, and a management letter you can act on.',
   eyebrow='Assurance', h1='An audit is only as good as the approach behind it.',
   sub='Most audited financial statements look alike on the surface. What determines their value is how the audit was planned, what was tested, and what you are told afterward.',
   body='''
<h2>The short answer</h2>
<p>We perform financial statement audits for governmental organizations, non-profits, and privately held companies. Our objective is to render an opinion on the financial statements in accordance with generally accepted auditing standards — and, along the way, to tell you what we learned about your business.</p>

<h2>Our general approach</h2>
<p>The approach is built on decades of audit experience. The main objective is the opinion. But the audit team is always looking for ways to provide advisory observations that help clients operate more efficiently and effectively, because a team that has just spent weeks inside your accounting system knows things worth telling you.</p>

<h2>How we plan the specific audit</h2>
<h3>1. Risk assessment</h3>
<p>Planning begins by assessing the general risks of the organization: comparison to similar entities, consideration of national and local economic conditions, and an independent analysis through ratio analysis. This is where an audit either becomes targeted or becomes a checklist.</p>

<h3>2. The specific audit plan</h3>
<p>From the risk assessment we develop the audit plan and design our substantive procedures, together with tests of controls where we intend to rely on them. Generally accepted auditing standards require an understanding of internal control sufficient to assess risk, and the plan reflects what that assessment finds.</p>

<h3>3. Controls</h3>
<p>We are required to understand your internal control well enough to assess risk. Where we plan to rely on controls, we test them, and the results determine how much substantive testing specific balance sheet accounts require — strong, evidenced controls reduce testing, weak ones increase it. Where reliance is not planned or not practical, which is common in smaller organizations, we take a fully substantive approach instead. Either way, control documentation is worth doing well before the auditors arrive.</p>

<h3>4. Substantive testing</h3>
<p>Substantive procedures focus on confirmation with outside parties, observation, vouching of invoices, and recalculation of specific data — direct evidence rather than inference.</p>

<h3>5. Communication throughout</h3>
<p>During controls and substantive testing we stay in constant communication with management, evaluating and informing them of problems or adjustments as they are identified. Nothing material should be a surprise in the closing meeting.</p>

<h3>6. Closing and reporting</h3>
<p>When fieldwork is complete we meet with management to finalize adjustments and any other items that arose. After the statements are prepared but before final issuance, we review the draft statements and reports with management to close open items. We are then available to meet with the finance committee or the board of directors to review the audit.</p>

<div class="callout"><p><strong>What you get beyond the opinion.</strong> Our audit team looks for potential problems — waste, nonproductive assets, and other conditions that affect profitability. We discuss findings with you personally and provide a written report in the form of a management letter.</p></div>

<h2>Governmental and non-profit audits</h2>
<p>Two of our partners have specialized in governmental and non-profit audit work for decades. That environment has its own requirements, its own funder expectations, and its own audience: a board or finance committee that needs to understand the statements well enough to govern by them. Detail on our <a href="../industries/government-nonprofit.html">government and non-profit practice</a>.</p>

<h2>Independent verification of our own work</h2>
<p>Our accounting and auditing practice is enrolled in the AICPA peer review program and is independently reviewed every three years under the auspices of the Illinois CPA Society. The reviewer examines whether our quality control policies are suitable and whether we comply with them. <a href="../peer-review.html">More on peer review</a>.</p>
''',
   faqs=[("Do we need an audit at all?",
          "<p>Usually the requirement comes from outside — a lender's covenant, a bonding company, a grant agreement, a state agency, or your own operating agreement or bylaws. If nothing requires an audit, a <a href=\"financial-statements.html\">review or compilation</a> may be the right level of service and considerably less expensive.</p>"),
         ("How long does an audit take?",
          "<p>It depends on size, the condition of your records, and how quickly requested items arrive. The controllable variable on your side is preparation: reconciled accounts, supporting schedules, and available staff shorten fieldwork more than anything we can do.</p>"),
         ("What is a management letter?",
          "<p>A written report of the conditions we observed that affect your operations or controls — deficiencies, inefficiencies, waste, nonproductive assets. It is separate from the opinion and is frequently the most useful document an audit produces.</p>"),
         ("Will you present to our board or finance committee?",
          "<p>Yes. After the statements are finalized we make ourselves available to meet with the finance committee or board to review the audit.</p>")],
   related=[('financial-statements','Financial statements'),('accounting-compilation','Accounting services'),
            ('../peer-review.html','Peer review'),('../guides/audit-review-compilation.html','Audit vs. review vs. compilation')]),

 dict(slug='financial-statements', ic='doc', nav_title='Financial Statements',
   short='Audit, review, and compilation — plus internal, forecasted, projected, and pro forma statements prepared to the format your lender expects.',
   title='Financial Statement Services | Audit, Review & Compilation | KPW',
   desc='Three levels of financial statement service — audit, review, and compilation — plus forecasted, projected, and pro forma statements for Illinois businesses.',
   eyebrow='Reporting', h1='Three levels of service. The trick is choosing the right one.',
   sub='Depending on the extent of your needs, KPW provides audit, review, and compilation services — and the statement formats lenders, boards, and buyers actually ask for.',
   body='''
<h2>The short answer</h2>
<p>KPW provides three levels of financial statement service — audit, review, and compilation — and prepares statements in compiled, internal historical, forecasted, projected, and pro forma formats. Regardless of level, you receive insight and information you can use to strengthen the policies that drive your company's earnings and growth.</p>

<h2>Choosing the level</h2>
<table class="plain"><thead><tr><th>Level</th><th>Assurance provided</th><th>Typically required by</th></tr></thead><tbody>
<tr><td><strong>Audit</strong></td><td>Reasonable assurance — an opinion that the statements are fairly stated in all material respects</td><td>Bank covenants, bonding companies, government funders, grant agreements, buyers in due diligence</td></tr>
<tr><td><strong>Review</strong></td><td>Limited assurance, based on analytical procedures and inquiry</td><td>Lenders on smaller facilities, some franchisors, some operating agreements</td></tr>
<tr><td><strong>Compilation</strong></td><td>No assurance — your figures presented in financial statement format</td><td>Internal management use, some vendor and surety requirements</td></tr>
</tbody></table>
<p>Cost tracks the amount of work each level requires, which is why the useful first question is not "how much" but "who is requiring this, and what exactly did they ask for." If nobody is requiring anything, you may need less than you assumed. Our <a href="../guides/audit-review-compilation.html">full comparison guide</a> works through the decision.</p>

<h2>Statement formats we prepare</h2>
<ul>
<li><strong>Compiled statements</strong> — your figures, properly presented, for the reader who requested them.</li>
<li><strong>Internal historical statements</strong> — management reporting built for the people running the company rather than for outside compliance.</li>
<li><strong>Forecasted statements</strong> — expected results based on the conditions you expect to face.</li>
<li><strong>Projected statements</strong> — results under a stated set of hypothetical assumptions, such as an acquisition or a new facility.</li>
<li><strong>Pro forma statements</strong> — the effect of a specific completed or proposed transaction on historical results.</li>
</ul>
<p>Forecasted, projected, and pro forma statements are the ones lenders and buyers ask for at the least convenient moment. They rest on assumptions, and the assumptions have to be defensible.</p>

<h2>What a comprehensive audit includes</h2>
<p>Where an audit is the required level, the work includes:</p>
<ul>
<li>Obtaining an understanding of your accounting system and evaluating its procedures and controls</li>
<li>Observing physical inventory counts and testing inventory valuation</li>
<li>Testing compliance with manufacturers' selling agreements and management contracts</li>
<li>Confirmation with outside parties — banks, customers, vendors, and attorneys</li>
<li>Physical inspection and observation</li>
<li>Tracing transactions to supporting documents</li>
<li>Evaluating cash management and compensation practices as they affect the statements</li>
</ul>
<p>Auditor independence limits what we can do <em>for</em> you during an attest engagement — we observe and test rather than operate. What we learn along the way, however, we tell you. The team notes conditions that affect profitability, including waste and nonproductive assets, and we discuss them with you personally and set them out in a written management letter. Where you want us to actually build or fix something — inventory controls, close procedures, cash management — that is separate <a href="business-advisory.html">advisory work</a>, engaged separately.</p>

<div class="callout"><p><strong>The value is in the approach.</strong> Most audited statements look similar once bound. What differs is whether the audit was planned around your actual risks and whether anyone told you what they learned.</p></div>
''',
   faqs=[("What is the practical difference between a review and an audit?",
          "<p>A review consists mainly of analytical procedures and inquiry and provides limited assurance. An audit adds tests of controls, third-party confirmation, physical observation, and vouching, and provides reasonable assurance — a materially higher bar, at materially higher cost.</p>"),
         ("Can you prepare projections for a bank or a buyer?",
          "<p>Yes. We prepare forecasted, projected, and pro forma statements. The work is in the assumptions, which need to be supportable when a lender or a buyer's advisor tests them.</p>"),
         ("Our lender changed the requirement mid-year. Now what?",
          "<p>Call as early as possible. Moving from compilation to review, or review to audit, mid-cycle is workable but affects scope, timing, and sometimes what evidence is still obtainable for the earlier part of the year.</p>")],
   related=[('audit-assurance','Audit &amp; assurance'),('accounting-compilation','Accounting services'),
            ('business-advisory','Business advisory'),('../guides/audit-review-compilation.html','Comparison guide')]),

 dict(slug='accounting-compilation', ic='ledger', nav_title='Accounting Services',
   short='Financial statement preparation, month-end support, and the reporting discipline that makes every other decision easier.',
   title='Accounting Services for Illinois Businesses | KPW CPAs',
   desc='Accounting services from an Illinois CPA firm: financial statement preparation, month-end close support, chart of accounts design, and reporting built for owners and lenders.',
   eyebrow='Accounting', h1='Numbers you can run a company on.',
   sub='Accounting work exists so that somebody can make a decision. We prepare statements that answer questions rather than just satisfy a filing requirement.',
   body='''
<h2>The short answer</h2>
<p>We prepare financial statements in compiled, internal historical, forecasted, projected, and pro forma formats, and we support the accounting function behind them — chart of accounts structure, month-end close discipline, reconciliation practices, and the reporting package your owners and lenders actually read.</p>

<h2>The problem with most small-company financials</h2>
<p>They are built for the tax return. That is understandable and it is also why so many owners cannot answer basic questions from their own statements: which product line actually makes money, what the true cost of a job was, whether last month was good or merely busy.</p>
<p>A chart of accounts designed around a tax form produces a document that satisfies a filing and informs nobody. Restructuring it — separating direct costs from overhead, splitting revenue into the lines management thinks in, isolating owner-discretionary spending — usually costs one engagement and changes every conversation afterward.</p>

<h2>What we do</h2>
<h3>Financial statement preparation</h3>
<p>Statements prepared on the basis appropriate to your circumstances and the reader who requested them, in the formats listed on our <a href="financial-statements.html">financial statements page</a>.</p>

<h3>Month-end close support</h3>
<p>A close that finishes in the first week of the following month is worth more than a perfect close that finishes in six. We help set the cutoff procedures, reconciliations, and review steps that make it repeatable — and identify what does not need to be done monthly at all.</p>

<h3>Reconciliation and cleanup</h3>
<p>Bank and credit card reconciliations, undeposited funds, mis-posted accounts, inventory that never ties, loan balances that drift from the amortization schedule. These are unglamorous and they are also why year-end costs more than it should.</p>

<h3>Internal control procedures</h3>
<p>Segregation of duties is difficult in a small office and it is not impossible. There are practical controls that fit a company with three people in the back office, and there are controls that only work with thirty. We recommend the ones that fit. This work overlaps with our <a href="business-advisory.html">management advisory</a> practice.</p>

<h3>Reporting for owners and lenders</h3>
<p>A monthly package that a non-accountant owner can read in ten minutes — with the two or three measures that actually move the business, rather than fourteen pages of accounts.</p>

<div class="callout"><p><strong>Clean books lower every other fee you pay.</strong> Tax preparation, audits, valuations, due diligence, and loan applications all begin by establishing that the numbers can be relied upon. When they can, everything downstream is faster.</p></div>

<h2>Working with your existing bookkeeper</h2>
<p>Most of our clients have someone doing the day-to-day work, whether in-house or outsourced. That relationship usually should not change. What we add is structure, review, and the ability to answer the questions a bookkeeper is not positioned to answer.</p>
''',
   faqs=[("Do you replace our bookkeeper?",
          "<p>Rarely, and usually we recommend against it. The better arrangement is a bookkeeper handling daily transactions with our firm providing structure, periodic review, statement preparation, and the judgment calls.</p>"),
         ("Which accounting software do you work with?",
          "<p>We work with the systems our clients already use. Software matters far less than whether the chart of accounts is designed to answer management's questions and whether accounts are reconciled.</p>"),
         ("Our books are a mess. Is that a problem?",
          "<p>It is a common starting point, not a disqualification. Cleanup is a defined project with a beginning and an end, and it is almost always cheaper than continuing to make decisions on unreliable numbers.</p>")],
   related=[('financial-statements','Financial statements'),('tax-planning-preparation','Tax planning'),
            ('business-advisory','Business advisory'),('audit-assurance','Audit &amp; assurance')]),

 dict(slug='business-advisory', ic='chart', nav_title='Business Advisory',
   short='Cash flow projections, loan packaging, benefit plan design, internal controls, succession planning, and the operating questions in between.',
   title='Business & Management Advisory Services | KPW CPAs Illinois',
   desc='Management advisory for Illinois businesses — cash flow projections, loan packaging, benefit plans, buy-sell agreements, succession planning, and internal controls.',
   eyebrow='Advisory', h1='The questions that do not fit on a tax form.',
   sub='Cash flow, financing, benefit plans, buy-sell agreements, succession, internal controls — the decisions that sit between accounting and strategy, where an owner has no one independent to ask.',
   body='''
<h2>The short answer</h2>
<p>Our management advisory practice covers the operating and financial decisions that sit between accounting and strategy: cash flow projections, loan packaging and capital formation, mergers and acquisitions, due diligence, reconciliation work, insurance reviews, compensation and benefit plan design, buy-sell agreements, succession and estate planning, internal control procedures, business valuations, and personnel hiring and training.</p>

<h2>The pressures behind the questions</h2>
<p>Owner-operated companies contend with competition, taxes, product liability, cyclical seasons, environmental and safety requirements, financing choices, and increasingly sophisticated technology — usually several at once, and usually while the owner is also running the day-to-day. What a CPA firm adds is a place to take those decisions where the answer does not depend on the answer.</p>

<h2>Where we are most useful</h2>
<h3>Cash flow projections</h3>
<p>Profitable companies fail on cash, not on profit. Projections that model collection timing, seasonal working capital swings, debt service, and tax payments turn a vague worry into a schedule you can plan against — and they are the document a lender wants before a line of credit conversation gets serious.</p>

<h3>Loan packaging and capital formation</h3>
<p>Lenders want a specific package: historical statements at the level their credit policy requires, projections with defensible assumptions, personal financial statements, and a coherent explanation of the use of proceeds and repayment source. We assemble that package. One of our partners specifically assists clients in obtaining financing for both ongoing and start-up businesses.</p>

<h3>Compensation and benefit plans</h3>
<p>Profit sharing plans, 401(k) plans, pension plans, Section 125 cafeteria plans, and deferred compensation arrangements — evaluated for what they cost, what they accomplish for owners and employees, and what compliance obligations they create. See <a href="employee-benefit-plans.html">employee benefit plans</a>.</p>

<h3>Buy-sell agreements</h3>
<p>Most buy-sell agreements are drafted at formation and never revisited, which means the valuation mechanism inside them was written for a company that no longer exists. The provision that matters is how the price is determined; we review it, model what it would actually produce today, and coordinate with counsel on revisions. Related: <a href="business-valuation.html">business valuation</a>.</p>

<h3>Succession planning</h3>
<p>Transferring a company to the next generation or to a management team is a tax problem, a valuation problem, a financing problem, and a family problem simultaneously. Starting years early is what makes the tax-efficient answer available at all. See also <a href="estate-trust-planning.html">estate and trust planning</a>.</p>

<h3>Internal control procedures</h3>
<p>Practical controls sized to your actual staffing — the point is to make the common failures difficult, not to build a bureaucracy a ten-person company cannot sustain.</p>

<h3>Due diligence, insurance reviews, and reconciliation work</h3>
<p>Buying a business, evaluating whether coverage matches exposure, or untangling accounts that have not tied out in years. All three benefit from an outside professional who has no reason to tell you what you want to hear.</p>

<h3>Personnel hiring and training</h3>
<p>Specifically for accounting and finance roles: what the position actually requires, how to evaluate candidates when you are not an accountant, and how to bring a new controller or bookkeeper up to speed on your systems.</p>

<div class="callout"><p><strong>Independence is the product.</strong> Much of the advice available to an owner comes from people compensated on the transaction they are recommending. That does not make it wrong, but it does mean somebody should be looking at the decision without a position in it. A firm billing for its time is in that position.</p></div>
''',
   faqs=[("Do you help owners obtain financing?",
          "<p>Yes. Loan packaging and capital formation are core to this practice, and one partner specifically assists clients with financing for ongoing and start-up businesses.</p>"),
         ("Can you review our existing buy-sell agreement?",
          "<p>Yes. We look at how the agreement determines price, model what that formula produces given the company as it exists now, and coordinate with your attorney on changes. Agreements written a decade ago frequently produce a number no current owner would accept.</p>"),
         ("How early should succession planning start?",
          "<p>Years before the transition. The most tax-efficient approaches require time to execute — gifting programs, valuation discounts where legitimately available, financing structures, and management development all take multiple years.</p>"),
         ("Is advisory work billed separately from the tax engagement?",
          "<p>Yes. Some questions get answered in a phone call as part of the ongoing relationship; defined projects are scoped and priced as their own engagement.</p>")],
   related=[('business-valuation','Business valuation'),('mergers-acquisitions','Mergers &amp; acquisitions'),
            ('employee-benefit-plans','Employee benefit plans'),('estate-trust-planning','Estate &amp; trust planning')]),

 dict(slug='business-valuation', ic='scale', nav_title='Business Valuation',
   short='Defensible valuations for sales, buy-sell agreements, gift and estate filings, and litigation — by an AICPA-accredited valuation analyst.',
   title='Business Valuation Services | AICPA Accredited (ABV) | KPW Illinois',
   desc='Business valuations for sales, buy-sell agreements, gift and estate filings, and disputes — by a CPA Accredited in Business Valuation (ABV) by the AICPA.',
   eyebrow='Valuation', h1='A number is only useful if it survives scrutiny.',
   sub='Valuations performed by a CPA holding the AICPA\'s Accredited in Business Valuation credential — built to withstand an IRS examiner, an opposing expert, or a buyer\'s advisor.',
   body='''
<h2>The short answer</h2>
<p>We value closely held businesses and ownership interests for transactions, buy-sell agreements, gift and estate tax filings, divorce, shareholder disputes, and litigation. The work is led by Glenn Byers, CPA, who holds the AICPA's Accredited in Business Valuation (ABV) credential, and it is supported by the firm's audit and tax capability.</p>

<h2>Why the purpose comes first</h2>
<p>There is no single value for a business. The number depends on the standard of value being applied — fair market value, fair value, investment value — and that standard is dictated by why the valuation exists. A gift tax filing, an Illinois dissolution proceeding, and a strategic buyer's offer can each produce a defensible and materially different figure for the same company on the same date.</p>
<p>So the first conversation is about purpose, audience, and effective date. Everything else follows from those three answers.</p>

<h2>What valuations get used for</h2>
<ul>
<li><strong>Selling or buying a business.</strong> Establishing a supportable asking price, or testing whether an offer is reasonable. See <a href="mergers-acquisitions.html">mergers and acquisitions</a>.</li>
<li><strong>Buy-sell agreements.</strong> Setting or updating the value that governs a partner's departure, death, or disability — before it is needed, when it can still be negotiated calmly.</li>
<li><strong>Gift and estate tax filings.</strong> Transfers of closely held interests require support that withstands IRS examination, including any discounts claimed for lack of control or lack of marketability.</li>
<li><strong>Divorce.</strong> Illinois courts require a value for a marital interest in a closely held business, and the analysis is routinely contested.</li>
<li><strong>Shareholder disputes and dissenting shareholder matters.</strong> Where fair value rather than fair market value typically governs.</li>
<li><strong>Succession and estate planning.</strong> Knowing what the business is worth is a prerequisite to planning around it.</li>
</ul>

<h2>How the analysis works</h2>
<p>Valuation practice recognizes three approaches, and a competent engagement considers all three before concluding which deserve weight:</p>
<h3>Income approach</h3>
<p>Value derived from expected future economic benefits — capitalized earnings or discounted cash flow — with a discount or capitalization rate developed from market evidence and company-specific risk. Normalizing adjustments matter here: owner compensation above or below market, discretionary expenses, non-operating assets, and non-recurring items.</p>
<h3>Market approach</h3>
<p>Value inferred from transactions in comparable companies or comparable interests, adjusted for differences in size, growth, risk, and marketability.</p>
<h3>Asset approach</h3>
<p>Value built from adjusted net assets. Most relevant for holding companies, asset-intensive businesses, and situations where liquidation is the realistic alternative.</p>

<h3>Discounts and premiums</h3>
<p>Minority interests generally warrant a discount for lack of control; interests in closely held companies generally warrant a discount for lack of marketability. Both are heavily scrutinized in tax and litigation settings and both must be supported by evidence rather than convention.</p>

<div class="callout"><p><strong>Independence protects the conclusion.</strong> A valuation prepared to reach a predetermined number is worth nothing the moment it is challenged. Ours are prepared to be defended.</p></div>

<h2>Valuation in litigation</h2>
<p>Where the valuation will be contested, the analyst becomes a witness. The firm regularly provides expert testimony and consulting to law firms, including valuation and the calculation of lost wages and profits. See <a href="litigation-support.html">litigation support</a>.</p>
''',
   faqs=[("What does ABV mean?",
          "<p>Accredited in Business Valuation — a credential granted by the AICPA to CPAs who meet its experience and examination requirements in business valuation. It signals specific, tested competence in the discipline rather than general accounting practice.</p>"),
         ("How long does a valuation take?",
          "<p>Typically several weeks, driven by how quickly financial records, contracts, and management interviews come together, and by the level of report required. Litigation engagements are often longer because the analysis must anticipate challenge.</p>"),
         ("Can one valuation serve several purposes?",
          "<p>Sometimes, but not reliably. Different purposes invoke different standards of value and different effective dates. Tell us every intended use up front so the engagement is scoped correctly.</p>"),
         ("Will you defend the valuation if it is challenged?",
          "<p>Yes. We prepare valuations expecting them to be examined, and we provide expert testimony where the matter proceeds to litigation.</p>")],
   related=[('mergers-acquisitions','Mergers &amp; acquisitions'),('litigation-support','Litigation support'),
            ('estate-trust-planning','Estate &amp; trust planning'),('business-advisory','Business advisory')]),

 dict(slug='estate-trust-planning', ic='estate', nav_title='Estate &amp; Trust Planning',
   short='Minimizing estate tax impact on survivors, and moving a business interest to the next generation on favorable terms.',
   title='Estate & Trust Planning for Illinois Families and Business Owners | KPW',
   desc='Estate and trust tax planning in Illinois — minimizing estate tax impact on survivors, transferring business interests to the next generation, and fiduciary returns.',
   eyebrow='Estate', h1='Planning so the next generation inherits a business, not a problem.',
   sub='Our estate planning consultants work to minimize the impact of estate taxes on your survivors and to transfer your business interest to the next generation under the most favorable tax conditions.',
   body='''
<h2>The short answer</h2>
<p>We handle the tax and accounting side of estate and trust planning — projecting exposure, structuring transfers of closely held business interests, preparing fiduciary returns, and coordinating with the attorney who drafts the instruments. The legal documents are your lawyer's work. Whether they produce the intended tax result is ours.</p>

<h2>Why Illinois families face two problems, not one</h2>
<p>Illinois imposes its own estate tax with an exclusion that has historically been well below the federal amount. The practical effect for many families in the western suburbs and the city is an estate large enough to owe Illinois estate tax while owing nothing federally — a result that surprises people who have only read about the federal exemption.</p>
<p>Since the federal exclusion amount has changed repeatedly by legislation and is subject to future change, planning that depends entirely on a particular exemption level is fragile by construction. Plans that work do so across a range of outcomes.</p>

<h2>The business owner's version of the problem</h2>
<p>For an owner whose company is most of the estate, the difficulty is not sentiment but liquidity. Estate tax is payable in cash on a schedule. An illiquid estate concentrated in a closely held business can force the sale of the business to pay the tax on the business — the outcome nearly every succession plan exists to prevent.</p>
<p>Addressing it takes years and usually several tools at once:</p>
<ul>
<li><strong>Valuation as the foundation.</strong> Nothing can be planned around an unknown number. See <a href="business-valuation.html">business valuation</a>.</li>
<li><strong>Systematic lifetime transfers.</strong> Moving interests over time, using annual exclusion gifting and applicable exemptions, with legitimate discounts where the facts support them.</li>
<li><strong>Entity structure.</strong> How ownership is held affects both what transfers and what control the senior generation retains during the transition.</li>
<li><strong>Funded buy-sell agreements.</strong> A mechanism and a source of cash, so a death does not become a forced negotiation among heirs and surviving owners. See <a href="business-advisory.html">business advisory</a>.</li>
<li><strong>Basis planning.</strong> The interaction between transfer tax savings and the income tax basis heirs receive is frequently the deciding factor, and it cuts against reflexive lifetime gifting in many estates.</li>
</ul>

<h2>Fiduciary compliance</h2>
<p>We prepare income tax returns for trusts and estates and advise fiduciaries on distributions, income allocation between the entity and beneficiaries, and elections available during administration. Trustees and executors carry personal responsibility for getting this right, and most are serving in the role for the first time.</p>

<div class="callout"><p><strong>Coordination is not optional.</strong> Estate plans fail in the gaps — a trust drafted correctly but never funded, a beneficiary designation that overrides the will, a buy-sell that contradicts the estate plan. We work directly with your attorney so the pieces agree with one another.</p></div>

<h2>Asset protection</h2>
<p>Preservation and protection of assets is a related discipline and, for some clients, the more pressing one. See <a href="asset-protection.html">asset protection and wealth preservation</a>.</p>
''',
   faqs=[("Do you write wills and trusts?",
          "<p>No. Drafting legal instruments is the practice of law. We handle the tax analysis and the accounting, and we work alongside your attorney so the documents accomplish what the plan intends.</p>"),
         ("Does Illinois have its own estate tax?",
          "<p>Yes, separate from the federal estate tax and historically with a considerably lower exclusion. Estates that owe nothing federally can still owe Illinois estate tax. Current thresholds should be confirmed for your year — the planning point is that the two systems must be considered together.</p>"),
         ("When should a business owner begin?",
          "<p>Years before any anticipated transition. The tools that reduce exposure most — systematic gifting, structural changes, funded agreements — require time to execute and become unavailable once health or a transaction forces the timeline.</p>"),
         ("Can you prepare trust and estate income tax returns?",
          "<p>Yes. We prepare fiduciary returns and advise trustees and executors on the elections and allocations available during administration.</p>")],
   related=[('business-valuation','Business valuation'),('asset-protection','Asset protection'),
            ('tax-planning-preparation','Tax planning'),('business-advisory','Succession planning')]),

 dict(slug='litigation-support', ic='gavel', nav_title='Litigation Support',
   short='Expert testimony and consulting for law firms: bankruptcy, financial and tax fraud, lost wages and profits, wrongful death, personal injury, and divorce.',
   title='Litigation Support & Expert Witness Services | CPA Chicago | KPW',
   desc='Forensic accounting and expert witness services for Illinois law firms — bankruptcy, financial and tax fraud, lost wages and profits, personal injury, and divorce.',
   eyebrow='Forensic', h1='Testimony that holds up on cross-examination.',
   sub='Law firms retain KPW for expert testimony and consulting on complex matters. The work draws on every other capability in the firm — audit, valuation, and tax.',
   body='''
<h2>The short answer</h2>
<p>KPW is frequently asked by referring legal firms to provide expert testimony or consulting on complex cases involving federal bankruptcy (including debtor-in-possession representation), financial fraud, tax fraud and evasion, wrongful death, personal injury, and divorce. Two partners work regularly in this area, and the engagements draw on the firm's valuation and audit capability.</p>

<h2>Where we are engaged</h2>
<h3>Federal bankruptcy and debtor-in-possession representation</h3>
<p>Bankruptcy accounting has its own reporting requirements and its own audience — the court, the trustee, the committee, and the secured creditors, none of whom accept a company's ordinary internal reporting at face value. We prepare and analyze the accounting a proceeding requires and address the transaction history that precedes a filing.</p>

<h3>Financial fraud</h3>
<p>Tracing funds, reconstructing records that were never intended to be reconstructed, and quantifying loss. Fraud investigation differs from audit in objective: an audit tests whether statements are fairly stated, while a fraud engagement asks what happened, when, and how much.</p>

<h3>Tax fraud and evasion</h3>
<p>Analysis in matters involving unreported income, claimed deductions, and the distinction between an aggressive position and an intentional misstatement — a distinction that is frequently the entire case.</p>

<h3>Lost wages and lost profits</h3>
<p>Economic damages calculations in wrongful death, personal injury, and commercial disputes. Lost earnings analysis requires an earnings base, a work-life expectation, growth and discount assumptions, and offsets — every one of which the opposing expert will test. Lost profits require establishing what the business would have earned but for the conduct at issue, which demands a defensible baseline rather than an optimistic projection.</p>

<h3>Divorce</h3>
<p>Valuing a marital interest in a closely held business, analyzing income available for support where a spouse controls the entity that pays them, and tracing assets between marital and non-marital classifications. See <a href="business-valuation.html">business valuation</a>.</p>

<h2>How we work with counsel</h2>
<p>Engagements come in two shapes. As a <strong>consulting expert</strong>, we analyze the financial facts, test the other side's numbers, and help develop examination themes. As a <strong>testifying expert</strong>, we produce a report and defend it in deposition and at trial. The distinction affects discoverability, and counsel should establish it at the outset.</p>
<p>The practical value of a CPA firm in this setting is that the analysis is grounded in how the records were actually kept. Someone who has audited closely held companies for decades knows where owner-controlled entities hide things, because those are the same accounts that require the most audit attention in ordinary engagements.</p>

<div class="callout"><p><strong>We work with counsel across the Chicago metropolitan area.</strong> Most of this work happens in documents and depositions rather than in our office, so location rarely constrains the engagement.</p></div>

<h2>What we need to get started</h2>
<p>The pleadings, the financial records available, the deadline, and a clear statement of the question you want answered. An early conversation about scope generally saves more than it costs, because the wrong question analyzed thoroughly is still the wrong question.</p>
''',
   faqs=[("What types of cases do you take?",
          "<p>Federal bankruptcy including debtor-in-possession representation, financial fraud, tax fraud and evasion, wrongful death, personal injury, and divorce. The common thread is that the financial analysis will be contested.</p>"),
         ("Do you serve as a testifying expert or a consultant?",
          "<p>Both. Counsel should decide which role applies at engagement, since it affects work product protection and discoverability.</p>"),
         ("How early should we bring in an accounting expert?",
          "<p>Earlier than most matters do. Early involvement shapes discovery requests, and the documents you fail to request are the ones the analysis will later need.</p>"),
         ("Can you review the opposing expert's report?",
          "<p>Yes. Rebuttal analysis is a substantial part of this work — testing assumptions, methodology, and the sensitivity of a conclusion to inputs that were selected rather than derived.</p>")],
   related=[('business-valuation','Business valuation'),('audit-assurance','Audit &amp; assurance'),
            ('mergers-acquisitions','Mergers &amp; acquisitions'),('../locations/downers-grove.html','Our office')]),

 dict(slug='mergers-acquisitions', ic='merge', nav_title='Mergers &amp; Acquisitions',
   short='Valuation, tax and entity structuring, financial modeling, due diligence, capital formation, and contract review for buyers and sellers.',
   title='Mergers & Acquisitions Advisory | Illinois Businesses | KPW',
   desc='M&A advisory for Illinois businesses — valuation, tax and entity structuring, financial modeling, due diligence, capital formation, and contract negotiation.',
   eyebrow='Transactions', h1='The deal is won or lost in the structure.',
   sub='KPW assists clients with starting, buying, or selling a business enterprise — handling the valuation, structuring, modeling, diligence, and negotiation support the transaction requires.',
   body='''
<h2>The short answer</h2>
<p>Our team handles the accounting and tax side of a transaction end to end: business valuation, tax and entity structuring, financial modeling, due diligence, capital formation, and contract review and negotiation. The firm has worked on transactions across a wide range of industries, with total transaction value, by the firm's own count, in excess of one billion dollars.</p>

<h2>Industries we have worked in</h2>
<p>Entertainment · Real estate · Distribution and cartage · Biotech and pharmaceuticals · Food and beverage · Software · Media and publishing · Iron and steel processing · Consumer products · Personal care and beauty · Computer reseller (VAR) · Financial services · Health care · Construction · Hospitality and leisure · Design and engineering</p>

<h2>Structure is where the money is</h2>
<p>Sellers focus on price. Price matters less than what remains after tax, and that is a function of structure.</p>
<h3>Asset sale versus stock sale</h3>
<p>The single most consequential decision in most closely held transactions. Buyers generally prefer assets — a stepped-up basis and depreciable deductions going forward, plus insulation from unknown liabilities. Sellers generally prefer stock — one layer of tax and a cleaner exit. The gap between the two positions is real money, and it is negotiable rather than fixed. Purchase price allocation among asset classes then determines how each side is taxed and is a negotiated term in its own right, not a formality at closing.</p>
<h3>Entity considerations</h3>
<p>Whether the target is a C corporation, an S corporation, or an LLC changes the analysis substantially, as does S corporation history — a company converted from C status carries built-in gains exposure for a statutory period, which can decide the structure by itself.</p>
<h3>Deal terms that behave like price</h3>
<p>Earnouts, seller notes, escrows and holdbacks, working capital adjustments, consulting and non-compete allocations, and rollover equity all shift value and timing. A headline number with unfavorable terms beneath it is frequently worth less than a lower number cleanly structured.</p>

<h2>Due diligence</h2>
<p>For buyers, diligence means quality of earnings before anything else: which reported profit is recurring, which depends on the departing owner, and which is an accounting artifact. It also means working capital normalization, contingent liabilities, tax exposure in states where the target has been filing incorrectly or not at all, customer concentration, and whether contracts survive a change of control.</p>
<p>For sellers, the same exercise run early — sell-side diligence — surfaces the problems while you still have time to fix them. Issues discovered by a buyer become price reductions. Issues you found and resolved are simply not issues.</p>

<h2>Valuation and modeling</h2>
<p>Every transaction rests on a valuation, whether or not anyone writes one down. We prepare formal valuations through our <a href="business-valuation.html">ABV-credentialed practice</a> and build the financial models that test whether a deal works — debt service coverage under the proposed capital structure, sensitivity to the assumptions that drive the price, and what happens if the first year disappoints.</p>

<h2>Capital formation</h2>
<p>Acquisitions require funding. We assemble the package lenders and investors expect and support the process through closing. See <a href="business-advisory.html">business advisory</a>.</p>

<div class="callout"><p><strong>Start earlier than feels necessary.</strong> Owners who begin preparing two or three years before a sale — cleaning up the books, resolving state tax exposure, reducing owner dependence, formalizing contracts — consistently transact at better terms than those who begin when an offer arrives.</p></div>
''',
   faqs=[("Do you represent buyers or sellers?",
          "<p>Both, on separate transactions. We are not the broker; we handle the valuation, structuring, diligence, modeling, and negotiation support, and we work alongside your attorney and, where one is involved, your investment banker.</p>"),
         ("Is an asset sale or a stock sale better?",
          "<p>It depends on which side you are on and on the entity's history. Buyers usually prefer assets for basis step-up and liability insulation; sellers usually prefer stock for single-layer taxation. It is a negotiable term, and the difference is often the largest single dollar item in the deal.</p>"),
         ("What is a quality of earnings analysis?",
          "<p>An assessment of which reported earnings are genuinely recurring — normalizing for owner compensation, discretionary and non-recurring items, accounting policy choices, and revenue that depends on the departing owner. Buyers pay for recurring earnings, not reported ones.</p>"),
         ("How long before a sale should we start preparing?",
          "<p>Two to three years if the timing is yours to choose. Clean records, resolved tax exposure, reduced owner dependence, and documented contracts all take time and all raise what a buyer will pay.</p>")],
   related=[('business-valuation','Business valuation'),('business-advisory','Business advisory'),
            ('financial-statements','Financial statements'),('litigation-support','Litigation support')]),

 dict(slug='asset-protection', ic='vault', nav_title='Asset Protection',
   short='Preserving what has been built — from a single domestic entity to coordinated domestic and offshore structures.',
   title='Asset Protection & Wealth Preservation | KPW CPAs Illinois',
   desc='Asset protection and wealth preservation for Illinois business owners and families — entity structuring, domestic and offshore trusts, and coordinated tax structures.',
   eyebrow='Preservation', h1='Preserving what took a career to build.',
   sub='The firm\'s long-stated view is that preservation and protection of assets is critical — and that nearly every client benefits from some level of wealth preservation and estate planning.',
   body='''
<h2>The short answer</h2>
<p>We advise on the structures that preserve accumulated wealth. Depending on the client's needs this can range from establishing a single domestic legal entity to a sophisticated wealth preservation structure involving domestic and offshore trusts, investment accounts, and coordinated tax structures. We coordinate this work with legal and investment firms in the United States and Europe.</p>

<h2>What asset protection actually is</h2>
<p>Legitimate asset protection is structural and it is done in advance. It is deciding, while nothing is wrong, how assets are titled and which entities hold which risks — so that a claim arising in one part of a business or a family's holdings does not reach everything else.</p>
<p>What it is not: moving assets once a claim exists or is reasonably foreseeable. That is a fraudulent transfer, it is unwound by courts, and it converts a financial problem into a legal one. The only version of this planning that works is the version done early.</p>

<h2>Where exposure typically concentrates</h2>
<ul>
<li><strong>Operating risk held alongside valuable assets.</strong> Real estate, equipment, or intellectual property sitting inside the entity that also carries the operating liability.</li>
<li><strong>Personal guarantees.</strong> Frequently signed years ago, forgotten, and still outstanding long after the leverage that justified them is gone.</li>
<li><strong>Professional liability.</strong> Where the exposure is personal and cannot be entity-shielded, insurance and titling carry the load instead.</li>
<li><strong>Insufficient or mismatched coverage.</strong> Insurance is the first layer of any protection plan, and reviewing whether coverage matches actual exposure is part of our <a href="business-advisory.html">advisory work</a>.</li>
<li><strong>Concentration.</strong> A family whose net worth is one business and one building has a structural problem no entity chart solves.</li>
</ul>

<h2>The tools, in rough order of complexity</h2>
<h3>Entity structure</h3>
<p>Separating operations from assets — an operating company that leases from a separate real estate entity, or holds intellectual property in a separate entity — is the foundation. It is unglamorous, inexpensive, and does most of the work.</p>
<h3>Titling and beneficiary designation</h3>
<p>How property is held between spouses, and how retirement accounts and insurance are designated, determines both creditor exposure and what happens at death. These are often set once and never reviewed.</p>
<h3>Domestic trusts</h3>
<p>Irrevocable structures that can, depending on how they are drafted, remove assets from an individual's taxable estate and from creditors' reach — with the genuine trade-off that control is surrendered. Irrevocability by itself does not accomplish either; retained powers pull assets back in. Any structure that preserves full control tends not to preserve protection either.</p>
<h3>Domestic and offshore structures</h3>
<p>For clients whose circumstances warrant it, sophisticated structures involving domestic and offshore trusts, investment accounts, and coordinated tax planning — developed with legal and investment firms in the United States and Europe.</p>

<div class="callout"><p><strong>Reporting is not optional.</strong> Offshore structures carry substantial U.S. information reporting obligations, and the penalties for failing to file are severe and largely independent of whether any tax was owed. Any structure we participate in is fully reported.</p></div>

<h2>Working with your attorney</h2>
<p>Entities and trusts are legal instruments and are drafted by counsel. Our role is the tax and accounting analysis: what each structure costs in complexity and compliance, how it is reported, and whether the protection it provides justifies what it takes to maintain. Related: <a href="estate-trust-planning.html">estate and trust planning</a>.</p>
''',
   faqs=[("Is asset protection legal?",
          "<p>Structuring ownership before a claim exists is ordinary, lawful planning. Transferring assets after a claim arises or is reasonably foreseeable is a fraudulent transfer, is reversible by courts, and creates worse problems than it solves. Timing is what separates the two.</p>"),
         ("Do I need an offshore structure?",
          "<p>Most clients do not. Entity separation, appropriate titling, adequate insurance, and a domestic trust where warranted address the majority of realistic exposure at a fraction of the cost and complexity. Offshore structures fit specific circumstances, not general anxiety.</p>"),
         ("Does asset protection change my taxes?",
          "<p>It can, in both directions, which is exactly why the tax analysis belongs alongside the legal design rather than after it.</p>"),
         ("Who drafts the documents?",
          "<p>Your attorney. We handle the tax and accounting analysis and coordinate with legal and investment firms in the United States and Europe on more complex structures.</p>")],
   related=[('estate-trust-planning','Estate &amp; trust planning'),('business-valuation','Business valuation'),
            ('tax-planning-preparation','Tax planning'),('business-advisory','Business advisory')]),

 dict(slug='entertainment-sports-management', ic='mic', nav_title='Business Management',
   short='Financial and tax representation for musicians, actors, and professional athletes — designed to track, measure, and protect while they work.',
   title='Business Management for Entertainment & Sports | CPA Chicago | KPW',
   desc='KPW acts as financial and tax agency for musicians, actors, and professional athletes — cash management, bill payment, bookkeeping, tax, and contract review.',
   eyebrow='Business management', h1='Financial and tax representation for people whose income is anything but ordinary.',
   sub='KPW acts as financial and tax agency for the entertainment industry — geared toward musicians, actors, and professional athletes.',
   body='''
<h2>The short answer</h2>
<p>At the client's request we provide a full business management service: establishing bank accounts, processing monthly bills, monthly bookkeeping, compiling financial statements, income tax planning, preparation and representation, contract review and negotiation, asset sourcing and procurement including luxury real estate and automobiles, estate planning, and litigation support.</p>
<p>The firm describes this as a practice area it can only offer because of the breadth of its core accounting, tax, and finance services, and that is accurate — no single discipline covers it. The service is intensive by design, built to track, measure, and protect our clients' interests while they concentrate on their work.</p>

<h2>What the engagement actually looks like</h2>
<p>The mechanics matter more here than the philosophy. Accounts are opened in the client's name. Bills arrive and are processed on a schedule. The books are kept monthly rather than reconstructed in March. Statements are produced and delivered whether or not anyone asks. Estimates are funded quarterly against income that arrived unevenly. Filings go out in every jurisdiction the work touched.</p>
<p>None of that is complicated. It is simply continuous, and it fails the moment it becomes occasional — which is why it is a distinct service rather than a tax engagement with extras. For why these careers need it, see <a href="../industries/entertainment-sports.html">entertainment and sports</a>.</p>

<h2>What the engagement covers</h2>
<h3>Cash management and bill payment</h3>
<p>Establishing bank accounts, processing monthly bills, and maintaining the monthly bookkeeping so that spending is visible and reconciled rather than discovered later. This is the operating core of the service.</p>
<h3>Financial reporting</h3>
<p>Compiled financial statements that show, in plain terms, what came in, what went out, and what remains — prepared regularly rather than annually.</p>
<h3>Tax planning, preparation, and representation</h3>
<p>Multi-state and multi-jurisdiction filings are routine in this practice. Athletes owe tax in states where they compete; touring performers face similar allocation across every jurisdiction they work in. Structuring, quarterly funding of estimates, and representation when a jurisdiction takes an interest are all part of the engagement. See <a href="tax-planning-preparation.html">tax planning and preparation</a>.</p>
<h3>Contract review and negotiation</h3>
<p>Reviewing the financial terms of agreements — how and when compensation is paid, what is deducted before it reaches you, what the accounting and audit rights are, and what happens on termination.</p>
<h3>Asset sourcing and procurement</h3>
<p>Assistance acquiring significant assets such as luxury real estate and automobiles, so that a purchase is structured, financed, and titled deliberately.</p>
<h3>Estate planning and litigation support</h3>
<p>Coordinated with our <a href="estate-trust-planning.html">estate practice</a> and, where disputes arise, our <a href="litigation-support.html">litigation support</a> capability.</p>

<div class="callout"><p><strong>Protection is the design principle.</strong> The structure of this service — separate accounts, documented approvals, reconciled monthly reporting, and an independent CPA firm rather than a single individual holding the keys — exists because of how business management relationships have failed elsewhere in this industry. Visibility is the safeguard.</p></div>

<h2>Who this is for</h2>
<p>More on the clients this practice serves: <a href="../industries/entertainment-sports.html">entertainment and sports</a>.</p>
''',
   faqs=[("What does a business manager do that an accountant does not?",
          "<p>A business manager runs the financial operation day to day — accounts, bill payment, bookkeeping, reporting — in addition to tax planning and preparation. A tax accountant sees you periodically; a business manager is in the accounts continuously.</p>"),
         ("Do you handle multi-state and international filings?",
          "<p>Yes. Athletes and touring performers generate filing obligations in every jurisdiction where they work. Allocation and credit calculations across those jurisdictions are a standing part of the engagement.</p>"),
         ("Can you review my contracts?",
          "<p>We review and advise on financial terms — payment structure, deductions, accounting and audit rights, and termination consequences — and coordinate with your attorney on legal terms.</p>"),
         ("How is my money protected?",
          "<p>Through structure: accounts in your name, documented approval procedures, monthly reconciliation, and reporting you receive rather than request. An arrangement you cannot see into is the arrangement that fails.</p>")],
   related=[('tax-planning-preparation','Tax planning'),('asset-protection','Asset protection'),
            ('estate-trust-planning','Estate planning'),('../industries/entertainment-sports.html','Entertainment &amp; sports')]),

 dict(slug='employee-benefit-plans', ic='people', nav_title='Employee Benefit Plans',
   short='Profit sharing, 401(k), pension, Section 125, and deferred compensation plans — designed, evaluated, and kept compliant.',
   title='Employee Benefit & Retirement Plan Services | KPW CPAs Illinois',
   desc='Design and evaluation of profit sharing, 401(k), pension, Section 125, and deferred compensation plans for Illinois businesses, plus compliance support.',
   eyebrow='Benefit plans', h1='Retirement plans that do what the owner actually wanted.',
   sub='Profit sharing, 401(k), pension, Section 125, and deferred compensation arrangements — evaluated for cost, for what they accomplish, and for what they oblige you to maintain.',
   body='''
<h2>The short answer</h2>
<p>Compensation and benefit plan work is part of our management advisory practice: profit sharing plans, 401(k) plans, pension plans, Section 125 cafeteria plans, and deferred compensation arrangements. We help owners choose among them, understand the cost and the compliance obligations, and keep the plan aligned with what it was adopted to accomplish.</p>

<h2>Start with the objective</h2>
<p>Plan selection goes wrong when it starts with the product rather than the purpose. The right structure differs sharply depending on the answer to a simple question: what is this plan for?</p>
<ul>
<li><strong>Maximizing owner deferral.</strong> Points toward profit sharing with new comparability allocation, or a defined benefit or cash balance plan where the owner is older than the workforce and the cash flow can support a funding commitment.</li>
<li><strong>Recruiting and retention.</strong> Points toward a 401(k) with a competitive match and an employee experience that does not create friction.</li>
<li><strong>Rewarding a few key people.</strong> Points toward non-qualified deferred compensation, which escapes coverage testing at the cost of losing the deduction until payment and carrying real forfeiture risk for the executive.</li>
<li><strong>Reducing payroll taxes on benefits already provided.</strong> Points toward a Section 125 cafeteria plan, which lets employees pay premiums pre-tax and reduces employer payroll tax at modest cost.</li>
</ul>

<h2>The plan types</h2>
<h3>401(k) plans</h3>
<p>The default for most companies. The design decisions that matter are the match formula, whether to adopt a safe harbor provision to sidestep nondiscrimination testing, the vesting schedule, and automatic enrollment. Safe harbor is the usual answer for owner-heavy companies that would otherwise fail testing and be forced into corrective distributions.</p>
<h3>Profit sharing plans</h3>
<p>Discretionary employer contributions, which suits businesses with cyclical results. Allocation method is the lever: new comparability and age-weighted formulas can direct a substantially larger share to owners while satisfying the rules, when the demographics support it.</p>
<h3>Defined benefit and cash balance plans</h3>
<p>The largest deductible contributions available, and the most demanding. They create a funding obligation that persists through bad years, and they require actuarial work annually. Suited to consistently profitable companies with an older owner group and a genuine appetite for large deferrals.</p>
<h3>Section 125 cafeteria plans</h3>
<p>Pre-tax treatment for employee premium contributions and certain benefits, reducing employer payroll tax. Low cost, requires a written plan document, and is frequently missing at companies that already offer the underlying benefits.</p>
<h3>Deferred compensation</h3>
<p>Non-qualified arrangements for selected executives, outside the coverage rules but inside Section 409A — where the drafting and operational requirements are unforgiving and the penalties for failure fall on the employee.</p>

<h2>Compliance obligations</h2>
<p>Most qualified plans carry them: annual Form 5500 filing, nondiscrimination and coverage testing, timely deposit of employee deferrals, participant notices and disclosures, and a plan document that has been updated for statutory changes. (A one-participant plan below the filing threshold is the notable exception, and it has no testing population to speak of.) Larger plans reach an audit requirement based on participant count, which is a further reason plan design should account for eventual size.</p>

<div class="callout"><p><strong>Late deferral deposits are the most common failure we see.</strong> Employee contributions must be remitted as soon as they can reasonably be segregated from general assets. Delays are a prohibited transaction, are reportable, and are entirely avoidable with a fixed procedure.</p></div>

<h2>How this fits the rest of the plan</h2>
<p>Benefit plan choices interact with entity structure, owner compensation, and the overall tax picture — which is why this work belongs with the firm handling <a href="tax-planning-preparation.html">your tax planning</a> and <a href="business-advisory.html">advisory work</a> rather than in isolation.</p>
''',
   faqs=[("Which retirement plan is right for our company?",
          "<p>It depends on the objective, the owner-to-employee demographics, and how consistent your cash flow is. Maximizing owner deferral, recruiting, and rewarding a few key people each point to a different structure.</p>"),
         ("What is a safe harbor 401(k)?",
          "<p>A design that satisfies nondiscrimination testing automatically in exchange for a required employer contribution that vests immediately. It is the common solution for owner-heavy companies that would otherwise fail testing and have to refund owner deferrals.</p>"),
         ("When does a plan require an audit?",
          "<p>Plans reach an audit requirement based on participant count, so growing companies should anticipate the threshold rather than discover it at filing. If your plan is approaching that size, plan design and recordkeeping should be reviewed in advance.</p>"),
         ("How quickly must employee deferrals be deposited?",
          "<p>As soon as they can reasonably be segregated from the employer's general assets. Late deposits are a prohibited transaction and must be corrected and reported — the most common and most avoidable compliance failure we encounter.</p>")],
   related=[('business-advisory','Business advisory'),('tax-planning-preparation','Tax planning'),
            ('audit-assurance','Audit &amp; assurance'),('estate-trust-planning','Succession planning')]),
]

def _svc_page(s):
    d = 1
    url = BASE + 'services/' + s['slug'] + '.html'
    rel_links = ''
    for href, label in s['related']:
        h = href if href.startswith('..') or href.endswith('.html') else href+'.html'
        rel_links += '<li><a href="'+h+'"><span class="ck">&rarr;</span> '+label+'</a></li>'
    p = dict(path='services/'+s['slug']+'.html', depth=d, nav='services',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'])
    p['body'] = phero(p, [('Services','services/index.html'), (_plain(s['nav_title']), None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">'+s['body']+
      '<h2>Common questions</h2>'+faq_html(s['faqs'])+
      '</div>'
      '<div class="aside">'
      '<div class="acard"><div class="t">Talk to a partner</div>'
      '<p>Describe the situation and we will talk through what the engagement involves.</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a>'
      '</div>'
      '<div class="acard light"><div class="t">Related</div><ul>'+rel_links+'</ul></div>'
      '<div class="acard light"><div class="t">Why KPW</div><ul>'
      '<li><a href="../peer-review.html"><span class="ck">&#10003;</span> AICPA peer-reviewed practice</a></li>'
      '<li><span class="ck">&#10003;</span> Practicing in Illinois since 1974</li>'
      '<li><a href="../team/index.html"><span class="ck">&#10003;</span> Partner-led engagements</a></li>'
      '<li><span class="ck">&#10003;</span> Fair, transparent prices &mdash; no hidden fees</li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(),
      breadcrumb_schema([('Home',BASE),('Services',BASE+'services/'),(_plain(s['nav_title']),url)]),
      service_schema(_plain(s['nav_title']), _plain(s['short']), url),
      faq_schema([(q, _plain(a)) for q, a in s['faqs']])]
    return p

def pages():
    P = []
    # hub
    cards = ''
    for i, s in enumerate(SERVICES):
        cards += ('<a class="card reveal" href="'+s['slug']+'.html"><span class="num">'+('0'+str(i+1))[-2:]+'</span>'
                  '<div class="cic">'+icon(s['ic'])+'</div><h3>'+s['nav_title']+'</h3><p>'+s['short']+'</p>'
                  '<span class="more">Read more '+ARROW+'</span></a>')
    p = dict(path='services/index.html', depth=1, nav='services',
      title='Services | Tax, Audit, Valuation & Advisory | KPW CPAs Illinois',
      desc='Twelve practice areas from an Illinois CPA firm founded in 1974 — tax, audit and assurance, accounting, advisory, valuation, estate planning, litigation support, and M&A.',
      eyebrow='Services', h1='Twelve practice areas. One firm that connects them.',
      sub='Most of what a closely held business needs from an accountant touches more than one of these. Handling them under one roof is the point.')
    p['body'] = phero(p, [('Services', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>What we do</h2>'
      '<p class="lead">KPW specializes in the needs of privately owned businesses and their owners, and brings the same standard to the governmental and non-profit organizations we audit. Fair and transparent prices, with no hidden fees or extra charges.</p></div>'
      '<div class="cards">'+cards+'</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Why the connections matter</h2>'
      '<p>A closely held business rarely has an isolated problem. The owner planning a sale needs a valuation, a tax structure, diligence support, and an estate plan that accounts for the proceeds. The company adding a retirement plan needs benefit plan design, a tax analysis, and eventually a plan audit. The organization whose lender changed a covenant needs a different level of financial statement service and a conversation about what changed.</p>'
      '<p>Firms that specialize in one of these hand you off for the rest. We do not, and after fifty-two years the connections are where most of the value shows up.</p>'
      '<h3>Strengths we would point to</h3>'
      '<ul>'
      '<li>Decades of experience with the specific financial and reporting requirements of privately owned businesses</li>'
      '<li>Governmental and non-profit audit specialization at the partner level</li>'
      '<li>An <a href="business-valuation.html">AICPA-accredited business valuation</a> capability inside the firm</li>'
      '<li>Litigation support and expert witness work for law firms</li>'
      '<li>Membership in the American Institute of Certified Public Accountants and the Illinois CPA Society</li>'
      '<li>A practice enrolled in the <a href="../peer-review.html">AICPA peer review program</a></li>'
      '</ul>'
      ''
      '</div><div class="aside"><div class="acard"><div class="t">Not sure where you fit?</div>'
      '<p>Most first calls take ten minutes and end with a clear answer about what the work involves. Call the office.</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a></div>'
      '<div class="acard light"><div class="t">Industries</div><ul>'
      '<li><a href="../industries/privately-held-businesses.html"><span class="ck">&rarr;</span> Privately held businesses</a></li>'
      '<li><a href="../industries/government-nonprofit.html"><span class="ck">&rarr;</span> Government &amp; non-profit</a></li>'
      '<li><a href="../industries/entertainment-sports.html"><span class="ck">&rarr;</span> Entertainment &amp; sports</a></li>'
      '<li><a href="../industries/real-estate-construction.html"><span class="ck">&rarr;</span> Real estate &amp; construction</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home',BASE),('Services',BASE+'services/')]),
      {"@context":"https://schema.org","@type":"ItemList","name":"KPW services","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":_plain(s['nav_title']),"url":BASE+'services/'+s['slug']+'.html'}
        for i,s in enumerate(SERVICES)]}]
    P.append(p)
    for s in SERVICES:
        P.append(_svc_page(s))
    return P
