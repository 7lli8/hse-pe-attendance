from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators

from groups.database import get_groups_choices
from users.models import User


class StudentForm(StarletteForm):
    first_name = fields.StringField("Имя", validators=[validators.DataRequired()])
    last_name = fields.StringField("Фамилия", validators=[validators.DataRequired()])
    middle_name = fields.StringField("Отчество", validators=[])

    course = fields.SelectField(
        "Курс",
        validators=[validators.DataRequired()],
        coerce=int,
        choices=("1", "2"),
    )

    group = fields.SelectField("Группа", validators=[validators.DataRequired()])

    @classmethod
    async def create(
        cls, request: Request, session: Session, user: User
    ) -> "StudentForm":
        groups = get_groups_choices(session)
        form = await StudentForm.from_formdata(request, obj=user.student)
        form.group.choices = groups
        if user.student:
            form.group.data = user.student.group.name

        return form
