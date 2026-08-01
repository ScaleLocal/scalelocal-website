# -*- coding: utf-8 -*-
"""
Dorfman & Dorfman, CPAs — all page content.

Sourcing discipline: every claim about the firm comes from the firm's own site.
The two owners, the 2008 founding, the predecessor practice, the schools, the
FINRA background and the six-item service list are theirs. Everything else on
these pages is either general Massachusetts tax practice (true of the state, not
a claim about the firm) or explicitly hedged. There is no attest practice, no
membership claim, no published office hours and no portal, because they publish
none of those.
"""
import html, re
from build import (FIRM, BASE, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   breadcrumb_schema, faq_schema)
import calculators as C

ORG_ID = BASE + '#firm'


def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()


def org():
    """Our own organisation schema. Deliberately omits memberships, opening
    hours and geo coordinates — the firm publishes none of them."""
    return {"@context": "https://schema.org", "@type": "AccountingService", "@id": ORG_ID,
            "name": FIRM['name'], "legalName": FIRM['name'], "url": BASE,
            "email": FIRM['email'], "telephone": FIRM['ph'], "faxNumber": FIRM['fax'],
            "foundingDate": "2008", "priceRange": "$$",
            "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                        "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                        "postalCode": FIRM['zip'], "addressCountry": "US"},
            "areaServed": [{"@type": "AdministrativeArea", "name": "Middlesex County, Massachusetts"}],
            "hasMap": FIRM['maps'],
            "employee": [
                {"@type": "Person", "name": "Marvin H. Dorfman", "honorificSuffix": "CPA",
                 "jobTitle": "Owner", "url": BASE + 'team/marvin-h-dorfman.html'},
                {"@type": "Person", "name": "Estee C. Dorfman", "honorificSuffix": "CPA, MSA",
                 "jobTitle": "Owner", "url": BASE + 'team/estee-c-dorfman.html'}]}


def svc_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "description": desc, "url": url, "serviceType": name,
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "AdministrativeArea", "name": "Massachusetts"}}


CTA = ('Talk to one of the owners.',
       'Call the Wilmington office at (781) 780-7069, extension 11, or write to '
       'estee@dorfman-cpas.com. Marvin or Estee will answer — there is nobody else here '
       'to route you to, and your inquiry stays confidential.')


def _card(d, href, ic, title, text, num=None):
    return ('<a class="card reveal" href="' + rel(d, href) + '">'
            + ('<span class="num">' + num + '</span>' if num else '')
            + '<div class="cic">' + icon(ic) + '</div><h3>' + title + '</h3><p>' + text + '</p>'
            '<span class="more">Read more ' + ARROW + '</span></a>')


def _person_card(d, slug, initials, name, cred, text):
    return ('<a class="tcard reveal" href="' + rel(d, 'team/' + slug + '.html') + '">'
            '<div class="tava">' + initials + '</div><h3>' + name + '</h3>'
            '<div class="cred">' + cred + '</div><p>' + text + '</p></a>')


# ============================================================================
# SERVICES — the firm's own six-item list, with bookkeeping, write-up and
# financial statement preparation kept together because for a small business
# they are one piece of work.
# ============================================================================
SERVICES = [

 dict(slug='individual-tax', ic='calc', nav_title='Individual Tax Preparation',
   short='Federal and Massachusetts returns for households, sole proprietors, landlords and retirees — prepared and signed by the CPA you spoke to.',
   title='Individual Tax Preparation | CPA in Wilmington, MA | Dorfman',
   desc='Federal and Massachusetts individual tax return preparation from a two-person CPA firm in Wilmington, covering Schedule C, rental, retirement and multi-state income.',
   eyebrow='Individual tax', h1='Your return, prepared by the person you actually spoke to.',
   sub='Individual returns are the largest part of what a small firm does, and the part where being small is an advantage rather than a limitation.',
   body='''
<h2>The short answer</h2>
<p>We prepare federal and Massachusetts income tax returns for individuals: employees, retirees, sole proprietors, landlords, and the owners of the businesses we already work with. Two CPAs own this firm, and one of them prepares and signs your return.</p>

<h2>Who this is for</h2>
<ul>
<li><strong>Households with more than a W-2.</strong> Investment income, stock compensation, a rental unit, a side business, a 529 withdrawal, an inheritance — any one of these turns a simple return into one worth having a CPA look at.</li>
<li><strong>Sole proprietors and single-member LLCs.</strong> Schedule C, the home office and vehicle questions, depreciation, and the self-employment tax that catches most people out in their first profitable year.</li>
<li><strong>Landlords.</strong> Schedule E, basis and depreciation schedules that have to carry forward correctly for decades, passive loss limits, and what happens on sale.</li>
<li><strong>Retirees.</strong> Social Security taxation, pension and annuity income, required minimum distributions, and the Massachusetts treatment of retirement income, which does not match the federal treatment item for item.</li>
<li><strong>Owners of businesses we prepare returns for.</strong> The K-1 and the personal return are one calculation, not two, and it goes badly when two different firms each see half of it.</li>
</ul>

<h2>What is different about a Massachusetts return</h2>
<p>Massachusetts taxes most income at one flat rate rather than in graduated brackets, which surprises people who move here from almost anywhere else. The rate is rarely what causes a problem. These three are:</p>
<ul>
<li><strong>Health coverage reporting.</strong> Massachusetts still requires individuals to report coverage on the state return. If the Form MA 1099-HC never arrived, the schedule cannot be completed properly, and the state notices.</li>
<li><strong>Short-term capital gains.</strong> Massachusetts taxes short-term gains at a higher rate than ordinary income. A year of active trading can produce a state bill far larger than the federal one, and there is no withholding behind it.</li>
<li><strong>The surtax on high income.</strong> An additional levy applies above a threshold that is adjusted annually. Households nowhere near it in a normal year cross it in the year they sell a business, sell a property, or take a single large distribution — which is exactly the year to have the conversation before December rather than in April.</li>
</ul>
<p>Part-year and non-resident returns deserve their own mention. Massachusetts and New Hampshire share a long border and a great many commuters, and where income is sourced, where a remote worker is taxed, and how the credit for taxes paid to another state is computed are all genuine questions rather than formalities.</p>

<h2>How the work runs</h2>
<p>Most individual clients settle into a simple pattern. Documents come in as they arrive rather than in one envelope at the end. We ask about anything that changed — a move, a marriage, a new job, a property, a business started or closed — because the changes are where the tax consequences hide. If something in the return needs a decision from you, you get a call about it, not a footnote.</p>
<p>Where estimated payments are required, we compute them and tell you what to pay and when. Underpayment interest is one of the few costs in tax that is entirely avoidable and entirely self-inflicted.</p>

<div class="callout"><p><strong>An extension moves the filing date, not the payment date.</strong> If you owe, the payment is still due in April. An extension is a perfectly ordinary tool and nothing to be embarrassed about — but it works only if the payment goes with it.</p></div>

<h2>Before your first return with us</h2>
<p>Send last year&rsquo;s federal and state returns before anything else. They tell us your carryforwards, your depreciation history, your basis, and which elections you are already living with. Most of the errors we find on new clients&rsquo; returns are not errors in arithmetic; they are things carried forward incorrectly, or not carried forward at all.</p>
''',
   faqs=[("Do I need a CPA, or is software enough?",
          "<p>If your return is a W-2, a standard deduction and a bank interest statement, software is fine and we will tell you so. It becomes worth paying someone when there is a business, a property, equity compensation, a state line, or a year in which something significant changed. The value is in the questions asked before the return is prepared, not in the typing.</p>"),
         ("What should I send you?",
          "<p>Last year&rsquo;s federal and state returns, this year&rsquo;s W-2s and 1099s, closing statements for any property bought or sold, brokerage year-end statements, and a short note describing anything that changed. If you are missing pieces, send what you have and we will tell you what is still outstanding.</p>"),
         ("Can you prepare returns for other states?",
          "<p>Yes. Part-year, non-resident and multi-state returns are ordinary work here — Massachusetts households frequently have New Hampshire, Rhode Island or Connecticut income, or a remote job based somewhere else entirely.</p>"),
         ("What if I have not filed for a couple of years?",
          "<p>Say so at the start. Unfiled years are a solvable problem and they get worse with time, not better. The order of operations matters: the oldest open year usually has to be prepared first because it feeds everything after it.</p>")],
   related=[('business-tax', 'Business tax preparation'),
            ('small-business-consulting', 'Small business consulting'),
            ('../calculators/self-employment-tax.html', 'Self-employment tax calculator'),
            ('../faq.html', 'Common questions')]),

 dict(slug='business-tax', ic='building', nav_title='Business Tax Preparation',
   short='S corporations, partnerships, LLCs and sole proprietorships — federal returns and the Massachusetts filings that go with them.',
   title='Business Tax Preparation | Small Business CPA | Wilmington MA',
   desc='Business tax return preparation for Massachusetts S corporations, partnerships, LLCs and sole proprietors, including corporate excise and pass-through entity questions.',
   eyebrow='Business tax', h1='The entity return and the owner&rsquo;s return are one problem.',
   sub='For a closely held business, splitting the company return and the owner return between two firms is how planning opportunities get lost.',
   body='''
<h2>The short answer</h2>
<p>We prepare federal and Massachusetts business returns for S corporations, partnerships, multi-member and single-member LLCs, and sole proprietorships — and, for most of those clients, the owners&rsquo; personal returns alongside them.</p>

<h2>Why one firm should see both</h2>
<p>In a closely held company almost every meaningful number appears twice. Owner compensation is a deduction to the company and wages to the owner. A distribution is not deductible but may or may not be taxable depending on basis. A loss passes through only as far as basis allows and then waits. A loan from the owner to the company, or the other way, has consequences on both sides.</p>
<p>None of that is difficult once someone can see both returns. It becomes difficult, and expensive, when the entity accountant and the personal accountant each assume the other is handling it.</p>

<h2>The Massachusetts layer</h2>
<h3>Corporate excise</h3>
<p>Massachusetts does not call it a corporate income tax; it is the corporate excise, and it has a net income component and a property or net worth component. There is a minimum excise that applies even in a year the corporation loses money, which is worth knowing before the first loss year rather than after it.</p>

<h3>The pass-through entity election</h3>
<p>Massachusetts allows eligible pass-through entities to elect to pay an entity-level excise, with a corresponding credit to the owners. The point of the election is federal, not state, and whether it actually helps depends on each owner&rsquo;s own federal position — which means the arithmetic has to be redone as federal rules change rather than assumed to hold from last year.</p>

<h3>Sales and use tax</h3>
<p>Registration, collection and filing obligations start earlier than most owners expect, and use tax on out-of-state purchases is the piece almost everybody forgets. If you have been buying equipment or supplies from out-of-state vendors without tax, that is a use tax question, and it is cheaper to raise it than to have it found.</p>

<h3>Personal property tax</h3>
<p>Massachusetts municipalities tax business personal property, and the annual form is filed with your town&rsquo;s assessors, not with the state. It is a small filing that is easy to miss entirely in the first year of business, and towns do notice.</p>

<h2>Questions that come up every year</h2>
<ul>
<li><strong>Should this be an S corporation?</strong> Sometimes, and less often than the internet suggests. The answer depends on profit level, how much of it is genuinely a return on your labour, payroll cost, state treatment, and how long you intend to keep the structure.</li>
<li><strong>What is reasonable compensation?</strong> The question every S corporation owner would rather not think about. The safe position is documented, defensible, and set before the year rather than reverse-engineered after it.</li>
<li><strong>Am I filing where I should be?</strong> Selling into other states, employing a remote worker in another state, or storing inventory in a warehouse elsewhere can each create a filing obligation. These surface years late, in the form of a letter.</li>
<li><strong>Are these contractors really contractors?</strong> Massachusetts applies one of the strictest worker-classification tests in the country. Whether a worker is properly a contractor is a legal question, and the time to ask it is before the 1099s go out. Where it needs an attorney, we will say so.</li>
</ul>

<div class="callout"><p><strong>Deadlines move earlier than people remember.</strong> Partnership and S corporation returns are due before individual returns, and the entity return has to be finished before the owner&rsquo;s return can be. Working backwards from April is what causes the March scramble.</p></div>

<h2>What we need from you</h2>
<p>A trial balance or a full set of books, the prior year return, the fixed asset and depreciation schedule, loan statements, and payroll reports. If the books are not in a state you would want to hand to anyone, say so — see <a href="bookkeeping-write-up.html">bookkeeping and write-up</a>. Cleaning them up is ordinary work, and it is far cheaper done deliberately than done in a rush against a filing deadline.</p>
''',
   faqs=[("Do you prepare the owners&rsquo; personal returns too?",
          "<p>For most business clients, yes, and we would encourage it. Balancing what comes out of the company against what appears on the owner&rsquo;s return only works when one firm sees both.</p>"),
         ("We are an LLC. Which return do we file?",
          "<p>It depends on how many members there are and what, if anything, has been elected. A single-member LLC with no election is reported on the owner&rsquo;s Schedule C; a multi-member LLC files a partnership return by default; either can elect to be taxed as an S corporation. The Massachusetts consequences do not always follow the federal choice.</p>"),
         ("Can you take over mid-year?",
          "<p>Yes. Send the last filed return and whatever the books look like now. The prior return matters most — it carries the depreciation schedules, basis, carryforwards and elections that the next one has to build on.</p>"),
         ("Do you handle sales tax filings?",
          "<p>Talk to us about it. What we take on depends on the engagement and on the volume, and we would rather tell you plainly what we will and will not be doing than let it fall between us.</p>")],
   related=[('individual-tax', 'Individual tax preparation'),
            ('bookkeeping-write-up', 'Bookkeeping &amp; write-up'),
            ('../calculators/section-179.html', 'Equipment purchase calculator'),
            ('small-business-consulting', 'Small business consulting')]),

 dict(slug='bookkeeping-write-up', ic='ledger', nav_title='Bookkeeping &amp; Write-Up',
   short='Monthly and quarterly write-up, reconciliations, and financial statements prepared from your records — the reporting everything else depends on.',
   title='Bookkeeping, Write-Up & Financial Statements | Wilmington MA CPA',
   desc='Monthly and quarterly bookkeeping, write-up and financial statement preparation for Massachusetts small businesses, plus clean-up of records that have drifted.',
   eyebrow='Accounting', h1='Books that are right are cheaper than books that are late.',
   sub='Bookkeeping, write-up work and financial statement preparation are one job for a small business. Every tax and planning decision downstream depends on them.',
   body='''
<h2>The short answer</h2>
<p>We keep or review the books for small businesses on a monthly or quarterly cycle, reconcile them, make the adjusting entries a set of records needs before anyone can rely on it, and prepare financial statements from those records.</p>

<h2>What write-up actually means</h2>
<p>Write-up is the unglamorous middle of small business accounting: taking what the business recorded — a bank feed, a shoebox, a spreadsheet, a well-kept accounting file — and turning it into a set of books that balances, ties to the bank, and tells the truth about the year. It covers:</p>
<ul>
<li>Bank, credit card and loan reconciliations, every period, without exception</li>
<li>A chart of accounts that separates the things you actually need separated, and stops there</li>
<li>Payroll entries agreed back to the filed payroll returns rather than to what the software assumed</li>
<li>Fixed assets recorded and depreciated on a schedule that will still make sense in eight years</li>
<li>Owner draws, contributions and loans posted where they belong instead of into a suspense account</li>
<li>Adjusting and closing entries at year end, so the tax return is prepared from books rather than around them</li>
</ul>

<h2>Financial statements</h2>
<p>We prepare financial statements for you from those records — a balance sheet, an income statement, and whatever supporting detail the reader needs. They are prepared for management use and for the lenders and other readers who accept statements prepared this way.</p>
<div class="callout"><p><strong>What we do not do.</strong> There are higher levels of financial statement service that carry a CPA firm&rsquo;s formal assurance, including audits and reviews. We do not perform them. If a bank, a bonding company, a franchisor or a funder specifically requires one, you need a firm that does that work, and we would rather tell you that plainly than talk you into something adjacent. Read the requirement itself before buying anything — it is common to be told to get statements from a CPA when what was actually required is far less than an audit.</p></div>

<h2>Clean-up engagements</h2>
<p>A great many small businesses arrive with books that drifted. A year of unreconciled accounts, personal spending mixed into the business, receivables nobody has aged, inventory that has never tied, or a conversion between accounting packages that quietly dropped the history. This is normal and it is fixable.</p>
<p>The work is to establish a defensible starting point, correct the periods that matter, and put a routine in place so it does not recur. What it costs depends almost entirely on how far back the correction has to go, which is the argument for raising it now rather than next year.</p>

<h2>How much you keep in house</h2>
<p>There is no single right answer. Some clients enter everything themselves and want a professional reviewing and closing each quarter. Others send us the statements and let us do the entry. Most sit in between — the business records what it knows, we handle the entries that need judgment, and both sides know exactly which is which. That boundary is worth writing down at the start of an engagement, because the expensive failures all happen where each side assumed the other had it.</p>

<h2>Why this matters more than it looks</h2>
<p>Books are not paperwork. They are the input to your tax return, your borrowing, your pricing, and eventually your sale. A lender reading a balance sheet with a large unexplained equity movement will ask about it. A buyer performing diligence will find the personal expenses. And a tax return prepared from records nobody reconciled is a return prepared on faith.</p>
''',
   faqs=[("Do you work in our accounting software?",
          "<p>Tell us what you use. Most small business packages are workable, and the choice matters far less than whether the file is reconciled and consistently coded. We are more interested in the state of the records than the brand on them.</p>"),
         ("Can you fix a year that was never closed properly?",
          "<p>Yes, and it is common. The first step is to establish a starting point that can be defended, then correct forward. Bring the bank statements — reconciliation is what makes the rest possible.</p>"),
         ("Will these financial statements satisfy our bank?",
          "<p>Often, but ask the bank what they actually require and get it in writing. Statements prepared by a CPA from your records are accepted by many lenders. If yours specifically requires an audited or reviewed statement, that is different work and we will tell you so rather than sending you something that does not meet the covenant.</p>"),
         ("How often should we close the books?",
          "<p>Monthly if you are managing on the numbers, carry inventory, or have a lender watching. Quarterly is enough for a stable business with straightforward operations. Annually is not really closing the books; it is preparing a tax return.</p>")],
   related=[('business-tax', 'Business tax preparation'),
            ('payroll', 'Payroll'),
            ('small-business-consulting', 'Small business consulting'),
            ('../calculators/break-even.html', 'Break-even calculator')]),

 dict(slug='payroll', ic='people', nav_title='Payroll',
   short='Payroll for small employers, and the federal and Massachusetts filings that follow it — including the state-specific pieces that catch new employers out.',
   title='Payroll Services for Small Employers | Wilmington, MA CPA',
   desc='Payroll support for Massachusetts small employers: pay runs, quarterly and annual filings, W-2 and 1099 preparation, and the state programs new employers miss.',
   eyebrow='Payroll', h1='Payroll is the one deadline that does not wait for you.',
   sub='Late or wrong payroll filings generate penalties faster than anything else a small business does, and they compound quietly.',
   body='''
<h2>The short answer</h2>
<p>We handle payroll work for small employers. How much of the cycle we run depends on the engagement: some clients want the whole thing, others run their own pay runs and want the quarterly and annual filings prepared, checked and reconciled by a CPA. Both are ordinary — the important part is that it is agreed in advance and nothing is left between us.</p>

<h2>What the cycle involves</h2>
<ul>
<li><strong>Pay runs.</strong> Gross to net, withholding, deductions, and the deposits that follow each run on the schedule the IRS assigned you.</li>
<li><strong>Quarterly filings.</strong> The federal employment tax return, state withholding, and unemployment reporting, reconciled against what was actually paid rather than what the software assumed.</li>
<li><strong>Year end.</strong> W-2s and the annual reconciliation, plus 1099-NEC forms for contractors. These are due to recipients and to the agencies in January, which is earlier than most owners have in mind.</li>
<li><strong>Reconciliation to the books.</strong> Payroll is the single most common place where the general ledger and the filed returns quietly disagree. Agreeing them each quarter costs minutes; agreeing them a year later costs hours.</li>
</ul>

<h2>The Massachusetts pieces</h2>
<p>Massachusetts adds obligations that a national payroll package will handle only if it has been set up correctly for this state, and that a new employer will otherwise not know about:</p>
<ul>
<li><strong>Paid Family and Medical Leave.</strong> Contributions are withheld and remitted quarterly, with rates and thresholds set each year, and the employer&rsquo;s share depends on headcount. Notices must be given to employees.</li>
<li><strong>Unemployment insurance.</strong> Registration with the state, quarterly wage reporting, and the health-related employer contributions that accompany it.</li>
<li><strong>New hire reporting.</strong> Required promptly after each hire, and easy to skip entirely if nobody told you it exists.</li>
<li><strong>Earned sick time.</strong> Massachusetts requires accrual, and accrual has to be tracked whether or not your payroll system was configured to track it.</li>
</ul>

<div class="callout"><p><strong>Worker classification is the expensive one.</strong> Massachusetts applies an unusually strict test for treating a worker as an independent contractor, and getting it wrong is not a small correction — it reaches back across payroll taxes, insurance and leave contributions. It is a legal question. Ask it before the first payment, and where it needs counsel, get counsel.</p></div>

<h2>Hiring your first employee</h2>
<p>The step from no employees to one employee is larger than the step from one to ten. It means federal and state registrations, a deposit schedule, workers&rsquo; compensation insurance, the state leave and unemployment programs, a hiring report, and a set of recurring deadlines that begin immediately. Most of the penalties we see against small employers are from the first two quarters, before anyone had the registrations in place.</p>
<p>If you are approaching that point, call before the first pay run rather than after it.</p>

<h2>When payroll has already gone wrong</h2>
<p>Missed deposits, unfiled quarters and mismatched W-2s are all correctable, and the correction is much easier while the amounts are small. Bring the notices — including the ones you have not opened. A notice is far easier to deal with before it is answered badly than after.</p>
''',
   faqs=[("Do we have to run payroll if the company is just me?",
          "<p>If your business is an S corporation and you work in it, you are an employee of it and reasonable compensation has to run through payroll. A sole proprietor or single-member LLC without an election does not pay themselves through payroll at all — draws are not wages. Which of those you are is worth confirming rather than assuming.</p>"),
         ("Can you just check what our payroll provider is doing?",
          "<p>Yes, and it is often the most useful version of this engagement. Providers process accurately; what they do not do is notice that a state registration is missing, that a worker is misclassified, or that the general ledger stopped agreeing with the filings two quarters ago.</p>"),
         ("When are W-2s and 1099s due?",
          "<p>January, to both recipients and the agencies. The practical deadline is earlier than that, because contractor details and address changes always take longer to collect than anyone plans for. Start in December.</p>"),
         ("What happens if we missed a quarterly filing?",
          "<p>File it. Penalties and interest accrue on the unfiled period and they compound, so the cheapest version of this problem is always today&rsquo;s version. Send the notices along with it.</p>")],
   related=[('bookkeeping-write-up', 'Bookkeeping &amp; write-up'),
            ('business-tax', 'Business tax preparation'),
            ('small-business-consulting', 'Small business consulting'),
            ('../regulatory-background.html', 'Regulatory background')]),

 dict(slug='small-business-consulting', ic='chart', nav_title='Small Business Consulting',
   short='Entity choice, pricing, cash flow, equipment purchases, hiring and exit — the questions that come up between filings.',
   title='Small Business Consulting | Wilmington, MA CPA Firm',
   desc='Small business consulting from a Wilmington CPA firm: entity choice, pricing and break-even, cash flow, equipment purchases, hiring, and preparing for a sale.',
   eyebrow='Consulting', h1='The decisions that move the number are made during the year.',
   sub='By the time a return is prepared it is a record of choices already made. The useful conversations happen earlier, and they are usually short.',
   body='''
<h2>The short answer</h2>
<p>Small business consulting here means the questions an owner brings between filings — usually with a decision attached and a deadline behind it. It is not a formal programme with a deliverable at the end. It is access to a CPA who already knows your numbers.</p>

<h2>What owners actually ask</h2>
<h3>Structure</h3>
<p>Should this be an S corporation? Should the building sit inside the operating company or outside it? Should the second line of business be a separate entity? Structure decisions are cheap to make and expensive to unwind, and the right answer depends on facts that change — profit level, payroll, state exposure, who else might one day own part of it.</p>

<h3>Pricing and margin</h3>
<p>A surprising number of small businesses do not know their contribution margin, which means they do not know what volume covers the overhead. Working out the break-even is an hour of arithmetic that frequently changes a pricing decision. Our <a href="../calculators/break-even.html">break-even calculator</a> is the starting point; the conversation about which costs are genuinely fixed is the valuable half.</p>

<h3>Cash flow</h3>
<p>Profitable businesses run out of cash. Growth consumes it, receivables absorb it, inventory hides it, and debt service takes it before anything else. A simple forward projection — not a model, a schedule — is usually enough to see the pinch point far enough ahead to do something about it.</p>

<h3>Equipment and financing</h3>
<p>What a purchase actually costs after tax, whether to finance or pay cash, and what a loan does to monthly cash flow. Both of those are arithmetic before they are judgement: see the <a href="../calculators/section-179.html">equipment purchase</a> and <a href="../calculators/loan-payment.html">loan payment</a> calculators.</p>

<h3>People</h3>
<p>Hiring the first employee, moving a contractor onto payroll, adding a benefit, or paying a family member working in the business. Each has a tax consequence and a compliance consequence, and in Massachusetts the classification question in particular is one to settle in advance.</p>

<h3>Getting out</h3>
<p>Selling, handing on to family, or winding up. What a buyer will look at, how the deal is structured, and what the tax outcome is under each structure. These conversations are most useful several years before the event, when the structure can still be changed.</p>

<div class="callout"><p><strong>Where we stop.</strong> We are accountants. Legal instruments, employment law questions and formal business valuations belong with the appropriate professional, and we will say so rather than improvising. Telling a client that a question is outside our work is part of the job.</p></div>

<h2>How to use us this way</h2>
<p>Call before the decision, not after it. A ten-minute conversation before you sign a lease, take on a partner, buy a vehicle, or hire the first employee is worth more than any amount of analysis afterwards. Clients who use a small firm well treat the phone number as the service.</p>
''',
   faqs=[("Is consulting a separate engagement?",
          "<p>It depends on the size of the question. A short call about a decision is part of an ongoing relationship. Work with a defined scope and a real deliverable is agreed separately, and we will tell you which one you are asking for before we start.</p>"),
         ("Can you help us decide whether to become an S corporation?",
          "<p>Yes, and it is one of the most common questions we get. It turns on profit level, how much of that profit is a return on your own labour, the payroll cost of doing it properly, state treatment, and how long you plan to keep the structure. It is arithmetic, not ideology.</p>"),
         ("Do you provide business valuations?",
          "<p>No. A formal valuation for a sale, a dispute or a gift filing is specialist work with its own standards, and it should be done by someone who does it regularly. We will help you understand what drives the number and prepare the records the valuer will ask for.</p>"),
         ("We are thinking about buying a business. Can you look at it?",
          "<p>Talk to us early. What we can usefully do — reading the financial records, testing the assumptions behind the asking price, and identifying what to ask for in diligence — depends on what the seller is willing to provide and on the timetable.</p>")],
   related=[('business-tax', 'Business tax preparation'),
            ('bookkeeping-write-up', 'Bookkeeping &amp; write-up'),
            ('../calculators/index.html', 'Calculators'),
            ('../about.html', 'About the firm')]),
]

CALC_SLUGS = ['self-employment-tax', 'section-179', 'break-even', 'loan-payment']
CALC_INTRO = {
 'self-employment-tax': (
   '<h2>Why this one matters most in year one</h2>'
   '<p>The first profitable year of self-employment is where the surprise lives. Income tax is expected; '
   'self-employment tax on top of it usually is not, and there is no employer withholding standing behind it. '
   'This estimate covers the Social Security and Medicare portion only. It is not your income tax, and it says '
   'nothing about your filing status, the qualified business income deduction, or Massachusetts.</p>'
   '<p>The practical use is setting aside money and sizing quarterly instalments. If the number here is larger '
   'than what you have been putting away, that gap is the conversation to have with us now rather than in April. '
   'See <a href="../services/individual-tax.html">individual tax preparation</a>.</p>'),
 'section-179': (
   '<h2>Before you sign the purchase order</h2>'
   '<p>A deduction is worth your tax rate, not the price of the asset. This shows what a fully deductible '
   'equipment purchase is actually worth against the rate you enter, and what the asset costs after tax.</p>'
   '<p>Two cautions the arithmetic cannot show you. First, an expensing election cannot create a loss — you need '
   'enough taxable income to absorb it, and annual limits and phase-outs apply. Second, Massachusetts does not '
   'always follow the federal treatment of accelerated deductions, so the state answer can differ from the federal '
   'one. Both are worth a call before the order goes in, not after. See '
   '<a href="../services/business-tax.html">business tax preparation</a>.</p>'),
 'break-even': (
   '<h2>The number most owners have never worked out</h2>'
   '<p>Break-even is the volume at which the business stops losing money. It falls straight out of three figures: '
   'fixed costs, price, and the variable cost of delivering one more unit. The arithmetic takes a minute. Deciding '
   'which of your costs are genuinely fixed is the part worth doing carefully — most businesses classify too much '
   'as fixed and conclude, wrongly, that they cannot afford to change anything.</p>'
   '<p>If the contribution margin is at or below zero, no volume rescues it. That is a pricing or a cost problem, '
   'and volume will make it worse. See <a href="../services/small-business-consulting.html">small business '
   'consulting</a>.</p>'),
 'loan-payment': (
   '<h2>What the borrowing actually costs</h2>'
   '<p>Lenders quote a monthly payment. This shows the payment, the total interest across the term, and what an '
   'extra amount each month does to the payoff date — which is usually the most surprising figure on the page.</p>'
   '<p>For a business borrowing to buy equipment, run this alongside the '
   '<a href="section-179.html">equipment purchase calculator</a>: the tax saving reduces the effective cost of the '
   'asset, while the loan spreads the cash outlay. They are different questions and they deserve separate answers. '
   'See <a href="../services/small-business-consulting.html">small business consulting</a>.</p>'),
}


# ============================================================================
def pages():
    P = []
    CALCS = [c for c in C.CALCULATORS if c['slug'] in CALC_SLUGS]

    # ---------------------------------------------------------------- HOME
    svc_cards = ''.join([
      _card(0, 'services/individual-tax.html', 'calc', 'Individual Tax Preparation',
            'Federal and Massachusetts returns for households, sole proprietors, landlords and retirees — prepared and signed by an owner of the firm.', '01'),
      _card(0, 'services/business-tax.html', 'building', 'Business Tax Preparation',
            'S corporations, partnerships, LLCs and sole proprietorships, with the corporate excise and pass-through questions Massachusetts adds.', '02'),
      _card(0, 'services/bookkeeping-write-up.html', 'ledger', 'Bookkeeping &amp; Write-Up',
            'Monthly and quarterly write-up, reconciliations, adjusting entries, and financial statements prepared from your records.', '03'),
      _card(0, 'services/payroll.html', 'people', 'Payroll',
            'Pay runs, quarterly and annual filings, W-2s and 1099s, and the Massachusetts programmes new employers routinely miss.', '04'),
      _card(0, 'services/small-business-consulting.html', 'chart', 'Small Business Consulting',
            'Entity choice, pricing, cash flow, equipment purchases and hiring — the questions that arrive between filings.', '05'),
    ])
    people = (_person_card(0, 'marvin-h-dorfman', 'MD', 'Marvin H. Dorfman', 'CPA &middot; Owner',
                'Formed Dorfman &amp; Dorfman in 2008 after four years in his own practice, and before that was a senior partner at Dorfman &amp; Goldstein, CPAs. Bentley College.')
              + _person_card(0, 'estee-c-dorfman', 'ED', 'Estee C. Dorfman', 'CPA, MSA &middot; Owner',
                'Co-founded the firm in 2008. Formerly a Principal Examiner at FINRA, the regulator of the securities industry. Bentley College and Suffolk University.'))

    body = (
      '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" aria-hidden="true">' + GLYPH + '</svg>'
      '<div class="wrap"><div class="reveal in">'
      '<span class="eyebrow on-dark">Certified Public Accountants &middot; Wilmington, Massachusetts</span>'
      '<h1>A firm of two, which is why you always get a CPA.</h1>'
      '<p class="sub">Dorfman &amp; Dorfman is a family-owned CPA firm on Main Street in Wilmington, formed in 2008, bringing over 30 years of public accounting experience to small businesses and individuals. Marvin and Estee own the firm and do the work.</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a>'
      '<a class="btn b-gh" href="services/index.html">See what we do ' + ARROW + '</a></div>'
      '<div class="hero-trust"><span><b>Established 2008</b></span><span><b>Family-owned</b></span>'
      '<span><b>Two CPAs</b>, no hand-offs</span><span><b>Wilmington</b>, Massachusetts</span></div>'
      '</div></div></section>'

      '<section class="strip"><div class="wrap reveal">'
      '<div class="cell"><div class="n">2008</div><div class="l">the year the firm was formed</div></div>'
      '<div class="cell"><div class="n">30+</div><div class="l">years of public accounting experience</div></div>'
      '<div class="cell"><div class="n">2</div><div class="l">CPAs &mdash; and they own the firm</div></div>'
      '<div class="cell"><div class="n">1</div><div class="l">office, on Main Street in Wilmington</div></div>'
      '</div></section>'

      '<section class="sec" id="services"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">What we do</span><h2>Accounting and tax for small businesses and individuals.</h2>'
      '<p class="lead">A short list, done properly. Most clients use two or three of these together, because for an owner-operated business the books, the payroll and the two tax returns are one continuous piece of work rather than five separate purchases.</p>'
      '</div><div class="cards">' + svc_cards + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">All services ' + ARROW + '</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split">'
      '<div class="reveal"><span class="eyebrow">Why a firm this size</span>'
      '<h2>Nobody here can hand your file to somebody else.</h2>'
      '<p class="lead">Small firms are often described as if size were a compromise. For accounting work it is frequently the opposite: the person who answers the phone is the person who prepared the return, and they remember why it was done that way.</p>'
      '<div class="prose" style="margin-top:26px">'
      '<h3>You speak to an owner, every time</h3>'
      '<p>There are two of us. There is no account manager, no seasonal preparer who will not be here next year, and no layer between the question and the answer. When something changes in your business in July, the call goes to the person who will be preparing the return in March.</p>'
      '<h3>The whole picture, in one place</h3>'
      '<p>Most of our business clients also have their personal returns prepared here. That is not upselling; it is the only way the planning holds together. Owner compensation, distributions, basis, and the timing of income between the company and the household are one calculation, and splitting it between two firms is how opportunities get missed.</p>'
      '<h3>A regulator&rsquo;s eye for documentation</h3>'
      '<p>Estee Dorfman was a Principal Examiner at FINRA, the body that regulates securities firms in the United States, before co-founding this practice. Examination work teaches something specific: the difference between a position that is correct and a position that can be shown to be correct, years later, to somebody with no reason to take your word for it. <a href="regulatory-background.html">What that means for a client here</a>.</p>'
      '<h3>We will tell you what we do not do</h3>'
      '<p>We prepare accounting records, financial statements and tax returns. We do not perform audits, and we are not the right firm for every engagement. Being told that early is worth more than being taken on regardless.</p>'
      '</div></div>'
      '<div class="aside"><div class="acard"><div class="t">Talk to a CPA</div>'
      '<p>Describe the situation in five minutes. If we are the right firm for it, we will tell you what the work involves. If we are not, we will tell you that too.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">The firm</div><ul>'
      '<li><a href="about.html"><span class="ck">&rarr;</span> Family-owned, formed 2008</a></li>'
      '<li><a href="team/marvin-h-dorfman.html"><span class="ck">&rarr;</span> Marvin H. Dorfman, CPA</a></li>'
      '<li><a href="team/estee-c-dorfman.html"><span class="ck">&rarr;</span> Estee C. Dorfman, CPA, MSA</a></li>'
      '<li><a href="regulatory-background.html"><span class="ck">&rarr;</span> Regulatory background</a></li>'
      '<li><a href="calculators/index.html"><span class="ck">&rarr;</span> Calculators</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">The people</span><h2>Two owners. Both CPAs. Both named on the door.</h2>'
      '<p class="lead">Dorfman &amp; Dorfman is family-owned, and the family are the practitioners. Between them the firm carries over 30 years of public accounting experience.</p>'
      '</div><div class="cards two">' + people + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="about.html">About the firm ' + ARROW + '</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Run the numbers</span><h2>Four calculators, on our own page.</h2>'
      '<p class="lead">Self-employment tax, an equipment purchase, a break-even point, a loan payoff. They run entirely in your browser — nothing is sent anywhere, nothing is stored, and you are not handed off to a third-party site to use them.</p></div>'
      '<div class="cards">'
      + _card(0, 'calculators/self-employment-tax.html', 'calc', 'Self-employment tax',
              'What the Social Security and Medicare portion costs on net self-employment profit, and roughly what each quarterly instalment should be.')
      + _card(0, 'calculators/section-179.html', 'vault', 'Equipment purchase',
              'What a fully deductible equipment purchase is worth against your rate, and what the asset actually costs after tax.')
      + _card(0, 'calculators/break-even.html', 'chart', 'Break-even point',
              'The volume and revenue at which the business stops losing money, and what it takes to hit a target profit.')
      + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="calculators/index.html">All calculators ' + ARROW + '</a></p></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Where we are</span><h2>402 Main Street, Wilmington.</h2>'
      '<p class="lead">One office, north of Boston in Middlesex County, a few minutes from the neighbouring towns of Woburn, Reading, North Reading, Burlington, Billerica and Tewksbury.</p></div>'
      '<div class="split">'
      '<div>' + gmap('402 Main Street, Suite #2, Wilmington, Massachusetts 01887.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + FIRM['ph'] + ', extension 11<br>Facsimile ' + FIRM['fax'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Getting in touch</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Open in Google Maps</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the firm</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Common questions</span><h2>Answers before you call.</h2></div>'
      + faq_html(HOME_FAQS) +
      '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">More questions answered ' + ARROW + '</a></p></div></section>'
    )
    P.append(dict(path='index.html', depth=0, nav='home',
      title='Dorfman & Dorfman, CPAs | CPAs in Wilmington, Massachusetts',
      desc='A family-owned, two-person CPA firm in Wilmington, Massachusetts. Accounting and tax services for small businesses and individuals since 2008.',
      body=body, cta_args=CTA,
      schema=[org(),
              {"@context": "https://schema.org", "@type": "WebSite", "name": FIRM['name'],
               "url": BASE, "publisher": {"@id": ORG_ID}},
              faq_schema([(q, _plain(a)) for q, a in HOME_FAQS])]))

    # ---------------------------------------------------------------- ABOUT
    p = dict(path='about.html', depth=0, nav='about',
      title='About the Firm | Dorfman & Dorfman, CPAs | Wilmington, MA',
      desc='Dorfman & Dorfman, CPAs was formed in Wilmington in 2008 by Marvin and Estee Dorfman. A family-owned, two-person practice serving small businesses and individuals.',
      eyebrow='About the firm', h1='A family firm, formed in 2008, still run by the family.',
      sub='Marvin H. Dorfman, CPA and Estee C. Dorfman, CPA, MSA co-founded Dorfman &amp; Dorfman and have run it together since.')
    p['body'] = phero(p, [('About the firm', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>Marvin Dorfman had already spent a long career in public accounting before this firm existed. He was a senior partner at Dorfman &amp; Goldstein, CPAs until 2004, and practised on his own from 2004 until 2008. In 2008 he and Estee Dorfman formed Dorfman &amp; Dorfman, CPAs.</p>'
      '<p>Estee co-founded the firm that same year, after a period as a Principal Examiner at FINRA. She holds the CPA licence and an MSA, and studied at Bentley College and Suffolk University. Marvin is also a Bentley College graduate.</p>'
      '<p>The firm is family-owned. That is not a marketing description here; it is the operating model. There are two accountants, both owners, and between them the practice brings over 30 years of public accounting experience.</p>'

      '<h2>What we do, and what we do not</h2>'
      '<p>We provide accounting and tax services to small businesses and individuals. In practice that means five things: <a href="services/individual-tax.html">individual tax preparation</a>, <a href="services/business-tax.html">business tax preparation</a>, <a href="services/bookkeeping-write-up.html">bookkeeping, write-up and financial statement preparation</a>, <a href="services/payroll.html">payroll</a>, and <a href="services/small-business-consulting.html">small business consulting</a>.</p>'
      '<p>We do not perform audits. There are levels of financial statement service that carry a CPA firm&rsquo;s formal assurance, and they are specialist work with their own standards; if a lender or a funder requires one, you need a firm that does that work. We would rather say so at the first call than take an engagement we should not.</p>'

      '<h2>How a two-person firm behaves differently</h2>'
      '<h3>There is no second tier</h3>'
      '<p>Every client here is worked on by an owner. That has a practical consequence beyond the pleasant one: nothing has to be explained twice, and no context is lost between the person who took the call and the person doing the work.</p>'
      '<h3>We keep the client base to what two people can do properly</h3>'
      '<p>The constraint is deliberate. A firm of this size that takes on more than it can carry produces late work, and late work in this profession is expensive for the client, not for the firm.</p>'
      '<h3>The business and the household are one conversation</h3>'
      '<p>For an owner-operated company the entity return, the owner&rsquo;s return, payroll and the books all touch each other. Handling them together is the whole argument for using one small firm rather than several specialists.</p>'

      '<h2>Wilmington</h2>'
      '<p>The office is at 402 Main Street, Suite #2, in Wilmington — Middlesex County, north of Boston, next to Woburn, Reading, North Reading, Burlington, Billerica and Tewksbury. Most clients are within a short drive, though for the majority of the work nobody needs to be in the same room.</p>'

      '<h2>Where to go next</h2>'
      '<p>The <a href="services/index.html">services pages</a> describe each area in detail. The bios of <a href="team/marvin-h-dorfman.html">Marvin</a> and <a href="team/estee-c-dorfman.html">Estee</a> set out their backgrounds. The page on <a href="regulatory-background.html">regulatory background</a> explains what Estee&rsquo;s examination experience means in practice for a client here.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Firm at a glance</div>'
      '<p><strong style="color:#fff">Formed</strong><br>2008</p>'
      '<p><strong style="color:#fff">Ownership</strong><br>Family-owned, two owners</p>'
      '<p><strong style="color:#fff">Office</strong><br>Wilmington, Massachusetts</p>'
      '<p><strong style="color:#fff">Clients</strong><br>Small businesses and individuals</p>'
      '<a class="btn b-acc" href="contact.html">Contact the firm</a></div>'
      '<div class="acard light"><div class="t">The two of us</div><ul>'
      '<li><a href="team/marvin-h-dorfman.html"><span class="ck">&rarr;</span> Marvin H. Dorfman, CPA</a></li>'
      '<li><a href="team/estee-c-dorfman.html"><span class="ck">&rarr;</span> Estee C. Dorfman, CPA, MSA</a></li>'
      '<li><a href="regulatory-background.html"><span class="ck">&rarr;</span> Regulatory background</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(), breadcrumb_schema([('Home', BASE), ('About the firm', BASE + 'about.html')])]
    P.append(p)

    # ---------------------------------------------------------------- BIOS
    p = dict(path='team/marvin-h-dorfman.html', depth=1, nav='about',
      title='Marvin H. Dorfman, CPA | Owner | Dorfman & Dorfman, CPAs',
      desc='Marvin H. Dorfman, CPA is an owner of Dorfman & Dorfman, CPAs in Wilmington, Massachusetts. Formerly a senior partner at Dorfman & Goldstein, CPAs.',
      eyebrow='Marvin H. Dorfman', h1='Marvin H. Dorfman, CPA',
      sub='Owner &middot; formed Dorfman &amp; Dorfman, CPAs in 2008')
    p['body'] = phero(p, [('About the firm', 'about.html'), ('Marvin H. Dorfman', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Background</h2>'
      '<p>Marvin Dorfman is a Certified Public Accountant and an owner of this firm. He was a senior partner at Dorfman &amp; Goldstein, CPAs until 2004, practised as a sole practitioner from 2004 until 2008, and in 2008 formed Dorfman &amp; Dorfman, CPAs. He is a graduate of Bentley College.</p>'
      '<p>That is a long run in one profession and largely in one part of it: small businesses and the people who own them. It is a practice built on returning clients rather than on volume.</p>'

      '<h2>The work</h2>'
      '<p>At a firm of two the division of labour is practical rather than formal. Marvin works across the whole of what the firm does — <a href="../services/individual-tax.html">individual</a> and <a href="../services/business-tax.html">business tax preparation</a>, <a href="../services/bookkeeping-write-up.html">bookkeeping and write-up work</a>, <a href="../services/payroll.html">payroll</a>, and the <a href="../services/small-business-consulting.html">consulting questions</a> that arrive between filings.</p>'
      '<p>What a career of this length actually gives a client is pattern recognition. The owner asking whether to incorporate, whether to buy or lease the truck, whether to put the second location in the same entity, or how to bring a child into the business is asking a question that has been asked before, in a hundred variations, with the same three or four factors deciding it. Knowing which of those factors matters in this case is the work.</p>'

      '<h2>Continuity</h2>'
      '<p>There is a specific benefit to a client in an accountant with a long tenure and a small practice: the depreciation schedule, the basis history, the election made in 2011 and the reason for it are all in the same head that will prepare next year&rsquo;s return. Most of the expensive errors we see on incoming client files are not arithmetic. They are things that were carried forward wrongly by somebody who was not there when the decision was made.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Marvin H. Dorfman, CPA</div>'
      '<p><strong style="color:#fff">Role</strong><br>Owner</p>'
      '<p><strong style="color:#fff">Previously</strong><br>Senior partner, Dorfman &amp; Goldstein, CPAs, until 2004<br>Sole practitioner, 2004&ndash;2008</p>'
      '<p><strong style="color:#fff">Education</strong><br>Bentley College</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Also here</div><ul>'
      '<li><a href="estee-c-dorfman.html"><span class="ck">&rarr;</span> Estee C. Dorfman, CPA, MSA</a></li>'
      '<li><a href="../about.html"><span class="ck">&rarr;</span> About the firm</a></li>'
      '<li><a href="../services/index.html"><span class="ck">&rarr;</span> All services</a></li>'
      '<li><a href="../contact.html"><span class="ck">&rarr;</span> Contact</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(),
      breadcrumb_schema([('Home', BASE), ('About the firm', BASE + 'about.html'),
                         ('Marvin H. Dorfman', BASE + 'team/marvin-h-dorfman.html')]),
      {"@context": "https://schema.org", "@type": "Person", "name": "Marvin H. Dorfman",
       "honorificSuffix": "CPA", "jobTitle": "Owner", "alumniOf": "Bentley College",
       "url": BASE + 'team/marvin-h-dorfman.html', "worksFor": {"@id": ORG_ID}}]
    P.append(p)

    p = dict(path='team/estee-c-dorfman.html', depth=1, nav='about',
      title='Estee C. Dorfman, CPA, MSA | Owner | Dorfman & Dorfman, CPAs',
      desc='Estee C. Dorfman, CPA, MSA co-founded Dorfman & Dorfman, CPAs in 2008. She was formerly a Principal Examiner at FINRA, the securities industry regulator.',
      eyebrow='Estee C. Dorfman', h1='Estee C. Dorfman, CPA, MSA',
      sub='Owner &middot; co-founded Dorfman &amp; Dorfman, CPAs in 2008 &middot; formerly a Principal Examiner at FINRA')
    p['body'] = phero(p, [('About the firm', 'about.html'), ('Estee C. Dorfman', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Background</h2>'
      '<p>Estee Dorfman is a Certified Public Accountant, holds an MSA, and co-founded Dorfman &amp; Dorfman, CPAs in 2008. She studied at Bentley College and Suffolk University. Before co-founding the firm she was a Principal Examiner at FINRA.</p>'
      '<p>FINRA is the self-regulatory organisation that oversees broker-dealers in the United States. Its examiners review member firms against FINRA rules and the federal securities laws — reading records, testing whether what a firm says it does is what it actually does, and documenting the difference. That is an unusual background for the owner of a small accounting practice, and it shows in how the work here is done.</p>'

      '<h2>What an examination background changes</h2>'
      '<p>Examination work teaches a specific discipline: the gap between a position that is correct and a position that can be <em>demonstrated</em> to be correct, later, to somebody with no reason to take your word for it. Those are not the same thing, and the second one is what protects a client when a return or a set of records is questioned.</p>'
      '<p>In practice that shows up as ordinary habits rather than as a service line. Support kept with the entry rather than located later. Reconciliations that are actually done. A file that tells a coherent story about why a position was taken. Records built so that a third party reading them cold reaches the same conclusion you did.</p>'
      '<p>There is a fuller account of what that means for a client on the <a href="../regulatory-background.html">regulatory background</a> page — including a clear statement of what this firm does <em>not</em> do.</p>'

      '<h2>The work here</h2>'
      '<p>Estee works across the firm&rsquo;s service list: <a href="../services/individual-tax.html">individual</a> and <a href="../services/business-tax.html">business tax preparation</a>, <a href="../services/bookkeeping-write-up.html">bookkeeping, write-up and financial statement preparation</a>, <a href="../services/payroll.html">payroll</a>, and <a href="../services/small-business-consulting.html">small business consulting</a>. Her email address is the one the firm publishes, so a note sent to the office reaches her directly.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Estee C. Dorfman, CPA, MSA</div>'
      '<p><strong style="color:#fff">Role</strong><br>Owner and co-founder, 2008</p>'
      '<p><strong style="color:#fff">Previously</strong><br>Principal Examiner, FINRA</p>'
      '<p><strong style="color:#fff">Education</strong><br>Bentley College<br>Suffolk University</p>'
      '<a class="btn b-acc" href="mailto:' + FIRM['email'] + '">Email Estee</a></div>'
      '<div class="acard light"><div class="t">Also here</div><ul>'
      '<li><a href="marvin-h-dorfman.html"><span class="ck">&rarr;</span> Marvin H. Dorfman, CPA</a></li>'
      '<li><a href="../regulatory-background.html"><span class="ck">&rarr;</span> Regulatory background</a></li>'
      '<li><a href="../about.html"><span class="ck">&rarr;</span> About the firm</a></li>'
      '<li><a href="../contact.html"><span class="ck">&rarr;</span> Contact</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(),
      breadcrumb_schema([('Home', BASE), ('About the firm', BASE + 'about.html'),
                         ('Estee C. Dorfman', BASE + 'team/estee-c-dorfman.html')]),
      {"@context": "https://schema.org", "@type": "Person", "name": "Estee C. Dorfman",
       "honorificSuffix": "CPA, MSA", "jobTitle": "Owner",
       "alumniOf": ["Bentley College", "Suffolk University"],
       "url": BASE + 'team/estee-c-dorfman.html', "worksFor": {"@id": ORG_ID},
       "email": FIRM['email']}]
    P.append(p)

    # ---------------------------------------------------------- REGULATORY
    reg_faqs = [
      ("Does the firm provide securities compliance services?",
       "<p>No. Dorfman &amp; Dorfman provides accounting and tax services. Regulatory filings, compliance programmes, supervisory procedures and anything requiring a securities licence are outside what this firm does, and where a client needs them we will say so rather than improvise.</p>"),
      ("Does the firm audit broker-dealers, or anyone else?",
       "<p>No. We do not perform audits. Financial statements prepared here are prepared from your records for management and for readers who accept statements on that basis. Where a formal assurance engagement is required, that is a different firm&rsquo;s work.</p>"),
      ("So what does the FINRA background actually give a client?",
       "<p>A way of working, not a product. Records built to be read by an outsider, support kept with the entry, reconciliations genuinely performed, and a documented reason for positions that need one. It is most valuable in the situations nobody plans for: a notice, an examination, a lender&rsquo;s diligence request, or a buyer&rsquo;s accountant going through five years of history.</p>"),
      ("Is this only relevant to clients in financial services?",
       "<p>No. It happens to be useful for people who work in or around a regulated industry, because the recordkeeping expectations are familiar. But the underlying discipline &mdash; that a record has to satisfy somebody other than the person who made it &mdash; applies to a landscaping company as much as to a registered representative.</p>"),
      ("What should I do if I receive a notice from the IRS or the state?",
       "<p>Call before you reply to it. A notice answered quickly and badly is much harder to unwind than a notice answered properly a week later, and a meaningful number of them are simply wrong on their face.</p>"),
    ]
    p = dict(path='regulatory-background.html', depth=0, nav='regulatory',
      title='Regulatory Background | Dorfman & Dorfman, CPAs | Wilmington MA',
      desc='An owner of Dorfman & Dorfman was a Principal Examiner at FINRA. What that regulatory background means for a small business or individual client, and what it does not.',
      eyebrow='Regulatory background', h1='What a former regulator brings to a small accounting practice.',
      sub='Estee Dorfman was a Principal Examiner at FINRA before co-founding this firm. Here is the honest version of what that is worth to a client &mdash; and what it is not.')
    p['body'] = phero(p, [('Regulatory background', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>The fact itself</h2>'
      '<p>Before co-founding Dorfman &amp; Dorfman, CPAs in 2008, <a href="team/estee-c-dorfman.html">Estee C. Dorfman, CPA, MSA</a> was a Principal Examiner at FINRA — the self-regulatory organisation that oversees broker-dealers in the United States. FINRA examiners review member firms against FINRA rules and the federal securities laws.</p>'
      '<p>Very few two-person accounting firms have someone who has spent time on the regulator&rsquo;s side of the table. It is worth explaining what that actually changes, because the honest answer is more specific and more useful than a vague appeal to experience.</p>'

      '<div class="callout"><p><strong>The boundary, stated plainly.</strong> This firm provides accounting and tax services. It does not perform audits. It does not provide securities compliance, regulatory filing, supervisory or legal services, and it does not hold itself out as a substitute for a compliance professional or an attorney. The examination background described on this page informs <em>how the accounting and tax work is done</em>. It is not a separate service line, and nothing here should be read as an offer of one.</p></div>'

      '<h2>What examiners spend their time doing</h2>'
      '<p>An examination is, at bottom, an exercise in reading records made by other people and deciding whether those records support what the records say happened. The examiner has no relationship with the firm, was not there at the time, and cannot be persuaded by tone of voice. Everything turns on whether the documentation stands on its own.</p>'
      '<p>Anyone who has done that work for long enough stops thinking of documentation as administration. It becomes the point. And that habit does not switch off when the same person moves to preparing records instead of reading them.</p>'

      '<h2>Three things it changes about the work here</h2>'
      '<h3>1. Correct and demonstrably correct are different standards</h3>'
      '<p>Plenty of tax positions are right. Fewer are documented well enough that a stranger reading the file in three years would agree without a conversation. That gap is invisible until the moment it matters, and it matters exactly when you least want it to: a notice, an examination, a lender&rsquo;s diligence, a divorce, or a buyer&rsquo;s accountant going through five years of history.</p>'
      '<p>The practical consequence is boring and valuable: support kept with the entry rather than reconstructed later, a note in the file explaining why a position was taken, and reconciliations that were genuinely performed rather than marked as performed.</p>'

      '<h3>2. Records are written for a reader who is not you</h3>'
      '<p>Small business books are usually built for the person who made them. That is fine until somebody else has to read them — a lender, a buyer, an agency, or the accountant who takes over. A record built for an outside reader survives all four of those events; one built for its author survives none of them.</p>'
      '<p>This shows up in the way we structure a chart of accounts, in the insistence on reconciliations, and in refusing to let a suspense account become permanent furniture. See <a href="services/bookkeeping-write-up.html">bookkeeping and write-up</a>.</p>'

      '<h3>3. A calm view of what an agency actually does</h3>'
      '<p>Most notices are routine, many are automated, and a meaningful proportion are simply wrong. Someone who has worked inside a regulator is less likely to panic and less likely to be careless — those are different failure modes with the same cause, which is not knowing what the letter means. If a notice arrives, the useful first step is to send it over before answering it.</p>'

      '<h2>Who tends to find this relevant</h2>'
      '<ul>'
      '<li><strong>People who work in or near a regulated industry.</strong> If you are a registered representative, an adviser, or an employee of a financial services firm, your own return has features that are worth someone understanding — the mix of W-2 and 1099 income, deferred and equity compensation, expense reimbursement arrangements, and the recordkeeping expectations your employer imposes on you personally.</li>'
      '<li><strong>Businesses that will be examined by somebody, eventually.</strong> Any employer can be reviewed on payroll or worker classification; any business collecting sales tax can be reviewed on it. See <a href="services/payroll.html">payroll</a>.</li>'
      '<li><strong>Owners who intend to sell one day.</strong> Diligence is an examination conducted by someone with a financial interest in finding problems. The records that survive it are built years earlier. See <a href="services/small-business-consulting.html">small business consulting</a>.</li>'
      '<li><strong>Anyone who has had a bad experience with a notice.</strong> Usually the underlying position was fine and the file could not show it.</li>'
      '</ul>'

      '<h2>Questions about this</h2>'
      + faq_html(reg_faqs) +
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">The short version</div>'
      '<p>A former FINRA examiner co-owns this firm. It changes how records and returns are documented. It is not a compliance service, and this firm does not perform audits.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="team/estee-c-dorfman.html"><span class="ck">&rarr;</span> Estee C. Dorfman, CPA, MSA</a></li>'
      '<li><a href="services/bookkeeping-write-up.html"><span class="ck">&rarr;</span> Bookkeeping &amp; write-up</a></li>'
      '<li><a href="services/payroll.html"><span class="ck">&rarr;</span> Payroll</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = ('Ask what this means for your situation.',
                     'Call (781) 780-7069, extension 11, or write to estee@dorfman-cpas.com. '
                     'If the question belongs with a compliance professional or an attorney rather than '
                     'with an accountant, we will tell you that.')
    p['schema'] = [org(),
      breadcrumb_schema([('Home', BASE), ('Regulatory background', BASE + 'regulatory-background.html')]),
      faq_schema([(q, _plain(a)) for q, a in reg_faqs])]
    P.append(p)

    # ---------------------------------------------------------- SERVICES HUB
    hub_cards = ''.join(_card(0, s['slug'] + '.html', s['ic'], s['nav_title'], s['short'],
                              '%02d' % (i + 1)) for i, s in enumerate(SERVICES))
    p = dict(path='services/index.html', depth=1, nav='services',
      title='Services | Dorfman & Dorfman, CPAs | Wilmington, Massachusetts',
      desc='Accounting and tax services for small businesses and individuals: tax preparation, bookkeeping and write-up, financial statements, payroll, and consulting.',
      eyebrow='Services', h1='Accounting and tax for small businesses and individuals.',
      sub='Five areas, and most clients use two or three of them together. For an owner-operated business they are one continuous piece of work.')
    p['body'] = phero(p, [('Services', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>What the firm does</h2>'
      '<p class="lead">A deliberately short list. Two CPAs can do a limited number of things properly, and a small firm that tries to offer everything is really offering nothing in particular.</p>'
      '</div><div class="cards">' + hub_cards + '</div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>How these fit together</h2>'
      '<p>Most of our business clients use a combination rather than a single service, and the combination is the point. The books produce the financial statements. The financial statements produce the business return. The business return produces the K-1 that drives the owner&rsquo;s personal return. Payroll sits inside all of it and has to agree with the books every quarter.</p>'
      '<p>When one firm handles the whole chain, the reconciliations happen automatically because the same people are looking at both ends. When it is split between a bookkeeper, a payroll provider and two different tax preparers, the reconciliation is nobody&rsquo;s job — and it is normally discovered by a lender or an agency rather than by anyone on your side.</p>'
      '<h2>What we do not do</h2>'
      '<p>We do not perform audits. We do not provide legal advice, securities compliance services, or formal business valuations. Those are specialist engagements, and a firm this size that pretended otherwise would be doing a client no favours. Where a question belongs elsewhere, we will say so and, where we can, point you somewhere sensible.</p>'
      '<h2>Not sure which you need?</h2>'
      '<p>Call and describe the situation. Most first conversations take ten minutes and end with a clear answer about what the work involves — including, sometimes, that you need less than you thought.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Start with a call</div>'
      '<p>Tell us the entity type, roughly what the year looks like, and the deadline you are working against. That is normally enough for us to describe the engagement.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Useful next</div><ul>'
      '<li><a href="../calculators/index.html"><span class="ck">&rarr;</span> Calculators</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '<li><a href="../about.html"><span class="ck">&rarr;</span> About the firm</a></li>'
      '<li><a href="../contact.html"><span class="ck">&rarr;</span> Contact the firm</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(), breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/index.html')])]
    P.append(p)

    # ---------------------------------------------------------- SERVICE PAGES
    for s in SERVICES:
      rel_items = ''.join('<li><a href="' + (h if h.endswith('.html') else h + '.html') + '">'
                          '<span class="ck">&rarr;</span> ' + l + '</a></li>' for h, l in s['related'])
      p = dict(path='services/' + s['slug'] + '.html', depth=1, nav='services',
               title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'])
      p['body'] = phero(p, [('Services', 'services/index.html'), (_plain(s['nav_title']), None)]) + (
        '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
        + s['body'] +
        '<h2>Questions</h2>' + faq_html(s['faqs']) +
        '</div>'
        '<div class="aside"><div class="acard"><div class="t">Talk it through</div>'
        '<p>Five minutes on the phone is usually enough to establish what the work involves and whether we are the right firm for it.</p>'
        '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
        '<div class="acard light"><div class="t">Related</div><ul>' + rel_items + '</ul></div>'
        '</div></div></div></section>')
      p['cta_args'] = CTA
      p['schema'] = [org(),
        breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/index.html'),
                           (_plain(s['nav_title']), BASE + 'services/' + s['slug'] + '.html')]),
        svc_schema(_plain(s['nav_title']), s['desc'], BASE + 'services/' + s['slug'] + '.html'),
        faq_schema([(_plain(q), _plain(a)) for q, a in s['faqs']])]
      P.append(p)

    # ---------------------------------------------------------- CALCULATOR HUB
    cal_cards = ''.join(
      '<a class="calccard reveal" href="' + c['slug'] + '.html">'
      '<div class="cc">' + c['cat'] + '</div><h3>' + c['title'] + '</h3>'
      '<p>' + c['blurb'] + '</p></a>' for c in CALCS)
    p = dict(path='calculators/index.html', depth=1, nav='calculators',
      title='Calculators | Dorfman & Dorfman, CPAs | Wilmington, MA',
      desc='Four financial calculators for small businesses and individuals: self-employment tax, equipment purchases, break-even point, and loan payments. They run in your browser.',
      eyebrow='Calculators', h1='Four calculators, run on our page and nowhere else.',
      sub='Rough answers to the four questions clients ask most often. They calculate in your browser &mdash; nothing is sent anywhere and nothing is stored.')
    p['body'] = phero(p, [('Calculators', None)]) + (
      '<style>' + C.CALC_CSS + '</style>'
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Pick the question you are asking</h2>'
      '<p class="lead">Each of these is deliberately narrow. They give you an order of magnitude and a starting point for a conversation — not a filing position and not advice about your situation.</p>'
      '</div><div class="calcgrid">' + cal_cards + '</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>How to read the answers</h2>'
      '<p>Every one of these makes assumptions, and every one of them states its assumptions underneath the inputs. Read that note. A calculator that gives you a confident number without telling you what it ignored is worse than no calculator at all.</p>'
      '<p>Two things none of them account for: your filing status and the interaction between federal and Massachusetts treatment. Massachusetts does not always follow the federal rules — most visibly on accelerated deductions for equipment and on the treatment of short-term gains — so a federal answer is only ever half of a Massachusetts answer.</p>'
      '<h2>Nothing leaves your browser</h2>'
      '<p>These are written in plain JavaScript on this page. There is no third-party widget, no external script, no account, no cookie and no network request. Whatever you type stays on your machine, which is how a calculator on an accountant&rsquo;s website ought to work.</p>'
      '<h2>When the number matters</h2>'
      '<p>Call before you act on it. The cases where a calculator misleads are exactly the cases worth a conversation: the year you cross a threshold, the purchase that will not be fully deductible, the loan whose covenant matters more than its rate.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Check the number</div>'
      '<p>If a result surprises you, that is usually worth ten minutes on the phone before it becomes a decision.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related services</div><ul>'
      '<li><a href="../services/individual-tax.html"><span class="ck">&rarr;</span> Individual tax preparation</a></li>'
      '<li><a href="../services/business-tax.html"><span class="ck">&rarr;</span> Business tax preparation</a></li>'
      '<li><a href="../services/small-business-consulting.html"><span class="ck">&rarr;</span> Small business consulting</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(), breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/index.html')])]
    P.append(p)

    # ---------------------------------------------------------- CALCULATORS
    CDESC = {
     'self-employment-tax': 'Estimate the Social Security and Medicare tax on net self-employment profit, with the deductible half and a rough quarterly instalment broken out.',
     'section-179': 'Work out what a deductible equipment purchase is worth against your combined tax rate, and what the asset actually costs your business after tax.',
     'break-even': 'Work out the unit volume and revenue at which your business stops losing money, and what it takes to reach a target monthly profit.',
     'loan-payment': 'Work out a business or personal loan payment, the total interest across the term, and how much an extra monthly amount shortens the payoff.',
    }
    CTITLE = {
     'self-employment-tax': 'Self-Employment Tax Calculator | Dorfman & Dorfman, CPAs',
     'section-179': 'Equipment Purchase Tax Calculator | Dorfman & Dorfman, CPAs',
     'break-even': 'Break-Even Point Calculator | Dorfman & Dorfman, CPAs',
     'loan-payment': 'Loan Payment Calculator | Dorfman & Dorfman, CPAs',
    }
    CSUB = {
     'self-employment-tax': 'Social Security and Medicare on self-employment earnings &mdash; the tax that catches out almost every first profitable year.',
     'section-179': 'What the deduction is worth against your rate, and what the equipment really costs once tax is taken into account.',
     'break-even': 'The volume at which the business stops losing money, and the volume that hits your target.',
     'loan-payment': 'The payment, the total interest, and what paying a little extra each month actually does.',
    }
    for c in CALCS:
      p = dict(path='calculators/' + c['slug'] + '.html', depth=1, nav='calculators',
               title=CTITLE[c['slug']], desc=CDESC[c['slug']],
               eyebrow='Calculator', h1=c['title'], sub=CSUB[c['slug']])
      hero = phero(p, [('Calculators', 'calculators/index.html'), (c['title'], None)])
      p['body'] = ('<style>' + C.CALC_CSS + '</style>'
                   + C.calc_page_body(c, hero, rel, ARROW, 1)
                   + '<section class="sec tint"><div class="wrap"><div class="prose reveal">'
                   + CALC_INTRO[c['slug']]
                   + '<h2>What this is not</h2>'
                   '<p>An estimate, not advice about your situation, and not a filing position. It does not know your filing status, your other income, your state treatment, or the facts that usually decide the answer. If the number here is going to drive a decision, call us before it does.</p>'
                   '<p><a href="index.html">All four calculators</a> &middot; <a href="../services/index.html">Services</a> &middot; <a href="../contact.html">Contact the firm</a></p>'
                   '</div></div></section>'
                   + C.CALC_JS)
      p['cta_args'] = CTA
      p['schema'] = [org(),
        breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/index.html'),
                           (c['title'], BASE + 'calculators/' + c['slug'] + '.html')])]
      P.append(p)

    # ---------------------------------------------------------------- FAQ
    p = dict(path='faq.html', depth=0, nav='about',
      title='Common Questions | Dorfman & Dorfman, CPAs | Wilmington, MA',
      desc='Straight answers about working with a small CPA firm in Wilmington, Massachusetts: fees, scope, switching accountants, notices, deadlines, and what we do not do.',
      eyebrow='Answers', h1='Questions we get asked, answered plainly.',
      sub='If yours is not here, call and ask. Nobody will route you to a form &mdash; there is not one on this site.')
    p['body'] = phero(p, [('Common questions', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Working with the firm</h2><p class="lead">Scope, engagement, and what to expect from a first call.</p></div>'
      + faq_html(FAQS) +
      '<div class="sec-head reveal" style="margin-top:56px"><h2>Still deciding?</h2>'
      '<p class="lead">The <a href="services/index.html">services pages</a> describe each area in detail, the '
      '<a href="regulatory-background.html">regulatory background</a> page explains what an examiner&rsquo;s '
      'training changes about how the work is done, and the <a href="calculators/index.html">calculators</a> '
      'will get you an order of magnitude before you call.</p></div>'
      '</div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Useful official sources</h2>'
      '<p>Two links worth having, and both are primary sources rather than commentary:</p>'
      '<ul>'
      '<li><a href="https://www.mass.gov/orgs/massachusetts-department-of-revenue" target="_blank" rel="noopener">Massachusetts Department of Revenue</a> &mdash; state tax forms, guidance, and online account access.</li>'
      '<li><a href="https://www.irs.gov/" target="_blank" rel="noopener">Internal Revenue Service</a> &mdash; federal forms, payment options, and the tools for checking a refund or a balance due.</li>'
      '</ul>'
      '<p>If a letter has arrived from either of them, send it to us before replying to it.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Ask the question</div>'
      '<p>Most first calls take ten minutes and end with a straight answer about whether we are the right firm.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> All services</a></li>'
      '<li><a href="about.html"><span class="ck">&rarr;</span> About the firm</a></li>'
      '<li><a href="calculators/index.html"><span class="ck">&rarr;</span> Calculators</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the firm</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(), breadcrumb_schema([('Home', BASE), ('Common questions', BASE + 'faq.html')]),
                   faq_schema([(q, _plain(a)) for q, a in FAQS])]
    P.append(p)

    # ---------------------------------------------------------------- CONTACT
    p = dict(path='contact.html', depth=0, nav='contact',
      title='Contact | Dorfman & Dorfman, CPAs | Wilmington, Massachusetts',
      desc='Reach Dorfman & Dorfman, CPAs at 402 Main Street, Suite #2, Wilmington MA. Telephone (781) 780-7069 extension 11, or email the firm directly.',
      eyebrow='Contact', h1='Call the office. A CPA answers.',
      sub='Tell us what you are working through and we will tell you whether we are the right firm for it.')
    p['body'] = phero(p, [('Contact', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Wilmington, Massachusetts</h2>'
      '<p class="lead">One office, two owners, and no switchboard between them and you.</p></div>'
      '<div class="split">'
      '<div>' + gmap('402 Main Street, Suite #2, Wilmington, Massachusetts 01887.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + FIRM['ph'] + ', extension 11<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Quick links</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Directions in Google Maps</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '<li><a href="team/estee-c-dorfman.html"><span class="ck">&rarr;</span> Estee C. Dorfman, CPA, MSA</a></li>'
      '<li><a href="team/marvin-h-dorfman.html"><span class="ck">&rarr;</span> Marvin H. Dorfman, CPA</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>What a first call is like</h2>'
      '<p>Ten minutes, usually. What kind of entity, roughly what the year looks like, and what deadline is driving the question. From that we can normally say whether it is a tax matter, a bookkeeping matter, a payroll matter, or a combination — and what the work involves.</p>'
      '<p>If the engagement belongs somewhere else, we will say so. A firm of two cannot take everything, and telling you early is more useful than taking the work and disappointing you in March.</p>'

      '<h2>What to have handy</h2>'
      '<ul><li>The most recently filed return — the entity return if you are calling about a business, last year&rsquo;s personal return otherwise</li>'
      '<li>Whatever the books currently look like, in whatever state they are in</li>'
      '<li>Anything with a date on it: a notice, a loan agreement, a lease, a letter of intent</li>'
      '<li>For a new business, the formation documents and the federal identification number</li></ul>'
      '<p>Missing pieces are not a problem. Call anyway.</p>'

      '<h2>Office hours</h2>'
      '<p>The firm does not publish set hours, and we would rather tell you that than invent them. Call the office at ' + FIRM['ph'] + ', extension 11, and if nobody picks up, leave a message or email ' + FIRM['email'] + '. Expect the pace to be different in the weeks before a filing deadline than in the middle of the summer.</p>'

      '<h2>Sending documents</h2>'
      '<p>There is no upload facility on this site, deliberately: this is a demonstration build and it collects nothing. Arrange with us how you would like to send records — post, in person, fax on ' + FIRM['fax'] + ', or an email attachment — and we will tell you what we need.</p>'

      '<h2>Confidentiality</h2>'
      '<p>Client information is confidential, including the fact that you called. That obligation sits in the professional rules governing a CPA licence; it is not a policy we adopted.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Prefer email?</div>'
      '<p>Write to the firm and one of the owners will reply.</p>'
      '<a class="btn b-acc" href="mailto:' + FIRM['email'] + '">' + FIRM['email'] + '</a></div>'
      '<div class="acard light"><div class="t">Before you call</div><ul>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> What we do</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '<li><a href="calculators/index.html"><span class="ck">&rarr;</span> Calculators</a></li>'
      '<li><a href="about.html"><span class="ck">&rarr;</span> About the firm</a></li>'
      '</ul></div></div></div></div></section>')
    p['cta_args'] = CTA
    p['schema'] = [org(), breadcrumb_schema([('Home', BASE), ('Contact', BASE + 'contact.html')]),
      {"@context": "https://schema.org", "@type": "ContactPage",
       "name": "Contact Dorfman & Dorfman, CPAs", "url": BASE + 'contact.html'}]
    P.append(p)

    return P


# ============================================================================
# FAQ CONTENT
# ============================================================================
HOME_FAQS = [
 ("Who will actually be doing my work?",
  "<p>Marvin or Estee. There are two of us and we both own the firm, so there is no junior preparer you never meet and no account manager between you and the work. The person who takes your call in July is the person preparing the return in March.</p>"),
 ("Do you perform audits?",
  "<p>No. We prepare accounting records, financial statements and tax returns. There are higher levels of financial statement service that carry a CPA firm&rsquo;s formal assurance, and we do not provide them. If a lender, a bonding company or a funder specifically requires one, you need a different firm, and we will tell you so at the first call rather than sell you something adjacent.</p>"),
 ("What does the work cost?",
  "<p>It depends on the engagement. An individual return is priced on complexity; recurring business work &mdash; books, payroll, the entity return &mdash; is normally settled for the year so it can be budgeted. Call and describe the situation and we will talk about what the work involves. The single largest variable is the condition of your records when we start, and that one is yours to control.</p>"),
 ("Can you handle both my business and my personal return?",
  "<p>Yes, and for an owner-operated business it is the point. Compensation, distributions, basis and the timing of income between the company and the household are one calculation. Splitting them between two firms is how planning opportunities get missed.</p>"),
 ("Are you taking new clients?",
  "<p>Call and ask. A firm of two has a real capacity limit and we would rather be honest about it than take on work we cannot do properly. If we are not the right firm for the engagement, we will say so.</p>"),
]

FAQS = HOME_FAQS + [
 ("How do I switch accountants without breaking anything?",
  "<p>It is more routine than it feels. What matters is the handover of documents: the last filed federal and state returns, the depreciation and fixed asset schedules, basis records, any elections made and when, payroll filings, and the accounting file itself. Those carry forward and they are what a new preparer has to build on. You are entitled to your own records; ask for them in writing and keep the request polite.</p>"),
 ("What is the difference between a CPA and an accountant?",
  "<p>Anyone may describe themselves as an accountant or a bookkeeper. A Certified Public Accountant has passed the Uniform CPA Examination, met a state&rsquo;s education and experience requirements, and holds an active licence &mdash; with continuing education and professional conduct rules attached to it. Both owners of this firm are CPAs.</p>"),
 ("When should a business owner start tax planning?",
  "<p>Before the year ends, and ideally before the transaction. Entity structure, owner compensation, the timing of income and expenses, equipment purchases and how they are financed, and retirement plan contributions are all decided during the year. By the filing deadline you are recording history rather than changing it.</p>"),
 ("Should my business be an S corporation?",
  "<p>Sometimes, and less often than the internet suggests. It turns on profit level, how much of that profit is genuinely a return on your own labour rather than on capital, the cost of running payroll properly, the Massachusetts treatment, and how long you expect to keep the structure. It is arithmetic, and it is worth redoing every few years because the answer changes as the business does.</p>"),
 ("A letter arrived from the IRS or the Department of Revenue. What now?",
  "<p>Send it over before you reply to it. Many notices are automated, a meaningful number are simply wrong, and nearly all of them are easier to resolve before an answer has been given than afterwards. Do not ignore it either &mdash; most have a response window, and the window is shorter than people assume.</p>"),
 ("Do you work with clients outside Wilmington?",
  "<p>Yes. The office is on Main Street in Wilmington and a good deal of the client base is nearby, but most of this work does not require anyone to be in the same room. Documents, calls and email cover the great majority of an engagement.</p>"),
 ("Is there a portal, or a way to settle an invoice through this site?",
  "<p>No, and that is deliberate. This demonstration build does not add systems the firm has not chosen for itself. Records are exchanged however you and the firm agree, and the calculators here run entirely in your own browser without sending anything anywhere.</p>"),
 ("What if my books are a mess?",
  "<p>That is a normal way to arrive and it is fixable. The first step is to establish a defensible starting point and correct forward from there. Bring the bank statements &mdash; reconciliation makes everything else possible. See <a href=\"services/bookkeeping-write-up.html\">bookkeeping and write-up</a>.</p>"),
 ("Can you help with a formal business valuation?",
  "<p>No. A valuation for a sale, a dispute or a gift tax filing is specialist work with its own professional standards and should be done by somebody who does it regularly. We will help you understand what drives the number and prepare the records the valuer will want.</p>"),
 ("Is my information confidential?",
  "<p>Yes. Client information is confidential, including the fact that you contacted us. That obligation comes from the professional rules governing a CPA licence rather than from an internal policy.</p>"),
]
