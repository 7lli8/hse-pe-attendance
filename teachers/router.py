from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import get_session
from database.deps import GetSession
from templates import templates
from users.deps import GetCurrentUser

from .admin import router as admin_router
from .controllers import get_all_teachers, save_teacher_profile
from .forms import TeacherForm

router = APIRouter()
router.include_router(admin_router, prefix="/admin")


@router.get("/", response_class=HTMLResponse)
def get_teachers_list(
    request: Request, session: Annotated[Session, Depends(get_session)]
):
    teachers = get_all_teachers(session)

    return templates.TemplateResponse(
        request, "teachers/list.html", context={"teachers": teachers}
    )


@router.post("/profile", name="teachers.profile")
async def students_profile_post(
    request: Request, user: GetCurrentUser, session: GetSession
):
    form = await TeacherForm.create(request, session, user)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "users/profile.html", {"form": form}
        )
    save_teacher_profile(session, form, user)

    return RedirectResponse(
        request.url_for("users.profile"),
        status_code=status.HTTP_302_FOUND,
    )
