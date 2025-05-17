from fastapi import Request
from sqlalchemy.orm import Session

from admin.table import TableQuery
from teachers.forms import TeacherAdminForm
from teachers.tables import TeachersAdminTable
from users.database import get_user_by_id
from users.models import User

from .database import get_teachers
from .models import Teacher


def get_teacher(session: Session, user_id: int) -> User | None:
    return get_user_by_id(session, user_id)


def get_all_teachers(session: Session) -> list[Teacher]:
    return get_teachers(session)


def get_teachers_table(
    request: Request, session: Session, query: TableQuery
) -> TeachersAdminTable:
    return TeachersAdminTable(request, session, query)


def save_teacher_profile(session: Session, form: TeacherAdminForm, user: User):
    teacher = user.teacher

    if not teacher:
        teacher = Teacher(user_id=user.id)

    form.populate_obj(teacher)
    session.add(teacher)
    session.commit()
