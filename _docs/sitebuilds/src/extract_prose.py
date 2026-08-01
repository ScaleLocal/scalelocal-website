# -*- coding: utf-8 -*-
"""
Extract honesty-checked prose from built (or deployed) pages so a site can be
re-laid into a new architecture without rewriting a word.

    python3 extract_prose.py <dir-of-html> <out.json>
    python3 extract_prose.py out/carellacpa content_blocks_carellacpa.json

Works equally on a local build directory or a folder of pages saved from the live
site. Strips chrome (masthead, nav, footer, widgets, scripts) and keeps the ordered
semantic blocks: h2/h3/h4, p, ul, ol, table, blockquote.
"""
import os, sys, json
from bs4 import BeautifulSoup

CHROME = ('.demostrip,.topbar,.hdr,header,nav,.foot,footer,.launch,.helpdesk,'
          'script,style,.crumbs,.trail,.cta,.closing,.colophon,.notice,'
          '.calcform,.calcout,.fields,.result')
KEEP = {'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'table', 'blockquote'}


def extract(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dp, f), root).replace('\\', '/')
            soup = BeautifulSoup(open(os.path.join(dp, f), encoding='utf-8').read(), 'html.parser')
            for bad in soup.select(CHROME):
                bad.decompose()
            h1 = soup.find('h1')
            sub = soup.select_one('.sub, .stand')
            blocks = []
            for el in soup.find_all(list(KEEP)):
                if el.find_parent(['ul', 'ol', 'table', 'blockquote']):
                    continue
                txt = el.get_text(' ', strip=True)
                if not txt:
                    continue
                blocks.append({'tag': el.name, 'html': el.decode_contents().strip(), 'text': txt})
            out[rel] = dict(
                title=(soup.find('title').get_text() if soup.find('title') else ''),
                desc=(soup.find('meta', attrs={'name': 'description'}) or {}).get('content', ''),
                h1=h1.get_text(strip=True) if h1 else '',
                sub=sub.get_text(strip=True) if sub else '',
                blocks=blocks)
    return out


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    data = extract(sys.argv[1])
    json.dump(data, open(sys.argv[2], 'w'), indent=1)
    print('%d pages, %d blocks, %d words -> %s' % (
        len(data), sum(len(p['blocks']) for p in data.values()),
        sum(len(b['text'].split()) for p in data.values() for b in p['blocks']), sys.argv[2]))
