from getpass import getpass

from app.database.connection import SessionLocal
from app.repositories.user_repository import (
    create_user,
    get_user_by_username,
)
from app.security import hash_password


def main():
    username = input(
        "Admin username: "
    ).strip()

    password = getpass(
        "Admin password: "
    )

    with SessionLocal() as db:
        existing = get_user_by_username(
            db,
            username,
        )

        if existing:
            print(
                "User already exists."
            )
            return

        create_user(
            db=db,
            username=username,
            password_hash=hash_password(
                password
            ),
            is_admin=True,
        )

    print(
        "Administrator created."
    )


if __name__ == "__main__":
    main()