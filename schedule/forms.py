from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import ValidationError, fields, validators

from enums import WeekDay
from sections.database import get_sections
from teachers.database import get_teachers

from .models import Schedule


class ScheduleForm(StarletteForm):
    teacher_id = fields.SelectField(
        "Преподаватель", validators=[validators.DataRequired()]
    )
    section_id = fields.SelectField(
        "Секция", validators=[validators.DataRequired()]
    )
    time_start = fields.TimeField(
        "Начало занятия", validators=[validators.DataRequired()]
    )
    time_end = fields.TimeField(
        "Конец занятия", validators=[validators.DataRequired()]
    )
    weekday = fields.SelectField(
        "День недели",
        validators=[validators.DataRequired()],
        choices=[
            (value.value, key)
            for value, key in [
                (WeekDay.MONDAY, "Понедельник"),
                (WeekDay.TUESDAY, "Вторник"),
                (WeekDay.WEDNESDAY, "Среда"),
                (WeekDay.THURSDAY, "Четверг"),
                (WeekDay.FRIDAY, "Пятница"),
            ]
        ],
    )

    submit = fields.SubmitField("Сохранить")

    def validate_time_end(self, field: fields.TimeField):
        if not self.time_start.data < field.data:
            raise ValidationError(
                "Время начала должно быть раньше времени окончания"
            )

    @classmethod
    async def create(
        cls, request: Request, session: Session, schedule: Schedule | None
    ) -> "ScheduleForm":
        sections = get_sections(session)
        teachers = get_teachers(session)

        form = await ScheduleForm.from_formdata(request, obj=schedule)
        form.teacher_id.choices = [
            (teacher.user_id, teacher.full_name) for teacher in teachers
        ]
        form.section_id.choices = [
            (section.id, section.name) for section in sections
        ]
        if schedule and request.method == "GET":
            form.weekday.data = schedule.weekday.value

        return form
