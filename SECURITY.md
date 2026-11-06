# Security policy

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Report privately through GitHub: go to the repository's **Security** tab and choose **Report a vulnerability**. Include what you found, how to reproduce it, and the impact you expect.

We aim to acknowledge reports within 3 working days and to keep you updated until a fix ships.

## Scope

In scope: the TaelioAI API (`backend/`) and web app (`frontend/`) in this repository, including authentication, rate limiting, API keys, and handling of user content.

## Running TaelioAI safely

- Set a long random `JWT_SECRET`; the code default is a placeholder and must never be used outside local development.
- Keep provider API keys in `backend/.env` or your platform's secret store, never in the repository.
- Restrict CORS origins in `backend/app/main.py` to your real web app domains before deploying.
