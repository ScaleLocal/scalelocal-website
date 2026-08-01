# -*- coding: utf-8 -*-
"""
Mill City Accounting Services LLC — all page content.

Sixteen pages: home, about, services hub + four services, two specialism pages
(quick-serve restaurants, rental real estate), FAQ, contact, calculators hub +
four calculators.

Honesty posture for this build:
  * Scott Marchlik claims no professional credential on his own site. Nothing
    here calls him a CPA or an EA, and no page implies a licence, a membership,
    a staff, or an experience figure the firm has not published itself.
  * The only verified biography facts are the ones on his own About page:
    UMass Lowell, BBA with an accounting concentration, spring 2007; staff
    accountant at a CPA firm in Cambridge from summer 2007, starting as a
    bookkeeper and moving into business and individual tax preparation;
    a clientele there of mostly quick-serve restaurant owners and rental real
    estate owners; left as accounting supervisor in spring 2018 to open Mill City.
  * "Accounting You Can Count On" and "Serving Our Community" are the firm's
    own lines and are used as such.
"""
import html, re
from build import (FIRM, BASE, T, icon, ARROW, phero, faq_html, rel, gmap,
                   breadcrumb_schema, faq_schema)
import calculators as C

PAY = 'https://square.link/u/1BBydiwq'          # preserved verbatim from the live site
ORG = BASE + '#firm'


# --------------------------------------------------------------------------
# small builders — every one of these opens and closes its own containers, so
# nesting stays balanced no matter how the pages are assembled (GATE A).
# --------------------------------------------------------------------------
def _plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('  ', ' ').strip()


def _sec(inner, cls='sec', pid=None):
    return ('<section class="' + cls + '"' + (' id="' + pid + '"' if pid else '')
            + '><div class="wrap">' + inner + '</div></section>')


def _head(title, lead=None, eyebrow=None):
    return ('<div class="sec-head reveal">'
            + ('<span class="eyebrow">' + eyebrow + '</span>' if eyebrow else '')
            + '<h2>' + title + '</h2>'
            + ('<p class="lead">' + lead + '</p>' if lead else '')
            + '</div>')


def _split(main, aside):
    return '<div class="split">' + main + '<div class="aside">' + aside + '</div></div>'


def _prose(inner):
    return '<div class="prose reveal">' + inner + '</div>'


def _acard(t, inner, light=False):
    return ('<div class="acard' + (' light' if light else '') + '"><div class="t">'
            + t + '</div>' + inner + '</div>')


def _links(items):
    return ('<ul>' + ''.join('<li><a href="' + h + '"><span class="ck">&rarr;</span> ' + l
                             + '</a></li>' for h, l in items) + '</ul>')


def _checks(items):
    return ('<ul>' + ''.join('<li><span class="ck">&#10003;</span> ' + l + '</li>'
                             for l in items) + '</ul>')


def _card(d, href, ic, title, text, num=None):
    return ('<a class="card reveal" href="' + rel(d, href) + '">'
            + ('<span class="num">' + num + '</span>' if num else '')
            + '<div class="cic">' + icon(ic) + '</div><h3>' + title + '</h3><p>' + text + '</p>'
            '<span class="more">Read more ' + ARROW + '</span></a>')


def _call_card(text='Describe what you need in a couple of minutes. Scott will tell you what '
                    'the work involves and whether he is the right person for it.'):
    return _acard('Talk to Scott', '<p>' + text + '</p>'
                  '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">' + FIRM['ph'] + '</a>')


def _pay_card(d=0):
    return _acard('Pay your invoice',
                  '<p>Card payments go through Square. The link opens Mill City&rsquo;s own '
                  'secure Square checkout page &mdash; no account needed.</p>'
                  '<a class="btn b-acc" href="' + PAY + '" target="_blank" rel="noopener">'
                  'Pay by card ' + ARROW + '</a>')


def _weave(n, x0, x1, t, g):
    """Plain-weave lattice: warp and weft, each thread broken where it passes
    under the one crossing it. Same construction as the logo, more threads."""
    step = (x1 - x0 - t) / float(n - 1)
    xs = [round(x0 + i * step, 2) for i in range(n)]
    out = []
    for i, x in enumerate(xs):
        segs, cur = [], x0
        for j, y in enumerate(xs):
            if (i + j) % 2 == 0:
                segs.append((cur, y - g))
                cur = y + t + g
        segs.append((cur, x1))
        out += [(x, round(a, 2), t, round(b - a, 2)) for a, b in segs if b - a > 0.4]
    for j, y in enumerate(xs):
        segs, cur = [], x0
        for i, x in enumerate(xs):
            if (i + j) % 2 == 1:
                segs.append((cur, x - g))
                cur = x + t + g
        segs.append((cur, x1))
        out += [(round(a, 2), y, round(b - a, 2), t) for a, b in segs if b - a > 0.4]
    return out


HERO_ART = ''.join('<rect x="%s" y="%s" width="%s" height="%s" rx="1.5"/>' % r
                   for r in _weave(5, 8, 120, 13, 4.5))


# The engine collapses .cards to one column below 860px, but `.cards.two` wins
# on specificity and stays two-up on a phone. Two 165px cards is not readable;
# this is scoped to the pages that use the two-column grid.
GRID_FIX = ('<style>@media(max-width:700px){.cards.two{grid-template-columns:minmax(0,1fr)}}'
            '@media(max-width:560px){.strip .l{font-size:.78rem}}</style>')


# --------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------
def _org():
    return {
        "@context": "https://schema.org", "@type": "AccountingService", "@id": ORG,
        "name": FIRM['name'], "legalName": FIRM['name'], "url": BASE,
        "email": FIRM['email'], "telephone": FIRM['ph'], "faxNumber": FIRM['fax'],
        "foundingDate": "2018", "slogan": "Accounting You Can Count On",
        "founder": {"@type": "Person", "name": "Scott Marchlik", "jobTitle": "Founder"},
        "address": {"@type": "PostalAddress", "streetAddress": FIRM['addr'],
                    "addressLocality": FIRM['city'], "addressRegion": FIRM['state'],
                    "postalCode": FIRM['zip'], "addressCountry": "US"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "09:00", "closes": "17:00"}],
        "areaServed": [{"@type": "AdministrativeArea",
                        "name": "Lowell and the Merrimack Valley, Massachusetts"}],
        "knowsAbout": ["Tax preparation", "Bookkeeping", "Payroll",
                       "Notary public services", "Restaurant accounting",
                       "Rental property accounting"],
        "hasMap": FIRM['maps'],
    }


def _svc_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "description": desc, "url": url, "serviceType": name,
            "provider": {"@id": ORG},
            "areaServed": {"@type": "AdministrativeArea",
                           "name": "Lowell, Massachusetts"}}


def _faq_ld(faqs):
    return faq_schema([(q, _plain(a)) for q, a in faqs])


CTA = ('Talk to Scott.',
       'Call the office or write to scott@millcityaccounting.com. Describe the situation, '
       'and you will get a straight answer about what the work involves and what happens next.')


# --------------------------------------------------------------------------
# services
# --------------------------------------------------------------------------
SERVICES = [
 dict(slug='tax-preparation', ic='calc', nav_title='Tax Preparation',
   short='Federal and Massachusetts returns for businesses and for the people who own them, prepared by the same person who keeps the books.',
   title='Tax Preparation in Lowell, MA | Mill City Accounting',
   desc='Business and individual tax preparation in Lowell, Massachusetts. Federal and Massachusetts returns for sole proprietors, LLCs, S corporations, landlords and families.',
   eyebrow='Tax', h1='Business and individual returns, prepared together.',
   sub='When you own the business, the entity return and your own return are one problem. Mill City prepares both, which is the only way the numbers stay consistent.',
   body='''
<h2>The short answer</h2>
<p>Scott Marchlik prepares federal and Massachusetts income tax returns for small businesses and for individuals. Tax preparation has been part of his work since he moved from bookkeeping into business and individual returns at a CPA firm in Cambridge in the years before he opened Mill City in 2018.</p>

<h2>Whose returns these are</h2>
<h3>Business owners</h3>
<p>Sole proprietors and single-member LLCs reporting on Schedule C. Partnerships and multi-member LLCs filing Form 1065, with a K-1 out to each owner and a Massachusetts Form 3 alongside it. S corporations filing Form 1120-S and Massachusetts Form 355S, where owner compensation is the question that comes up every single year.</p>
<p>The K-1 or the Schedule C does not end the job. It lands on a personal return, usually with a spouse&rsquo;s wages, sometimes with rental income, occasionally with a property sale. Preparing the business return without seeing where it lands is how avoidable surprises happen.</p>
<h3>Individuals and families</h3>
<p>Form 1040 with the Massachusetts Form 1: wages, retirement income, investment income, education credits, and the very common Lowell situation of a two- or three-family house where the owner lives in one unit and rents the others.</p>

<h2>What tends to matter on a Massachusetts return</h2>
<ul>
<li><strong>Massachusetts does not simply mirror the federal code.</strong> Depreciation is the familiar example &mdash; the federal and Massachusetts write-off for the same asset can differ, which means two sets of records for as long as you own it. That divergence is easy to start and expensive to reconstruct later.</li>
<li><strong>The surtax on high income is measured on the whole year.</strong> Massachusetts applies an additional tax above a threshold that is adjusted annually, and it looks at total income. A single large event &mdash; selling a building, a business, or a large block of stock &mdash; can push an ordinary year over the line. That is worth modelling before the closing, not after.</li>
<li><strong>Sales and meals tax are their own filings.</strong> They are not part of the income tax return, they run on their own calendar, and missing them creates penalties that have nothing to do with how profitable the year was.</li>
<li><strong>Estimated payments.</strong> Once a business throws off income that is not on a W-2, quarterly estimates start to matter federally and to the Commonwealth. Getting the first year right avoids an underpayment penalty on top of a tax bill you were not expecting.</li>
</ul>

<h2>What Scott needs from you</h2>
<p>For a business: the prior year&rsquo;s return, the year&rsquo;s books in whatever state they are in, bank and credit-card statements, payroll reports, loan statements, and a list of anything bought that will last more than a year. For an individual: last year&rsquo;s return, the W-2s and 1099s, mortgage interest and property tax, tuition and student loan statements, and a short description of what changed.</p>
<p>If some of it is missing, come in anyway. Reconstructing a year from bank statements is ordinary work, and it is better done in February than in September.</p>

<div class="callout"><p><strong>Behind on a year, or several?</strong> Unfiled years do not improve with age, and the penalties are usually a bigger problem than the tax. Bring what you have. Scott will tell you what is genuinely missing and in what order to file.</p></div>

<h2>If a notice arrives</h2>
<p>Bring it in before you answer it. A large share of notices are arithmetic, a matching problem with a 1099 the agency has and you do not, or simply wrong. The reply is usually a short letter with the right documents attached &mdash; but the deadline printed on the notice is real, so do not sit on it.</p>

<h2>How the year actually runs</h2>
<p>Clients whose books Mill City keeps have most of the return finished before the year ends, because the numbers are already reconciled. Clients who bring in a shoebox in March get a return prepared from a shoebox in March. Both are honest work; only one of them leaves room to do anything about the result.</p>
''',
   faqs=[("When should I get my documents in?",
          "<p>As soon as they are complete. Brokerage statements and corrected 1099s are the usual reason a return waits, and filing early only to amend later costs more than waiting two weeks. If you are a business client, the useful date is not April &mdash; it is whenever the books close for the year.</p>"),
         ("Do you file extensions?",
          "<p>Yes, and an extension is not a red flag. It extends the time to file, not the time to pay, so the estimate that goes with it matters. A well-estimated extension is a better outcome than a rushed return.</p>"),
         ("Can you prepare a year I never filed?",
          "<p>Yes. Prior-year returns are prepared on the forms for that year, and the order in which years get filed can matter. Bring whatever records exist and any notices you have received.</p>"),
         ("I moved to New Hampshire, or I work there. Does that change things?",
          "<p>It can, and the answer depends on where you live, where the work is physically performed, and what your employer withholds. Describe the situation on the phone before you assume either way.</p>"),
         ("Do you prepare both my business return and my personal one?",
          "<p>Yes &mdash; and for an owner-operated business that is the point. One person sees the K-1 leave the entity return and land on the 1040, so the two agree.</p>")],
   related=[('bookkeeping.html', 'Bookkeeping'), ('payroll.html', 'Payroll'),
            ('../restaurant-accounting.html', 'Restaurant accounting'),
            ('../rental-property-accounting.html', 'Rental property accounting'),
            ('../calculators/self-employment-tax.html', 'Self-employment tax calculator')]),

 dict(slug='bookkeeping', ic='ledger', nav_title='Bookkeeping',
   short='Monthly books that are reconciled, categorised and ready to answer a question — not a pile of receipts reassembled in March.',
   title='Bookkeeping for Lowell Small Businesses | Mill City',
   desc='Monthly bookkeeping, bank reconciliation and catch-up work for small businesses in Lowell, Massachusetts. Books that hold up at tax time and answer questions during the year.',
   eyebrow='Bookkeeping', h1='Books you can make a decision from.',
   sub='Scott started as a bookkeeper before he started preparing returns, and it shows in the order the work gets done.',
   body='''
<h2>The short answer</h2>
<p>Mill City keeps the books for small businesses in and around Lowell: transactions categorised, bank and credit-card accounts reconciled, payroll posted, and a set of statements you can actually read at the end of each month.</p>

<h2>What a month looks like</h2>
<ol>
<li><strong>Everything gets categorised.</strong> Bank feeds, card activity, cash sales, owner contributions and draws. The point of a chart of accounts is that the same kind of expense lands in the same place every month, so a change in it means something.</li>
<li><strong>Accounts get reconciled.</strong> Every bank and credit-card account, to the statement, every month. This is the step most often skipped, and it is the one that catches duplicate charges, missed deposits and the vendor who billed twice.</li>
<li><strong>Payroll and taxes get posted.</strong> Gross wages, the employer&rsquo;s share, withholding held and remitted &mdash; posted as they actually happen rather than as one lump.</li>
<li><strong>Statements go out.</strong> A profit and loss, a balance sheet, and a plain answer to whatever question you asked that month.</li>
</ol>

<h2>Catch-up work</h2>
<p>A meaningful share of first engagements start with a year or two that was never really finished. That is normal and it is fixable. The sequence is: reconstruct from bank and card statements, reconcile every account to the statements, fix the categorisation, then look at what the corrected numbers say &mdash; frequently that a prior return should be looked at again.</p>
<p>Catch-up is priced by how much there is to catch up. The honest first step is a phone call describing how far behind you are; nothing about it is unusual enough to be embarrassing.</p>

<h2>The chart of accounts is not a filing cabinet</h2>
<p>It is the instrument you measure the business with. A restaurant that lumps food, paper goods and cleaning supplies into &ldquo;Supplies&rdquo; cannot compute a food cost percentage, and a food cost percentage is the number that tells you whether the menu prices still work. A landlord with one account called &ldquo;Repairs&rdquo; cannot separate the deductible repair from the improvement that has to be capitalised. Both problems are set up on day one and paid for at tax time.</p>

<h2>Why the same person should do the books and the return</h2>
<p>The bookkeeper decides what a transaction is. The preparer lives with that decision. When they are the same person, the questions get asked in January rather than discovered in April, and the return is largely a summary of work already done.</p>

<div class="callout"><p><strong>Which software?</strong> Bring what you already use. The bigger determinant of whether books are useful is not the package &mdash; it is whether anyone reconciles them.</p></div>

<h2>Sales, meals and use tax</h2>
<p>If you sell taxable goods or serve prepared food, the tax you collect is not revenue and never was. It belongs to the Commonwealth and sits on your balance sheet until it is remitted. Books that treat collected tax as income overstate the business and understate the liability, and the correction usually arrives with interest attached. Restaurant owners can read more on the <a href="../restaurant-accounting.html">quick-serve page</a>.</p>
''',
   faqs=[("How far behind can I be before it is a problem?",
          "<p>Behind is a workload, not a verdict. What matters is whether the records still exist &mdash; bank and card statements, deposit records, payroll reports. Those can be pulled for prior years, so even a badly neglected set of books is usually reconstructable.</p>"),
         ("Do I have to switch accounting software?",
          "<p>No. Bring what you use. If something about the setup is genuinely making the work harder, Scott will say so and explain what changing would involve.</p>"),
         ("Can you just do the year-end and skip the monthly work?",
          "<p>Yes, and plenty of very small businesses run that way. Understand the trade: annual-only bookkeeping produces a tax return but not a management number, so you find out how the year went once the year is over.</p>"),
         ("Do you handle 1099s for my subcontractors?",
          "<p>Yes, and the time to deal with it is when you hire someone, not in January. Collecting a W-9 before the first payment turns a January scramble into a filing.</p>")],
   related=[('tax-preparation.html', 'Tax preparation'), ('payroll.html', 'Payroll'),
            ('../restaurant-accounting.html', 'Restaurant accounting'),
            ('../calculators/break-even.html', 'Break-even calculator')]),

 dict(slug='payroll', ic='people', nav_title='Payroll',
   short='Payroll run, taxes remitted, quarterly returns filed, W-2s out in January — including the tipped-employee arithmetic most packages get wrong.',
   title='Payroll Services in Lowell, MA | Mill City Accounting',
   desc='Payroll for Massachusetts small businesses: withholding, unemployment, Paid Family and Medical Leave, tipped employees, quarterly filings and January W-2s, handled in Lowell.',
   eyebrow='Payroll', h1='Payroll is a deadline business.',
   sub='The calculation is the easy part. What costs employers money is a missed deposit, a late quarterly return, or a tipped-wage rule applied loosely.',
   body='''
<h2>The short answer</h2>
<p>Mill City runs payroll for small Massachusetts employers: gross-to-net for each employee, the employer&rsquo;s share calculated, deposits made on schedule, quarterly returns filed, and W-2s and 1099s issued in January.</p>

<h2>What running payroll in Massachusetts actually involves</h2>
<p>More moving parts than most owners expect when they hire their first employee:</p>
<ul>
<li><strong>Federal.</strong> Income tax withholding, Social Security and Medicare withheld and matched, federal unemployment, deposits on whatever schedule your history puts you on, quarterly Form 941 and annual Form 940.</li>
<li><strong>Massachusetts withholding.</strong> Remitted to the Department of Revenue on a frequency that depends on your volume, with a quarterly reconciliation.</li>
<li><strong>Unemployment insurance.</strong> Quarterly wage reporting and contributions to the Department of Unemployment Assistance, at a rate that is specific to your account and moves as your experience changes.</li>
<li><strong>Paid Family and Medical Leave.</strong> Massachusetts contributions withheld and remitted quarterly, with an employer share that depends on headcount.</li>
<li><strong>New hire reporting</strong> for every employee, promptly, and a properly completed I-9 kept on file.</li>
<li><strong>Year end.</strong> W-2s to employees and 1099-NECs to contractors in January, and the corresponding filings with the agencies.</li>
</ul>
<p>Rates, thresholds and deposit frequencies change; the current figures are what get applied to your run, not the ones printed in an article.</p>

<h2>Tipped employees</h2>
<p>This is where quick-serve and counter-service employers get into trouble, and it is the part of a restaurant payroll that most often turns into a claim.</p>
<h3>The service rate and the make-up obligation</h3>
<p>Massachusetts allows a lower hourly service rate for tipped employees, but only if the employee&rsquo;s tips actually bring them to at least the full minimum wage for the shift. If they do not, the employer owes the difference. The obligation is tested on the shift, so a slow Tuesday is not covered by a strong Friday.</p>
<h3>Reporting and pooling</h3>
<p>Tips are wages for tax purposes and have to run through the payroll records. Tip pools have their own rules about who may participate; managers and owners generally may not. Getting this wrong is a wage claim, not an accounting error.</p>
<h3>The credit you may be leaving behind</h3>
<p>Employers of tipped staff can be eligible for a federal credit for the Social Security and Medicare tax paid on reported tips. It is claimed on the business return and it depends on payroll records being right, which is another reason the payroll and the return belong with the same person.</p>

<h2>Paying yourself</h2>
<p>If the business is a sole proprietorship or a single-member LLC, what you take out is a draw and does not go through payroll. If it is an S corporation, the owner working in the business has to be on payroll at reasonable compensation before distributions &mdash; it is one of the most commonly examined items on a small S corporation return, and the answer is a payroll question long before it is a tax question.</p>

<h2>The calendar you are actually working against</h2>
<table class="plain">
<tr><th>When</th><th>What</th></tr>
<tr><td>Every pay run</td><td>Gross-to-net, employer share accrued, withholding held</td></tr>
<tr><td>On your deposit schedule</td><td>Federal deposits; Massachusetts withholding remitted</td></tr>
<tr><td>Each quarter</td><td>Form 941, Massachusetts withholding reconciliation, unemployment wage report, Paid Family and Medical Leave</td></tr>
<tr><td>January</td><td>W-2s to employees, 1099-NECs to contractors, Form 940, agency copies</td></tr>
<tr><td>When you hire</td><td>New hire report, I-9, W-4 and M-4, W-9 if the person is a contractor</td></tr>
</table>

<div class="callout"><p><strong>Employee or contractor?</strong> Massachusetts applies a strict test, and calling someone a contractor because both sides prefer it is not one of the factors. Misclassification is expensive on both the payroll tax side and the wage-and-hour side. Ask before the first payment, not after the first claim.</p></div>
''',
   faqs=[("How many employees do I need before payroll is worth outsourcing?",
          "<p>One. The filing obligations are almost identical for one employee and for fifteen; what changes is how much time you lose learning them.</p>"),
         ("Can you take over mid-year?",
          "<p>Yes. What is needed is the year-to-date detail per employee and copies of the filings already made, so the totals on the W-2s at year end are right.</p>"),
         ("We pay some staff in cash. Is that a problem?",
          "<p>Paying in cash is not itself the problem &mdash; not running it through payroll is. The wages still have to be reported, withheld on and covered by workers' compensation. Unreported cash wages are the single most expensive habit a small restaurant can have.</p>"),
         ("Do you handle workers' compensation?",
          "<p>The policy comes from an insurer, not from an accountant. What payroll records do is supply the wage figures the audit at the end of the policy year is based on &mdash; and clean records are what keep that audit from producing a surprise bill.</p>")],
   related=[('bookkeeping.html', 'Bookkeeping'), ('tax-preparation.html', 'Tax preparation'),
            ('../restaurant-accounting.html', 'Restaurant accounting'),
            ('../faq.html', 'Common questions')]),

 dict(slug='notary-services', ic='doc', nav_title='Notary Services',
   short='Scott is licensed as a notary public in the Commonwealth of Massachusetts. Notarization is done at the Lowell office, by appointment.',
   title='Notary Public in Lowell, MA | Mill City Accounting',
   desc='Notarization at the Mill City Accounting office in Lowell. Scott Marchlik is licensed as a notary public in the Commonwealth of Massachusetts. Call ahead to arrange a time.',
   eyebrow='Notary', h1='Notarization, at the Kearney Square office.',
   sub='Licensed in the Commonwealth of Massachusetts. Call first &mdash; this is a one-person office, and the whole point of a notary is that somebody has to be there.',
   body='''
<h2>The short answer</h2>
<p>Scott Marchlik is licensed as a notary public in the Commonwealth of Massachusetts and notarizes documents at the Mill City office at 10 Kearney Square in downtown Lowell. Call ahead to arrange a time.</p>

<h2>What a notary actually does</h2>
<p>Less than most people assume, and it matters. A notary confirms that the person signing is who they say they are, that they are signing willingly and appear to understand what they are doing, and that the signature was made or acknowledged in the notary&rsquo;s presence. The notary then completes a certificate and records the act.</p>
<p>A notary does not verify that the contents of a document are true, does not approve the transaction, and cannot tell you whether the document is the right one for your situation. That last part is legal advice, and a notary who is not an attorney may not give it.</p>

<h2>The two things you will be asked for</h2>
<h3>An acknowledgment</h3>
<p>The most common. You confirm to the notary that the signature on the document is yours and that you made it freely. Deeds, powers of attorney and most real estate paperwork use this form.</p>
<h3>A jurat</h3>
<p>Used when the document contains a statement you are swearing to. You sign in front of the notary and take an oath or affirmation that the contents are true. Affidavits and sworn statements use this form.</p>
<p>The document itself usually tells you which one it needs, in the certificate wording printed at the bottom. If it does not, the person who is going to receive the document is the one to ask &mdash; a notary cannot choose for you.</p>

<h2>What to bring</h2>
<ul>
<li><strong>The document, unsigned.</strong> For most acts the signature has to be made or acknowledged in front of the notary. Signing at home first is the most common reason someone has to come back.</li>
<li><strong>Valid, current photo identification</strong> for every signer &mdash; a driver&rsquo;s licence, a state ID, a passport.</li>
<li><strong>Every signer, in person.</strong> A notary cannot notarize for someone who is not in the room, however well you know them.</li>
<li><strong>A complete document.</strong> Blank spaces have to be filled in or struck through before the act.</li>
<li><strong>Any witnesses the document requires.</strong> Some documents need witnesses in addition to the notary, and the notary generally cannot be one of them.</li>
</ul>

<div class="callout"><p><strong>Call before you come.</strong> Mill City is one accountant in one office, and during filing season he may be with a client or out. A two-minute call is the difference between a five-minute errand and a wasted trip. The number is <a href="tel:''' + FIRM['tel'] + '''">''' + FIRM['ph'] + '''</a>.</p></div>

<h2>What a notary cannot do</h2>
<ul>
<li>Tell you what a document means, whether to sign it, or which form of certificate to use.</li>
<li>Prepare or draft a legal document for you.</li>
<li>Notarize a signature made outside their presence, or for a signer who cannot be identified.</li>
<li>Notarize a document in which they have a personal interest.</li>
<li>Certify a copy of a vital record such as a birth, marriage or death certificate &mdash; those come from the issuing authority.</li>
</ul>

<h2>Why an accountant has a notary commission</h2>
<p>Because the documents keep arriving. Small business filings, lender paperwork, landlord and tenant documents, powers of attorney for an elderly parent, forms for a family member overseas. Having the commission means a client does not have to make a second trip to a bank branch on the day they are already sitting in the office.</p>
''',
   faqs=[("Do I have to be a client already?",
          "<p>Call and ask. Notarization is arranged by appointment, and the practical constraint is whether Scott is in the office when you need it.</p>"),
         ("Can it be done remotely, over video?",
          "<p>Plan on coming in. In-person notarization at the Lowell office is what to arrange, and it avoids every question about whether a remote act will be accepted by whoever receives the document. If your paperwork says otherwise, mention it when you call.</p>"),
         ("What does it cost?",
          "<p>Ask when you call. Massachusetts sets the framework notaries work within, and Scott will tell you before you make the trip.</p>"),
         ("I already signed it. Is that a problem?",
          "<p>Sometimes. For an acknowledgment you can appear and acknowledge a signature you made earlier. For a jurat you have to sign in front of the notary. Bring it in and ask &mdash; and if a fresh copy is easy to print, bring one.</p>")],
   related=[('../contact.html', 'Office &amp; directions'), ('tax-preparation.html', 'Tax preparation'),
            ('../rental-property-accounting.html', 'Rental property accounting'),
            ('../about.html', 'About Scott')]),
]


def _service_page(s):
    url = BASE + 'services/' + s['slug'] + '.html'
    p = dict(path='services/' + s['slug'] + '.html', depth=1, nav='services',
             title=s['title'], desc=s['desc'], eyebrow=s['eyebrow'], h1=s['h1'],
             sub=s['sub'], cta_args=CTA)
    aside = (_call_card()
             + _acard('Related', _links(s['related']), light=True)
             + _acard('Good to know', _checks([
                 'One accountant, start to finish',
                 'Lowell, Massachusetts, since 2018',
                 'Quick-serve restaurants and rental property',
                 'Notary, licensed in the Commonwealth']), light=True))
    p['body'] = phero(p, [('Services', 'services/index.html'), (_plain(s['nav_title']), None)]) + _sec(
        _split(_prose(s['body'] + '<h2>Common questions</h2>' + faq_html(s['faqs'])), aside))
    p['schema'] = [_org(),
                   breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/'),
                                      (_plain(s['nav_title']), url)]),
                   _svc_schema(_plain(s['nav_title']), _plain(s['short']), url),
                   _faq_ld(s['faqs'])]
    return p


# --------------------------------------------------------------------------
# calculators carried on this site
# --------------------------------------------------------------------------
CALC_PICK = [
 dict(slug='mortgage-payment', ic='estate',
      title='Mortgage Payment Calculator | Mill City Accounting',
      desc='Work out the monthly payment, escrow and total interest on a fixed-rate mortgage before you make an offer on a Merrimack Valley house or rental property.',
      eyebrow='Home &amp; mortgage', h1='What the payment actually comes to.',
      sub='Principal, interest, taxes and insurance on a fixed-rate loan, plus the total interest over the life of the note.',
      why='''
<h2>Why this one is here</h2>
<p>Most of the landlords Scott works with bought their first property before they had ever seen a Schedule E. The payment is the number that decides whether a property works, and it is not the number the listing quotes. Property tax and insurance are real monthly costs, and on a rental they sit above the line with everything else.</p>
<p>Two things this calculator does not include, because they vary too much to guess: mortgage insurance, which you should expect above 80% loan-to-value, and condominium or association fees. Add them to the monthly figure before you compare it to rent.</p>
<h3>What to do with the answer</h3>
<p>For a rental, take the monthly payment, add taxes, insurance, water and sewer, an honest maintenance allowance, and a vacancy allowance. Compare that to realistic rent, not the best rent the building has ever achieved. The gap is what you are buying. Then read the <a href="../rental-property-accounting.html">rental property page</a> for what happens to that gap on a tax return, because the deductible number and the cash number are not the same.</p>'''),

 dict(slug='loan-payment', ic='calc',
      title='Loan Payment Calculator | Mill City Accounting, Lowell',
      desc='Monthly payment, total interest, and what an extra payment each month does to the payoff date — for equipment loans, vehicle notes and small business term debt.',
      eyebrow='Loans', h1='What the loan costs, and what paying extra buys.',
      sub='Payment, total interest, and the number of months an extra payment each month takes off the end of the note.',
      why='''
<h2>Why this one is here</h2>
<p>Small businesses borrow for specific things: a hood system, a walk-in, a delivery vehicle, a build-out, a line that got termed out. The monthly payment is what the lender talks about. The total interest is what you actually pay, and it is the figure that decides whether a five-year note at a lower payment beats a three-year note at a higher one.</p>
<h3>The extra-payment field is the interesting one</h3>
<p>Put a realistic figure in it &mdash; not an aspirational one &mdash; and look at the months saved. On short-term business debt the effect is often smaller than people expect; on long amortisations it is dramatic. Either way it is better to know before you commit the cash, because cash paid into principal is cash you cannot use for payroll in a slow month.</p>
<h3>One tax note</h3>
<p>Interest on a business loan is generally deductible; the principal portion of the payment is not. This means the payment and the deduction are two different numbers, which is a regular source of confusion when an owner compares the bank statement to the profit and loss. If you are financing equipment, the <a href="../services/tax-preparation.html">tax treatment of the purchase itself</a> is a separate question worth asking before you sign.</p>'''),

 dict(slug='break-even', ic='chart',
      title='Break-Even Calculator for Small Business | Mill City',
      desc='Find the sales volume where a small business stops losing money, and what it takes to reach a target profit. Built for restaurant, retail and service owners in Lowell.',
      eyebrow='Business', h1='The point where the business stops losing money.',
      sub='Fixed costs, price, and cost per unit &mdash; and the volume you have to do before anything above it is profit.',
      why='''
<h2>Why this one is here</h2>
<p>Break-even is the most useful piece of arithmetic a small business owner can carry in their head, and it is the one most often never worked out. Rent, insurance, the loan payment and the salaried staff are there whether or not a single customer walks in. Every sale contributes its price minus what it cost to produce; once those contributions cover the fixed costs, the business is above water.</p>
<h3>Making it work for a restaurant</h3>
<p>For a quick-serve operation, treat the &ldquo;unit&rdquo; as an average check rather than a menu item, and put food and paper cost per check into the variable field. Hourly labour that scales with volume is variable; salaried management is fixed. The output is a covers-per-month number you can compare to what the dining room and the delivery apps actually produce. More on how those numbers get built in the <a href="../restaurant-accounting.html">quick-serve restaurant page</a>.</p>
<h3>Reading the result honestly</h3>
<p>If the contribution margin is thin, break-even is very sensitive to price and to food cost &mdash; a few percentage points of food cost can move the required volume more than a rent increase would. That sensitivity is the argument for a chart of accounts that separates food, paper and supplies, which is a <a href="../services/bookkeeping.html">bookkeeping</a> decision made long before it becomes a management one.</p>'''),

 dict(slug='self-employment-tax', ic='scale',
      title='Self-Employment Tax Calculator | Mill City Accounting',
      desc='Estimate Social Security and Medicare tax on self-employment profit, the deductible half, and roughly what each quarterly instalment ought to be for a small business owner.',
      eyebrow='Tax', h1='The tax that surprises people in their first year.',
      sub='Social Security and Medicare on net self-employment earnings, with the deductible half and a rough quarterly instalment broken out.',
      why='''
<h2>Why this one is here</h2>
<p>The first year out of a W-2 job produces the same phone call every time. The business made money, the owner set aside what felt like a reasonable amount for income tax, and then self-employment tax arrived on top of it. This is the employer&rsquo;s half of Social Security and Medicare, which an employer used to pay quietly on your behalf and which now comes out of the same pocket as everything else.</p>
<h3>What the calculator does and does not tell you</h3>
<p>It estimates self-employment tax only. It is not your income tax, it takes no account of filing status, the qualified business income deduction, or Massachusetts tax on the same profit. Add all of those before you decide what to set aside &mdash; and set the money aside in a separate account, because it is not yours.</p>
<h3>Quarterly instalments</h3>
<p>Once you owe meaningfully, federal and Massachusetts estimates start to matter, and underpaying carries a penalty even if the balance is paid in full in April. The rough quarterly figure here is a starting point; the real one takes account of the rest of your return, which is a conversation rather than a calculator.</p>
<h3>If you are an S corporation</h3>
<p>The arithmetic changes: the owner is on payroll, and payroll taxes apply to the wage rather than to the whole profit. Whether that is worth doing depends on the profit level, the reasonable compensation the role supports, and the cost of running payroll all year. See <a href="../services/payroll.html">payroll</a>, and ask before you elect.</p>'''),
]

CALC_BY_SLUG = {c['slug']: c for c in C.CALCULATORS}


# --------------------------------------------------------------------------
# FAQ content
# --------------------------------------------------------------------------
HOME_FAQS = [
 ("Who actually does my work?",
  "<p>Scott does. Mill City Accounting Services is one accountant, which means the person who takes your call is the person who categorises your transactions, runs your payroll and prepares your return. There is nobody to be handed to.</p><p>It also means the honest limit of the firm is one person&rsquo;s time. If a piece of work is not something Scott should take on, you will be told that rather than routed around it.</p>"),
 ("Are you taking new clients?",
  "<p>Call and ask. The useful first conversation is short: what kind of entity, roughly what the year looks like, and what deadline you are working against.</p>"),
 ("What does it cost?",
  "<p>It depends on what the work is. A single-owner Schedule C with clean records is not the same job as a restaurant with tipped payroll and two years of unreconciled books, and pricing either one from a web page would be guessing. Describe the situation on the phone and you will get a real answer about what the work involves.</p>"),
 ("Do you work with restaurants and landlords specifically?",
  "<p>Those are the two client types Scott worked with most before opening Mill City &mdash; quick-serve restaurant owners and rental real estate owners &mdash; and they are still the two he knows best. There are separate pages for <a href=\"restaurant-accounting.html\">quick-serve restaurants</a> and <a href=\"rental-property-accounting.html\">rental property</a>.</p>"),
 ("How do I pay an invoice?",
  "<p>By card, through Mill City&rsquo;s Square page. <a href=\"" + PAY + "\" target=\"_blank\" rel=\"noopener\">Pay your invoice here</a> &mdash; it opens a secure Square checkout and does not require an account.</p>"),
]

FAQS = HOME_FAQS + [
 ("I have not filed for two years. Where do I start?",
  "<p>With a phone call, and with whatever records still exist. Unfiled years are a workload rather than a catastrophe, but they get worse on their own: penalties accrue, and agencies eventually file a substitute return that gives you no deductions at all. The order in which years are filed can matter, so ask before you file anything.</p>"),
 ("Can you catch up a set of books that has been neglected?",
  "<p>Yes, and it is a common way engagements start. Bank and credit-card statements can be pulled for prior periods, so even badly neglected books are usually reconstructable. See <a href=\"services/bookkeeping.html\">bookkeeping</a>.</p>"),
 ("My restaurant has tipped staff. Can you handle that payroll?",
  "<p>Yes. Tipped payroll is the part of quick-serve accounting that goes wrong most often &mdash; the service rate, the obligation to make up the difference when tips fall short on a shift, who may be in a tip pool, and reporting tips as wages. It is covered on the <a href=\"services/payroll.html\">payroll page</a>.</p>"),
 ("I own a three-family in Lowell and live in one unit. How does that work?",
  "<p>The building gets split. The units you rent are a rental activity with their own income, expenses and depreciation; the unit you live in is your home, with mortgage interest and property tax treated the way any homeowner&rsquo;s would be. Shared costs &mdash; the roof, the boiler, the water bill &mdash; get allocated on a defensible basis and that basis has to stay consistent year to year. Detail on the <a href=\"rental-property-accounting.html\">rental property page</a>.</p>"),
 ("Can you notarize something for me?",
  "<p>Yes. Scott is licensed as a notary public in the Commonwealth of Massachusetts and notarizes at the Lowell office. Call first to make sure he is in, bring current photo identification, and bring the document unsigned. See <a href=\"services/notary-services.html\">notary services</a>.</p>"),
 ("Do I have to come to the office?",
  "<p>Not for most of the work. Documents can be dropped off, mailed or sent electronically, and plenty of clients only come in when there is a reason to. Notarization is the exception &mdash; that one requires you in the room.</p>"),
 ("What are the hours?",
  "<p>Monday to Friday, 9:00 AM to 5:00 PM. Saturday by appointment. Closed Sunday. During filing season it is worth calling ahead either way.</p>"),
 ("What should I bring to a first meeting?",
  "<p>For a business: the last filed return, the books in whatever state they are in, bank and card statements, payroll reports, and any notice you have received. For an individual: last year&rsquo;s return and a short description of what changed. Missing pieces are normal &mdash; bring what you have.</p>"),
 ("Is what I tell you confidential?",
  "<p>Yes. Tax return information is protected by federal rules that bind every preparer, and client information stays with the firm &mdash; including the fact that you called.</p>"),
]


# ==========================================================================
def pages():
    P = []

    # ------------------------------------------------------------ HOME
    svc_cards = ''.join([
      _card(0, 'services/tax-preparation.html', 'calc', 'Tax Preparation',
            'Federal and Massachusetts returns for businesses and for the people who own them &mdash; prepared together, by the same person.', '01'),
      _card(0, 'services/bookkeeping.html', 'ledger', 'Bookkeeping',
            'Monthly books that are categorised, reconciled to the statement and ready to answer a question &mdash; including catch-up on years that got away.', '02'),
      _card(0, 'services/payroll.html', 'people', 'Payroll',
            'Pay runs, deposits, quarterly filings and January W-2s, including the tipped-employee arithmetic that trips up counter-service employers.', '03'),
      _card(0, 'services/notary-services.html', 'doc', 'Notary Services',
            'Licensed in the Commonwealth of Massachusetts. Notarization at the Kearney Square office, by appointment.', '04'),
    ])
    spec_cards = ''.join([
      _card(0, 'restaurant-accounting.html', 'building', 'Quick-serve restaurants',
            'Daily sales journals, meals tax, tipped payroll, delivery-app settlements and the prime cost number that decides whether the menu still works.'),
      _card(0, 'rental-property-accounting.html', 'estate', 'Rental real estate',
            'Schedule E by property, repairs versus improvements, depreciation, passive loss limits, and the Massachusetts rules that catch out new landlords.'),
    ])
    calc_cards = ''.join([
      _card(0, 'calculators/mortgage-payment.html', 'estate', 'Mortgage payment',
            'Principal, interest, taxes and insurance on a fixed-rate loan &mdash; and the total interest over the life of the note.'),
      _card(0, 'calculators/loan-payment.html', 'calc', 'Loan payment and payoff',
            'What an equipment loan or vehicle note really costs, and what an extra payment each month takes off the end of it.'),
      _card(0, 'calculators/break-even.html', 'chart', 'Break-even point',
            'The volume at which the business stops losing money, and what it takes to reach a target profit.'),
      _card(0, 'calculators/self-employment-tax.html', 'scale', 'Self-employment tax',
            'Social Security and Medicare on business profit, the deductible half, and roughly what to put aside each quarter.'),
    ])

    body = (
      GRID_FIX +
      '<section class="hero" id="top"><svg class="hero-art" viewBox="0 0 128 128" aria-hidden="true">'
      + HERO_ART + '</svg>'
      '<div class="wrap"><div class="reveal in">'
      '<span class="eyebrow on-dark">Accounting &amp; Tax Services &middot; Lowell, Massachusetts</span>'
      '<h1>Accounting you can count on, from the person who does the work.</h1>'
      '<p class="sub">Mill City Accounting Services has prepared returns, kept books, run payroll and '
      'notarized documents for Lowell small businesses and families since 2018. Scott Marchlik founded '
      'the firm, and he is the one who answers the phone.</p>'
      '<div class="acts"><a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a>'
      '<a class="btn b-gh" href="services/index.html">What Scott does ' + ARROW + '</a></div>'
      '<div class="hero-trust"><span><b>Since 2018</b></span>'
      '<span><b>Lowell</b>, Massachusetts</span>'
      '<span><b>Notary</b> &middot; licensed in the Commonwealth</span>'
      '<span><b>Restaurants</b> &amp; rental property</span></div>'
      '</div></div></section>'

      '<section class="strip"><div class="wrap reveal">'
      '<div class="cell"><div class="n">2018</div><div class="l">the year Scott opened Mill City</div></div>'
      '<div class="cell"><div class="n">One</div><div class="l">accountant &mdash; the one you called</div></div>'
      '<div class="cell"><div class="n">2007</div><div class="l">the year he started in accounting</div></div>'
      '<div class="cell"><div class="n">Notary</div><div class="l">licensed in the Commonwealth of Massachusetts</div></div>'
      '</div></section>'

      + _sec(_head('Four things, done properly, by one person.',
                   'Tax preparation, bookkeeping, payroll and notarization &mdash; the services a small '
                   'business and its owner actually need, without a chain of handoffs between them.',
                   'What Mill City does')
             + '<div class="cards two">' + svc_cards + '</div>'
             + '<p style="margin-top:32px"><a class="btn b-ln" href="services/index.html">All services '
               + ARROW + '</a></p>', pid='services')

      + _sec(_head('Two kinds of business he already understands.',
                   'Before opening Mill City, Scott spent his years at a CPA firm in Cambridge working '
                   'mostly with two groups: quick-serve restaurant owners, and rental real estate owners. '
                   'Both have accounting problems that generic advice does not touch.',
                   'Where the experience is')
             + '<div class="cards two">' + spec_cards + '</div>', cls='sec tint')

      + _sec(_split(
          _prose(
            '<h2>A one-person firm is an advantage, if you use it properly.</h2>'
            '<p>The reason small businesses end up with bad books is almost never that nobody could do '
            'the arithmetic. It is that the work is split &mdash; a bookkeeper who categorises without '
            'knowing what the return needs, a payroll service that files without seeing the general '
            'ledger, a preparer who meets the numbers for the first time in March and has no way to '
            'question them. Every seam is a place for something to go wrong quietly.</p>'
            '<p>Mill City has no seams, because there is one person. That is the whole design.</p>'
            '<h3>The same person, from the first transaction to the filed return</h3>'
            '<p>Whoever decides what a transaction is has to live with that decision at tax time. When '
            'those are the same person, the awkward questions get asked in January &mdash; is this a '
            'repair or an improvement, is this contractor really a contractor, why did food cost move '
            'four points &mdash; and the return becomes a summary of work already done.</p>'
            '<h3>Serving our community</h3>'
            '<p>Scott studied accounting at UMass Lowell. Mill City is named for the city it stands '
            'in &mdash; the Mill City is what Lowell has been called since the textile mills lined the '
            'Merrimack &mdash; and it serves the small businesses and families around it. Being small '
            'and local is not a marketing position here; it is the operating model.</p>'
            '<h3>What that means in practice</h3>'
            '<ul>'
            '<li>You call a number and Scott answers it, or calls you back.</li>'
            '<li>The books, the payroll and the return are one continuous piece of work.</li>'
            '<li>If something is outside what he should take on, you get told plainly.</li>'
            '<li>The office is on Kearney Square in downtown Lowell, and you can come to it.</li>'
            '</ul>'),
          _call_card() + _pay_card()
          + _acard('Go deeper', _links([
              ('about.html', 'About Scott Marchlik'),
              ('restaurant-accounting.html', 'Quick-serve restaurants'),
              ('rental-property-accounting.html', 'Rental property'),
              ('faq.html', 'Common questions'),
              ('contact.html', 'Office &amp; directions')]), light=True)))

      + _sec(_head('Four calculators that run on this page.',
                   'No sign-up, no third-party widget, no handing your numbers to somebody else&rsquo;s '
                   'site. They work in the browser, and they are chosen for the two client types Mill '
                   'City sees most.', 'New here')
             + '<div class="cards two">' + calc_cards + '</div>'
             + '<p style="margin-top:32px"><a class="btn b-ln" href="calculators/index.html">'
               'All calculators ' + ARROW + '</a></p>', cls='sec tint')

      + _sec(_head('10 Kearney Square, downtown Lowell.',
                   'Suite 302, in downtown Lowell where Merrimack, Bridge and Central streets converge. '
                   'Monday to Friday, 9:00 AM to 5:00 PM, and Saturday by appointment.',
                   'Where to find him')
             + _split('<div>' + gmap('Open the map full screen for turn-by-turn directions to Kearney Square.') + '</div>',
                      _acard('The office',
                             '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
                             '<p>Telephone ' + FIRM['ph'] + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
                             '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a>')
                      + _acard('Getting there', _links([
                          (FIRM['maps'], 'Open in Google Maps'),
                          ('contact.html', 'Contact page &amp; what to bring'),
                          ('services/notary-services.html', 'Notarization &mdash; call first')]), light=True)))

      + _sec(_head('Answers before you call.') + faq_html(HOME_FAQS)
             + '<p style="margin-top:28px"><a class="btn b-ln" href="faq.html">More questions answered '
               + ARROW + '</a></p>', cls='sec tint')
    )
    P.append(dict(path='index.html', depth=0, nav='home',
        title='Mill City Accounting Services LLC | Lowell, MA Accountant',
        desc='Tax preparation, bookkeeping, payroll and notarization for small businesses and individuals in Lowell, Massachusetts. Founded by Scott Marchlik in 2018.',
        body=body, cta_args=CTA,
        schema=[_org(),
                {"@context": "https://schema.org", "@type": "WebSite", "name": FIRM['name'],
                 "url": BASE, "publisher": {"@id": ORG}},
                _faq_ld(HOME_FAQS)]))

    # ------------------------------------------------------------ ABOUT
    p = dict(path='about.html', depth=0, nav='about', cta_args=CTA,
        title='About Scott Marchlik | Mill City Accounting, Lowell MA',
        desc='Scott Marchlik founded Mill City Accounting Services in Lowell in 2018, after more than a decade at a CPA firm in Cambridge working with restaurant and rental property owners.',
        eyebrow='About', h1='Scott Marchlik opened Mill City in 2018.',
        sub='One accountant, in the city he studied in, doing the work he had already been doing for somebody else for more than a decade.')
    p['body'] = phero(p, [('About', None)]) + _sec(_split(
        _prose(
          '<h2>How the firm started</h2>'
          '<p>Scott studied at the University of Massachusetts Lowell and graduated in the spring of '
          '2007 with a BBA and a concentration in accounting. That summer he took a job at a CPA firm '
          'in Cambridge, Massachusetts.</p>'
          '<p>He started there as a bookkeeper. Over the years that followed he moved into preparing '
          'business and individual tax returns, and his clientele settled into a shape that has stayed '
          'with him: mostly owners of quick-serve restaurants, and owners of rental real estate. He '
          'left that firm in the spring of 2018 as an accounting supervisor, and opened Mill City '
          'Accounting Services on his own.</p>'
          '<p>Everything about how the firm works follows from that history. The order the work is '
          'learned in matters &mdash; bookkeeping first, then returns &mdash; because a preparer who '
          'has reconciled a bank account knows what a set of books is hiding.</p>'

          '<h2>Serving our community</h2>'
          '<p>Mill City is named for Lowell. The nickname comes from the textile mills that lined the '
          'Merrimack and the power canals that ran them, and it is still the name people here use for '
          'the city. The firm sits in the middle of it, at Kearney Square, and it serves the small '
          'businesses and families of Lowell and the Merrimack Valley.</p>'
          '<p>That is not a slogan about being local. It is a description of the practice: a one-person '
          'firm serves the people who can reach it, and the work comes from the neighbourhood, from '
          'people who already know somebody who uses it.</p>'

          '<h2>What Scott takes on</h2>'
          '<p>Tax preparation for businesses and individuals. Bookkeeping, monthly or as a catch-up '
          'exercise on years that got away. Payroll, including the tipped-employee arithmetic that '
          'counter-service employers have to get right. And notarization &mdash; Scott is licensed as '
          'a notary public in the Commonwealth of Massachusetts.</p>'
          '<p>Two client types get their own pages, because they are the two he knows best and because '
          'their problems are genuinely specific: '
          '<a href="restaurant-accounting.html">quick-serve restaurants</a> and '
          '<a href="rental-property-accounting.html">rental real estate</a>.</p>'

          '<h2>What a one-person firm can and cannot do</h2>'
          '<p>What it can do: give you the same person every time, hold the whole picture in one head, '
          'answer the phone, and tell you the truth about a number without a committee.</p>'
          '<p>What it cannot do: be everywhere at once. During filing season, calling ahead is the '
          'difference between a five-minute errand and a wasted trip. And if a piece of work belongs '
          'with somebody else &mdash; a specialist, an attorney, a larger firm &mdash; you will be told '
          'that rather than sold something.</p>'

          '<div class="callout"><p><strong>Accounting you can count on.</strong> That is the line Mill '
          'City has used since it opened, and the whole of it is the second half: you can count on it '
          'because you know who did it.</p></div>'

          '<h2>Where to go next</h2>'
          '<p>The <a href="services/index.html">services pages</a> set out the four things the firm '
          'does. The <a href="faq.html">common questions</a> page answers most of what people ask on a '
          'first call. And the <a href="contact.html">contact page</a> has the office details, the '
          'hours and a map.</p>'),
        _call_card()
        + _acard('The firm at a glance',
                 '<p><strong style="color:#fff">Founded</strong><br>2018, by Scott Marchlik</p>'
                 '<p><strong style="color:#fff">Office</strong><br>10 Kearney Square, Suite 302<br>Lowell, Massachusetts</p>'
                 '<p><strong style="color:#fff">Works most with</strong><br>Quick-serve restaurants and rental real estate owners</p>'
                 '<p><strong style="color:#fff">Notary</strong><br>Licensed in the Commonwealth of Massachusetts</p>'
                 '<a class="btn b-acc" href="contact.html">Contact the office</a>')
        + _acard('Pages', _links([
            ('services/index.html', 'All services'),
            ('restaurant-accounting.html', 'Quick-serve restaurants'),
            ('rental-property-accounting.html', 'Rental property'),
            ('calculators/index.html', 'Financial calculators'),
            ('faq.html', 'Common questions')]), light=True)))
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('About', BASE + 'about.html')]),
                   {"@context": "https://schema.org", "@type": "Person", "name": "Scott Marchlik",
                    "jobTitle": "Founder", "worksFor": {"@id": ORG},
                    "url": BASE + 'about.html',
                    "alumniOf": {"@type": "CollegeOrUniversity",
                                 "name": "University of Massachusetts Lowell"},
                    "knowsAbout": ["Tax preparation", "Bookkeeping", "Payroll",
                                   "Restaurant accounting", "Rental property accounting"]}]
    P.append(p)

    # ------------------------------------------------------------ SERVICES HUB
    cards = ''.join(_card(1, 'services/' + s['slug'] + '.html', s['ic'], s['nav_title'],
                          s['short'], ('0' + str(i + 1))[-2:])
                    for i, s in enumerate(SERVICES))
    p = dict(path='services/index.html', depth=1, nav='services', cta_args=CTA,
        title='Services | Mill City Accounting Services, Lowell MA',
        desc='Tax preparation, bookkeeping, payroll and notary services for small businesses and individuals in Lowell, Massachusetts, handled by one accountant from start to finish.',
        eyebrow='Services', h1='Four services that are really one job.',
        sub='Books feed payroll, payroll feeds the return, and the return raises questions that go back into the books. Splitting them across three providers is how small businesses lose track.')
    p['body'] = phero(p, [('Services', None)]) + GRID_FIX + _sec(
        _head('What Mill City does',
              'A small business and its owner need a short list of things done reliably: the books kept, '
              'the payroll filed on time, the returns prepared, and occasionally a signature witnessed. '
              'That is the list.')
        + '<div class="cards two">' + cards + '</div>') + _sec(_split(
        _prose(
          '<h2>Why they belong together</h2>'
          '<p>Take one example that comes up every year. A restaurant buys a walk-in cooler in November. '
          'The bookkeeper has to decide whether it is an expense or an asset. If it is coded as a repair, '
          'the profit and loss for the year is wrong and the depreciation schedule never learns the cooler '
          'exists. If it is capitalised, there is a decision to make on the return about how fast to write '
          'it off, and that decision interacts with the owner&rsquo;s personal return, the estimated '
          'payments already made, and whether the year is unusually good or unusually bad.</p>'
          '<p>Three providers make that a game of telephone. One person makes it a two-minute conversation '
          'in November, which is when it can still be influenced.</p>'
          '<h3>The seams that cost money</h3>'
          '<ul>'
          '<li><strong>Payroll filed away from the ledger.</strong> The gross wage, the employer share and '
          'the withholding held all have to land in the books. When they do not, labour cost is wrong all '
          'year and the year-end adjustment is a nasty surprise.</li>'
          '<li><strong>Books kept without knowing the return.</strong> Categories that make sense to a '
          'bookkeeper can be useless on a tax form &mdash; meals, entertainment, owner draws and '
          'improvements are the usual casualties.</li>'
          '<li><strong>A return prepared from numbers nobody questioned.</strong> A preparer who meets the '
          'books in March has two options: file what he is given, or start asking questions with a deadline '
          'in the way. Neither is a good position.</li>'
          '</ul>'
          '<h2>Where to start</h2>'
          '<p>Most engagements begin with one urgent thing &mdash; a return that is due, a payroll that has '
          'to run, books that have to be caught up &mdash; and expand once the urgent thing is handled. '
          'That is a sensible order. Call and describe the urgent thing.</p>'),
        _call_card()
        + _pay_card()
        + _acard('Specialisms', _links([
            ('../restaurant-accounting.html', 'Quick-serve restaurants'),
            ('../rental-property-accounting.html', 'Rental real estate'),
            ('../calculators/index.html', 'Financial calculators'),
            ('../about.html', 'About Scott Marchlik')]), light=True)), cls='sec tint')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Services', BASE + 'services/')]),
                   {"@context": "https://schema.org", "@type": "ItemList",
                    "name": "Mill City Accounting Services",
                    "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                         "name": _plain(s['nav_title']),
                                         "url": BASE + 'services/' + s['slug'] + '.html'}
                                        for i, s in enumerate(SERVICES)]}]
    P.append(p)

    for s in SERVICES:
        P.append(_service_page(s))

    # ------------------------------------------------------------ RESTAURANTS
    r_faqs = [
      ("My POS gives me a sales report. Is that not enough?",
       "<p>It is the raw material, not the accounting. A POS report tells you what was rung in. It does not reconcile to what reached the bank, it does not separate the meals tax you are holding for the Commonwealth from your own revenue, and it does not account for what a delivery platform kept before remitting. The daily journal entry is what turns the report into books.</p>"),
      ("The delivery apps deposit a net figure. Why does that matter?",
       "<p>Because the gross sale is your sale. Booking only the deposit understates revenue, hides the commission you are paying as a cost, and can misstate the tax you are responsible for. It also means you have no idea what the platforms actually cost you as a percentage &mdash; which is the number you need before you decide whether to stay on them.</p>"),
      ("How often do I have to file meals tax?",
       "<p>On the schedule the Department of Revenue assigns you, which depends on how much you collect. It is a separate filing from your income tax return and it has its own deadlines and its own penalties. The safest habit is to treat collected tax as money that was never yours.</p>"),
      ("What is prime cost and why does everyone talk about it?",
       "<p>Food and paper cost plus total labour cost, as a percentage of sales. It is the pair of numbers you can actually control week to week, and it moves faster than anything else on the profit and loss. Rent is fixed; prime cost is a decision you make every day.</p>"),
      ("We take a lot of cash. What is the right way to handle it?",
       "<p>Record it all, deposit it all, and pay wages through payroll. Cash that never reaches the books cannot be defended in an examination, distorts every ratio you would otherwise manage by, and reduces what the business is worth if you ever sell it &mdash; a buyer values the reported number.</p>"),
    ]
    p = dict(path='restaurant-accounting.html', depth=0, nav='restaurants', cta_args=(
        'Talk to somebody who has seen your P&L before.',
        'Call the office or write to scott@millcityaccounting.com. Bring a month of POS reports and a '
        'bank statement, and the conversation will be about your numbers rather than about accounting.'),
        title='Restaurant Accounting in Lowell, MA | Mill City',
        desc='Bookkeeping, payroll and tax work for quick-serve restaurant owners: daily sales journals, meals tax, tipped payroll, delivery-app settlements and prime cost.',
        eyebrow='Quick-serve restaurants', h1='Quick-serve restaurants have a different set of books.',
        sub='High volume, small tickets, cash and cards mixed, tipped staff, tax collected on every sale, and three delivery platforms all remitting differently. Generic bookkeeping does not survive it.')
    p['body'] = phero(p, [('Quick-serve restaurants', None)]) + _sec(_split(
        _prose(
          '<h2>The short answer</h2>'
          '<p>Quick-serve restaurant owners were the largest part of Scott&rsquo;s clientele in the years '
          'before he opened Mill City. It is the environment he learned the work in, and the shape of the '
          'job is specific: bookkeeping built around '
          'a daily sales journal, payroll that handles tipped staff correctly, meals tax filed on its own '
          'calendar, and a return that reflects all of it.</p>'

          '<h2>Why the books look different</h2>'
          '<h3>The daily sales journal</h3>'
          '<p>A restaurant does not have invoices. It has a day. The correct unit of bookkeeping is one '
          'journal entry per day, built from the POS close, and it has more lines than owners expect:</p>'
          '<ul>'
          '<li>Gross sales, split by the categories you want to manage &mdash; food, beverage, retail</li>'
          '<li>Meals tax collected, which is a liability and not revenue</li>'
          '<li>Discounts, comps and voids, recorded rather than netted away</li>'
          '<li>Tips collected on cards, which are payable to staff and not yours</li>'
          '<li>Card settlements as a receivable until the deposit lands</li>'
          '<li>Cash counted, cash deposited, and the difference &mdash; over/short is a control, and a '
          'restaurant that never records one is not counting</li>'
          '</ul>'
          '<p>Get this entry right and everything downstream works. Get it wrong and every ratio you try '
          'to manage by is built on sand.</p>'

          '<h3>The deposit never matches the sales</h3>'
          '<p>It never will, and that is normal: card batches settle a day or two late, processors take '
          'fees gross or net depending on the contract, chargebacks appear weeks later, and cash goes to '
          'the bank when somebody has time. The reconciliation is the work. A restaurant whose bank '
          'account is reconciled monthly finds a skimming problem or a duplicated vendor payment in weeks. '
          'One that is not finds it in years, if ever.</p>'

          '<h3>Third-party delivery is a gross-and-net problem</h3>'
          '<p>The platforms deposit a net figure: your sale, minus commission, sometimes minus marketing, '
          'sometimes with tax handled by the platform and sometimes not, depending on the arrangement. If '
          'you book the deposit as revenue, three things go wrong at once. Sales are understated. '
          'Commission &mdash; frequently the largest single cost increase a small restaurant has taken on '
          'in a decade &mdash; is invisible, so nobody can decide whether it is worth it. And the tax '
          'treatment of the sale is unexamined. The right way is to record the gross sale, the commission '
          'as an expense, the tax as a liability or as remitted by the platform, and then reconcile to the '
          'deposit.</p>'
          '<p>You should also expect a Form 1099-K from processors and platforms. It reports gross, which '
          'will not match your deposits &mdash; and if your books were built from deposits, you have a '
          'reconciliation to explain.</p>'

          '<h2>The numbers worth watching</h2>'
          '<table class="plain">'
          '<tr><th>Number</th><th>What it is</th><th>Why it moves</th></tr>'
          '<tr><td>Food and paper cost %</td><td>Cost of what you sold, over sales</td><td>Supplier price rises, portion drift, waste, theft, menu mix</td></tr>'
          '<tr><td>Labour cost %</td><td>All wages and payroll taxes, over sales</td><td>Scheduling against forecast volume, overtime, minimum-wage changes</td></tr>'
          '<tr><td>Prime cost</td><td>The two above, added</td><td>The pair you control weekly; watch it weekly, not monthly</td></tr>'
          '<tr><td>Break-even covers</td><td>Volume needed to cover fixed costs</td><td>Rent, insurance, salaried staff, debt service</td></tr>'
          '<tr><td>Average check</td><td>Sales divided by transactions</td><td>Menu pricing, upsell, delivery mix</td></tr>'
          '</table>'
          '<p>The <a href="calculators/break-even.html">break-even calculator</a> on this site works for a '
          'restaurant if you treat the &ldquo;unit&rdquo; as an average check and put food and paper cost '
          'per check into the variable field.</p>'

          '<h2>Meals tax</h2>'
          '<p>Massachusetts taxes prepared food and meals at a state rate, and cities and towns may adopt '
          'an additional local option on top of it &mdash; so the rate that applies to you depends on '
          'where the restaurant is. Confirm the combined rate for your location rather than assuming it '
          'is the same as the next town over.</p>'
          '<p>Whatever the rate, the money is not yours. It is collected on behalf of the Commonwealth, '
          'sits as a liability on the balance sheet, and is remitted on a schedule the Department of '
          'Revenue assigns based on volume. The failure mode is always the same: a slow month, the tax '
          'account gets used for payroll, and the shortfall compounds with penalties. Books that keep the '
          'liability visible make that much harder to do by accident.</p>'

          '<h2>Payroll with tipped staff</h2>'
          '<p>This is where the money is lost. Massachusetts allows a lower service rate for tipped '
          'employees, but only where tips actually bring the employee to at least full minimum wage &mdash; '
          'tested on the shift, so a slow Tuesday is not rescued by a busy Friday, and the employer owes '
          'the difference when it falls short. Tips are wages and have to run through payroll records. Tip '
          'pools have rules about who may participate. And employers of tipped staff may be eligible for a '
          'federal credit on the Social Security and Medicare tax paid on reported tips &mdash; which is '
          'only claimable if the payroll records support it.</p>'
          '<p>The detail is on the <a href="services/payroll.html">payroll page</a>.</p>'

          '<div class="callout"><p><strong>Paying kitchen staff in cash is the most expensive habit in the '
          'industry.</strong> It creates unreported wages, uninsured workers, a books-to-bank gap that '
          'cannot be explained, and a business that is worth less when you sell it, because a buyer pays '
          'for the reported number. There is no version of this that is cheaper once it goes wrong.</p></div>'

          '<h2>Equipment, build-out and the lease</h2>'
          '<p>Fryers, hoods, walk-ins, POS hardware and the build-out itself are assets, not expenses, and '
          'the write-off choices available in the year of purchase are genuinely valuable &mdash; but only '
          'if the purchase is on the depreciation schedule and only if the business has income to absorb '
          'the deduction. Leasehold improvements have their own treatment and their own trap: they follow '
          'the lease, so what happens at renewal or on exit matters. Ask before the purchase order, not '
          'after. The <a href="calculators/loan-payment.html">loan calculator</a> covers the financing '
          'side.</p>'

          '<h2>What Scott does for a restaurant client</h2>'
          '<ul>'
          '<li>Sets up a chart of accounts that separates food, paper, beverage and supplies, so a food '
          'cost percentage is computable</li>'
          '<li>Builds the daily sales journal from your POS close and reconciles it to the bank</li>'
          '<li>Books delivery-platform activity gross, with commission visible as a cost</li>'
          '<li>Runs payroll, including the service rate, the make-up obligation and tip reporting</li>'
          '<li>Files meals tax on schedule and keeps the liability visible on the balance sheet</li>'
          '<li>Maintains the depreciation schedule for equipment and build-out</li>'
          '<li>Prepares the business return and the owner&rsquo;s personal return together</li>'
          '</ul>'
          '<h2>Common questions</h2>' + faq_html(r_faqs)),
        _call_card('Bring a month of POS reports and a bank statement. The first conversation is about '
                   'your numbers, not about accounting.')
        + _pay_card()
        + _acard('For restaurants', _links([
            ('services/payroll.html', 'Tipped payroll'),
            ('services/bookkeeping.html', 'Daily sales bookkeeping'),
            ('services/tax-preparation.html', 'Business tax returns'),
            ('calculators/break-even.html', 'Break-even calculator'),
            ('calculators/loan-payment.html', 'Equipment loan calculator')]), light=True)))
    p['schema'] = [_org(),
                   breadcrumb_schema([('Home', BASE), ('Quick-serve restaurants',
                                                       BASE + 'restaurant-accounting.html')]),
                   _svc_schema('Restaurant accounting',
                               'Bookkeeping, payroll and tax preparation for quick-serve restaurant owners in Lowell, Massachusetts.',
                               BASE + 'restaurant-accounting.html'),
                   _faq_ld(r_faqs)]
    P.append(p)

    # ------------------------------------------------------------ RENTALS
    l_faqs = [
      ("I replaced the roof. Is that a repair?",
       "<p>Almost certainly not. A new roof restores a major component of the building and is normally capitalised and depreciated rather than deducted in the year you paid for it. Patching a section of the same roof after a storm usually is a repair. The distinction is about whether the work restores or betters the property, not about how the invoice is worded.</p>"),
      ("My rentals show a loss. Can I use it against my salary?",
       "<p>Sometimes, partly, or not at all. Rental activity is generally passive, and passive losses are limited. There is a special allowance for actively participating owners that phases out as income rises, and different rules again for people whose work genuinely qualifies them as real estate professionals. Losses you cannot use are not lost &mdash; they are suspended and carry forward, frequently to the year you sell.</p>"),
      ("I live in one unit of my three-family. How is that handled?",
       "<p>The building is split between personal use and rental use on a defensible basis &mdash; square footage or unit count, applied consistently. Rental-side expenses and depreciation follow the rental portion; your own unit's mortgage interest and property tax are treated the way any homeowner's would be. The allocation basis has to stay the same year to year, so it is worth setting it correctly at the start.</p>"),
      ("Do I need a separate bank account for each property?",
       "<p>Separate from your personal money, without question. Separate per property is better once there are several, because it makes the per-property figures fall out of the statements instead of having to be reconstructed. Security deposits are a different question &mdash; Massachusetts has specific requirements about how those are held.</p>"),
      ("What happens to depreciation when I sell?",
       "<p>It comes back. Depreciation you claimed reduces your basis, so it increases the gain on sale, and a portion is taxed under recapture rules at its own rate. This is not a reason to skip depreciation &mdash; the recapture is calculated on the depreciation you were allowed, whether or not you actually claimed it. Skipping it means paying twice.</p>"),
    ]
    p = dict(path='rental-property-accounting.html', depth=0, nav='rentals', cta_args=(
        'Talk through the building before you buy it.',
        'Call the office or write to scott@millcityaccounting.com. Bring the numbers on the property and '
        'the conversation will be about whether it works, not about accounting theory.'),
        title='Rental Property Accounting, Lowell MA | Mill City',
        desc='Accounting and tax work for Massachusetts landlords: Schedule E by property, repairs versus improvements, depreciation, passive loss rules and security deposit requirements.',
        eyebrow='Rental real estate', h1='Rental property is an accounting problem before it is an investment.',
        sub='Owners of rental real estate were the other half of Scott&rsquo;s client base before he opened Mill City. The mistakes are consistent, and almost all of them are made in the first year.')
    p['body'] = phero(p, [('Rental real estate', None)]) + _sec(_split(
        _prose(
          '<h2>The short answer</h2>'
          '<p>Mill City keeps the books and prepares the returns for owners of rental property &mdash; '
          'the two- and three-family houses that make up so much of Lowell and the Merrimack Valley, and '
          'the small multi-family and mixed-use buildings above them. The work is per-property '
          'recordkeeping, a defensible line between repairs and improvements, a depreciation schedule '
          'that is actually maintained, and a return that survives being looked at.</p>'

          '<h2>One set of records per property</h2>'
          '<p>Federal rental income and expense is reported property by property, so books that pool three '
          'buildings into one column have to be taken apart before anything can be filed. Worse, pooled '
          'books hide the thing you most need to know: which building is carrying the others. Separate '
          'the income, the expenses, the mortgage, the insurance and the capital work from the day you '
          'buy, and both problems disappear.</p>'

          '<h2>Repairs versus improvements &mdash; the question that costs the most</h2>'
          '<p>A repair is deducted now. An improvement is capitalised and written off over years. Owners '
          'consistently guess in their own favour, and it is the most commonly adjusted item on a small '
          'landlord&rsquo;s return.</p>'
          '<p>The rough shape of the rule: work that keeps the property in its ordinary operating '
          'condition tends to be a repair. Work that betters it, restores a major component, or adapts it '
          'to a new use tends to be an improvement. Fixing a section of failed roof after a storm is one '
          'thing; a whole new roof is another. Replacing a broken window is a repair; replacing every '
          'window in the building is not.</p>'
          '<h3>The safe harbours are worth knowing</h3>'
          '<p>There are elections that let smaller purchases be expensed rather than capitalised, and a '
          'safe harbour aimed at buildings owned by smaller taxpayers. They have dollar thresholds, they '
          'have to be elected properly, and some of them require an accounting policy to be in place '
          '<em>before</em> the year starts. That is a conversation to have in December, not in April.</p>'

          '<h2>Depreciation, done once, properly</h2>'
          '<p>The building depreciates. The land does not, so the purchase price has to be allocated '
          'between them on a supportable basis at the moment you buy &mdash; commonly with reference to '
          'the assessment, and documented at the time. Certain closing costs are added to basis rather '
          'than deducted; certain loan costs are amortised separately. Appliances and improvements have '
          'their own lives and their own start dates.</p>'
          '<p>All of that is set up once, in year one, and then carried for as long as you own the '
          'property. A schedule set up badly is carried badly for decades, and it surfaces on '
          'the day you sell.</p>'
          '<p>Note also that Massachusetts does not necessarily give you the same write-off in the same '
          'year as the federal return. Where the two diverge, two sets of records have to be kept for the '
          'life of the asset.</p>'

          '<h2>When a loss is not a loss</h2>'
          '<p>Rental activities are generally passive, and passive losses cannot simply be netted against '
          'wages. There is a special allowance for owners who actively participate in the activity, and it '
          'phases out as income rises. There is a separate and much stricter set of tests for people whose '
          'work qualifies them as real estate professionals, and claiming that status without the hours '
          'and the records to support it is a bad idea.</p>'
          '<p>Losses that are limited are suspended rather than lost. They carry forward, and they '
          'commonly become useful in the year the property is sold. That makes the carryforward schedule '
          'a document worth keeping accurately, because nobody else will reconstruct it for you.</p>'

          '<h2>Massachusetts particulars</h2>'
          '<h3>Security deposits and last month&rsquo;s rent</h3>'
          '<p>Massachusetts regulates security deposits tightly. A deposit is the tenant&rsquo;s money, '
          'held under specific requirements about where and how it is kept, with interest and accounting '
          'obligations attached, and the penalties for getting it wrong are severe. From an accounting '
          'point of view the consequence is simple: a security deposit is a liability on your balance '
          'sheet and is not rental income when you receive it. Last month&rsquo;s rent is treated '
          'differently again. The legal side of this belongs with an attorney; the bookkeeping side '
          'belongs here, and the two have to agree.</p>'
          '<h3>Local reality</h3>'
          '<p>Lowell&rsquo;s housing stock is dominated by two- and three-family houses, much of it old, '
          'much of it in the middle of expensive systems work &mdash; heating, knob-and-tube, roofs, '
          'porches. That means the repair-versus-improvement question is not academic here. It is the '
          'main event, several times a year.</p>'

          '<h2>The owner-occupied two- or three-family</h2>'
          '<p>The most common Lowell case, and the one most often filed wrong. The building has to be '
          'split between the part you live in and the part you rent, on a basis you can defend &mdash; '
          'square footage or unit count &mdash; and used consistently. Rental-side expenses and '
          'depreciation follow the rental fraction. Your own unit is a home: mortgage interest and '
          'property tax on that share follow the ordinary homeowner rules. Shared costs get allocated. '
          'Work done only inside your own unit is not a rental expense at all, however much it improves '
          'the building.</p>'

          '<h2>When you sell</h2>'
          '<p>The gain is not the difference between what you paid and what you sold for. It is measured '
          'against adjusted basis: purchase price, plus capital improvements, plus certain closing costs, '
          'minus all the depreciation you were allowed to claim. Depreciation comes back as recapture at '
          'its own rate. Suspended passive losses generally free up. A like-kind exchange can defer the '
          'gain, but it has strict deadlines that start running at the closing, so it has to be planned '
          'before the property goes under agreement rather than after.</p>'
          '<p>And in Massachusetts, a large gain in one year can push an otherwise ordinary year over the '
          'threshold for the surtax on high income. That is a modelling exercise, and it is worth doing '
          'before you sign.</p>'

          '<h2>What Scott does for a landlord client</h2>'
          '<ul>'
          '<li>Sets up per-property books, with capital work separated from repairs as it happens</li>'
          '<li>Allocates purchase price between land and building, documented at the time</li>'
          '<li>Builds and maintains the depreciation schedule, including the Massachusetts differences</li>'
          '<li>Tracks security deposits as liabilities, not as income</li>'
          '<li>Handles the personal and rental split on an owner-occupied multi-family</li>'
          '<li>Keeps the suspended passive loss carryforward accurate year to year</li>'
          '<li>Prepares the return, and models a sale before it happens rather than after</li>'
          '</ul>'
          '<p>If you are looking at a building, the <a href="calculators/mortgage-payment.html">mortgage '
          'payment calculator</a> will give you the debt service. Add taxes, insurance, water, an honest '
          'maintenance allowance and a vacancy allowance before you compare it to rent.</p>'
          '<h2>Common questions</h2>' + faq_html(l_faqs)),
        _call_card('Buying, refinancing or selling a building is worth a phone call first. Most of the '
                   'expensive mistakes are made before the closing.')
        + _pay_card()
        + _acard('For landlords', _links([
            ('calculators/mortgage-payment.html', 'Mortgage payment calculator'),
            ('services/tax-preparation.html', 'Tax preparation'),
            ('services/bookkeeping.html', 'Per-property bookkeeping'),
            ('services/notary-services.html', 'Notarization'),
            ('faq.html', 'Common questions')]), light=True)))
    p['schema'] = [_org(),
                   breadcrumb_schema([('Home', BASE), ('Rental real estate',
                                                       BASE + 'rental-property-accounting.html')]),
                   _svc_schema('Rental property accounting',
                               'Bookkeeping and tax preparation for owners of rental real estate in Lowell and the Merrimack Valley, Massachusetts.',
                               BASE + 'rental-property-accounting.html'),
                   _faq_ld(l_faqs)]
    P.append(p)

    # ------------------------------------------------------------ FAQ
    p = dict(path='faq.html', depth=0, nav='about', cta_args=CTA,
        title='Common Questions | Mill City Accounting, Lowell MA',
        desc='Straight answers about working with a one-person accounting firm in Lowell: who does the work, what to bring, catch-up bookkeeping, notary visits and paying an invoice.',
        eyebrow='Answers', h1='Questions people ask on the first call.',
        sub='If yours is not here, call and ask it. There is no queue and no form to fill in first.')
    p['body'] = phero(p, [('Common questions', None)]) + _sec(
        _head('Working with Mill City',
              'How the firm operates, what things cost, and what to bring.')
        + faq_html(FAQS)
        + '<div class="sec-head reveal" style="margin-top:56px"><h2>Still deciding?</h2>'
          '<p class="lead">Two pages go into more depth than a paragraph allows: '
          '<a href="restaurant-accounting.html">quick-serve restaurant accounting</a> and '
          '<a href="rental-property-accounting.html">rental property accounting</a>. There are also '
          '<a href="calculators/index.html">four working calculators</a> if you would rather start with '
          'numbers than with a phone call.</p></div>')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Common questions', BASE + 'faq.html')]),
                   _faq_ld(FAQS)]
    P.append(p)

    # ------------------------------------------------------------ CONTACT
    p = dict(path='contact.html', depth=0, nav='contact', cta_args=CTA,
        title='Contact Mill City Accounting | Lowell, Massachusetts',
        desc='Mill City Accounting Services, 10 Kearney Square, Suite 302, Lowell MA. Call (978) 979-2904. Monday to Friday 9 to 5, Saturday by appointment. Map and directions.',
        eyebrow='Contact', h1='Call the office. Scott picks up.',
        sub='Tell him what you are working through and you will get a straight answer about whether it is work he should take on.')
    p['body'] = phero(p, [('Contact', None)]) + _sec(
        _head('10 Kearney Square, Suite 302, Lowell',
              'One office, in downtown Lowell, where Merrimack, Bridge and Central streets converge.')
        + _split('<div>' + gmap('Pan, zoom, or open the map full screen for turn-by-turn directions.') + '</div>',
                 _acard('Office &amp; hours',
                        '<p>' + FIRM['addr'] + '<br>' + FIRM['city'] + ', ' + FIRM['state'] + ' ' + FIRM['zip'] + '</p>'
                        '<p>Telephone ' + FIRM['ph'] + '<br>Facsimile ' + FIRM['fax'] + '<br>' + FIRM['email'] + '</p>'
                        '<p>Monday&ndash;Friday, 9:00 AM&ndash;5:00 PM<br>Saturday by appointment<br>Closed Sunday</p>'
                        '<a class="btn b-acc" href="tel:' + FIRM['tel'] + '">Call ' + FIRM['ph'] + '</a>')
                 + _pay_card()
                 + _acard('Quick links', _links([
                     (FIRM['maps'], 'Directions in Google Maps'),
                     ('mailto:' + FIRM['email'], FIRM['email']),
                     ('services/notary-services.html', 'Notarization &mdash; call first'),
                     ('faq.html', 'Common questions')]), light=True))) + _sec(_split(
        _prose(
          '<h2>What a first call is like</h2>'
          '<p>Short. What kind of entity, roughly what the year looks like, and what deadline is driving '
          'the question. From that it is usually clear whether the work is a return, a set of books, a '
          'payroll problem or some combination &mdash; and roughly what it involves.</p>'
          '<p>If it belongs somewhere else, you will be told that. A one-person firm has a finite amount '
          'of time, and taking on work that should go elsewhere serves nobody.</p>'

          '<h2>What to have handy</h2>'
          '<ul>'
          '<li>The most recently filed return, business or personal</li>'
          '<li>Your books, in whatever state they are in &mdash; including no state at all</li>'
          '<li>Anything with a date on it: an agency notice, a lender&rsquo;s request, a purchase and '
          'sale agreement, a lease</li>'
          '<li>For a restaurant: a month of POS reports and the matching bank statement</li>'
          '<li>For a rental: the closing statement, the mortgage statement, and last year&rsquo;s '
          'Schedule E</li>'
          '</ul>'
          '<p>Missing pieces are normal. Bring what exists.</p>'

          '<h2>Hours, and why calling ahead helps</h2>'
          '<p>The office keeps regular hours Monday to Friday, 9:00 AM to 5:00 PM, with Saturday '
          'appointments available and Sunday closed. Because this is one accountant in one office, a call '
          'before you drive in is worth the two minutes &mdash; particularly for '
          '<a href="services/notary-services.html">notarization</a>, which needs him physically present.</p>'

          '<h2>Paying an invoice</h2>'
          '<p>Mill City takes card payments through Square. '
          '<a href="' + PAY + '" target="_blank" rel="noopener">The payment link</a> opens a secure '
          'Square checkout page; you do not need a Square account to use it.</p>'

          '<h2>Confidentiality</h2>'
          '<p>Client information stays with the firm &mdash; including the fact that you called.</p>'),
        _call_card()
        + _acard('Before you come in', _links([
            ('faq.html', 'What to bring'),
            ('services/index.html', 'All services'),
            ('restaurant-accounting.html', 'Restaurant owners'),
            ('rental-property-accounting.html', 'Landlords'),
            ('about.html', 'About Scott Marchlik')]), light=True)), cls='sec tint')
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Contact', BASE + 'contact.html')]),
                   {"@context": "https://schema.org", "@type": "ContactPage",
                    "name": "Contact Mill City Accounting Services LLC",
                    "url": BASE + 'contact.html'}]
    P.append(p)

    # ------------------------------------------------------------ CALCULATOR HUB
    cc = ''.join(
        '<a class="calccard reveal" href="' + c['slug'] + '.html">'
        '<div class="cc">' + CALC_BY_SLUG[c['slug']]['cat'] + '</div>'
        '<h3>' + CALC_BY_SLUG[c['slug']]['title'] + '</h3>'
        '<p>' + CALC_BY_SLUG[c['slug']]['blurb'] + '</p></a>'
        for c in CALC_PICK)
    p = dict(path='calculators/index.html', depth=1, nav='calculators', cta_args=CTA,
        title='Financial Calculators | Mill City Accounting, Lowell',
        desc='Four working calculators for small business owners and landlords: mortgage payment, loan payoff, break-even point and self-employment tax. No sign-up and no third-party site.',
        eyebrow='Calculators', h1='Four calculators, running on this page.',
        sub='They work in your browser. Nothing is sent anywhere, nothing is stored, and you are not handed off to somebody else&rsquo;s website to use them.')
    p['body'] = phero(p, [('Calculators', None)]) + (
        '<style>' + C.CALC_CSS + '</style>'
        + _sec(_head('Chosen for the people Mill City works with',
                     'A landlord looking at a building, an owner deciding whether to finance a piece of '
                     'equipment, a restaurant working out how many covers a week it has to do, and '
                     'anybody in their first year of self-employment.')
               + '<div class="calcgrid">' + cc + '</div>')
        + _sec(_split(
            _prose(
              '<h2>A calculator is a starting point, not an answer</h2>'
              '<p>Every one of these makes assumptions, and each page says which ones. They hold rates '
              'constant, they ignore the parts of your situation they cannot see, and they do not know '
              'what else is on your return. Treat the output as the beginning of a question.</p>'
              '<h3>Why they run here rather than somewhere else</h3>'
              '<p>Financial calculators on accounting websites are usually a licensed widget hosted by a '
              'vendor: the click leaves the firm&rsquo;s site, the numbers you type go to a third party, '
              'and the whole thing disappears the day the firm changes providers. These are part of the '
              'site. They work offline, they set no cookies, and they make no network calls.</p>'
              '<h3>Where to go from a number</h3>'
              '<p>If the break-even figure is higher than the restaurant is doing, the next conversation '
              'is about food cost and labour, not about the calculator &mdash; see '
              '<a href="../restaurant-accounting.html">quick-serve restaurants</a>. If the mortgage '
              'payment works but you are unsure what the tax return will look like, see '
              '<a href="../rental-property-accounting.html">rental property</a>. And if the '
              'self-employment tax figure was a shock, that is exactly the call worth making early in '
              'the year rather than in April.</p>'),
            _call_card()
            + _acard('The calculators', _links(
                [(c['slug'] + '.html', CALC_BY_SLUG[c['slug']]['title']) for c in CALC_PICK]
                + [('../services/index.html', 'All services')]), light=True)), cls='sec tint'))
    p['schema'] = [_org(), breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/')]),
                   {"@context": "https://schema.org", "@type": "ItemList",
                    "name": "Mill City Accounting calculators",
                    "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                         "name": CALC_BY_SLUG[c['slug']]['title'],
                                         "url": BASE + 'calculators/' + c['slug'] + '.html'}
                                        for i, c in enumerate(CALC_PICK)]}]
    P.append(p)

    # ------------------------------------------------------------ CALCULATOR PAGES
    for c in CALC_PICK:
        calc = CALC_BY_SLUG[c['slug']]
        url = BASE + 'calculators/' + c['slug'] + '.html'
        p = dict(path='calculators/' + c['slug'] + '.html', depth=1, nav='calculators',
                 title=c['title'], desc=c['desc'], eyebrow=c['eyebrow'], h1=c['h1'],
                 sub=c['sub'], cta_args=CTA)
        ph = phero(p, [('Calculators', 'calculators/index.html'), (calc['title'], None)])
        others = [(o['slug'] + '.html', CALC_BY_SLUG[o['slug']]['title'])
                  for o in CALC_PICK if o['slug'] != c['slug']]
        p['body'] = ('<style>' + C.CALC_CSS + '</style>'
                     + C.calc_page_body(calc, ph, rel, ARROW, depth=1)
                     + _sec(_split(_prose(c['why']),
                                   _call_card()
                                   + _acard('Other calculators', _links(others), light=True)
                                   + _acard('Related reading', _links([
                                       ('../restaurant-accounting.html', 'Quick-serve restaurants'),
                                       ('../rental-property-accounting.html', 'Rental property'),
                                       ('../services/index.html', 'All services')]), light=True)),
                            cls='sec tint')
                     + C.CALC_JS)
        p['schema'] = [_org(),
                       breadcrumb_schema([('Home', BASE), ('Calculators', BASE + 'calculators/'),
                                          (calc['title'], url)]),
                       {"@context": "https://schema.org", "@type": "WebApplication",
                        "name": calc['title'], "description": calc['blurb'], "url": url,
                        "applicationCategory": "FinanceApplication",
                        "operatingSystem": "Any modern web browser",
                        "isAccessibleForFree": True,
                        "publisher": {"@id": ORG}}]
        P.append(p)

    return P
