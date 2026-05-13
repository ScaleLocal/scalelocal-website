"""BD++ FastAPI app entry point.

Run dev server:
    uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .api import search, enrich, queue, export, jobs, spend
from .auth import require_auth
from .db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="BD++ API",
    version="0.2.0",
    description="Business Development prospecting engine — search, enrich, export.",
    lifespan=lifespan,
)

# CORS — allow the frontend (local dev + Vercel-deployed) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


deps = [Depends(require_auth)]
app.include_router(search.router, dependencies=deps)
app.include_router(enrich.router, dependencies=deps)
app.include_router(queue.router, dependencies=deps)
app.include_router(export.router, dependencies=deps)
app.include_router(jobs.router, dependencies=deps)
app.include_router(spend.router, dependencies=deps)
