from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_users"),
        UniqueConstraint("corporate_email", name="uq_users_email")
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    corporate_email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)