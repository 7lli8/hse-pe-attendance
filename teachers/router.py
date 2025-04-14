from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_session
from templates import templates
from .controllers import get_teachers

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def get_teachers_list(request: Request, session: Annotated[Session, Depends(get_session)]):
    teachers = get_teachers(session)

    return templates.TemplateResponse(
        request,
        "teachers/list.html",
        context={
            "teachers": teachers
        }
    )
