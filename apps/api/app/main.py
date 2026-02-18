import logging
import uuid

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import check_database_connectivity
from app.logging_utils import RequestLoggerAdapter, sanitize_headers, setup_logging
from app.settings import get_settings

setup_logging()
settings = get_settings()

app = FastAPI(title="Life Learn API")

if settings.app_env == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["content-type", "authorization"],
        allow_credentials=True,
    )


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    logger = RequestLoggerAdapter(logging.getLogger("api.request"), {"request_id": request_id})
    logger.info(
        "request-start method=%s path=%s headers=%s",
        request.method,
        request.url.path,
        sanitize_headers(dict(request.headers)),
    )

    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    logger.info("request-end status_code=%s", response.status_code)
    return response


@app.get("/health")
async def health(_: None = Depends(check_database_connectivity)) -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/health")
async def v1_health(_: None = Depends(check_database_connectivity)) -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/me")
async def me() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"error": "Authentication stub: endpoint not yet implemented."},
    )


@app.get("/v1/integrations/status")
async def integrations_status() -> dict[str, list[dict[str, str | bool]]]:
    providers: list[dict[str, str | bool]] = [
        {"provider": "notion", "connected": False},
        {"provider": "todoist", "connected": False},
        {"provider": "google_drive", "connected": False},
        {"provider": "habitica", "connected": False},
        {"provider": "anki", "connected": False},
    ]
    return {"providers": providers}
