#!/usr/bin/env python3
"""
ScaleLocal daily article publisher.
Runs once/day (via Windows Task Scheduler). Takes the OLDEST queued article from
_article_queue/, installs it into /blog/<slug>/index.html, adds it to the blog
index + sitemap.xml, then git commit + push (Vercel auto-deploys).

A queued article is a single .json file in _article_queue/ shaped like:
{
  "slug": "how-to-...", "title": "...", "description": "...",
  "card_blurb": "one-line teaser for the blog index",
  "html": "<full <!DOCTYPE html>...</html> page>"
}
Zero-touch: needs no internet from the user, only the PC on + online at run time.
"""
import os, sys, json, glob, subprocess, datetime, re

REPO = os.path.dirname(os.path.abspath(__file__))
os.chdir(REPO)
QUEUE = os.path.join(REPO, "_article_queue")
LOGDIR = os.path.join(REPO, "_published_log")
os.makedirs(LOGDIR, exist_ok=True)
LOG = os.path.join(LOGDIR, "publish.log")
SITE = "https://www.scalelocal.net"

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
        os.remove(qfile); return
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

    # 4) add a card to blog/index.html (after the first <a ... class="post-card"> block start area)
    bi_path = os.path.join(REPO, "blog", "index.html")
    bi = open(bi_path, encoding="utf-8").read()
    if f'/blog/{slug}/' not in bi:
        card = (f'    <a href="/blog/{slug}/" class="post-card">\n'
                f'      <h2>{art["title"]}</h2>\n'
                f'      <p>{art.get("card_blurb","")}</p>\n'
                f'      <span class="meta">{datetime.date.today().strftime("%B %-d, %Y") if os.name!="nt" else datetime.date.today().strftime("%B %d, %Y")}</span>\n'
                f'    </a>\n')
        # insert right before the first existing post-card link
        m = re.search(r'(\n\s*<a href="/blog/[^"]+" class="post-card">)', bi)
        if m:
            bi = bi[:m.start()] + "\n" + card + bi[m.start():]
        else:
            log("  !! couldn't find a post-card anchor in blog/index.html — card not added (post still live).")
        open(bi_path, "w", encoding="utf-8").write(bi)
        log("  added card to blog/index.html")

    # 5) archive the queue item, then git publish
    done_dir = os.path.join(LOGDIR, "published_items"); os.makedirs(done_dir, exist_ok=True)
    os.replace(qfile, os.path.join(done_dir, os.path.basename(qfile)))

    log("  syncing + pushing...")
    run(["git", "add", f"blog/{slug}/index.html", "sitemap.xml", "blog/index.html"])
    run(["git", "commit", "-m", f"blog: publish '{slug}' (auto daily)"], check=False)
    # pull-rebase to stay in sync (auto-resolve unrelated conflicts to remote), then push
    run(["git", "pull", "--rebase", "-X", "theirs"], check=False)
    run(["git", "push"])
    log(f"  DONE — https://www.scalelocal.net/blog/{slug}/ will be live after Vercel build (~1-2 min).")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code: log(f"ABORTED: {e}")
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}")
