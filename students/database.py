from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Student


def get_students(session: Session) -> list[Student]:
    return list(
        session.execute(select(Student).order_by(Student.last_name))
        .unique()
        .scalars()
        .all()
    )
