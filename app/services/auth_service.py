from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_username,
)
from app.schemas import UserCreate
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def register_user(
    db: Session,
    data: UserCreate,
) -> User:
    existing_user = (
        get_user_by_username(
            db,
            data.username,
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    hashed_password = hash_password(
        data.password
    )

    return create_user(
        db=db,
        username=data.username,
        password_hash=hashed_password,
    )


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    user = get_user_by_username(
        db,
        username,
    )

    if (
        user is None
        or not verify_password(
            password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return user


def issue_token(
    user: User,
) -> str:
    return create_access_token(
        subject=user.username
    )