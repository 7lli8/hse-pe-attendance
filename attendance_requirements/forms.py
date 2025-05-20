from fastapi import Request
from sqlalchemy.orm import Session
from starlette_wtf import StarletteForm
from wtforms import fields, validators

from enums import AttestationType

from .database import get_requirements_visits

LABELS = {
    AttestationType.CREDIT: "Зачёт",
    AttestationType.AUTO_CREDIT: "Автомат",
}


class AttestationForm(StarletteForm):
    credit = fields.IntegerField(
        f"Посещений для {LABELS[AttestationType.CREDIT]}",
        validators=[validators.DataRequired(), validators.NumberRange(min=0)],
    )
    auto_credit = fields.IntegerField(
        f"Посещений для {LABELS[AttestationType.AUTO_CREDIT]}",
        validators=[validators.DataRequired(), validators.NumberRange(min=0)],
    )

    submit = fields.SubmitField("Сохранить")

    @classmethod
    async def create(cls, request: Request, session: Session) -> "AttestationForm":
        requirements = get_requirements_visits(session)
        form = await AttestationForm.from_formdata(request)
        if request.method == "GET":
            form.credit.data = requirements.get(AttestationType.CREDIT, 0)
            form.auto_credit.data = requirements.get(AttestationType.AUTO_CREDIT, 0)
        return form
