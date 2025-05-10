from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from database.deps import GetSession
from templates import templates
from users.deps import GetCurrentUser

from .admin import router as admin_router
from .controllers import save_student_profile
from .forms import StudentForm

router = APIRouter()

router.include_router(admin_router, prefix="/admin")


@router.post("/profile", name="students.profile")
async def students_profile_post(
    request: Request, user: GetCurrentUser, session: GetSession
):
    form = await StudentForm.create(request, session, user)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "users/profile.html", {"form": form}
        )
    save_student_profile(session, form, user)

    return RedirectResponse(
        request.url_for("users.profile"),
        status_code=status.HTTP_302_FOUND,
    )
