from datetime import datetime, timezone

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from database import Base


class Attendance(Base):
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.user_id", ondelete="CASCADE"), index=True
    )
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.user_id"))
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"))

    visit_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    @validates("visit_time")
    def validate_visit_time(self, key, value: datetime | None):
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value
        raise ValueError("datetime object is required")
