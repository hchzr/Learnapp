import logging
import re
from collections.abc import Mapping
from typing import Any

SENSITIVE_PATTERN = re.compile(r"(token|authorization|cookie)", re.IGNORECASE)


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return SENSITIVE_PATTERN.sub("[REDACTED]", message)


def sanitize_headers(headers: Mapping[str, str]) -> dict[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in headers.items():
        cleaned[key] = "[REDACTED]" if SENSITIVE_PATTERN.search(key) else value
    return cleaned


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        RedactingFormatter("%(asctime)s %(levelname)s %(name)s request_id=%(request_id)s %(message)s")
    )
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]


class RequestLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg: Any, kwargs: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
        extra = kwargs.setdefault("extra", {})
        extra.setdefault("request_id", self.extra.get("request_id", "-"))
        return msg, kwargs
