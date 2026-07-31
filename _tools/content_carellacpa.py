# -*- coding: utf-8 -*-
"""
All pages for Charles M. Carella, CPA — North Billerica, Massachusetts.

Editorial rule for this build: the firm’s published material names no person, gives
no founding date, no headcount, no memberships and no specialism, so none of those
appear here. The site is written about the work instead of about a biography. Where
this file makes a first-person statement, it is either (a) one of the four services
the firm’s own site lists, or (b) an obligation that already binds every paid
preparer and every CPA — signature and copy requirements, the e-file authorization,
confidentiality. Everything else is written in the informational register: what the
work involves, what to have ready, what the deadlines are.

The engine’s shared org_schema()/service_schema() helpers are deliberately NOT used:
they assert a founding date, professional memberships and fixed opening hours, none
of which this firm publishes. Local equivalents are defined below.
"""
import html, re
from build import (FIRM, BASE, T, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   breadcrumb_schema, faq_schema)
import calculators as C

ORG_ID = BASE + '#firm'
TEL = FIRM['tel']
PH = FIRM['ph']


def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()


def _org():
    """Organization schema containing only what the firm publishes about itself.
    No foundingDate, no memberOf, no openingHours, no priceRange, no areaServed."""
    return {"@context": "https://schema.org", "@type": "AccountingService", "@id": ORG_ID,
            "name": FIRM['name'], "url": BASE, "email": FIRM['email'],
            "telephone": PH, "faxNumber": FIRM['fax'],
            "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                        "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                        "postalCode": FIRM['zip'], "addressCountry": "US"},
            "hasMap": FIRM['maps']}


def _svc_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "description": desc, "url": url, "serviceType": name,
            "provider": {"@id": ORG_ID}}


def _card(d, href, ic, title, text, num=None):
    return ('<a class="card reveal" href="' + rel(d, href) + '">'
            + ('<span class="num">' + num + '</span>' if num else '')
            + '<div class="cic">' + icon(ic) + '</div><h3>' + title + '</h3><p>' + text + '</p>'
            '<span class="more">Read more ' + ARROW + '</span></a>')


CALL_CARD = ('<div class="acard"><div class="t">Call the office</div>'
             '<p>Describe the situation in a couple of minutes and you will get a straight answer '
             'about what the work involves.</p>'
             '<a class="btn b-acc" href="tel:' + TEL + '">' + PH + '</a></div>')


# ===========================================================================
# SERVICES — exactly the four the firm’s own Client Services page lists.
# ===========================================================================
SERVICES = [
 dict(slug='tax-preparation-planning', ic='calc',
   nav_title='Tax Preparation &amp; Planning',
   short='Federal and Massachusetts returns for individuals and small businesses &mdash; and the conversations that have to happen before the year closes.',
   title='Tax Preparation & Planning | Charles M. Carella, CPA',
   desc='Federal and Massachusetts income tax preparation and planning for individuals and small businesses, from a CPA office at 330 Boston Road in North Billerica.',
   eyebrow='Tax', h1='A return is a record. The planning happens earlier.',
   sub='Income tax preparation and planning for individuals and for the small businesses they own, federal and Massachusetts.',
   body='''
<h2>What this covers</h2>
<p>Preparation of federal and Massachusetts income tax returns for individuals and small businesses, and the planning work that sits in front of them. Those two halves are usually sold as one service and treated as one job. They are not. Preparation records decisions that have already been made. Planning is the part where the decisions are still open.</p>

<h2>Why the calendar decides most of it</h2>
<p>By the time a return is being prepared, the year is closed and the arithmetic is fixed. Nearly everything that moves the number happened months earlier: how the business is organized, what the owner took as wages against distributions, when equipment was bought and how it was paid for, whether a retirement plan contribution was made, how a property sale was structured, which state the work was performed in.</p>
<p>Some of it can still be adjusted after year end &mdash; a self-employed retirement plan contribution, an IRA, an accounting method question. Most of it cannot. That is the argument for a conversation in the autumn rather than a scramble in April.</p>

<h2>Individual returns</h2>
<p>A straightforward wage return is straightforward. Returns stop being straightforward at fairly predictable points: a first year of self-employment or 1099 income, a house bought or sold, equity compensation, a rental unit, an inheritance, a move across a state line, a year with two states in it, marriage, divorce, a child in college, retirement account withdrawals starting.</p>
<p>Each of those changes what has to be reported and what can be claimed, and each of them is a reason to raise the question before the year ends rather than after.</p>

<h3>Massachusetts, specifically</h3>
<p>The state return is not a copy of the federal one, and the differences catch people out:</p>
<ul>
<li>Massachusetts taxes most income &mdash; wages, interest, dividends, long-term capital gains &mdash; at a flat 5%. Short-term capital gains are taxed at a higher rate of their own.</li>
<li>A 4% surtax applies to taxable income above a threshold near one million dollars, adjusted annually. It reaches one-off events, so the year you sell a business or a building is the year to check it.</li>
<li>There is no state standard deduction. Massachusetts uses personal exemptions and its own list of deductions instead, which is why federal and state taxable income rarely match.</li>
<li>Residents file Form 1; part-year residents and non-residents file Form 1-NR/PY. If you moved during the year, or you live in one state and work in another, the apportionment is the whole exercise.</li>
<li>Massachusetts does not follow the federal bonus-depreciation rules. A purchase that produces a large federal deduction may produce a much smaller state one, and the two sets of books diverge from that point on.</li>
</ul>

<h2>Small business returns</h2>
<p>How a business is organized decides which return it files, when it is due, and how the profit reaches the owner’s personal return. A sole proprietorship or single-member LLC reports on Schedule C inside the owner’s Form 1040. A partnership or multi-member LLC files its own return and issues a Schedule K-1 to each partner. An S corporation files its own return, issues K-1s, and adds the question of reasonable compensation for any owner who works in the business. A C corporation is taxed in its own right and owes a Massachusetts corporate excise even in a year it loses money.</p>
<p>Those returns are due on different dates, and the entity return has to be finished before the owner’s personal return can be. A business return filed late is expensive in a way an individual return is not: the penalty is charged per owner, per month.</p>

<h2>Estimated tax</h2>
<p>Income that arrives without withholding &mdash; self-employment profit, K-1 income, investment income, a large capital gain &mdash; carries an obligation to pay in quarterly. The federal installments are due in April, June, September and January; Massachusetts uses the same schedule on Form 1-ES.</p>
<p>The underpayment penalty is not a fine for owing money at filing. It is interest charged for paying late in the year, and it can be avoided even in a year of unexpected income by paying in at least what last year’s tax was &mdash; a higher percentage of it if your income is above the threshold in the rule. That safe harbor is the single most useful thing to know about estimates, and it is worth checking in the autumn rather than in January.</p>

<div class="callout"><p><strong>An extension buys time to file, not time to pay.</strong> The federal extension moves the filing deadline to October and nothing else; interest and penalties run on any unpaid balance from the original due date. Massachusetts grants an automatic extension only if enough of the year’s tax has already been paid &mdash; miss that and the extension is void, with a late-filing penalty on top.</p></div>

<h2>Notices and prior years</h2>
<p>A letter from the IRS or the Massachusetts Department of Revenue is a starting point, not a verdict. Some are wrong. Many are answered with a single letter and a document. Almost all of them have a deadline printed on them, and the deadline is the part that matters &mdash; a notice that is ignored becomes an assessment.</p>
<p>Unfiled years work the same way. They are more common than most people assume, and the situation only compounds while it is left alone. Say so plainly on the first call; it changes what the work looks like but not whether it can be done.</p>

<h2>What is on your side of the job</h2>
<p>The quality of a return is mostly decided by the completeness of what it is built from. Complete records shorten the work, reduce the questions, and lower the chance of an amendment later. The <a href="../about.html#bring">list of what to gather</a> covers the usual case; anything unusual about your year is worth mentioning at the start rather than being discovered at the end.</p>
''',
   faqs=[("When should I call about planning rather than preparation?",
          "<p>Before the year closes, and before the transaction if there is one. Selling a property, buying equipment, changing how the business is organized, taking a large distribution, exercising options &mdash; all of those have a better and a worse version, and the choice closes on 31 December. Planning after year end is limited to a short list: certain retirement contributions, an IRA, and a few accounting method questions.</p>"),
         ("Do you prepare both the business return and the owner’s personal return?",
          "<p>Tax preparation and planning for individuals and small businesses is what this office does, and for an owner-operated business the two returns are one problem. The entity return produces the K-1 or the Schedule C figure that the personal return depends on, so the entity return has to be finished first.</p>"),
         ("I have income with no tax withheld. How much should I be paying in?",
          "<p>Enough to land inside the safe harbor. Paying in at least the amount of last year’s total tax &mdash; a higher percentage of it above an income threshold &mdash; avoids the underpayment penalty regardless of what this year turns out to be. The <a href=\"../calculators/self-employment-tax.html\">self-employment tax calculator</a> gives you the Social Security and Medicare half of the estimate; income tax sits on top of it.</p>"),
         ("What happens if I cannot pay what I owe?",
          "<p>File anyway. The penalty for filing late is several times the penalty for paying late, so a return filed on time with a partial payment costs far less than a return held back until the money is there. Both the IRS and the Massachusetts Department of Revenue have installment arrangements; both are easier to arrange before the balance is in collection.</p>")],
   related=[('accounting-bookkeeping', 'Accounting &amp; bookkeeping'),
            ('business-consulting', 'Business consulting'),
            ('../calculators/self-employment-tax.html', 'Self-employment tax calculator'),
            ('../faq.html', 'Common questions')]),

 dict(slug='accounting-bookkeeping', ic='ledger',
   nav_title='Accounting &amp; Bookkeeping',
   short='The monthly discipline underneath everything else &mdash; a chart of accounts that fits the business, accounts that reconcile, and a set of books that can be relied on.',
   title='Accounting & Bookkeeping | Charles M. Carella, CPA',
   desc='Accounting and bookkeeping for small businesses in Massachusetts: chart of accounts, monthly reconciliation, and books that hold up at tax time. North Billerica, MA.',
   eyebrow='Accounting', h1='Books that are right cost less than books that get fixed.',
   sub='Accounting and bookkeeping for small businesses &mdash; the monthly work that every other number on this site depends on.',
   body='''
<h2>What this covers</h2>
<p>Accounting and bookkeeping for small businesses: setting up or repairing a chart of accounts, recording activity, reconciling accounts, and producing figures at the end of each period that mean what they say.</p>

<h2>What bookkeeping actually buys</h2>
<p>Bookkeeping is usually described as a compliance chore &mdash; something done because the tax return needs it. That is the least valuable thing it does.</p>
<p>A set of books that reconciles every month tells you which jobs make money and which ones only look busy, whether the business is generating cash or borrowing against next month, when receivables are drifting, and what a slow quarter actually costs. None of that is visible from a bank balance. A bank balance tells you what has already happened to the cash; the books tell you what is about to.</p>
<p>The other thing it buys is optionality. A business with three years of clean books can apply for a loan, take on an investor, price itself for sale, or answer a state notice. A business without them can do none of those quickly, and the cost of reconstructing the history always exceeds the cost of having kept it.</p>

<h2>The chart of accounts is the whole design</h2>
<p>Most bookkeeping problems are really chart-of-accounts problems. The default chart that comes with accounting software is designed to suit everyone, which means it suits nobody: too many accounts in places that do not matter, one undifferentiated bucket where the business actually makes its decisions.</p>
<p>A chart that fits the business separates the things you would want to compare and combines the things you would not. It puts direct costs where they can be read against revenue instead of scattering them through overhead. It gives the two or three lines you actually manage their own place. Getting it right early is cheap; changing it after four years of history is not, because every comparison to a prior year has to be restated.</p>

<h2>The monthly cycle</h2>
<p>The work is not complicated, but it is unforgiving about being skipped:</p>
<ul>
<li><strong>Reconcile every account with an outside statement.</strong> Bank accounts, credit cards, loans, merchant processors, payroll clearing. An account that has not been reconciled is not evidence of anything.</li>
<li><strong>Code the activity properly rather than plausibly.</strong> Software will suggest a category based on the vendor name. It is right often enough to be dangerous.</li>
<li><strong>Deal with the awkward items rather than parking them.</strong> An <em>Ask My Accountant</em> account with forty entries in it is a decision that has been deferred twelve times.</li>
<li><strong>Look at the result.</strong> A profit and loss compared to the prior month and the same month last year takes five minutes to read and catches most errors before they compound.</li>
</ul>

<h2>The failures that come up again and again</h2>
<h3>Personal and business money in one account</h3>
<p>It makes every subsequent step harder, it obscures what the business actually earns, and for a company or LLC it weakens the separation that the entity exists to provide in the first place. A separate account and a separate card cost nothing and solve it permanently.</p>
<h3>Owner draws recorded as expenses</h3>
<p>Money an owner takes out of a sole proprietorship or a partnership is a draw against equity, not a deductible cost. Recorded as an expense it understates profit, which is pleasant right up to the point a lender, a buyer or an examiner reads the statements.</p>
<h3>Sales tax treated as revenue</h3>
<p>Massachusetts sales tax collected from a customer never belonged to the business. It is money held on the state’s behalf until it is remitted. Booked as income it inflates revenue and hides a liability that is already accruing.</p>
<h3>Payroll recorded from the net</h3>
<p>Recording only the amount that left the bank omits the withholding and the employer’s own share. The wage deduction ends up understated and the payroll liability accounts never clear.</p>
<h3>Reconciliations that are forced</h3>
<p>An adjustment entered to make a reconciliation balance does not fix anything; it moves the discrepancy somewhere it will be harder to find. The forced entries are usually what makes a year of books take three days to unpick instead of three hours.</p>

<div class="callout"><p><strong>Books and the tax return are one job in two parts.</strong> Every hour spent reconstructing a year at filing time is an hour billed at filing time, under a deadline, with worse information. It is the most expensive way to buy bookkeeping.</p></div>

<h2>Records, and how long to keep them</h2>
<p>The general rule is three years from filing, because that is the ordinary window in which a return can be examined. It stretches to six years where income has been substantially understated, and there is no limit at all on a year that was never filed. Employment tax records, property and improvement records, and anything establishing the cost basis of an asset should outlive that schedule &mdash; basis records need to survive until the asset is sold, which can be decades.</p>

<h2>Where this leads</h2>
<p>Reconciled books are the input to <a href="financial-statements.html">financial statement preparation</a> and to <a href="tax-preparation-planning.html">the tax return</a>, and they are the precondition for any <a href="business-consulting.html">useful conversation about the business</a>. Nothing downstream is better than the books it came from.</p>
''',
   faqs=[("We do our own bookkeeping. Is that a problem?",
          "<p>Not in itself. Plenty of small businesses keep their own books perfectly well. What matters is whether the accounts reconcile to outside statements every month, whether the chart of accounts reflects how the business actually works, and whether anything unresolved has been parked rather than answered. Those three things are worth a review even if nothing else changes.</p>"),
         ("How far behind is too far behind?",
          "<p>There is no point at which it becomes impossible, only points at which it becomes more expensive. Bank and card statements can be obtained, and a year can be rebuilt from them. What cannot be recovered is the memory of what an unexplained transaction was for, which is why the cost rises with age rather than with volume.</p>"),
         ("Which accounting software should we use?",
          "<p>Almost any of the mainstream small-business packages will do the job. The choice matters far less than the chart of accounts inside it and the discipline of reconciling monthly. Software does not produce good books; it produces fast books, in whatever condition the inputs put them.</p>"),
         ("What is the difference between bookkeeping and accounting?",
          "<p>Bookkeeping is the recording: capturing transactions, coding them, reconciling the accounts. Accounting is what is done with the result &mdash; period-end adjustments, depreciation, accruals, and presenting the figures so they can be read and relied on. The same records support both, which is why the recording standard determines everything above it.</p>")],
   related=[('financial-statements', 'Financial statements'),
            ('tax-preparation-planning', 'Tax preparation &amp; planning'),
            ('business-consulting', 'Business consulting'),
            ('../calculators/break-even.html', 'Break-even calculator')]),

 dict(slug='financial-statements', ic='doc',
   nav_title='Financial Statement Preparation',
   short='Statements a lender, a landlord, a bonding company or an owner can read &mdash; and a clear answer about which level of service the request actually requires.',
   title='Financial Statement Preparation | Charles M. Carella, CPA',
   desc='Financial statement preparation for small businesses in Massachusetts, plus a plain explanation of the four levels of service and which one a lender is really asking for.',
   eyebrow='Reporting', h1='Find out which level of service you are being asked for.',
   sub='Financial statement preparation for small businesses &mdash; and the conversation that should happen before you sign anything requiring a particular kind of report.',
   body='''
<h2>What this covers</h2>
<p>Preparation of financial statements for small businesses: a balance sheet, an income statement, and the supporting detail, built from the books and presented so that somebody outside the business can read them.</p>

<h2>Four different things share one name</h2>
<p>When a lender, a landlord, a bonding company or a buyer asks for “financial statements”, they may mean any of four levels of service. They differ enormously in what the accountant does and in what the recipient is entitled to rely on, and it is worth knowing which one is being asked for before agreeing to produce it.</p>

<table class="plain">
<tr><th>Level</th><th>What the accountant does</th><th>What the reader gets</th></tr>
<tr><td><strong>Preparation</strong></td><td>Assembles statements from the client’s records under professional standards.</td><td>Statements, with no report attached and no assurance offered. Each page says so.</td></tr>
<tr><td><strong>Compilation</strong></td><td>The same assembly, plus a reading of the statements for obvious problems, plus a signed report.</td><td>A report from the accountant. Still no assurance &mdash; the accountant does not verify the figures.</td></tr>
<tr><td><strong>Review</strong></td><td>Analytical procedures and inquiry of management. Substantially narrower than an audit.</td><td>Limited assurance: nothing came to the accountant’s attention suggesting material misstatement.</td></tr>
<tr><td><strong>Audit</strong></td><td>Risk assessment, testing, third-party confirmation, evaluation of internal control.</td><td>An opinion. Reasonable assurance that the statements are free of material misstatement.</td></tr>
</table>

<p>The cost difference between the top and the bottom of that table is large &mdash; a multiple, not a percentage. So is the difference in what is required from you.</p>

<h2>Who decides which one you need</h2>
<p>Almost always somebody else. A loan agreement, a line-of-credit covenant, a bonding requirement, a franchise agreement, a lease, a grant, a state licensing body, or a company’s own operating agreement will name a level of service, and that requirement drives the engagement.</p>
<p>Two things are worth doing about that. First, read the clause before signing it: the difference between “reviewed” and “audited” in a covenant is a real annual cost for as long as the agreement runs, and it is frequently negotiable at the outset and never afterwards. Second, if the request came verbally, ask which level is meant. Requests for “audited statements” are often satisfied by something considerably less.</p>
<p>If nothing external requires anything, the honest answer is usually that you need less than you have been told.</p>

<div class="callout"><p><strong>Independence is part of the answer.</strong> Assurance work &mdash; a review or an audit &mdash; must be performed by an accountant who is independent of the business. An accountant who keeps the books ordinarily cannot also provide assurance on them. That constraint sometimes decides who does what, and it is better understood at the start than discovered at the deadline.</p></div>

<h2>What the statements themselves say</h2>
<h3>The balance sheet</h3>
<p>A position at one instant: what the business owns, what it owes, and what is left. Read it for the relationship between current assets and current liabilities, for how much of the business is financed by debt, and for the two accounts that hide the most trouble &mdash; receivables that are ageing and inventory that is not moving.</p>
<h3>The income statement</h3>
<p>Performance across a period. The useful reading is never the bottom line on its own but the shape above it: gross margin, and whether it is holding; which costs move with revenue and which do not; and the comparison against the same period last year rather than against the month before.</p>
<h3>Cash flow</h3>
<p>Profit is an opinion about timing. Cash is a fact. A growing business is perfectly capable of being profitable and insolvent at the same time, because growth consumes cash before it produces any &mdash; inventory bought, wages paid, invoices outstanding. The statement that reconciles profit to cash movement is the one that explains where the money went.</p>

<h2>What lenders actually look at</h2>
<p>Not the statements alone. A lender reads them against the debt service they are being asked to support, checks the covenants they intend to impose, compares the figures to the tax returns, and looks at whether the equity account moves in a way the drawings explain. Statements that agree with the returns, and drawings that are recorded as drawings, remove most of the friction from that process before it starts.</p>

<h2>What has to be true first</h2>
<p>Statements are only as good as the records under them. Reconciled accounts, a chart of accounts that separates what matters, and no unresolved items are the precondition &mdash; see <a href="accounting-bookkeeping.html">accounting and bookkeeping</a>. Statements produced from books that do not reconcile are an expensive way of formatting a guess.</p>
''',
   faqs=[("Our bank asked for financial statements. What do they mean?",
          "<p>Ask them. The word covers four different levels of service with very different costs, and lenders frequently ask for more than their own policy requires. Get the requirement in writing, ideally from the loan document rather than from the conversation, before anyone starts work.</p>"),
         ("Can we just use the tax return instead?",
          "<p>Sometimes, and it is always worth asking. A tax return is prepared under tax rules rather than accounting rules, so the figures legitimately differ &mdash; depreciation is the usual culprit. Many small-business lending decisions are made on returns alone. Where statements are genuinely required, the two should still agree with each other in every place they can.</p>"),
         ("How often should we produce statements?",
          "<p>For internal use, monthly, because that is the frequency at which a problem is still small. For outside recipients, whatever the agreement requires &mdash; typically annually, sometimes quarterly for a business under covenants.</p>"),
         ("What does “no assurance is provided” mean on a statement?",
          "<p>That the accountant assembled the statements from records supplied by the business and did not verify them. It is a statement of scope, not a warning about the figures. Statements at that level are entirely appropriate for internal management and for many outside purposes; they are not the same thing as an audited statement and are not priced like one.</p>")],
   related=[('accounting-bookkeeping', 'Accounting &amp; bookkeeping'),
            ('business-consulting', 'Business consulting'),
            ('tax-preparation-planning', 'Tax preparation &amp; planning'),
            ('../calculators/loan-payment.html', 'Loan payment calculator')]),

 dict(slug='business-consulting', ic='chart',
   nav_title='Business Consulting',
   short='The questions that come up between filings &mdash; how to organize, what a hire really costs, whether to buy the equipment, and what the numbers are actually telling you.',
   title='Business Consulting | Charles M. Carella, CPA',
   desc='Business consulting for small businesses in Massachusetts: entity choice, pricing and break-even, cash flow, hiring costs, and equipment decisions. North Billerica, MA.',
   eyebrow='Advisory', h1='The decisions that matter are made between filings.',
   sub='Business consulting for small businesses &mdash; entity choice, pricing, cash flow, hiring, and the purchases that look affordable until you model them.',
   body='''
<h2>What this covers</h2>
<p>Business consulting for small businesses: the operating and structural questions that arise during the year and do not wait for a filing deadline.</p>

<h2>How the business is organized</h2>
<p>Entity choice gets treated as a one-off decision made at the start and never revisited. It should be revisited, because the answer changes as the business does.</p>
<p>A sole proprietorship is the default and costs nothing to maintain, but every dollar of profit carries self-employment tax and there is no separation between the business and the person. An LLC adds that separation and, in Massachusetts, an annual filing fee that is not trivial for a very small business. Electing S corporation treatment can reduce self-employment tax on the portion of profit taken as a distribution rather than as wages &mdash; but only if the owner is paid reasonable compensation first, only above a certain level of profit, and only against the added cost of payroll, a separate return and more bookkeeping.</p>
<p>The right answer depends on profit, on how many owners there are, on whether outside investment or a sale is plausible, and on how much administration the business can absorb. It is arithmetic, not preference, and it is worth redoing when profit changes materially.</p>

<h2>Pricing and break-even</h2>
<p>Most small businesses under-price, and most of them discover it by working harder without earning more.</p>
<p>The number that matters is contribution margin: what is left from a sale after the costs that only exist because the sale happened. Fixed costs are then paid out of the accumulated contribution, and the point at which they are covered is break-even. Two consequences follow, and they are not intuitive. A modest price increase moves break-even far more than the same percentage cut in costs, because the whole increase lands in the margin. And a low-margin business needs a great deal more volume to absorb a fixed cost increase &mdash; which is why adding a person or a unit can be safe for one business and fatal for another with the same revenue.</p>
<p>The <a href="../calculators/break-even.html">break-even calculator</a> on this site does the arithmetic for a single line of business.</p>

<h2>Cash, and why profitable businesses run out of it</h2>
<p>Growth consumes cash. Inventory is bought before it is sold, wages are paid before the work is invoiced, and invoices are paid on the customer’s schedule rather than yours. The gap between paying and being paid is a working capital requirement, and it grows in proportion to sales &mdash; so the faster a business grows, the more of it needs funding.</p>
<p>The practical levers are deposits and progress billing, invoicing on the day work is finished instead of at month end, terms that are actually enforced, and inventory that is bought against demand rather than against a discount. A short cash projection &mdash; thirteen weeks is the conventional horizon &mdash; converts all of that from an anxiety into a schedule.</p>

<h2>What a hire really costs</h2>
<p>The wage is roughly two thirds of it. On top sits the employer’s share of Social Security and Medicare, federal and Massachusetts unemployment insurance, workers’ compensation, the Massachusetts paid family and medical leave contribution, any benefits, and the payroll administration itself. Then there is the part that never appears in a budget: the time spent training somebody, and the productivity that is lost while it happens.</p>
<p>The other question is whether the role is an employee at all. The distinction between an employee and an independent contractor is not a matter of what the parties agree; Massachusetts applies a strict test of its own, stricter than the federal one, and getting it wrong is expensive in back taxes, penalties and unpaid wage claims. It is worth settling before the first payment, not after.</p>

<h2>Equipment, vehicles and the purchases that look like tax savings</h2>
<p>A deduction is not a rebate. Spending a dollar to save thirty cents of tax leaves you seventy cents down, which is fine if the asset earns its keep and a poor decision if it was bought for the deduction. The order of the questions is: does the business need it, can the cash or the financing be carried, and only then, how is it treated for tax.</p>
<p>The treatment itself is worth modeling rather than assuming. Immediate expensing and bonus depreciation are limited by rules that change, a deduction is worth only your marginal rate, an immediate deduction cannot create a loss in some cases, and Massachusetts does not follow the federal bonus-depreciation rules at all. The <a href="../calculators/section-179.html">equipment purchase calculator</a> shows what a deduction is worth against a given rate and what the asset actually costs after it.</p>

<div class="callout"><p><strong>The cheapest advice is early advice.</strong> Almost every expensive problem in a small business was cheap at the point it was a question &mdash; the lease that was signed, the contractor who should have been an employee, the covenant nobody read, the equipment bought in December. None of those are fixable afterwards at anything like the cost of asking first.</p></div>

<h2>Reading your own numbers</h2>
<p>A small business does not need a dashboard. It needs three or four figures that are looked at on a schedule: gross margin against last year, cash and the thirteen-week projection, receivables over sixty days, and whatever the single operational number is that drives the business &mdash; utilization, occupancy, jobs closed, average ticket. Everything else is commentary.</p>
''',
   faqs=[("Should we become an S corporation?",
          "<p>It depends on profit, on what reasonable compensation for the owner’s role would be, and on whether the business can carry payroll, a separate return and tighter bookkeeping. Below a certain level of profit the added cost exceeds the saving. Above it the saving can be substantial. It is worth calculating rather than assuming, and worth recalculating when profit changes materially.</p>"),
         ("Is buying equipment before year end a good way to reduce tax?",
          "<p>Only if the equipment is needed. A deduction returns your marginal rate, so the purchase still costs most of its price in cash. Buying an asset you would have bought anyway, slightly earlier, is sound. Buying one you would not have bought is spending a dollar to save a fraction of it.</p>"),
         ("How do I know whether to raise prices?",
          "<p>Start from contribution margin rather than from what competitors charge. A price rise lands entirely in the margin, so a small one moves break-even further than a large cost saving. The real question is usually how much volume you can afford to lose at the new price &mdash; and the answer is often more than expected.</p>"),
         ("Can we treat this person as a contractor?",
          "<p>Massachusetts applies its own test and it is strict &mdash; stricter than the federal rules, and it does not care what the written agreement says. Misclassification is corrected with back employment taxes, penalties and potential wage claims. Settle the question before the first payment.</p>")],
   related=[('tax-preparation-planning', 'Tax preparation &amp; planning'),
            ('accounting-bookkeeping', 'Accounting &amp; bookkeeping'),
            ('financial-statements', 'Financial statements'),
            ('../calculators/index.html', 'All calculators')]),
]


# ===========================================================================
# QUESTIONS
# ===========================================================================
HOME_FAQS = [
 ("What does a CPA do that other tax preparers do not?",
  "<p>Anyone with a preparer tax identification number may prepare a return for a fee. A Certified Public Accountant has passed the Uniform CPA Examination and holds an active state license, which carries continuing education requirements and a professional code of conduct with enforcement behind it.</p><p>The practical difference shows up in two places. A CPA has unlimited rights to represent a taxpayer before the IRS &mdash; in an examination, in collection, on appeal &mdash; which most preparers do not. And a CPA can work across the whole picture rather than the return alone: the books that feed it, the statements a lender wants, and the structural questions that decide next year’s number.</p>"),
 ("Do you work with businesses as well as individuals?",
  "<p>Both. This office prepares returns and plans for individuals and for small businesses, and does the accounting and bookkeeping, financial statement preparation and business consulting behind them. For an owner-operated business that combination is the point: the entity return, the owner’s return and the books are one problem seen from three sides.</p>"),
 ("What does it cost?",
  "<p>There is no published fee schedule, because the work is not uniform. What a return or an engagement takes depends on how many moving parts there are and on the condition of the records it is built from &mdash; which is why the useful first step is a short call describing the situation rather than a price list. Call <a href=\"tel:" + TEL + "\">" + PH + "</a> and describe what you have.</p>"),
 ("What should I bring to the first appointment?",
  "<p>Last year’s return, this year’s income documents, and anything that changed. The <a href=\"about.html#bring\">full list is here</a>, but the general rule is that more is better and gaps are worth mentioning rather than working around. If something is missing, say so at the start &mdash; it usually changes the order of the work rather than whether it can be done.</p>"),
 ("How do I get my documents to the office?",
  "<p>Call the office and ask. Which route makes sense depends on what you have and what form it is in, and it is a two-minute conversation rather than something worth guessing at. The office is at 330 Boston Road, Suite 12, in North Billerica.</p>"),
]

MORE_FAQS = [
 ("Is it too late to do anything about this year?",
  "<p>It depends what month it is. Before 31 December, most things are still open &mdash; the timing of income and purchases, retirement plan contributions, how a transaction is structured, whether an entity election makes sense. After 31 December the list shortens to a handful of items: certain self-employed retirement contributions, an IRA, and a few accounting method questions. That is the argument for an autumn conversation.</p>"),
 ("I have not filed for a few years. What happens now?",
  "<p>It is a more common situation than people assume, and it does not improve while it is left. There is no time limit on assessing a year that was never filed, and the penalties for failing to file are considerably heavier than those for failing to pay. Say it plainly on the first call. Unfiled years change what the work looks like &mdash; usually oldest first, using transcripts to reconstruct what was reported to the agencies &mdash; but not whether it can be done.</p>"),
 ("I got a letter from the IRS. Do I need to panic?",
  "<p>No, but you do need to read the date on it. Most notices are automated, some are simply wrong, and many are resolved with one letter and a document. What turns a notice into a real problem is letting the response window close, because an unanswered proposal becomes an assessment. Send the notice on before responding to it.</p><p>CPAs hold unlimited representation rights before the IRS. Whether representation forms part of your engagement is something to agree with the office.</p>"),
 ("I moved into or out of Massachusetts this year. Which return do I file?",
  "<p>A part-year resident files Massachusetts Form 1-NR/PY and reports income earned while resident, plus Massachusetts-source income from the rest of the year. If you also worked in another state, both states may tax the same income, and a credit mechanism is meant to prevent that being paid twice. It is worth getting right; it is one of the more common sources of an amended return.</p>"),
 ("Does an extension give me more time to pay?",
  "<p>No. A federal extension moves the filing deadline to October and does nothing about the balance &mdash; interest and penalties run from the original due date. Massachusetts is stricter still: its extension is automatic only if enough of the year’s tax has already been paid, and if that condition is not met the extension is void and a late-filing penalty applies on top.</p>"),
 ("Do I have to sign anything before my return is filed?",
  "<p>Yes. A return that is filed electronically requires a signed authorization from the taxpayer first &mdash; that is a rule, not a courtesy, and it exists so that nothing is transmitted before you have seen it. A paid preparer must also sign the return and give you a complete copy of it. Keep that copy; it is the starting point for next year and for anything that arises later.</p>"),
 ("How long should I keep my records?",
  "<p>Three years from filing covers the ordinary examination window. Six years is the safer figure where income might have been substantially understated, and there is no limit at all on a year that was never filed. Some records outlive all of that: anything establishing the cost basis of an asset should be kept until the asset is sold and the gain reported, which for a house or a business interest can mean decades.</p>"),
 ("Can I do my own bookkeeping and have you handle the return?",
  "<p>Yes, and many small businesses do exactly that. What determines whether it works is the state of the books rather than who keeps them: accounts that reconcile to outside statements, a chart of accounts that reflects the business, and nothing significant parked in a suspense account. A review of the books at the start of the engagement is usually cheaper than the alternative, which is discovering the problems while a deadline is running.</p>"),
 ("Are my records confidential?",
  "<p>Yes. Confidentiality is a professional obligation for a CPA rather than an internal policy, and it is enforceable as one. Separately, federal law restricts what a tax preparer may do with information supplied for the preparation of a return, including disclosing it to anyone else, without the taxpayer’s written consent.</p>"),
 ("Are the calculators on this site giving me tax advice?",
  "<p>No. They are estimating tools that run entirely in your browser, using assumptions you can see and change. Rates, thresholds and contribution limits change every year, and none of them account for your filing status, your state position or anything else on your return. Use them to size a question and then call about the answer.</p>"),
]

ALL_FAQS = HOME_FAQS + MORE_FAQS


# ===========================================================================
# CALCULATOR PAGE METADATA
# ===========================================================================
CALC_META = {
 'mortgage-payment': ('Mortgage Payment Calculator | Charles M. Carella, CPA',
   'Estimate a monthly mortgage payment including taxes and insurance, the total interest over the term, and the loan-to-value ratio.'),
 'refinance-breakeven': ('Refinance Break-Even Calculator | Charles M. Carella, CPA',
   'Work out how many months of lower payments it takes to earn back the cost of refinancing, and compare the lifetime cost of both loans.'),
 'loan-payment': ('Loan Payment Calculator | Charles M. Carella, CPA',
   'Calculate a loan payment and total interest, and see how much sooner the balance clears if you add a fixed amount to every payment.'),
 'retirement-savings': ('Retirement Savings Calculator | Charles M. Carella, CPA',
   'Project what a retirement account will be worth from your current balance, your contributions and an employer match over the years remaining.'),
 'self-employment-tax': ('Self-Employment Tax Calculator | Charles M. Carella, CPA',
   'Estimate Social Security and Medicare tax on self-employment profit, the deductible half, and roughly what each quarterly installment should be.'),
 'section-179': ('Equipment Purchase Tax Calculator | Charles M. Carella, CPA',
   'See what an equipment deduction is worth against your combined tax rate and what the purchase actually costs after tax. Massachusetts differs federally.'),
 'break-even': ('Break-Even Calculator | Charles M. Carella, CPA',
   'Find the unit volume and revenue at which a business covers its fixed costs, and what it takes to reach a target monthly profit on top.'),
 'college-savings': ('College Savings Calculator | Charles M. Carella, CPA',
   'Project the cost of four years of college when your child starts and what you need to set aside each month to close the gap.'),
}

CALC_RELATED = {
 'mortgage-payment': [('refinance-breakeven', 'Refinance break-even'), ('loan-payment', 'Loan payment')],
 'refinance-breakeven': [('mortgage-payment', 'Mortgage payment'), ('loan-payment', 'Loan payment')],
 'loan-payment': [('break-even', 'Break-even point'), ('mortgage-payment', 'Mortgage payment')],
 'retirement-savings': [('college-savings', 'Saving for college'), ('self-employment-tax', 'Self-employment tax')],
 'self-employment-tax': [('section-179', 'Equipment purchase'), ('break-even', 'Break-even point')],
 'section-179': [('break-even', 'Break-even point'), ('self-employment-tax', 'Self-employment tax')],
 'break-even': [('section-179', 'Equipment purchase'), ('loan-payment', 'Loan payment')],
 'college-savings': [('retirement-savings', 'Retirement savings'), ('mortgage-payment', 'Mortgage payment')],
}

CALC_SERVICE = {
 'mortgage-payment': ('tax-preparation-planning', 'Tax preparation &amp; planning'),
 'refinance-breakeven': ('tax-preparation-planning', 'Tax preparation &amp; planning'),
 'loan-payment': ('financial-statements', 'Financial statements'),
 'retirement-savings': ('tax-preparation-planning', 'Tax preparation &amp; planning'),
 'self-employment-tax': ('tax-preparation-planning', 'Tax preparation &amp; planning'),
 'section-179': ('business-consulting', 'Business consulting'),
 'break-even': ('business-consulting', 'Business consulting'),
 'college-savings': ('tax-preparation-planning', 'Tax preparation &amp; planning'),
}


# ===========================================================================
def _svc_page(s):
    url = BASE + 'services/' + s['slug'] + '.html'
    rel_links = ''
    for href, label in s['related']:
        h = href if href.startswith('..') or href.endswith('.html') else href + '.html'
        rel_links += '<li><a href="' + h + '"><span class="ck">&rarr;</span> ' + label + '</a></li>'
    p = dict(path='services/' + s['slug'] + '.html', depth=1, nav='services',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'])
    p['body'] = phero(p, [('Services', 'services/index.html'), (_plain(s['nav_title']), None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">' + s['body'] +
      '<h2>Common questions</h2>' + faq_html(s['faqs']) +
      '</div>'
      '<div class="aside">'
      '<div class="acard"><div class="t">Talk it through</div>'
      '<p>Describe what you are dealing with and you will get a straight answer about what the work involves.</p>'
      '<a class="btn b-acc" href="tel:' + TEL + '">' + PH + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>' + rel_links + '</ul></div>'
      '<div class="acard light"><div class="t">Also on this site</div><ul>'
      '<li><a href="../about.html#engagement"><span class="ck">&rarr;</span> How an engagement runs</a></li>'
      '<li><a href="../about.html#bring"><span class="ck">&rarr;</span> What to bring</a></li>'
      '<li><a href="../calculators/index.html"><span class="ck">&rarr;</span> Financial calculators</a></li>'
      '<li><a href="../contact.html"><span class="ck">&rarr;</span> Office &amp; directions</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [_org(),
      breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/'), (_plain(s['nav_title']), url)]),
      _svc_schema(_plain(s['nav_title']), _plain(s['short']), url),
      faq_schema([(q, _plain(a)) for q, a in s['faqs']])]
    return p


def _calc_page(calc):
    slug = calc['slug']
    title, desc = CALC_META[slug]
    url = BASE + 'calculators/' + slug + '.html'
    p = dict(path='calculators/' + slug + '.html', depth=1, nav='calculators',
             # phero() html-escapes the eyebrow, so this must be a literal character,
             # not an entity reference.
             title=title, desc=desc, eyebrow='Calculators · ' + calc['cat'],
             h1=calc['title'], sub=calc['blurb'])
    ph = phero(p, [('Calculators', 'calculators/index.html'), (calc['title'], None)])

    rl = ''
    for s2, label in CALC_RELATED[slug]:
        rl += ('<li><a href="' + s2 + '.html"><span class="ck">&rarr;</span> ' + label + '</a></li>')
    svc_slug, svc_label = CALC_SERVICE[slug]

    body = ('<style>' + C.CALC_CSS + '</style>'
            + C.calc_page_body(calc, ph, rel, ARROW, depth=1)
            + '<section class="sec tint"><div class="wrap"><div class="split">'
              '<div class="prose reveal">'
              '<h2>How to read the result</h2>'
              '<p>Everything above is an estimate built from the assumptions in the boxes on the left. '
              'Change one and the figures change with it &mdash; which is the useful part, because the '
              'range a number moves through under plausible assumptions tells you more than any single '
              'answer does.</p>'
              '<p>The calculation runs in your browser. Nothing is transmitted, stored or sent anywhere, '
              'and no third-party script is involved. Rates, thresholds and limits change from year to '
              'year, so check the current figures before relying on any of it, and treat the output as a '
              'way of sizing a question rather than as advice about your own position.</p>'
              '<p>When the answer matters, call the office on <a href="tel:' + TEL + '">' + PH + '</a> and '
              'describe the actual facts.</p>'
              '</div>'
              '<div class="aside">' + CALL_CARD +
              '<div class="acard light"><div class="t">Related calculators</div><ul>' + rl +
              '<li><a href="index.html"><span class="ck">&rarr;</span> All eight calculators</a></li>'
              '</ul></div>'
              '<div class="acard light"><div class="t">Related service</div><ul>'
              '<li><a href="../services/' + svc_slug + '.html"><span class="ck">&rarr;</span> ' + svc_label + '</a></li>'
              '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
              '</ul></div></div></div></div></section>'
            + C.CALC_JS)
    p['body'] = body
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/'),
                                              (calc['title'], url)])]
    p['cta_args'] = ('Numbers are a starting point.',
                     'A calculator sizes the question. Call the office on ' + PH.replace('&', 'and')
                     + ' or write to ' + FIRM['email'] + ' to talk about the answer.')
    return p


# ===========================================================================
def pages():
    P = []

    # ------------------------------------------------------------------ HOME
    svc_cards = ''.join([
      _card(0, 'services/' + s['slug'] + '.html', s['ic'], s['nav_title'], s['short'],
            ('0' + str(i + 1))[-2:])
      for i, s in enumerate(SERVICES)])

    calc_cards = ''.join([
      _card(0, 'calculators/self-employment-tax.html', 'calc', 'Self-employment tax',
            'Social Security and Medicare on self-employment profit, the deductible half, and roughly what each quarterly installment comes to.'),
      _card(0, 'calculators/break-even.html', 'chart', 'Break-even point',
            'The volume and revenue at which a business covers its fixed costs &mdash; and what it takes to reach a target profit on top.'),
      _card(0, 'calculators/mortgage-payment.html', 'estate', 'Mortgage payment',
            'Principal, interest, taxes and insurance on a fixed-rate loan, with total interest over the term and the loan-to-value ratio.'),
    ])

    body = (
      '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" aria-hidden="true">' + GLYPH + '</svg>'
      '<div class="wrap"><div class="reveal in">'
      '<span class="eyebrow on-dark">Certified Public Accountant &middot; North Billerica, Massachusetts</span>'
      '<h1>Tax and accounting for people and the businesses they run.</h1>'
      '<p class="sub">A CPA office at 330 Boston Road in North Billerica. Tax preparation and planning, '
      'accounting and bookkeeping, financial statement preparation, and business consulting &mdash; for '
      'individuals and for small businesses.</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:' + TEL + '">Call ' + PH + '</a>'
      '<a class="btn b-gh" href="services/index.html">See what the office does ' + ARROW + '</a></div>'
      '<div class="hero-trust"><span><b>Certified</b> Public Accountant</span>'
      '<span><b>North Billerica</b>, Massachusetts</span>'
      '<span><b>Individuals</b> and small businesses</span>'
      '<span><b>Eight</b> calculators on this site</span></div>'
      '</div></div></section>'

      '<section class="strip"><div class="wrap reveal">'
      '<div class="cell"><div class="n">Tax</div><div class="l">preparation and planning</div></div>'
      '<div class="cell"><div class="n">Books</div><div class="l">accounting and bookkeeping</div></div>'
      '<div class="cell"><div class="n">Statements</div><div class="l">prepared for owners and lenders</div></div>'
      '<div class="cell"><div class="n">Advice</div><div class="l">business consulting</div></div>'
      '</div></section>'

      '<section class="sec" id="services"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">What the office does</span>'
      '<h2>Four services, and they are the same conversation.</h2>'
      '<p class="lead">For somebody who owns a small business, the return, the books, the statements a '
      'lender asks for and the decision about next year are not separate problems. They are one problem '
      'looked at from four directions, which is the argument for handling them in one place.</p>'
      '</div><div class="cards">' + svc_cards + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">All four services ' + ARROW + '</a></p>'
      '</div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split">'
      '<div class="reveal"><span class="eyebrow">How the work runs</span>'
      '<h2>What actually happens, in the order it happens.</h2>'
      '<p class="lead">There is no mystery to an accounting engagement, and knowing the shape of it in '
      'advance removes most of the friction. Four steps, and the first one is short.</p>'
      '<div class="prose" style="margin-top:26px">'
      '<h3>1. A short call</h3>'
      '<p>What kind of return or work it is, roughly what the year looked like, and what deadline is '
      'driving the question. Ten minutes is usually enough to establish whether this is a tax matter, an '
      'accounting matter, or both, and what it will take.</p>'
      '<h3>2. Gathering</h3>'
      '<p>The records come together &mdash; last year’s return, this year’s income documents, '
      'the books if there is a business. Completeness at this stage decides most of what follows. '
      '<a href="about.html#bring">The list is here.</a></p>'
      '<h3>3. The work, and the questions</h3>'
      '<p>Preparation, then the questions that arise from it, ideally in one batch rather than a trickle. '
      'Something unusual in your year is a reason for a conversation, not a reason for an assumption.</p>'
      '<h3>4. Review, signature, filing</h3>'
      '<p>You see the return before it goes anywhere. A return filed electronically cannot be transmitted '
      'until the taxpayer has signed the authorization, a paid preparer signs it too, and you are entitled '
      'to a complete copy. That copy is the starting point for next year.</p>'
      '<h3>And then the useful part</h3>'
      '<p>Filing closes the year that is finished. The conversation worth having is about the one that is '
      'still open &mdash; which is why the autumn call tends to be worth more than the April one.</p>'
      '</div></div>'
      '<div class="aside">' + CALL_CARD +
      '<div class="acard light"><div class="t">Before you call</div><ul>'
      '<li><a href="about.html#bring"><span class="ck">&rarr;</span> What to bring</a></li>'
      '<li><a href="about.html#engagement"><span class="ck">&rarr;</span> How an engagement runs</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> The four services</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Tools</span><h2>Eight calculators that run on this page.</h2>'
      '<p class="lead">Mortgage and refinance, loans, retirement and college saving, self-employment tax, '
      'equipment purchases and break-even. No third-party script, no sign-in, nothing sent anywhere &mdash; '
      'the arithmetic happens in your browser and stops there.</p>'
      '</div><div class="cards">' + calc_cards + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="calculators/index.html">All eight calculators ' + ARROW + '</a></p>'
      '</div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Where the office is</span><h2>330 Boston Road, North Billerica.</h2>'
      '<p class="lead">Suite 12, on Boston Road in North Billerica, Massachusetts.</p></div>'
      '<div class="split">'
      '<div>' + gmap('Pan, zoom, or open the map full screen for turn-by-turn directions.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + PH + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + TEL + '">Call ' + PH + '</a></div>'
      '<div class="acard light"><div class="t">Getting there</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Open in Google Maps</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the office</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Common questions</span><h2>Answers before you call.</h2></div>'
      + faq_html(HOME_FAQS) +
      '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">More questions answered ' + ARROW + '</a></p>'
      '</div></section>'
    )
    P.append(dict(path='index.html', depth=0, nav='home',
      title='Charles M. Carella, CPA | North Billerica, Massachusetts',
      desc='Certified Public Accountant at 330 Boston Road in North Billerica, Massachusetts. Tax preparation and planning, bookkeeping, financial statements and business consulting.',
      body=body,
      schema=[_org(),
              {"@context": "https://schema.org", "@type": "WebSite", "name": FIRM['name'],
               "url": BASE, "publisher": {"@id": ORG_ID}}]))

    # ----------------------------------------------------------------- ABOUT
    p = dict(path='about.html', depth=0, nav='about',
      title='About the Practice | Charles M. Carella, CPA',
      desc='What this CPA office does, how an engagement runs from first call to filing, and exactly what to gather before an appointment. North Billerica, Massachusetts.',
      eyebrow='About the practice', h1='About the work.',
      sub='A short account of what this office does, how an engagement actually runs, and what to have ready before it starts.')
    p['body'] = phero(p, [('About the practice', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>Charles M. Carella, CPA is a Certified Public Accountant’s office at 330 Boston Road, '
      'Suite 12, in North Billerica, Massachusetts. The work is tax preparation and planning, accounting '
      'and bookkeeping, financial statement preparation, and business consulting, for individuals and for '
      'small businesses.</p>'
      '<p>That is a deliberately plain description, and this page is going to stay plain. What follows is '
      'about the work: what the license behind it means, how an engagement runs, and what to bring.</p>'

      '<h2>What the credential is</h2>'
      '<p>Anybody may prepare a tax return for payment provided they hold a preparer tax identification '
      'number. The bar for calling yourself an accountant is lower still: there is not one.</p>'
      '<p>A Certified Public Accountant is licensed by a state board. The license requires passing the '
      'Uniform CPA Examination, meeting education and experience requirements, and then continuing to meet '
      'annual professional education requirements to keep it. It carries a code of professional conduct '
      'with a disciplinary process attached, and it can be revoked.</p>'
      '<p>Two consequences matter to a client. A CPA has unlimited rights to represent a taxpayer before '
      'the IRS &mdash; in an examination, in collection, on appeal &mdash; which most paid preparers do '
      'not. And the same license covers the work either side of the return: the books it is built from, '
      'the statements a lender asks for, and the structural questions that decide what next year’s '
      'return will look like.</p>'

      '<h2 id="engagement">How an engagement runs</h2>'
      '<p>Accounting work has a shape, and it is worth knowing before you start.</p>'
      '<h3>The first conversation</h3>'
      '<p>Short, and mostly diagnostic: what kind of return or engagement this is, roughly what the year '
      'looked like, whether there is a business and how it is organized, and what deadline is driving the '
      'question. Ten minutes normally settles whether the work is a tax matter, an accounting matter, or '
      'both, and what it involves.</p>'
      '<p>The most useful thing you can do in that conversation is describe the awkward part. Unfiled '
      'years, a notice sitting on the desk, books that stopped reconciling in June, a partner who left &mdash; '
      'none of those are unusual, and all of them change the order of the work. Discovered at the start '
      'they are a plan. Discovered at the end they are a problem.</p>'
      '<h3>Gathering</h3>'
      '<p>Then the records. Completeness here decides most of what follows: a complete file produces fewer '
      'questions, a shorter engagement and a lower chance of an amended return later. The list is below.</p>'
      '<h3>The work</h3>'
      '<p>Preparation, and then the questions that come out of it. Anything unusual in your year is a '
      'reason to ask rather than to assume, and the questions are better delivered in one batch than as a '
      'trickle over three weeks.</p>'
      '<h3>Review and filing</h3>'
      '<p>Nothing is transmitted before you have seen it, and that is a rule rather than a courtesy: a '
      'return filed electronically requires the taxpayer’s signed authorization first. A paid '
      'preparer signs the return as well and must give you a complete copy of it. Keep the copy. It is the '
      'starting point for next year, for a lender, and for anything that surfaces afterwards.</p>'
      '<h3>The year that is still open</h3>'
      '<p>Filing closes a year that has already happened. Almost every decision that changes a tax bill '
      'belongs to the year that has not finished yet &mdash; how the business is organized, what the owner '
      'takes as wages against distributions, when equipment is bought, whether a retirement plan '
      'contribution gets made, how a sale is structured. Which is why an autumn conversation is generally '
      'worth more than an April one.</p>'

      '<h2 id="bring">What to bring</h2>'
      '<p>More is better than less, and a gap is worth mentioning rather than working around.</p>'
      '<h3>Everyone</h3>'
      '<ul>'
      '<li>Last year’s federal and state returns, complete, including the schedules</li>'
      '<li>Names, dates of birth and Social Security numbers for everyone on the return</li>'
      '<li>Bank details if a refund is to be deposited directly</li>'
      '<li>Any notice received from the IRS or the Massachusetts Department of Revenue, with its envelope</li>'
      '</ul>'
      '<h3>Income</h3>'
      '<ul>'
      '<li>W-2 forms, and the 1099 forms &mdash; interest, dividends, retirement distributions, brokerage '
      'proceeds, contract income, state refunds</li>'
      '<li>Brokerage statements showing cost basis for anything sold, not just the proceeds</li>'
      '<li>K-1 forms from a partnership, an S corporation, a trust or an estate</li>'
      '<li>Rental income and the expenses against it</li>'
      '<li>Records of any income that arrived without a form attached to it</li>'
      '</ul>'
      '<h3>Deductions, credits and payments</h3>'
      '<ul>'
      '<li>Mortgage interest and property tax statements</li>'
      '<li>Tuition statements, student loan interest, and childcare paid, with the provider’s '
      'identification number</li>'
      '<li>Retirement and health savings account contributions made outside payroll</li>'
      '<li>Charitable receipts, and written acknowledgement for anything substantial</li>'
      '<li>Health coverage forms</li>'
      '<li>Estimated tax payments made during the year, with the dates and amounts</li>'
      '</ul>'
      '<h3>If there is a business</h3>'
      '<ul>'
      '<li>The books for the year, or the bank and card statements if there are no books</li>'
      '<li>A depreciation schedule, and details of anything bought or sold during the year</li>'
      '<li>Payroll reports and any 1099 forms issued to contractors</li>'
      '<li>Loan statements showing the year-end balance and the interest paid</li>'
      '<li>The entity’s formation documents and any election filed &mdash; especially an S election '
      '&mdash; if this is a first engagement</li>'
      '</ul>'
      '<h3>Anything that changed</h3>'
      '<p>A marriage or a divorce, a birth, a death, a house bought or sold, a move to or from another '
      'state, a business started or closed, a large gift given or received, an inheritance, a retirement, '
      'a first year of self-employment. Each of these changes the return, and each is easier to handle '
      'when it is mentioned at the start.</p>'

      '<div class="callout"><p><strong>On scope and fees.</strong> This site describes the services '
      'offered and what the work generally involves. What your own engagement covers, how long it takes '
      'and what it costs are settled in conversation with the office &mdash; there is no published fee '
      'schedule, because the work is not uniform.</p></div>'

      '<h2>Confidentiality</h2>'
      '<p>Client information is confidential. For a CPA that is a professional obligation with enforcement '
      'behind it rather than an internal policy, and it covers the fact of the engagement as well as its '
      'contents. Federal law adds a further restriction specific to tax work: information supplied for the '
      'preparation of a return may not be used for another purpose or disclosed to anybody else without '
      'the taxpayer’s written consent.</p>'

      '<h2>Where to go next</h2>'
      '<p>The <a href="services/index.html">services section</a> covers the four practice areas in detail. '
      'The <a href="faq.html">questions page</a> answers the things people ask before they call. The '
      '<a href="calculators/index.html">calculators</a> are there for sizing a question before you raise '
      'it. Or call <a href="tel:' + TEL + '">' + PH + '</a>.</p>'
      '</div>'
      '<div class="aside">' + CALL_CARD +
      '<div class="acard light"><div class="t">On this page</div><ul>'
      '<li><a href="#engagement"><span class="ck">&rarr;</span> How an engagement runs</a></li>'
      '<li><a href="#bring"><span class="ck">&rarr;</span> What to bring</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div>'
      '<div class="acard light"><div class="t">The four services</div><ul>'
      + ''.join('<li><a href="services/' + s['slug'] + '.html"><span class="ck">&rarr;</span> '
                + s['nav_title'] + '</a></li>' for s in SERVICES) +
      '</ul></div></div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('About the practice', BASE + 'about.html')])]
    P.append(p)

    # ------------------------------------------------------------------- FAQ
    p = dict(path='faq.html', depth=0, nav='faq',
      title='Common Questions | Charles M. Carella, CPA',
      desc='Straight answers on CPA fees, deadlines and extensions, unfiled returns, IRS notices, Massachusetts part-year filing, record retention, and confidentiality.',
      eyebrow='Answers', h1='Questions worth asking before you call.',
      sub='If yours is not here, the answer is a short phone call rather than a form.')
    p['body'] = phero(p, [('Common questions', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Working with a CPA</h2>'
      '<p class="lead">What the credential means, what an engagement involves, and what things cost.</p>'
      '</div>' + faq_html(HOME_FAQS) + '</div></section>'
      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Deadlines, notices and records</h2>'
      '<p class="lead">The questions that arrive with a letter, a date, or a year that got away.</p>'
      '</div>' + faq_html(MORE_FAQS) +
      '<div class="sec-head reveal" style="margin-top:56px"><h2>Still deciding?</h2>'
      '<p class="lead">The <a href="about.html#engagement">engagement page</a> sets out how the work runs '
      'from first call to filing, and <a href="about.html#bring">what to bring</a> lists what to gather '
      'before an appointment. The <a href="services/index.html">four services</a> are described in full.</p>'
      '</div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Common questions', BASE + 'faq.html')]),
                   faq_schema([(q, _plain(a)) for q, a in ALL_FAQS])]
    P.append(p)

    # --------------------------------------------------------------- CONTACT
    p = dict(path='contact.html', depth=0, nav='contact',
      title='Contact | Charles M. Carella, CPA | North Billerica, MA',
      desc='Reach the office at 330 Boston Road, Suite 12, North Billerica, Massachusetts. Telephone (978) 663-6419 ext. 11, with a map and directions.',
      eyebrow='Contact', h1='Call the office.',
      sub='Describe the situation in a couple of minutes and you will get a straight answer about what the work involves.')
    p['body'] = phero(p, [('Contact', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>330 Boston Road, Suite 12</h2>'
      '<p class="lead">One office, in North Billerica, Massachusetts.</p></div>'
      '<div class="split">'
      '<div>' + gmap('The map is interactive &mdash; pan, zoom, or open it full screen for directions.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + PH + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + TEL + '">Call ' + PH + '</a></div>'
      '<div class="acard light"><div class="t">Quick links</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Directions in Google Maps</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '<li><a href="about.html#bring"><span class="ck">&rarr;</span> What to bring</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Dialing the number</h2>'
      '<p>The office number is <a href="tel:' + TEL + '">' + PH + '</a>. The extension is dialled after '
      'the call connects &mdash; on a mobile, tapping the link places the call and you enter <strong>11</strong> '
      'when prompted. The fax line is ' + FIRM['fax'] + '.</p>'
      '<h2>What a first call covers</h2>'
      '<p>Three things, and it rarely takes longer than ten minutes: what kind of return or engagement '
      'this is, roughly what the year looked like, and what deadline is driving the question. If there is '
      'a business, how it is organized matters as well &mdash; sole proprietorship, partnership, LLC, S '
      'corporation, corporation &mdash; because that decides which return is involved and when it is due.</p>'
      '<p>The most useful thing to raise early is whatever is awkward. Years that were never filed, a '
      'notice with a date on it, books that stopped reconciling, a business that closed mid-year. None of '
      'those are unusual. All of them change the order in which the work is done.</p>'
      '<h2>What to have in front of you</h2>'
      '<ul>'
      '<li>Last year’s return, if you can find it &mdash; not essential for a first call, but useful</li>'
      '<li>Any notice you have received, so the date on it can be read out</li>'
      '<li>For a business: how it is organized, and roughly what revenue looks like</li>'
      '<li>The deadline you are working against, if there is one</li>'
      '</ul>'
      '<p>The <a href="about.html#bring">full list of what to gather</a> is for the appointment rather '
      'than the call. Missing pieces are not a reason to wait.</p>'
      '<h2>By post or by fax</h2>'
      '<p>Documents can be sent to 330 Boston Road, Suite 12, North Billerica, MA ' + FIRM['zip'] + ', or '
      'to the fax line above. Which route makes sense depends on what you have, so it is worth asking on '
      'the call rather than guessing. Never send Social Security numbers or account details in an '
      'unencrypted email.</p>'
      '<h2>Confidentiality</h2>'
      '<p>Everything said in that first conversation is confidential, including the fact that you called. '
      'For a CPA that obligation is professional and enforceable rather than a matter of policy.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Prefer to write?</div>'
      '<p>Send a note describing the situation and what you are working against.</p>'
      '<a class="btn b-acc" href="mailto:' + FIRM['email'] + '">' + FIRM['email'] + '</a></div>'
      '<div class="acard light"><div class="t">Before the appointment</div><ul>'
      '<li><a href="about.html#bring"><span class="ck">&rarr;</span> What to bring</a></li>'
      '<li><a href="about.html#engagement"><span class="ck">&rarr;</span> How an engagement runs</a></li>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> The four services</a></li>'
      '<li><a href="calculators/index.html"><span class="ck">&rarr;</span> Financial calculators</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Contact', BASE + 'contact.html')]),
      {"@context": "https://schema.org", "@type": "ContactPage",
       "name": "Contact " + FIRM['name'], "url": BASE + 'contact.html'}]
    P.append(p)

    # ---------------------------------------------------------- SERVICES HUB
    cards = ''
    for i, s in enumerate(SERVICES):
        cards += ('<a class="card reveal" href="' + s['slug'] + '.html">'
                  '<span class="num">' + ('0' + str(i + 1))[-2:] + '</span>'
                  '<div class="cic">' + icon(s['ic']) + '</div><h3>' + s['nav_title'] + '</h3>'
                  '<p>' + s['short'] + '</p>'
                  '<span class="more">Read more ' + ARROW + '</span></a>')
    p = dict(path='services/index.html', depth=1, nav='services',
      title='Services | Charles M. Carella, CPA | North Billerica, MA',
      desc='Tax preparation and planning, accounting and bookkeeping, financial statement preparation, and business consulting for individuals and small businesses in Massachusetts.',
      eyebrow='Services', h1='Four services, and the connections between them.',
      sub='Tax preparation and planning, accounting and bookkeeping, financial statement preparation, and business consulting.')
    p['body'] = phero(p, [('Services', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>What the office does</h2>'
      '<p class="lead">A short list, described honestly. Each of these is a real service with real work '
      'behind it, and for a small business the four of them tend to arrive together.</p>'
      '</div><div class="cards">' + cards + '</div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Why they belong together</h2>'
      '<p>Take a business with a lender asking for statements. The statements come from the books, so the '
      'books have to reconcile before anything can be produced. The statements have to agree with the tax '
      'return, so whoever prepares them needs to know how the return was filed. The covenant behind the '
      'request will constrain distributions, which changes what the owner can take out, which changes the '
      'personal return. That is one problem with four names on it.</p>'
      '<p>Splitting it across three providers means somebody has to hold the whole picture, and in '
      'practice that somebody is the owner, at the exact moment they have least time for it.</p>'

      '<h2>What each one actually is</h2>'
      '<h3>Tax preparation and planning</h3>'
      '<p>Federal and Massachusetts returns for individuals and small businesses, plus the planning that '
      'has to happen before the year closes to be worth anything. '
      '<a href="tax-preparation-planning.html">In detail</a>.</p>'
      '<h3>Accounting and bookkeeping</h3>'
      '<p>A chart of accounts that fits the business, activity recorded properly, accounts reconciled '
      'against outside statements, and period-end figures that can be relied on. '
      '<a href="accounting-bookkeeping.html">In detail</a>.</p>'
      '<h3>Financial statement preparation</h3>'
      '<p>Statements assembled from the books for owners, lenders, landlords and buyers &mdash; and a '
      'clear answer about which of the four levels of service a given request actually requires, since '
      'the difference in cost is a multiple rather than a percentage. '
      '<a href="financial-statements.html">In detail</a>.</p>'
      '<h3>Business consulting</h3>'
      '<p>The questions that arrive between filings: how the business should be organized, what a hire '
      'really costs, whether the equipment purchase makes sense, why a profitable business is short of '
      'cash. <a href="business-consulting.html">In detail</a>.</p>'

      '<h2>What is not on this list</h2>'
      '<p>Assurance work &mdash; a review or an audit &mdash; is a different engagement with an '
      'independence requirement attached, and it is not among the services above. If a lender or a '
      'contract is asking for reviewed or audited statements, that is worth establishing early, because '
      'the requirement is frequently negotiable when the agreement is signed and never afterwards. The '
      '<a href="financial-statements.html">financial statements page</a> explains the four levels and how '
      'to tell which one is being asked for.</p>'
      '</div>'
      '<div class="aside">' + CALL_CARD +
      '<div class="acard light"><div class="t">Before you call</div><ul>'
      '<li><a href="../about.html#engagement"><span class="ck">&rarr;</span> How an engagement runs</a></li>'
      '<li><a href="../about.html#bring"><span class="ck">&rarr;</span> What to bring</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '<li><a href="../calculators/index.html"><span class="ck">&rarr;</span> Financial calculators</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/')]),
      {"@context": "https://schema.org", "@type": "ItemList",
       "name": "Services — " + FIRM['name'],
       "itemListElement": [{"@type": "ListItem", "position": i + 1,
                            "name": _plain(s['nav_title']),
                            "url": BASE + 'services/' + s['slug'] + '.html'}
                           for i, s in enumerate(SERVICES)]}]
    P.append(p)

    for s in SERVICES:
        P.append(_svc_page(s))

    # ------------------------------------------------------- CALCULATORS HUB
    groups = ''
    for cat in C.CATEGORIES:
        items = [c for c in C.CALCULATORS if c['cat'] == cat]
        cardz = ''.join('<a class="calccard reveal" href="' + c['slug'] + '.html">'
                        '<div class="cc">' + c['cat'] + '</div><h3>' + c['title'] + '</h3>'
                        '<p>' + c['blurb'] + '</p></a>' for c in items)
        groups += ('<div class="sec-head reveal" style="margin-top:44px;margin-bottom:0">'
                   '<h3>' + cat + '</h3></div><div class="calcgrid">' + cardz + '</div>')

    p = dict(path='calculators/index.html', depth=1, nav='calculators',
      title='Financial Calculators | Charles M. Carella, CPA',
      desc='Eight financial calculators covering mortgages, refinancing, loans, retirement, self-employment tax, equipment purchases, break-even and college saving.',
      eyebrow='Calculators', h1='Eight calculators, running on this page.',
      sub='Mortgage and refinance, loans, retirement and college saving, self-employment tax, equipment purchases, and break-even.')
    p['body'] = ('<style>' + C.CALC_CSS + '</style>'
      + phero(p, [('Calculators', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Size the question before you ask it</h2>'
      '<p class="lead">Each of these takes a handful of assumptions and shows what falls out of them. The '
      'point is not the single answer &mdash; it is watching the answer move as you change an assumption, '
      'because that is what tells you which variable the decision actually turns on.</p>'
      '</div>' + groups + '</div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>How these work</h2>'
      '<p>The arithmetic runs in your browser. There is no third-party script, no sign-in, no cookie and '
      'no network request: nothing you type is transmitted, stored or seen by anybody. Every assumption is '
      'visible in a box you can change, and the working behind each one is described on its page.</p>'
      '<p>The spread is deliberate. Household questions &mdash; a mortgage, a refinance, a loan, saving '
      'for retirement or for college &mdash; sit alongside the ones a small business runs into: '
      'self-employment tax, what an equipment deduction is worth, where break-even actually falls. Those '
      'are the questions that come up in practice, so those are the calculators here.</p>'

      '<h2>What they are not</h2>'
      '<p>They are not advice, and they are not a substitute for a return. Every one of them makes '
      'simplifying assumptions that are stated on its page. Tax rates, contribution limits and thresholds '
      'change annually, and none of these tools knows your filing status, your other income, your state '
      'position or anything else that determines the real answer.</p>'
      '<p>Used properly they do one useful thing: they tell you whether a question is worth a phone call. '
      'A break-even that lands at twice your current volume, or a self-employment tax estimate several '
      'thousand dollars above what you have paid in, is worth raising before the year closes rather than '
      'after.</p>'

      '<h2>Where each one leads</h2>'
      '<ul>'
      '<li><a href="self-employment-tax.html">Self-employment tax</a> and '
      '<a href="section-179.html">equipment purchases</a> connect to '
      '<a href="../services/tax-preparation-planning.html">tax preparation and planning</a>.</li>'
      '<li><a href="break-even.html">Break-even</a> connects to '
      '<a href="../services/business-consulting.html">business consulting</a>.</li>'
      '<li><a href="loan-payment.html">Loan payment</a> and '
      '<a href="refinance-breakeven.html">refinance break-even</a> tend to arrive alongside '
      '<a href="../services/financial-statements.html">financial statement</a> requests from a lender.</li>'
      '<li><a href="retirement-savings.html">Retirement</a>, '
      '<a href="college-savings.html">college saving</a> and '
      '<a href="mortgage-payment.html">mortgage payments</a> are personal-side questions that still land '
      'on a tax return.</li>'
      '</ul>'
      '</div>'
      '<div class="aside">' + CALL_CARD +
      '<div class="acard light"><div class="t">Services</div><ul>'
      + ''.join('<li><a href="../services/' + s['slug'] + '.html"><span class="ck">&rarr;</span> '
                + s['nav_title'] + '</a></li>' for s in SERVICES) +
      '</ul></div></div></div></div></section>'))
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/')]),
      {"@context": "https://schema.org", "@type": "ItemList", "name": "Financial calculators",
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c['title'],
                            "url": BASE + 'calculators/' + c['slug'] + '.html'}
                           for i, c in enumerate(C.CALCULATORS)]}]
    P.append(p)

    for c in C.CALCULATORS:
        P.append(_calc_page(c))

    return P
