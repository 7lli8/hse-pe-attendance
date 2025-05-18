from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from database.deps import GetSession
from sections.controllers import (
    delete_section,
    get_section_form,
    save_section_form,
)
from templates import templates
from users.deps import GetAdmin

router = APIRouter()


@router.get("/", name="sections.admin.list")
def sections_list():
    pass


@router.get("/create", name="sections.admin.create")
async def create_section_form(
    request: Request, session: GetSession, _: GetAdmin
):
    form = await get_section_form(request, session)
    return templates.TemplateResponse(
        request, "admin/sections_update.html", {"form": form}
    )


@router.post("/create", name="sections.admin.create")
async def create_section_form_post(
    request: Request, session: GetSession, _: GetAdmin
):
    form = await get_section_form(request, session)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "admin/sections_update.html", {"form": form}
        )
    await save_section_form(session, form)
    return RedirectResponse(
        request.url_for("sections.admin.list"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/{section_id}", name="sections.admin.update")
async def update_section_form(
    request: Request, session: GetSession, _: GetAdmin, section_id: int
):
    form = await get_section_form(request, session, section_id)
    return templates.TemplateResponse(
        request, "admin/sections_update.html", {"form": form}
    )


@router.post("/{section_id}", name="sections.admin.update")
async def update_section_form_post(
    request: Request,
    session: GetSession,
    _: GetAdmin,
    section_id: int,
):
    form = await get_section_form(request, session, section_id)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "admin/sections_update.html", {"form": form}
        )
    await save_section_form(session, form, section_id)
    return RedirectResponse(
        request.url_for("sections.admin.list"),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/{section_id}", name="sections.admin.delete")
def delete_section_post(
    request: Request, session: GetSession, _: GetAdmin, section_id: int
):
    if not delete_section(session, section_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="section not found"
        )
    return RedirectResponse(
        request.url_for("sections.admin.list"),
        status_code=status.HTTP_302_FOUND,
    )
