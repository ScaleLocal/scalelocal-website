# -*- coding: utf-8 -*-
"""
Mass Tax Pros — all 22 pages.

Sourcing discipline for this build (see research/masstaxpros.md):
  * The firm publishes no founding date, no office hours, no memberships, no
    portal and no online payments. None of those appear anywhere below.
  * The only experience figure used is the firm's own "more than 50 years of
    combined experience". Their live site's "approximately 15 years" and
    "quarter century" lines are 13 years stale and are not repeated.
  * Thomas P. Craig is a CPA and an Enrolled Agent. Joseph W. Brine is an
    Enrolled Agent and is not a CPA; he is never described as one.
  * Their existing testimonials are real but the quote text was not captured in
    the audit, so no testimonial is reproduced. Inventing one is not an option.
  * The firm does not advertise audit or review engagements, so no attest
    capability is claimed.
Everything else is general professional or statutory background (IRS Circular
230 practice rights, Massachusetts licensing, filing mechanics) that stands on
its own and is not a claim about this firm.
"""
import html, re, os, json, zlib, struct

import calculators as C
from build import (FIRM, BASE, T, OUT, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   breadcrumb_schema, faq_schema)

LEGAL = 'Thomas P. Craig, CPA, PC'
ORG_ID = BASE + '#firm'
CTA = ('Talk to Tom or Joe.',
       'Call the office or write to info@tpc-cpa.com. Describe what you are working on — a return, '
       'a set of books that has drifted, a letter you did not expect — and one of us will come back '
       'to you. What you tell us stays between us.')


def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()


# ---------------------------------------------------------------------------
# Schema builders. build.org_schema() hard-codes an Illinois membership set, a
# founding date and Chicagoland service area, none of which apply here, so this
# build defines its own. No rating markup, no openingHours (not published), no
# foundingDate (not published), no memberOf (none claimed).
# ---------------------------------------------------------------------------
def org_schema():
    return {"@context": "https://schema.org", "@type": "AccountingService", "@id": ORG_ID,
            "name": LEGAL, "legalName": LEGAL, "alternateName": "Mass Tax Pros",
            "url": BASE, "email": FIRM['email'], "telephone": FIRM['ph'],
            "faxNumber": FIRM['fax'], "priceRange": "$$",
            "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                        "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                        "postalCode": FIRM['zip'], "addressCountry": "US"},
            "areaServed": [{"@type": "AdministrativeArea", "name": "Massachusetts"}],
            "hasMap": FIRM['maps']}


def service_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "description": desc, "url": url, "serviceType": name,
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "AdministrativeArea", "name": "Massachusetts"}}


def person_schema(name, suffix, url, desc, alumni=None):
    d = {"@context": "https://schema.org", "@type": "Person", "name": name,
         "honorificSuffix": suffix, "url": url, "description": desc,
         "worksFor": {"@id": ORG_ID}}
    if alumni:
        d["alumniOf"] = [{"@type": "EducationalOrganization", "name": n} for n in alumni]
    return d


def article_schema(title, desc, url):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title,
            "description": desc, "url": url,
            "author": {"@type": "Organization", "name": LEGAL},
            "publisher": {"@id": ORG_ID}}


# ---------------------------------------------------------------------------
# apple-touch-icon.png. The engine's <head> links one on every page and the
# shared asset renderer is hard-wired to another firm, so this build writes its
# own 180x180 PNG with a dependency-free encoder: brand green, the two logo
# brackets, and the single-letter favicon glyph.
# ---------------------------------------------------------------------------
def _touch_icon():
    W = 180
    ink = (0x12, 0x3A, 0x2E)
    buf = bytearray(ink[i % 3] for i in range(W * W * 3))

    def px(x, y, c):
        if 0 <= x < W and 0 <= y < W:
            o = (y * W + x) * 3
            buf[o], buf[o + 1], buf[o + 2] = c

    def rect(x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1)):
            for x in range(int(x0), int(x1)):
                px(x, y, c)

    def seg(ax, ay, bx, by, t, c):
        dx, dy = bx - ax, by - ay
        dd = dx * dx + dy * dy
        r = t / 2.0
        for y in range(int(min(ay, by) - r - 1), int(max(ay, by) + r + 2)):
            for x in range(int(min(ax, bx) - r - 1), int(max(ax, bx) + r + 2)):
                u = 0.0 if dd == 0 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / dd))
                px_, py_ = ax + u * dx, ay + u * dy
                if (x - px_) ** 2 + (y - py_) ** 2 <= r * r:
                    px(x, y, c)

    w = (255, 255, 255)
    s = W / 64.0
    rect(5 * s, 5 * s, 24 * s, 8.6 * s, w)        # top-left bracket, horizontal arm
    rect(5 * s, 5 * s, 8.6 * s, 24 * s, w)        # top-left bracket, vertical arm
    rect(40 * s, 55.4 * s, 59 * s, 59 * s, w)     # bottom-right bracket, horizontal
    rect(55.4 * s, 40 * s, 59 * s, 59 * s, w)     # bottom-right bracket, vertical
    seg(62, 62, 62, 120, 10, w)                   # M, left stem
    seg(118, 62, 118, 120, 10, w)                 # M, right stem
    seg(62, 62, 90, 103, 10, w)                   # M, left diagonal
    seg(118, 62, 90, 103, 10, w)                  # M, right diagonal

    raw = b''.join(b'\x00' + bytes(buf[y * W * 3:(y + 1) * W * 3]) for y in range(W))

    def chunk(tag, data):
        body = tag + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', W, W, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'apple-touch-icon.png'), 'wb') as f:
        f.write(png)


# ---------------------------------------------------------------------------
# Services — the four the firm's own site publishes, no more.
# ---------------------------------------------------------------------------
SERVICES = [
 dict(slug='income-tax', ic='calc', nav_title='Income Tax Services',
   short='Federal and Massachusetts returns for businesses, owners and individuals &mdash; prepared, planned for, and defended if a notice arrives.',
   title='Income Tax Services | Mass Tax Pros, Wilmington MA',
   desc='Federal and Massachusetts income tax preparation and planning for businesses and individuals in Wilmington, with IRS and DOR representation by Enrolled Agents.',
   eyebrow='Tax', h1='Returns are the easy part. The year before them is the work.',
   sub='Preparation for businesses, their owners, and individuals &mdash; plus the planning during the year that decides what the return says.',
   body='''
<h2>What we do</h2>
<p>We prepare federal and Massachusetts income tax returns for businesses and for individuals, and we plan for them during the year rather than reporting on them afterwards. For an owner-operated company those two jobs are one job: the entity return and the owner's personal return are the same set of decisions seen from two sides.</p>

<h2>Business returns</h2>
<p>Partnerships, S corporations, C corporations and single-member LLCs each carry their own filing mechanics, their own Massachusetts treatment, and their own traps. The recurring ones we see:</p>
<ul>
<li><strong>Owner compensation.</strong> An S corporation shareholder who works in the business has to take reasonable wages before distributions. Set too low and it is an examination issue; set carelessly high and it costs payroll tax that never had to be paid.</li>
<li><strong>Basis.</strong> Losses are only deductible to the extent of basis, and basis has to be tracked year by year. Reconstructing it later, under pressure, is expensive.</li>
<li><strong>The Massachusetts layer.</strong> Massachusetts does not simply adopt the federal number. Corporate excise, the non-income measure, the pass-through entity excise election and personal-income conformity all have to be worked separately.</li>
<li><strong>Fixed assets.</strong> Whether an equipment purchase is expensed or depreciated changes this year's bill and every year after it. The <a href="../calculators/section-179.html">equipment purchase calculator</a> gives you the order of magnitude before you sign anything.</li>
</ul>

<h2>Individual returns</h2>
<p>Wages, self-employment, rental property, investment income, retirement distributions, equity compensation, a house sale, a year with two states in it. Most individual returns are straightforward; the ones that are not usually became complicated because something happened during the year that nobody thought to mention.</p>
<p>If your year contained an event &mdash; a sale, a move, an inheritance, a business started or closed &mdash; that is the conversation to have before December, not in April.</p>

<h2>Planning during the year</h2>
<p>The decisions that move a tax bill are made while the year is still open: how to structure a purchase, when to recognise income, what to do with a good quarter, whether to make an election, how much to put into a retirement plan, whether the entity you chose three years ago still fits. Once the year closes, a preparer is recording history.</p>
<p>Self-employed clients in particular are usually better served by getting the quarterly estimates roughly right than by any single deduction. The <a href="../calculators/self-employment-tax.html">self-employment tax calculator</a> shows where the number comes from.</p>

<h2>Notices, examinations and representation</h2>
<p>An IRS or Massachusetts Department of Revenue letter is not automatically bad news, and a surprising share of them are simply wrong &mdash; a mismatched information return, a payment applied to the wrong period, a return that crossed a notice in the post.</p>
<div class="callout"><p><strong>Both professionals here are Enrolled Agents.</strong> An Enrolled Agent is licensed by the Treasury and has unlimited rights to represent taxpayers before the IRS in examinations, collections and appeals. Send us the letter before you answer it. <a href="../guides/cpa-vs-enrolled-agent.html">What the credentials actually mean</a>.</p></div>

<h2>What we need from you</h2>
<p>For a business: last year's filed return, the books for the year (or access to them), the fixed asset detail, payroll reports, and anything with a deadline attached. For an individual: last year's return, the forms as they arrive, and a short note on anything that changed. Missing pieces are normal &mdash; bring what you have and we will tell you what is still needed.</p>
''',
   faqs=[("When should I get in touch about next year's return?",
          "<p>Before the year ends. Almost everything that changes a tax bill &mdash; entity choice, owner compensation, the timing of a large purchase or a sale, retirement contributions, an election &mdash; is decided while the year is still open. By April the arithmetic is fixed.</p>"),
         ("Can you prepare both my company return and my personal return?",
          "<p>Yes, and for a closely held business that is the point. Reasonable compensation, distributions, basis and loss limitations only work out sensibly when the same people see both returns.</p>"),
         ("I got a letter from the IRS. What should I do?",
          "<p>Send it to us before you reply. Both professionals here are Enrolled Agents, which carries unlimited representation rights before the IRS. Many notices are resolved with one correctly worded letter, and some are simply incorrect.</p>"),
         ("Do you handle returns in more than one state?",
          "<p>Yes. People who move mid-year, work across a state line, or own rental property elsewhere routinely need more than one return, and the credit mechanics between states are where the mistakes happen.</p>")],
   related=[('accounting', 'Accounting services'), ('quickbooks', 'QuickBooks services'),
            ('../calculators/self-employment-tax.html', 'Self-employment tax calculator'),
            ('../guides/cpa-vs-enrolled-agent.html', 'CPA, EA or preparer?')]),

 dict(slug='accounting', ic='ledger', nav_title='Accounting Services',
   short='Books that close on time, reconcile to the bank, and produce a statement you can actually make a decision from.',
   title='Accounting Services | Mass Tax Pros, Wilmington MA',
   desc='Bookkeeping, monthly close, reconciliations and financial statement preparation for Massachusetts businesses, from the Wilmington office of Thomas P. Craig, CPA, PC.',
   eyebrow='Accounting', h1='A return is only as good as the books behind it.',
   sub='Bookkeeping, the monthly close, reconciliations, and financial statements prepared so the numbers mean something before the filing deadline arrives.',
   body='''
<h2>What we do</h2>
<p>We keep books, close months, reconcile accounts, and prepare financial statements for businesses that would rather not run an accounting department. For some clients that is the whole engagement; for most it runs alongside the tax work, which is the arrangement that costs least in the end.</p>

<h2>Why the bookkeeping decides the tax bill</h2>
<p>Almost every unpleasant surprise at filing time started months earlier in the ledger: an owner draw recorded as an expense, a loan repayment posted to income, a credit card that was never reconciled, a fixed asset sitting in supplies. None of it is exotic. All of it changes the return, and all of it costs more to unpick in March than it did to record correctly in July.</p>
<p>The other cost is decisions. If the statements are three months behind, they are history, and pricing, hiring and borrowing all get decided on instinct instead.</p>

<h2>What the work covers</h2>
<ul>
<li><strong>Transaction recording and coding</strong> &mdash; consistently, to a chart of accounts that answers the questions you actually ask.</li>
<li><strong>Bank, credit card and loan reconciliations</strong> &mdash; the step most often skipped, and the one that catches everything else.</li>
<li><strong>Monthly or quarterly close</strong> &mdash; accruals, prepayments, depreciation, payroll journals, and a set of statements that tie out.</li>
<li><strong>Financial statement preparation</strong> &mdash; balance sheet, profit and loss, and cash flow in a form you can hand to a lender or a landlord.</li>
<li><strong>Year-end packaging</strong> &mdash; the trial balance, schedules and fixed asset detail that the return is built from.</li>
<li><strong>Cleanup work</strong> &mdash; a year or two of records that drifted, brought back to something reliable.</li>
</ul>

<h2>Chart of accounts, and why yours is probably wrong</h2>
<p>Most charts of accounts are inherited from whatever the software suggested on day one. That is fine until you want to know which side of the business earns its keep, what a job actually costs, or why gross margin moved. A chart built around your operations &mdash; by service line, by location, by crew &mdash; turns the same bookkeeping effort into management information at no extra cost.</p>

<h2>Payroll, and where it sits</h2>
<p>Payroll is where small businesses get hurt fastest, because the penalties are mechanical and the deadlines do not move. Whether you run it in-house or through a service, the postings have to land correctly in the books and the quarterly filings have to agree with the general ledger. Joseph Brine's experience spans the healthcare, construction and payroll industries, and payroll-heavy businesses tend to be where he is most useful.</p>

<div class="callout"><p><strong>Reading your own statements.</strong> If you want the numbers explained rather than delivered, ask. Most owners do not need an accounting course; they need someone to point at three lines and say what they mean.</p></div>

<h2>How engagements usually run</h2>
<p>Either we do the bookkeeping, or you do it and we review and close. The second costs less and works well when someone in the business is careful and has been shown what to watch. The first is better when nobody has the time, which is more common than owners like to admit.</p>
''',
   faqs=[("Do you take on books that are behind?",
          "<p>Yes. Cleanup work is normal &mdash; a year or two of unreconciled accounts, or a file that was never set up properly. The first step is finding out how far back the records can be trusted.</p>"),
         ("Can we keep doing our own bookkeeping?",
          "<p>Often, yes, and it is usually cheaper. We set up the file, agree the coding rules, and then review and close periodically so errors are caught in weeks rather than at year end.</p>"),
         ("Do you prepare audited or reviewed financial statements?",
          "<p>The statements we prepare are management and tax-basis financial statements. If a lender or a contract specifically requires an independent audit or review, tell us what the requirement says and we will help you work out what is genuinely being asked for.</p>"),
         ("How often should we close the books?",
          "<p>Monthly if the business carries inventory, employees or a line of credit. Quarterly is enough for a simple service business. Annually means the statements are history and nothing can be corrected in time.</p>")],
   related=[('quickbooks', 'QuickBooks services'), ('income-tax', 'Income tax services'),
            ('../calculators/break-even.html', 'Break-even calculator'),
            ('../team/joseph-w-brine.html', 'Joseph W. Brine, EA')]),

 dict(slug='quickbooks', ic='doc', nav_title='QuickBooks Services',
   short='Setup, cleanup and ongoing support for the file your business actually runs on &mdash; built so the reports mean something.',
   title='QuickBooks Services | Mass Tax Pros, Wilmington MA',
   desc='QuickBooks setup, cleanup, reconciliation and ongoing support for Massachusetts businesses, from an accounting practice that also prepares the tax return.',
   eyebrow='QuickBooks', h1='The software is not the problem. The setup usually is.',
   sub='Getting the file right at the start, fixing it when it has drifted, and keeping it in a state where the reports can be trusted.',
   body='''
<h2>What we do</h2>
<p>We set up QuickBooks files, repair files that have gone wrong, and support the people who use them day to day. Because the same practice prepares the tax return, the file is built to produce what the return needs rather than what a generic template produces.</p>

<h2>Setup</h2>
<p>A new file takes an afternoon to create and years to regret. The choices that matter are made in the first hour:</p>
<ul>
<li><strong>Chart of accounts.</strong> Detailed enough to answer your questions, not so detailed that nobody codes consistently.</li>
<li><strong>Items and services.</strong> The single biggest source of unreliable profit-and-loss reporting in small business files.</li>
<li><strong>Opening balances.</strong> Entered from a real trial balance, not typed in from a bank statement.</li>
<li><strong>Bank feeds and rules.</strong> Useful when supervised, quietly destructive when they auto-post two years of transactions to the wrong account.</li>
<li><strong>Sales tax, payroll and users.</strong> Configured once, correctly, with permissions that suit who actually touches the file.</li>
</ul>

<h2>Cleanup</h2>
<p>Files usually arrive with the same handful of problems: an undeposited funds account that has been growing for years, bank accounts that have never been reconciled, negative inventory, duplicated vendors, an opening balance equity line nobody can explain, and personal spending mixed in with business. Cleanup is a defined piece of work &mdash; we find out where the records stop being trustworthy, fix forward from there, and tell you what it will take.</p>

<h2>Ongoing support</h2>
<p>Most businesses want to run their own file and call someone when it stops making sense. That works. Common questions: how to record a loan payment so the principal and interest split correctly, what to do with an owner contribution, how to handle a customer deposit, why the balance sheet is out by exactly the amount of one cheque, how to record a fixed asset purchase that was financed.</p>

<div class="callout"><p><strong>Desktop, Online, or something else.</strong> We work with the file you have. If you are choosing, the honest answer depends on how you invoice, whether you carry inventory, and who needs access from where &mdash; not on which version is newer.</p></div>

<h2>Reporting that earns its keep</h2>
<p>Once a file is clean, the reports are worth building properly: profit and loss by class or location, job costing for contractors, aged receivables that get looked at weekly, and a cash view that is not just the bank balance. This is where a tidy file stops being an accounting chore and starts being useful.</p>
''',
   faqs=[("Our file is a mess. Is it worth fixing or should we start again?",
          "<p>Usually fixing. A new file loses the history, and history is what makes comparisons possible. Starting again is the right call when the damage runs to the opening balances themselves.</p>"),
         ("Can you work in our file remotely?",
          "<p>Yes, for QuickBooks Online. For desktop files there are several ways to share a copy or work on a hosted file &mdash; tell us how yours is set up.</p>"),
         ("Will you train our bookkeeper?",
          "<p>Yes. Most support turns out to be a handful of recurring transaction types someone was never shown. Once those are right, the file stays right.</p>"),
         ("Do bank feeds mean we do not need a bookkeeper?",
          "<p>No. Feeds import transactions; they do not decide what an item is. Unsupervised rules are the most common cause of a file that reconciles perfectly and reports nonsense.</p>")],
   related=[('accounting', 'Accounting services'), ('income-tax', 'Income tax services'),
            ('../calculators/loan-payment.html', 'Loan payment calculator'),
            ('../services/index.html', 'All services')]),

 dict(slug='financial-services', ic='chart', nav_title='Financial Services',
   short='The financial side of a decision discussed in the same room as the tax side, rather than in two offices that never speak.',
   title='Financial Services | Mass Tax Pros, Wilmington MA',
   desc='Financial services alongside tax and accounting in Wilmington, Massachusetts. Thomas P. Craig is licensed to sell securities and insurance products.',
   eyebrow='Financial', h1='Most financial advice is given without sight of the tax return.',
   sub='Thomas P. Craig is licensed to sell securities and insurance products &mdash; so the tax consequence and the product decision can be discussed together.',
   body='''
<h2>What this is</h2>
<p>Financial services sit alongside the tax and accounting work at this practice. Thomas P. Craig is a CPA and an Enrolled Agent, and is also licensed to sell securities and insurance products. That combination is the whole argument for keeping the two conversations in one place.</p>

<h2>Why separation costs money</h2>
<p>The usual arrangement is that an adviser recommends and an accountant reports. The adviser does not see the return; the accountant sees the consequence a year later and cannot change it. That gap is where avoidable tax lives:</p>
<ul>
<li>A retirement plan chosen without reference to what the business actually earns, or to who else is on the payroll.</li>
<li>Investments held in the wrong type of account, so income that could have been deferred is taxed every year.</li>
<li>A sale or a rebalance executed in December that could have been executed in January for a materially different result.</li>
<li>Insurance bought to solve a problem the business does not have, or absent for one it does.</li>
<li>Beneficiary designations that quietly override the will nobody has looked at since it was signed.</li>
</ul>

<h2>Where it meets the business</h2>
<p>For owner-operated companies the personal and business questions are inseparable. How much to take as wages against distributions, what retirement plan the company can carry, how to fund a buy-sell arrangement between partners, what happens to the business if one owner is not there next year &mdash; all of these are simultaneously tax questions, cash questions and family questions.</p>

<div class="callout"><p><strong>Order of operations.</strong> Get the numbers straight first. A projection built on books that have not been reconciled is arithmetic, not planning. That is why the <a href="accounting.html">accounting</a> and <a href="income-tax.html">tax</a> work usually comes first.</p></div>

<h2>Running your own numbers</h2>
<p>Several of the questions people bring here can be sized up in two minutes. The <a href="../calculators/retirement-savings.html">retirement projection</a>, the <a href="../calculators/college-savings.html">college saving</a> calculator, the <a href="../calculators/mortgage-payment.html">mortgage payment</a> and the <a href="../calculators/refinance-breakeven.html">refinance break-even</a> all run on this site, in your browser, with nothing sent anywhere. They will not answer a planning question on their own, but they will tell you whether the question is worth a meeting.</p>

<h2>What we will say plainly</h2>
<p>If a decision is fine as it stands, we will say so. If the honest answer is that the number is too small for the structure being proposed, we will say that too. Complexity has an ongoing cost &mdash; in fees, in filings and in the risk of getting it wrong &mdash; and it has to earn its place.</p>
''',
   faqs=[("Is this investment advice?",
          "<p>This page describes the services offered by the practice. Thomas P. Craig is licensed to sell securities and insurance products. Any specific recommendation depends entirely on your circumstances and is made in a conversation, not on a website.</p>"),
         ("Do I have to use you for tax as well?",
          "<p>No. But the argument for this practice is that the two sit together, and if the tax work is somewhere else that advantage is largely lost.</p>"),
         ("Can you look at a plan someone else has proposed?",
          "<p>Yes. A second reading focused on the tax consequences of a proposal is often the most useful hour in the process.</p>"),
         ("What about retirement plans for a small company?",
          "<p>Plan choice depends on how many employees there are, how the owners are paid, and how much flexibility you want year to year. It is a tax question and a payroll question before it is an investment question.</p>")],
   related=[('income-tax', 'Income tax services'), ('accounting', 'Accounting services'),
            ('../team/thomas-p-craig.html', 'Thomas P. Craig, CPA, EA'),
            ('../calculators/index.html', 'Calculators')]),
]


# ---------------------------------------------------------------------------
# The two named professionals.
# ---------------------------------------------------------------------------
TEAM = [
 dict(slug='thomas-p-craig', initials='TC', name='Thomas P. Craig', short='Tom Craig',
   cred='CPA &middot; Enrolled Agent', suffix='CPA, EA',
   alumni=['University of Massachusetts'],
   card='Certified Public Accountant and Enrolled Agent, and licensed to sell securities and insurance products. Accounting and economics at the University of Massachusetts.',
   title='Thomas P. Craig, CPA, EA | Mass Tax Pros, Wilmington MA',
   desc='Thomas P. Craig is a Certified Public Accountant and an Enrolled Agent, and is licensed to sell securities and insurance products. The practice trades as Mass Tax Pros.',
   eyebrow='Mass Tax Pros', h1='Thomas P. Craig, CPA, EA',
   sub='Certified Public Accountant and Enrolled Agent &mdash; and the name on the practice, Thomas P. Craig, CPA, PC.',
   body='''
<h2>Credentials</h2>
<p>Tom Craig is a Certified Public Accountant and an Enrolled Agent. He is also licensed to sell securities and insurance products. He studied at the University of Massachusetts, where he majored in accounting with a minor in economics.</p>
<p>Holding both the CPA licence and the Enrolled Agent designation is unusual and practically useful. The CPA licence is granted by a state board and covers the full breadth of accounting practice. The Enrolled Agent designation is granted by the Treasury and carries unlimited rights to represent taxpayers before the IRS in examinations, collections and appeals. A client who receives a notice does not have to be handed to anyone else. <a href="../guides/cpa-vs-enrolled-agent.html">What the credentials mean</a>.</p>

<h2>How the practice came together</h2>
<p>In 2006 Joe and Tom formed Craig, Brine &amp; Associates, and the company was later incorporated as Thomas P. Craig, CPA, PC &mdash; the practice that trades today as the Mass Tax Pros. In 2013 the firm announced the acquisition of Emond Tax &amp; Financial Group.</p>

<h2>Where the securities and insurance licences matter</h2>
<p>Most people receive financial recommendations from someone who has never seen their tax return, and tax preparation from someone who was not consulted before the decision was made. Because Tom holds the licences as well as the accounting credentials, both halves of a question can be discussed at once &mdash; which account a holding belongs in, what a distribution will cost, whether a plan design fits the payroll it has to sit on. See <a href="../services/financial-services.html">financial services</a>.</p>

<h2>Working with him</h2>
<p>Business owners, self-employed clients and individuals with something unusual in the year &mdash; a sale, a move, an inheritance, a new venture &mdash; are the situations where the combination of credentials earns its keep. The most useful first conversation is a short one about what changed.</p>
''',
   focus=['Certified Public Accountant', 'Enrolled Agent, admitted to practice before the IRS',
          'Licensed to sell securities and insurance products',
          'University of Massachusetts &mdash; accounting major, economics minor']),

 dict(slug='joseph-w-brine', initials='JB', name='Joseph W. Brine', short='Joe Brine',
   cred='Enrolled Agent', suffix='EA',
   alumni=['Merrimack College'],
   card='Enrolled Agent, federally licensed to represent taxpayers before the IRS. Experience across the healthcare, construction and payroll industries. Merrimack College.',
   title='Joseph W. Brine, EA | Mass Tax Pros, Wilmington MA',
   desc='Joseph W. Brine is an Enrolled Agent with experience in the healthcare, construction and payroll industries. He holds a bachelor’s degree from Merrimack College.',
   eyebrow='Mass Tax Pros', h1='Joseph W. Brine, EA',
   sub='Enrolled Agent &mdash; federally licensed to represent taxpayers before the Internal Revenue Service.',
   body='''
<h2>Credentials</h2>
<p>Joe Brine is an Enrolled Agent. He holds a bachelor's degree from Merrimack College, where he majored in accounting.</p>
<p>An Enrolled Agent is licensed by the United States Treasury rather than by a state, and the designation is earned either by passing the three-part Special Enrollment Examination or through qualifying experience at the IRS. It carries unlimited practice rights under Circular 230: an Enrolled Agent may represent any taxpayer, on any tax matter, before any IRS office &mdash; examinations, collections and appeals included. Enrolled Agents are also subject to continuing education requirements and to the ethical rules of Circular 230. <a href="../guides/cpa-vs-enrolled-agent.html">How the credentials compare</a>.</p>

<h2>Industry experience</h2>
<p>Joe's experience spans the healthcare, construction and payroll industries.</p>
<p>Those three overlap more than they look. Construction lives on job costing, retainage, progress billing and a payroll that moves week to week. Healthcare practices carry payroll, insurance receivables that age unpredictably, and equipment decisions with real tax consequences. Payroll itself is where the deadlines are mechanical and the penalties arrive without argument. A business with employees and jobs to cost needs an accountant who has seen those particular problems before.</p>

<h2>How the practice came together</h2>
<p>In 2006 Joe and Tom formed Craig, Brine &amp; Associates, and the company was later incorporated as Thomas P. Craig, CPA, PC, trading today as the Mass Tax Pros.</p>

<h2>Working with him</h2>
<p>Businesses with payroll, contractors and trades, healthcare practices, and anyone facing an IRS matter that needs representation rather than another letter. See <a href="../services/accounting.html">accounting services</a> and <a href="../services/income-tax.html">income tax services</a>.</p>
''',
   focus=['Enrolled Agent, admitted to practice before the IRS',
          'Experience in the healthcare, construction and payroll industries',
          'Merrimack College &mdash; accounting major']),
]


HOME_FAQS = [
 ("What is the difference between a CPA and an Enrolled Agent?",
  "<p>A Certified Public Accountant is licensed by a state board of accountancy after passing the Uniform CPA Examination and meeting that state's education and experience requirements. An Enrolled Agent is licensed federally by the Treasury, either by passing the three-part Special Enrollment Examination or through qualifying IRS experience, and holds unlimited rights to represent taxpayers before the IRS.</p><p>This practice has both. Thomas P. Craig is a CPA and an Enrolled Agent; Joseph W. Brine is an Enrolled Agent. Our <a href=\"guides/cpa-vs-enrolled-agent.html\">guide to the credentials</a> sets out what each one can and cannot do.</p>"),
 ("Do you work with businesses, individuals, or both?",
  "<p>Both, and they are frequently the same client. For an owner-operated business the company return and the owner's personal return are one problem, and splitting them between two firms is how planning opportunities get missed.</p>"),
 ("Can you take over books that are behind?",
  "<p>Yes. Catch-up and cleanup work is routine &mdash; unreconciled accounts, a QuickBooks file that drifted, a year that was never closed. The first step is establishing how far back the records can be relied on. See <a href=\"services/accounting.html\">accounting services</a>.</p>"),
 ("I received a notice from the IRS or the Massachusetts DOR. Can you help?",
  "<p>Yes, and send it before you respond. Both professionals here are Enrolled Agents, which carries unlimited representation rights before the IRS. A good number of notices are resolved with one accurate letter, and some of them are wrong to begin with.</p>"),
 ("Are you taking on new clients?",
  "<p>The most useful first step is a short call. Tell us what kind of entity you are, roughly what the year looked like, and what deadline you are working against. If the work belongs somewhere else, we will say so.</p>"),
]


# ---------------------------------------------------------------------------
def _card(d, href, ic, title, text, num=None):
    return ('<a class="card reveal" href=' + '"' + rel(d, href) + '">'
            + ('<span class="num">' + num + '</span>' if num else '')
            + '<div class="cic">' + icon(ic) + '</div><h3>' + title + '</h3><p>' + text + '</p>'
            '<span class="more">Read more ' + ARROW + '</span></a>')


def _svc_page(s):
    url = BASE + 'services/' + s['slug'] + '.html'
    rel_links = ''
    for href, label in s['related']:
        h = href if href.startswith('..') or href.endswith('.html') else href + '.html'
        rel_links += '<li><a href="' + h + '"><span class="ck">&rarr;</span> ' + label + '</a></li>'
    p = dict(path='services/' + s['slug'] + '.html', depth=1, nav='services',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'],
             cta_args=CTA)
    p['body'] = phero(p, [('Services', 'services/index.html'), (_plain(s['nav_title']), None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">' + s['body']
      + '<h2>Common questions</h2>' + faq_html(s['faqs'])
      + '</div>'
      '<div class="aside"><div class="acard"><div class="t">Talk it through</div>'
      '<p>Describe the situation in a few minutes and we will tell you what the work involves.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>' + rel_links + '</ul></div>'
      '<div class="acard light"><div class="t">The practice</div><ul>'
      '<li><a href="../team/thomas-p-craig.html"><span class="ck">&#10003;</span> Thomas P. Craig, CPA and Enrolled Agent</a></li>'
      '<li><a href="../team/joseph-w-brine.html"><span class="ck">&#10003;</span> Joseph W. Brine, Enrolled Agent</a></li>'
      '<li><span class="ck">&#10003;</span> More than 50 years of combined experience</li>'
      '<li><a href="../contact.html"><span class="ck">&#10003;</span> Wilmington, Massachusetts</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/'),
                                      (_plain(s['nav_title']), url)]),
                   service_schema(_plain(s['nav_title']), _plain(s['short']), url),
                   faq_schema([(q, _plain(a)) for q, a in s['faqs']])]
    return p


def _bio(t):
    url = BASE + 'team/' + t['slug'] + '.html'
    focus = ''.join('<li>' + x + '</li>' for x in t['focus'])
    other = [o for o in TEAM if o['slug'] != t['slug']][0]
    p = dict(path='team/' + t['slug'] + '.html', depth=1, nav='team',
             title=t['title'], desc=t['desc'], eyebrow=t['eyebrow'], h1=t['h1'], sub=t['sub'],
             cta_args=CTA)
    p['body'] = phero(p, [('Our team', 'team/index.html'), (t['name'], None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">' + t['body']
      + '<h2>At a glance</h2><ul>' + focus + '</ul>'
      '<div class="callout"><p><strong>Contact.</strong> '
      '<a href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a> &middot; '
      '<a href="mailto:' + FIRM['email'] + '">' + FIRM['email'] + '</a></p></div>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">' + t['name'] + '</div>'
      '<p>' + t['cred'] + '<br>' + LEGAL + '<br>Wilmington, Massachusetts</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Also here</div><ul>'
      '<li><a href="' + other['slug'] + '.html"><span class="ck">&rarr;</span> ' + other['name'] + ', ' + other['suffix'] + '</a></li>'
      '<li><a href="../guides/cpa-vs-enrolled-agent.html"><span class="ck">&rarr;</span> CPA, EA or preparer?</a></li>'
      '<li><a href="../services/index.html"><span class="ck">&rarr;</span> What the practice does</a></li>'
      '<li><a href="../about.html"><span class="ck">&rarr;</span> About the practice</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(),
                   breadcrumb_schema([('Home', BASE), ('Our team', BASE + 'team/'), (t['name'], url)]),
                   person_schema(t['name'], t['suffix'], url, _plain(t['card']), t['alumni'])]
    return p


# ---------------------------------------------------------------------------
def pages():
    _touch_icon()
    P = []

    # ------------------------------------------------------------------ HOME
    svc_cards = ''.join([
      _card(0, 'services/income-tax.html', 'calc', 'Income Tax Services',
            'Federal and Massachusetts returns for businesses, owners and individuals &mdash; and the planning during the year that decides what they say.', '01'),
      _card(0, 'services/accounting.html', 'ledger', 'Accounting Services',
            'Bookkeeping, the monthly close, reconciliations and financial statements you can make a decision from.', '02'),
      _card(0, 'services/quickbooks.html', 'doc', 'QuickBooks Services',
            'Setup, cleanup and support for the file the business actually runs on, built so the reports can be trusted.', '03'),
      _card(0, 'services/financial-services.html', 'chart', 'Financial Services',
            'The financial side of a decision and the tax side of it discussed in the same room, by the same people.', '04'),
    ])
    team_preview = ''.join([
      '<a class="tcard reveal" href="team/' + t['slug'] + '.html"><div class="tava">' + t['initials'] + '</div>'
      '<h3>' + t['name'] + '</h3><div class="cred">' + t['cred'] + '</div><p>' + t['card'] + '</p></a>'
      for t in TEAM])
    body = (
      '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" aria-hidden="true">' + GLYPH + '</svg>'
      '<div class="wrap"><div class="reveal in">'
      '<span class="eyebrow on-dark">Tax &amp; Accounting Service Professionals &middot; Wilmington, Massachusetts</span>'
      '<h1>A CPA and an Enrolled Agent, with more than fifty years between them.</h1>'
      '<p class="sub">Thomas P. Craig, CPA, PC trades as the Mass Tax Pros from Heritage Commons on Middlesex Avenue. '
      'Income tax, accounting, QuickBooks and financial services &mdash; for businesses and for the people who own them.</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a>'
      '<a class="btn b-gh" href="services/index.html">What we do ' + ARROW + '</a></div>'
      '<div class="hero-trust"><span><b>Tom Craig</b>, CPA and Enrolled Agent</span>'
      '<span><b>Joe Brine</b>, Enrolled Agent</span>'
      '<span><b>50+ years</b> combined experience</span>'
      '<span><b>Wilmington</b>, Massachusetts</span></div>'
      '</div></div></section>'

      '<section class="strip"><div class="wrap reveal">'
      '<div class="cell"><div class="n">50+</div><div class="l">years of combined experience</div></div>'
      '<div class="cell"><div class="n">CPA</div><div class="l">and Enrolled Agent &mdash; Thomas P. Craig</div></div>'
      '<div class="cell"><div class="n">EA</div><div class="l">Enrolled Agent &mdash; Joseph W. Brine</div></div>'
      '<div class="cell"><div class="n">8</div><div class="l">calculators, running on this site</div></div>'
      '</div></section>'

      '<section class="sec" id="services"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">What we do</span><h2>Four services, and they are the same conversation.</h2>'
      '<p class="lead">The books produce the return. The return shapes the planning. The planning decides what the '
      'books need to capture next year. Splitting those across three firms is how small businesses end up paying '
      'for the same information three times.</p>'
      '</div><div class="cards">' + svc_cards + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">All services ' + ARROW + '</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split">'
      '<div class="reveal"><span class="eyebrow">For businesses and for individuals</span>'
      '<h2>Two people, both credentialed, and you will speak to one of them.</h2>'
      '<p class="lead">There is no account management layer here. Thomas P. Craig is a Certified Public Accountant '
      'and an Enrolled Agent; Joseph W. Brine is an Enrolled Agent. Between them the practice states more than 50 '
      'years of combined experience.</p>'
      '<div class="prose" style="margin-top:26px">'
      '<h3>For businesses</h3>'
      '<p>Entity and owner returns prepared together, books kept or reviewed, a QuickBooks file that produces '
      'reports worth reading, payroll postings that agree with the quarterly filings, and someone to call before '
      'a decision rather than after it. Joe Brine\'s experience covers the healthcare, construction and payroll '
      'industries &mdash; the businesses where job costing and payroll deadlines do the most damage when they slip.</p>'
      '<h3>For individuals</h3>'
      '<p>Federal and Massachusetts returns, self-employment and rental income, retirement distributions, a house '
      'sale, a year with two states in it. Most personal returns are straightforward; the ones that are not became '
      'complicated because something happened during the year that nobody mentioned at the time.</p>'
      '<h3>When a letter arrives</h3>'
      '<p>Both professionals here are Enrolled Agents, licensed by the Treasury with unlimited rights to represent '
      'taxpayers before the IRS in examinations, collections and appeals. That means a notice can be handled by the '
      'same people who prepared the return, without a handover and without explaining the facts twice.</p>'
      '<h3>The financial side</h3>'
      '<p>Thomas P. Craig is also licensed to sell securities and insurance products, so a decision can be looked at '
      'from the product side and the tax side in one conversation instead of two. See '
      '<a href="services/financial-services.html">financial services</a>.</p>'
      '</div></div>'
      '<div class="aside"><div class="acard"><div class="t">Call the Mass Tax Pros</div>'
      '<p>Five minutes on the phone is usually enough to work out whether we are the right practice for the job.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Credentials</div><ul>'
      '<li><a href="team/thomas-p-craig.html"><span class="ck">&#10003;</span> Certified Public Accountant</a></li>'
      '<li><a href="team/joseph-w-brine.html"><span class="ck">&#10003;</span> Enrolled Agents, admitted to practice before the IRS</a></li>'
      '<li><a href="services/financial-services.html"><span class="ck">&#10003;</span> Securities and insurance licensed</a></li>'
      '<li><a href="guides/cpa-vs-enrolled-agent.html"><span class="ck">&#10003;</span> What the credentials mean</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">The people</span><h2>You already know who will do the work.</h2>'
      '<p class="lead">Two named professionals, both credentialed, both reachable on the number at the top of this page.</p>'
      '</div><div class="tgrid">' + team_preview + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="team/index.html">More about Tom and Joe ' + ARROW + '</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Tools</span><h2>Run the numbers before you pick up the phone.</h2>'
      '<p class="lead">Eight calculators, built into this site rather than borrowed from a vendor. They run in '
      'your browser: nothing is uploaded, nothing is stored, and no one is asked for an email address first.</p></div>'
      '<div class="cards">'
      + _card(0, 'calculators/self-employment-tax.html', 'calc', 'Self-employment tax',
              'Social Security and Medicare on net self-employment profit, with the deductible half and a quarterly figure.')
      + _card(0, 'calculators/section-179.html', 'chart', 'Equipment purchase',
              'What a Section 179 deduction is worth against your bracket, and the real after-tax cost of the asset.')
      + _card(0, 'calculators/mortgage-payment.html', 'estate', 'Mortgage payment',
              'Principal, interest, taxes and insurance on a fixed-rate loan, plus lifetime interest and loan-to-value.')
      + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="calculators/index.html">All calculators ' + ARROW + '</a></p></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Where we are</span><h2>Heritage Commons, Middlesex Avenue, Wilmington.</h2>'
      '<p class="lead">One office, two professionals, and a telephone that is answered by people who know your file.</p></div>'
      '<div class="split">'
      '<div>' + gmap('Suite 3 at Heritage Commons, 11 Middlesex Avenue, Wilmington, Massachusetts 01887.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + FIRM['ph'] + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Getting in touch</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Open in Google Maps</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the practice</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Common questions</span><h2>Answers before you call.</h2></div>'
      + faq_html(HOME_FAQS)
      + '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">More questions answered ' + ARROW + '</a></p></div></section>'
    )
    P.append(dict(path='index.html', depth=0, nav='home', cta_args=CTA,
      title='Mass Tax Pros | Thomas P. Craig, CPA, PC | Wilmington, MA',
      desc='Tax, accounting, QuickBooks and financial services in Wilmington, Massachusetts. Thomas P. Craig, CPA and Enrolled Agent, with Joseph W. Brine, Enrolled Agent.',
      body=body,
      schema=[org_schema(),
              {"@context": "https://schema.org", "@type": "WebSite", "name": "Mass Tax Pros",
               "alternateName": LEGAL, "url": BASE, "publisher": {"@id": ORG_ID}}]))

    # ----------------------------------------------------------------- ABOUT
    p = dict(path='about.html', depth=0, nav='about', cta_args=CTA,
      title='About the Practice | Thomas P. Craig, CPA, PC | Mass Tax Pros',
      desc='Thomas P. Craig, CPA, PC trades as the Mass Tax Pros in Wilmington, Massachusetts. Tom Craig, CPA and Enrolled Agent, and Joe Brine, Enrolled Agent.',
      eyebrow='About the practice', h1='Two credentialed professionals and one telephone number.',
      sub='Thomas P. Craig, CPA, PC &mdash; trading as the Mass Tax Pros &mdash; works from Heritage Commons on Middlesex Avenue in Wilmington, Massachusetts.')
    p['body'] = phero(p, [('About the practice', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>The practice is small on purpose. Two named professionals, both credentialed, and between them the firm '
      'states more than 50 years of combined experience. There is no account manager, no rotating junior, and '
      'nobody who has to be brought up to speed on your file each spring.</p>'
      '<h2>How it came together</h2>'
      '<p>In 2006 Joe and Tom formed Craig, Brine &amp; Associates, and the company was later incorporated as '
      'Thomas P. Craig, CPA, PC. In 2013 the firm announced the acquisition of Emond Tax &amp; Financial Group. '
      'The practice trades today as the Mass Tax Pros &mdash; Tax and Accounting Service Professionals.</p>'
      '<h2>The two credentials, and why both are here</h2>'
      '<p><strong>Thomas P. Craig</strong> is a Certified Public Accountant and an Enrolled Agent, and is licensed to '
      'sell securities and insurance products. He studied accounting with a minor in economics at the University of '
      'Massachusetts.</p>'
      '<p><strong>Joseph W. Brine</strong> is an Enrolled Agent. He holds a bachelor\'s degree from Merrimack College, '
      'where he majored in accounting, and his experience spans the healthcare, construction and payroll industries.</p>'
      '<p>The CPA licence is granted by a state board and covers the breadth of accounting practice. The Enrolled '
      'Agent designation is granted by the United States Treasury and carries unlimited rights to represent taxpayers '
      'before the IRS &mdash; examinations, collections and appeals. Having both in a two-person practice means the '
      'people who prepared a return are the people who can defend it. <a href="guides/cpa-vs-enrolled-agent.html">'
      'What each credential covers</a>.</p>'
      '<h2>What the practice does</h2>'
      '<p>Four things, and they interlock. <a href="services/income-tax.html">Income tax services</a> for businesses '
      'and individuals. <a href="services/accounting.html">Accounting services</a> &mdash; bookkeeping, the monthly '
      'close and financial statements. <a href="services/quickbooks.html">QuickBooks services</a>, because for most '
      'small businesses the file is the accounting system and it is usually set up wrong. And '
      '<a href="services/financial-services.html">financial services</a>, which exist here so that a product '
      'decision and its tax consequence can be discussed in one conversation.</p>'
      '<h2>How we work</h2>'
      '<h3>Small enough to answer the phone</h3>'
      '<p>A two-person practice cannot serve everybody, and does not try. What it can do is make sure the person who '
      'takes the call is the person who did the work. That is the whole trade.</p>'
      '<h3>Straight answers, including inconvenient ones</h3>'
      '<p>If a structure someone has proposed to you is more complexity than your numbers justify, we will say so. '
      'If the work belongs with a specialist we will point you at one. Neither of those is generosity; it is cheaper '
      'for everyone than taking an engagement that was never a good fit.</p>'
      '<h3>Before, not after</h3>'
      '<p>The decisions that change a tax outcome &mdash; how a purchase is structured, when income lands, what an '
      'owner takes as wages, whether an election is worth making &mdash; are all made while the year is open. '
      'Preparation without planning is transcription.</p>'
      '<h2>Where to go next</h2>'
      '<p>The <a href="services/index.html">services pages</a> set out each area in detail. The '
      '<a href="team/index.html">team pages</a> cover Tom and Joe individually. The '
      '<a href="calculators/index.html">calculators</a> run in your browser if you want to size something up first, '
      'and the <a href="faq.html">common questions</a> page answers most of what people ask on a first call.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">The practice at a glance</div>'
      '<p><strong style="color:#fff">Legal name</strong><br>' + LEGAL + '</p>'
      '<p><strong style="color:#fff">Trading as</strong><br>Mass Tax Pros</p>'
      '<p><strong style="color:#fff">Office</strong><br>Wilmington, Massachusetts</p>'
      '<p><strong style="color:#fff">Professionals</strong><br>Two &mdash; a CPA and Enrolled Agent, and an Enrolled Agent</p>'
      '<a class="btn b-acc" href="contact.html">Contact the practice</a></div>'
      '<div class="acard light"><div class="t">Practice pages</div><ul>'
      '<li><a href="team/index.html"><span class="ck">&rarr;</span> Tom Craig &amp; Joe Brine</a></li>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> All services</a></li>'
      '<li><a href="calculators/index.html"><span class="ck">&rarr;</span> Calculators</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home', BASE), ('About the practice', BASE + 'about.html')])]
    P.append(p)

    # -------------------------------------------------------------- SERVICES
    cards = ''
    for i, s in enumerate(SERVICES):
        cards += ('<a class="card reveal" href="' + s['slug'] + '.html"><span class="num">' + ('0' + str(i + 1))[-2:] + '</span>'
                  '<div class="cic">' + icon(s['ic']) + '</div><h3>' + s['nav_title'] + '</h3><p>' + s['short'] + '</p>'
                  '<span class="more">Read more ' + ARROW + '</span></a>')
    p = dict(path='services/index.html', depth=1, nav='services', cta_args=CTA,
      title='Services | Tax, Accounting & QuickBooks | Mass Tax Pros MA',
      desc='Income tax, accounting, QuickBooks and financial services for businesses and individuals from Thomas P. Craig, CPA, PC in Wilmington, Massachusetts.',
      eyebrow='Services', h1='Four services that only work properly together.',
      sub='Income tax, accounting, QuickBooks and financial services &mdash; for businesses and for the people who own them.')
    p['body'] = phero(p, [('Services', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>What the practice does</h2>'
      '<p class="lead">Thomas P. Craig, CPA, PC works with businesses and with individuals, and for owner-operated '
      'companies those are usually the same engagement seen from two sides.</p></div>'
      '<div class="cards">' + cards + '</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>For businesses</h2>'
      '<p>A small company rarely has an isolated accounting problem. The bookkeeping decides what the return can '
      'say. The return decides what the owner takes home. What the owner takes home decides how the retirement '
      'plan is designed and how much the company can afford to borrow. When those sit with different firms, each '
      'one optimises its own piece and nobody owns the result.</p>'
      '<ul>'
      '<li>Partnership, S corporation, C corporation and single-member LLC returns, federal and Massachusetts</li>'
      '<li>Bookkeeping, the monthly close, reconciliations and financial statements</li>'
      '<li>QuickBooks setup, cleanup and ongoing support</li>'
      '<li>Owner compensation, distributions and basis &mdash; the questions that decide the personal return</li>'
      '<li>Representation before the IRS by Enrolled Agents when a notice or an examination arrives</li>'
      '</ul>'
      '<h2>For individuals</h2>'
      '<p>Federal and Massachusetts returns for employees, the self-employed, landlords, retirees, and people whose '
      'year contained something unusual. If you sold a property, moved between states, exercised equity '
      'compensation, inherited something, or started a business on the side, that is the year to talk to somebody '
      'before December rather than after April.</p>'
      '<ul>'
      '<li>Federal and Massachusetts individual returns</li>'
      '<li>Self-employment and Schedule C income, including quarterly estimates</li>'
      '<li>Rental property, investment income and retirement distributions</li>'
      '<li>Multi-state returns and the credit mechanics between them</li>'
      '<li>IRS notices, examinations, collections and appeals</li>'
      '</ul>'
      '<h2>Where the calculators fit</h2>'
      '<p>The <a href="../calculators/index.html">calculators on this site</a> are there to size a question up '
      'before it becomes a meeting. They run in your browser and send nothing anywhere. They are estimates, not '
      'advice &mdash; but knowing roughly what a quarterly estimate or an equipment purchase does to the number '
      'makes the conversation that follows a much shorter one.</p>'
      '</div><div class="aside"><div class="acard"><div class="t">Not sure where you fit?</div>'
      '<p>Most first calls take ten minutes and end with a clear answer about what the work involves.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Also useful</div><ul>'
      '<li><a href="../guides/cpa-vs-enrolled-agent.html"><span class="ck">&rarr;</span> CPA, EA or preparer?</a></li>'
      '<li><a href="../calculators/index.html"><span class="ck">&rarr;</span> Calculators</a></li>'
      '<li><a href="../team/index.html"><span class="ck">&rarr;</span> Tom Craig &amp; Joe Brine</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/')]),
      {"@context": "https://schema.org", "@type": "ItemList", "name": "Mass Tax Pros services",
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": _plain(s['nav_title']),
                            "url": BASE + 'services/' + s['slug'] + '.html'}
                           for i, s in enumerate(SERVICES)]}]
    P.append(p)
    for s in SERVICES:
        P.append(_svc_page(s))

    # ------------------------------------------------------------------ TEAM
    tcards = ''.join(
      '<a class="tcard reveal" href="' + t['slug'] + '.html"><div class="tava">' + t['initials'] + '</div>'
      '<h3>' + t['name'] + '</h3><div class="cred">' + t['cred'] + '</div><p>' + t['card'] + '</p></a>'
      for t in TEAM)
    p = dict(path='team/index.html', depth=1, nav='team', cta_args=CTA,
      title='Tom Craig & Joe Brine | Mass Tax Pros, Wilmington MA',
      desc='Thomas P. Craig, CPA and Enrolled Agent, and Joseph W. Brine, Enrolled Agent — the two professionals of Thomas P. Craig, CPA, PC in Wilmington, Massachusetts.',
      eyebrow='The people', h1='Two professionals. Both credentialed. Both reachable.',
      sub='The practice states more than 50 years of combined experience between Tom Craig and Joe Brine.')
    p['body'] = phero(p, [('Our team', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Who does the work</h2>'
      '<p class="lead">Credentials, education and the kind of work each one is most often called for.</p></div>'
      '<div class="tgrid">' + tcards + '</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="prose reveal" style="max-width:820px">'
      '<h2>Why the credentials are worth reading carefully</h2>'
      '<p>"Accountant" is not a protected title, and the differences between the people who prepare tax returns are '
      'not cosmetic. Two of them matter here.</p>'
      '<p>A <strong>Certified Public Accountant</strong> is licensed by a state board of accountancy, having passed '
      'the Uniform CPA Examination and met that state\'s education and experience requirements. Thomas P. Craig is '
      'a CPA, and the practice is a professional corporation in his name.</p>'
      '<p>An <strong>Enrolled Agent</strong> is licensed by the United States Treasury, either by passing the '
      'three-part Special Enrollment Examination or through qualifying experience at the IRS. Under Circular 230 an '
      'Enrolled Agent has unlimited practice rights: any taxpayer, any tax matter, any IRS office. Both Tom Craig '
      'and Joe Brine are Enrolled Agents.</p>'
      '<p>The practical difference shows up when something goes wrong. An unenrolled preparer\'s ability to act for '
      'you in front of the IRS is limited; a credentialed practitioner\'s is not. Our '
      '<a href="../guides/cpa-vs-enrolled-agent.html">guide to the credentials</a> works through what each one can '
      'and cannot do.</p>'
      '<h2>What each is most often called for</h2>'
      '<ul>'
      '<li><a href="thomas-p-craig.html">Thomas P. Craig, CPA, EA</a> &mdash; the situations where the tax question '
      'and the financial question are the same question. He is licensed to sell securities and insurance products '
      'as well as holding the accounting credentials.</li>'
      '<li><a href="joseph-w-brine.html">Joseph W. Brine, EA</a> &mdash; businesses with payroll and jobs to cost. '
      'His experience spans the healthcare, construction and payroll industries.</li>'
      '</ul>'
      '<p><a class="btn b-ln" href="../about.html">More about the practice ' + ARROW + '</a></p>'
      '</div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home', BASE), ('Our team', BASE + 'team/')]),
      {"@context": "https://schema.org", "@type": "ItemList", "name": "Mass Tax Pros professionals",
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t['name'],
                            "url": BASE + 'team/' + t['slug'] + '.html'} for i, t in enumerate(TEAM)]}]
    P.append(p)
    for t in TEAM:
        P.append(_bio(t))

    # ----------------------------------------------------------------- GUIDE
    g_faqs = [
      ("Can an Enrolled Agent represent me in an IRS audit?",
       "<p>Yes, without limitation. Circular 230 grants Enrolled Agents unlimited practice rights before the IRS &mdash; any taxpayer, any tax matter, any office, including examinations, collections and appeals.</p>"),
      ("Is a CPA better than an Enrolled Agent?",
       "<p>They are different licences, not different grades. The CPA licence is granted by a state board and spans the breadth of accounting practice, including work an Enrolled Agent is not licensed for. The Enrolled Agent designation is federal and tax-specific, and carries the same unlimited representation rights before the IRS that a CPA has. For a tax matter, either is a credentialed practitioner.</p>"),
      ("What is a PTIN?",
       "<p>A Preparer Tax Identification Number. Anyone paid to prepare a federal return must have one and must sign the return. Holding a PTIN is a registration requirement, not a credential &mdash; it involves no examination of competence.</p>"),
      ("How do I check that someone is who they say they are?",
       "<p>The IRS publishes a public directory of federal tax return preparers with credentials and select qualifications. State boards of accountancy publish CPA licence lookups. Both are free, and a practitioner worth hiring will not mind being checked.</p>"),
    ]
    p = dict(path='guides/cpa-vs-enrolled-agent.html', depth=1, nav='services', cta_args=CTA,
      title='CPA, Enrolled Agent or Tax Preparer? What Each One Can Do',
      desc='What separates a CPA, an Enrolled Agent and an unenrolled tax preparer — licensing, examinations, and who can represent you before the IRS when something goes wrong.',
      eyebrow='Guide', h1='CPA, Enrolled Agent, or preparer: who can actually do what.',
      sub='Three different things sit behind the word &ldquo;accountant&rdquo;. The difference rarely matters &mdash; until the day it matters a great deal.')
    p['body'] = phero(p, [('Guides', 'guides/cpa-vs-enrolled-agent.html'), ('CPA, EA or preparer?', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>Anyone may call themselves an accountant. Nothing stops it, and plenty of competent people who prepare '
      'returns hold no licence at all. But the credentials behind the title are not interchangeable, and the '
      'difference is most visible at exactly the moment you would rather it were not: when the IRS writes to you.</p>'

      '<h2>Certified Public Accountant</h2>'
      '<p>A CPA is licensed by a state board of accountancy. Getting there means passing the Uniform CPA '
      'Examination and meeting that state\'s education and experience requirements; keeping it means continuing '
      'professional education and adherence to professional conduct rules, enforced by the board that issued the '
      'licence.</p>'
      '<p>The licence is broad. It covers tax, but also the parts of accounting practice &mdash; independent '
      'reporting on financial statements in particular &mdash; that an unlicensed person may not perform at all. '
      'A CPA also has unlimited rights to represent taxpayers before the IRS.</p>'

      '<h2>Enrolled Agent</h2>'
      '<p>An Enrolled Agent is licensed by the United States Treasury rather than by a state. There are two routes '
      'in: passing the three-part Special Enrollment Examination, which covers individuals, businesses, and '
      'representation and procedure; or qualifying experience as a former IRS employee. Enrolled Agents must '
      'complete continuing education and are governed by Treasury Circular 230.</p>'
      '<p>The designation is narrower than a CPA licence in scope and identical to it in one respect that matters: '
      'representation. Under Circular 230, Enrolled Agents, CPAs and attorneys all hold <strong>unlimited practice '
      'rights</strong> before the IRS. Any taxpayer, any tax matter, any IRS office. The federal licence also means '
      'an Enrolled Agent is not confined to one state\'s clients.</p>'

      '<h2>The unenrolled preparer</h2>'
      '<p>Anyone paid to prepare federal returns must hold a Preparer Tax Identification Number and must sign the '
      'returns they prepare. That is a registration, not a qualification: no examination, no continuing education '
      'requirement in itself.</p>'
      '<p>Preparers without a credential have <strong>limited</strong> representation rights, and only in narrow '
      'circumstances tied to returns they personally prepared and signed. They cannot represent you at appeals or '
      'in collection matters. If your preparer is unenrolled and your return is selected for examination, you will '
      'be finding new representation at the worst possible moment.</p>'

      '<h2>Side by side</h2>'
      '<table class="plain"><thead><tr><th>&nbsp;</th><th>CPA</th><th>Enrolled Agent</th><th>Unenrolled preparer</th></tr></thead><tbody>'
      '<tr><td><strong>Licensed by</strong></td><td>State board of accountancy</td><td>United States Treasury</td><td>Nobody &mdash; PTIN registration only</td></tr>'
      '<tr><td><strong>Examination</strong></td><td>Uniform CPA Examination</td><td>Special Enrollment Examination, or IRS experience</td><td>None required</td></tr>'
      '<tr><td><strong>Scope</strong></td><td>Accounting practice generally, including tax</td><td>Federal tax matters</td><td>Return preparation</td></tr>'
      '<tr><td><strong>IRS representation</strong></td><td>Unlimited</td><td>Unlimited</td><td>Limited, and only for returns they signed</td></tr>'
      '<tr><td><strong>Continuing education</strong></td><td>Required by the state board</td><td>Required under Circular 230</td><td>Not required</td></tr>'
      '</tbody></table>'

      '<h2>What this means when choosing</h2>'
      '<p>For a simple wage return with no complications, the credential may genuinely not matter. It starts to '
      'matter when there is a business, property, more than one state, equity compensation, a large one-off '
      'transaction, or any history of notices. It matters absolutely if you are already in a dispute.</p>'
      '<p>Three questions worth asking anyone before you engage them:</p>'
      '<ul>'
      '<li><strong>What are you licensed as, and by whom?</strong> The answer should be immediate and checkable.</li>'
      '<li><strong>If this return is examined, can you represent me &mdash; through appeals?</strong> Only a '
      'credentialed practitioner can say yes without qualification.</li>'
      '<li><strong>Will you sign the return?</strong> A paid preparer is required to. Anyone unwilling to is '
      'telling you something important.</li>'
      '</ul>'

      '<h2>How this practice is set up</h2>'
      '<p><a href="../team/thomas-p-craig.html">Thomas P. Craig</a> is a Certified Public Accountant and an '
      'Enrolled Agent. <a href="../team/joseph-w-brine.html">Joseph W. Brine</a> is an Enrolled Agent. Both '
      'therefore hold unlimited practice rights before the IRS, which is the practical reason a notice arriving at '
      'this office does not have to go anywhere else to be dealt with.</p>'

      '<h2>Questions people ask</h2>' + faq_html(g_faqs)
      + '</div>'
      '<div class="aside"><div class="acard"><div class="t">Ask about your own situation</div>'
      '<p>If you are weighing up who should handle a return, describe it in five minutes and we will tell you '
      'straight whether it needs a credentialed practitioner.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="../team/thomas-p-craig.html"><span class="ck">&rarr;</span> Thomas P. Craig, CPA, EA</a></li>'
      '<li><a href="../team/joseph-w-brine.html"><span class="ck">&rarr;</span> Joseph W. Brine, EA</a></li>'
      '<li><a href="../services/income-tax.html"><span class="ck">&rarr;</span> Income tax services</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(),
      breadcrumb_schema([('Home', BASE), ('Guides', BASE + 'guides/cpa-vs-enrolled-agent.html'),
                         ('CPA, EA or preparer?', BASE + 'guides/cpa-vs-enrolled-agent.html')]),
      article_schema('CPA, Enrolled Agent, or preparer: who can actually do what',
                     'What separates a CPA, an Enrolled Agent and an unenrolled tax preparer.',
                     BASE + 'guides/cpa-vs-enrolled-agent.html'),
      faq_schema([(q, _plain(a)) for q, a in g_faqs])]
    P.append(p)

    # ------------------------------------------------------------------- FAQ
    FAQS = HOME_FAQS + [
     ("What should I bring to a first appointment?",
      "<p>For a business: last year's filed return, the books or access to them, the fixed asset detail, payroll reports, and anything carrying a deadline &mdash; a loan agreement, a lease, a letter from a tax authority. For an individual: last year's return and a short note on what changed. If you do not have all of it, come anyway; part of the first meeting is working out what is missing.</p>"),
     ("Do you prepare Massachusetts returns as well as federal?",
      "<p>Yes, and they are not the same exercise. Massachusetts does not simply adopt the federal figure &mdash; personal income conformity, the corporate excise and its non-income measure, and the pass-through entity excise election all have to be worked separately.</p>"),
     ("Can you handle a return that involves more than one state?",
      "<p>Yes. People who move part-way through a year, work across a state line, or own property elsewhere routinely need more than one return. The mistakes usually happen in the credit mechanics between the states rather than in either return on its own.</p>"),
     ("What does an Enrolled Agent's representation actually cover?",
      "<p>Under Treasury Circular 230, unlimited practice rights before the IRS: any taxpayer, any tax matter, any IRS office &mdash; examinations, collections and appeals. It is a federal licence, so it is not limited to one state's residents.</p>"),
     ("Do you do bookkeeping, or only the return?",
      "<p>Both. Some clients want the books kept entirely; others keep their own and have us review and close periodically. The second is cheaper and works well when somebody in the business is careful and has been shown what to watch.</p>"),
     ("Our QuickBooks file is a mess. Can it be fixed?",
      "<p>Almost always, and fixing is usually better than starting again because a new file throws away the comparatives. The first job is finding the point at which the records stop being trustworthy. See <a href=\"services/quickbooks.html\">QuickBooks services</a>.</p>"),
     ("Should I be an S corporation?",
      "<p>Sometimes, and it depends on numbers rather than on principle: what the business earns, what reasonable compensation would look like, how many owners there are, what the state treatment does to the answer, and whether you will keep up with the extra filings. The savings are real in the right situation and illusory in the wrong one.</p>"),
     ("How do the calculators on this site work?",
      "<p>They run entirely in your browser. Nothing is uploaded, nothing is stored, and no email address is asked for. They are estimates built on the assumptions stated beneath each one, and they are not a substitute for advice about your own facts. <a href=\"calculators/index.html\">See them all</a>.</p>"),
     ("What does it cost?",
      "<p>It depends on the work. A straightforward individual return and a business with payroll, inventory and two states are not comparable engagements. Describe the situation on the phone and we will tell you what it involves before anyone commits to anything.</p>"),
     ("Is what I tell you confidential?",
      "<p>Yes. Client information is confidential, and for credentialed practitioners that is a professional obligation with rules behind it rather than a matter of policy.</p>"),
    ]
    p = dict(path='faq.html', depth=0, nav='about', cta_args=CTA,
      title='Common Questions | Mass Tax Pros, Wilmington MA',
      desc='Straight answers about CPA and Enrolled Agent credentials, Massachusetts returns, bookkeeping, QuickBooks cleanups, IRS notices and how engagements at this practice work.',
      eyebrow='Answers', h1='Questions we get asked, answered plainly.',
      sub='If yours is not here, call the office and ask. Nobody will route you to a form.')
    p['body'] = phero(p, [('Common questions', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Working with this practice</h2>'
      '<p class="lead">Credentials, scope, and what to expect from a first conversation.</p></div>'
      + faq_html(FAQS)
      + '<div class="sec-head reveal" style="margin-top:56px"><h2>Still deciding?</h2>'
      '<p class="lead">The longer piece on <a href="guides/cpa-vs-enrolled-agent.html">what separates a CPA, an '
      'Enrolled Agent and an unenrolled preparer</a> covers the question that ought to come first, and the '
      '<a href="calculators/index.html">calculators</a> will size up most of the rest.</p></div>'
      '</div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home', BASE), ('Common questions', BASE + 'faq.html')]),
                   faq_schema([(q, _plain(a)) for q, a in FAQS])]
    P.append(p)

    # --------------------------------------------------------------- CONTACT
    p = dict(path='contact.html', depth=0, nav='contact', cta_args=CTA,
      title='Contact | Mass Tax Pros | Wilmington, Massachusetts',
      desc='Reach Thomas P. Craig, CPA, PC at (978) 657-5272 or info@tpc-cpa.com. Heritage Commons, 11 Middlesex Avenue, Suite 3, Wilmington, Massachusetts 01887.',
      eyebrow='Contact', h1='Call the office. You will get one of us.',
      sub='Heritage Commons, 11 Middlesex Avenue, Suite 3, Wilmington, Massachusetts 01887.')
    p['body'] = phero(p, [('Contact', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Wilmington, Massachusetts</h2>'
      '<p class="lead">One office, two professionals, and no telephone tree between you and them.</p></div>'
      '<div class="split">'
      '<div>' + gmap() + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + FIRM['ph'] + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Quick links</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Directions in Google Maps</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> What the practice does</a></li>'
      '<li><a href="team/index.html"><span class="ck">&rarr;</span> Tom Craig &amp; Joe Brine</a></li>'
      '</ul></div></div></div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>What a first call is like</h2>'
      '<p>Ten minutes, usually. What kind of entity you are or whether this is a personal return, roughly what the '
      'year looked like, and what deadline is driving the question. From that we can normally tell you whether this '
      'is a tax matter, a bookkeeping matter, a QuickBooks matter, or some combination &mdash; and what the work '
      'would involve.</p>'
      '<p>If it belongs somewhere else, we will say so and point you somewhere useful.</p>'
      '<h2>What to have to hand</h2>'
      '<ul>'
      '<li>Last year\'s filed return &mdash; the business return, the personal one, or both</li>'
      '<li>Your most recent financial statements or a copy of the bookkeeping file, in whatever state it is in</li>'
      '<li>Anything with a date on it: a loan agreement, a lease, a letter of intent, an IRS or Department of '
      'Revenue notice</li>'
      '<li>A short description of what changed during the year</li>'
      '</ul>'
      '<p>Missing pieces are normal. Bring what exists.</p>'
      '<h2>If you have had a letter</h2>'
      '<p>Send it before you reply to it. Notices carry response deadlines, and a reply that concedes a point you '
      'did not need to concede is difficult to walk back. Both professionals here are Enrolled Agents with '
      'unlimited rights to represent taxpayers before the IRS.</p>'
      '<h2>Confidentiality</h2>'
      '<p>What you tell us is confidential, including the fact that you called. For credentialed practitioners that '
      'obligation sits in professional rules, not in a policy document.</p>'
      '<h2>Post and fax</h2>'
      '<p>The office address is ' + FIRM['addr'] + ', ' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip']
      + '. The fax line is ' + FIRM['fax'] + '. Email reaches the practice at '
      '<a href="mailto:' + FIRM['email'] + '">' + FIRM['email'] + '</a> &mdash; note that this is a different '
      'domain from the website address, and it is the correct one.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Prefer to write?</div>'
      '<p>Email the practice and one of us will come back to you.</p>'
      '<a class="btn b-acc" href="mailto:' + FIRM['email'] + '">' + FIRM['email'] + '</a></div>'
      '<div class="acard light"><div class="t">Before you call</div><ul>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '<li><a href="guides/cpa-vs-enrolled-agent.html"><span class="ck">&rarr;</span> CPA, EA or preparer?</a></li>'
      '<li><a href="calculators/index.html"><span class="ck">&rarr;</span> Run the numbers first</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home', BASE), ('Contact', BASE + 'contact.html')]),
      {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact " + LEGAL,
       "url": BASE + 'contact.html'}]
    P.append(p)

    # ----------------------------------------------------------- CALCULATORS
    P += _calculator_pages()

    return P


# ---------------------------------------------------------------------------
CALC_INTRO = (
  'These run entirely in your browser. Nothing is uploaded, nothing is stored, and you are not asked for an '
  'email address before you see the answer. Each one states the assumptions it makes underneath the inputs &mdash; '
  'read them, because the assumptions are usually where the difference between an estimate and your actual '
  'position lives.')


def _calculator_pages():
    P = []
    hub_url = BASE + 'calculators/'

    # ------------------------------------------------------------------ hub
    groups = ''
    for cat in C.CATEGORIES:
        items = [c for c in C.CALCULATORS if c['cat'] == cat]
        cards = ''.join(
          '<a class="calccard" href="' + c['slug'] + '.html"><div class="cc">' + c['cat'] + '</div>'
          '<h3>' + c['title'] + '</h3><p>' + c['blurb'] + '</p></a>' for c in items)
        groups += ('<div class="sec-head reveal" style="margin-top:44px"><h3>' + cat + '</h3></div>'
                   '<div class="calcgrid">' + cards + '</div>')

    p = dict(path='calculators/index.html', depth=1, nav='calculators', cta_args=CTA,
      title='Financial Calculators | Mass Tax Pros, Wilmington MA',
      desc='Eight financial calculators that run in your browser — self-employment tax, Section 179, mortgage and refinance, loans, retirement, college saving and business break-even.',
      eyebrow='Calculators', h1='Run the numbers before you pick up the phone.',
      sub='Estimates you can get to in thirty seconds, built into this site rather than borrowed from somewhere else.')
    p['body'] = phero(p, [('Calculators', None)]) + (
      '<style>' + C.CALC_CSS + '</style>'
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Eight calculators, no sign-up</h2>'
      '<p class="lead">' + CALC_INTRO + '</p></div>'
      + groups
      + '</div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>What a calculator is good for</h2>'
      '<p>Sizing a question. Whether a refinance is worth the closing costs, roughly what a quarter\'s '
      'self-employment tax will be, what a piece of equipment really costs after the deduction, how far off a '
      'retirement number is. Those are answerable in a minute, and knowing the order of magnitude changes what you '
      'do next.</p>'
      '<h2>What it is not good for</h2>'
      '<p>Deciding. Every model here holds constant things that do not hold constant: rates change, the Social '
      'Security wage base is reset annually, deduction limits and phase-outs move, and none of these calculators '
      'knows your filing status, your other income, or the Massachusetts consequences of any of it.</p>'
      '<p>Treat the output as the start of a conversation. When the number is big enough to matter, call the '
      'office and we will work it properly.</p>'
      '<h2>Where they connect to the work</h2>'
      '<ul>'
      '<li><a href="self-employment-tax.html">Self-employment tax</a> and <a href="section-179.html">equipment '
      'purchase</a> &mdash; see <a href="../services/income-tax.html">income tax services</a>.</li>'
      '<li><a href="break-even.html">Break-even</a> and <a href="loan-payment.html">loan payment</a> &mdash; see '
      '<a href="../services/accounting.html">accounting services</a>.</li>'
      '<li><a href="retirement-savings.html">Retirement</a> and <a href="college-savings.html">college saving</a> '
      '&mdash; see <a href="../services/financial-services.html">financial services</a>.</li>'
      '</ul>'
      '</div><div class="aside"><div class="acard"><div class="t">Got a number you do not like?</div>'
      '<p>That is usually the moment a conversation is worth having. Call the office.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="../services/index.html"><span class="ck">&rarr;</span> All services</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '<li><a href="../contact.html"><span class="ck">&rarr;</span> Contact the practice</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [org_schema(), breadcrumb_schema([('Home', BASE), ('Calculators', hub_url)]),
      {"@context": "https://schema.org", "@type": "ItemList", "name": "Mass Tax Pros calculators",
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c['title'],
                            "url": BASE + 'calculators/' + c['slug'] + '.html'}
                           for i, c in enumerate(C.CALCULATORS)]}]
    P.append(p)

    # ------------------------------------------------------------ one each
    for i, c in enumerate(C.CALCULATORS):
        url = BASE + 'calculators/' + c['slug'] + '.html'
        desc = c['blurb']
        if len(desc) < 100:
            desc += ' A free calculator from Mass Tax Pros in Wilmington, Massachusetts.'
        nxt = C.CALCULATORS[(i + 1) % len(C.CALCULATORS)]
        prv = C.CALCULATORS[(i - 1) % len(C.CALCULATORS)]
        cp = dict(path='calculators/' + c['slug'] + '.html', depth=1, nav='calculators', cta_args=CTA,
                  title=c['title'] + ' calculator | Mass Tax Pros',
                  desc=desc, eyebrow=c['cat'], h1=c['title'],
                  sub=c['blurb'])
        ph = phero(cp, [('Calculators', 'calculators/index.html'), (c['title'], None)])
        cp['body'] = (
          '<style>' + C.CALC_CSS + '</style>'
          + C.calc_page_body(c, ph, rel, ARROW, 1)
          + '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
            '<h2>Before you rely on this</h2>'
            '<p class="lead">It is an estimate. It runs in your browser on the assumptions printed beside the '
            'inputs, it does not know your filing status or your other income, and it does not model the '
            'Massachusetts consequences. When the number matters, call the office on '
            '<a href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a> and we will work it properly.</p></div>'
            '<div class="cards two">'
            '<a class="card reveal" href="' + prv['slug'] + '.html"><div class="cic">' + icon('calc') + '</div>'
            '<h3>' + prv['title'] + '</h3><p>' + prv['blurb'] + '</p>'
            '<span class="more">Open it ' + ARROW + '</span></a>'
            '<a class="card reveal" href="' + nxt['slug'] + '.html"><div class="cic">' + icon('chart') + '</div>'
            '<h3>' + nxt['title'] + '</h3><p>' + nxt['blurb'] + '</p>'
            '<span class="more">Open it ' + ARROW + '</span></a>'
            '</div>'
            '<p style="margin-top:30px"><a class="btn b-ln" href="index.html">All calculators ' + ARROW + '</a></p>'
            '</div></section>'
          + C.CALC_JS)
        cp['schema'] = [org_schema(),
          breadcrumb_schema([('Home', BASE), ('Calculators', hub_url), (c['title'], url)]),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": c['title'] + ' calculator',
           "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
           "description": _plain(c['blurb']), "url": url,
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "publisher": {"@id": ORG_ID}}]
        P.append(cp)

    return P
