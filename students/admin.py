from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request, status

from admin.table import TableQuery
from database.deps import GetSession
from templates import templates
from users.deps import GetAdmin

from .controllers import get_student, get_students_table, save_student_profile
from .forms import StudentForm

router = APIRouter()


@router.get("/", name="students.admin.list")
def students_admin_get(
    request: Request,
    session: GetSession,
    query: Annotated[TableQuery, Query()],
    _: GetAdmin,
):
    table = get_students_table(request, session, query)
    return templates.TemplateResponse(
        request, "admin/students.html", {"table": table}
    )


@router.get("/{user_id}", name="students.admin.update")
async def students_admin_update(
    request: Request,
    session: GetSession,
    user_id: int,
    _: GetAdmin,
):
    user = get_student(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    form = await StudentForm.create(request, session, user)

    return templates.TemplateResponse(
        request, "admin/students_update.html", {"form": form, "student": user}
    )


@router.post("/{user_id}", name="students.admin.update")
async def students_admin_update_post(
    request: Request,
    session: GetSession,
    user_id: int,
    _: GetAdmin,
):
    user = get_student(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    form = await StudentForm.create(request, session, user)
    save_student_profile(session, form, user)

    return templates.TemplateResponse(
        request, "admin/students_update.html", {"form": form, "student": user}
    )
