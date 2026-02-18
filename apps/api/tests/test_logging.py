import logging

from fastapi.testclient import TestClient

from app.db import check_database_connectivity
from app.main import app


async def _fake_db_check() -> None:
    return None


client = TestClient(app)


def test_request_logs_include_request_id_and_redact_sensitive_headers(caplog) -> None:
    app.dependency_overrides[check_database_connectivity] = _fake_db_check
    with caplog.at_level(logging.INFO):
        try:
            response = client.get(
                "/health",
                headers={
                    "x-request-id": "req-123",
                    "authorization": "Bearer secret-token",
                },
            )
        finally:
            app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-123"

    request_logs = [record for record in caplog.records if record.name == "api.request"]
    assert len(request_logs) >= 2
    assert all(getattr(record, "request_id", "-") == "req-123" for record in request_logs)

    start_log = next(record for record in request_logs if "request-start" in record.getMessage())
    message = start_log.getMessage()
    assert "[REDACTED]" in message
    assert "secret-token" not in message
