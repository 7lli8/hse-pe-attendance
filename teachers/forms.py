from starlette_wtf import StarletteForm
from wtforms import fields, validators


class TeacherForm(StarletteForm):
    first_name = fields.StringField(
        "Имя",
        validators=[validators.DataRequired()],
    )
    last_name = fields.StringField(
        "Фамилия", validators=[validators.DataRequired()]
    )
    middle_name = fields.StringField("Отчество", validators=[])

    position = fields.StringField(
        "Должность", validators=[validators.DataRequired()]
    )


class TeacherAdminForm(TeacherForm):
    is_verified = fields.BooleanField(
        "Подтверждён", validators=[validators.DataRequired()]
    )
    submit = fields.SubmitField("Сохранить профиль преподавателя")
