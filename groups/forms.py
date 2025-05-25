from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators

from .models import Group


class GroupForm(StarletteForm):
    name = fields.StringField("Название группы", validators=[validators.DataRequired()])
    submit = fields.SubmitField("Сохранить")

    @classmethod
    async def create(
        cls, request: Request, session: Session, group: Group | None = None
    ):
        form = await cls.from_formdata(request, obj=group)
        return form
