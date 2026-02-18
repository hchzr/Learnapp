# life-learn monorepo bootstrap

This repository contains the initial skeleton for web, API, and worker services with quality guardrails and CI.

## Repository structure

- `apps/web` — Next.js App Router UI shell with sidebar routes and dark mode toggle.
- `apps/api` — FastAPI skeleton with health endpoints, request-id logging middleware, redaction, and Alembic scaffold.
- `apps/workers` — Celery worker skeleton with `hello_world` example job.
- `packages/shared` — reusable TypeScript API contract types.
- `packages/prompts` — placeholder prompt versioning package.
- `docs` — architecture, decisions, integrations, runbook, acceptance docs.
- `infra/docker` — infrastructure scaffolding location.

## Prerequisites

- Node.js 22+
- pnpm 9+
- Python 3.12+
- Docker + Docker Compose

## Setup

```bash
pnpm install
python -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements.txt
pip install -r apps/workers/requirements.txt
cp .env.example .env
```

## Local development

Start infrastructure:

```bash
docker compose up -d
```

Run services (separate terminals):

```bash
make dev-web
make dev-api
make dev-workers
```

## Quality commands

```bash
make lint
make typecheck
make test
```

## Service checks

- API health: `curl http://localhost:8000/health`
- API v1 health: `curl http://localhost:8000/v1/health`
- API auth stub: `curl http://localhost:8000/v1/me`
- API admin job enqueue: `curl -X POST http://localhost:8000/v1/admin/jobs/hello`

## Known limitations / next steps

- No OAuth integrations yet.
- No business data models/tables yet (Alembic migration is a no-op scaffold).
- Playwright smoke test is scaffolded but not wired into CI yet.
