from fastapi import Request
from sqlalchemy.orm import Session

from admin.table import TableQuery
from extra_attendances.database import delete_extra_attendance_by_id
from extra_attendances.forms import ExtraAttendanceForm
from extra_attendances.models import ExtraAttendance
from extra_attendances.tables import (
    ExtraAttendancesStudentTable,
    ExtraAttendancesTeacherTable,
)
from users.models import User


async def get_extra_attendance_form(request: Request):
    return await ExtraAttendanceForm.create(request)


def get_extra_attendances_table(
    request: Request,
    session: Session,
    query: TableQuery,
    user_id: int,
    user: User,
):
    if user_id == user.id:
        return ExtraAttendancesStudentTable(request, session, user_id, query)
    if user.is_admin or user.teacher and user.teacher.is_verified:
        return ExtraAttendancesTeacherTable(request, session, user_id, query)


async def save_extra_attendance_form(
    session: Session,
    form: ExtraAttendanceForm,
    student_id: int,
) -> ExtraAttendanceForm:
    if not await form.validate():
        return form
    extra_attendance = ExtraAttendance(student_id=student_id)
    form.populate_obj(extra_attendance)

    session.add(extra_attendance)
    session.commit()

    return form


def delete_extra_attendance(
    session: Session, extra_attendance_id: int
) -> ExtraAttendance | None:
    return delete_extra_attendance_by_id(session, extra_attendance_id)
