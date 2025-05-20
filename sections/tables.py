from fastapi import Request
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from admin.table import Table, TableField, TableQuery
from admin.widgets import DeleteButtonWidget, LinkWidget

from .models import Section


class SectionsAdminTable(Table[Section]):
    fields = [
        TableField(
            "name",
            "Название",
            LinkWidget("sections.admin.update", lambda e: {"section_id": e.id}),
        ),
        TableField(
            lambda _: "",
            "Действия",
            DeleteButtonWidget(
                "sections.admin.delete",
                lambda e: {"section_id": e.id},
                "post",
            ),
        ),
    ]

    add_link_name = "sections.admin.create"

    def __init__(
        self,
        request: Request,
        session: Session,
        query: TableQuery | None = None,
    ):
        super().__init__(request, session, query)

    def get_query(self) -> Select:
        ilike = f"%{self.query.search}%"
        return (
            select(Section).where(Section.name.ilike(ilike)).order_by(Section.id.desc())
        )
