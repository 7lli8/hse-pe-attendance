from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from teachers.router import router as teachers_router

from teachers.models import Teacher
from sections.models import Section
from schedule.models import Schedule
from groups.models import Group
from students.models import Student
from extra_attendances.models import ExtraAttendance
from attendances.models import Attendance
from attendance_requirements.models import AttendanceRequirement
from templates import templates

app = FastAPI()

app.include_router(teachers_router, prefix="/teachers")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")
