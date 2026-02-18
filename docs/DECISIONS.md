# Engineering Decisions

## ADR-001: Monorepo structure

- **Decision:** Keep deployable services under `apps/*` and shared artifacts under `packages/*`.
- **Tradeoff:** Slightly more tooling setup now, but lower coordination overhead for cross-service work.

## ADR-002: Frontend stack

- **Decision:** Next.js App Router + TypeScript + Tailwind + shadcn-style component primitives.
- **Tradeoff:** Requires some UI boilerplate, but gives consistent component ergonomics and fast route scaffolding.

## ADR-003: Backend and workers

- **Decision:** FastAPI + Pydantic v2 for API, Celery + Redis for async jobs.
- **Tradeoff:** Python runtime split between API and workers, but shared tooling (`ruff`, `pytest`, `mypy`) keeps maintenance simple.

## ADR-004: Package management

- **Decision:** Use `pnpm` for JS workspaces and `pip + requirements.txt` for Python apps.
- **Tradeoff:** Two ecosystem toolchains, but avoids premature complexity from introducing uv/poetry in bootstrap.


## ADR-005: Database baseline and encrypted provider credentials

- **Decision:** Establish PostgreSQL + Alembic as the canonical persistence layer with SQLAlchemy async sessions.
- **Decision:** Store external provider tokens encrypted at rest using a shared `ENCRYPTION_KEY`-derived Fernet key.
- **Tradeoff:** App-level encryption keeps implementation simple and portable, but key rotation will require a migration plan.
