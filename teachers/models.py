from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    corporate_email: Mapped[str] = mapped_column(unique=True)

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None] = mapped_column(default=None)
    position: Mapped[str]
