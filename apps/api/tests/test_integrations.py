from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_integrations_status() -> None:
    response = client.get("/v1/integrations/status")

    assert response.status_code == 200
    assert response.json() == {
        "providers": [
            {"provider": "notion", "connected": False},
            {"provider": "todoist", "connected": False},
            {"provider": "google_drive", "connected": False},
            {"provider": "habitica", "connected": False},
            {"provider": "anki", "connected": False},
        ]
    }
