from fastapi import APIRouter, Request, HTTPException, status
from starlette.responses import RedirectResponse
from admin.table import GetTableQuery
from database.deps import GetSession
from templates import templates
from users.deps import GetAdmin
from .tables import GroupsAdminTable
from .forms import GroupForm
from .controllers import save_group_form, delete_group, get_group_form
from .database import get_group_by_id

router = APIRouter()


@router.get("/", name="groups.admin.list")
def list_groups(
    request: Request, session: GetSession, query: GetTableQuery, _: GetAdmin
):
    table = GroupsAdminTable(request, session, query)
    return templates.TemplateResponse(request, "admin/groups.html", {"table": table})


@router.get("/create", name="groups.admin.create")
async def create_group_get(request: Request, _: GetAdmin):
    form = GroupForm(request)
    return templates.TemplateResponse(
        request, "admin/groups_update.html", {"form": form}
    )


@router.post("/create", name="groups.admin.create")
async def create_group_post(request: Request, session: GetSession, _: GetAdmin):
    form = await GroupForm.from_formdata(request)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "admin/groups_update.html", {"form": form}
        )
    save_group_form(session, form)
    return RedirectResponse(request.url_for("groups.admin.list"), status_code=302)


@router.get("/{group_id}", name="groups.admin.update")
async def update_group_get(
    request: Request,
    session: GetSession,
    group_id: int,
    _: GetAdmin,
):
    group = get_group_by_id(session, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    form = await get_group_form(request, session, group)
    return templates.TemplateResponse(
        request, "admin/groups_update.html", {"form": form}
    )


@router.post("/{group_id}", name="groups.admin.update")
async def update_group_post(
    request: Request,
    session: GetSession,
    group_id: int,
    _: GetAdmin,
):
    group = get_group_by_id(session, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    form = await get_group_form(request, session, group)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "admin/groups_update.html", {"form": form}
        )

    save_group_form(session, form, group)
    return RedirectResponse(
        request.url_for("groups.admin.list"),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/{group_id}", name="groups.admin.delete")
def delete_group_post(
    request: Request, session: GetSession, _: GetAdmin, group_id: int
):
    if not delete_group(session, group_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="group not found"
        )
    return RedirectResponse(
        request.url_for("groups.admin.list"),
        status_code=status.HTTP_302_FOUND,
    )
