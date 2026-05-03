from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_invalid_credentials():
    response = client.post(
        "/auth/token",
        data={"username": "wrong", "password": "wrong"},
    )
    assert response.status_code == 401


def test_auth_valid_credentials():
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_agent_requires_auth():
    response = client.post("/agent/query", json={"query": "hello"})
    assert response.status_code == 401
