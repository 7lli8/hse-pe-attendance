from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import Table, Column, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from teachers.models import Teacher

teacher_section = Table(
    "teacher_section", 
    Base.metadata,
    Column("teacher_id", ForeignKey("teachers.user_id"), primary_key=True), 
    Column("section_id", ForeignKey("sections.id"), primary_key=True)
)

class Section(Base):
    __tablename__ = "sections"
    # __table_args__ = (
    #     PrimaryKeyConstraint("id", name="pk_sections"),
    #     UniqueConstraint("name", name="uq_sections_name"),
    # )


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    teachers: Mapped[list[Teacher]] = relationship(secondary=teacher_section)
