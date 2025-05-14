from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from students.models import Student
from teachers.models import Teacher


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    corporate_email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    is_admin: Mapped[bool] = mapped_column(default=False, server_default="false")

    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    student: Mapped[Student | None] = relationship(lazy="joined")
    teacher: Mapped[Teacher | None] = relationship(lazy="joined")

    @property
    def has_student_email(self) -> bool:
        return get_email_domain(self.corporate_email) == "edu.hse.ru"

    @property
    def has_teacher_email(self) -> bool:
        return get_email_domain(self.corporate_email) == "hse.ru"


def get_email_domain(email: str) -> str:
    return ".".join(email.split("@")[-1].strip().split("."))
