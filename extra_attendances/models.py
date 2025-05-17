from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ExtraAttendance(Base):
    __tablename__ = "extra_attendances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.user_id", ondelete="CASCADE"), nullable=False
    )

    description: Mapped[str] = mapped_column(nullable=False)
    event_date: Mapped[date] = mapped_column(default=date.today)

    visits_count: Mapped[int] = mapped_column(nullable=False)

    is_expired: Mapped[bool] = mapped_column(server_default="false")
