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


class HtmlWidget(Widget[T, E]):
    def __init__(
        self,
        tag: str,
        class_name: str = "",
        **attrs,
    ) -> None:
        self.tag = tag
        self.class_name = class_name
        self.attrs = attrs

    def __call__(
        self, value: Any | None, entity: E, request: Request, **kwargs
    ) -> Markup:
        extra_attrs = {
            key: value
            for key, value in kwargs.get("attrs", {}).items()
            if value is not None
        }
        attrs = {
            **self.attrs,
            "class": self.class_name,
            **extra_attrs,
        }

        attrs_str = " ".join(
            {f'{key}="{value}"' for key, value in attrs.items()}
        )

        return Markup(f"<{self.tag} {attrs_str}>{value}</{self.tag}>")


class ContainerWidget(HtmlWidget[T, E]):
    def __init__(
        self,
        widgets: list[Widget[T, E]],
        class_name: str = "is-flex is-align-items-center",
        style: str = "gap: 10px;",
        **attrs,
    ):
        self.widgets = widgets
        super().__init__(tag="div", class_name=class_name, style=style, **attrs)

    def __call__(self, value: T, entity: E, request: Request, **kwargs):
        markups = "\n".join(
            [
                widget(value, entity, request, **kwargs)
                for widget in self.widgets
            ]
        )
        return super().__call__(markups, entity, request, **kwargs)


class LinkWidget(HtmlWidget[T, E]):
    def __init__(
        self,
        link_name: str,
        params_getter: Callable[[E], dict],
        **attrs,
    ):
        self.link_name = link_name
        self.params_getter = params_getter
        super().__init__(**{"tag": "a", **attrs})

    def __call__(
        self, value: T | None, entity: E, request: Request, **kwargs
    ) -> Markup:
        return super().__call__(
            value or "",
            entity,
            request,
            **{
                **kwargs,
                "attrs": {
                    "href": request.url_for(
                        self.link_name, **self.params_getter(entity)
                    ),
                    **kwargs.get("attrs", {}),
                },
            },
        )


class ButtonWidget(LinkWidget[str, E]):
    def __init__(
        self,
        link_name: str,
        params_getter: Callable[[E], dict],
        label: str,
        class_name: str = "button is-small",
        **attrs,
    ):
        self.label = label
        super().__init__(
            link_name=link_name,
            params_getter=params_getter,
            class_name=class_name,
            **attrs,
        )

    def __call__(
        self, value: str | None, entity: E, request: Request, **kwargs
    ) -> Markup:
        return super().__call__(self.label, entity, request, **kwargs)


class IconButtonWidget(ButtonWidget[E]):
    def __init__(
        self,
        link_name: str,
        params_getter: Callable[[E], dict],
        icon: str | None = None,
        label: str | None = None,
        **attrs,
    ):
        markup_list = []
        if icon:
            markup_list.append(
                Markup(
                    f'<span class="icon"><i class="fa-solid {icon}"></i></span>'
                )
            )
        if label:
            markup_list.append(Markup(f"<span>{label}</span>"))

        super().__init__(
            link_name, params_getter, "\n".join(markup_list), **attrs
        )


class DeleteButtonWidget(IconButtonWidget[E]):
    def __init__(
        self,
        link_name: str,
        params_getter: Callable[[E], dict],
        method: str,
        label: str | None = None,
        **attrs,
    ):
        self.method = method
        super().__init__(
            link_name,
            params_getter,
            "fa-trash",
            label=label,
            **attrs,
            tag="button",
        )

    def __call__(
        self, value: str | None, entity: E, request: Request, **kwargs
    ) -> Markup:
        markup = super().__call__(
            value,
            entity,
            request,
            **kwargs,
            attrs={
                "href": None,
                "type": "submit",
                **kwargs.get("attrs", {}),
            },
        )
        return Markup(
            f'<form action="{request.url_for(self.link_name, **self.params_getter(entity))}" method="{self.method}">{markup}</form>'
        )
