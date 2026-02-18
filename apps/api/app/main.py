import logging
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from app.db import check_database_connectivity, get_db_session
from app.feature_flags import is_feature_enabled, list_feature_flags, validate_feature_flag_name
from app.logging_utils import RequestLoggerAdapter, sanitize_headers, setup_logging
from app.models import FeatureFlag
from app.settings import get_settings

setup_logging()
settings = get_settings()

app = FastAPI(title="Life Learn API")


class FeatureFlagUpdateRequest(BaseModel):
    enabled: bool

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
    call_next: RequestResponseEndpoint,
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


@app.get("/v1/me")
async def me() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"error": "Authentication stub: endpoint not yet implemented."},
    )


@app.get("/v1/feature-flags")
async def get_feature_flags(
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, dict[str, bool]]:
    flags = await list_feature_flags(session)
    return {"flags": flags}


@app.get("/v1/feature-flags/{name}")
async def get_feature_flag(
    name: str,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, object]:
    if not validate_feature_flag_name(name):
        raise HTTPException(status_code=404, detail="Unknown feature flag.")

    return {"name": name, "enabled": await is_feature_enabled(session, name)}


@app.patch("/v1/admin/feature-flags/{name}")
async def update_feature_flag(
    name: str,
    payload: FeatureFlagUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, object]:
    if not validate_feature_flag_name(name):
        raise HTTPException(status_code=404, detail="Unknown feature flag.")

    feature_flag = await session.get(FeatureFlag, name)
    if feature_flag is None:
        feature_flag = FeatureFlag(name=name, enabled=payload.enabled)
        session.add(feature_flag)
    else:
        feature_flag.enabled = payload.enabled

    await session.commit()
    await session.refresh(feature_flag)

    return {"name": feature_flag.name, "enabled": feature_flag.enabled}
