from starlette_wtf import StarletteForm
from wtforms import validators
from wtforms.fields import EmailField, PasswordField


class RegisterForm(StarletteForm):
    email = EmailField("E-Mail", validators=[validators.DataRequired()])
    password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
            validators.EqualTo(
                "password_confirm", message="Пароли не совпадают"
            ),
        ],
    )
    password_confirm = PasswordField("Повторите пароль")


class LoginForm(StarletteForm):
    email = EmailField("E-Mail", validators=[validators.DataRequired()])
    password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
        ],
    )
