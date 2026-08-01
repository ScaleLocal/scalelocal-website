# -*- coding: utf-8 -*-
"""
Native financial calculators.

Why these exist: every calculator on every one of the six audited firm sites is a
vendor-licensed widget on the VENDOR's account — CalcXML skin 481 (Hickey, Mass Tax
Pros) or cchwebsites.com (Carella). None of it transfers when the firm leaves the
vendor, and the click currently hands the visitor to a third-party domain with the
firm's branding nowhere in sight.

These run on the firm's own page. No iframe, no third-party script, no network call,
no cookies. They are indexable, they work offline, and they survive a vendor change.

Each calculator is declared as data: inputs, a pure JS expression body that returns
an object of outputs, and output formatting. The shared runtime handles parsing,
live recalculation, number formatting, and accessible announcement of results.
"""

MONEY = 'money'
PCT = 'pct'
NUM = 'num'
YEARS = 'years'


def _f(id, label, kind, default, hint=None, step=None, min=None, max=None):
    return dict(id=id, label=label, kind=kind, default=default, hint=hint,
                step=step, min=min, max=max)


def _o(id, label, primary=False, kind=MONEY, note=None):
    return dict(id=id, label=label, primary=primary, kind=kind, note=note)


CALCULATORS = [

    # ---------------------------------------------------------------- mortgage
    dict(
        slug='mortgage-payment', cat='Home & mortgage',
        title='Monthly mortgage payment',
        blurb='Principal, interest, taxes and insurance on a fixed-rate loan, plus the total interest over the life of the note.',
        inputs=[
            _f('price', 'Purchase price', MONEY, 450000, step=1000),
            _f('down', 'Down payment', MONEY, 90000, step=1000),
            _f('rate', 'Interest rate', PCT, 6.5, step=0.05),
            _f('term', 'Term', YEARS, 30, step=1, min=1, max=50),
            _f('tax', 'Annual property tax', MONEY, 6800, step=100),
            _f('ins', 'Annual homeowner insurance', MONEY, 1800, step=100),
        ],
        js='''
var P = Math.max(price - down, 0);
var i = rate / 100 / 12, n = term * 12;
var pi = (i === 0) ? (n ? P / n : 0) : P * i / (1 - Math.pow(1 + i, -n));
var esc = (tax + ins) / 12;
return {
  total: pi + esc,
  pi: pi,
  esc: esc,
  principal: P,
  interest: pi * n - P,
  ltv: P > 0 && price > 0 ? (P / price) * 100 : 0
};''',
        outputs=[
            _o('total', 'Monthly payment (PITI)', primary=True),
            _o('pi', 'Principal & interest'),
            _o('esc', 'Taxes & insurance, monthly'),
            _o('principal', 'Amount financed'),
            _o('interest', 'Total interest over the term'),
            _o('ltv', 'Loan-to-value', kind=PCT,
               note='Above 80% you should expect to pay mortgage insurance.'),
        ],
        note='Excludes mortgage insurance, HOA dues and closing costs. Escrow is shown at one twelfth of the annual figures you enter.',
    ),

    # ---------------------------------------------------------------- refinance
    dict(
        slug='refinance-breakeven', cat='Home & mortgage',
        title='Refinance break-even',
        blurb='How many months of lower payments it takes to earn back what the refinance costs you.',
        inputs=[
            _f('bal', 'Current balance', MONEY, 320000, step=1000),
            _f('oldrate', 'Current rate', PCT, 7.25, step=0.05),
            _f('oldleft', 'Years left on current loan', YEARS, 26, step=1, min=1, max=50),
            _f('newrate', 'New rate', PCT, 6.0, step=0.05),
            _f('newterm', 'New term', YEARS, 30, step=1, min=1, max=50),
            _f('costs', 'Closing costs', MONEY, 6500, step=250),
        ],
        js='''
function pmt(P, r, yrs){ var i = r/100/12, n = yrs*12;
  return i === 0 ? (n ? P/n : 0) : P*i/(1-Math.pow(1+i,-n)); }
var oldPmt = pmt(bal, oldrate, oldleft);
var newPmt = pmt(bal, newrate, newterm);
var save = oldPmt - newPmt;
var months = save > 0 ? costs / save : 0;
return {
  months: months,
  oldPmt: oldPmt,
  newPmt: newPmt,
  save: save,
  oldTotal: oldPmt * oldleft * 12,
  newTotal: newPmt * newterm * 12 + costs
};''',
        outputs=[
            _o('months', 'Months to break even', primary=True, kind=NUM,
               note='If you expect to sell or refinance again before this point, the refinance loses money.'),
            _o('save', 'Monthly saving'),
            _o('oldPmt', 'Current payment'),
            _o('newPmt', 'New payment'),
            _o('oldTotal', 'Total remaining on current loan'),
            _o('newTotal', 'Total on new loan, including costs'),
        ],
        note='Compares principal and interest only. Extending the term lowers the payment while often raising lifetime interest — look at the two totals, not just the monthly saving.',
    ),

    # ---------------------------------------------------------------- loan
    dict(
        slug='loan-payment', cat='Loans & credit',
        title='Loan payment and payoff',
        blurb='Payment, total interest, and what an extra monthly amount does to the payoff date.',
        inputs=[
            _f('amt', 'Loan amount', MONEY, 40000, step=500),
            _f('rate', 'Interest rate', PCT, 8.9, step=0.05),
            _f('term', 'Term', YEARS, 5, step=1, min=1, max=40),
            _f('extra', 'Extra payment each month', MONEY, 0, step=25),
        ],
        js='''
var i = rate/100/12, n = term*12;
var base = i === 0 ? (n ? amt/n : 0) : amt*i/(1-Math.pow(1+i,-n));
var pay = base + extra, bal = amt, months = 0, paid = 0;
while (bal > 0.01 && months < 1200) {
  var interest = bal * i;
  var principal = Math.min(pay - interest, bal);
  if (principal <= 0) { months = 0; break; }
  bal -= principal; paid += interest; months++;
}
return {
  base: base, pay: pay, months: months,
  saved: (base*n - amt) - paid,
  interest: paid,
  early: n - months
};''',
        outputs=[
            _o('pay', 'Total monthly payment', primary=True),
            _o('base', 'Scheduled payment'),
            _o('interest', 'Total interest paid'),
            _o('months', 'Months to pay off', kind=NUM),
            _o('early', 'Months saved by paying extra', kind=NUM),
            _o('saved', 'Interest saved by paying extra'),
        ],
        note='Assumes the extra payment is applied to principal every month and the rate is fixed.',
    ),

    # ---------------------------------------------------------------- retirement
    dict(
        slug='retirement-savings', cat='Retirement',
        title='What my retirement account will be worth',
        blurb='Projected balance from what you have now plus what you and your employer add each year.',
        inputs=[
            _f('bal', 'Current balance', MONEY, 85000, step=1000),
            _f('salary', 'Annual salary', MONEY, 110000, step=1000),
            _f('pct', 'You contribute', PCT, 8, step=0.5),
            _f('match', 'Employer matches', PCT, 4, step=0.5),
            _f('yrs', 'Years until retirement', YEARS, 22, step=1, min=1, max=60),
            _f('ret', 'Assumed annual return', PCT, 6.5, step=0.25),
            _f('raise', 'Annual salary increase', PCT, 2.5, step=0.25),
        ],
        js='''
var b = bal, sal = salary, contrib = 0, r = ret/100;
for (var y = 0; y < yrs; y++) {
  var add = sal * (pct + match) / 100;
  contrib += add;
  b = (b + add) * (1 + r);
  sal *= (1 + raise/100);
}
return {
  b: b, contrib: contrib, growth: b - bal - contrib,
  start: bal, first: salary * (pct + match) / 100,
  matchTotal: 0
};''',
        outputs=[
            _o('b', 'Projected balance at retirement', primary=True),
            _o('contrib', 'Total you and your employer contribute'),
            _o('growth', 'Growth on top of contributions'),
            _o('first', 'Contributions in year one'),
            _o('start', "Today's balance"),
        ],
        note='Contributions are treated as added at the start of each year and returns compounded annually. Real markets do not deliver a steady rate, and this ignores contribution limits and inflation.',
    ),

    # ---------------------------------------------------------------- self-employment
    dict(
        slug='self-employment-tax', cat='Tax',
        title='Self-employment tax estimate',
        blurb='Social Security and Medicare on net self-employment earnings, with the deductible half broken out.',
        inputs=[
            _f('net', 'Net self-employment profit', MONEY, 95000, step=1000),
            _f('w2', 'Wages already subject to Social Security', MONEY, 0, step=1000,
               hint='From a W-2 job in the same year. These use up the Social Security wage base first.'),
            _f('base', 'Social Security wage base', MONEY, 184500, step=100,
               hint='Set each year by the Social Security Administration — check the current figure before relying on this.'),
        ],
        js='''
var seBase = Math.max(net, 0) * 0.9235;
var ssRoom = Math.max(base - w2, 0);
var ssWages = Math.min(seBase, ssRoom);
var ss = ssWages * 0.124;
var med = seBase * 0.029;
var addl = Math.max(seBase + w2 - 200000, 0) * 0.009;
var total = ss + med + addl;
return {
  total: total, ss: ss, med: med, addl: addl,
  seBase: seBase, deduction: (ss + med) / 2,
  quarterly: total / 4
};''',
        outputs=[
            _o('total', 'Estimated self-employment tax', primary=True),
            _o('quarterly', 'Roughly, per quarterly instalment'),
            _o('ss', 'Social Security portion'),
            _o('med', 'Medicare portion'),
            _o('addl', 'Additional Medicare surtax',
               note='0.9% above $200,000. The real threshold depends on your filing status.'),
            _o('deduction', 'Deductible half, against income tax'),
            _o('seBase', 'Net earnings subject to the tax',
               note='92.35% of profit — the statutory adjustment.'),
        ],
        note='This is self-employment tax only. It is not your income tax, and it does not account for filing status, the qualified business income deduction, or state tax. Rates and the wage base change annually.',
    ),

    # ---------------------------------------------------------------- section 179
    dict(
        slug='section-179', cat='Business',
        title='Equipment purchase tax saving',
        blurb='What a Section 179 or bonus-depreciation deduction is worth against your bracket, and the real after-tax cost of the asset.',
        inputs=[
            _f('cost', 'Equipment cost', MONEY, 75000, step=1000),
            _f('rate', 'Combined federal and state tax rate', PCT, 30, step=1),
            _f('pctbiz', 'Business-use percentage', PCT, 100, step=5, min=0, max=100),
        ],
        js='''
var eligible = cost * Math.min(Math.max(pctbiz,0),100) / 100;
var save = eligible * rate / 100;
return {
  net: cost - save, save: save, eligible: eligible,
  effective: cost > 0 ? (save / cost) * 100 : 0
};''',
        outputs=[
            _o('net', 'After-tax cost of the purchase', primary=True),
            _o('save', 'Tax saving from the deduction'),
            _o('eligible', 'Deductible portion'),
            _o('effective', 'Effective discount', kind=PCT),
        ],
        note='Assumes the asset qualifies and is placed in service this year, and that you have enough taxable income to absorb the deduction — Section 179 cannot create a loss. Annual limits and phase-outs apply. Talk to us before you sign a purchase order.',
    ),

    # ---------------------------------------------------------------- break-even
    dict(
        slug='break-even', cat='Business',
        title='Break-even point',
        blurb='The revenue and unit volume at which the business stops losing money.',
        inputs=[
            _f('fixed', 'Fixed costs per month', MONEY, 24000, step=500),
            _f('price', 'Price per unit', MONEY, 250, step=5),
            _f('varcost', 'Variable cost per unit', MONEY, 95, step=5),
            _f('target', 'Target monthly profit', MONEY, 0, step=500),
        ],
        js='''
var cm = price - varcost;
var margin = price > 0 ? cm / price * 100 : 0;
var units = cm > 0 ? fixed / cm : 0;
var tUnits = cm > 0 ? (fixed + target) / cm : 0;
return {
  units: units, revenue: units * price, cm: cm, margin: margin,
  tUnits: tUnits, tRevenue: tUnits * price
};''',
        outputs=[
            _o('units', 'Units per month to break even', primary=True, kind=NUM),
            _o('revenue', 'Revenue at break-even'),
            _o('cm', 'Contribution margin per unit'),
            _o('margin', 'Contribution margin', kind=PCT),
            _o('tUnits', 'Units to hit your target profit', kind=NUM),
            _o('tRevenue', 'Revenue to hit your target profit'),
        ],
        note='If the contribution margin is zero or negative, no volume breaks even — the price or the unit cost has to change first.',
    ),

    # ---------------------------------------------------------------- college
    dict(
        slug='college-savings', cat='Saving',
        title='Saving for college',
        blurb='What a four-year education is projected to cost when your child starts, and what you need to put aside monthly.',
        inputs=[
            _f('cost', 'Annual cost today', MONEY, 28000, step=1000),
            _f('age', "Child's age now", NUM, 6, step=1, min=0, max=18),
            _f('start', 'Age they start', NUM, 18, step=1, min=15, max=25),
            _f('infl', 'Annual cost inflation', PCT, 5, step=0.25),
            _f('saved', 'Saved so far', MONEY, 12000, step=1000),
            _f('ret', 'Assumed return', PCT, 5.5, step=0.25),
        ],
        js='''
var yrs = Math.max(start - age, 0);
var total = 0;
for (var y = 0; y < 4; y++) total += cost * Math.pow(1 + infl/100, yrs + y);
var r = ret/100/12, n = yrs*12;
var fvSaved = saved * Math.pow(1 + ret/100, yrs);
var need = Math.max(total - fvSaved, 0);
var monthly = n <= 0 ? need : (r === 0 ? need/n : need * r / (Math.pow(1+r, n) - 1));
return {
  monthly: monthly, total: total, fvSaved: fvSaved, need: need, yrs: yrs,
  todayTotal: cost * 4
};''',
        outputs=[
            _o('monthly', 'Save this much each month', primary=True),
            _o('total', 'Projected four-year cost'),
            _o('todayTotal', "Same four years at today's prices"),
            _o('fvSaved', 'What your current savings grow to'),
            _o('need', 'Gap left to fund'),
            _o('yrs', 'Years to save', kind=NUM),
        ],
        note='Ignores financial aid, scholarships and tax treatment of 529 plans. College inflation has historically run above general inflation.',
    ),
]


CATEGORIES = []
for _c in CALCULATORS:
    if _c['cat'] not in CATEGORIES:
        CATEGORIES.append(_c['cat'])


# ============================================================================
# RENDERING
# ============================================================================
CALC_CSS = """
.calcwrap{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:44px;align-items:start;margin-top:8px}
.calcform{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:30px;box-shadow:var(--sh1)}
.calcform .row{margin-bottom:20px}
.calcform label{display:block;font-weight:600;font-size:.92rem;margin-bottom:7px;color:var(--ink)}
.calcform .hint{font-size:.82rem;color:var(--muted);margin-top:6px;line-height:1.5}
.ifield{display:flex;align-items:stretch;border:1.5px solid var(--line);border-radius:9px;background:#fff;overflow:hidden;transition:border-color .15s}
.ifield:focus-within{border-color:var(--acc)}
.ifield .pre,.ifield .suf{display:flex;align-items:center;padding:0 13px;background:var(--cream);color:var(--muted);font-size:.92rem;font-weight:600}
.ifield input{flex:1;min-width:0;border:0;padding:13px 14px;font:inherit;font-size:1rem;color:var(--ink);background:transparent;-moz-appearance:textfield}
.ifield input:focus{outline:none}
.ifield input::-webkit-outer-spin-button,.ifield input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.calcout{position:sticky;top:96px;background:linear-gradient(155deg,var(--ink),var(--ink2));color:#fff;border-radius:18px;padding:30px;box-shadow:var(--sh2)}
.calcout .big{border-bottom:1px solid rgba(255,255,255,.18);padding-bottom:20px;margin-bottom:20px}
.calcout .big .l{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:#e8d3a8;font-weight:700}
.calcout .big .v{font-family:var(--serif);font-size:2.5rem;line-height:1.1;margin-top:10px;word-break:break-word}
.calcout dl{display:grid;gap:13px;margin:0}
.calcout .orow{display:flex;justify-content:space-between;gap:16px;align-items:baseline}
.calcout dt{color:#c8c4ba;font-size:.9rem}
.calcout dd{margin:0;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}
.calcout .onote{font-size:.8rem;color:#b0aca2;margin-top:3px;line-height:1.45}
.calcnote{font-size:.88rem;color:var(--muted);margin-top:26px;padding-top:20px;border-top:1px solid var(--line);line-height:1.6}
.calcgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:20px;margin-top:26px}
.calccard{display:block;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:26px;text-decoration:none;color:inherit;box-shadow:var(--sh1);transition:transform .2s,box-shadow .2s,border-color .2s}
.calccard:hover{transform:translateY(-3px);box-shadow:var(--sh2);border-color:var(--acc)}
.calccard .cc{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accd);font-weight:700}
.calccard h3{margin:10px 0 8px;font-size:1.14rem}
.calccard p{font-size:.92rem;color:#3c4038;margin:0}
@media(max-width:900px){.calcwrap{grid-template-columns:minmax(0,1fr)}.calcout{position:static}}
"""

CALC_JS = r"""
<script>(function(){
var host=document.querySelector('[data-calc]');if(!host)return;
var spec=JSON.parse(document.getElementById('calcspec').textContent);
var f=spec.inputs,outs=spec.outputs;
var fmtM=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
var fmtM2=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2});
var fmtN=new Intl.NumberFormat('en-US',{maximumFractionDigits:1});
function fmt(v,kind){
  if(!isFinite(v))return '—';
  if(kind==='money')return Math.abs(v)<100?fmtM2.format(v):fmtM.format(v);
  if(kind==='pct')return fmtN.format(v)+'%';
  return fmtN.format(v);
}
var compute=new Function(f.map(function(x){return x.id;}).join(','),spec.js);
function read(){
  return f.map(function(x){
    var el=document.getElementById('f_'+x.id);
    var v=parseFloat(String(el.value).replace(/[^0-9.\-]/g,''));
    return isFinite(v)?v:0;
  });
}
function run(){
  var res;
  try{res=compute.apply(null,read());}catch(e){return;}
  outs.forEach(function(o){
    var el=document.getElementById('o_'+o.id);
    if(el)el.textContent=fmt(res[o.id],o.kind);
  });
}
f.forEach(function(x){
  var el=document.getElementById('f_'+x.id);
  el.addEventListener('input',run);
  el.addEventListener('change',run);
});
run();
})();</script>
"""


def calc_page_body(calc, phero, rel, ARROW, depth=1):
    """Body HTML for one calculator page."""
    import json as _json
    rows = ''
    for x in calc['inputs']:
        pre = '<span class="pre">$</span>' if x['kind'] == MONEY else ''
        suf = ('<span class="suf">%</span>' if x['kind'] == PCT else
               '<span class="suf">yrs</span>' if x['kind'] == YEARS else '')
        attrs = ' step="' + str(x['step']) + '"' if x.get('step') else ''
        if x.get('min') is not None:
            attrs += ' min="' + str(x['min']) + '"'
        if x.get('max') is not None:
            attrs += ' max="' + str(x['max']) + '"'
        rows += ('<div class="row"><label for="f_' + x['id'] + '">' + x['label'] + '</label>'
                 '<div class="ifield">' + pre +
                 '<input type="number" inputmode="decimal" id="f_' + x['id'] + '" '
                 'value="' + str(x['default']) + '"' + attrs + '>' + suf + '</div>'
                 + ('<p class="hint">' + x['hint'] + '</p>' if x.get('hint') else '')
                 + '</div>')

    primary = next((o for o in calc['outputs'] if o['primary']), calc['outputs'][0])
    secondary = [o for o in calc['outputs'] if not o['primary']]
    srows = ''
    for o in secondary:
        srows += ('<div><div class="orow"><dt>' + o['label'] + '</dt>'
                  '<dd id="o_' + o['id'] + '">&mdash;</dd></div>'
                  + ('<div class="onote">' + o['note'] + '</div>' if o.get('note') else '')
                  + '</div>')

    spec = _json.dumps(dict(
        inputs=[dict(id=x['id']) for x in calc['inputs']],
        outputs=[dict(id=o['id'], kind=o['kind']) for o in calc['outputs']],
        js=calc['js'],
    ))

    return (
        phero + '<section class="sec"><div class="wrap">'
        '<div class="calcwrap" data-calc>'
        '<div class="calcform">' + rows +
        '<p class="calcnote">' + calc['note'] + '</p></div>'
        '<div class="calcout" aria-live="polite">'
        '<div class="big"><div class="l">' + primary['label'] + '</div>'
        '<div class="v" id="o_' + primary['id'] + '">&mdash;</div></div>'
        '<dl>' + srows + '</dl></div>'
        '</div>'
        '<script type="application/json" id="calcspec">' + spec + '</script>'
        '</div></section>'
    )
