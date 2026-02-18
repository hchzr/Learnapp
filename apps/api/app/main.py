import logging
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.auth import (
    AuthUser,
    LoginRequest,
    MeResponse,
    clear_session_cookie,
    get_current_user,
    set_session_cookie,
)
from app.db import check_database_connectivity
from app.logging_utils import RequestLoggerAdapter, sanitize_headers, setup_logging
from app.settings import Settings, get_settings

setup_logging()
settings = get_settings()

app = FastAPI(title="Life Learn API")

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


@app.post("/v1/auth/login")
async def login(
    body: LoginRequest,
    response: Response,
    auth_settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    set_session_cookie(response=response, email=body.email, settings=auth_settings)
    return {"status": "ok"}


@app.post("/v1/auth/logout")
async def logout(
    response: Response,
    auth_settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    clear_session_cookie(response=response, settings=auth_settings)
    return {"status": "ok"}


@app.get("/v1/auth/me", response_model=MeResponse)
async def auth_me(current_user: AuthUser = Depends(get_current_user)) -> MeResponse:
    return MeResponse(user=current_user)


@app.get("/v1/me", response_model=MeResponse)
async def me(current_user: AuthUser = Depends(get_current_user)) -> MeResponse:
    return MeResponse(user=current_user)
