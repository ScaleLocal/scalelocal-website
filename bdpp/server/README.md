# BD++ Backend

FastAPI server that powers the BD++ web app. Re-uses the engine logic from the parent
package; new "queue / spend / jobs" tables persist to Postgres in prod (SQLite locally).

## Local dev

```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp dotenv.example .env   # then fill in keys
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for the Swagger UI.

## API surface

| Method | Path                | Purpose                                            |
|--------|---------------------|----------------------------------------------------|
| POST   | /api/search         | Start discovery; appends DISCOVERED rows to queue  |
| POST   | /api/enrich         | Process selected / first-N DISCOVERED rows         |
| GET    | /api/queue          | List queue items (filter by status)                |
| GET    | /api/queue/counts   | Counts per status                                  |
| POST   | /api/queue/delete   | Soft-delete items (status -> DELETED)              |
| POST   | /api/queue/reset    | Re-set items to any status (e.g. re-enrich)        |
| GET    | /api/export         | Stream CSV in BD++ format                          |
| GET    | /api/jobs/{id}      | Poll background-job status                         |
| GET    | /api/jobs           | List recent jobs                                   |
| GET    | /api/spend          | Today / 7d / lifetime spend                        |

## Deploy targets

- **Render (cheap, simple)** — point at this dir, set env vars, attach a Postgres add-on.
- **Fly.io** — `fly launch` from this dir.
- **Railway / Vercel (with Python runtime)** — also works.

Database URL switches between SQLite (dev) and Postgres (prod) automatically via DATABASE_URL.

## Contact-resolver behavior

Hybrid: free path first, Apollo fallback if either slot is empty. To enable Apollo,
set `APOLLO_API_KEY` in `.env`. Free path uses:

1. "Reports to: <Name>" parse from JD
2. Company website /team scrape
3. Google CSE LinkedIn search (only if `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` set)
