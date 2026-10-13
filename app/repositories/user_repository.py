from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserCreate


def create_user(
    db: Session,
    data: UserCreate,
) -> User:
    user = User(
        username=data.username,
        password=data.password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = select(User).where(
        User.username == username
    )

    return db.scalar(statement)


def get_users(
    db: Session,
) -> list[User]:
    statement = select(User)

    return list(
        db.scalars(statement).all()
    )