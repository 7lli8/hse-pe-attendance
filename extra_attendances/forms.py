from datetime import date

from fastapi import Request
from starlette_wtf import StarletteForm
from wtforms import ValidationError, fields, validators


class ExtraAttendanceForm(StarletteForm):
    description = fields.TextAreaField(
        "Описание события", validators=[validators.DataRequired()]
    )
    event_date = fields.DateField(
        "Дата события",
        validators=[validators.DataRequired()],
        default=date.today,
    )
    visits_count = fields.IntegerField(
        "Количество посещений",
        validators=[validators.DataRequired()],
    )

    submit = fields.SubmitField("Добавить доп. посещения")

    def validate_visits_count(self, field: fields.IntegerField):
        if not (field.data or 0) > 0:
            raise ValidationError("Посещений должно быть больше 0")

    @classmethod
    async def create(cls, request: Request):
        form = await cls.from_formdata(request)

        return form
