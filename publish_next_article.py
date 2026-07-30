#!/usr/bin/env python3
"""
ScaleLocal daily article publisher.
Runs once/day (via Windows Task Scheduler). Takes the OLDEST queued article from
_article_queue/, installs it into /blog/<slug>/index.html, adds it to the blog
index + sitemap.xml, then git commit + push (Vercel auto-deploys). After pushing,
it nudges search engines to re-crawl the fresh sitemap (best-effort).

A queued article is a single .json file in _article_queue/ shaped like:
{
  "slug": "how-to-...", "title": "...", "description": "...",
  "card_blurb": "one-line teaser for the blog index",
  "html": "<full <!DOCTYPE html>...</html> page>"
}
Zero-touch: needs no internet from the user, only the PC on + online at run time.
"""
import os, sys, json, glob, subprocess, datetime, re
import urllib.request, urllib.parse

REPO = os.path.dirname(os.path.abspath(__file__))
os.chdir(REPO)
QUEUE = os.path.join(REPO, "_article_queue")
LOGDIR = os.path.join(REPO, "_published_log")
os.makedirs(LOGDIR, exist_ok=True)
LOG = os.path.join(LOGDIR, "publish.log")
SITE = "https://www.scalelocal.net"
SITEMAP = SITE + "/sitemap.xml"

def log(msg):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def run(cmd, check=True):
    log("  $ " + " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout.strip(): log("    " + r.stdout.strip().replace("\n","\n    "))
    if r.returncode != 0 and r.stderr.strip(): log("    ! " + r.stderr.strip().replace("\n","\n    "))
    if check and r.returncode != 0: raise SystemExit(f"command failed: {' '.join(cmd)}")
    return r

def ping_search_engines(slug):
    """Tell search engines a new URL + the sitemap are fresh. All best-effort:
    any failure is logged and ignored so it never blocks a publish.
    NOTE: Google deprecated its sitemap-ping endpoint in 2023, so we no longer
    call it (it would be dead weight). Google still discovers via the sitemap it
    already re-reads on its own crawl schedule; the IndexNow ping below covers
    Bing + Yandex, which DO honor instant pings, and Google increasingly reads
    IndexNow signals too. We also warm our own sitemap URL so Vercel serves the
    freshest copy when crawlers arrive."""
    new_url = f"{SITE}/blog/{slug}/"
    def _get(url, timeout=12):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ScaleLocal-Publisher/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status
        except Exception as e:
            return f"err:{type(e).__name__}"

    # a) Warm our own sitemap (forces Vercel edge to cache the freshest version)
    log(f"  ping: sitemap warm -> {_get(SITEMAP)}")
    # b) IndexNow (Bing + Yandex honor this instantly; key is a public token file
    #    that must exist at SITE/<key>.txt -- we only ping if that file is present).
    key_file = os.path.join(REPO, "indexnow-key.txt")
    if os.path.exists(key_file):
        try:
            key = open(key_file, encoding="utf-8").read().strip()
            endpoint = ("https://api.indexnow.org/indexnow?url="
                        f"{urllib.parse.quote(new_url, safe='')}&key={key}"
                        f"&keyLocation={SITE}/{key}.txt")
            log(f"  ping: IndexNow -> {_get(endpoint)}")
        except Exception as e:
            log(f"  ping: IndexNow skipped ({type(e).__name__})")
    else:
        log("  ping: IndexNow skipped (no indexnow-key.txt yet)")

def main():
    # 1) pick oldest queued article
    items = sorted(glob.glob(os.path.join(QUEUE, "*.json")))
    if not items:
        log("Queue empty — nothing to publish today. (Not an error.)")
        return
    qfile = items[0]
    art = json.load(open(qfile, encoding="utf-8"))
    slug = art["slug"]
    log(f"Publishing: {slug}  ({len(items)} in queue)")

    # 2) write the blog post
    outdir = os.path.join(REPO, "blog", slug)
    if os.path.exists(os.path.join(outdir, "index.html")):
        log(f"  !! /blog/{slug}/ already exists — skipping this item, removing from queue.")
        qrel_skip = os.path.relpath(qfile, REPO).replace("\\", "/")
        os.remove(qfile)
        # stage + commit the dequeue, else it lingers unstaged and breaks pull --rebase
        run(["git", "add", "-A", "--", qrel_skip], check=False)
        run(["git", "commit", "-m", f"blog: dequeue duplicate '{slug}' (auto daily)"], check=False)
        return
    os.makedirs(outdir, exist_ok=True)
    html = art["html"]
    # sanity: must be a full page
    if "</html>" not in html or "<title>" not in html:
        log("  !! queued html looks incomplete — aborting, leaving in queue for review."); raise SystemExit(1)
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(html)
    log(f"  wrote blog/{slug}/index.html")

    # 3) add to sitemap.xml (before </urlset>)
    sm_path = os.path.join(REPO, "sitemap.xml")
    sm = open(sm_path, encoding="utf-8").read()
    loc = f"{SITE}/blog/{slug}/"
    if loc not in sm:
        today = datetime.date.today().isoformat()
        entry = f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
        sm = sm.replace("</urlset>", entry + "</urlset>", 1)
        open(sm_path, "w", encoding="utf-8").write(sm)
        log("  added to sitemap.xml")

    # 4) add a card to blog/index.html (before the first existing post-card link)
    bi_path = os.path.join(REPO, "blog", "index.html")
    bi = open(bi_path, encoding="utf-8").read()
    if f'/blog/{slug}/' not in bi:
        card = (f'    <a href="/blog/{slug}/" class="post-card">\n'
                f'      <h2>{art["title"]}</h2>\n'
                f'      <p>{art.get("card_blurb","")}</p>\n'
                f'      <span class="meta">{datetime.date.today().strftime("%B %-d, %Y") if os.name!="nt" else datetime.date.today().strftime("%B %d, %Y")}</span>\n'
                f'    </a>\n')
        m = re.search(r'(\n\s*<a href="/blog/[^"]+" class="post-card">)', bi)
        if m:
            bi = bi[:m.start()] + "\n" + card + bi[m.start():]
        else:
            log("  !! couldn't find a post-card anchor in blog/index.html — card not added (post still live).")
        open(bi_path, "w", encoding="utf-8").write(bi)
        log("  added card to blog/index.html")

    # 5) archive the queue item, then git publish
    done_dir = os.path.join(LOGDIR, "published_items"); os.makedirs(done_dir, exist_ok=True)
    qrel = os.path.relpath(qfile, REPO).replace("\\", "/")
    os.replace(qfile, os.path.join(done_dir, os.path.basename(qfile)))

    log("  syncing + pushing...")
    # NOTE: the queue .json is TRACKED, and the os.replace above deletes it from
    # _article_queue/. That deletion must be staged here. Without "-A" and qrel it
    # stayed unstaged forever, and every later `git pull --rebase` died with
    # "cannot pull with rebase: You have unstaged changes." (Fixed 2026-07-30.)
    run(["git", "add", "-A", "--", f"blog/{slug}/index.html", "sitemap.xml", "blog/index.html", qrel])
    run(["git", "commit", "-m", f"blog: publish '{slug}' (auto daily)"], check=False)
    # pull-rebase to stay in sync (auto-resolve unrelated conflicts to remote), then push
    _pull = run(["git", "pull", "--rebase", "-X", "theirs"], check=False)
    if _pull.returncode != 0:
        log("  !! WARNING: `git pull --rebase` FAILED. The push below may be rejected, and")
        log("  !! local/remote can drift. Do not ignore this line — check `git status`.")
    run(["git", "push"])
    log(f"  DONE — https://www.scalelocal.net/blog/{slug}/ will be live after Vercel build (~1-2 min).")

    # 6) Nudge search engines to re-crawl the fresh sitemap. Best-effort, never fatal.
    try:
        ping_search_engines(slug)
    except Exception as e:
        log(f"  ping: skipped ({type(e).__name__})")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code: log(f"ABORTED: {e}")
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}")
