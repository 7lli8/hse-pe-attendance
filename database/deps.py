from typing import Annotated

from fastapi import Depends
from sqlalchemy import orm

from .session import Session


def get_session():
    with Session() as session:
        yield session


GetSession = Annotated[orm.Session, Depends(get_session)]
