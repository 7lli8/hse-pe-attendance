from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
        unique=True,
    )

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None] = mapped_column(default=None)
    position: Mapped[str]
