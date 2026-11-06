#!/usr/bin/env bash
set -e
echo "Starting TaelioAI API..."
cd "$(dirname "$0")/backend"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created backend/.env from .env.example. Add your GEMINI_API_KEY, then run this again."
  exit 1
fi
alembic upgrade head
uvicorn app.main:app --reload --port 8000
