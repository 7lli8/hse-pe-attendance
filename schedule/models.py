from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, CheckConstraint, PrimaryKeyConstraint
from database import Base
from enums import WeekDay

class Schedule(Base):
    __tablename__ = "schedule"
    __table_args__ = (
        CheckConstraint(
            "time_end_in_minutes_since_midnight > time_start_in_minutes_since_midnight",
            name="check_time_end_after_start"
        ), 
        CheckConstraint(
           "time_start_in_minutes_since_midnight BETWEEN 0 AND 1439",
            name="check_valid_start_time" 
        ),
        CheckConstraint(
            "time_end_in_minutes_since_midnight BETWEEN 0 AND 1439",
            name="check_valid_end_time"
        ),
        # PrimaryKeyConstraint("id", name="pk_schedule"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE", onupdate="CASCADE"))

    time_start_in_minutes_since_midnight: Mapped[int] = mapped_column()
    time_end_in_minutes_since_midnight: Mapped[int] = mapped_column()
    
    weekday: Mapped[WeekDay] = mapped_column(
        Enum(WeekDay, create_constraint=True),
        nullable=False
    )

