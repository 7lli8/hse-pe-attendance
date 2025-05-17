from fastapi import Request
from sqlalchemy.orm import Session

from sections.database import get_sections
from sections.models import Section

from .database import delete_schedule_by_id, get_schedule_by_id
from .forms import ScheduleForm
from .models import Schedule


def get_all_sections(session: Session) -> list[Section]:
    return get_sections(session)


async def get_schedule_form(
    request: Request, session: Session, schedule_id: int | None = None
) -> ScheduleForm:
    schedule = get_schedule_by_id(session, schedule_id) if schedule_id else None
    return await ScheduleForm.create(request, session, schedule)


async def save_schedule_form(
    request: Request,
    session: Session,
    schedule_id: int | None = None,
) -> ScheduleForm:
    schedule = (
        get_schedule_by_id(session, schedule_id) if schedule_id else Schedule()
    )

    form = await ScheduleForm.create(request, session, schedule)
    if not await form.validate():
        return form

    form.populate_obj(schedule)

    session.add(schedule)
    session.commit()
    return form


def delete_schedule(session: Session, schedule_id: int):
    delete_schedule_by_id(session, schedule_id)
