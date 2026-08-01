# -*- coding: utf-8 -*-
"""
Content for James L. Hickey, CPA PC — Tewksbury, Massachusetts.

Honesty posture for this build: the firm's site names one person (James L. Hickey,
CPA) with no title and no bio, states no founding year, no staff count, no
memberships and no office hours. None of those are asserted here. The site is
substantial on services, which the firm genuinely has, and silent everywhere else.
"""
import html, re
from build import (FIRM, BASE, T, icon, ARROW, GLYPH, phero, faq_html, rel, gmap,
                   breadcrumb_schema, faq_schema, article_schema)
import calculators as C

PORTAL = 'https://www.securefirmportal.com/Account/Login/4700'
ORG_ID = BASE + '#firm'

DEFAULT_CTA = ('Start with a phone call.',
               'Call the office at (978) 851-8945 or write to info@hickeycpa.com. Describe the '
               'situation, and we will tell you what the work involves and whether this is the '
               'right office for it.')


def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()


def _org():
    """Organisation schema built only from published facts. Deliberately carries no
    foundingDate, no memberOf and no openingHours — the site states none of them."""
    return {"@context": "https://schema.org", "@type": "AccountingService", "@id": ORG_ID,
            "name": FIRM['name'], "legalName": FIRM['name'], "url": BASE,
            "email": FIRM['email'], "telephone": FIRM['ph'], "faxNumber": FIRM['fax'],
            "priceRange": "$$",
            "description": ("A full service tax, accounting and business consulting firm "
                            "located in Tewksbury, Massachusetts."),
            "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                        "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                        "postalCode": FIRM['zip'], "addressCountry": "US"},
            "areaServed": [{"@type": "AdministrativeArea", "name": "Merrimack Valley, Massachusetts"}],
            "hasMap": FIRM['maps']}


def _svc_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "description": desc, "url": url, "serviceType": name,
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "AdministrativeArea", "name": "Merrimack Valley, Massachusetts"}}


def _card(d, href, ic, title, text, num=None):
    return ('<a class="card reveal" href="' + rel(d, href) + '">'
            + ('<span class="num">' + num + '</span>' if num else '')
            + '<div class="cic">' + icon(ic) + '</div><h3>' + title + '</h3><p>' + text + '</p>'
            '<span class="more">Read more ' + ARROW + '</span></a>')


def _why_aside(d):
    """Four claims, each of them checkable against the firm's own site."""
    return ('<div class="acard light"><div class="t">About this office</div><ul>'
            '<li><a href="' + rel(d, 'contact.html') + '"><span class="ck">&#10003;</span> '
            'One office &mdash; 170 Main Street, Tewksbury</a></li>'
            '<li><a href="' + rel(d, 'services/irs-representation.html') + '"><span class="ck">&#10003;</span> '
            'A working IRS problem-resolution practice</a></li>'
            '<li><a href="' + rel(d, 'services/quickbooks.html') + '"><span class="ck">&#10003;</span> '
            'QuickBooks setup, training and tune-ups</a></li>'
            '<li><a href="' + rel(d, 'client-portal.html') + '"><span class="ck">&#10003;</span> '
            'Secure portal for exchanging documents</a></li>'
            '</ul></div>')


# =========================================================================
# SERVICES
# =========================================================================
SERVICES = [

 dict(slug='tax-preparation', ic='ledger', nav_title='Tax Return Preparation',
   short='Federal and Massachusetts returns for individuals, families, sole proprietors, partnerships, corporations and fiduciaries.',
   title='Tax Return Preparation | James L. Hickey, CPA, Tewksbury MA',
   desc='Federal and Massachusetts tax return preparation for individuals, small businesses, partnerships, corporations and fiduciaries, from a CPA office in Tewksbury.',
   eyebrow='Tax', h1='Returns prepared by a CPA, in an office you can walk into.',
   sub='Individual, business and fiduciary returns, federal and Massachusetts &mdash; prepared, reviewed and signed here on Main Street.',
   body='''
<h2>The short answer</h2>
<p>We prepare federal and Massachusetts income tax returns for individuals and families, for sole proprietors and single-member LLCs, for partnerships and multi-member LLCs, for S corporations and C corporations, and for the fiduciaries who administer trusts and estates. Where a business owner and the business are both our clients, the returns are prepared together, by the same office, in the same cycle.</p>

<h2>Why the entity return and the owner return belong together</h2>
<p>For a closely held company they are one calculation split across two forms. Owner compensation, shareholder basis, distributions, loans between the owner and the company, health insurance for a more-than-2% S corporation shareholder, the qualified business income deduction and its limits &mdash; every one of those items is decided on the entity return and lands on the individual return. When two different offices prepare the two returns, the reconciliation nobody performed is the item that surfaces later.</p>

<h2>Massachusetts, specifically</h2>
<p>A Merrimack Valley practice sees the same state questions repeatedly, and they are not the questions a national tax program prompts you about:</p>
<ul>
<li><strong>Living in one state, earning in another.</strong> Tewksbury sits close enough to New Hampshire that a large share of local households have income sourced across a state line. Non-resident and part-year filings, and the credit for taxes paid to another jurisdiction, decide who ends up taxing what.</li>
<li><strong>Remote and hybrid work.</strong> Where the work is physically performed drives the sourcing. Arrangements that changed quietly during the year tend to be discovered at filing.</li>
<li><strong>The pass-through entity excise election.</strong> Massachusetts offers an entity-level election for pass-through businesses with a corresponding credit for owners. It helps some owners and does nothing for others, and it is an election with a deadline.</li>
<li><strong>Rental property and second homes.</strong> Depreciation history, passive activity limits, and what happens on sale &mdash; including the depreciation recapture that owners are almost never expecting.</li>
<li><strong>Massachusetts estimated payments.</strong> Underpayment interest is charged quarter by quarter, so a large fourth-quarter payment does not cure the first three.</li>
</ul>

<h2>What to send, and how</h2>
<p>The list is shorter than most people fear: last year's return if we did not prepare it, the income documents you have received, records for anything you intend to deduct, and a short note describing what changed during the year. Documents can be dropped at the office or uploaded through the <a href="../client-portal.html">secure client portal</a> rather than emailed &mdash; ordinary email is not a good place for a Social Security number.</p>

<h2>The half of the work that is not typing</h2>
<p>A return is a record of decisions that were already made. The useful part of the engagement is the review that happens alongside it: whether the entity is still the right one, whether estimated payments are set correctly for next year, whether a retirement plan contribution is worth making, whether a large purchase should be timed differently, and whether anything on the return will draw an inquiry. That work is <a href="tax-planning.html">tax planning</a>, and it is worth more than the preparation fee.</p>

<div class="callout"><p><strong>Behind on filings?</strong> Prior-year returns are prepared here as a matter of routine, and getting current is the first step in almost every IRS matter. See <a href="non-filed-returns.html">non-filed returns</a>.</p></div>

<h2>Extensions</h2>
<p>An extension moves the filing deadline, not the payment deadline. The balance is still due on the original date, and interest runs from that date regardless. Filed properly, with a reasonable payment attached, an extension is an ordinary and unremarkable thing. Filed as a way of not thinking about it, it is how a small balance becomes a collection matter.</p>
''',
   faqs=[("Do you prepare returns for people who are not business clients?",
          "<p>Yes. Individual and family returns are a substantial part of the practice, including retirees, households with income in more than one state, and people with rental property or investment activity.</p>"),
         ("Can you prepare returns for a state other than Massachusetts?",
          "<p>Yes. Non-resident and part-year filings, and the credits that keep the same income from being taxed twice, come up constantly in this part of the state.</p>"),
         ("How do I get documents to you safely?",
          "<p>Drop them at the office, or upload them through the <a href=\"../client-portal.html\">secure client portal</a>. Please do not send tax documents as ordinary email attachments.</p>"),
         ("Will you sign the return as preparer?",
          "<p>Yes. A paid preparer is required to sign the return and provide a preparer identification number. Anyone unwilling to do that is telling you something.</p>")],
   related=[('tax-planning', 'Tax planning'), ('irs-representation', 'IRS problem resolution'),
            ('small-business-services', 'Small business services'),
            ('../calculators/self-employment-tax.html', 'Self-employment tax calculator')]),

 dict(slug='tax-planning', ic='plan', nav_title='Tax Planning',
   short='Work done during the year, while the decisions that move the number are still in front of you rather than behind you.',
   title='Tax Planning | James L. Hickey, CPA PC, Tewksbury MA',
   desc='Year-round tax planning for Merrimack Valley individuals and small businesses: entity choice, owner compensation, timing, retirement plans and estimated payments.',
   eyebrow='Tax', h1='Planning happens during the year. Filing only records it.',
   sub='By April the decisions have been made. The conversations that change a tax bill happen in June, in September and before you sign a purchase order.',
   body='''
<h2>The short answer</h2>
<p>Tax planning is the part of the engagement that changes the number. It covers entity structure, owner compensation, the timing of income and deductions, equipment and vehicle purchases, retirement plan contributions, the treatment of a property sale, and the estimated payments that keep the whole thing from becoming a penalty. It happens while the year is still open.</p>

<h2>Where the money actually moves</h2>
<h3>Entity structure and owner compensation</h3>
<p>Whether a business is a sole proprietorship, a partnership, an S corporation or a C corporation changes what is subject to self-employment tax, what is available as a qualified business income deduction, and what happens on an eventual sale. For an S corporation the follow-on question is reasonable compensation: too little invites an adjustment, too much converts profit into payroll tax voluntarily. Neither answer is a formula, and both are decided during the year. See <a href="entity-formation.html">entity selection</a>.</p>

<h3>Timing</h3>
<p>Accelerating a deduction into this year or deferring income into next is worth doing only when you know which year carries the higher rate. That requires a projection, not an instinct. A projection also tells you when the opposite is true &mdash; a year with unusually low income is often the right year to recognise a gain, convert a retirement account, or take a distribution.</p>

<h3>Buying equipment</h3>
<p>Section 179 and bonus depreciation let a business deduct much of an asset in the year it is placed in service, but the deduction cannot create a loss, business-use percentage matters, and vehicles carry their own limits. Run the numbers before the purchase order rather than after: the <a href="../calculators/section-179.html">equipment purchase calculator</a> shows what a deduction is worth against your rate and what the asset really costs after tax.</p>

<h3>Retirement plans</h3>
<p>For an owner with profit and no plan, this is frequently the largest single lever available. A SEP, a SIMPLE, a solo 401(k) and a profit sharing plan each have different contribution ceilings, different employee coverage consequences, and different deadlines &mdash; some of which fall before year end, which is exactly why the conversation cannot wait for filing season.</p>

<h3>Estimated payments</h3>
<p>Underpayment interest is calculated quarter by quarter. The safe-harbour rules based on the prior year's liability are the practical tool for anyone with variable income, and setting the payments correctly costs nothing.</p>

<h2>What a planning conversation looks like</h2>
<p>Usually one meeting late in the year with a projection in front of us, and short calls whenever something material happens: a large purchase, a new state, a change in ownership, an offer for the business, a property under agreement, a spouse changing jobs. The calls are the cheap part. The unannounced transaction is the expensive part.</p>

<div class="callout"><p><strong>Before you sign anything unusual, call.</strong> Nearly every expensive tax outcome we are asked to fix was structured without a five-minute phone call that would have been free.</p></div>

<h2>Planning for individuals</h2>
<p>Not all of it is business work. Sale of a home, an inheritance, exercising options, a Roth conversion, funding education, charitable giving, and the year someone retires all have a right and a wrong sequence. See <a href="personal-financial-planning.html">personal financial planning</a> and <a href="estate-planning.html">estate planning</a>.</p>
''',
   faqs=[("When should planning happen?",
          "<p>Before the transaction, and at the latest before December 31. After year end the facts are fixed and the return simply records them.</p>"),
         ("Is planning a separate engagement from preparing my return?",
          "<p>It is separate work and takes separate time, whether or not it is billed separately. Preparation records history; planning changes it.</p>"),
         ("Can you project what I will owe before the year ends?",
          "<p>Yes, and for anyone with variable income that projection is the point. It drives the estimated payments and shows whether a year-end move is worth making.</p>"),
         ("Does an S election always save tax?",
          "<p>No. It shifts part of the profit out of self-employment tax, and it adds payroll, a separate return, reasonable compensation exposure and basis tracking. Below a certain level of profit the arithmetic does not favour it.</p>")],
   related=[('tax-preparation', 'Tax return preparation'), ('entity-formation', 'Entity selection'),
            ('small-business-services', 'Small business services'),
            ('../calculators/section-179.html', 'Equipment purchase calculator')]),

 dict(slug='irs-representation', ic='shield', nav_title='IRS Problem Resolution',
   short='Representation before the IRS: examinations, notices, collection, liens and levies, and the transcripts that tell you what the Service actually has.',
   title='IRS Problem Resolution & Representation | Tewksbury MA CPA',
   desc='Representation before the IRS from a Tewksbury CPA office: examinations, collection notices, liens, levies and wage garnishment, and getting your IRS file first.',
   eyebrow='IRS problems', h1='When the IRS writes, you do not have to answer it alone.',
   sub='A CPA may represent you before the Internal Revenue Service at every level. That means the correspondence, the calls and the meetings can stop coming to you.',
   body='''
<h2>The short answer</h2>
<p>This office represents taxpayers before the IRS. That covers examinations of a return, correspondence notices, the collection process, liens and levies, wage garnishment, unfiled returns and payment arrangements. Representation begins with a signed authorisation; from that point the Service deals with us.</p>

<h2>Who is allowed to represent you</h2>
<p>Three categories of practitioner may represent a taxpayer before the IRS without limitation: attorneys, certified public accountants, and enrolled agents. A seasonal preparer without credentials generally cannot, which is why a great many people discover at the worst moment that the person who prepared the return cannot accompany them to defend it.</p>

<h2>Start by finding out what they actually have</h2>
<p>The single most common mistake is answering a notice before reading the file. With a signed authorisation we can obtain your IRS transcripts: what returns are on record and which are missing, what income was reported to the Service under your Social Security or employer number, what assessments exist, what has been paid, what penalties and interest have accrued, and where each year sits in the collection cycle.</p>
<p>That file routinely contradicts the notice. Income gets double-reported. A return filed on time gets posted to the wrong year. A substitute return prepared by the Service for a non-filer allows no deductions at all and produces a balance far larger than the real one. None of that is visible from the letter on your kitchen table.</p>

<div class="callout"><p><strong>Deadlines on IRS letters are real.</strong> Some notices carry a fixed window after which an appeal right is simply gone. Bring the letter in with the envelope &mdash; the dates matter.</p></div>

<h2>The matters we handle</h2>
<h3>Examinations and correspondence audits</h3>
<p>Most examinations now arrive as a letter proposing a change, not as an agent at the door. They are answerable, and they are answerable much better with documentation assembled in the order the examiner needs it. An unanswered proposal becomes an assessment by default.</p>

<h3>Collection</h3>
<p>Once a balance is assessed, the Service moves through a sequence of notices and then to enforced collection: a federal tax lien, a levy on a bank account, or a garnishment of wages. Each stage has procedural rights attached, and each has a way out that is available before the stage is reached and harder afterward. See <a href="irs-payment-plans.html">payment arrangements</a>.</p>

<h3>Unfiled returns</h3>
<p>Nothing else can be resolved until the missing returns are filed. It is also the step people avoid longest. <a href="non-filed-returns.html">How that gets unwound</a>.</p>

<h3>Liability that belongs to a spouse or former spouse</h3>
<p>A joint return makes both signers responsible for the whole balance. There are statutory routes out for a spouse who did not know, and a separate remedy for a spouse whose refund was taken for the other's separate debt. See <a href="innocent-injured-spouse.html">innocent and injured spouse relief</a>.</p>

<h3>Payroll tax</h3>
<p>Unpaid payroll tax is treated differently from every other business balance, because part of it is money withheld from employees. It can be assessed personally against the people responsible for paying it, and it is the fastest-escalating balance a small business can carry. If you are behind on deposits, call before the next one is due.</p>

<h2>What we will not tell you</h2>
<p>That the balance can be made to disappear, or that a settlement for a fraction of it is available. Some taxpayers do qualify for a reduced settlement and many do not, and the answer depends on income, assets and allowable expenses measured against published standards &mdash; not on who you hire. An honest first conversation sorts realistic outcomes from advertising.</p>

<h2>Massachusetts too</h2>
<p>State notices from the Department of Revenue follow their own procedures and their own timetables, and a federal adjustment usually produces a state one a few months later. Both sides of the problem are handled here.</p>
''',
   faqs=[("What is the first thing I should do with an IRS letter?",
          "<p>Read the deadline, keep the envelope, and do not throw it away. Then bring it in before responding. Many notices are wrong, and some carry rights that expire.</p>"),
         ("Can you talk to the IRS on my behalf?",
          "<p>Yes, once a written authorisation is filed. A CPA has unlimited representation rights before the Service, which means examinations, collection and appeals.</p>"),
         ("Can you find out what the IRS has on file for me?",
          "<p>Yes. Transcripts show filed and missing returns, income reported under your number, assessments, payments, and penalty and interest accruals. That file is where any serious matter starts.</p>"),
         ("Will hiring a CPA make the problem worse?",
          "<p>Representation is an ordinary and expected part of the process. What makes matters worse is silence: unanswered notices become assessments, and assessments become liens and levies.</p>"),
         ("Do you handle Massachusetts Department of Revenue matters as well?",
          "<p>Yes. State notices run on their own schedule, and a federal change generally produces a state one in its wake.</p>")],
   related=[('non-filed-returns', 'Non-filed returns'), ('irs-payment-plans', 'IRS payment plans'),
            ('innocent-injured-spouse', 'Innocent &amp; injured spouse'),
            ('../guides/irs-notice-what-to-do.html', 'Guide: an IRS notice arrived')]),

 dict(slug='non-filed-returns', ic='doc', nav_title='Non-Filed Returns',
   short='Getting current on missing years, and correcting the substitute returns the Service prepares when you do not file one yourself.',
   title='Non-Filed Tax Returns | James L. Hickey, CPA, Tewksbury MA',
   desc='Behind on tax returns? A Tewksbury CPA office reconstructs missing years, corrects IRS substitute returns, and gets you current before collection escalates.',
   eyebrow='IRS problems', h1='Every year you have not filed is still open.',
   sub='Nothing else can be settled until the missing returns are in. It is almost always less serious than the person avoiding it believes.',
   body='''
<h2>The short answer</h2>
<p>We prepare and file prior-year returns, reconstruct the records needed to support them, and correct the substitute returns the IRS files on a non-filer's behalf. Getting current is the precondition for everything else &mdash; no payment arrangement, no settlement, no release of a levy is available to a taxpayer who is not filed up to date.</p>

<h2>What happens while you are not filing</h2>
<p>The Service does not simply wait. Using the income reported to it by employers, banks, brokers and clients, it can prepare a substitute return for you. That return allows no itemised deductions, no business expenses, no dependants, and no favourable filing status. The resulting balance is often several times the real one, and penalties and interest then accrue on that inflated figure.</p>
<p>The good news buried in that: filing an accurate return for the year usually reduces the assessment substantially, and it can be done after the substitute return has been issued.</p>

<h2>Penalties, plainly</h2>
<p>There are two separate penalties and they are commonly confused. The failure-to-file penalty accrues at a materially higher monthly rate than the failure-to-pay penalty, and it is capped. In practice that means the single most expensive thing a taxpayer can do is not file because they cannot pay. Filing on time and paying late costs far less than the reverse. Interest runs on all of it.</p>

<div class="callout"><p><strong>If you are owed a refund, it expires.</strong> There is a limited window to claim a refund for a given year. Wait past it and the money is simply gone &mdash; while any year with a balance stays collectible.</p></div>

<h2>How the work actually goes</h2>
<h3>1. Pull the file</h3>
<p>Transcripts tell us which years are genuinely missing, what income was reported under your number for each of them, and whether the Service has already assessed anything. That takes the guesswork out of a pile of years.</p>
<h3>2. Reconstruct what is missing</h3>
<p>Almost nobody has clean records for the years they did not file. Bank and card statements, third-party income records, prior returns, mileage evidence, mortgage and property tax records and vendor histories are usually enough to build a defensible return. Reasonable reconstruction is expected and accepted; guessing is not.</p>
<h3>3. File in the right order</h3>
<p>Which years go first is a decision, not a formality &mdash; it affects refund windows, carryforwards, and how quickly the Service will consider a payment arrangement.</p>
<h3>4. Deal with the balance</h3>
<p>Once the real numbers exist, the balance is usually smaller than the substitute assessments suggested, and it can be addressed through an <a href="irs-payment-plans.html">arrangement</a>. Penalty relief is worth asking about where there is a clean prior history or a genuine reason for the lapse.</p>

<h2>Businesses behind on filings</h2>
<p>An entity that has stopped filing accumulates its own problems: state charter status, payroll filings, and information returns that carry per-form penalties. Where a company is behind, the entity and the owner have to be brought current together, because each return depends on the other.</p>

<h2>The part nobody says out loud</h2>
<p>People do not fail to file because they are careless. They fail to file because one bad year became two, and by year three the pile felt unapproachable. It is a common situation, it is fixable, and the conversation is a professional one rather than a moral one.</p>
''',
   faqs=[("How many years do I have to file?",
          "<p>It depends on what is missing and what the Service has already assessed. Transcripts settle it. In many cases getting current means a specific and limited set of years rather than everything.</p>"),
         ("I have no records for those years. Is it hopeless?",
          "<p>No. Returns are routinely reconstructed from bank and card statements, third-party income records and other documentation. Reasonable reconstruction is expected.</p>"),
         ("What if the IRS already filed a return for me?",
          "<p>A substitute return allows no deductions or exemptions and usually overstates the tax badly. Filing an accurate return for the year normally reduces it, and that remains possible after the substitute has been issued.</p>"),
         ("Will filing old returns trigger enforcement?",
          "<p>Non-filing is what drives enforcement. Voluntarily getting current is the step that stops the escalation and opens the arrangements that resolve the balance.</p>")],
   related=[('irs-representation', 'IRS representation'), ('irs-payment-plans', 'IRS payment plans'),
            ('tax-preparation', 'Tax return preparation'),
            ('../guides/irs-notice-what-to-do.html', 'Guide: an IRS notice arrived')]),

 dict(slug='irs-payment-plans', ic='clock', nav_title='IRS Payment Plans',
   short='Installment agreements, hardship status and the arithmetic the Service actually applies to a balance you cannot pay at once.',
   title='IRS Payment Plans & Installment Agreements | Tewksbury MA CPA',
   desc='Help arranging an IRS installment agreement or hardship status from a Tewksbury CPA office, including what the Service counts as income, assets and allowable expenses.',
   eyebrow='IRS problems', h1='A balance you cannot pay at once is a process, not a verdict.',
   sub='The Service has defined routes for taxpayers who owe more than they can pay today. Which one applies is arithmetic, and the arithmetic is knowable in advance.',
   body='''
<h2>The short answer</h2>
<p>Where a balance is owed and cannot be paid immediately, we work out which resolution the numbers actually support and put it in place: a short-term extension to pay, an installment agreement, a temporary hardship suspension of collection, or in the right circumstances an application to settle for less than the full amount. Filing must be current first &mdash; the Service will not arrange anything for a taxpayer with missing returns.</p>

<h2>The routes, and who each one fits</h2>
<h3>Short-term extension to pay</h3>
<p>For a balance that will be cleared within a few months. No agreement fee, interest and the failure-to-pay penalty continue, and it is the cheapest option when it is genuinely achievable.</p>

<h3>Installment agreement</h3>
<p>Monthly payments over time. Below certain balance thresholds these are close to automatic and require little financial disclosure. Above them, the Service wants a full financial picture, and the monthly figure is derived from it rather than proposed by you. Direct debit lowers the setup fee and reduces the chance of default.</p>

<h3>Partial payment arrangements</h3>
<p>Where the full balance cannot be paid within the remaining collection period, a smaller monthly payment can be accepted with the understanding that the balance may expire before it is fully paid. These carry periodic financial review.</p>

<h3>Currently not collectible</h3>
<p>Where allowable living expenses genuinely consume income, collection can be suspended. Interest and penalties continue and the account is reviewed periodically, but levies and garnishment stop. For a household in real difficulty this is often the correct answer, and it is under-used because taxpayers do not know to ask.</p>

<h3>Offer in compromise</h3>
<p>A settlement for less than the balance, available where the Service concludes it cannot collect more within the remaining period. Acceptance rests on a formula: realisable equity in assets plus a multiple of monthly income remaining after allowable expenses. It is a real remedy for the taxpayers who fit it, and it is heavily advertised to taxpayers who do not. We will run your numbers through the same test the Service applies and tell you what it produces before you spend anything on an application.</p>

<div class="callout"><p><strong>Allowable expenses are not your expenses.</strong> Collection calculations use published standards for food, housing, transport and health care. A budget that includes private school fees and two car payments will not survive the substitution &mdash; which is why an arrangement should be built on the Service's arithmetic rather than on yours.</p></div>

<h2>Things that quietly matter</h2>
<ul>
<li><strong>Penalties and interest keep running</strong> throughout every arrangement. An installment agreement is not a freeze.</li>
<li><strong>A federal tax lien may still be filed</strong> above certain balance levels even while you are paying. That affects credit and the sale or refinancing of property.</li>
<li><strong>Default is easy.</strong> A missed payment, a new balance, or a late return in a later year can terminate the agreement and restart enforcement. Keeping current going forward is part of the deal.</li>
<li><strong>Refunds are applied to the balance</strong> while an arrangement is running.</li>
<li><strong>Collection has a time limit,</strong> and where each year sits within it changes which resolution is sensible.</li>
</ul>

<h2>Business balances</h2>
<p>Arrangements for a business follow different rules, and payroll tax balances follow rules of their own because part of the money was withheld from employees. Those can be assessed personally against the people responsible. A business behind on deposits should call before the next deposit is due rather than after.</p>

<h2>What we need to start</h2>
<p>The notices you have received, the last two or three years of returns, and an honest picture of income, expenses, assets and debts. From that we can usually tell you within a meeting which route the numbers support.</p>
''',
   faqs=[("Can I set up a payment plan if I have unfiled returns?",
          "<p>No. Getting <a href=\"non-filed-returns.html\">current on filings</a> is the precondition for every arrangement the Service offers.</p>"),
         ("Do penalties stop once I am on a plan?",
          "<p>No. Interest and the failure-to-pay penalty continue to accrue while the balance is outstanding, which is why a shorter arrangement costs less overall.</p>"),
         ("Will a lien be filed against me?",
          "<p>Possibly, depending on the balance. A lien can attach even while an agreement is in place, and it affects credit and any sale or refinancing of property.</p>"),
         ("Can I settle for less than I owe?",
          "<p>Sometimes. Acceptance rests on a defined formula covering asset equity and income remaining after allowable expenses. We will run your figures through that formula and tell you the answer before you spend money on an application.</p>")],
   related=[('irs-representation', 'IRS representation'), ('non-filed-returns', 'Non-filed returns'),
            ('innocent-injured-spouse', 'Innocent &amp; injured spouse'),
            ('../calculators/loan-payment.html', 'Loan payment calculator')]),

 dict(slug='innocent-injured-spouse', ic='gavel', nav_title='Innocent &amp; Injured Spouse',
   short='Two different remedies for two different problems: liability that belongs to a spouse, and a refund taken for a spouse&rsquo;s separate debt.',
   title='Innocent Spouse & Injured Spouse Relief | Tewksbury MA CPA',
   desc='Innocent spouse and injured spouse relief explained and prepared by a Tewksbury CPA office: which remedy applies, what the IRS weighs, and the deadlines involved.',
   eyebrow='IRS problems', h1='A joint return makes both signatures responsible for all of it.',
   sub='There are two separate remedies, they solve two different problems, and they are constantly confused with each other.',
   body='''
<h2>The short answer</h2>
<p>Sign a joint return and each spouse is responsible for the entire balance, regardless of whose income or error produced it. Two distinct remedies exist. <strong>Innocent spouse relief</strong> asks to be released from a liability caused by the other spouse. <strong>Injured spouse allocation</strong> asks for the return of your share of a joint refund that was seized for your spouse's separate debt. Different forms, different tests, different deadlines.</p>

<h2>Innocent spouse relief</h2>
<p>This applies where a joint return understated the tax because of the other spouse's income or improper deduction, and you did not know and had no reason to know. Three routes exist within it, and which one fits depends on whether you are still married, whether the tax was understated or merely unpaid, and how the household actually operated.</p>
<p>What the Service weighs, in practice: your involvement in the household finances and in the business, whether you received a material benefit from the unreported income, your education and business experience, whether you were deceived or prevented from asking questions, whether there was abuse or financial control, your current financial position, and whether you have been compliant since.</p>
<p>The claim is stronger when the story is specific. A spouse who never saw a bank statement, whose name was on a return signed at the kitchen table, and who learned about the business only when the notice arrived is describing something an examiner recognises. A spouse who signed knowing the figures were wrong is not.</p>

<div class="callout"><p><strong>There is a deadline, and it is not obvious.</strong> The principal route generally has to be claimed within a limited period after collection activity begins &mdash; not after the return was filed. Do not wait to see whether the problem goes away.</p></div>

<h2>Injured spouse allocation</h2>
<p>Entirely different situation. The joint return is correct and produces a refund, but the refund is taken to satisfy a debt that belongs to your spouse alone: past-due child support, a defaulted student loan, a state obligation, or federal tax from before the marriage. The injured spouse claim recovers the portion of the refund attributable to your income and your withholding.</p>
<p>It can be filed with the return if you know the offset is coming, or afterwards once it has happened. In a community property state the allocation follows different rules; Massachusetts is not one, which keeps the arithmetic comparatively clean.</p>

<h2>Which one is yours</h2>
<table class="plain"><thead><tr><th>Your situation</th><th>Remedy</th></tr></thead><tbody>
<tr><td>A joint return understated tax because of your spouse's income or deductions, and you did not know</td><td>Innocent spouse relief</td></tr>
<tr><td>Your joint refund was taken for a debt that is your spouse's alone</td><td>Injured spouse allocation</td></tr>
<tr><td>A joint balance you both knew about, and you are now separated or divorced</td><td>Separation of liability may apply; equitable relief is the fallback</td></tr>
<tr><td>You signed under pressure, or were not permitted to see the finances</td><td>Innocent spouse relief, with the circumstances documented</td></tr>
</tbody></table>

<h2>A note on divorce decrees</h2>
<p>A decree that assigns the tax debt to your former spouse binds the two of you. It does not bind the IRS, which was not a party to it and will continue to collect from whichever signature it can reach. This is one of the most common and most damaging misunderstandings we encounter.</p>

<h2>How this is handled here</h2>
<p>Discreetly. These matters usually arrive alongside a separation, a bereavement or a business failure, and the facts are personal. We work from the transcripts and the documents, prepare the claim with the narrative that the form requires, and deal with the Service directly so that the correspondence does not keep landing on your doormat.</p>
''',
   faqs=[("What is the difference between innocent spouse and injured spouse?",
          "<p>Innocent spouse relief releases you from a liability created by your spouse. Injured spouse allocation recovers your share of a joint refund that was taken for your spouse's separate debt. Different forms and different tests.</p>"),
         ("My divorce decree says the tax is my former spouse's responsibility.",
          "<p>That agreement binds the two of you, not the IRS. The Service was not a party to the decree and will continue to pursue either signature on the joint return.</p>"),
         ("Is there a time limit?",
          "<p>Yes, and the main route generally runs from when collection activity started rather than from when the return was filed. It is worth checking the date early.</p>"),
         ("Will my spouse be told that I applied?",
          "<p>The other spouse is notified and given the opportunity to participate; that is built into the process. Your address and personal information are not disclosed to them.</p>")],
   related=[('irs-representation', 'IRS representation'), ('irs-payment-plans', 'IRS payment plans'),
            ('non-filed-returns', 'Non-filed returns'), ('tax-preparation', 'Tax return preparation')]),

 dict(slug='small-business-services', ic='chart', nav_title='Small Business Services',
   short='Bookkeeping oversight, financial statements, cash management, payroll and sales tax filings, and the internal controls a small office can actually run.',
   title='Small Business Accounting Services | Tewksbury, Massachusetts',
   desc='Accounting for Merrimack Valley small businesses: financial statements, bookkeeping oversight, cash management, payroll and sales tax filings, and internal controls.',
   eyebrow='Business', h1='Numbers a small business can actually run on.',
   sub='Most owners are not short of data. They are short of a monthly figure they trust and a person to interpret it.',
   body='''
<h2>The short answer</h2>
<p>We support the accounting function of small and closely held businesses: financial statement preparation, review and oversight of the bookkeeping, month-end close discipline, cash management, payroll and sales tax filings, and internal controls sized for an office with three people in it rather than thirty.</p>

<h2>The problem with most small-company financials</h2>
<p>They are built for the tax return. That is understandable, and it is also why so many owners cannot answer basic questions from their own statements: which job actually made money, what the real cost of a crew hour is, whether last month was profitable or merely busy.</p>
<p>A chart of accounts designed around a tax form satisfies a filing and informs nobody. Restructuring it &mdash; separating direct costs from overhead, splitting revenue into the lines management thinks in, isolating owner-discretionary spending &mdash; usually takes one engagement and changes every conversation afterwards.</p>

<h2>What the work covers</h2>
<h3>Financial statements</h3>
<p>Statements prepared on the basis appropriate to whoever is going to read them: an owner, a bank, a bonding company, a landlord or a buyer. Where an outside party has specified a level of service &mdash; a compilation, a review, or an audit &mdash; the requirement usually comes from a document you already signed. Read the covenant before you buy the higher level; the difference in cost is substantial and the requirement is often lower than assumed.</p>

<h3>Bookkeeping oversight</h3>
<p>Most of our business clients have somebody doing the day-to-day entry, in house or outsourced. That arrangement usually should not change. What we add is structure, periodic review, reconciliation discipline and the judgement calls a bookkeeper is not positioned to make. Where the books live in QuickBooks, see <a href="quickbooks.html">QuickBooks consulting</a>.</p>

<h3>Cash management</h3>
<p>Profit and cash are different things, and businesses fail on the second one. The practical work is a thirteen-week cash projection, a receivables ageing that somebody actually acts on, payment terms that are enforced, inventory that is not quietly financing itself, and a plan for the seasonal trough before the trough arrives. Cash management sits directly alongside <a href="bank-financing.html">bank financing</a>, because a lender is buying your cash forecast more than your profit.</p>

<h3>Payroll and sales tax</h3>
<p>Payroll tax deposits and returns, and Massachusetts sales and use tax filings, are the obligations with the least forgiving penalties, because part of the money was never yours. Worker classification is the other recurring exposure: treating someone as a contractor who is functionally an employee is a costly assumption, and Massachusetts applies a stricter test than most states.</p>

<h3>Internal controls</h3>
<p>Segregation of duties is difficult in a small office and it is not impossible. There are controls that fit a company with two people in the back office: the owner opening the bank statement before anyone else sees it, dual authorisation above a threshold, a second signature on new vendor setup, someone other than the person who writes cheques performing the reconciliation. Small-business fraud is almost always committed by a long-serving, trusted employee in an environment where one person controlled the whole cycle.</p>

<div class="callout"><p><strong>Clean books lower every other fee you pay.</strong> Tax preparation, financing applications, valuations and diligence all begin by establishing that the numbers can be relied on. When they can, everything downstream is faster and cheaper.</p></div>

<h2>Reporting an owner will actually read</h2>
<p>A monthly package that takes ten minutes: the two or three measures that move this particular business, a comparison against last year and against the budget, a cash position, and a short note on what changed. Fourteen pages of general ledger accounts is not a management report.</p>

<h2>How this connects to the rest</h2>
<p>The same office prepares the <a href="tax-preparation.html">business and owner returns</a>, handles the <a href="tax-planning.html">planning</a>, deals with an <a href="irs-representation.html">IRS matter</a> if one arises, and can value the business when it comes time to sell or hand it on. That is the argument for a small firm doing all of it.</p>
''',
   faqs=[("Do you replace our bookkeeper?",
          "<p>Rarely, and usually we advise against it. Daily entry belongs with a bookkeeper; the firm should be providing structure, review, statement preparation and judgement.</p>"),
         ("How often should we close the books?",
          "<p>Monthly, finished within the first two weeks. A perfect close delivered in June informs nothing. Speed matters more than precision in management reporting.</p>"),
         ("Can you handle payroll and sales tax filings?",
          "<p>Yes. These carry the least forgiving penalties because the money was withheld or collected on somebody else's behalf, and they should never be the thing that slips.</p>"),
         ("We think an employee may be taking money. What now?",
          "<p>Call before confronting anyone and before touching the records. What matters first is preserving the evidence and understanding the exposure, and the sequence is easy to get wrong.</p>")],
   related=[('quickbooks', 'QuickBooks consulting'), ('bank-financing', 'Bank financing'),
            ('entity-formation', 'Entity selection'),
            ('../calculators/break-even.html', 'Break-even calculator')]),

 dict(slug='bank-financing', ic='handshake', nav_title='Bank Financing &amp; Business Plans',
   short='Loan packages, projections and business plans built to answer the questions a credit committee is going to ask.',
   title='Bank Financing & Business Plans | Tewksbury MA CPA Firm',
   desc='Help preparing a loan package, projections and a business plan for a Massachusetts lender or SBA application, from a CPA office in Tewksbury.',
   eyebrow='Business', h1='Lenders are buying a forecast. Give them one that holds.',
   sub='A financing package is a document written for a reader you will never meet. The work is anticipating their questions.',
   body='''
<h2>The short answer</h2>
<p>We prepare the accounting side of a financing application: historical statements in the form the lender expects, projections with assumptions that can be defended, a debt service coverage calculation, personal financial statements, and the written business plan that carries the whole thing. We also help evaluate the terms you are offered.</p>

<h2>Who reads it, and what they are looking for</h2>
<p>The loan officer you meet is not the person who approves the credit. Your package will be summarised for a committee by somebody working from the numbers alone, so it has to be self-explanatory. Four questions decide the outcome:</p>
<ol>
<li><strong>Can the business service the debt?</strong> Debt service coverage &mdash; cash available for debt service against total obligations, including the proposed loan. Lenders have a floor and it is not negotiable.</li>
<li><strong>What happens if the forecast is wrong?</strong> Collateral, personal guarantees and the equity the owner has in the deal.</li>
<li><strong>Is the history consistent with the projection?</strong> A forecast showing a step change with no explanation reads as optimism.</li>
<li><strong>Who is behind it?</strong> The personal financial statement and credit history of the owners, particularly where guarantees are involved.</li>
</ol>

<h2>What we prepare</h2>
<h3>Historical financial statements</h3>
<p>Two to three years, in the level of service the lender specified. Adjustments for owner-discretionary items should be shown transparently as add-backs and explained, not buried &mdash; a normalising adjustment that surfaces later looks like something else entirely.</p>

<h3>Projections</h3>
<p>Monthly for the first year, annually beyond it, with the assumptions written down beside the figures. The credibility is entirely in the assumptions: where the revenue comes from, what has to be true for it to arrive, how the cost base moves with it, and what the loan proceeds actually buy. A projection that only goes up is not persuasive.</p>

<h3>The business plan</h3>
<p>Short and specific beats long and general. What the business does, who buys it and why, who else sells it, what the money is for, what it produces, how the debt gets repaid, and who is running it. Ten pages that answer those questions outperform forty that avoid them.</p>

<h3>Personal financial statements</h3>
<p>Required almost universally where a guarantee is involved, and worth preparing carefully rather than from memory.</p>

<div class="callout"><p><strong>Covenants are the part nobody reads.</strong> A minimum coverage ratio, a leverage ceiling, restrictions on distributions or additional debt, and a reporting requirement with a deadline. Every one of them is a promise you are making about how the company will be run for the next several years. Ask what happens if you breach one &mdash; before you sign.</p></div>

<h2>SBA and local lending</h2>
<p>SBA-guaranteed programmes carry heavier documentation and longer timelines, and they exist to make a loan possible where a conventional one is not. Massachusetts also has community lenders and local bank programmes with different appetites from the national institutions. Which door to knock on is worth a conversation before you have three declines on your record.</p>

<h2>Terms are negotiable, in both directions</h2>
<p>Rate is the number everyone focuses on and it is rarely the most expensive term. Amortisation period, prepayment penalties, the reporting burden, personal guarantee scope, and whether the facility renews annually all cost real money or real freedom. A slightly higher rate on a longer amortisation with a lighter covenant package is frequently the better deal.</p>

<h2>Related work</h2>
<p>Financing questions run into <a href="small-business-services.html">cash management</a>, <a href="entity-formation.html">entity structure</a>, and eventually <a href="business-valuation.html">valuation</a>. The <a href="../calculators/loan-payment.html">loan payment calculator</a> shows what a given facility costs monthly.</p>
''',
   faqs=[("What do lenders ask for first?",
          "<p>Two to three years of financial statements and returns for the business and its owners, an interim statement, a projection, a personal financial statement, and a description of what the money is for.</p>"),
         ("How far out should projections go?",
          "<p>Monthly for the first twelve months and annually for two or three more, with written assumptions. The assumptions are what get tested.</p>"),
         ("Is a business plan really necessary for an existing company?",
          "<p>For a straightforward equipment loan, often not. For an acquisition, an expansion, a new line or an SBA application, yes &mdash; because the request is about the future rather than the record.</p>"),
         ("Should I take the lowest rate offered?",
          "<p>Not automatically. Amortisation, prepayment terms, guarantee scope and covenants often cost more than the rate difference.</p>")],
   related=[('small-business-services', 'Small business services'), ('business-valuation', 'Business valuation'),
            ('entity-formation', 'Entity selection'),
            ('../calculators/loan-payment.html', 'Loan payment calculator')]),

 dict(slug='business-valuation', ic='scale', nav_title='Business Valuation',
   short='What a closely held business is worth, for a sale, a buy-sell agreement, a gift or estate filing, a divorce or a shareholder dispute.',
   title='Business Valuation | James L. Hickey, CPA PC, Tewksbury MA',
   desc='Business valuation for Massachusetts closely held companies: sales and acquisitions, buy-sell agreements, gift and estate filings, divorce and shareholder disputes.',
   eyebrow='Business', h1='The number depends on why you are asking.',
   sub='Value is not a single fact about a company. It is a conclusion reached under a stated standard, for a stated purpose, on a stated date.',
   body='''
<h2>The short answer</h2>
<p>We value closely held businesses and ownership interests in them. The first question in every engagement is not what the company is worth but why the figure is needed, because the purpose determines the standard of value, the level of report, and often the answer itself.</p>

<h2>Why the purpose changes the number</h2>
<p>The same company can be worth materially different amounts on the same day depending on the question being asked:</p>
<ul>
<li><strong>Sale or acquisition.</strong> Investment value &mdash; what the business is worth to a particular buyer, including the savings or opportunities that buyer specifically brings.</li>
<li><strong>Gift and estate filings.</strong> Fair market value under the standard the tax authorities apply, with discounts for lack of control and lack of marketability where the facts support them. This is the setting where documentation matters most, because the reader may be an examiner.</li>
<li><strong>Buy-sell agreements.</strong> Whatever the agreement says, which is why the agreement should say something sensible before anyone needs to rely on it.</li>
<li><strong>Divorce.</strong> Governed by state law and, in a professional practice, by the difficult question of what part of the value is personal to the owner and therefore not transferable.</li>
<li><strong>Shareholder disputes.</strong> Fair value, which in many contexts excludes the minority and marketability discounts that would apply in a market transaction.</li>
</ul>

<h2>How a valuation is built</h2>
<h3>Normalising the earnings</h3>
<p>Reported profit for a closely held business is an artefact of tax planning. The work is to restate it: owner compensation to a market rate, personal expenses removed, related-party rent adjusted to market, one-off items stripped out, and non-operating assets separated. The normalised earnings figure is where most of the argument lives, and where most of the value is created or lost.</p>

<h3>The three approaches</h3>
<p>An income approach capitalises or discounts expected earnings, and turns on the rate applied &mdash; which prices the risk that those earnings do not repeat. A market approach compares transactions in similar businesses, useful where genuine comparables exist. An asset approach values the underlying assets net of liabilities, and generally sets the floor rather than the answer for a profitable operating business. Most conclusions weight more than one.</p>

<h3>Discounts</h3>
<p>A minority interest cannot force a distribution, a sale or a change of management, and an interest in a private company cannot be sold quickly at a known price. Both facts reduce value, and both have to be supported rather than asserted.</p>

<div class="callout"><p><strong>The cheapest valuation you will ever buy is the one for your buy-sell agreement, bought while everyone is still on good terms.</strong> The most expensive is the one commissioned after a death, a divorce or a falling out, when every assumption is contested.</p></div>

<h2>What drives value up before a sale</h2>
<p>Owners consistently underestimate how much of the price is decided in the two or three years beforehand. Customer concentration, dependence on the owner personally, whether the accounting records survive scrutiny, the state of contracts and leases, whether there is a second layer of management, and how clean the tax history is all move the multiple, and most of them are fixable with lead time. See <a href="succession-planning.html">succession planning</a>.</p>

<h2>What we will tell you</h2>
<p>Where the value is defensible, where it is soft, and what a buyer or an examiner is likely to attack. A valuation that only says what the client hoped it would say is worth nothing at the point it is needed.</p>
''',
   faqs=[("How long does a valuation take?",
          "<p>It depends on the purpose, the level of report and the condition of the records. Complete financial information for the last several years is the single biggest factor in the timetable.</p>"),
         ("What do you need from us?",
          "<p>Several years of financial statements and returns, interim figures, the ownership documents and any buy-sell agreement, major contracts and leases, and a conversation about how the business actually operates.</p>"),
         ("Why is my business worth less than the revenue multiple I read about?",
          "<p>Rules of thumb ignore margin, customer concentration, owner dependence, capital requirements and the quality of the records &mdash; which is to say, everything a buyer prices.</p>"),
         ("Can one valuation serve several purposes?",
          "<p>Usually not. The standard of value and the level of report differ by purpose, and a report prepared for one use is vulnerable when produced in another.</p>")],
   related=[('succession-planning', 'Succession planning'), ('estate-planning', 'Estate planning'),
            ('bank-financing', 'Bank financing'), ('small-business-services', 'Small business services')]),

 dict(slug='succession-planning', ic='merge', nav_title='Succession Planning',
   short='Moving a business to the next owner &mdash; family, management or an outside buyer &mdash; with the tax and the timetable worked out in advance.',
   title='Business Succession Planning | Tewksbury, Massachusetts CPA',
   desc='Succession planning for Massachusetts family and closely held businesses: transfers to family or management, sale readiness, buy-sell funding and the tax sequence.',
   eyebrow='Business', h1='Every owner leaves. Only some of them choose how.',
   sub='Succession is a transaction that takes years to prepare and hours to regret. The planning is mostly about sequence.',
   body='''
<h2>The short answer</h2>
<p>We work with owners on the transfer of a business: to family, to management, or to an outside buyer. That covers valuation, the structure of the transfer, the tax consequences on both sides, buy-sell agreements and how they are funded, and the practical question of what the business looks like once the owner is no longer in it every day.</p>

<h2>The three exits</h2>
<h3>To family</h3>
<p>The hardest of the three, because it is a business decision inside a family. The questions are rarely financial first: which children are in the business and which are not, whether the ones who are not should receive equity or something else, whether the successor is genuinely capable and genuinely willing, and whether the departing owner can actually let go of the decisions. Gifting programmes, family entity structures and valuation discounts are all available, and none of them fix the underlying question.</p>

<h3>To management</h3>
<p>Preserves continuity and generally sells for less than an outside buyer would pay, because the buyers are funding it from the business itself. Structures usually involve seller financing, an earn-out, or a gradual transfer of equity over several years &mdash; which means the departing owner remains exposed to the performance of a company they no longer control.</p>

<h3>To an outside buyer</h3>
<p>Usually the highest price and the least continuity. The preparation is different in kind: two or three years of clean, reviewable records, reduced customer concentration, contracts that transfer, a management layer beneath the owner, and a tax structure decided before a letter of intent is signed rather than after.</p>

<h2>Asset sale or share sale, and why it matters</h2>
<p>Buyers generally want to buy assets: a stepped-up basis to depreciate, and no inherited liabilities. Sellers generally prefer to sell shares: one layer of tax, and the liabilities go with the company. The gap between those positions is real money, and it is a price term, not a legal detail. The negotiation goes far better when the seller understands the arithmetic before the offer arrives. For a C corporation the double-tax exposure on an asset sale can be severe enough to change the whole plan &mdash; and it takes years to unwind.</p>

<div class="callout"><p><strong>Start earlier than feels necessary.</strong> Most of the levers &mdash; entity structure, records quality, reducing owner dependence, gifting programmes &mdash; need two to five years to work. An owner who decides to sell in January and wants to close by December has already given up most of them.</p></div>

<h2>Buy-sell agreements</h2>
<p>Every business with more than one owner needs one, and a large share of the agreements we read do not work. The recurring failures: a fixed price set years ago and never updated, a valuation formula nobody has tested against reality, no funding mechanism, and no provision for the events that actually happen &mdash; disability, divorce, an owner who simply stops turning up. Life insurance funding is common and its structure matters, because who owns the policy changes the tax result.</p>

<h2>The part that is not a document</h2>
<p>A business where the owner holds all the customer relationships, all the pricing knowledge and all the supplier goodwill is difficult to transfer at any price. Building the second layer &mdash; delegating the relationships, writing down what is in the owner's head, letting somebody else make decisions badly for a while &mdash; is the work that raises the value most and gets started last.</p>

<h2>Related</h2>
<p>Succession runs directly into <a href="business-valuation.html">valuation</a>, <a href="estate-planning.html">estate planning</a> and <a href="tax-planning.html">tax planning</a>. It should be one conversation, not three.</p>
''',
   faqs=[("How far ahead should succession planning start?",
          "<p>Two to five years for most of the levers to work, and longer where entity structure has to change or a successor has to be developed.</p>"),
         ("Is selling to my children better than selling outside?",
          "<p>Different, not better. Family transfers preserve continuity and typically realise less cash. The right answer depends on what the owner needs financially and whether a capable successor genuinely wants it.</p>"),
         ("Our buy-sell agreement has a fixed price from years ago.",
          "<p>Then it will produce a wrong answer at the worst moment. Fixed prices should be revisited annually or replaced with a defensible mechanism.</p>"),
         ("Why does asset versus share sale matter so much?",
          "<p>It changes who bears which tax and how much of the price survives it. For a C corporation seller in particular the difference can be large enough to reshape the deal.</p>")],
   related=[('business-valuation', 'Business valuation'), ('estate-planning', 'Estate planning'),
            ('tax-planning', 'Tax planning'), ('entity-formation', 'Entity selection')]),

 dict(slug='entity-formation', ic='building', nav_title='New Business Formation',
   short='Choosing between a sole proprietorship, an LLC, an S corporation and a C corporation, and setting the new business up so it works from day one.',
   title='New Business Formation & Entity Selection | Tewksbury MA CPA',
   desc='Entity selection and new business setup in Massachusetts: sole proprietorship, LLC, S corporation or C corporation, plus registrations, payroll and record keeping.',
   eyebrow='Business', h1='The entity you choose decides what you pay for years.',
   sub='It is a cheap decision to make correctly at the start and an expensive one to change later.',
   body='''
<h2>The short answer</h2>
<p>We help people starting a business choose an entity, register it properly in Massachusetts, and set up the accounting, payroll and record keeping so the first year does not have to be reconstructed afterwards. Where an existing business has outgrown its structure, we look at whether changing is worth what it costs.</p>

<h2>The choice, without the marketing</h2>
<table class="plain"><thead><tr><th>Structure</th><th>Liability</th><th>How profit is taxed</th><th>Typically suits</th></tr></thead><tbody>
<tr><td><strong>Sole proprietorship</strong></td><td>None &mdash; personal exposure</td><td>On your return; all profit subject to self-employment tax</td><td>Testing an idea with little risk and little profit</td></tr>
<tr><td><strong>LLC (single member)</strong></td><td>Limited, if maintained properly</td><td>Same as a proprietorship by default</td><td>Almost every small start &mdash; protection without complexity</td></tr>
<tr><td><strong>LLC (multi member)</strong></td><td>Limited</td><td>As a partnership, with an operating agreement governing the split</td><td>Two or more owners who need the split written down</td></tr>
<tr><td><strong>S corporation</strong></td><td>Limited</td><td>Profit passes through; only reasonable wages face payroll tax</td><td>Consistent profit well above a market salary for the owner</td></tr>
<tr><td><strong>C corporation</strong></td><td>Limited</td><td>Taxed at the entity, again on distribution</td><td>Outside investors, retained earnings for growth, certain benefit plans</td></tr>
</tbody></table>
<p>An LLC is a legal form, not a tax classification. The same LLC can be taxed as a proprietorship, a partnership, an S corporation or a C corporation. Most of the internet argument about LLCs versus S corporations is a confusion between those two levels.</p>

<h2>When an S election is worth it</h2>
<p>Only when profit is comfortably and reliably above what the owner would have to be paid as a salary. Below that, the payroll administration, the separate return, the reasonable compensation exposure and the basis tracking cost more than the saving. Above it, the arithmetic can be substantial. It is a calculation, run on your actual figures, and it should be revisited as the business grows into or out of it.</p>

<div class="callout"><p><strong>The Massachusetts details that catch people.</strong> Annual reports are due to the Commonwealth and lapsing has consequences. Sales and use tax registration is required before you make a taxable sale, not after. Workers compensation coverage is effectively mandatory once you have employees. And worker classification is tested strictly here &mdash; treating someone as a contractor because it is simpler is one of the more expensive assumptions a new business can make.</p></div>

<h2>Setting it up so it works</h2>
<ul>
<li><strong>A separate bank account from the first dollar.</strong> Commingling is the fastest way to weaken the liability protection you paid for, and the surest way to make year one expensive to reconstruct.</li>
<li><strong>An employer identification number,</strong> and state registrations for withholding and sales tax where they apply.</li>
<li><strong>A chart of accounts that reflects the business,</strong> set up once rather than patched for three years. See <a href="quickbooks.html">QuickBooks setup</a>.</li>
<li><strong>An accounting method and a year end,</strong> chosen deliberately.</li>
<li><strong>Estimated tax payments,</strong> because nobody is withholding for you any more. This is the single most common first-year shock.</li>
<li><strong>An operating agreement or shareholder agreement</strong> where there is more than one owner, including what happens if one of them leaves. See <a href="succession-planning.html">buy-sell agreements</a>.</li>
</ul>

<h2>Changing structure later</h2>
<p>Possible, and rarely free. Electing S status for an existing corporation raises built-in gains exposure; converting an S corporation to a C corporation carries a waiting period before it can be reversed; moving assets between entities can trigger tax. None of that is a reason to stay in a structure that no longer fits, but all of it is a reason to model the change before making it.</p>
''',
   faqs=[("Do I need an LLC to start?",
          "<p>Not legally, but the protection is inexpensive relative to what it guards against, and it costs nothing in tax terms by default. The usual answer for a small start is an LLC taxed as a proprietorship.</p>"),
         ("At what profit does an S election make sense?",
          "<p>When profit is reliably above a market salary for the owner's role, by enough to cover payroll administration and a separate return. It is a calculation on your figures, not a threshold you read online.</p>"),
         ("Can I set the company up myself online?",
          "<p>You can file the formation documents yourself. What the filing does not do is choose the tax classification, register you for the taxes you owe, or set up the books &mdash; and those are the parts that cost money when they are wrong.</p>"),
         ("What do new owners get wrong most often?",
          "<p>Not making estimated tax payments, and mixing personal and business money in one account. Both are trivial to avoid and painful to unwind.</p>")],
   related=[('small-business-services', 'Small business services'), ('tax-planning', 'Tax planning'),
            ('quickbooks', 'QuickBooks consulting'),
            ('../calculators/break-even.html', 'Break-even calculator')]),

 dict(slug='non-profit', ic='gov', nav_title='Non-Profit Organizations',
   short='Accounting, reporting and annual filings for charities and other exempt organizations, and the governance work that keeps exemption intact.',
   title='Non-Profit Accounting & Form 990 | Tewksbury MA CPA Firm',
   desc='Accounting and reporting for Massachusetts non-profit organizations: Form 990 and state filings, fund accounting, board reporting and protecting exempt status.',
   eyebrow='Organizations', h1='An exempt organization answers to more readers than a business does.',
   sub='Members, a board, funders, the Commonwealth and the public can all see the filings. That changes what the accounting has to do.',
   body='''
<h2>The short answer</h2>
<p>We work with non-profit organizations on their accounting, their annual information returns and state filings, their board and funder reporting, and the internal controls and governance practices that keep exempt status secure.</p>

<h2>Why non-profit accounting is genuinely different</h2>
<p>The organization is accountable for how money was used, not for what it earned. That produces requirements a commercial business never meets: contributions with donor restrictions tracked separately from unrestricted funds, expenses allocated across programme, management and fundraising, in-kind contributions valued and recorded, and grants recognised according to the terms of each award rather than when the cash arrives. A bookkeeper who has only worked in commercial accounting will usually get the restriction tracking wrong, and it is not a small error &mdash; it is the whole point of the statements.</p>

<h2>The annual filing is a public document</h2>
<p>The federal information return is published. Donors read it, watchdogs score it, journalists check it, and competing organizations look at it. Two things follow. First, the functional expense allocation matters, because the programme percentage it produces is the figure people quote. Second, the narrative sections are an opportunity most organizations waste: they are the place to describe what the organization actually accomplished, and they are frequently left as a single sentence.</p>
<p>Which version of the return applies depends on gross receipts and assets. Small organizations file a short electronic notice; larger ones file the full return with its schedules. Missing the filing for three consecutive years causes exemption to be revoked automatically, and getting it back is slow and expensive.</p>

<div class="callout"><p><strong>Massachusetts has its own requirements.</strong> Public charities register and file annually with the Attorney General&rsquo;s Division of Public Charities, and the level of accompanying financial statement &mdash; none, a review, or an audit &mdash; steps up with the organization&rsquo;s support. Solicitation registration applies before you ask the public for money. These are separate from the federal filing and they are commonly overlooked.</p></div>

<h2>Where exempt status is actually put at risk</h2>
<ul>
<li><strong>Private benefit and insider transactions.</strong> Compensation and contracts with board members and their relatives need documented, disinterested approval and evidence that the terms are reasonable.</li>
<li><strong>Unrelated business income.</strong> Revenue from a trade or business not related to the exempt purpose is taxable and reported separately. Advertising, some rental arrangements and certain services are the usual sources.</li>
<li><strong>Political activity.</strong> Prohibited for charities in the case of candidate campaigns, and limited for lobbying.</li>
<li><strong>Missed filings.</strong> The most common cause of lost exemption, and entirely avoidable.</li>
</ul>

<h2>Controls in an organization run by volunteers</h2>
<p>Small charities carry a specific risk: enthusiastic people, thin administration, and often one bookkeeper or treasurer with complete control of the cycle. Practical safeguards exist &mdash; a board member reviewing the bank statement independently, dual signatures above a threshold, two people counting cash collections, and a treasurer who is not also the person entering the transactions. A board that never sees a reconciliation is not overseeing anything.</p>

<h2>Reporting a board can govern with</h2>
<p>A statement of financial position, a statement of activities against budget, a cash position with the runway stated in months, and a short note on restricted funds and what remains unspent. Board members are volunteers, most are not accountants, and a package they cannot read produces a board that approves everything.</p>
''',
   faqs=[("Which annual return does our organization file?",
          "<p>It depends on gross receipts and total assets. Very small organizations file a short electronic notice; larger ones file the full return with schedules. Missing it three years running revokes exemption automatically.</p>"),
         ("Do we need an audit?",
          "<p>Not necessarily. The requirement usually comes from the state charities registration thresholds, a funder, or your own bylaws. Read the source before commissioning one.</p>"),
         ("What is unrelated business income?",
          "<p>Income from a regularly carried on trade or business that is not substantially related to the exempt purpose. It is taxable and reported separately, and advertising and some rental income are frequent examples.</p>"),
         ("Can board members be paid?",
          "<p>Reasonable compensation for actual services is permitted, but the approval must be documented, the interested party must not participate in the decision, and the terms must be supportable.</p>")],
   related=[('small-business-services', 'Small business services'), ('quickbooks', 'QuickBooks consulting'),
            ('tax-preparation', 'Tax return preparation'), ('../contact.html', 'Contact the office')]),

 dict(slug='personal-financial-planning', ic='vault', nav_title='Personal Financial Planning',
   short='The accounting view of a household: cash flow, tax position, retirement projections, education funding and how the pieces interact.',
   title='Personal Financial Planning | James L. Hickey, CPA, Tewksbury',
   desc='Personal financial planning from a Tewksbury CPA office: household cash flow, retirement projections, education funding, insurance review and the tax consequences.',
   eyebrow='Individuals', h1='A plan is what happens after the arithmetic.',
   sub='Most household financial questions turn out to be tax questions wearing different clothes.',
   body='''
<h2>The short answer</h2>
<p>We work with individuals and families on the financial planning that sits next to the tax return: household cash flow, retirement projections, education funding, the tax treatment of what you already hold, insurance adequacy in outline, and the sequence in which large decisions should be taken.</p>

<h2>What a CPA brings to this that is different</h2>
<p>We see the return. That means the analysis starts from what is actually happening rather than from what you remember: the real income, the real deductions, the actual investment income and its character, the retirement contributions being made and the ones being missed, and the marginal rate that determines whether any given move is worth making. And we are not selling a product, which changes which recommendations are available.</p>

<h2>The questions that come up most</h2>
<h3>Am I saving enough, and where should it go?</h3>
<p>The ordering matters more than the amount for most households: capture any employer match first, clear high-rate debt, build a cash reserve, then fill tax-advantaged space, then taxable investing. The choice between pre-tax and Roth contributions is a bet on your rate now against your rate later, and for many people the answer changes at least once during a career. The <a href="../calculators/retirement-savings.html">retirement savings calculator</a> shows what a given rate compounds to.</p>

<h3>What does retirement actually look like?</h3>
<p>Two projections, not one: what you will have, and what you will need. The gap between them is the plan. Sequencing then matters as much as the total &mdash; which accounts to draw first, how that interacts with Social Security timing, and how the years between retiring and required minimum distributions can be used for conversions at a low rate. That window is one of the most valuable and most missed planning opportunities in a household's life.</p>

<h3>College</h3>
<p>Massachusetts households face high costs and a state that offers a deduction for contributions to its own plan. The <a href="../calculators/college-savings.html">college savings calculator</a> gives the projected number, which is usually larger than expected. Worth saying plainly: retirement cannot be borrowed for, and education can.</p>

<h3>Debt, in what order</h3>
<p>Rate order is mathematically correct. Smallest-balance order works better for some people because it is finished more often. Where mortgage refinancing is in question, the <a href="../calculators/refinance-breakeven.html">break-even calculator</a> answers the only question that matters: how long you have to stay for it to pay.</p>

<h3>Insurance</h3>
<p>We do not sell it. We do look at whether the coverage in place matches the obligation it exists to cover, and disability cover is the one most commonly missing entirely &mdash; for a self-employed household it is usually the largest uninsured exposure.</p>

<div class="callout"><p><strong>The biggest wins are usually structural rather than clever.</strong> Contributing enough to get the whole match. Setting estimated payments so there is no April surprise. Holding the right asset in the right account. Choosing which year to realise a gain. None of it is exotic and all of it compounds.</p></div>

<h2>Working alongside your other advisers</h2>
<p>Where you have an investment adviser or an attorney, this work sits beside theirs rather than replacing it. Our contribution is the tax and cash flow view and a second opinion that is not attached to a product. Where an <a href="estate-planning.html">estate plan</a> or an <a href="elder-care.html">elder care</a> question is in the picture, the same office handles that too.</p>
''',
   faqs=[("Do you manage investments or sell financial products?",
          "<p>No. This work is analysis and advice on the tax and cash flow side. Not selling anything is part of what makes a second opinion useful.</p>"),
         ("Should I contribute to a Roth or a pre-tax account?",
          "<p>It depends on your marginal rate now against your expected rate in retirement. For many households the answer changes over a career, and splitting between the two is a reasonable hedge.</p>"),
         ("When should I claim Social Security?",
          "<p>It depends on health, other income, whether you are still working, and survivor considerations for a married couple. Delaying increases the benefit, which makes it valuable insurance against living a long time.</p>"),
         ("Is a 529 plan worth it in Massachusetts?",
          "<p>Growth is tax-free when used for qualifying education costs, and Massachusetts offers a deduction for contributions to its own plan within limits. Whether it beats other saving depends on the timeframe and your bracket.</p>")],
   related=[('estate-planning', 'Estate planning'), ('elder-care', 'Elder care'),
            ('tax-planning', 'Tax planning'),
            ('../calculators/retirement-savings.html', 'Retirement calculator')]),

 dict(slug='estate-planning', ic='estate', nav_title='Estate Planning',
   short='The tax and accounting side of passing on what you have built, coordinated with the attorney who drafts the documents.',
   title='Estate Planning | James L. Hickey, CPA PC, Tewksbury MA',
   desc='The accounting and tax side of estate planning in Massachusetts: the state estate tax threshold, basis planning, gifting, trust and estate returns, and executor support.',
   eyebrow='Individuals', h1='Massachusetts taxes estates that the federal government ignores.',
   sub='The state threshold is far below the federal one, which puts ordinary households in a bracket they never expected to be in.',
   body='''
<h2>The short answer</h2>
<p>We handle the tax and accounting side of estate planning and estate administration, working alongside the attorney who drafts the instruments. That covers projecting the estate tax exposure, basis and gifting strategy, trust and estate income tax returns, and support for the executor or trustee once the responsibility actually arrives.</p>

<h2>The Massachusetts problem</h2>
<p>Federal estate tax reaches only very large estates. The Massachusetts estate tax applies at a far lower level, and it is calculated on the whole estate rather than only on the amount above the threshold. That catches households who never thought of themselves as wealthy: a long-owned house in the Merrimack Valley, a retirement account, a life insurance policy owned by the person insured, and a modest business interest add up faster than people expect.</p>
<p>Two details do most of the damage. Life insurance proceeds are included in the estate when the deceased owned the policy &mdash; and most people own their own policies without ever considering it. And Massachusetts does not follow federal portability, so a couple who leave everything to each other and take no other step can waste one threshold entirely.</p>

<div class="callout"><p><strong>Thresholds and rates change.</strong> Massachusetts has revised its estate tax rules, and both state and federal figures move with legislation. Any projection should be run against the current numbers rather than the ones you remember, which is a good reason to review a plan that has been sitting in a drawer.</p></div>

<h2>Basis, and the mistake it causes</h2>
<p>Assets held at death generally receive a step-up in basis to their date-of-death value, wiping out unrealised capital gain. Assets given away during life carry the giver's original basis to the recipient. That single distinction reverses a great deal of well-meaning advice.</p>
<p>The classic example is the parent who adds a child to the deed of a long-held house. It feels tidy, it avoids probate on that asset, and it hands the child the parent's original basis on the transferred share &mdash; producing a capital gains bill on sale that can dwarf whatever it saved. For an estate below the taxable threshold, holding appreciated assets until death is frequently the better answer.</p>

<h2>What the work involves</h2>
<ul>
<li><strong>An inventory and a projection.</strong> Everything counts, including retirement accounts, life insurance you own, business interests and jointly held property. Most people are surprised by the total.</li>
<li><strong>Beneficiary designations.</strong> Retirement accounts and insurance pass by designation and ignore the will entirely. Out-of-date designations are the most common defect in an otherwise careful plan, and the cheapest to correct.</li>
<li><strong>Gifting.</strong> Annual exclusion gifts reduce the estate over time. The interaction with basis, and with any future need for long-term care, has to be considered together.</li>
<li><strong>Trust coordination.</strong> The attorney drafts; we model what the structure does to income tax and estate tax, and later prepare the fiduciary returns.</li>
<li><strong>Business interests.</strong> A closely held business needs a valuation and a plan for who receives it, which runs into <a href="succession-planning.html">succession planning</a> and <a href="business-valuation.html">valuation</a>.</li>
</ul>

<h2>After a death</h2>
<p>Executors inherit a set of deadlines and a personal responsibility that most have never encountered. The work includes the final individual return, the estate income tax returns during administration, the estate tax filings where required, valuations at date of death, and the accounting the probate court and the beneficiaries expect. Where an executor is a grieving family member, having the filings handled by someone who does this routinely is worth a great deal.</p>

<h2>Related</h2>
<p>Estate questions frequently arrive alongside <a href="elder-care.html">elder care</a> concerns, and both sit inside <a href="personal-financial-planning.html">personal financial planning</a>. We coordinate with your attorney rather than duplicating them.</p>
''',
   faqs=[("Do I need an estate plan if I am not wealthy?",
          "<p>Massachusetts applies its estate tax at a level far below the federal one, and it counts the whole estate including your home, retirement accounts and life insurance you own. A projection is the only way to know where you sit.</p>"),
         ("Should I put my house in my children's names?",
          "<p>Usually not without advice. It transfers your original basis to them and can create a large capital gains bill on sale that outweighs what it saved, particularly for an estate below the taxable threshold.</p>"),
         ("Do you draft wills and trusts?",
          "<p>No. Those are legal documents drafted by an attorney. We handle the tax projections, the basis and gifting analysis, and the fiduciary returns, and we coordinate with the attorney throughout.</p>"),
         ("What does an executor actually have to file?",
          "<p>Typically a final individual return, income tax returns for the estate during administration, and estate tax filings where the thresholds are met. Values at date of death have to be established and documented.</p>")],
   related=[('elder-care', 'Elder care'), ('succession-planning', 'Succession planning'),
            ('personal-financial-planning', 'Personal financial planning'),
            ('business-valuation', 'Business valuation')]),

 dict(slug='elder-care', ic='people', nav_title='Elder Care',
   short='Financial oversight for an older client or a parent: bill paying, statement review, coordination with family and the tax work that comes with care.',
   title='Elder Care Financial Services | Tewksbury, Massachusetts CPA',
   desc='Elder care financial services from a Tewksbury CPA office: oversight of bills and accounts, statement review, family coordination and the tax side of long-term care.',
   eyebrow='Individuals', h1='Somebody has to open the mail. It should be someone accountable.',
   sub='When managing money becomes difficult, the practical need is oversight from a professional the whole family can see the work of.',
   body='''
<h2>The short answer</h2>
<p>Elder care work is financial oversight for an older client whose affairs have become difficult to manage alone, or for a family managing them at a distance. It covers bill payment and record keeping, review of bank and investment statements, coordination with family members and other advisers, and the tax and reporting work that accompanies care decisions.</p>

<h2>What it looks like in practice</h2>
<ul>
<li><strong>Bills paid and recorded,</strong> with a clear trail rather than a shoebox and a good memory.</li>
<li><strong>Statements reviewed monthly</strong> by somebody who will notice an unfamiliar withdrawal, a doubled charge, a new payee or a subscription that has quietly tripled.</li>
<li><strong>Reporting to the family,</strong> at whatever cadence the family wants, so that adult children in another state can see what is happening without cross-examining a parent.</li>
<li><strong>Tax returns prepared</strong> with the deductions that matter at this stage, including medical and long-term care costs, which are frequently large enough to matter once the threshold is crossed.</li>
<li><strong>Coordination with the attorney, the care manager and the investment adviser,</strong> so that decisions are not being made in four places at once.</li>
</ul>

<h2>Why an outside professional helps</h2>
<p>Two reasons, and the second is the one families do not say out loud. The first is competence: the work is unglamorous and it is easy to let slip. The second is that money is where family relationships strain. An adult child who takes over a parent's accounts is placed in a position where every decision can look, to a sibling, like something other than what it was. An independent professional keeping the records removes that suspicion before it forms &mdash; which protects the person doing the work as much as the person being cared for.</p>

<div class="callout"><p><strong>Financial exploitation of older adults is common, and it is most often committed by somebody known to the victim.</strong> Regular independent review of statements by a professional is one of the few practical defences, and it is a great deal cheaper than the loss.</p></div>

<h2>The tax and planning questions that arrive with care</h2>
<h3>Medical and long-term care costs</h3>
<p>Nursing home and assisted living costs can be deductible in whole or in part depending on the level of care and the certification behind it. For a household paying these amounts the deduction is often the largest item on the return and it is regularly missed.</p>

<h3>Paying for care from assets</h3>
<p>Which account to draw on first is a tax decision. Liquidating a retirement account creates income; selling appreciated property creates gain; a reverse mortgage does neither but has costs of its own. The order can change the after-tax cost materially.</p>

<h3>Gifting, and the risk in it</h3>
<p>Transferring assets to family with an eye to future benefit eligibility has real consequences: a look-back period, potential ineligibility, loss of the step-up in basis, and the loss of control at exactly the stage of life when control matters most. This is one of the areas where advice from a neighbour is the most expensive kind available. Coordinate it with an elder law attorney and with us together.</p>

<h3>Selling the family home</h3>
<p>The exclusion on a principal residence has occupancy requirements that interact awkwardly with a move into care. Timing matters, and it is worth checking before the house is listed rather than after it is sold.</p>

<h2>Getting started</h2>
<p>Usually a conversation with the family and, wherever possible, with the older person themselves. Dignity is part of the engagement: the objective is to keep somebody in control of their own affairs for as long as possible, with support behind them, rather than to take the affairs away.</p>
''',
   faqs=[("Can you pay bills on behalf of a family member?",
          "<p>Bill payment and record keeping is part of this work, arranged with the appropriate written authority in place and with reporting to the family.</p>"),
         ("Are nursing home costs deductible?",
          "<p>Often, in whole or in part, depending on the level of care and how it is certified. For families paying these amounts it is frequently the largest deduction on the return.</p>"),
         ("Should my parents give assets to the children now?",
          "<p>Rarely without coordinated advice. There is a look-back period for benefit eligibility, the basis step-up is lost, and control is given up at the point in life when it is most needed.</p>"),
         ("We live out of state. Can this still work?",
          "<p>Yes. Distance is one of the main reasons families ask for it. The office is local to the parent and the reporting goes to the family wherever they are.</p>")],
   related=[('estate-planning', 'Estate planning'), ('personal-financial-planning', 'Personal financial planning'),
            ('tax-preparation', 'Tax return preparation'), ('../contact.html', 'Contact the office')]),

 dict(slug='quickbooks', ic='calc', nav_title='QuickBooks Consulting',
   short='Setup, training and tune-ups &mdash; so the file produces numbers you can rely on rather than a year-end reconstruction project.',
   title='QuickBooks Setup, Training & Tune-Ups | Tewksbury MA CPA',
   desc='QuickBooks help from a Tewksbury CPA office: file setup, one-to-one training, tune-ups and cleanups, and answers to the questions that come up during the year.',
   eyebrow='QuickBooks', h1='The software is not the hard part. The setup is.',
   sub='Most QuickBooks problems we are called about were created in the first week of using it and compounded quietly for two years.',
   body='''
<h2>The short answer</h2>
<p>We set QuickBooks up for new businesses, train the person who is going to use it, tune up and clean up files that have drifted, and answer the questions that come up during the year. The objective is a file that produces reliable monthly numbers and a year end that takes days rather than weeks.</p>

<h2>Why QuickBooks at all</h2>
<p>Because almost everyone can work in it. A bookkeeper you hire will know it, an accountant can open the file without translation, a lender recognises the reports, and if you change advisers your records go with you. That interoperability is worth more to a small business than any individual feature, and it is why a well-kept QuickBooks file remains the practical default.</p>

<h2>Setup</h2>
<p>The decisions made when a file is created determine what it can tell you for as long as it exists:</p>
<ul>
<li><strong>A chart of accounts built for your business</strong> rather than the generic template &mdash; direct costs separated from overhead, revenue split into the lines you actually think in, and owner-discretionary spending isolated so it can be added back when a lender or a buyer asks.</li>
<li><strong>Items, classes and locations</strong> configured so that job, department or location profitability is available without a rebuild later.</li>
<li><strong>Opening balances entered correctly,</strong> tied to the last tax return or closing statements. A file that starts wrong is wrong forever.</li>
<li><strong>Bank feeds and rules,</strong> set up so that the automation categorises rather than merely accumulating.</li>
<li><strong>Sales tax, payroll and users,</strong> configured before the first transaction rather than retrofitted.</li>
</ul>

<h2>Training</h2>
<p>One-to-one, on your own file, on the transactions you actually process. Generic courses teach the software; what a small business needs is confidence with the twenty operations it performs every week &mdash; invoicing, receiving payment, entering bills, reconciling, handling a customer deposit, correcting a mistake without making a worse one. We would rather train the person doing the work than do the work permanently.</p>

<h2>Tune-ups and cleanups</h2>
<p>Files drift. The symptoms are consistent:</p>
<ul>
<li>Bank and credit card accounts that have not reconciled in months, or that reconcile only because a plug entry was made</li>
<li>Undeposited funds carrying a balance that has been growing for a year</li>
<li>Accounts receivable and payable full of items that were paid, cancelled or duplicated long ago</li>
<li>An opening balance equity account with a balance in it, which is always a sign of something unresolved</li>
<li>A chart of accounts that has grown to several hundred lines because a new one was created every time somebody was unsure</li>
<li>Loan balances that no longer match the amortisation schedule, because payments were posted entirely to expense</li>
<li>Personal expenses mixed into the business, uncategorised</li>
<li>Prior periods still open, so last year's figures change every time somebody touches something</li>
</ul>
<p>A cleanup fixes those, ties the file to the last filed return, and closes the periods behind you so the history stays fixed.</p>

<div class="callout"><p><strong>Reconcile every account, every month.</strong> If nothing else survives from this page, that one habit prevents most of the problems above. An unreconciled file is not evidence of anything, and a lender, a buyer or an examiner will treat it accordingly.</p></div>

<h2>The questions we get asked most</h2>
<p>Whether to use classes or separate income accounts. What to do with an owner draw. How to record a loan payment so that principal reduces the liability and only the interest hits expense. How to handle a customer deposit taken before the work is done. Whether the file should be converted to the online version. Whether to invoice through QuickBooks or through the industry system you already use. None of these takes long &mdash; they simply need answering by somebody who will also be looking at the tax return.</p>

<h2>Getting ready for year end</h2>
<p>Most of the cost of a year end is created by the state of the file when it arrives. Our <a href="../guides/quickbooks-year-end-checklist.html">year-end checklist</a> sets out what to reconcile, tie out and review before sending it over.</p>
''',
   faqs=[("Desktop or online?",
          "<p>Online for most small businesses now, because of remote access, bank feeds and the ability for your accountant to work in the same file. Some inventory-heavy and job-costing workflows are still better served by desktop.</p>"),
         ("Can you train our bookkeeper rather than doing the work?",
          "<p>Yes, and it is usually the better arrangement. Training on your own file, on your own transactions, is far more effective than a general course.</p>"),
         ("Our file is a mess. Is it worth fixing or should we start again?",
          "<p>Usually fixing is cheaper, because the history has value and a new file has to be tied to something anyway. A fresh start makes sense where the opening balances were never right at all.</p>"),
         ("How often should we reconcile?",
          "<p>Every account, every month, without exception. It is the single habit that prevents most of the problems we are called in to fix.</p>")],
   related=[('small-business-services', 'Small business services'), ('entity-formation', 'New business formation'),
            ('bank-financing', 'Bank financing'),
            ('../guides/quickbooks-year-end-checklist.html', 'Year-end checklist')]),
]


# =========================================================================
# GUIDES
# =========================================================================
GUIDES = [

 dict(slug='irs-notice-what-to-do', nav_title='An IRS notice arrived',
   title='An IRS Notice Arrived. What To Do First | Hickey CPA, Tewksbury',
   desc='A plain order of operations for an IRS letter: what to check first, which deadlines are real, why you should never pay before reading the file, and when to get help.',
   eyebrow='Guide', h1='An IRS notice arrived. Here is the order to do things in.',
   sub='Most notices are routine, a surprising number are wrong, and almost all of them get worse if they are ignored.',
   body='''
<div class="callout"><p><strong>Short version:</strong> do not throw away the envelope, find the notice number and the deadline, check the figures against your own return before agreeing to anything, never pay a balance you have not verified, and never give payment details to somebody who telephoned you claiming to be the IRS. If money or a deadline is involved, get the letter in front of a professional before you reply.</p></div>

<h2>1. Establish that it is genuine</h2>
<p>The Internal Revenue Service initiates contact by post. It does not open a matter with a telephone call, a text message or an email, it does not demand payment by gift card or wire transfer, it does not threaten immediate arrest, and it does not refuse to let you verify a balance before paying it. Every one of those is a hallmark of the impersonation scams that run continuously, and they run hardest at the two points in the year when people are already anxious about tax.</p>
<p>A genuine notice carries a notice or letter number, printed in the top right of the first page. That number tells you exactly what the letter is, and it is the first thing to find.</p>

<h2>2. Read the deadline before you read the argument</h2>
<p>Different notices carry different response windows, and some of them attach rights that expire. A statutory notice of deficiency, for example, opens a fixed period in which the assessment can be challenged in the Tax Court &mdash; and that window does not reopen. A notice of intent to levy similarly starts a clock on the right to request a collection due process hearing.</p>
<p>Write the deadline on the front of the letter, keep the envelope with its postmark, and treat the date as the fact that governs everything else.</p>

<h2>3. Work out which kind of letter you are holding</h2>
<table class="plain"><thead><tr><th>What it is doing</th><th>What it usually means</th><th>Urgency</th></tr></thead><tbody>
<tr><td>Adjusting a figure on your return</td><td>An automated match found a difference between your return and what a third party reported</td><td>Respond by the date; frequently disputable</td></tr>
<tr><td>Asking for a missing form or signature</td><td>Processing has stalled</td><td>Straightforward, but it stops any refund until answered</td></tr>
<tr><td>Proposing additional tax</td><td>A proposal, not yet an assessment &mdash; agreeing by silence is a choice</td><td>High; the window is what protects you</td></tr>
<tr><td>Stating a balance due</td><td>Tax already assessed; interest and penalties accruing</td><td>High</td></tr>
<tr><td>Intent to levy, or a lien filing</td><td>The collection process has escalated</td><td>Immediate &mdash; procedural rights attach and expire</td></tr>
<tr><td>Requesting an examination of records</td><td>An audit, usually of specific items rather than the whole return</td><td>High; representation is worth having from the start</td></tr>
</tbody></table>

<h2>4. Check it against your own return before agreeing</h2>
<p>Automated notices are generated by matching. Matching produces false positives routinely, and the most common causes are mundane: a brokerage sale reported at gross proceeds with no basis, so the whole sale looks like profit; a form issued under the wrong identification number; income reported twice because a corrected form was filed; a return filed on time but posted to the wrong year; an estimated payment applied to the wrong period; a joint return where income was attributed to one spouse only.</p>
<p>Take the notice, take your copy of the return, and compare line by line. If the letter is right, that is worth knowing quickly. If it is wrong, saying so with documentation is straightforward &mdash; but only within the window.</p>

<h2>5. Do not pay a balance you have not verified</h2>
<p>Paying is an agreement. Once a proposed adjustment is paid it is considerably harder to argue with, and the amount shown on a notice is frequently based on incomplete information &mdash; particularly where the Service has prepared a return on your behalf, which allows no deductions of any kind.</p>
<p>If the balance is genuinely owed and cannot be paid at once, there are defined routes: a short extension to pay, an installment agreement, hardship status, or in the right circumstances a settlement. See <a href="../services/irs-payment-plans.html">IRS payment plans</a>.</p>

<h2>6. Answer, in writing, and keep everything</h2>
<p>Respond in writing wherever a written response is possible. Reference the notice number and the tax year on every page. Include copies rather than originals. Send it in a way that produces proof of delivery, and keep the proof. Keep a copy of everything you send, and note the date, name and identification number of anyone you speak to.</p>
<p>Expect the process to be slow, and expect follow-up notices to keep arriving while your response is being processed. A second letter is not a rejection of your first.</p>

<h2>7. Know when to bring somebody in</h2>
<p>A missing signature or a small arithmetic correction is a letter you can answer yourself. Get help where any of the following apply:</p>
<ul>
<li>The amount is significant to you</li>
<li>The letter proposes an examination of records or an interview</li>
<li>The matter involves business income, self-employment, rental property or investment basis</li>
<li>Returns are missing for one or more years</li>
<li>A lien, a levy or a garnishment has been mentioned</li>
<li>The balance relates to payroll taxes</li>
<li>The liability arises from a joint return with a spouse or former spouse &mdash; see <a href="../services/innocent-injured-spouse.html">innocent and injured spouse relief</a></li>
<li>You do not understand what the letter is asking for</li>
</ul>
<p>Attorneys, certified public accountants and enrolled agents may represent a taxpayer before the Service without limitation. With a signed authorisation the correspondence and the telephone calls go to your representative instead of to you, which is worth something on its own.</p>

<h2>8. The Massachusetts letter that follows</h2>
<p>A federal adjustment usually produces a state one some months later, because the states receive federal changes. If you settle a federal matter, expect the Commonwealth in due course &mdash; and factor it into the arrangement rather than being surprised by it.</p>

<h2>What not to do</h2>
<ul>
<li>Do not ignore it. Proposals become assessments, and assessments become liens and levies.</li>
<li>Do not throw the envelope away. Postmarks matter.</li>
<li>Do not telephone the number on a suspicious message. Use a number you looked up yourself.</li>
<li>Do not send original documents.</li>
<li>Do not sign an agreement you have not read and understood, and be particularly careful about anything that extends the time the Service has to assess.</li>
<li>Do not assume the figure is correct because it is printed.</li>
</ul>
''',
   faqs=[("Does the IRS ever call or email first?",
          "<p>No. Contact is initiated by post. Unsolicited calls, texts and emails demanding payment are impersonation attempts, and the demand for gift cards or a wire transfer is a certainty of fraud.</p>"),
         ("How long do I have to respond?",
          "<p>It depends on the notice, and some carry rights that expire permanently. Find the date on the letter first and work backwards from it.</p>"),
         ("The notice says I owe money I do not think I owe.",
          "<p>Compare it against your return before doing anything. Missing basis on a securities sale, duplicated income and misapplied payments are common causes, and all are correctable within the response window.</p>"),
         ("Should I just pay it to make it go away?",
          "<p>Not before verifying it. Paying is a form of agreement, and the balance shown is often based on incomplete information.</p>"),
         ("Can somebody deal with the IRS for me?",
          "<p>Yes. With a signed authorisation a CPA can act for you throughout, and the correspondence goes to the representative rather than to you.</p>")]),

 dict(slug='quickbooks-year-end-checklist', nav_title='QuickBooks year-end checklist',
   title='QuickBooks Year-End Checklist | Hickey CPA, Tewksbury MA',
   desc='What to reconcile, tie out and review in QuickBooks before sending the file to your accountant, and why doing it yourself lowers what the year end costs.',
   eyebrow='Guide', h1='Closing your QuickBooks year before it reaches your accountant.',
   sub='Most of what a year end costs is decided by the condition of the file when it arrives. This is the list.',
   body='''
<div class="callout"><p><strong>Short version:</strong> reconcile every bank and card account through the last day of the year, clear undeposited funds, tie loans to their statements, age and clean receivables and payables, review the profit and loss line by line for anything that looks odd, confirm payroll and contractor records, and then close the period so the numbers stop moving.</p></div>

<h2>Why this is worth an afternoon</h2>
<p>Professional time spent finding out why an account does not reconcile is the most expensive work in the engagement and the least valuable. Every item on this list either removes that work or turns it into a question you can answer in one sentence. The file that arrives reconciled and explained costs less to work with, and it produces a set of numbers you can rely on during the following year rather than only at its end.</p>

<h2>1. Reconcile everything, through 31 December</h2>
<p>Every bank account, every credit card, every line of credit, through the final statement of the year. Reconciled means the statement balance and the book balance agree with a documented list of outstanding items &mdash; not that a difference was forced into an adjustment.</p>
<p>Then look at the uncleared items. Cheques written eight months ago that have never cleared are usually void, duplicated, or evidence of something that needs investigating.</p>

<h2>2. Clear undeposited funds</h2>
<p>A growing balance in undeposited funds nearly always means payments were recorded as received but the deposit was never matched to the bank. The result is overstated income, overstated cash, or both. It should be at or near zero at year end.</p>

<h2>3. Tie the loans out</h2>
<p>Take the December statement for every loan and every finance agreement and compare the balance with the liability account. They diverge when payments have been posted entirely to expense instead of being split between principal and interest. Fixing it at year end is routine; discovering it three years later is not.</p>

<h2>4. Age and clean the receivables</h2>
<p>Run the open invoice report. Genuinely uncollectable invoices should be written off with a decision behind it, not left inflating the balance. Invoices that were paid but never matched should be applied. Credits sitting unapplied should be applied. Anything more than a year old needs an explanation.</p>

<h2>5. Do the same for payables</h2>
<p>Old open bills are usually duplicates, or bills that were paid by card or bank transfer and never matched. Both overstate liabilities and distort the picture a lender sees.</p>

<h2>6. Check the balance sheet accounts nobody looks at</h2>
<ul>
<li><strong>Opening balance equity.</strong> Should be zero. A balance means something was never resolved from setup or from a conversion.</li>
<li><strong>Uncategorised income and uncategorised expense.</strong> Should be empty.</li>
<li><strong>Ask my accountant,</strong> or whatever the equivalent holding account is called in your file. Empty it &mdash; that is what this exercise is for.</li>
<li><strong>Inventory,</strong> where you carry it: does the book figure agree with a physical count taken at year end?</li>
<li><strong>Fixed assets.</strong> Anything purchased during the year that should be capitalised rather than expensed, and anything disposed of that is still on the books.</li>
<li><strong>Owner draws and contributions.</strong> Recorded as equity movements, not as expenses.</li>
<li><strong>Payroll liabilities.</strong> Should agree with what is actually owed at year end.</li>
</ul>

<h2>7. Read the profit and loss line by line</h2>
<p>Compare this year against last year, account by account. Every large movement should have an explanation you can give in a sentence. This exercise finds miscodings faster than any reconciliation, and it is also the first time most owners genuinely look at their own numbers.</p>
<p>Look particularly for personal expenses that have found their way in, categories that were invented mid-year and duplicate an existing one, and anything sitting in miscellaneous.</p>

<h2>8. Payroll and contractors</h2>
<p>Confirm that wage totals agree with the payroll returns filed during the year, that any owner health insurance or personal use of a company vehicle has been treated correctly, and that every contractor paid over the reporting threshold has a current taxpayer identification number on file. Chasing an identification number in January, from somebody who no longer works for you, is a bad use of everybody's time. Collect it before the first payment instead.</p>

<h2>9. Sales tax</h2>
<p>Compare what the file says was collected with what was actually remitted. A difference is either a filing to correct or a coding problem, and both are cheaper to find now.</p>

<h2>10. Close the period, and back it up</h2>
<p>Set a closing date with a password once the year is agreed. Without it, a well-meaning correction posted in March silently changes figures on a return that has already been filed. Take a backup, or confirm the archive if you are on the online version.</p>

<h2>What to send over</h2>
<p>The file access or the backup, the December bank and credit card statements, loan statements, the payroll returns for the year, the inventory count if you carry stock, and a short note listing anything unusual that happened during the year &mdash; an asset bought or sold, a loan taken out, a new state, a change in ownership, an insurance settlement. That note saves more time than any single reconciliation.</p>

<h2>If the file is beyond an afternoon</h2>
<p>Some files need a cleanup rather than a checklist, and that is a normal thing rather than an embarrassing one. See <a href="../services/quickbooks.html">QuickBooks consulting</a>, or call the office and describe what you are looking at.</p>
''',
   faqs=[("How long before year end should we start?",
          "<p>Reconciling monthly means there is nothing to start. Where that has not happened, allow a few weeks &mdash; missing statements and unanswered questions are what take the time.</p>"),
         ("Should we set a closing date password?",
          "<p>Yes. Without one, entries posted into a closed year change figures on returns that have already been filed, and nobody notices until the following year fails to tie.</p>"),
         ("Our bank feed categorises everything automatically. Is that enough?",
          "<p>No. Rules apply the last category used, which is right until it is not. Bank feeds reduce typing; they do not replace review or reconciliation.</p>"),
         ("What if we cannot get an account to reconcile?",
          "<p>Stop and note where it went wrong rather than forcing an adjustment. A documented difference is a question we can answer quickly; a plug entry hides the problem and carries it forward.</p>")]),
]


# =========================================================================
# PAGE BUILDERS
# =========================================================================
def _svc_page(s):
    d = 1
    url = BASE + 'services/' + s['slug'] + '.html'
    rel_links = ''
    for href, label in s['related']:
        h = href if href.startswith('..') or href.endswith('.html') else href + '.html'
        rel_links += '<li><a href="' + h + '"><span class="ck">&rarr;</span> ' + label + '</a></li>'
    p = dict(path='services/' + s['slug'] + '.html', depth=d, nav='services',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'], sub=s['sub'])
    p['body'] = phero(p, [('Services', 'services/index.html'), (_plain(s['nav_title']), None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">' + s['body'] +
      '<h2>Common questions</h2>' + faq_html(s['faqs']) +
      '</div>'
      '<div class="aside">'
      '<div class="acard"><div class="t">Talk it through</div>'
      '<p>Describe the situation on the phone and we will tell you what the work involves.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a>'
      '</div>'
      '<div class="acard light"><div class="t">Related</div><ul>' + rel_links + '</ul></div>'
      + _why_aside(d) +
      '</div></div></div></section>')
    p['schema'] = [_org(),
      breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/'), (_plain(s['nav_title']), url)]),
      _svc_schema(_plain(s['nav_title']), _plain(s['short']), url),
      faq_schema([(q, _plain(a)) for q, a in s['faqs']])]
    return p


def _guide_page(g):
    url = BASE + 'guides/' + g['slug'] + '.html'
    others = ''.join('<li><a href="' + o['slug'] + '.html"><span class="ck">&rarr;</span> ' + o['nav_title'] + '</a></li>'
                     for o in GUIDES if o['slug'] != g['slug'])
    p = dict(path='guides/' + g['slug'] + '.html', depth=1, nav='about',
             title=g['title'], desc=g['desc'], eyebrow=g['eyebrow'], h1=g['h1'], sub=g['sub'])
    p['body'] = phero(p, [('Guides', 'guides/' + g['slug'] + '.html'), (g['nav_title'], None)]) + (
      '<section class="sec"><div class="wrap"><div class="split">'
      '<div class="prose reveal">' + g['body'] +
      '<h2>Common questions</h2>' + faq_html(g['faqs']) +
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Ask instead of reading</div>'
      '<p>Ten minutes on the telephone settles more than any guide can.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">More</div><ul>' + others +
      '<li><a href="../services/irs-representation.html"><span class="ck">&rarr;</span> IRS problem resolution</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li></ul></div>'
      + _why_aside(1) +
      '</div></div></div></section>')
    p['schema'] = [_org(),
      breadcrumb_schema([('Home', BASE), ('Guides', BASE + 'guides/' + g['slug'] + '.html'), (g['nav_title'], url)]),
      article_schema(_plain(g['h1']), g['desc'], url),
      faq_schema([(q, _plain(a)) for q, a in g['faqs']])]
    return p


# ---------------------------------------------------------------- calculators
CALC_TITLES = {
 'mortgage-payment': 'Mortgage Payment Calculator',
 'refinance-breakeven': 'Refinance Break-Even Calculator',
 'loan-payment': 'Loan Payment &amp; Payoff Calculator',
 'retirement-savings': 'Retirement Savings Calculator',
 'self-employment-tax': 'Self-Employment Tax Calculator',
 'section-179': 'Section 179 Equipment Calculator',
 'break-even': 'Business Break-Even Calculator',
 'college-savings': 'College Savings Calculator',
}


def _calc_pages():
    P = []
    # ---- hub
    groups = ''
    for cat in C.CATEGORIES:
        cards = ''
        for c in C.CALCULATORS:
            if c['cat'] != cat:
                continue
            cards += ('<a class="calccard reveal" href="' + c['slug'] + '.html">'
                      '<div class="cc">' + cat + '</div><h3>' + c['title'] + '</h3>'
                      '<p>' + c['blurb'] + '</p></a>')
        groups += ('<div class="sec-head reveal" style="margin:44px 0 0"><h2>' + cat + '</h2></div>'
                   '<div class="calcgrid">' + cards + '</div>')
    p = dict(path='calculators/index.html', depth=1, nav='calculators',
      title='Financial Calculators | James L. Hickey, CPA PC, Tewksbury MA',
      desc='Eight financial calculators covering mortgages, loans, retirement, self-employment tax, equipment purchases, break-even and college saving. Nothing leaves your browser.',
      eyebrow='Calculators', h1='Eight calculators that run on this page.',
      sub='No third-party widget, no sign-up, no figures sent anywhere. Type into the boxes and the answers move as you type.')
    p['body'] = phero(p, [('Calculators', None)]) + (
      '<style>' + C.CALC_CSS + '</style>'
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>Rough answers, quickly</h2>'
      '<p class="lead">These are here to get you to an order of magnitude before a conversation, not to replace one. '
      'Every one of them runs entirely in your browser: nothing you type is transmitted, stored or seen by anyone. '
      'When the number matters &mdash; a purchase, a filing, a retirement decision &mdash; '
      '<a href="../contact.html">call the office</a> and we will work it properly.</p></div>'
      + groups +
      '</div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>What these will not do</h2>'
      '<p>They do not know your filing status, your state, your basis, your carryforwards or the rest of your return, '
      'and several of them rely on figures that the IRS resets annually. Treat the output as an estimate to think with.</p>'
      '<p>Where a calculator points at a decision worth getting right &mdash; whether to refinance, whether an equipment '
      'purchase makes sense this year, what to set aside for self-employment tax &mdash; the underlying work is '
      '<a href="../services/tax-planning.html">tax planning</a>, and it is a conversation rather than a form.</p>'
      '</div><div class="aside"><div class="acard"><div class="t">Run it properly</div>'
      '<p>Bring the figures to the office and we will run them against your actual return.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      + _why_aside(1) + '</div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/')]),
      {"@context": "https://schema.org", "@type": "ItemList", "name": "Financial calculators",
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c['title'],
                            "url": BASE + 'calculators/' + c['slug'] + '.html'}
                           for i, c in enumerate(C.CALCULATORS)]}]
    P.append(p)

    # ---- one page per calculator
    for c in C.CALCULATORS:
        url = BASE + 'calculators/' + c['slug'] + '.html'
        others = ''.join('<li><a href="' + o['slug'] + '.html"><span class="ck">&rarr;</span> ' + o['title'] + '</a></li>'
                         for o in C.CALCULATORS if o['slug'] != c['slug'])
        p = dict(path='calculators/' + c['slug'] + '.html', depth=1, nav='calculators',
                 title=_plain(CALC_TITLES[c['slug']]) + ' | James L. Hickey, CPA',
                 desc='Free calculator from a Tewksbury, MA CPA office: ' + c['blurb'],
                 eyebrow='Calculators', h1=c['title'], sub=c['blurb'])
        hero = phero(p, [('Calculators', 'calculators/index.html'), (c['title'], None)])
        p['body'] = ('<style>' + C.CALC_CSS + '</style>'
                     + C.calc_page_body(c, hero, rel, ARROW, depth=1)
                     + '<section class="sec tint"><div class="wrap"><div class="split">'
                       '<div class="prose reveal"><h2>Before you rely on it</h2>'
                       '<p>This runs entirely in your browser and nothing you type is transmitted or stored. '
                       'It also knows nothing about the rest of your situation &mdash; your filing status, your '
                       'state, your basis or your carryforwards &mdash; and some of the figures behind it are '
                       'reset each year. Use it to get to an order of magnitude, then '
                       '<a href="../contact.html">call the office</a> before acting on it.</p>'
                       '<p><a class="btn b-ln" href="index.html">All eight calculators ' + ARROW + '</a></p></div>'
                       '<div class="aside"><div class="acard"><div class="t">Run the real numbers</div>'
                       '<p>Bring your figures in and we will work them against your actual return.</p>'
                       '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
                       '<div class="acard light"><div class="t">Other calculators</div><ul>' + others + '</ul></div>'
                       '</div></div></div></section>'
                     + C.CALC_JS)
        p['schema'] = [_org(),
          breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/'), (c['title'], url)]),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": c['title'],
           "description": c['blurb'], "url": url, "applicationCategory": "FinanceApplication",
           "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "publisher": {"@id": ORG_ID}}]
        P.append(p)
    return P


# ---------------------------------------------------------------- services hub
def _services_hub():
    cards = ''
    for i, s in enumerate(SERVICES):
        cards += ('<a class="card reveal" href="' + s['slug'] + '.html"><span class="num">'
                  + ('0' + str(i + 1))[-2:] + '</span>'
                  '<div class="cic">' + icon(s['ic']) + '</div><h3>' + s['nav_title'] + '</h3>'
                  '<p>' + s['short'] + '</p><span class="more">Read more ' + ARROW + '</span></a>')
    p = dict(path='services/index.html', depth=1, nav='services',
      title='Services | James L. Hickey, CPA PC, Tewksbury Massachusetts',
      desc='Tax preparation and planning, IRS problem resolution, small business accounting, QuickBooks consulting, valuation, succession, estate and elder care services.',
      eyebrow='Services', h1='A full service practice, in one office on Main Street.',
      sub='Tax, IRS problems, small business accounting, QuickBooks, valuation, succession, estate and elder care &mdash; handled by the same people who see your return.')
    p['body'] = phero(p, [('Services', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>What this office does</h2>'
      '<p class="lead">A full service tax, accounting and business consulting firm serving individuals, '
      'small businesses and non-profit organizations across the Merrimack Valley. Sixteen practice areas, '
      'and most clients need more than one of them.</p></div>'
      '<div class="cards">' + cards + '</div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>Why the range matters more than it looks</h2>'
      '<p>A small business rarely has an isolated problem. The owner thinking about selling needs a valuation, a '
      'transaction structure, a tax projection and an estate plan that accounts for the proceeds. The household '
      'facing a parent&rsquo;s care needs the deduction analysis, the account sequencing and somebody keeping the '
      'records. The company that fell behind on filings needs the returns prepared, the transcripts pulled and a '
      'payment arrangement negotiated &mdash; in that order.</p>'
      '<p>Firms that do one of those hand you to somebody else for the rest. Here it is one office and one set of '
      'files, which is the practical argument for a practice this size.</p>'
      '<h3>Where to start</h3>'
      '<ul>'
      '<li><strong>A letter from the IRS.</strong> Read the deadline, keep the envelope, and see '
      '<a href="irs-representation.html">IRS problem resolution</a> or the '
      '<a href="../guides/irs-notice-what-to-do.html">guide to what a notice means</a>.</li>'
      '<li><strong>Starting a business.</strong> The entity decision is cheap now and expensive later &mdash; '
      '<a href="entity-formation.html">new business formation</a>.</li>'
      '<li><strong>Books that nobody trusts.</strong> <a href="quickbooks.html">QuickBooks consulting</a>, then '
      '<a href="small-business-services.html">monthly reporting</a>.</li>'
      '<li><strong>An owner thinking about the next ten years.</strong> '
      '<a href="business-valuation.html">Valuation</a> and <a href="succession-planning.html">succession</a>.</li>'
      '<li><strong>An ageing parent.</strong> <a href="elder-care.html">Elder care</a> and '
      '<a href="estate-planning.html">estate planning</a>.</li>'
      '</ul>'
      '</div><div class="aside"><div class="acard"><div class="t">Not sure where you fit?</div>'
      '<p>Most first calls take ten minutes and end with a clear answer about what the work involves.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Also here</div><ul>'
      '<li><a href="../calculators/index.html"><span class="ck">&rarr;</span> Eight financial calculators</a></li>'
      '<li><a href="../client-portal.html"><span class="ck">&rarr;</span> Secure client portal</a></li>'
      '<li><a href="../pay.html"><span class="ck">&rarr;</span> Paying your invoice</a></li>'
      '<li><a href="../faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/')]),
      {"@context": "https://schema.org", "@type": "ItemList", "name": "Services",
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": _plain(s['nav_title']),
                            "url": BASE + 'services/' + s['slug'] + '.html'}
                           for i, s in enumerate(SERVICES)]}]
    return p


# ---------------------------------------------------------------- home
HOME_FAQS = [
 ("What does this office actually do?",
  "<p>Tax return preparation and planning for individuals and businesses, a working IRS problem-resolution practice, small business accounting and QuickBooks consulting, business valuation and succession work, and the personal side &mdash; financial planning, estate planning and elder care. The firm describes itself as a full service tax, accounting and business consulting firm, and the <a href=\"services/index.html\">services section</a> sets out each area.</p>"),
 ("I have a letter from the IRS. Can you help?",
  "<p>Yes. A CPA may represent a taxpayer before the Service without limitation, which covers examinations, collection, liens and levies, unfiled returns and payment arrangements. Bring the letter in with the envelope before you respond to it &mdash; some notices carry rights that expire. See <a href=\"services/irs-representation.html\">IRS problem resolution</a>.</p>"),
 ("Are you taking new clients?",
  "<p>The most useful first step is a short call describing the situation: what kind of return or entity, roughly what the year looks like, and what deadline you are working against. If this is not the right office for the work, we will say so.</p>"),
 ("Can you handle both my business and my personal return?",
  "<p>Yes, and for a closely held business that is the point. Owner compensation, distributions, basis and the qualified business income deduction are one calculation split across two returns, and they only reconcile when the same office sees both.</p>"),
 ("How do I send documents securely?",
  "<p>Through the <a href=\"client-portal.html\">secure client portal</a>, or by dropping them at the office. Ordinary email is not a suitable way to send a Social Security number or a full set of tax documents.</p>"),
 ("Where are you, and is there parking?",
  "<p>170 Main Street, Suite 110, in Tewksbury. The <a href=\"contact.html\">contact page</a> has an interactive map and directions.</p>"),
]


def _home():
    svc_cards = ''.join([
      _card(0, 'services/tax-preparation.html', 'ledger', 'Tax Return Preparation',
            'Federal and Massachusetts returns for individuals, families, businesses and fiduciaries, prepared and signed here.', '01'),
      _card(0, 'services/irs-representation.html', 'shield', 'IRS Problem Resolution',
            'Representation before the Service: examinations, collection, liens and levies, unfiled returns and payment arrangements.', '02'),
      _card(0, 'services/tax-planning.html', 'plan', 'Tax Planning',
            'The work that changes the number, done during the year rather than recorded after it.', '03'),
      _card(0, 'services/small-business-services.html', 'chart', 'Small Business Services',
            'Financial statements, bookkeeping oversight, cash management, payroll and sales tax, and controls a small office can run.', '04'),
      _card(0, 'services/quickbooks.html', 'calc', 'QuickBooks Consulting',
            'Setup, one-to-one training and tune-ups, so the file produces numbers you can rely on all year.', '05'),
      _card(0, 'services/business-valuation.html', 'scale', 'Business Valuation',
            'What a closely held business is worth &mdash; for a sale, a buy-sell agreement, an estate filing or a dispute.', '06'),
    ])
    body = (
      '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" aria-hidden="true">' + GLYPH + '</svg>'
      '<div class="wrap"><div class="reveal in">'
      '<span class="eyebrow on-dark">Tax, accounting &amp; business consulting &middot; Tewksbury, Massachusetts</span>'
      '<h1>Straight tax and accounting work, and a practice built for IRS problems.</h1>'
      '<p class="sub">James L. Hickey, CPA PC is a full service tax, accounting and business consulting firm at '
      '170 Main Street in Tewksbury, working with individuals, small businesses and non-profit organizations '
      'across the Merrimack Valley.</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a>'
      '<a class="btn b-gh" href="services/index.html">See what we do ' + ARROW + '</a></div>'
      '<div class="hero-trust"><span><b>Tewksbury</b>, Massachusetts</span>'
      '<span><b>IRS</b> representation and resolution</span>'
      '<span><b>QuickBooks</b> setup and training</span>'
      '<span><b>Secure</b> client portal</span></div>'
      '</div></div></section>'

      '<section class="strip"><div class="wrap reveal">'
      '<div class="cell"><div class="n">IRS</div><div class="l">representation, back returns and payment plans</div></div>'
      '<div class="cell"><div class="n">QuickBooks</div><div class="l">setup, training and tune-ups</div></div>'
      '<div class="cell"><div class="n">Portal</div><div class="l">secure document exchange with the office</div></div>'
      '<div class="cell"><div class="n">Tewksbury</div><div class="l">one office, 170 Main Street</div></div>'
      '</div></section>'

      '<section class="sec" id="services"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">What we do</span><h2>One office, and a wider range than its size suggests.</h2>'
      '<p class="lead">Tax preparation and planning, a full IRS problem-resolution practice, small business '
      'accounting and QuickBooks work, business valuation and succession planning, and the personal side &mdash; '
      'financial planning, estate planning and elder care.</p>'
      '</div><div class="cards">' + svc_cards + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">All sixteen services ' + ARROW + '</a></p>'
      '</div></section>'

      '<section class="sec tint"><div class="wrap"><div class="split">'
      '<div class="reveal"><span class="eyebrow">Why clients call</span>'
      '<h2>Small enough that the person who prepares the return is the person who answers the phone.</h2>'
      '<p class="lead">The firm describes itself as one of the leading firms in the Tewksbury and Merrimack Valley '
      'areas. What that means day to day is a single office where the tax work, the bookkeeping questions and the '
      'IRS correspondence all land on the same desk.</p>'
      '<div class="prose" style="margin-top:26px">'
      '<h3>The entity return and the owner return are one problem</h3>'
      '<p>Owner compensation, distributions, shareholder basis and the qualified business income deduction are '
      'decided on one return and land on the other. Where two different offices prepare them, the reconciliation '
      'nobody performed is the item that surfaces later.</p>'
      '<h3>IRS matters are handled here, not referred out</h3>'
      '<p>Attorneys, certified public accountants and enrolled agents may represent a taxpayer before the Internal '
      'Revenue Service without limitation. A great many people discover at the worst possible moment that whoever '
      'prepared the return cannot come with them to defend it. Examinations, collection, liens and levies, unfiled '
      'returns and payment arrangements are all <a href="services/irs-representation.html">work this office does</a>.</p>'
      '<h3>Documents move securely</h3>'
      '<p>A secure portal is available for exchanging returns and source documents with the office, so that a full '
      'set of tax records is not sitting in an email thread. <a href="client-portal.html">How it works</a>.</p>'
      '<h3>The books and the return are the same conversation</h3>'
      '<p>Most of what a year end costs is decided by the state of the file when it arrives. Getting QuickBooks set '
      'up properly and keeping it reconciled is not a separate service from tax work &mdash; it is the reason the '
      'tax work is affordable. <a href="services/quickbooks.html">QuickBooks consulting</a>.</p>'
      '</div></div>'
      '<div class="aside"><div class="acard"><div class="t">Talk to a CPA</div>'
      '<p>Describe the situation in five minutes. If this is the right office for it, we will tell you what the '
      'engagement involves. If it is not, we will tell you that too.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      + _why_aside(0) + '</div></div></div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">IRS problems</span><h2>Unopened letters do not become smaller.</h2>'
      '<p class="lead">Proposals become assessments, assessments become liens and levies, and every stage has a way '
      'out that is easier before it is reached than afterwards. All of the following is work this office handles.</p>'
      '</div><div class="cards">'
      + _card(0, 'services/irs-representation.html', 'shield', 'Representation',
              'A signed authorisation puts us between you and the Service. Examinations, collection, appeals, and the transcripts that show what they actually have.')
      + _card(0, 'services/non-filed-returns.html', 'doc', 'Non-Filed Returns',
              'Years that were never filed, and the substitute returns the Service prepares with no deductions at all. Nothing else resolves until these do.')
      + _card(0, 'services/irs-payment-plans.html', 'clock', 'Payment Arrangements',
              'Installment agreements, hardship status and settlements &mdash; and an honest answer about which of them your numbers actually support.')
      + '</div>'
      '<p style="margin-top:32px"><a class="btn b-ln" href="guides/irs-notice-what-to-do.html">'
      'A notice arrived &mdash; what to do first ' + ARROW + '</a></p></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">On this site</span><h2>Eight calculators, and nothing you type leaves the page.</h2>'
      '<p class="lead">Mortgage and refinance, loan payoff, retirement projections, self-employment tax, equipment '
      'purchases under Section 179, business break-even and college saving. They run in your browser: no sign-up, '
      'no third-party widget, no figures transmitted anywhere.</p></div>'
      '<p><a class="btn b-ln" href="calculators/index.html">Open the calculators ' + ARROW + '</a></p>'
      '</div></section>'

      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Where we are</span><h2>170 Main Street, Suite 110, Tewksbury.</h2>'
      '<p class="lead">One office in the Merrimack Valley, convenient to Wilmington, Billerica, Andover, North '
      'Reading, Dracut and Lowell.</p></div>'
      '<div class="split">'
      '<div>' + gmap('170 Main Street, Suite 110 &middot; Tewksbury, Massachusetts 01876.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + FIRM['ph'] + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Getting here</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Open in Google Maps</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the office</a></li>'
      '<li><a href="client-portal.html"><span class="ck">&rarr;</span> Send documents securely</a></li>'
      '<li><a href="pay.html"><span class="ck">&rarr;</span> Paying your invoice</a></li>'
      '</ul></div></div></div></div></section>'

      '<section class="sec tint"><div class="wrap"><div class="sec-head reveal">'
      '<span class="eyebrow">Common questions</span><h2>Answers before you call.</h2></div>'
      + faq_html(HOME_FAQS) +
      '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">More questions answered ' + ARROW + '</a></p>'
      '</div></section>'
    )
    return dict(path='index.html', depth=0, nav='home',
      title='James L. Hickey, CPA PC | Tax & Accounting, Tewksbury MA',
      desc='A full service tax, accounting and business consulting firm in Tewksbury, Massachusetts. Tax preparation, planning, IRS problem resolution, QuickBooks and small business work.',
      body=body,
      schema=[_org(),
              {"@context": "https://schema.org", "@type": "WebSite", "name": FIRM['name'],
               "url": BASE, "publisher": {"@id": ORG_ID}},
              faq_schema([(q, _plain(a)) for q, a in HOME_FAQS])])


# ---------------------------------------------------------------- about
def _about():
    p = dict(path='about.html', depth=0, nav='about',
      title='About the Firm | James L. Hickey, CPA PC, Tewksbury MA',
      desc='A full service tax, accounting and business consulting firm in Tewksbury, Massachusetts: what the practice does, who it works with, and how an engagement runs.',
      eyebrow='About the firm', h1='A full service practice, run out of one office in Tewksbury.',
      sub='James L. Hickey, CPA PC works with individuals, small businesses and non-profit organizations across the Merrimack Valley.')
    p['body'] = phero(p, [('About the firm', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>James L. Hickey, CPA PC is a full service tax, accounting and business consulting firm located in '
      'Tewksbury, Massachusetts. The practice describes itself as one of the leading firms in the Tewksbury and '
      'Merrimack Valley areas, and it works from a single office at 170 Main Street, Suite 110.</p>'
      '<p>The range is wide for a practice this size, and deliberately so. Tax preparation and planning sit '
      'alongside a working IRS problem-resolution practice; small business accounting and QuickBooks consulting '
      'sit alongside business valuation, succession planning and entity formation; and the personal side covers '
      'financial planning, estate planning and elder care. Most clients eventually need more than one of those, '
      'and having them in one place is the practical argument for a firm like this one.</p>'

      '<h2>Who you are dealing with</h2>'
      '<p>The practice carries the name of James L. Hickey, CPA. A certified public accountant has passed the '
      'Uniform CPA Examination, met a state&rsquo;s education and experience requirements, and holds an active '
      'licence &mdash; and, relevant to a great deal of the work here, may represent a taxpayer before the '
      'Internal Revenue Service without limitation.</p>'
      '<p>Behind the tax and accounting work is the firm&rsquo;s staff. Whom you speak to about a given matter '
      'depends on what the matter is; the office is small enough that this is a short conversation rather than '
      'a routing exercise.</p>'

      '<h2>Who the practice works with</h2>'
      '<h3>Individuals and families</h3>'
      '<p>Returns for households across the Merrimack Valley, including the ones that are more complicated than '
      'their owners expect: income earned across a state line, rental property, investment activity with a basis '
      'history nobody has tracked, a retirement that started mid-year, an inheritance. Alongside that, the '
      '<a href="services/personal-financial-planning.html">planning</a>, <a href="services/estate-planning.html">'
      'estate</a> and <a href="services/elder-care.html">elder care</a> work that tends to arrive with them.</p>'

      '<h3>Small and closely held businesses</h3>'
      '<p>From a first-year sole proprietor deciding whether to form an LLC through to an established company '
      'preparing to change hands. The work runs from <a href="services/entity-formation.html">setting the entity '
      'up</a> and <a href="services/quickbooks.html">getting the books working</a>, through '
      '<a href="services/small-business-services.html">monthly reporting</a>, '
      '<a href="services/bank-financing.html">financing packages</a> and '
      '<a href="services/tax-planning.html">planning</a>, to '
      '<a href="services/business-valuation.html">valuation</a> and '
      '<a href="services/succession-planning.html">succession</a>.</p>'

      '<h3>Non-profit organizations</h3>'
      '<p>Charities and other exempt organizations have a different reporting audience &mdash; a board, funders, '
      'the Commonwealth and the public &mdash; and an annual filing that anyone can read. See '
      '<a href="services/non-profit.html">non-profit services</a>.</p>'

      '<h3>Taxpayers with an IRS problem</h3>'
      '<p>People arrive at this part of the practice from every direction: a business that fell behind on payroll '
      'deposits, a household that stopped filing after a bad year, a spouse who signed a joint return without '
      'seeing the figures, a notice that is simply wrong. It is a defined, procedural area of work, and it is '
      'handled here rather than referred elsewhere. See <a href="services/irs-representation.html">IRS problem '
      'resolution</a>.</p>'

      '<h2>How an engagement runs</h2>'
      '<p>It starts with a phone call, usually ten minutes: what kind of return or entity, roughly what the year '
      'looked like, and what deadline is driving the question. From that it is normally clear whether the matter '
      'is a preparation job, a planning conversation, a bookkeeping problem, an IRS matter, or some combination.</p>'
      '<p>Documents come in through the <a href="client-portal.html">secure portal</a> or across the desk. Work is '
      'done, questions are asked as they arise rather than saved for a covering letter, and the return or the '
      'report is reviewed with you rather than mailed at you.</p>'

      '<div class="callout"><p><strong>Client information is confidential.</strong> That obligation is part of the '
      'professional rules governing a CPA licence, not an office policy, and it covers the fact that you called '
      'as much as anything you said.</p></div>'

      '<h2>What is on this site</h2>'
      '<p>The <a href="services/index.html">services section</a> covers all sixteen practice areas in detail. '
      'There are <a href="calculators/index.html">eight financial calculators</a> that run entirely in your '
      'browser, a <a href="guides/irs-notice-what-to-do.html">guide to what to do when an IRS notice arrives</a>, '
      'a <a href="guides/quickbooks-year-end-checklist.html">QuickBooks year-end checklist</a>, and the '
      '<a href="faq.html">questions this office is asked most</a>.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">The office</div>'
      '<p><strong style="color:#fff">Address</strong><br>' + FIRM['addr'] + '<br>'
      + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p><strong style="color:#fff">Telephone</strong><br>' + FIRM['ph'] + '</p>'
      '<p><strong style="color:#fff">Facsimile</strong><br>' + FIRM['fax'] + '</p>'
      '<a class="btn b-acc" href="contact.html">Contact the office</a></div>'
      + _why_aside(0) +
      '<div class="acard light"><div class="t">Firm pages</div><ul>'
      '<li><a href="services/index.html"><span class="ck">&rarr;</span> All services</a></li>'
      '<li><a href="client-portal.html"><span class="ck">&rarr;</span> Client portal</a></li>'
      '<li><a href="pay.html"><span class="ck">&rarr;</span> Paying your invoice</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div></div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('About the firm', BASE + 'about.html')])]
    return p


# ---------------------------------------------------------------- FAQ
FAQS_EXTRA = [
 ("What is the difference between a CPA and a tax preparer?",
  "<p>Anyone may prepare returns for payment with a preparer identification number. A certified public accountant has passed the Uniform CPA Examination, met a state&rsquo;s education and experience requirements and holds an active licence. The distinction matters most when something goes wrong: attorneys, CPAs and enrolled agents may represent a taxpayer before the IRS without limitation, and other preparers generally cannot.</p>"),
 ("When should I start thinking about tax planning?",
  "<p>Before the transaction, and at the latest before December 31. Entity structure, owner compensation, the timing of income and deductions, equipment purchases and retirement contributions are all decided during the year. By the filing deadline the return is simply recording what happened. See <a href=\"services/tax-planning.html\">tax planning</a>.</p>"),
 ("I have not filed in several years. What happens now?",
  "<p>Less than you fear, and it is fixable. Transcripts establish which years are genuinely missing and what the Service already has on record; returns are then reconstructed and filed, usually reducing balances that were assessed on substitute returns prepared without any deductions. See <a href=\"services/non-filed-returns.html\">non-filed returns</a>.</p>"),
 ("Can you set up a payment plan with the IRS for me?",
  "<p>Yes, once filings are current &mdash; that is a precondition for every arrangement the Service offers. Which route fits depends on the balance, your income and assets, and the allowable expense standards the Service applies. See <a href=\"services/irs-payment-plans.html\">payment arrangements</a>.</p>"),
 ("Should my business be an S corporation?",
  "<p>Only when profit is reliably above what the owner would have to be paid as a salary, by enough to cover payroll administration, a separate return and the reasonable compensation exposure. It is a calculation on your figures rather than a rule. See <a href=\"services/entity-formation.html\">entity selection</a>.</p>"),
 ("Do you work with QuickBooks?",
  "<p>Yes &mdash; setup for new businesses, one-to-one training on your own file, and tune-ups for files that have drifted. See <a href=\"services/quickbooks.html\">QuickBooks consulting</a> and the <a href=\"guides/quickbooks-year-end-checklist.html\">year-end checklist</a>.</p>"),
 ("Can you value my business?",
  "<p>Yes. The first question is why the figure is needed &mdash; a sale, a buy-sell agreement, a gift or estate filing, a divorce or a dispute &mdash; because the purpose sets the standard of value and often the answer. See <a href=\"services/business-valuation.html\">business valuation</a>.</p>"),
 ("Do you draft wills and trusts?",
  "<p>No. Those are legal instruments drafted by an attorney. We handle the tax projections, the basis and gifting analysis, the fiduciary returns and the executor support, and we coordinate with your attorney. See <a href=\"services/estate-planning.html\">estate planning</a>.</p>"),
 ("Do you sell investments or insurance?",
  "<p>No. The <a href=\"services/personal-financial-planning.html\">financial planning work</a> here is analysis and advice on the tax and cash flow side, which is part of what makes a second opinion useful.</p>"),
 ("What should I bring to a first meeting?",
  "<p>For a business: the last filed entity return, the most recent financial statements, and anything imposing a deadline on you &mdash; a loan agreement, a lease, a letter of intent, an IRS notice. For an individual: last year&rsquo;s return and a short description of what changed. If you do not have all of it, come anyway.</p>"),
 ("Do you work with clients outside Tewksbury?",
  "<p>Yes. The office is on Main Street in Tewksbury and much of the client base is in the surrounding Merrimack Valley towns, but very little of this work requires anyone to be in the same room.</p>"),
 ("Is my information kept confidential?",
  "<p>Yes. Confidentiality is part of the professional rules governing a CPA licence rather than an office policy, and the <a href=\"client-portal.html\">secure portal</a> exists so that documents do not have to travel by ordinary email.</p>"),
]


def _faq():
    allq = HOME_FAQS + FAQS_EXTRA
    p = dict(path='faq.html', depth=0, nav='about',
      title='Common Questions | James L. Hickey, CPA PC, Tewksbury MA',
      desc='Answers about tax preparation and planning, IRS notices and payment plans, entity choice, QuickBooks, valuation and estate work at a Tewksbury CPA office.',
      eyebrow='Answers', h1='Questions this office gets asked, answered plainly.',
      sub='If yours is not here, telephone and ask. Nobody will route you to a form.')
    p['body'] = phero(p, [('Common questions', None)]) + (
      '<section class="sec"><div class="wrap"><div class="sec-head reveal">'
      '<h2>Working with the firm</h2>'
      '<p class="lead">What this office does, how an engagement starts, and the questions that come up most.</p></div>'
      + faq_html(allq) +
      '<div class="sec-head reveal" style="margin-top:56px"><h2>Longer answers</h2>'
      '<p class="lead">Two pieces cover the questions that need more than a paragraph: '
      '<a href="guides/irs-notice-what-to-do.html">what to do when an IRS notice arrives</a> and '
      '<a href="guides/quickbooks-year-end-checklist.html">closing your QuickBooks year</a>. '
      'There are also <a href="calculators/index.html">eight calculators</a> for the arithmetic.</p></div>'
      '</div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Common questions', BASE + 'faq.html')]),
                   faq_schema([(q, _plain(a)) for q, a in allq])]
    return p


# ---------------------------------------------------------------- contact
def _contact():
    p = dict(path='contact.html', depth=0, nav='contact',
      title='Contact | James L. Hickey, CPA PC, Tewksbury Massachusetts',
      desc='Reach the office at 170 Main Street, Suite 110, Tewksbury, Massachusetts. Telephone (978) 851-8945, facsimile (978) 851-9314, with an interactive map.',
      eyebrow='Contact', h1='170 Main Street, Suite 110, Tewksbury.',
      sub='Telephone, facsimile, email or the secure portal &mdash; whichever suits what you are sending.')
    p['body'] = phero(p, [('Contact', None)]) + (
      '<section class="sec"><div class="wrap">'
      '<div class="sec-head reveal"><h2>The office</h2>'
      '<p class="lead">One office in Tewksbury, in the Merrimack Valley, convenient to Wilmington, Billerica, '
      'Andover, North Reading, Dracut, Chelmsford and Lowell.</p></div>'
      '<div class="split">'
      '<div>' + gmap('Pan, zoom or open the map full screen for turn-by-turn directions.') + '</div>'
      '<div class="aside"><div class="acard"><div class="t">Reach us</div>'
      '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<p>Telephone ' + FIRM['ph'] + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Quick links</div><ul>'
      '<li><a href="' + FIRM['maps'] + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Directions in Google Maps</a></li>'
      '<li><a href="mailto:' + FIRM['email'] + '"><span class="ck">&rarr;</span> ' + FIRM['email'] + '</a></li>'
      '<li><a href="client-portal.html"><span class="ck">&rarr;</span> Send documents securely</a></li>'
      '<li><a href="pay.html"><span class="ck">&rarr;</span> Paying your invoice</a></li>'
      '</ul></div></div></div></div></section>'
      '<section class="sec tint"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>What a first call is like</h2>'
      '<p>Usually about ten minutes. What kind of return or entity, roughly what the year looks like, and what '
      'deadline is driving the question. From that it is normally clear whether the matter is a preparation job, '
      'a planning conversation, a bookkeeping problem, an IRS matter, or a combination &mdash; and what the work '
      'involves.</p>'
      '<p>If the work belongs somewhere else, we will say so and point you in a useful direction.</p>'

      '<h2>What to have to hand</h2>'
      '<ul>'
      '<li>For a business: the most recently filed entity return and the most recent financial statements, in '
      'whatever form they exist</li>'
      '<li>Anything with a date on it &mdash; a loan agreement, a lease, a letter of intent, a board resolution, '
      'an IRS or Massachusetts notice (keep the envelope)</li>'
      '<li>For an individual: last year&rsquo;s return and a short description of what changed</li>'
      '<li>For a QuickBooks question: access to the file, or a recent set of reports</li>'
      '</ul>'
      '<p>Missing pieces are not a problem. Bring what you have.</p>'

      '<h2>Sending documents</h2>'
      '<p>Tax documents should not travel as ordinary email attachments. The <a href="client-portal.html">secure '
      'client portal</a> exists for exactly this, and documents can also be dropped at the office or sent by '
      'facsimile to ' + FIRM['fax'] + '.</p>'

      '<h2>Visiting</h2>'
      '<p>The office is at 170 Main Street, Suite 110, in Tewksbury. Please telephone or email to arrange a time '
      'before coming in &mdash; filing season in particular runs on appointments.</p>'

      '<h2>Confidentiality</h2>'
      '<p>Client information is confidential, including the fact that you called. That obligation runs through the '
      'professional rules governing a CPA licence rather than through an office policy.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Prefer email?</div>'
      '<p>Write to the office and describe the situation. For anything containing personal tax data, use the '
      'portal instead.</p>'
      '<a class="btn b-acc" href="mailto:' + FIRM['email'] + '">' + FIRM['email'] + '</a></div>'
      + _why_aside(0) + '</div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Contact', BASE + 'contact.html')]),
      {"@context": "https://schema.org", "@type": "ContactPage",
       "name": "Contact James L. Hickey, CPA PC", "url": BASE + 'contact.html'}]
    return p


# ---------------------------------------------------------------- client portal
PORTAL_FAQS = [
 ("How do I get a portal login?",
  "<p>Logins are issued by the office. Telephone (978) 851-8945 or write to info@hickeycpa.com and one will be set up for you. It is not something you can create for yourself, which is deliberate &mdash; the account has to be tied to a known client.</p>"),
 ("Why not just email documents?",
  "<p>Ordinary email is not encrypted end to end, is copied across several servers on the way, and stays in two mailboxes indefinitely. A W-2, a full return or a page with a Social Security number on it is exactly the material that should not travel that way.</p>"),
 ("What should go through the portal?",
  "<p>Anything with identifying or financial information on it: source documents, prepared returns, financial statements, bank records, payroll reports and signature pages.</p>"),
 ("Can I get last year's return from it?",
  "<p>Documents the office has posted to your account remain available to download. If something you need is not there, ask and it can be posted.</p>"),
 ("I have forgotten my password.",
  "<p>Use the password reset on the login page. If that does not resolve it, telephone the office rather than trying repeatedly &mdash; repeated failures lock the account.</p>"),
]


def _portal():
    p = dict(path='client-portal.html', depth=0, nav='portal',
      title='Client Portal | James L. Hickey, CPA PC, Tewksbury MA',
      desc='The secure client portal for exchanging tax documents, returns and financial records with the Tewksbury office, instead of sending them by ordinary email.',
      eyebrow='Client portal', h1='A secure place to send documents that should not be emailed.',
      sub='Returns, source documents and financial records move between you and the office through an encrypted portal rather than through your inbox.')
    p['body'] = phero(p, [('Client portal', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<p>The office operates a secure firm portal for exchanging documents with clients. You upload source '
      'documents to it; the office posts prepared returns, financial statements and reports back to it; and both '
      'sides have a record of what was sent and when.</p>'
      '<p><a class="btn b-acc" href="' + PORTAL + '" target="_blank" rel="noopener">Open the client portal '
      + ARROW + '</a></p>'

      '<h2>Why this exists</h2>'
      '<p>A tax file is the single most useful package of documents an identity thief can obtain: full name, '
      'address, Social Security numbers for an entire household, dates of birth, employer, bank account and '
      'routing numbers, and a year of financial detail. Ordinary email carries all of that in the clear, copies '
      'it across intermediate servers, and then leaves it sitting in two mailboxes for as long as either account '
      'exists.</p>'
      '<p>Tax-related identity theft usually shows up as a return rejected because one has already been filed '
      'under your Social Security number, and unwinding it takes months. The portal is a small habit that removes '
      'one of the common ways the information gets out.</p>'

      '<h2>How to use it</h2>'
      '<ol>'
      '<li><strong>Ask the office for a login.</strong> Accounts are issued by the office rather than created by '
      'visitors &mdash; telephone ' + FIRM['ph'] + ' or write to ' + FIRM['email'] + '.</li>'
      '<li><strong>Sign in and upload.</strong> Scans or photographs are both fine, as long as every page is '
      'legible and complete, including the reverse of anything printed on both sides.</li>'
      '<li><strong>Tell us it is there.</strong> A short note saying what you uploaded and what is still to come '
      'saves a round of correspondence.</li>'
      '<li><strong>Collect what is posted back.</strong> Prepared returns, statements and reports are posted to '
      'the same account for you to download.</li>'
      '</ol>'

      '<div class="callout"><p><strong>A note on scanning.</strong> Photographs taken on a telephone are perfectly '
      'usable if the whole page is in frame, flat and in focus. The most common problem is a corner cut off a form '
      '&mdash; which is exactly where the figure we need tends to be.</p></div>'

      '<h2>What to send, and when</h2>'
      '<p>For an individual return: the income documents as they arrive rather than in one batch at the end, '
      'records supporting anything you intend to deduct, last year&rsquo;s return if this office did not prepare '
      'it, and a note describing what changed during the year. For a business: the accounting file or reports, '
      'bank and loan statements, payroll returns, and the note listing anything unusual that happened. The '
      '<a href="guides/quickbooks-year-end-checklist.html">year-end checklist</a> sets that out in full.</p>'

      '<h2>Other ways to reach the office</h2>'
      '<p>Documents can also be dropped at 170 Main Street, Suite 110, or sent by facsimile to ' + FIRM['fax'] +
      '. For anything that is not a document, <a href="contact.html">telephone or email</a> is easiest.</p>'

      '<h2>Common questions</h2>' + faq_html(PORTAL_FAQS) +
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Portal access</div>'
      '<p>Logins are issued by the office. Call or email and one will be set up for you.</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="' + PORTAL + '" target="_blank" rel="noopener"><span class="ck">&rarr;</span> Open the portal</a></li>'
      '<li><a href="pay.html"><span class="ck">&rarr;</span> Paying your invoice</a></li>'
      '<li><a href="guides/quickbooks-year-end-checklist.html"><span class="ck">&rarr;</span> Year-end checklist</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the office</a></li>'
      '</ul></div>' + _why_aside(0) + '</div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Client portal', BASE + 'client-portal.html')]),
                   faq_schema([(q, _plain(a)) for q, a in PORTAL_FAQS])]
    return p


# ---------------------------------------------------------------- pay
def _pay():
    p = dict(path='pay.html', depth=0, nav='portal',
      title='Paying Your Invoice | James L. Hickey, CPA PC, Tewksbury',
      desc='How to pay an invoice from the Tewksbury office: by cheque through the post or in person, or by card, and what to include so the payment is applied correctly.',
      eyebrow='Payments', h1='Paying an invoice from the office.',
      sub='By cheque through the post, in person at 170 Main Street, or by card. Whichever route you use, quote the invoice number.')
    p['body'] = phero(p, [('Paying your invoice', None)]) + (
      '<section class="sec"><div class="wrap"><div class="split"><div class="prose reveal">'
      '<h2>By cheque</h2>'
      '<p>Make it payable to <strong>James L. Hickey, CPA PC</strong> and post it to:</p>'
      '<p><strong>James L. Hickey, CPA PC<br>' + FIRM['addr'] + '<br>'
      + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</strong></p>'
      '<p>Write the invoice number on the memo line. Where a payment covers more than one invoice, or covers a '
      'business and a personal engagement, a short note saying how it should be split prevents it being applied '
      'to the wrong account.</p>'

      '<h2>In person</h2>'
      '<p>Payment can be left at the office at 170 Main Street, Suite 110. Telephone ' + FIRM['ph'] + ' first if '
      'you need someone to be there.</p>'

      '<h2>By card</h2>'
      '<p>Card payment is available. Please <a href="contact.html">telephone the office</a> to arrange it rather '
      'than sending card details by email or leaving them on a voicemail &mdash; a card number in an inbox is a '
      'problem waiting to happen.</p>'

      '<div class="callout"><p><strong>What to quote.</strong> The invoice number, the name the work was done '
      'under, and the tax year or period it relates to. Those three items are what allow a payment to be matched '
      'without a telephone call.</p></div>'

      '<h2>Questions about an invoice</h2>'
      '<p>If something on an invoice is unclear, or does not match what you expected the engagement to involve, '
      'telephone the office and ask. That is a short conversation and it is a great deal better than a silence.</p>'

      '<h2>Paying a tax balance is a different thing</h2>'
      '<p>An invoice from this office is a fee for professional work. Tax owed to the IRS or to the Commonwealth '
      'is paid directly to them, never to us, and never to anyone who telephones you demanding immediate payment '
      'by gift card or wire transfer. If a balance cannot be paid at once there are proper routes for that &mdash; '
      'see <a href="services/irs-payment-plans.html">payment arrangements</a>.</p>'
      '</div>'
      '<div class="aside"><div class="acard"><div class="t">Post payment to</div>'
      '<p>James L. Hickey, CPA PC<br>' + FIRM['addr'] + '<br>'
      + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
      '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a></div>'
      '<div class="acard light"><div class="t">Related</div><ul>'
      '<li><a href="client-portal.html"><span class="ck">&rarr;</span> Client portal</a></li>'
      '<li><a href="contact.html"><span class="ck">&rarr;</span> Contact the office</a></li>'
      '<li><a href="services/irs-payment-plans.html"><span class="ck">&rarr;</span> IRS payment arrangements</a></li>'
      '<li><a href="faq.html"><span class="ck">&rarr;</span> Common questions</a></li>'
      '</ul></div>' + _why_aside(0) + '</div></div></div></section>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Paying your invoice', BASE + 'pay.html')])]
    return p


# =========================================================================
def pages():
    P = [_home(), _about(), _faq(), _contact(), _portal(), _pay(), _services_hub()]
    P += [_svc_page(s) for s in SERVICES]
    P += _calc_pages()
    P += [_guide_page(g) for g in GUIDES]
    for p in P:
        p.setdefault('cta_args', DEFAULT_CTA)
    return P
