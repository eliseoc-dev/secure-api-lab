from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import (
    create_user,
    get_user_by_username,
    get_users,
)
from app.schemas import (
    LoginRequest,
    UserCreate,
    UserResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    existing = get_user_by_username(
        db,
        data.username,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    return create_user(
        db,
        data,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
):
    return get_users(db)


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = get_user_by_username(
        db,
        data.username,
    )

    if (
        user is None
        or user.password != data.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    return {
        "message": "Login successful.",
        "user_id": user.id,
        "is_admin": user.is_admin,
    }