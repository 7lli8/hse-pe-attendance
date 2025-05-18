from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from admin.table import GetTableQuery
from database.deps import GetSession
from extra_attendances.controllers import (
    delete_extra_attendance,
    get_extra_attendance_form,
    get_extra_attendances_table,
    save_extra_attendance_form,
)
from templates import templates
from users.database import get_user_by_id
from users.deps import GetCurrentUser, GetTeacher

router = APIRouter()


@router.get("/{student_id}", name="extra_attendances.student.list")
def extra_attendances_list(
    request: Request,
    session: GetSession,
    user: GetCurrentUser,
    student_id: int,
    query: GetTableQuery,
):
    student = get_user_by_id(session, student_id)
    if not student or not student.student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="student not found",
        )
    table = get_extra_attendances_table(
        request, session, query, student_id, user
    )

    return templates.TemplateResponse(
        request,
        "extra_attendances/list.html",
        {
            "table": table,
            "student": student,
        },
    )


@router.get("/create/{student_id}", name="extra_attendances.create")
async def create_form_get(
    request: Request, session: GetSession, student_id: int, _: GetTeacher
):
    student = get_user_by_id(session, student_id)
    if not student or not student.student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="student not found",
        )
    form = await get_extra_attendance_form(request)
    return templates.TemplateResponse(
        request,
        "extra_attendances/create.html",
        {"form": form, "student": student},
    )


@router.post("/create/{student_id}", name="extra_attendances.create")
async def create_form_post(
    request: Request, session: GetSession, student_id: int, _: GetTeacher
):
    student = get_user_by_id(session, student_id)
    if not student or not student.student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="student not found",
        )
    form = await get_extra_attendance_form(request)
    if not await form.validate():
        return templates.TemplateResponse(
            request,
            "extra_attendances/create.html",
            {"form": form, "student": student},
        )

    await save_extra_attendance_form(session, form, student_id)
    return RedirectResponse(
        request.url_for(
            "extra_attendances.student.list", student_id=student.id
        ),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/delete/{extra_attendance_id}", name="extra_attendances.delete")
def delete_extra_attendance_post(
    request: Request,
    session: GetSession,
    _: GetTeacher,
    extra_attendance_id: int,
):
    extra_attendance = delete_extra_attendance(session, extra_attendance_id)
    if not extra_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="extra attendance not found",
        )

    return RedirectResponse(
        request.url_for(
            "extra_attendances.student.list",
            student_id=extra_attendance.student_id,
        ),
        status_code=status.HTTP_302_FOUND,
    )
