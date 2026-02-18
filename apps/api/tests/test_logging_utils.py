import json
import logging

from app.logging_utils import JsonRedactingFormatter


def test_json_formatter_redacts_sensitive_message_fields() -> None:
    formatter = JsonRedactingFormatter()
    record = logging.LogRecord(
        name="api.request",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="authorization token=%s",
        args=("top-secret",),
        exc_info=None,
    )
    record.request_id = "req-1"

    rendered = formatter.format(record)
    payload = json.loads(rendered)

    assert payload["logger"] == "api.request"
    assert payload["request_id"] == "req-1"
    assert payload["run_id"] == "-"
    assert "top-secret" not in payload["message"]
