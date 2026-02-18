import logging
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import check_database_connectivity
from app.logging_utils import (
    RequestLoggerAdapter,
    request_id_context,
    sanitize_headers,
    setup_logging,
)
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
async def request_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request.state.request_id = request_id
    token = request_id_context.set(request_id)
    logger = RequestLoggerAdapter(logging.getLogger("api.request"), {"request_id": request_id})
    logger.info(
        "request-start method=%s path=%s headers=%s",
        request.method,
        request.url.path,
        sanitize_headers(dict(request.headers)),
    )

    try:
        response = await call_next(request)
    finally:
        request_id_context.reset(token)
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
