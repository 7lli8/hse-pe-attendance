from fastapi import Request
from markupsafe import Markup
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators, widgets

from sections.models import Section
from teachers.database import get_teachers


class CheckboxListWidget(widgets.ListWidget):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        for subfield in field:
            html.append(
                f'<label class="checkbox">{subfield(checked=subfield.data in field.data)}\n{subfield.label.text}</label>'
            )
        checkboxes = "".join(html)
        return Markup(f'<div class="checkboxes">{checkboxes}</div>')


class SectionForm(StarletteForm):
    name = fields.StringField(
        "Название", validators=[validators.DataRequired()]
    )
    teachers = fields.SelectMultipleField(
        "Преподаватели",
        validators=[validators.DataRequired()],
        widget=CheckboxListWidget(),
        option_widget=widgets.CheckboxInput(),
    )
    submit = fields.SubmitField("Сохранить секцию")

    @classmethod
    async def create(
        cls, request: Request, session: Session, section: Section | None = None
    ):
        form = await cls.from_formdata(request, obj=section)
        teachers = get_teachers(session)

        form.teachers.choices = [
            (teacher.user_id, teacher.full_name) for teacher in teachers
        ]
        if section and request.method == "GET":
            form.teachers.data = [
                teacher.user_id for teacher in section.teachers
            ]

        return form
