# Architecture Overview

## Monorepo Layout

- `apps/web`: Next.js App Router frontend (TypeScript, Tailwind, shadcn-style UI primitives).
- `apps/api`: FastAPI service for REST endpoints, settings, middleware, and migrations.
- `apps/workers`: Celery workers for background jobs.
- `packages/shared`: shared TypeScript types (API contracts).
- `packages/prompts`: versioned prompt templates placeholder.
- `infra/docker`: infrastructure assets and Docker-related scaffolding.

## Runtime Components

- **Web** calls the **API** via `NEXT_PUBLIC_API_BASE_URL`.
- **API** serves synchronous endpoints and enqueues async work to **Redis/Celery**.
- **Workers** consume tasks from Redis and execute background jobs.
- **PostgreSQL** is the source of truth for canonical application data.

## Why FastAPI

FastAPI was chosen for fast iteration, typed request/response contracts, and simple integration with Pydantic settings and Celery workers.

## Guardrails Included

- Request logging middleware with per-request `request_id`.
- Header redaction for sensitive key names (`token`, `authorization`, `cookie`).
- Environment-driven CORS behavior (development permissive, non-development restricted).
- CI checks for lint, type-checking, and tests across web + python services.

## Persistence Layer (PR #2)

- API now uses SQLAlchemy 2.0 async engine/session (`AsyncSession`) with request-scoped dependency injection.
- Canonical schema includes `users`, `external_accounts`, and `audit_logs` managed through Alembic migrations.
- `external_accounts` tokens are encrypted at rest via an application-level SQLAlchemy type backed by `ENCRYPTION_KEY`.
- Health endpoints validate database connectivity via `SELECT 1` before returning `{"status": "ok"}`.

## Feature Flags (PR #7)

- API stores runtime feature toggles in PostgreSQL table `feature_flags`.
- Supported flags: `notion_sync`, `todoist_sync`, `drive_ingestion`, `anki`, `exercises`, `planner`.
- API exposes read endpoints at `/v1/feature-flags` and `/v1/feature-flags/{name}`, plus admin toggle endpoint `PATCH /v1/admin/feature-flags/{name}`.
- Frontend fetches flags from the API and hides disabled modules from sidebar navigation and integrations UI.
