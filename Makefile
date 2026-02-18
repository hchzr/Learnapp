.PHONY: dev dev-web dev-api dev-workers lint typecheck test

dev:
	@echo "Run each service in separate terminals: make dev-web, make dev-api, make dev-workers"

dev-web:
	pnpm --filter @life-learn/web dev

dev-api:
	cd apps/api && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-workers:
	cd apps/workers && python -m workers.cli

lint:
	pnpm -r lint
	cd apps/api && ruff check .
	cd apps/workers && ruff check .

typecheck:
	pnpm -r typecheck
	cd apps/api && mypy app
	cd apps/workers && mypy workers

test:
	pnpm -r test
	cd apps/api && pytest
	cd apps/workers && pytest
