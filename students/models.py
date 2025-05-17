from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from attendances.models import Attendance
from database import Base
from extra_attendances.models import ExtraAttendance
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
    attendances: Mapped[list[Attendance]] = relationship(
        lazy="joined",
        primaryjoin="and_(Student.user_id == Attendance.student_id, Attendance.is_expired == False)",
        foreign_keys="[Attendance.student_id]",
    )
    extra_attendances: Mapped[list[ExtraAttendance]] = relationship(
        lazy="joined",
        primaryjoin="and_(Student.user_id == ExtraAttendance.student_id, ExtraAttendance.is_expired == False)",
        foreign_keys="[ExtraAttendance.student_id]",
    )

    @property
    def total_attendances(self) -> int:
        return len(self.attendances) + sum(
            [attendance.visits_count for attendance in self.extra_attendances]
        )

    @property
    def full_name(self) -> str:
        return " ".join(
            [
                part
                for part in [self.last_name, self.first_name, self.middle_name]
                if part
            ]
        )
