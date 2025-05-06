from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    corporate_email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
