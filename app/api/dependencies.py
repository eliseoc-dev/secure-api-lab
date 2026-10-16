from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from app.security_logging import (
    security_logger,
)
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_username,
)
from app.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:
        payload = decode_access_token(
            token
        )

        username = payload.get("sub")

        if not username:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(
        db,
        username,
    )

    if user is None:
        raise credentials_exception

    return user


def require_admin(
    current_user: User = Depends(
        get_current_user
    ),
) -> User:
    if not current_user.is_admin:
        security_logger.warning(
         "Admin access denied "
         f"for username="
         f"{current_user.username}"
)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return current_user