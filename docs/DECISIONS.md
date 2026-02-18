# Engineering Decisions

## ADR-001: Monorepo structure

**Decision:** Use a monorepo with `apps/*` for deployable services and `packages/*` for reusable code.

**Rationale:**
- Shared ownership and consistent tooling.
- Easier refactoring across frontend, workers, and shared utilities.
- Centralized CI quality checks.

## ADR-002: API framework choice

**Decision:** Use **FastAPI** for `apps/api`.

**Rationale:**
- Fast setup and strong productivity for small and medium services.
- Native type hints and automatic OpenAPI generation.
- Lightweight async-friendly model that integrates well with worker patterns.
- Lower boilerplate compared with NestJS for this initial platform baseline.

**Consequence:**
- The backend uses Python-specific tooling (`ruff`, `mypy`, `pytest`) in addition to Node tooling for other apps.
