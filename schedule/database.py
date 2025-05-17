from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Schedule


def get_schedule_by_id(session: Session, schedule_id: int) -> Schedule:
    return session.execute(
        select(Schedule).where(Schedule.id == schedule_id)
    ).scalar_one()


def delete_schedule_by_id(session: Session, schedule_id: int):
    schedule = get_schedule_by_id(session, schedule_id)
    session.delete(schedule)
    session.commit()
