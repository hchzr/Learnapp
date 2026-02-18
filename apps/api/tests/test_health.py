from fastapi.testclient import TestClient

from app.db import check_database_connectivity
from app.main import app


async def _fake_db_check() -> None:
    return None


client = TestClient(app)


def test_health() -> None:
    app.dependency_overrides[check_database_connectivity] = _fake_db_check
    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
