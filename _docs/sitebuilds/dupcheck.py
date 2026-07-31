import os, re, sys, html as H
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))

# The ScaleLocal demonstration notice is deliberately word-for-word identical on
# every build in the batch — it is the disclaimer, not firm copy. It is filtered
# out here rather than reworded, so the count reports genuine leakage only.
NOTICE = {
    "Not affiliated with, authorized by, or endorsed by the firm",
    "Reproduction or use of this site or its contents is prohibited",
}

def sentences(root):
    d = defaultdict(set)
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if not fn.endswith('.html'): continue
            p = os.path.join(dp, fn)
            t = open(p, encoding='utf-8').read()
            t = re.sub(r'(?is)<(script|style|svg)\b.*?</\1>', ' ', t)
            t = re.sub(r'(?s)<!--.*?-->', ' ', t)
            t = re.sub(r'(?s)<[^>]+>', ' ', t)
            t = H.unescape(t)
            t = t.replace('’',"'").replace('—',' - ').replace('–',' - ')
            t = re.sub(r'\s+', ' ', t).strip()
            for s in re.split(r'[.?!]+', t):
                s = re.sub(r'\s+',' ', s).strip()
                if len(s.split()) >= 8:
                    d[s].add(os.path.relpath(p, root))
    return d

def cmp(a, b):
    A, B = sentences(os.path.join(HERE,'out',a)), sentences(os.path.join(HERE,'out',b))
    shared = sorted((set(A) & set(B)) - NOTICE)
    print("=== %s vs %s : %d shared sentences ===" % (a, b, len(shared)))
    for s in shared:
        print("  [%s | %s]\n    %s" % (','.join(sorted(A[s])), ','.join(sorted(B[s])), s))
    return len(shared)

if __name__ == '__main__':
    pairs = [('carellacpa','masstaxpros'), ('carellacpa','hickeycpa'),
             ('masstaxpros','hickeycpa')]
    if len(sys.argv) > 2: pairs = [(sys.argv[1], sys.argv[2])]
    tot = 0
    for a,b in pairs: tot += cmp(a,b)
    print("TOTAL SHARED:", tot)
