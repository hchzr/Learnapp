import json
import logging
import re
from collections.abc import MutableMapping
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


def _redact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, str) and SENSITIVE_PATTERN.search(key):
            redacted[key] = "[REDACTED]"
        elif isinstance(value, str):
            sanitized = SENSITIVE_VALUE_PATTERN.sub(r"\1[REDACTED]", value)
            sanitized = BEARER_PATTERN.sub("Bearer [REDACTED]", sanitized)
            redacted[key] = sanitized
        else:
            redacted[key] = value
    return redacted


class JsonRedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "run_id": getattr(record, "run_id", "-"),
            "request_id": getattr(record, "request_id", "-"),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(_redact_payload(payload))


class RunIdLoggerAdapter(logging.LoggerAdapter):  # type: ignore[type-arg]
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
        run_id = self.extra["run_id"] if self.extra and "run_id" in self.extra else "-"
        extra.setdefault("run_id", run_id)
        return msg, kwargs


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonRedactingFormatter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
