from fastapi import FastAPI, Request
from starlette_session import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from attendance_requirements.models import AttendanceRequirement  # noqa
from attendances.models import Attendance  # noqa
from attendances.router import router as attendances_router
from extra_attendances.models import ExtraAttendance  # noqa
from groups.models import Group  # noqa
from schedule.models import Schedule  # noqa
from schedule.router import router as schedule_router
from sections.models import Section  # noqa
from settings import settings
from students.models import Student  # noqa
from students.router import router as students_router
from teachers.models import Teacher  # noqa
from teachers.router import router as teachers_router
from templates import templates
from users.models import User  # noqa
from users.router import router as users_router

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    cookie_name="session",
)
app.add_middleware(
    CSRFProtectMiddleware,
    csrf_secret=settings.secret_key,
)

app.include_router(teachers_router, prefix="/teachers")
app.include_router(users_router, prefix="/users")
app.include_router(students_router, prefix="/students")
app.include_router(schedule_router, prefix="/schedule")
app.include_router(attendances_router, prefix="/attendances")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")
