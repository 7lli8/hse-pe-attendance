from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from database.deps import GetSession
from templates import templates
from users.deps import GetCurrentUser

from .controllers import save_student_profile
from .forms import StudentForm

router = APIRouter()


@router.post("/profile", name="students.profile")
async def profile_post(
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
