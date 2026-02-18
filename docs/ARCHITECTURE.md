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

## Authentication and Session Flow (PR #3)

- API exposes `POST /v1/auth/login`, `POST /v1/auth/logout`, and `GET /v1/auth/me`.
- Login issues a signed `learnapp_session` cookie containing user identity (`email`) and issue timestamp.
- Session cookie policy: `HttpOnly`, `SameSite=Lax`, and `Secure` only in production.
- `get_current_user` is the shared FastAPI dependency for protected API handlers.
- Web middleware protects app routes by requiring the session cookie and redirects anonymous users to `/login`.
- Web header resolves current identity by calling `/v1/auth/me` and displays signed-in email.
