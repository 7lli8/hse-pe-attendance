from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from math import ceil
from typing import Any, Callable, Generic, TypeVar

from fastapi import Request
from pydantic import BaseModel, NonNegativeInt
from sqlalchemy import Select, func
from sqlalchemy.orm import Session

from admin.fields import TableField

T = TypeVar("T")


@dataclass
class EntityPage(Generic[T]):
    entities: list[T]
    total: int


class TableQuery(BaseModel):
    page: NonNegativeInt = 0
    page_size: NonNegativeInt = 20
    search: str = ""


class Table(Generic[T], metaclass=ABCMeta):
    action: str | None = None
    fields: list[TableField] = []
    fields_mappers: dict[str, Callable[[Any], str]] = {}

    query: TableQuery

    def __init__(
        self,
        request: Request,
        session: Session,
        query: TableQuery | None = None,
    ):
        if not query:
            query = TableQuery()
        self.query = query
        self._session = session
        self._request = request
        self._cached_entities = None

    @property
    def total_pages(self) -> int:
        return ceil(self.page.total / self.query.page_size)

    def get_page_link(self, page: int) -> str:
        return str(self._request.url.include_query_params(page=page))

    def get_page_size_link(self, page_size: int) -> str:
        return str(self._request.url.include_query_params(page_size=page_size))

    @property
    def page(self) -> EntityPage[T]:
        if not self._cached_entities:
            self._cached_entities = self._get_entities()
        return self._cached_entities

    def _get_entities(self) -> EntityPage[T]:
        query = self.get_query()

        total = int(
            self._session.execute(
                query.with_only_columns(func.count()).order_by(None)
            ).scalar_one()
        )
        entities = list(
            self._session.execute(
                query.offset(self.query.page * self.query.page_size).limit(
                    self.query.page_size
                )
            )
            .scalars()
            .all()
        )
        return EntityPage(entities=entities, total=total)

    @abstractmethod
    def get_query(self) -> Select: ...

    def get_field_value(self, entity: T, field: str) -> str:
        value = self._get_field_by_path(entity, field)
        if field in self.fields_mappers:
            return self.fields_mappers[field](value)
        if value is None:
            return ""
        return str(value)

    def _get_field_by_path(self, entity: T, field: str) -> Any:
        """
        Получение значений атрибутов, записанных в виде `parent.nested.attr`
        """
        path = field.split(".")
        last_value = entity
        for part in path:
            try:
                last_value = getattr(last_value, part)
            except AttributeError:
                return
        return last_value
