from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .widgets import StringWidget, Widget

T = TypeVar("T")


@dataclass
class TableField(Generic[T]):
    field: str | Callable[[T], str]
    header: str = ""
    widget: Widget = StringWidget()
