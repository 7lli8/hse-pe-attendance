from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Group (Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(unique=True)
