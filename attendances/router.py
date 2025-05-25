from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from admin.table import GetTableQuery
from database.deps import GetSession
from templates import templates
from users.database import get_user_by_id
from users.deps import GetCurrentUser, GetTeacher, get_unauthorized_and_redirect

from .controllers import (
    delete_attendance,
    get_attendance_form,
    get_attendances_table,
    save_attendance_form,
)
from students.export import get_attestation_progress
from attendance_requirements.database import get_requirements_visits

router = APIRouter()


@router.get("/{user_id}", name="attendances.student.list")
def attendance_list(
    request: Request,
    session: GetSession,
    user_id: int,
    user: GetCurrentUser,
    query: GetTableQuery,
):
    student = get_user_by_id(session, user_id)
    if not student or not student.student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )
    table = get_attendances_table(request, session, query, user_id, user)
    if not table:
        raise get_unauthorized_and_redirect(request)

    requirements = get_requirements_visits(session)
    total = student.student.total_attendances
    progress = get_attestation_progress(total, requirements)
    return templates.TemplateResponse(
        request,
        "attendances/list.html",
        {
            "student": student,
            "table": table,
            "progress": progress,
        },
    )


@router.get("/create/{user_id}", name="attendances.create")
async def attendance_create_get(
    request: Request, session: GetSession, user_id: int, user: GetTeacher
):
    form = await get_attendance_form(request, session, user.id)
    return templates.TemplateResponse(
        request, "attendances/create.html", {"form": form}
    )


@router.post("/create/{user_id}", name="attendances.create")
async def attendance_create_post(
    request: Request, session: GetSession, user_id: int, user: GetTeacher
):
    form = await get_attendance_form(request, session, user.id)
    if not form.validate():
        return templates.TemplateResponse(
            request, "attendances/create.html", {"form": form}
        )

    save_attendance_form(session, form, user_id, user.id)

    link = "students.admin.list" if user.is_admin else "students.list"

    return RedirectResponse(
        request.url_for(link),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/delete/{attendance_id}", name="attendances.delete")
async def attendance_delete(
    request: Request, session: GetSession, attendance_id: int, _: GetTeacher
):
    attendance = delete_attendance(session, attendance_id)
    return RedirectResponse(
        request.url_for("attendances.student.list", user_id=attendance.student_id),
        status_code=status.HTTP_302_FOUND,
    )
