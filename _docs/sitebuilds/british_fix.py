# -*- coding: utf-8 -*-
"""British -> American spelling across every build source. Case-preserving.
Deliberately does NOT touch words that are already correct American English:
analysis, specialist, expertise, enterprise, advertise, exercise, etc."""
import os, re, sys, collections

# (regex, replacement) — regex is applied case-insensitively; the replacement
# re-cases itself from the match so Title Case and UPPER survive.
MAP = [
 (r'authoris(e|es|ed|ing)',      r'authoriz\1'),
 (r'authorisation(s)?',          r'authorization\1'),
 (r'organis(e|es|ed|ing)',       r'organiz\1'),
 (r'organisation(s|al)?',        r'organization\1'),
 (r'recognis(e|es|ed|ing)',      r'recogniz\1'),
 (r'realis(e|es|ed|ing)',        r'realiz\1'),
 (r'specialis(e|es|ed|ing)',     r'specializ\1'),   # NOT specialist/specialists
 (r'specialisms',                'specialties'),
 (r'specialism',                 'specialty'),
 (r'minimis(e|es|ed|ing)',       r'minimiz\1'),
 (r'maximis(e|es|ed|ing)',       r'maximiz\1'),
 (r'summaris(e|es|ed|ing)',      r'summariz\1'),
 (r'analys(e|es|ed|ing)\b',      r'analyz\1'),      # NOT analysis
 (r'categoris(e|es|ed|ing)',     r'categoriz\1'),
 (r'prioritis(e|es|ed|ing)',     r'prioritiz\1'),
 (r'itemis(e|es|ed|ing)',        r'itemiz\1'),
 (r'capitalis(e|es|ed|ing)',     r'capitaliz\1'),
 (r'capitalisation(s)?',         r'capitalization\1'),
 (r'penalis(e|es|ed|ing)',       r'penaliz\1'),
 (r'finalis(e|es|ed|ing)',       r'finaliz\1'),
 (r'normalis(e|es|ed|ing)',      r'normaliz\1'),
 (r'standardis(e|es|ed|ing)',    r'standardiz\1'),
 (r'utilis(e|es|ed|ing)',        r'utiliz\1'),
 (r'utilisation(s)?',            r'utilization\1'),
 (r'characteris(e|es|ed|ing)',   r'characteriz\1'),
 (r'emphasis(e|es|ed|ing)\b',    r'emphasiz\1'),
 (r'criticis(e|es|ed|ing|m)',    r'criticiz\1'),
 (r'notaris(e|es|ed|ing)',       r'notariz\1'),
 (r'notarisation(s)?',           r'notarization\1'),
 (r'amortis(e|es|ed|ing)',       r'amortiz\1'),
 (r'amortisation',               'amortization'),
 (r'apologis(e|es|ed|ing)',      r'apologiz\1'),
 (r'centralis(e|es|ed|ing)',     r'centraliz\1'),
 (r'formalis(e|es|ed|ing)',      r'formaliz\1'),
 (r'modernis(e|es|ed|ing)',      r'moderniz\1'),
 (r'legitimis(e|es|ed|ing)',     r'legitimiz\1'),
 # -our
 (r'colour(s|ed|ing|ful)?',      r'color\1'),
 (r'favourab(le|ly)',            r'favorab\1'),
 (r'favour(s|ed|ing)?',          r'favor\1'),
 (r'behaviour(s|al)?',           r'behavior\1'),
 (r'labour(s|ed|ing)?',          r'labor\1'),
 (r'honourab(le|ly)',            r'honorab\1'),
 (r'honour(s|ed|ing)?',          r'honor\1'),
 (r'neighbourhood(s)?',          r'neighborhood\1'),
 (r'neighbour(s|ing)?',          r'neighbor\1'),
 (r'endeavour(s|ed|ing)?',       r'endeavor\1'),
 (r'rumour(s)?',                 r'rumor\1'),
 (r'humour(s|ous)?',             r'humor\1'),
 (r'vigour',                     'vigor'),
 (r'odour(s)?',                  r'odor\1'),
 (r'harbour(s|ed|ing)?',         r'harbor\1'),
 (r'savour(s|ed|ing|y)?',        r'savor\1'),
 # -re
 (r'centre(s|d)?',               r'center\1'),
 (r'metre(s)?',                  r'meter\1'),
 (r'litre(s)?',                  r'liter\1'),
 (r'theatre(s)?',                r'theater\1'),
 (r'fibre(s)?',                  r'fiber\1'),
 (r'calibre',                    'caliber'),
 (r'sombre',                     'somber'),
 (r'spectre',                    'specter'),
 (r'lustre',                     'luster'),
 (r'manoeuvr(e|es|ed|ing)',      r'maneuver\1'),
 # -ce / -se
 (r'licence(s|d)?',              r'license\1'),
 (r'practis(e|es|ed|ing)',       r'practic\1'),
 (r'defence(s|less)?',           r'defense\1'),
 (r'offence(s)?',                r'offense\1'),
 (r'pretence',                   'pretense'),
 # doubled l
 (r'travell(ed|ing|er|ers)',     r'travel\1'),
 (r'labell(ed|ing)',             r'label\1'),
 (r'modell(ed|ing)',             r'model\1'),
 (r'cancell(ed|ing)',            r'cancel\1'),
 (r'marvell(ed|ous)',            r'marvel\1'),
 (r'signall(ed|ing)',            r'signal\1'),
 (r'totall(ed|ing)',             r'total\1'),
 (r'fuell(ed|ing)',              r'fuel\1'),
 (r'counsell(ed|ing|or|ors)',    r'counsel\1'),
 (r'diall(ed|ing)',              r'dial\1'),
 (r'fulfilment',                 'fulfillment'),
 (r'fulfil\b',                   'fulfill'),
 (r'enrolment(s)?',              r'enrollment\1'),
 (r'instalment(s)?',             r'installment\1'),
 (r'skilful(ly)?',               r'skillful\1'),
 (r'wilful(ly)?',                r'willful\1'),
 # misc
 (r'judgement(s|al)?',           r'judgment\1'),
 (r'acknowledgement(s)?',        r'acknowledgment\1'),
 (r'programme(s|d)?',            r'program\1'),
 (r'cheque(s)?',                 r'check\1'),
 (r'grey(s|ing|ish)?',           r'gray\1'),
 (r'storey(s)?',                 r'story\1'),
 (r'ageing',                     'aging'),
 (r'cosy',                       'cozy'),
 (r'sceptic(al|ism)?',           r'skeptic\1'),
 (r'draught(s)?',                r'draft\1'),
 (r'kerb(s)?',                   r'curb\1'),
 (r'tyre(s)?',                   r'tire\1'),
 (r'aluminium',                  'aluminum'),
 (r'speciality',                 'specialty'),
 (r'orientated',                 'oriented'),
 (r'per cent\b',                 'percent'),
 (r'whilst',                     'while'),
 (r'amongst',                    'among'),
 (r'towards',                    'toward'),
 (r'learnt',                     'learned'),
 (r'spelt',                      'spelled'),
 (r'burnt',                      'burned'),
 (r'dreamt',                     'dreamed'),
 (r'maths\b',                    'math'),
 (r'favourite(s)?',              r'favorite\1'),
 (r'plough(s|ed|ing)?',          r'plow\1'),
]
RX = [(re.compile(r'\b' + p + r'\b', re.I), r) for p, r in MAP]


def recase(src, out):
    if src.isupper() and len(src) > 1: return out.upper()
    if src[:1].isupper():              return out[:1].upper() + out[1:]
    return out


def convert(text):
    n = 0
    for rx, rep in RX:
        def sub(m):
            nonlocal n
            n += 1
            new = m.expand(rep) if '\\' in rep else rep
            return recase(m.group(0), new.lower())
        text = rx.sub(sub, text)
    return text, n


targets = []
for f in sorted(os.listdir('.')):
    if f.endswith(('.py', '.json', '.md')) and f not in ('gates_bespoke.py',):
        targets.append(f)
for d in ('content_dorfman', 'content_goguen', 'content_millcity', 'firms'):
    if os.path.isdir(d):
        targets += [os.path.join(d, f) for f in sorted(os.listdir(d))
                    if f.endswith(('.html', '.py', '.json', '.md'))]

total = 0
changed = []
for p in targets:
    s = open(p, encoding='utf-8').read()
    new, n = convert(s)
    if n:
        open(p, 'w', encoding='utf-8').write(new)
        changed.append((p, n)); total += n
for p, n in changed:
    print('  %-42s %4d' % (p, n))
print('FILES %d   REPLACEMENTS %d' % (len(changed), total))
