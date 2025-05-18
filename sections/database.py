from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Section


def get_section_by_id(session: Session, section_id: int) -> Section | None:
    return (
        session.execute(select(Section).where(Section.id == section_id))
        .unique()
        .scalar_one_or_none()
    )


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


def delete_section_by_id(session: Session, section_id: int) -> Section | None:
    if section := get_section_by_id(session, section_id):
        session.delete(section)
        session.commit()
        return section
