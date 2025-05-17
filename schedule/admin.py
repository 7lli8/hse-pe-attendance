from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from database.deps import GetSession
from templates import templates
from users.deps import GetAdmin

from .controllers import (
    delete_schedule,
    get_all_sections,
    get_schedule_form,
    save_schedule_form,
)

router = APIRouter()


@router.get("/", name="schedule.admin.list")
def schedule_get(request: Request, session: GetSession):
    sections = get_all_sections(session)
    return templates.TemplateResponse(
        request, "schedule/table.html", {"sections": sections}
    )


@router.get("/create", name="schedule.admin.create")
async def schedule_create_form(
    request: Request,
    session: GetSession,
    _: GetAdmin,
):
    form = await get_schedule_form(request, session)
    return templates.TemplateResponse(
        request, "admin/schedule_create.html", {"form": form}
    )


@router.post("/create", name="schedule.admin.create")
async def schedule_create_form_post(
    request: Request,
    session: GetSession,
    _: GetAdmin,
):
    form = await save_schedule_form(request, session)
    if not form.validate():
        return templates.TemplateResponse(
            request, "admin/schedule_create.html", {"form": form}
        )
    return RedirectResponse(
        request.url_for("schedule"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/{schedule_id}", name="schedule.admin.update")
async def schedule_edit_form(
    request: Request,
    session: GetSession,
    _: GetAdmin,
    schedule_id: int,
):
    form = await get_schedule_form(request, session, schedule_id)
    return templates.TemplateResponse(
        request,
        "admin/schedule_update.html",
        {"form": form, "schedule_id": schedule_id},
    )


@router.post("/{schedule_id}", name="schedule.admin.update")
async def schedule_edit_form_post(
    request: Request,
    session: GetSession,
    _: GetAdmin,
    schedule_id: int,
):
    form = await save_schedule_form(request, session, schedule_id)
    return templates.TemplateResponse(
        request,
        "admin/schedule_update.html",
        {"form": form, "schedule_id": schedule_id},
    )


@router.post("/{schedule_id}/delete", name="schedule.admin.delete")
def schedule_delete(
    request: Request, session: GetSession, _: GetAdmin, schedule_id: int
):
    delete_schedule(session, schedule_id)
    return RedirectResponse(
        request.url_for("schedule"),
        status_code=status.HTTP_302_FOUND,
    )
