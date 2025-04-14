from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base
from groups.models import Group


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    corporate_email: Mapped[str] = mapped_column(unique=True)

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None] = mapped_column(default=None)
    course: Mapped[int]

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[Group] = relationship()
