#!/usr/bin/env bash
# Dev launcher — runs uvicorn with auto-reload
cd "$(dirname "$0")"
export $(grep -v '^#' .env 2>/dev/null | xargs) 2>/dev/null
uvicorn app.main:app --reload --port 8000
