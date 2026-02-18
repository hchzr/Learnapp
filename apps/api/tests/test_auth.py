from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_creates_session() -> None:
    response = client.post("/v1/auth/login", json={"email": "user@example.com"})

    assert response.status_code == 200
    set_cookie = response.headers.get("set-cookie", "")
    assert "learnapp_session=" in set_cookie
    assert "HttpOnly" in set_cookie


def test_logout_clears_session() -> None:
    response = client.post("/v1/auth/logout")

    assert response.status_code == 200
    set_cookie = response.headers.get("set-cookie", "")
    assert "learnapp_session=" in set_cookie
    assert "Max-Age=0" in set_cookie


def test_me_denies_anonymous() -> None:
    response = client.get("/v1/auth/me")

    assert response.status_code == 401


def test_me_returns_current_user_after_login() -> None:
    login_response = client.post("/v1/auth/login", json={"email": "person@example.com"})
    assert login_response.status_code == 200

    me_response = client.get("/v1/auth/me")

    assert me_response.status_code == 200
    assert me_response.json() == {"user": {"email": "person@example.com"}}
