# -*- coding: utf-8 -*-
"""final verification copy — identical content to _batchB.py"""

ARTICLES = [

    {
        "slug": "why-is-my-competitor-outranking-me-on-google",
        "body_html": """<p>One more thing worth hearing: ranking is a moving target. The competitor on top today got there by doing this work consistently, and they can be passed by someone who does it more consistently. That someone can be you. The contractors who win don’t treat this as a one-time project — they treat it as a habit, the same way they treat showing up on time and cleaning up the job site. Steady wins the local-search race every single time.</p>""",
    },
    {
        "slug": "how-to-get-more-calls-from-google",
        "body_html": """<p>And track it. If you don’t know how many calls Google sends you, you’re flying blind — your Business Profile dashboard shows calls and direction requests, and a simple call-tracking number tells you which channel actually rings the phone. Once you can see the numbers, you stop guessing and start fixing the one stage that’s costing you the most.</p>""",
    },
    {
        "slug": "what-marketing-works-best-in-the-slow-season",
        "body_html": """<h2>One caveat: match the work to your trade’s calendar</h2>
<p>“Slow season” isn’t the same month for everyone. A snow-removal company’s slow season is summer; a pool installer’s is winter. The principle holds either way, but the tactics shift — your reactivation offers and seasonal content should point at <em>your</em> next busy stretch, not a generic one. The contractors who get this wrong run a spring-tune-up campaign in the dead of their actual peak. Map your year first, then aim the slow-season build at the demand you know is coming. Done right, the quiet months stop feeling like a threat to your cash flow and start feeling like the runway that launches your best season yet.</p>""",
    },
]

import re, html
for a in ARTICLES:
    t = html.unescape(re.sub('<[^>]+>', ' ', a['body_html']))
    t = re.sub(r'[—–]', ' ', t)
    wc = len([w for w in re.split(r'\s+', t) if re.search(r'[A-Za-z0-9]', w)])
    print(a['slug'], 'added_words=', wc)
