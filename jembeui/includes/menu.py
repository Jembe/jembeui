from typing import TYPE_CHECKING, Any, Callable, List, Optional, Sequence, Union
from copy import copy
from dataclasses import dataclass
from uuid import uuid4
from markupsafe import Markup
from flask import render_template

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("Menu",)


class Menu:
    """Organize and display menu build from links and other menues

    Menu can chose to use Link render method to display individual
    menu items on can handle rendering items by it self depending
    of menu style.

    For higly customizable menues use jinja template and control
    rendering process manually skipping render capitabilities of Menus and Links
    """

    MENU_TEMPLATE: List[str] = ["/jembeui/includes/menu.html"]

    @dataclass
    class Style:
        HORIZONTAL = "horizontal"
        VERTICAL = "vertical"
        VERTICAL_NESTED = "vertical_nested"
        VERTICAL_COLLAPSIBLE = "vertical_collapsible"
        DROPDOWNS = "dropdowns"
        VARIANTS = (
            HORIZONTAL,
            VERTICAL,
            VERTICAL_NESTED,
            VERTICAL_COLLAPSIBLE,
            DROPDOWNS,
        )

        display_as: str = HORIZONTAL
        classes: Optional[str] = None
        full_classes: bool = False
        title_hidden: bool = False
        # btn_classes  are used for dropdowns 
        # to style dropdown button
        btn_classes: Optional[str] = None
        btn_full_classes: bool = False
        dropdown_classes: Optional[str] = None

        ignore_active: bool = False

        def __post_init__(self):
            if self.display_as not in self.VARIANTS:
                raise ValueError("Invalid Menu style")

    @dataclass
    class Icon:
        """
        - name: name of the icon to display
        - icon_set: name of the icon set to use from heroicons (outline, solid, mini)
        - classes: classes to add
        - full_classes: should the default classes be replaced
        - display_last: when true display icon after title
        """

        name: str
        icon_set: str = "outline"
        classes: Optional[str] = None
        full_classes: bool = False
        display_last: bool = False

    def __init__(
        self,
        items: Union[
            Sequence[Union["jembeui.Link", "jembeui.Menu"]],
            Callable[
                ["jembe.Component"], Sequence[Union["jembeui.Link", "jembeui.Menu"]]
            ],
        ],
        title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
        description: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
        style: Optional[
            Union[
                str,
                "jembeui.Menu.Style",
                Callable[["jembe.Component"], Union[str, "jembeui.Menu.Style"]],
            ]
        ] = None,
        icon: Optional[
            Union[
                str,
                "jembeui.Menu.Icon",
                Callable[["jembe.Component"], Union[str, "jembeui.Menu.Icon"]],
            ]
        ] = None,
    ):
        self._id = str(uuid4())
        self._items = items
        self._title = title
        self._description = description
        self._style = style
        self._icon = icon

        self._binded_items: Sequence[Union["jembeui.Menu", "jembeui.Link"]]
        self._component: Optional["jembe.Component"] = None

    def bind_to(self, component: "jembe.Component") -> "Menu":
        """Binds menu to component instance

        Menu must be binded before it's used in template"""
        bmenu = Menu([], title=self._title, description=self._description)
        bmenu._id = self._id
        bmenu._component = component
        bmenu._binded_items = [
            item.bind_to(component)
            for item in (
                self._items
                if isinstance(self._items, (tuple, list))
                else self.items(component)  # type:ignore
            )
        ]
        bmenu._icon = copy(self._icon)
        bmenu._style = copy(self._style)
        return bmenu

    @property
    def id(self) -> str:
        "Unique menu identifier"
        return self._id

    @property
    def is_binded(self) -> bool:
        return self._component is not None

    @property
    def is_accessible(self) -> bool:
        if not self.is_binded:
            raise ValueError("Menu must be binded to component")
        for item in self.items:  # type:ignore
            if item.is_accessible:
                return True
        return False

    def render(self) -> str:
        if not self.is_binded:
            raise ValueError("Menu is not binded to component")

        if not self.is_accessible:
            return ""

        context: dict = dict(menu=self)
        return Markup(render_template(self.MENU_TEMPLATE, **context))  # type:ignore

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.render()

    @property
    def items(self) -> Sequence[Union["jembeui.Link", "jembeui.Menu"]]:
        if not self.is_binded:
            raise ValueError("Menu must be binded to component")
        return self._binded_items

    @property
    def title(self) -> Optional[str]:
        if not self.is_binded:
            raise ValueError("Menu must be binded to component")

        if self._title is None:
            return "Unknown Menu" if self.icon is None else None
        elif isinstance(self._title, str):
            return self._title
        else:
            # callable
            title = self._title(self._component)
            if title is None and self.icon is None:
                return "Unknown Menu"
            return title

    @property
    def description(self) -> Optional[str]:
        if not self.is_binded:
            raise ValueError("Menu must be binded to component")

        return (
            self._description
            if self._description is None or isinstance(self._description, str)
            else self._description(self._component)
        )

    @property
    def style(self) -> Optional["jembeui.Menu.Style"]:
        if not self.is_binded:
            raise ValueError("Menu must be binded to component")

        style: "jembeui.Menu.Style"
        if self._style is None:
            style = self.Style()
        elif isinstance(self._style, str):
            style = self.Style(classes=self._style)
        elif isinstance(self._style, self.Style):
            style = self._style
        else:
            # callable
            res = self._style(self._component)
            style = res if isinstance(res, self.Style) else self.Style(classes=res)
        return style

    @property
    def icon(self) -> Optional["jembeui.Menu.Icon"]:
        if not self.is_binded:
            raise ValueError("Menu must be binded to component")
        if self._icon is None:
            return None
        elif isinstance(self._icon, str):
            split = self._icon.split(" ", 2)
            return self.Icon(
                name=split[0], classes=split[1] if len(split) == 2 else None
            )
        elif isinstance(self._icon, self.Icon):
            return self._icon
        else:
            # callable
            icon = self._icon(self._component)
            return icon if isinstance(icon, self.Icon) else self.Icon(name=icon)
