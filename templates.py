from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates

from database.session import Session
from enums import WeekDay
from users.database import get_user_by_id
from users.session import get_user_id


def get_user_from_request(request: Request) -> dict[str, Any]:
    user_id = get_user_id(request)
    if not user_id and not isinstance(user_id, int):
        return {}
    with Session() as session:
        user = get_user_by_id(session, user_id)
        if not user:
            return {}
        return {"user": user}


def get_weekday(request: Request) -> dict[str, Any]:
    return {"weekday": WeekDay, "weekdays": list(WeekDay)}


templates = Jinja2Templates(
    directory="templates",
    context_processors=[get_user_from_request, get_weekday],
)
