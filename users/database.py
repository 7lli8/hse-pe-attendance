from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import User
from .passwords import create_password


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return (
        session.execute(select(User).where(User.id == user_id))
        .unique()
        .scalar_one_or_none()
    )


def create_user(session: Session, email: str, password: str) -> User | None:
    hashed_password = create_password(password)
    try:
        user = User(
            corporate_email=email,
            hashed_password=hashed_password,
        )
        session.add(user)
        session.commit()
        return user
    except IntegrityError:
        return


def get_user_by_email(session: Session, email: str) -> User | None:
    return (
        session.execute(select(User).where(User.corporate_email == email))
        .unique()
        .scalar()
    )
