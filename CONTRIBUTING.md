# Contributing to TaelioAI

TaelioAI is proprietary software. Contributions are by invitation; by opening a pull request you agree that your contribution is assigned to the TaelioAI authors under the terms in [LICENSE](LICENSE).

## Setup

Follow the [Quick start](README.md#quick-start). Use Python 3.11 or 3.12; some pinned dependencies don't have wheels for newer versions yet.

## Workflow

1. Branch from `main`: `feat/<short-name>`, `fix/<short-name>` or `docs/<short-name>`.
2. Keep pull requests focused on one change, and include screenshots for UI changes.
3. Make sure CI passes. Locally:

   ```bash
   # web app
   cd frontend && npx tsc --noEmit && npm run build
   # API
   cd backend && python -c "import app.main" && alembic upgrade head
   ```

4. Use [Conventional Commits](https://www.conventionalcommits.org/) for messages, e.g. `feat(studio): add revision history`.

## Conventions

- **Product truth.** [PRODUCT.md](PRODUCT.md) records who TaelioAI is for and what it promises. Don't add claims (usage numbers, testimonials, prices, features) that aren't real.
- **Design.** UI follows the paperback-series system described in [docs/architecture.md](docs/architecture.md#web-app): genre band colours from `src/lib/series.ts` and the shared tokens in `tailwind.config.js`. Don't introduce gradients, new fonts or one-off colours.
- **Secrets.** Never commit `.env` files, API keys or databases. Add new settings to `backend/.env.example` and the README configuration table.
- **Schema changes.** Create an Alembic migration: `alembic revision --autogenerate -m "..."`.
