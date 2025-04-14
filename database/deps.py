from typing import Generator
from sqlalchemy import orm

from .session import Session


def get_session():
    with Session() as session:
        yield session
