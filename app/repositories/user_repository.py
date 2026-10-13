from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    username: str,
    password_hash: str,
    is_admin: bool = False,
) -> User:
    user = User(
        username=username,
        password_hash=password_hash,
        is_admin=is_admin,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = (
        select(User)
        .where(
            User.username == username
        )
    )

    return db.scalar(statement)


def get_users(
    db: Session,
) -> list[User]:
    statement = (
        select(User)
        .order_by(User.id.asc())
    )

    return list(
        db.scalars(statement).all()
    )