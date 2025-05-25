from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from database.deps import GetSession
from templates import templates
from users.deps import GetAdmin

from .controllers import save_attestation
from .forms import AttestationForm

router = APIRouter()


@router.get("/", name="attestation.admin")
async def attestation_get(request: Request, session: GetSession, _: GetAdmin):
    form = await AttestationForm.create(request, session)
    return templates.TemplateResponse(
        request,
        "attendance_requirements/form.html",
        {"form": form},
    )


@router.post("/", name="attestation.admin")
async def attestation_post(request: Request, session: GetSession, _: GetAdmin):
    form = await AttestationForm.create(request, session)
    if not await form.validate():
        return templates.TemplateResponse(
            request, "attendance_requirements/form.html", {"form": form}
        )

    save_attestation(
        session,
        form.credit.data,
        form.auto_credit.data,
    )
    return RedirectResponse(
        request.url_for("attestation.admin"), status_code=status.HTTP_302_FOUND
    )
