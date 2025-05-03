from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from datetime import date
from database import Base


class ExtraAttendance(Base):
    __tablename__ = "extra_attendances"
    # __table_args__ = (
    #     PrimaryKeyConstraint("id"),
    # )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.user_id", 
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    
    description: Mapped[str] = mapped_column(nullable=False)
    event_date: Mapped[date] = mapped_column(default=date.today)

    visits_count: Mapped[int] = mapped_column(nullable=False)
