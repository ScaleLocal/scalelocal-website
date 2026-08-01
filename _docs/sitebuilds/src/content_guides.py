# -*- coding: utf-8 -*-
"""Three long-form guides — the AEO / question-intent layer."""
import html, re
from build import (FIRM, BASE, ARROW, phero, faq_html,
                   org_schema, breadcrumb_schema, faq_schema, article_schema)

def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()

GUIDES = [
 dict(slug='cpa-cost-small-business', nav_title='What a CPA costs a small business',
   title='How Much Does a CPA Cost for a Small Business? | KPW Illinois',
   desc='What actually drives CPA fees for a small business: fee structures, the factors that move the number, where owners overpay, and what to ask before engaging a firm.',
   eyebrow='Guide', h1='How much does a CPA cost for a small business?',
   sub='The honest answer is that it depends on five things — and any firm that quotes you before asking about them is guessing.',
   body='''
<div class="callout"><p><strong>Short answer:</strong> CPA fees are driven by the level of service required, the condition of your records, the complexity of your entity and filings, how much planning work you want, and the deadline you are working against. Fees are usually structured as a fixed fee per engagement, an hourly rate, or a monthly retainer. The single largest cost variable is the one you control: how clean your books are when the work starts.</p></div>

<h2>Why nobody can quote you from a web page</h2>
<p>Every published figure for "average CPA cost" is an average across returns that have nothing in common — a single-member LLC with one bank account and twelve transactions a month, and a multi-state S corporation with inventory, a benefit plan, and an equipment loan. The average of those two numbers describes neither business.</p>
<p>What is worth understanding is the structure of the pricing, because that lets you evaluate a quote instead of just comparing it.</p>

<h2>The five things that move the number</h2>
<h3>1. What level of service is actually required</h3>
<p>This is the largest single factor and the one most often gotten wrong. A compilation, a review, and an audit are three different products with three very different costs, and the requirement usually comes from outside — a lender, a bonding company, a grant agreement, a franchisor, or your own operating agreement.</p>
<p>Owners routinely pay for a level of service nobody asked them for, because at some point somebody said "we should probably get audited." Read the actual covenant before you buy the audit. Our <a href="audit-review-compilation.html">comparison guide</a> works through the distinction.</p>

<h3>2. The condition of your records</h3>
<p>This is the variable you control, and it changes fees more than anything else on this list. Reconciled accounts, a chart of accounts that separates what needs separating, supporting schedules for balance sheet accounts, and a person who can answer questions promptly all compress the hours required.</p>
<p>The reverse is also true. Unreconciled bank accounts, personal expenses mixed into the business, an accounts receivable balance nobody has aged in two years, and inventory that has never tied — every one of those becomes billable time, and it becomes billable time at professional rates rather than bookkeeping rates.</p>

<h3>3. Entity type and filing complexity</h3>
<p>A single-member LLC reported on a Schedule C is a different engagement from an S corporation with multiple shareholders, basis tracking, and a separate entity return that has to reconcile to each owner's individual return. Add states — every jurisdiction where you have nexus adds a filing, and multi-state allocation and apportionment work is genuinely technical.</p>
<p>Other complexity multipliers: inventory, fixed asset schedules with several years of depreciation history, related-party transactions, retirement plan filings, foreign accounts or activity, and any year in which you bought, sold, or restructured something.</p>

<h3>4. How much planning you want, versus compliance</h3>
<p>Preparing a return is compliance — recording what already happened. Planning is the work that changes the number, and it happens during the year. Planning costs more because it takes more time and more judgment. It is also the part of the relationship that most often pays for itself several times over, which is why comparing firms purely on preparation fees selects against the thing you most want.</p>

<h3>5. Timing</h3>
<p>Work delivered in January is cheaper to produce than the same work delivered in the week of the deadline, because the firm is not simultaneously serving every other client with the same deadline. Firms that price for rush work are not being opportunistic; they are pricing overtime honestly.</p>

<h2>How fees are usually structured</h2>
<table class="plain"><thead><tr><th>Structure</th><th>How it works</th><th>Best suited to</th></tr></thead><tbody>
<tr><td><strong>Fixed fee per engagement</strong></td><td>One price agreed for a defined scope</td><td>Tax returns, audits, valuations — anything with a definable deliverable</td></tr>
<tr><td><strong>Hourly</strong></td><td>Billed against actual time at professional rates</td><td>Advisory work, cleanup projects, and anything whose scope genuinely cannot be known in advance</td></tr>
<tr><td><strong>Monthly retainer</strong></td><td>A recurring fee covering an agreed bundle of recurring work</td><td>Ongoing accounting and reporting support where the volume is steady</td></tr>
</tbody></table>
<p>Fixed-fee arrangements are better for the client on defined work, because they move the estimation risk to the firm — which is the party in a position to estimate. Hourly is appropriate where nobody honestly knows the scope, and cleanup engagements are the common example.</p>

<h2>Where small businesses actually overpay</h2>
<ul>
<li><strong>Buying assurance nobody required.</strong> Paying audit fees when a compilation satisfies the requirement.</li>
<li><strong>Paying professional rates for bookkeeping.</strong> If a CPA firm is doing data entry, either the price is wrong or the process is. Day-to-day work belongs with a bookkeeper; the firm should be supervising, reviewing, and advising.</li>
<li><strong>Deferring cleanup indefinitely.</strong> Messy records do not cost you once. They cost you every year, on every engagement, and they inflate the cost of financing, diligence, and valuation as well.</li>
<li><strong>Buying preparation and skipping planning.</strong> The cheapest return in town is often the most expensive decision of the year.</li>
<li><strong>Changing firms to save a few hundred dollars.</strong> The first year with any new firm carries learning cost. Switching for a marginally lower preparation fee routinely costs more in year one than it saves.</li>
</ul>

<h2>What to ask before you engage anyone</h2>
<ol>
<li>What exactly is included, and what falls outside the quote?</li>
<li>What would cause this fee to change, and will I hear about it before the work happens?</li>
<li>Who will actually do the work, and who will I speak to when I have a question?</li>
<li>Is planning included, or is this preparation only?</li>
<li>What do you need from me to keep the fee at the low end of the range?</li>
<li>May I see your most recent peer review report? (For any firm doing audit, review, or attest work.)</li>
</ol>
<p>A firm that answers all six clearly is telling you something useful about how it operates.</p>

<div class="callout"><p><strong>Where we stand.</strong> We believe in offering fair and transparent prices, with no hidden fees or extra charges. Ask us the six questions above — we would rather answer them than have you guess.</p></div>

<h2>Related reading</h2>
<p><a href="audit-review-compilation.html">Audit, review, or compilation — which do you actually need?</a> &middot; <a href="choosing-a-cpa-firm.html">How to choose a CPA firm in Illinois</a> &middot; <a href="../services/tax-planning-preparation.html">Tax planning and preparation</a></p>
''',
   faqs=[("Is a CPA worth it for a very small business?",
          "<p>It depends on what you need. If your situation is a single-owner business with simple records and no planning questions, software plus a bookkeeper may be sufficient. The value of a CPA rises sharply with entity complexity, multi-state activity, employees and benefit plans, financing, and any transaction — and with the number of decisions you are making that have tax consequences.</p>"),
         ("Why do CPA quotes for the same work vary so much?",
          "<p>Usually because the firms are scoping different work. One quote may assume clean books and no planning; another may include cleanup, planning conversations, and support during the year. Compare what is included before comparing the numbers.</p>"),
         ("Can I lower my fee?",
          "<p>Yes, mostly through preparation. Reconcile accounts, keep business and personal separate, deliver requested items promptly, and consolidate questions rather than sending them one at a time. Timing helps too — earlier work is cheaper to produce.</p>"),
         ("Should I pay hourly or a fixed fee?",
          "<p>Fixed fee for anything with a definable deliverable, because it moves estimation risk to the party best able to estimate. Hourly is appropriate for cleanup and open-ended advisory work where the scope genuinely is unknown.</p>")]),

 dict(slug='audit-review-compilation', nav_title='Audit vs. review vs. compilation',
   title='Audit vs. Review vs. Compilation: Which Do You Need? | KPW',
   desc='A plain comparison of the three levels of financial statement service — assurance provided, procedures performed, cost, and who typically requires each.',
   eyebrow='Guide', h1='Audit, review, or compilation — which do you actually need?',
   sub='Three levels of service, three very different price points, and one question that answers it: who is requiring this, and what exactly did they ask for?',
   body='''
<div class="callout"><p><strong>Short answer:</strong> An audit provides reasonable assurance and involves testing, third-party confirmation, and evaluation of internal control. A review provides limited assurance through analytical procedures and inquiry. A compilation provides no assurance — it presents your figures in financial statement format. The level you need is almost always dictated by an outside party, so start by reading what they actually require.</p></div>

<h2>The comparison</h2>
<table class="plain"><thead><tr><th></th><th>Compilation</th><th>Review</th><th>Audit</th></tr></thead><tbody>
<tr><td><strong>Assurance</strong></td><td>None</td><td>Limited</td><td>Reasonable</td></tr>
<tr><td><strong>Core procedures</strong></td><td>Presenting management's figures in statement format</td><td>Analytical procedures and inquiry</td><td>Risk assessment, tests of controls, confirmation, observation, vouching, recalculation</td></tr>
<tr><td><strong>Internal control evaluated</strong></td><td>No</td><td>No</td><td>Yes</td></tr>
<tr><td><strong>Third parties contacted</strong></td><td>No</td><td>No</td><td>Yes — confirmations with banks, customers, vendors, attorneys</td></tr>
<tr><td><strong>Relative cost</strong></td><td>Lowest</td><td>Middle</td><td>Highest</td></tr>
<tr><td><strong>Typically required by</strong></td><td>Internal management use; some vendors and sureties</td><td>Lenders on smaller facilities; some franchisors and operating agreements</td><td>Bank covenants, bonding companies, government funders, grant agreements, buyers in due diligence</td></tr>
</tbody></table>

<h2>Compilation</h2>
<p>A compilation takes the financial information you provide and presents it in proper financial statement format. The accountant applies professional knowledge of accounting and reporting, but performs no procedures to verify the information and expresses no assurance about it.</p>
<p>This is the right level when the reader is you, your management team, or a party who has told you a compilation is sufficient. It is also the most common level for smaller companies that need presentable statements for a specific, limited purpose.</p>

<h2>Review</h2>
<p>A review is substantially narrower in scope than an audit. It consists principally of analytical procedures — comparing balances and relationships against expectations and prior periods, and following up on anything that does not behave as it should — together with inquiry of management.</p>
<p>The result is limited assurance: the accountant is not aware of any material modifications that should be made to the statements. That is a real but much weaker statement than an audit opinion, and it is achieved for meaningfully less cost.</p>
<p>Reviews suit companies whose lender wants outside involvement without requiring the full audit — a common arrangement on smaller credit facilities.</p>

<h2>Audit</h2>
<p>An audit provides reasonable assurance that the statements are fairly stated in all material respects. Getting there requires substantially more work:</p>
<ul>
<li><strong>Risk assessment,</strong> including comparison to similar entities, consideration of economic conditions, and independent ratio analysis</li>
<li><strong>Evaluation of internal control,</strong> and tests of controls whose results determine how much further testing specific accounts require</li>
<li><strong>Substantive testing</strong> — confirmation with outside parties, physical inspection and observation, vouching of invoices to support, and recalculation</li>
<li><strong>An understanding of the accounting system,</strong> and evaluation of current procedures and controls</li>
<li><strong>A management letter</strong> reporting the control weaknesses and operating conditions observed during the work</li>
</ul>
<p>The full approach is described on our <a href="../services/audit-assurance.html">audit and assurance page</a>.</p>

<h2>How to decide</h2>
<h3>Step one: find out what is actually required</h3>
<p>Read the loan agreement, the grant agreement, the bylaws, the operating agreement, or the bonding requirement. The language is usually specific. Companies regularly buy an audit when the covenant says "reviewed financial statements," and that mistake costs real money every year it is repeated.</p>
<h3>Step two: ask whether it can be negotiated</h3>
<p>Requirements are sometimes negotiable, particularly at renewal, particularly for a borrower with a clean history. It is worth one conversation with your lender.</p>
<h3>Step three: if nothing requires it, decide what it is worth</h3>
<p>Occasionally a company chooses a higher level voluntarily — preparing for a sale, satisfying a minority owner, or giving a board genuine comfort. Those are legitimate reasons. "It seems more professional" is not one.</p>

<div class="callout"><p><strong>The audit's byproduct is often the point.</strong> For organizations that require one anyway, the management letter — the written report of control weaknesses, inefficiencies, and conditions affecting profitability — is frequently more useful to management than the opinion itself.</p></div>

<h2>A note for non-profits and governmental organizations</h2>
<p>In this sector the requirement usually arrives with the funding, and grant agreements may impose testing and reporting obligations beyond the financial statement audit itself. Understanding exactly what each funder requires — before agreeing to it — avoids paying for overlapping engagements. See <a href="../industries/government-nonprofit.html">government and non-profit</a>.</p>

<h2>How to compare firms once you know the level</h2>
<p>Ask for the firm's most recent peer review report. Any firm performing audit, review, or attest work should be enrolled in a practice-monitoring program with an independent review every three years. Ask who will be on site and how much experience they have in your reporting environment. Then compare fees. <a href="../peer-review.html">More on peer review</a>.</p>

<h2>Related reading</h2>
<p><a href="cpa-cost-small-business.html">How much does a CPA cost for a small business?</a> &middot; <a href="choosing-a-cpa-firm.html">How to choose a CPA firm in Illinois</a> &middot; <a href="../services/financial-statements.html">Financial statement services</a></p>
''',
   faqs=[("Can a review be upgraded to an audit later in the year?",
          "<p>It is possible but complicated, and it should be raised as early as possible. Some audit evidence — inventory observation, for instance — is time-sensitive and may no longer be obtainable for earlier periods.</p>"),
         ("Does a compilation mean the numbers are wrong?",
          "<p>No. It means no assurance is being provided about them. The figures may be entirely accurate; the accountant simply has not performed procedures to verify them and says so plainly in the report.</p>"),
         ("Why does an audit cost so much more?",
          "<p>Because it requires substantially more work: risk assessment, evaluating and testing internal control, confirming balances with third parties, physical observation, and tracing transactions to supporting documents. The cost difference reflects hours, not markup.</p>"),
         ("Who decides which level we need?",
          "<p>Almost always an outside party — a lender, bonding company, funder, franchisor, or your own governing documents. If nobody requires anything, you may need less than you assumed.</p>")]),

 dict(slug='choosing-a-cpa-firm', nav_title='Choosing a CPA firm in Illinois',
   title='How to Choose a CPA Firm in Illinois | KPW',
   desc='A practical framework for evaluating an Illinois CPA firm — license verification, peer review, who does the work, fee transparency, and the questions worth asking.',
   eyebrow='Guide', h1='How to choose a CPA firm in Illinois',
   sub='Most people choose an accountant on a referral and a fee quote. Here is what to check instead — including two things almost nobody asks for.',
   body='''
<div class="callout"><p><strong>Short answer:</strong> Verify the license, ask for the peer review report, find out who will actually do your work, get the fee arrangement in writing, and confirm the firm handles both your entity and your personal return. Referrals are a starting point, not diligence.</p></div>

<h2>1. Verify that they are actually a CPA</h2>
<p>Anyone may call themselves an accountant or a tax preparer. "Certified Public Accountant" is a protected designation requiring the Uniform CPA Examination, education and experience requirements, and an active state license. In Illinois, licensure is administered by the state and licensee status is verifiable through the Illinois Department of Financial and Professional Regulation.</p>
<p>This matters practically as well as legally: only a licensed CPA firm can issue an audit or review report on financial statements. If you will ever need assurance work, a non-CPA cannot provide it.</p>
<p>Related credentials worth understanding: an <strong>Enrolled Agent</strong> is federally licensed by the IRS and may represent taxpayers in examinations, collections, and appeals — a tax-specific credential with no attest authority. <strong>ABV</strong> (Accredited in Business Valuation) is an AICPA credential for CPAs specializing in valuation. <strong>CFP®</strong> denotes financial planning certification.</p>

<h2>2. Ask for the peer review report</h2>
<p>This is the diligence step almost nobody performs, and it is the most informative one available.</p>
<p>Firms performing accounting and auditing work must undergo an independent peer review every three years, conducted by an independent licensed CPA who is qualified under the program's requirements and has no interest in the firm. The reviewer determines whether the firm has suitable quality control policies and procedures and whether it complies with them — including evidence that the firm's professionals meet continuing education requirements and that the firm satisfies state licensing requirements.</p>
<p>Ask for the report. A firm that produces it readily is telling you something. A firm that cannot, or will not, is telling you something else. <a href="../peer-review.html">More on how peer review works</a>.</p>

<h2>3. Find out who will actually do the work</h2>
<p>At larger firms the partner who sells the engagement frequently is not the person who performs it, and the staff assigned may rotate annually. That is not necessarily bad — it is how firms scale — but you should know it going in, because it determines who you are actually hiring.</p>
<p>Ask directly: Who prepares this? Who reviews it? Who do I reach mid-year when something unexpected happens? Will the same people be here next year?</p>

<h2>4. Match the firm to the work</h2>
<p>Size is a genuine trade-off rather than a quality signal in either direction.</p>
<table class="plain"><thead><tr><th></th><th>Larger firm</th><th>Smaller firm</th></tr></thead><tbody>
<tr><td><strong>Strength</strong></td><td>Deep specialist bench; capacity for large or unusual engagements</td><td>Partner-level attention; continuity; direct access</td></tr>
<tr><td><strong>Trade-off</strong></td><td>You may not be a significant client; staff turnover on your file</td><td>Highly specialized niches may be outside their scope</td></tr>
<tr><td><strong>Fits</strong></td><td>Complex multi-national structures, public filings, specialized industry compliance</td><td>Privately held companies, owner-operators, most non-profits and local governmental units</td></tr>
</tbody></table>
<p>The most common mismatch is a small business at a firm large enough that the business will never be a priority — receiving competent work and no attention.</p>

<h2>5. Confirm they handle both sides</h2>
<p>For any business owner this is non-negotiable. Reasonable compensation, distributions, basis, loans between owner and company, and personally guaranteed debt all cross the line between the entity return and the personal one. A firm handling only one side is optimizing half the picture and cannot see the other half.</p>

<h2>6. Get the fee arrangement in writing</h2>
<p>An engagement letter should state what is included, what is excluded, how fees are structured, and what would cause them to change. This is standard professional practice, and its absence is a warning sign on its own. See <a href="cpa-cost-small-business.html">what a CPA costs a small business</a>.</p>

<h2>7. Test whether they will tell you no</h2>
<p>The most valuable characteristic in an accountant is willingness to give you an answer you do not want. In a first conversation, describe something you are considering that is aggressive or ill-advised and see what happens. A firm that agrees with everything is not going to protect you when it matters — and the position they take with you is the position they will take with an examiner.</p>

<h2>Warning signs</h2>
<ul>
<li>A refund promised before anyone has seen your records</li>
<li>Fees based on a percentage of your refund</li>
<li>Reluctance to provide the peer review report, or to say who will do the work</li>
<li>No engagement letter</li>
<li>Unwillingness to sign the return as preparer</li>
<li>Reachable only from January through April</li>
<li>Agreement with every idea you float</li>
</ul>

<h2>Questions worth asking in the first meeting</h2>
<ol>
<li>Are you licensed in Illinois, and may I have your license number?</li>
<li>May I see your most recent peer review report?</li>
<li>Who specifically will prepare and review my work?</li>
<li>How many clients like me do you serve?</li>
<li>Do you handle both entity and individual returns for owners?</li>
<li>What does your fee include, and what would change it?</li>
<li>How do you handle questions during the year — and are you reachable outside filing season?</li>
<li>What do you think I am currently doing wrong? <em>(The most revealing question on the list.)</em></li>
</ol>

<div class="callout"><p><strong>For what it is worth:</strong> KPW has practiced in Illinois since 1974, our accounting and auditing practice is enrolled in the AICPA peer review program, a partner is responsible for your engagement, and we believe in fair and transparent prices with no hidden fees or extra charges. Ask us all eight questions.</p></div>

<h2>Related reading</h2>
<p><a href="cpa-cost-small-business.html">How much does a CPA cost for a small business?</a> &middot; <a href="audit-review-compilation.html">Audit vs. review vs. compilation</a> &middot; <a href="../about.html">About our firm</a></p>
''',
   faqs=[("How do I verify an Illinois CPA license?",
          "<p>Licensure in Illinois is administered by the state, and licensee status can be verified through the Illinois Department of Financial and Professional Regulation. Ask the firm for the license name and number and confirm it independently.</p>"),
         ("Should I choose a big firm or a small one?",
          "<p>Match the firm to the work. Large firms offer specialist depth and capacity; small firms offer partner attention and continuity. The common mistake is being a small client at a firm where you will never be a priority.</p>"),
         ("What is the single best question to ask a prospective accountant?",
          "<p>\"What do you think I am currently doing wrong?\" It reveals whether they have actually looked at your situation and whether they are willing to say something uncomfortable — which is the trait you are really hiring for.</p>"),
         ("Is it hard to switch accountants?",
          "<p>Less than most people assume. Your prior returns and records belong to you. The real cost is the learning curve in year one, which is why switching for a small fee difference rarely pays.</p>")]),
]

def _guide(g):
    url = BASE + 'guides/' + g['slug'] + '.html'
    others = ''.join('<li><a href="'+o['slug']+'.html"><span class="ck">&rarr;</span> '+o['nav_title']+'</a></li>'
                     for o in GUIDES if o['slug'] != g['slug'])
    p = dict(path='guides/'+g['slug']+'.html', depth=1, nav='about',
             title=g['title'], desc=g['desc'], eyebrow=g['eyebrow'], h1=g['h1'], sub=g['sub'])
    p['body'] = phero(p, [('Guides','guides/'+g['slug']+'.html'), (g['nav_title'], None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">'+g['body']+
      '<h2>Common questions</h2>'+faq_html(g['faqs'])+
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Ask us directly</div>'
      '<p>Ten minutes on the phone answers more than any guide.</p>'
      '<a class="btn b-acc" href="tel:'+FIRM['tel']+'">'+FIRM['ph']+'</a>'
      '</div>'
      '<div class="acard light"><div class="t">Other guides</div><ul>'+others+
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> All common questions</a></li></ul></div></div>'
      '</div></div></section>')
    p['schema'] = [org_schema(),
      breadcrumb_schema([('Home',BASE),('Guides',BASE+'guides/'+g['slug']+'.html'),(g['nav_title'],url)]),
      article_schema(_plain(g['h1']), g['desc'], url),
      faq_schema([(q, _plain(a)) for q, a in g['faqs']])]
    return p

def pages():
    return [_guide(g) for g in GUIDES]
