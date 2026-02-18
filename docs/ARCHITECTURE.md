# Learnapp Monorepo Architecture

## Repository layout

- `apps/web`: Next.js 15 + TypeScript frontend.
- `apps/api`: FastAPI backend service.
- `apps/workers`: TypeScript background workers.
- `packages/shared`: Shared TypeScript utilities used by web/workers.
- `docs/`: Architecture and engineering decision records.

## High-level flow

1. Browser requests are served by `apps/web`.
2. Frontend calls backend endpoints from `apps/api`.
3. Long-running or async jobs are delegated to `apps/workers`.
4. Shared formatting/types live in `packages/shared`.

## Quality gates

- JavaScript/TypeScript: `lint`, `typecheck`, `test` across workspaces.
- Python API: `ruff`, `mypy`, `pytest`.
- CI runs these checks on every push and pull request.
