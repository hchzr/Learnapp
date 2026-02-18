# Local Runbook

## 1) Start infrastructure

```bash
docker compose up -d
```

This starts PostgreSQL (`localhost:5432`) and Redis (`localhost:6379`).

## 2) Web app

```bash
pnpm install
pnpm --filter @life-learn/web dev
```

Web runs on `http://localhost:3000`.

## 3) API service

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements.txt
cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health endpoint: `GET http://localhost:8000/health`.

## 4) Workers

```bash
source .venv/bin/activate
pip install -r apps/workers/requirements.txt
cd apps/workers && python -m workers.cli
```

## 5) Database migrations

```bash
source .venv/bin/activate
cd apps/api && alembic upgrade head
```

## 6) API persistence tests

```bash
source .venv/bin/activate
cd apps/api && pytest tests/test_db_persistence.py
```

## 7) Common troubleshooting

- **Port already in use:** stop conflicting process or change port.
- **Redis connection errors:** ensure `docker compose ps` reports redis healthy.
- **DB migration checks:** `cd apps/api && alembic upgrade head`.


## 8) Trigger a background job

```bash
curl -X POST http://localhost:8000/v1/admin/jobs/hello
```

Expected response: `{"status":"queued","task_id":"..."}` and the worker logs a successful `workers.hello_world` execution.
