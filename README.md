# Learnapp Monorepo

## Structure

- `apps/web` – Next.js TypeScript web app
- `apps/api` – FastAPI backend
- `apps/workers` – TypeScript workers
- `packages/shared` – shared TypeScript package
- `docs/` – architecture and decision records

## Quickstart

```bash
npm install
python -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements.txt
```

## Checks

```bash
npm run lint
npm run typecheck
npm run test
ruff check apps/api
mypy apps/api/app
pytest apps/api/tests
```
