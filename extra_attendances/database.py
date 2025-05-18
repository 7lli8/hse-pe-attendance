from sqlalchemy import select
from sqlalchemy.orm import Session

from extra_attendances.models import ExtraAttendance


def get_extra_attendance_by_id(
    session: Session, extra_attendance_id: int
) -> ExtraAttendance | None:
    return (
        session.execute(
            select(ExtraAttendance).where(
                ExtraAttendance.id == extra_attendance_id
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def delete_extra_attendance_by_id(
    session: Session, extra_attendance_id: int
) -> ExtraAttendance | None:
    if attendance := get_extra_attendance_by_id(session, extra_attendance_id):
        session.delete(attendance)
        session.commit()
        return attendance
