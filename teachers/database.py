from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Teacher


def get_teachers(session: Session) -> list[Teacher]:
    return list(
        session.scalars(select(Teacher).order_by(Teacher.last_name)).all()
    )
