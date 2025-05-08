from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import validators
from wtforms.fields import EmailField, PasswordField

from students.forms import StudentForm
from teachers.forms import TeacherForm
from users.models import User


class RegisterForm(StarletteForm):
    email = EmailField("E-Mail", validators=[validators.DataRequired()])
    password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
            validators.EqualTo(
                "password_confirm", message="Пароли не совпадают"
            ),
        ],
    )
    password_confirm = PasswordField("Повторите пароль")


class LoginForm(StarletteForm):
    email = EmailField("E-Mail", validators=[validators.DataRequired()])
    password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
        ],
    )


async def get_user_form(request: Request, session: Session, user: User):
    if user.student or user.has_student_email:
        return await StudentForm.create(request, session, user)
    if user.teacher:
        return TeacherForm(request)
