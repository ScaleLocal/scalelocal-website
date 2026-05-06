# Launch Day Checklist — TNJ Landscape

When the real domain is live and ready to be indexed, run through this checklist
to flip the site from demo-mode (no-index, no-AI) to production-mode (full
indexing + AI visibility).

## 1. DNS + Vercel
- [ ] Real domain pointed at Vercel deployment
- [ ] HTTPS cert valid
- [ ] `www.` and apex both resolve and 301 to canonical (pick one)

## 2. De-noindex the site

Find every `<meta name="robots" content="noindex,nofollow">` in the HTML and
remove it. From the repo root:

```bash
# remove the demo noindex meta from every file
find test-builds/tnj-landscape -name "*.html" -exec \
  sed -i 's|<meta name="robots" content="noindex,nofollow">||g' {} \;

# also remove the older noindex,follow on town pages (if they should be indexed
# at launch — they should, since they're SEO landing pages)
find test-builds/tnj-landscape/towns -name "*.html" -exec \
  sed -i 's|<meta name="robots" content="noindex,follow">||g' {} \;
```

## 3. Replace robots.txt with production version

```bash
cp test-builds/tnj-landscape/_launch_bundle/robots-PROD.txt \
   test-builds/tnj-landscape/robots.txt
# then update [REAL-DOMAIN] inside that file to the actual domain
```

## 4. Drop in llms.txt at site root

```bash
cp test-builds/tnj-landscape/_launch_bundle/llms-PROD.txt \
   test-builds/tnj-landscape/llms.txt
# then update [REAL-DOMAIN] inside that file to the actual domain
```

## 5. Update absolute URLs across the site

Find/replace every `scalelocal.net/test-builds/tnj-landscape` with the new
domain. Affects: meta og:url, og:image, JSON-LD @id and image fields, sitemap.xml.

```bash
# preview matches first
grep -rl "scalelocal.net/test-builds/tnj-landscape" test-builds/tnj-landscape/

# then bulk-replace (after backing up)
find test-builds/tnj-landscape -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" -o -name "*.md" \) \
  -exec sed -i 's|scalelocal.net/test-builds/tnj-landscape|REAL-DOMAIN-HERE|g' {} \;
```

## 6. Submit to search engines

- [ ] Google Search Console — add property, verify, submit `sitemap.xml`
- [ ] Bing Webmaster Tools — same

## 7. Off-site activation (per AI_Search_Visibility_Strategy.md Part 2)

- [ ] Claim/update Google Business Profile (rebrand TLC → TNJ)
- [ ] Bing Places listing
- [ ] Apple Business Connect
- [ ] Top-tier directories: Yelp, BBB, Houzz, Angi, Thumbtack, HomeAdvisor, Yellow Pages, Manta, Foursquare, Nextdoor
- [ ] Set up review request system (text customers post-job)
- [ ] First batch of GBP posts ready to publish

## 8. Verify it's working

After 24–72 hours:
- [ ] Google Search Console shows the sitemap accepted, pages indexed
- [ ] Bing Webmaster Tools same
- [ ] `site:realdomain.com` in Google returns the pages
- [ ] AI tests (per AI_Search_Visibility_Strategy.md Part 3.1) — establish baseline

## 9. Pending build work (still TODO before launch)

The full AI/SEO build per `AI_Search_Visibility_Strategy.md` hasn't shipped yet.
Trigger the full bundle by saying "ship the AI/SEO bundle" — it includes:

- [ ] Beefed-up LocalBusiness JSON-LD on every page
- [ ] Service schema on each pillar page
- [ ] FAQPage schema + visible FAQ sections (home, masonry, asphalt, landscape, all 5 town pages)
- [ ] Pricing-reality content blocks
- [ ] Embedded Google Map on each town page
- [ ] NAP consistency audit + fixes
- [ ] Add Saugus, Winchester, Woburn, Burlington, North Reading town pages

That work should ship BEFORE going live so it's all in the first crawl.

---

*Reference doc: `AI_Search_Visibility_Strategy.md` in the test-build root.*
