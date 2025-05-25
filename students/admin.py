import io
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import StreamingResponse

from admin.table import GetTableQuery, TableQuery
from attendance_requirements.database import get_requirements_visits
from attendances.controllers import get_attendances_table
from database.deps import GetSession
from templates import templates
from users.deps import GetAdmin

from .controllers import (
    get_student,
    get_students_admin_table,
    save_student_profile,
)
from .database import get_students
from .export import generate_attendance_xlsx
from .forms import StudentForm

router = APIRouter()


@router.get("/", name="students.admin.list")
def students_admin_get(
    request: Request,
    session: GetSession,
    query: Annotated[TableQuery, Query()],
    _: GetAdmin,
):
    table = get_students_admin_table(request, session, query)
    return templates.TemplateResponse(request, "admin/students.html", {"table": table})


@router.get("/export", name="students.admin.export")
def export_students_attendance(session: GetSession, _: GetAdmin):
    students = get_students(session)
    requirements = get_requirements_visits(session)
    content = generate_attendance_xlsx(students, requirements)

    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=attestation.xlsx"},
    )


@router.get("/{user_id}", name="students.admin.update")
async def students_admin_update(
    request: Request,
    session: GetSession,
    user_id: int,
    admin: GetAdmin,
    query: GetTableQuery,
):
    user = get_student(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    form = await StudentForm.create(request, session, user)
    attendances_table = get_attendances_table(request, session, query, user_id, admin)

    return templates.TemplateResponse(
        request,
        "admin/students_update.html",
        {
            "form": form,
            "student": user,
            "attendances_table": attendances_table,
        },
    )


@router.post("/{user_id}", name="students.admin.update")
async def students_admin_update_post(
    request: Request,
    session: GetSession,
    user_id: int,
    admin: GetAdmin,
    query: GetTableQuery,
):
    user = get_student(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    form = await StudentForm.create(request, session, user)
    attendances_table = get_attendances_table(request, session, query, user_id, admin)
    save_student_profile(session, form, user)

    return templates.TemplateResponse(
        request,
        "admin/students_update.html",
        {"form": form, "student": user, "attendances_table": attendances_table},
    )
