from fastapi.testclient import TestClient

from app.main import app
from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

client = TestClient(app)


def test_password_is_hashed():
    password = "SecurePassword123!"

    hashed = hash_password(
        password
    )

    assert hashed != password


def test_password_verification():
    password = "SecurePassword123!"

    hashed = hash_password(
        password
    )

    assert verify_password(
        password,
        hashed,
    )

    assert not verify_password(
        "WrongPassword",
        hashed,
    )


def test_jwt_round_trip():
    token = create_access_token(
        "test_user"
    )

    payload = decode_access_token(
        token
    )

    assert payload["sub"] == "test_user"


def test_security_headers():
    response = client.get(
        "/health"
    )

    assert (
        response.headers[
            "X-Content-Type-Options"
        ]
        == "nosniff"
    )

    assert (
        response.headers[
            "X-Frame-Options"
        ]
        == "DENY"
    )

    assert (
        response.headers[
            "Referrer-Policy"
        ]
        == "no-referrer"
    )


def test_users_requires_authentication():
    response = client.get(
        "/users"
    )

    assert response.status_code == 401