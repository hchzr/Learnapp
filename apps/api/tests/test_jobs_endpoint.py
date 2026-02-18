from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_queue_hello_world_job(monkeypatch) -> None:
    def _fake_enqueue() -> str:
        return "task-123"

    monkeypatch.setattr("app.main.enqueue_hello_world", _fake_enqueue)

    response = client.post("/v1/admin/jobs/hello")

    assert response.status_code == 202
    assert response.json() == {"status": "queued", "task_id": "task-123"}
