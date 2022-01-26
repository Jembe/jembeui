from typing import (
    Callable,
    Sequence,
    TYPE_CHECKING,
    Optional,
    Union,
    Dict,
    Any,
)

from functools import cached_property
from dataclasses import dataclass, field
from uuid import uuid4


from ..exceptions import JembeUIError


if TYPE_CHECKING:
    import jembe
    import jembeui


@dataclass
class Menu:
    items: Union[
        Sequence[Union["jembeui.Link", "jembeui.Menu"]],
        Callable[["jembe.Component"], Sequence[Union["jembeui.Link", "jembeui.Menu"]]],
    ] = field(
        default_factory=list
    )  # type:ignore
    title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None
    description: Optional[Union[str, Callable[["jembe.Component"], str]]] = None
    icon: Optional[Union[str, Callable[["jembe.Component"], str]]] = None
    icon_html: Optional[Union[str, Callable[["jembe.Component"], str]]] = None
    params: Dict[str, Any] = field(default_factory=dict)
    styling: Dict[str, Any] = field(default_factory=dict)

    id: str = field(default="", init=False)

    def __post_init__(self):
        self._items: Sequence[Union["jembeui.Link", "jembeui.Menu"]]
        self._component: Optional["jembe.Component"] = None
        self.id = str(uuid4())

    def bind_to(self, component: "jembe.Component") -> "Menu":
        """bind menu to component instance"""
        binded_menu = Menu(
            title=self.title,
            description=self.description,
            icon=self.icon,
            icon_html=self.icon_html,
            params=self.params,
        )
        binded_menu.id = self.id
        binded_menu._component = component
        binded_menu.items = [
            item.bind_to(component) for item in self.__get_items(component)
        ]
        binded_menu.title = (
            self.title
            if isinstance(self.title, str) or self.title is None
            else self.title(component)
        )
        binded_menu.description = (
            self.description
            if isinstance(self.description, str) or self.description is None
            else self.description(component)
        )
        binded_menu.icon = (
            self.icon
            if isinstance(self.icon, str) or self.icon is None
            else self.icon(component)
        )
        binded_menu.icon_html = (
            self.icon_html
            if isinstance(self.icon_html, str) or self.icon_html is None
            else self.icon_html(component)
        )
        return binded_menu

    @property
    def binded(self) -> bool:
        return self._component is not None

    @property
    def component(self) -> "jembe.Component":
        if self._component:
            return self._component
        raise JembeUIError("Menu is not binded to component")

    @cached_property
    def is_accessible(self) -> bool:
        if not self.binded:
            raise ValueError("Menu must be binded to component!")
        for item in self.items:  # type:ignore
            if item.is_accessible:
                return True
        return False

    @property
    def is_empty(self) -> bool:
        if not self.binded:
            raise ValueError("Menu must be binded to component!")
        for item in self.items:  # type:ignore
            if item.is_accessible:
                return False
        return True

    @property
    def is_menu(self) -> bool:
        return True

    def __get_items(self, component: "jembe.Component"):
        if isinstance(self.items, (tuple, list)):
            self._items = self.items
        else:
            self._items = self.items(component)  # type:ignore
        return self._items
