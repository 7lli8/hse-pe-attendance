from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Section


def get_sections(session: Session) -> list[Section]:
    return list(
        session.execute(select(Section).order_by(Section.name))
        .scalars()
        .unique()
        .all()
    )


def get_teacher_sections(session: Session, teacher_id: int) -> list[Section]:
    return list(
        session.execute(
            select(Section)
            .where(Section.teachers.any(user_id=teacher_id))
            .order_by(Section.name)
        )
        .scalars()
        .unique()
        .all()
    )
