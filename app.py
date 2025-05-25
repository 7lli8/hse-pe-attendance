from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette_session import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from attendance_requirements.models import AttendanceRequirement  # noqa
from attendance_requirements.router import router as attestation_router
from attendances.models import Attendance  # noqa
from attendances.router import router as attendances_router
from extra_attendances.models import ExtraAttendance  # noqa
from extra_attendances.router import router as extra_attendances_router
from groups.models import Group  # noqa
from groups.router import router as groups_router
from schedule.models import Schedule  # noqa
from schedule.router import router as schedule_router
from sections.models import Section  # noqa
from sections.router import router as sections_router
from settings import settings
from students.models import Student  # noqa
from students.router import router as students_router
from teachers.models import Teacher  # noqa
from teachers.router import router as teachers_router
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
app.include_router(extra_attendances_router, prefix="/extra_attendances")
app.include_router(sections_router, prefix="/sections")
app.include_router(attestation_router, prefix="/attestation")
app.include_router(groups_router, prefix="/groups")


@app.get("/")
def read_root(request: Request):
    return RedirectResponse(url="users/login")
