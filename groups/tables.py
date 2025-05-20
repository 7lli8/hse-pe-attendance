from fastapi import Request
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from admin.table import Table, TableField, TableQuery
from admin.widgets import DeleteButtonWidget, LinkWidget

from .models import Group


class GroupsAdminTable(Table[Group]):
    fields = [
        TableField(
            "name",
            "Название",
            LinkWidget("groups.admin.update", lambda e: {"group_id": e.id}),
        ),
        TableField(
            lambda _: "",
            "Действия",
            DeleteButtonWidget(
                "groups.admin.delete",
                lambda e: {"group_id": e.id},
                "post",
            ),
        ),
    ]

    add_link_name = "groups.admin.create"

    def __init__(
        self,
        request: Request,
        session: Session,
        query: TableQuery | None = None,
    ):
        super().__init__(request, session, query)

    def get_query(self) -> Select:
        ilike = f"%{self.query.search}%"
        return select(Group).where(Group.name.ilike(ilike)).order_by(Group.id.desc())
