from fastapi import Request
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from admin.table import Table, TableField, TableQuery
from admin.widgets import DeleteButtonWidget

from .models import ExtraAttendance


class ExtraAttendancesStudentTable(Table[ExtraAttendance]):
    fields = [
        TableField("description", "Описание"),
        TableField("event_date", "Дата события"),
        TableField("visits_count", "Количество посещений"),
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
            select(ExtraAttendance)
            .where(ExtraAttendance.student_id == self.student_id)
            .where(ExtraAttendance.description.ilike(ilike))
            .order_by(ExtraAttendance.event_date.desc())
        )


class ExtraAttendancesTeacherTable(ExtraAttendancesStudentTable):
    fields = [
        *ExtraAttendancesStudentTable.fields,
        TableField(
            lambda _: "",
            "Действия",
            DeleteButtonWidget(
                "extra_attendances.delete",
                lambda e: {"extra_attendance_id": e.id},
                "post",
            ),
        ),
    ]

    add_link_name = "extra_attendances.create"
