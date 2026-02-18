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

## UI System Foundation (PR #9)

- Web app now has a shadcn/ui configuration (`apps/web/components.json`) to standardize component generation and aliases.
- Shared UI primitives include structured cards (`CardHeader/Content/Footer`), typography variants, loading skeletons, and an error alert component.
- Next.js global `app/loading.tsx` and `app/error.tsx` route handlers consume those shared primitives so loading/error states are consistent across pages.
- Route pages render through `PageShell`, ensuring common spacing and typography across the app shell.
