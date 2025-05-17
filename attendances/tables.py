from fastapi import Request
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from admin.table import Table, TableField, TableQuery
from admin.widgets import DeleteButtonWidget
from sections.models import Section
from teachers.models import Teacher

from .models import Attendance


class AttendancesStudentTable(Table[Attendance]):
    fields = [
        TableField("teacher.full_name", "Преподаватель"),
        TableField("section.name", "Секция"),
        TableField("visit_time", "Дата посещения"),
    ]

    def __init__(
        self,
        request: Request,
        session: Session,
        student_id: int,
        query: TableQuery | None = None,
    ):
        self.student_id = student_id
        super().__init__(request, session, query)

    def get_query(self) -> Select:
        ilike = f"%{self.query.search}%"
        return (
            select(Attendance)
            .join(Teacher)
            .join(Section)
            .where(Attendance.student_id == self.student_id)
            .where(
                Teacher.first_name.ilike(ilike)
                | Teacher.last_name.ilike(ilike)
                | Section.name.ilike(ilike)
            )
            .order_by(Attendance.visit_time.desc())
        )


class AttendancesTeacherTable(AttendancesStudentTable):
    fields = [
        *AttendancesStudentTable.fields,
        TableField(
            lambda _: "",
            "Действия",
            DeleteButtonWidget(
                "attendances.delete",
                lambda e: {"attendance_id": e.id},
                "post",
            ),
        ),
    ]
