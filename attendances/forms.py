from datetime import datetime

from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators

from sections.database import get_teacher_sections


class AttendanceForm(StarletteForm):
    section_id = fields.SelectField(
        "Секция", validators=[validators.DataRequired()]
    )
    visit_time = fields.DateTimeField(
        "Время посещения",
        validators=[validators.DataRequired()],
        default=datetime.now,
    )

    submit = fields.SubmitField("Добавить посещение")

    @classmethod
    async def create(cls, request: Request, session: Session, teacher_id: int):
        sections = get_teacher_sections(session, teacher_id)
        form = await cls.from_formdata(request)
        form.section_id.choices = [
            (section.id, section.name) for section in sections
        ]
        if sections:
            form.section_id.data = sections[0].id

        return form
