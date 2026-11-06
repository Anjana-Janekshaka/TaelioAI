@echo off
echo Starting TaelioAI API...
cd backend
if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
)
call .venv\Scripts\activate
pip install -q -r requirements.txt
if not exist .env (
  copy .env.example .env >nul
  echo Created backend\.env from .env.example. Add your GEMINI_API_KEY, then run this again.
  pause
  exit /b 1
)
alembic upgrade head
uvicorn app.main:app --reload --port 8000
pause
