from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators

from users.models import User


class TeacherForm(StarletteForm):
    first_name = fields.StringField(
        "Имя",
        validators=[validators.DataRequired()],
    )
    last_name = fields.StringField("Фамилия", validators=[validators.DataRequired()])
    middle_name = fields.StringField("Отчество", validators=[])

    position = fields.StringField("Должность", validators=[validators.DataRequired()])

    submit = fields.SubmitField("Сохранить профиль")

    @classmethod
    async def create(
        cls, request: Request, session: Session, user: User
    ) -> "TeacherForm":
        form = await TeacherForm.from_formdata(request, obj=user.teacher)
        return form


class TeacherAdminForm(TeacherForm):
    is_verified = fields.BooleanField(
        "Подтверждён", validators=[validators.DataRequired()]
    )
    submit = fields.SubmitField("Сохранить профиль преподавателя")
