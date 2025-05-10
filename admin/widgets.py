from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Generic, TypeVar

from fastapi import Request
from markupsafe import Markup

T = TypeVar("T")
E = TypeVar("E")


class Widget(Generic[T, E], metaclass=ABCMeta):
    @abstractmethod
    def __call__(
        self, value: T | None, entity: E, request: Request, **kwargs
    ) -> Markup: ...


class StringWidget(Widget[Any, E]):
    def __call__(self, value: Any, entity: E, request: Request) -> Markup:
        return Markup(self.coerce(value))

    def coerce(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value)


class LinkWidget(Widget[str, E]):
    def __init__(
        self, link_name: str, params_getter: Callable[[E], dict]
    ) -> None:
        self.link_name = link_name
        self.params_getter = params_getter

    def __call__(
        self, value: str | None, entity: E, request: Request, **kwargs
    ) -> Markup:
        return Markup(
            f'<a href="{request.url_for(self.link_name, **self.params_getter(entity))}">{value or ""}</a>'
        )
