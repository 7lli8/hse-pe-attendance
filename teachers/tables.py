from sqlalchemy import Select, select

from admin.fields import TableField
from admin.table import Table
from admin.widgets import LinkWidget
from teachers.models import Teacher
from users.models import User


class TeachersAdminTable(Table[User]):
    fields = [
        TableField(
            "corporate_email",
            "Почта",
            LinkWidget("teachers.admin.update", lambda e: {"user_id": e.id}),
        ),
        TableField("teacher.last_name", "Фамилия"),
        TableField("teacher.first_name", "Имя"),
        TableField("teacher.middle_name", "Отчество"),
        TableField("teacher.position", "Должность"),
        TableField("teacher.is_verified", "Подтверждён"),
    ]

    def get_query(self) -> Select:
        ilike = f"%{self.query.search}%"
        return (
            select(User)
            .join(Teacher)
            .where(
                User.corporate_email.ilike(ilike)
                | Teacher.first_name.ilike(ilike)
                | Teacher.last_name.ilike(ilike)
                | Teacher.position.ilike(ilike)
            )
            .order_by(Teacher.last_name)
        )
