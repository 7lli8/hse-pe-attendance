from fastapi import Request
from sqlalchemy.orm import Session

from admin.table import TableQuery
from groups.database import get_group_by_name
from users.database import get_user_by_id
from users.models import User

from .forms import StudentForm
from .models import Student
from .tables import StudentsAdminTable


def get_student(session: Session, user_id: int) -> User | None:
    return get_user_by_id(session, user_id)


def get_students_table(
    request: Request, session: Session, query: TableQuery
) -> StudentsAdminTable:
    return StudentsAdminTable(request, session, query)


def save_student_profile(
    session: Session,
    form: StudentForm,
    user: User,
):
    student = user.student

    if not student:
        student = Student(user_id=user.id)
    group = get_group_by_name(session, form.group.data)
    form.group.data = group

    form.populate_obj(student)

    session.add(student)
    session.commit()
