from sqlalchemy import Select, select

from admin.table import Table, TableField
from admin.widgets import LinkWidget
from groups.models import Group
from users.models import User

from .models import Student


class StudentsAdminTable(Table[User]):
    fields = [
        TableField(
            "corporate_email",
            "Почта",
            LinkWidget("students.admin.update", lambda e: {"user_id": e.id}),
        ),
        TableField("student.last_name", "Фамилия"),
        TableField("student.first_name", "Имя"),
        TableField("student.middle_name", "Отчество"),
        TableField("student.group.name", "Группа"),
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
