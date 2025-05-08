from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Group


def get_groups_choices(session: Session) -> list[str]:
    return [
        group.name
        for group in session.execute(select(Group).order_by(Group.name))
        .scalars()
        .all()
    ]


def get_group_by_name(session: Session, name: str) -> Group:
    return session.execute(select(Group).where(Group.name == name)).scalar_one()
