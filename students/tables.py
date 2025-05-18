from sqlalchemy import Select, select

from admin.table import Table, TableField
from admin.widgets import (
    ContainerWidget,
    IconButtonWidget,
    LinkWidget,
    StringWidget,
)
from groups.models import Group
from users.models import User

from .models import Student

common_fields = []


class StudentsCommonTable(Table[User]):
    fields = [
        TableField("student.last_name", "Фамилия"),
        TableField("student.first_name", "Имя"),
        TableField("student.middle_name", "Отчество"),
        TableField("student.group.name", "Группа"),
        TableField(
            "student.total_attendances",
            "Посещений",
            ContainerWidget(
                [
                    StringWidget(),
                    IconButtonWidget(
                        "attendances.create",
                        lambda e: {"user_id": e.id},
                        icon="fa-plus",
                    ),
                    IconButtonWidget(
                        "extra_attendances.create",
                        lambda e: {"student_id": e.id},
                        icon="fa-plus",
                        label="Доп.",
                    ),
                ]
            ),
        ),
    ]

    def get_query(self) -> Select:
        ilike = f"%{self.query.search}%"
        return (
            select(User)
            .join(Student)
            .join(Group)
            .where(
                User.corporate_email.ilike(ilike)
                | Student.first_name.ilike(ilike)
                | Student.last_name.ilike(ilike)
                | Group.name.ilike(ilike)
            )
            .order_by(Student.last_name)
        )


class StudentsAdminTable(StudentsCommonTable):
    fields = [
        TableField(
            "corporate_email",
            "Почта",
            LinkWidget("students.admin.update", lambda e: {"user_id": e.id}),
        ),
        *StudentsCommonTable.fields,
    ]


class StudentsTeacherTable(StudentsCommonTable):
    fields = [
        TableField(
            "corporate_email",
            "Почта",
            LinkWidget("attendances.student.list", lambda e: {"user_id": e.id}),
        ),
        *StudentsCommonTable.fields,
    ]
