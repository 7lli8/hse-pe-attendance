from dataclasses import dataclass

from .widgets import StringWidget, Widget


@dataclass
class TableField:
    field: str
    header: str = ""
    widget: Widget = StringWidget()
