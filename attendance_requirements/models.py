from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from enums import AttestationType


class AttendanceRequirement(Base):
    __tablename__ = "attendance_requirements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    attestation_type: Mapped[AttestationType] = mapped_column(
        Enum(
            AttestationType,
            name="attestation_type_enum",
            create_constraint=True,
        ),
        nullable=False,
    )

    required_visits: Mapped[int] = mapped_column()
