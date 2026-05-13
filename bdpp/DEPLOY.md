# BD++ Sniper — Deployment Guide

How to get **https://scalelocal.net/sniper** live, end-to-end.

---

## Architecture

```
  scalelocal.net (Vercel)
      ├── /sniper       → static sniper.html
      └── /sniper/api/* → proxy → bdpp-api.onrender.com/api/*

  bdpp-api.onrender.com (Render)
      ├── FastAPI app (Docker)
      └── Postgres (Render add-on)
```

---

## Step 1 — Push backend to GitHub

```bash
cd C:\Users\matty\OneDrive\ScaleLocal\BDPlusPlus
git init
git remote add origin git@github.com:ScaleLocal/bdpp-server.git
git add server/ config/
git commit -m "Initial BD++ backend"
git push -u origin main
```

The `config/fortune500.txt` blacklist needs to ship with the backend, hence pushing
both `server/` and `config/`.

---

## Step 2 — Deploy backend to Render

1. Log into https://render.com
2. Click **New > Blueprint**, point at your `bdpp-server` repo
3. Render reads `server/render.yaml` and provisions:
   - Web service `bdpp-api` (Docker, free tier)
   - Postgres `bdpp-postgres` (free tier — 90-day expiration!)
4. After provisioning, open the `bdpp-api` service → **Environment** tab and fill in:
   - `MILLIONVERIFIER_TOKEN` = `<MILLIONVERIFIER_TOKEN from your secrets vault>`
   - `OUTSCRAPER_TOKEN` = `<OUTSCRAPER_TOKEN from your secrets vault>`
   - `GOOGLE_API_KEY` = (your existing key — but consider provisioning a new one without IP restrictions specifically for the server)
   - `APOLLO_API_KEY` = (when you upgrade Apollo to a paid tier)
5. Render auto-generated `BDPP_ACCESS_TOKEN` — **copy this value**, you'll need it for the frontend.
6. Wait ~5 min for the first build. Final URL will be something like `https://bdpp-api-xxxxx.onrender.com` — note this URL.

---

## Step 3 — Add the sniper page to scalelocal.net

1. Copy `web/sniper.html` into your existing `scalelocal-website` repo at `public/sniper.html`
2. Copy `web/vercel.json` rewrites into your existing `vercel.json` (merge `rewrites` array if you already have one)
3. **Update the rewrite destination** in your `vercel.json`:
   ```json
   { "source": "/sniper/api/:path*", "destination": "https://bdpp-api-xxxxx.onrender.com/api/:path*" }
   ```
   (use the actual Render URL from step 2)
4. **Update the API_BASE in `sniper.html`** — change `const API_BASE = "http://127.0.0.1:8765";` to `const API_BASE = "/sniper/api";` so the frontend uses the Vercel rewrite proxy (no CORS issues)
5. Git commit + push to your `scalelocal-website` repo. Vercel auto-deploys.

---

## Step 4 — First login

1. Visit https://scalelocal.net/sniper
2. Browser prompts for token — paste the `BDPP_ACCESS_TOKEN` from step 2.5
3. Token is stored in browser localStorage; you won't be prompted again on this device.

---

## Step 5 — Smoke test

1. Click **Run Search** with defaults (Manufacturing / Controls Engineer + Electrical Engineer / 5 NE states / 72h)
2. Wait ~10s — queue table should populate with ~10-20 companies
3. Click **Enrich Queue** with default $6 budget
4. Wait — rows flip ENRICHING → ENRICHED as backend works
5. Click **Export ENRICHED** — CSV downloads

---

## Caveats

- **Render free tier sleeps after 15 min inactivity.** First request after sleep wakes the dyno (~15s cold-start). Upgrade to $7/mo Starter for always-on.
- **Render Postgres free tier expires after 90 days.** Migrate to a $7/mo Starter Postgres before then, or use Supabase / Neon (both have permanent free tiers).
- **Google API key IP restriction.** Your current key is IP-restricted (per API_Keys.md). When called from Render's dynamic IPs, it will fail. Either remove the IP restriction or provision a new key with just an HTTP referrer restriction (`scalelocal.net/*`) instead.
- **Single-password auth is shared-secret.** If you give the token to a teammate, they have your access. Future: magic-link or per-user JWT.

---

## Total cost

- **Free** for ~the first 90 days (Render free + Postgres free)
- **$14/mo** after upgrading to always-on web + always-on Postgres
- **API costs** (variable): MillionVerifier ~$0.003/check, Apollo ~$0.10/credit when enabled

