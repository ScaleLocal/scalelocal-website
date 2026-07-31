# -*- coding: utf-8 -*-
"""Find British spellings in the built sites and the build sources."""
import os, re, sys, collections

PAIRS = [
 # -ise / -isation family
 (r'\bauthoris(e|ed|es|ing|ation)\b', 'authoriz'), (r'\borganis(e|ed|es|ing|ation|ational)\b','organiz'),
 (r'\brecognis(e|ed|es|ing)\b','recogniz'), (r'\brealis(e|ed|es|ing)\b','realiz'),
 (r'\bspecialis(e|ed|es|ing|ation|t|ts|m|ms)\b','specializ'), (r'\bminimis(e|ed|es|ing)\b','minimiz'),
 (r'\bmaximis(e|ed|es|ing)\b','maximiz'), (r'\bsummaris(e|ed|es|ing)\b','summariz'),
 (r'\banalys(e|ed|es|ing|is)\b','analyz'), (r'\bcategoris(e|ed|es|ing)\b','categoriz'),
 (r'\bprioritis(e|ed|es|ing)\b','prioritiz'), (r'\bitemis(e|ed|es|ing)\b','itemiz'),
 (r'\bcapitalis(e|ed|es|ing|ation)\b','capitaliz'), (r'\bpenalis(e|ed|es|ing)\b','penaliz'),
 (r'\bfinalis(e|ed|es|ing)\b','finaliz'), (r'\bnormalis(e|ed|es|ing)\b','normaliz'),
 (r'\bstandardis(e|ed|es|ing)\b','standardiz'), (r'\butilis(e|ed|es|ing|ation)\b','utiliz'),
 (r'\bcharacteris(e|ed|es|ing)\b','characteriz'), (r'\bemphasis(e|ed|es|ing)\b','emphasiz'),
 (r'\bcriticis(e|ed|es|ing|m)\b','criticiz'), (r'\bnotaris(e|ed|es|ing|ation)\b','notariz'),
 (r'\bamortis(e|ed|es|ing|ation)\b','amortiz'), (r'\bapologis(e|ed|es|ing)\b','apologiz'),
 (r'\blegitimis(e|ed|es|ing)\b','legitimiz'), (r'\bcentralis(e|ed|es|ing)\b','centraliz'),
 (r'\bformalis(e|ed|es|ing)\b','formaliz'), (r'\bmodernis(e|ed|es|ing)\b','moderniz'),
 # -our
 (r'\bcolour(s|ed|ing|ful)?\b','color'), (r'\bfavour(s|ed|ing|able|ably)?\b','favor'),
 (r'\bbehaviour(s|al)?\b','behavior'), (r'\blabour(s|ed|ing)?\b','labor'),
 (r'\bhonour(s|ed|ing|able)?\b','honor'), (r'\bneighbour(s|ing|hood)?\b','neighbor'),
 (r'\bendeavour(s|ed|ing)?\b','endeavor'), (r'\brumour(s)?\b','rumor'),
 (r'\bhumour(s|ous)?\b','humor'), (r'\bvigour\b','vigor'), (r'\bodour(s)?\b','odor'),
 (r'\bharbour(s|ed|ing)?\b','harbor'), (r'\bsavour(s|ed|ing|y)?\b','savor'),
 # -re
 (r'\bcentre(s|d)?\b','center'), (r'\bmetre(s)?\b','meter'), (r'\blitre(s)?\b','liter'),
 (r'\btheatre(s)?\b','theater'), (r'\bfibre(s)?\b','fiber'), (r'\bcalibre\b','caliber'),
 (r'\bsombre\b','somber'), (r'\bspectre\b','specter'), (r'\blustre\b','luster'),
 (r'\bmanoeuvr(e|es|ed|ing)\b','maneuver'),
 # -ce / -se nouns
 (r'\blicence(s|d)?\b','license'), (r'\bpractis(e|ed|es|ing)\b','practic'),
 (r'\bdefence(s|less)?\b','defense'), (r'\boffence(s)?\b','offense'), (r'\bpretence\b','pretense'),
 # doubled l
 (r'\btravell(ed|ing|er|ers)\b','travel'), (r'\blabell(ed|ing)\b','label'),
 (r'\bmodell(ed|ing)\b','model'), (r'\bcancell(ed|ing)\b','cancel'),
 (r'\bmarvell(ed|ous)\b','marvel'), (r'\bsignall(ed|ing)\b','signal'),
 (r'\btotall(ed|ing)\b','total'), (r'\bfuell(ed|ing)\b','fuel'),
 (r'\bcounsell(ed|ing|or|ors)\b','counsel'), (r'\bdiall(ed|ing)\b','dial'),
 (r'\bfulfil\b','fulfill'), (r'\bfulfilment\b','fulfillment'),
 (r'\benrolment(s)?\b','enrollment'), (r'\binstalment(s)?\b','installment'),
 (r'\bskilful(ly)?\b','skillful'), (r'\bwilful(ly)?\b','willful'),
 # misc
 (r'\bjudgement(s|al)?\b','judgment'), (r'\backnowledgement(s)?\b','acknowledgment'),
 (r'\bprogramme(s|d)?\b','program'), (r'\bcheque(s)?\b','check'),
 (r'\bgrey(s|ing|ish)?\b','gray'), (r'\bstorey(s)?\b','story'),
 (r'\bageing\b','aging'), (r'\bcosy\b','cozy'), (r'\bsceptic(al|ism)?\b','skeptic'),
 (r'\bdraught(s)?\b','draft'), (r'\bkerb(s)?\b','curb'), (r'\btyre(s)?\b','tire'),
 (r'\baluminium\b','aluminum'), (r'\bspeciality\b','specialty'),
 (r'\borientated\b','oriented'), (r'\bper cent\b','percent'),
 (r'\bwhilst\b','while'), (r'\bamongst\b','among'), (r'\btowards\b','toward'),
 (r'\blearnt\b','learned'), (r'\bspelt\b','spelled'), (r'\bburnt\b','burned'),
 (r'\bdreamt\b','dreamed'), (r'\bleapt\b','leaped'), (r'\bmaths\b','math'),
 (r'\bfavourite(s)?\b','favorite'), (r'\bmoustache\b','mustache'),
 (r'\bpyjama(s)?\b','pajama'), (r'\bplough(s|ed|ing)?\b','plow'),
 (r'\bstorey\b','story'), (r'\btravelling\b','traveling'),
]

def scan(paths, label):
    hits = collections.Counter(); where = collections.defaultdict(set)
    for p in paths:
        try: t = open(p, encoding='utf-8').read()
        except Exception: continue
        for rx, _ in PAIRS:
            for m in re.finditer(rx, t, re.I):
                hits[m.group(0).lower()] += 1
                where[m.group(0).lower()].add(p)
    print('=== %s' % label)
    for w, n in hits.most_common():
        ex = sorted(where[w])[:3]
        print('  %-18s %4d   %s' % (w, n, ', '.join(os.path.relpath(x) for x in ex)))
    if not hits: print('  clean')
    return hits, where

built = []
for root, _, fs in os.walk('out'):
    for f in fs:
        if f.endswith(('.html', '.css', '.xml', '.txt')): built.append(os.path.join(root, f))
scan(built, 'BUILT OUTPUT (out/)')

src = [f for f in os.listdir('.') if f.endswith('.py')]
for d in ('content_dorfman','content_goguen','content_millcity','firms'):
    if os.path.isdir(d): src += [os.path.join(d,f) for f in os.listdir(d)]
scan(src, 'SOURCES')
