from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyCookie

from database.deps import GetSession
from users.models import User
from users.session import get_user_id

from .database import get_user_by_id

session_scheme = APIKeyCookie(name="session")


def get_current_user(
    _: Annotated[str, Depends(session_scheme)],
    request: Request,
    session: GetSession,
) -> User:
    user_id = get_user_id(request)
    if not user_id or not isinstance(user_id, int):
        raise raise_unauthorized_and_redirect()

    if user := get_user_by_id(session, cast(int, user_id)):
        return user
    raise raise_unauthorized_and_redirect()


GetCurrentUser = Annotated[User, Depends(get_current_user)]


def get_optional_user(
    request: Request,
    session: GetSession,
) -> User | None:
    user_id = get_user_id(request)
    if not user_id or not isinstance(user_id, int):
        return

    if user := get_user_by_id(session, cast(int, user_id)):
        return user


GetOptionalUser = Annotated[User | None, Depends(get_optional_user)]


def raise_unauthorized_and_redirect():
    # TODO: add redirect to login
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Authorization required to permit operation",
    )
