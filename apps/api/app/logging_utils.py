import contextvars
import json
import logging
import re
from collections.abc import Mapping, MutableMapping
from datetime import datetime, timezone
from typing import Any

SENSITIVE_PATTERN = re.compile(
    r"(token|authorization|cookie|secret|password|apikey|api_key)",
    re.IGNORECASE,
)
SENSITIVE_VALUE_PATTERN = re.compile(
    r"((?:token|authorization|cookie|secret|password|apikey|api_key)\s*[:=]\s*)([^,\s]+)",
    re.IGNORECASE,
)
BEARER_PATTERN = re.compile(r"bearer\s+[a-z0-9._~-]+", re.IGNORECASE)
request_id_context: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


def _redact_string(value: str) -> str:
    redacted = SENSITIVE_VALUE_PATTERN.sub(r"\1[REDACTED]", value)
    redacted = BEARER_PATTERN.sub("Bearer [REDACTED]", redacted)
    return redacted


def _redact_value(key: str, value: Any) -> Any:
    if SENSITIVE_PATTERN.search(key):
        return "[REDACTED]"
    if isinstance(value, str):
        return _redact_string(value)
    return value


def sanitize_headers(headers: Mapping[str, str]) -> dict[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in headers.items():
        cleaned[key] = _redact_value(key, value)
    return cleaned


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = request_id_context.get()
        if not hasattr(record, "run_id"):
            record.run_id = "-"
        return True


class JsonRedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
            "run_id": getattr(record, "run_id", "-"),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        redacted_payload = {key: _redact_value(key, value) for key, value in payload.items()}
        return json.dumps(redacted_payload)


class RequestLoggerAdapter(logging.LoggerAdapter):  # type: ignore[type-arg]
    def process(
        self,
        msg: Any,
        kwargs: MutableMapping[str, Any],
    ) -> tuple[Any, MutableMapping[str, Any]]:
        extra_value = kwargs.setdefault("extra", {})
        extra: MutableMapping[str, Any]
        if isinstance(extra_value, MutableMapping):
            extra = extra_value
        else:
            extra = {}
            kwargs["extra"] = extra
        request_id = (
            self.extra["request_id"]
            if self.extra and "request_id" in self.extra
            else request_id_context.get()
        )
        extra.setdefault("request_id", request_id)
        return msg, kwargs


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonRedactingFormatter())
    handler.addFilter(RequestContextFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
