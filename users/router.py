from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from database.deps import GetSession
from templates import templates

from .controllers import login_user, register_user
from .deps import GetCurrentUser
from .forms import LoginForm, RegisterForm, get_user_form
from .session import remove_user_id

router = APIRouter()


@router.get("/register", name="users.register")
async def register_get(
    request: Request,
):
    form = RegisterForm(request)
    return templates.TemplateResponse(
        request, "users/register.html", {"form": form}
    )


@router.post("/register", name="users.register")
async def register_post(
    request: Request,
    session: GetSession,
):
    form = await RegisterForm.from_formdata(request)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "users/register.html", {"form": form}
        )
    user = register_user(session, request, form)
    if not user:
        return templates.TemplateResponse(
            request, "users/register.html", {"form": form}
        )
    return RedirectResponse(
        request.url_for("users.profile"),
        status.HTTP_302_FOUND,
    )


@router.get("/login", name="users.login")
async def login_get(
    request: Request,
):
    form = LoginForm(request)
    return templates.TemplateResponse(
        request, "users/login.html", {"form": form}
    )


@router.post("/login", name="users.login")
async def login_post(request: Request, session: GetSession):
    form = await LoginForm.from_formdata(request)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "users/login.html", {"form": form}
        )
    user = login_user(session, request, form)
    if not user:
        return templates.TemplateResponse(
            request, "users/login.html", {"form": form}
        )
    return RedirectResponse(
        request.url_for("users.profile"),
        status.HTTP_302_FOUND,
    )


@router.get("/profile", name="users.profile")
async def profile(request: Request, session: GetSession, user: GetCurrentUser):
    form = await get_user_form(request, session, user)
    return templates.TemplateResponse(
        request,
        "users/profile.html",
        {"user": user, "form": form},
    )


@router.post("/logout", name="users.logout")
def logout(request: Request):
    remove_user_id(request)
    return RedirectResponse(
        request.url_for("users.login"),
        status.HTTP_302_FOUND,
    )
