from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200


def test_root():
    response = client.get("/")

    assert response.status_code == 200


def test_users_endpoint_exists():
    response = client.get(
        "/users"
    )

    assert response.status_code == 200