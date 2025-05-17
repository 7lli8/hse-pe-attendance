from fastapi import Request
from sqlalchemy.orm import Session

from admin.table import TableQuery
from attendances.tables import AttendancesStudentTable, AttendancesTeacherTable
from users.models import User

from .database import delete_attendance_by_id
from .forms import AttendanceForm
from .models import Attendance


async def get_attendance_form(
    request: Request, session: Session, teacher_id: int
) -> AttendanceForm:
    return await AttendanceForm.create(request, session, teacher_id)


def get_attendances_table(
    request: Request,
    session: Session,
    query: TableQuery,
    user_id: int,
    user: User,
):
    if user_id == user.id:
        return AttendancesStudentTable(request, session, user_id, query)
    if user.is_admin or user.teacher and user.teacher.is_verified:
        return AttendancesTeacherTable(request, session, user_id, query)


def save_attendance_form(
    session: Session, form: AttendanceForm, user_id: int, teacher_id: int
):
    attendance = Attendance(student_id=user_id, teacher_id=teacher_id)
    form.populate_obj(attendance)

    session.add(attendance)
    session.commit()
    return form


def delete_attendance(session: Session, attendance_id: int) -> Attendance:
    return delete_attendance_by_id(session, attendance_id)
