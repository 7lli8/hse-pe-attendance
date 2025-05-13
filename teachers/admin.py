from fastapi import APIRouter, HTTPException, Request, status

from admin.table import GetTableQuery
from database.deps import GetSession
from teachers.controllers import (
    get_teacher,
    get_teachers_table,
    save_teacher_profile,
)
from teachers.forms import TeacherAdminForm
from templates import templates
from users.deps import GetAdmin

router = APIRouter()


@router.get("/", name="teachers.admin.list")
def teachers_admin_get(
    request: Request,
    session: GetSession,
    query: GetTableQuery,
    _: GetAdmin,
):
    table = get_teachers_table(request, session, query)
    return templates.TemplateResponse(
        request, "admin/teachers.html", {"table": table}
    )


@router.get("/{user_id}", name="teachers.admin.update")
async def teachers_admin_update(
    request: Request,
    session: GetSession,
    user_id: int,
    _: GetAdmin,
):
    user = get_teacher(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    form = await TeacherAdminForm.from_formdata(request, obj=user.teacher)

    return templates.TemplateResponse(
        request, "admin/teachers_update.html", {"form": form, "teacher": user}
    )


@router.post("/{user_id}", name="teachers.admin.update")
async def teachers_admin_update_post(
    request: Request,
    session: GetSession,
    user_id: int,
    _: GetAdmin,
):
    user = get_teacher(session, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    form = await TeacherAdminForm.from_formdata(request, obj=user.teacher)
    save_teacher_profile(session, form, user)

    return templates.TemplateResponse(
        request, "admin/teachers_update.html", {"form": form, "teacher": user}
    )
