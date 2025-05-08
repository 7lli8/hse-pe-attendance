from sqlalchemy.orm import Session

from groups.database import get_group_by_name
from users.models import User

from .forms import StudentForm
from .models import Student


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
