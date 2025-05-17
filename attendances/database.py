from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Attendance


def get_attendance_by_id(session: Session, attendance_id: int) -> Attendance:
    return (
        session.execute(
            select(Attendance).where(Attendance.id == attendance_id)
        )
        .unique()
        .scalar_one()
    )


def delete_attendance_by_id(session: Session, attendance_id: int) -> Attendance:
    attendace = get_attendance_by_id(session, attendance_id)
    session.delete(attendace)
    session.commit()
    return attendace
