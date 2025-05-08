from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from groups.models import Group


class Student(Base):
    __tablename__ = "students"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
        unique=True,
    )

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None] = mapped_column(default=None)
    course: Mapped[int]

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[Group] = relationship(lazy="joined")
