from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    require_admin,
)
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import (
    get_users,
)
from app.schemas import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return get_users(db)