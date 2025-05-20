from fastapi import Request
from sqlalchemy.orm import Session

from admin.table import TableQuery
from teachers.database import get_teachers

from .database import get_section_by_id
from .forms import SectionForm
from .models import Section
from .tables import SectionsAdminTable


def get_sections_table(
    request: Request, session: Session, query: TableQuery
) -> SectionsAdminTable:
    return SectionsAdminTable(request, session, query)


async def get_section_form(
    request: Request, session: Session, section_id: int | None = None
):
    section = get_section_or_none(session, section_id)
    return await SectionForm.create(request, session, section)


async def save_section_form(
    session: Session,
    form: SectionForm,
    section_id: int | None = None,
):
    section = get_section_or_none(session, section_id) or Section()
    if not await form.validate():
        return form

    teachers_map = {teacher.user_id: teacher for teacher in get_teachers(session)}
    form.teachers.data = [
        teachers_map[int(teacher_id)] for teacher_id in form.teachers.data or []
    ]

    form.populate_obj(section)
    session.add(section)
    session.commit()

    form.teachers.data = [teacher.user_id for teacher in section.teachers]

    return form


def get_section_or_none(session: Session, section_id: int | None):
    if section_id:
        return get_section_by_id(session, section_id)


def delete_section(session: Session, section_id: int) -> Section | None:
    if section := get_section_by_id(session, section_id):
        session.delete(section)
        session.commit()
        return section
