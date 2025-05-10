from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyCookie

from database.deps import GetSession
from users.models import User
from users.session import get_user_id

from .database import get_user_by_id

session_scheme = APIKeyCookie(name="session")


def get_admin(
    request: Request,
    user: "GetCurrentUser",
) -> User:
    if not user.is_admin:
        raise get_forbidden_and_redirect(request)
    return user


def get_forbidden_and_redirect(request: Request):
    return HTTPException(
        status.HTTP_307_TEMPORARY_REDIRECT,
        headers={"Location": str(request.url_for("users.forbidden"))},
    )


GetAdmin = Annotated[User, Depends(get_admin)]


def get_current_user(
    _: Annotated[str, Depends(session_scheme)],
    request: Request,
    user: "GetOptionalUser",
) -> User:
    if not user:
        raise get_unauthorized_and_redirect(request)
    return user


def get_unauthorized_and_redirect(request: Request):
    # TODO: add redirect after login
    return HTTPException(
        status.HTTP_307_TEMPORARY_REDIRECT,
        headers={"Location": str(request.url_for("users.login"))},
    )


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
