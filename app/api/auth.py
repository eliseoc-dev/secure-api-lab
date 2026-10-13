from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
)
from app.database.session import get_db
from app.models.user import User
from app.schemas import (
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    issue_token,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(
        db,
        data,
    )


@router.post(
    "/token",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    token = issue_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(
    user: User = Depends(
        get_current_user
    ),
):
    return user