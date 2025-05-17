from fastapi import Request
from sqlalchemy.orm import Session

from users.database import create_user, get_user_by_email

from .forms import LoginForm, RegisterForm
from .models import User
from .passwords import is_password_valid
from .session import set_user_id


def register_user(
    session: Session, request: Request, form: RegisterForm
) -> User | None:
    user = create_user(session, form.email.data, form.password.data)
    if not user:
        form.email.errors = ("E-Mail уже используется",)
        return

    set_user_id(request, user)
    return user


def login_user(session: Session, request: Request, form: LoginForm) -> User | None:
    user = get_user_by_email(session, form.email.data)
    if not user:
        form.email.errors = ("Пользователь не найден",)
        return
    if not is_password_valid(form.password.data, user.hashed_password):
        form.password.errors = ("Неправильный пароль",)
        return

    set_user_id(request, user)
    return user
