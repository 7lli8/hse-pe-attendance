from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from schedule.models import Schedule


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

    is_verified: Mapped[bool] = mapped_column(server_default="false")

    schedule: Mapped[list[Schedule]] = relationship(lazy="selectin")

    @property
    def full_name(self) -> str:
        return " ".join(
            filter(bool, [self.last_name, self.first_name, self.middle_name])
        )
