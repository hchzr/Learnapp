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
