from fastapi import Request

from users.models import User


def get_user_id(request: Request) -> int | None:
    return request.session.get("user_id")


def set_user_id(request: Request, user: User):
    request.session.update({"user_id": user.id})


def remove_user_id(request: Request):
    request.session.clear()
