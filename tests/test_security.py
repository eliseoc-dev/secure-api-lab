from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


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