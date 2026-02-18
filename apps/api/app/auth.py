import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timezone

from fastapi import Cookie, Depends, HTTPException, Response, status
from pydantic import BaseModel, field_validator

from app.settings import Settings, get_settings

SESSION_COOKIE_NAME = "learnapp_session"
SESSION_TTL_SECONDS = 60 * 60 * 24 * 14


class LoginRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must be valid")
        return value


class AuthUser(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must be valid")
        return value


class MeResponse(BaseModel):
    user: AuthUser


@dataclass(frozen=True)
class SessionData:
    email: str
    issued_at: int


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * ((4 - len(value) % 4) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _sign_payload(payload: str, secret: str) -> str:
    signature = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).digest()
    return _base64url_encode(signature)


def create_session_token(email: str, secret: str) -> str:
    payload_data = {"email": email, "iat": int(datetime.now(tz=timezone.utc).timestamp())}
    payload = json.dumps(payload_data, sort_keys=True)
    encoded_payload = _base64url_encode(payload.encode("utf-8"))
    signature = _sign_payload(encoded_payload, secret)
    return f"{encoded_payload}.{signature}"


def decode_session_token(token: str, secret: str) -> SessionData | None:
    try:
        encoded_payload, signature = token.split(".", maxsplit=1)
    except ValueError:
        return None

    expected_signature = _sign_payload(encoded_payload, secret)
    if not hmac.compare_digest(signature, expected_signature):
        return None

    try:
        payload = json.loads(_base64url_decode(encoded_payload).decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None

    email = payload.get("email")
    issued_at = payload.get("iat")
    if not isinstance(email, str) or not isinstance(issued_at, int):
        return None

    if int(datetime.now(tz=timezone.utc).timestamp()) - issued_at > SESSION_TTL_SECONDS:
        return None

    return SessionData(email=email, issued_at=issued_at)


def set_session_cookie(response: Response, email: str, settings: Settings) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=create_session_token(email=email, secret=settings.session_secret),
        httponly=True,
        secure=settings.app_env == "production",
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
        path="/",
    )


def clear_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=settings.app_env == "production",
        samesite="lax",
        path="/",
    )


def get_current_user(
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    settings: Settings = Depends(get_settings),
) -> AuthUser:
    if session_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    session = decode_session_token(session_token, settings.session_secret)
    if session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return AuthUser(email=session.email)
