from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators

from students.forms import StudentForm
from teachers.forms import TeacherForm
from users.models import User


class RegisterForm(StarletteForm):
    email = fields.EmailField("E-Mail", validators=[validators.DataRequired()])
    password = fields.PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
            validators.EqualTo("password_confirm", message="Пароли не совпадают"),
        ],
    )
    password_confirm = fields.PasswordField("Повторите пароль")
    submit = fields.SubmitField("Создать аккаунт")


class LoginForm(StarletteForm):
    email = fields.EmailField("E-Mail", validators=[validators.DataRequired()])
    password = fields.PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
        ],
    )
    submit = fields.SubmitField("Войти в аккаунт")


async def get_user_form(request: Request, session: Session, user: User):
    if user.student or user.has_student_email:
        return await StudentForm.create(request, session, user)
    if user.teacher or user.has_teacher_email:
        return await TeacherForm.from_formdata(request, obj=user.teacher)
