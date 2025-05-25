from fastapi import Request
from sqlalchemy.orm import Session
from .models import Group
from .forms import GroupForm


async def get_group_form(
    request: Request, session: Session, group: Group | None = None
) -> GroupForm:
    return await GroupForm.create(request, session, group)


def save_group_form(
    session: Session, form: GroupForm, group: Group | None = None
) -> Group:
    if not group:
        group = Group()
    form.populate_obj(group)
    session.add(group)
    session.commit()
    return group


def delete_group(session: Session, group_id: int) -> None:
    group = session.get(Group, group_id)
    if group:
        session.delete(group)
        session.commit()
