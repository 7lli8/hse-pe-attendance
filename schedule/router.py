from fastapi import APIRouter, Request

from database.deps import GetSession
from templates import templates

from .admin import router as admin_router
from .controllers import get_all_sections

router = APIRouter()
router.include_router(admin_router, prefix="/admin")


@router.get("/", name="schedule")
def schedule_table(request: Request, session: GetSession):
    sections = get_all_sections(session)
    return templates.TemplateResponse(
        request, "schedule/table.html", {"sections": sections}
    )
