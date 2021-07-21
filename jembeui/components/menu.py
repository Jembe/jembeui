from typing import (
    Callable,
    Iterable,
    Sequence,
    TYPE_CHECKING,
    Optional,
    Tuple,
    Union,
    Dict,
    Any,
)
from abc import ABC, abstractmethod
from functools import cached_property, partial
from copy import copy
from urllib.parse import urlparse
from dataclasses import dataclass, field
from uuid import uuid4

from .component import Component
from jembe.component import component

if TYPE_CHECKING:
    import jembe

__all__ = ("Link", "URLLink", "ActionLink", "Menu", "CMenu")


class Link(ABC):
    def __init__(
        self,
        active_for_pathnames: Optional[Sequence[str]] = None,
        active_for_exec_names: Optional[Sequence[str]] = None,
    ):
        self.params: dict = dict()
        self.binded_to: Optional["jembe.Component"] = None

        self._active_for_pathnames: Optional[Tuple[str, ...]] = (
            tuple(active_for_pathnames) if active_for_pathnames is not None else None
        )
        self._active_for_exec_names: Optional[Tuple[str, ...]] = (
            tuple(active_for_exec_names) if active_for_exec_names is not None else None
        )

    @property
    @abstractmethod
    def is_internal(self) -> bool:
        """True if link is to Jembe Component and/or Action"""
        raise NotImplementedError()

    def bind_to(self, component: "jembe.Component") -> "Link":
        blink = copy(self)
        blink.binded_to = component
        return blink

    @property
    def binded(self) -> bool:
        return self.binded_to is not None

    def _chek_binded(self):
        if not self.binded:
            raise ValueError("Link must be binded to component!")

    @property
    @abstractmethod
    def url(self) -> Optional[str]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def jrl(self) -> Optional[str]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def active_for_pathnames(self) -> Sequence[str]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def active_for_exec_names(self) -> Sequence[str]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_accessible(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def icon(self) -> Optional[str]:
        """Name of the icon if it is supported by JUI Style"""
        raise NotImplementedError()

    @property
    @abstractmethod
    def icon_html(self) -> Optional[str]:
        """
        Raw HTML/SVG of custom icon for using icons not directly supported by JUI Style

        Used only if icon is None
        """
        raise NotImplementedError()

    def set(self, **kwargs) -> "Link":
        """Add additional paramas for callables and resets previous ones"""
        # setting additional params can change link output
        link = copy(self)
        link.params = dict()
        for k, v in kwargs.items():
            link.params[k] = v
        return link

    @property
    def is_menu(self) -> bool:
        return False


class URLLink(Link):
    def __init__(
        self,
        url: Union[str, Callable[["Link"], str]],
        title: Union[str, Callable[["Link"], str]],
        description: Optional[Union[str, Callable[["Link"], str]]] = None,
        is_accessible: Union[bool, Callable[["Link"], bool]] = True,
        icon: Optional[Union[str, Callable[["Link"], str]]] = None,
        icon_html: Optional[Union[str, Callable[["Link"], str]]] = None,
        active_for_pathnames: Optional[Sequence[str]] = None,
        active_for_exec_names: Optional[Sequence[str]] = None,
    ):
        self._url = url
        self._title = title
        self._description = description
        self._is_accessible = is_accessible
        self._icon = icon
        self._icon_html = icon_html
        super().__init__(
            active_for_pathnames=active_for_pathnames,
            active_for_exec_names=active_for_exec_names,
        )

    @property
    def is_internal(self) -> bool:
        return False

    @property
    def url(self) -> Optional[str]:
        self._chek_binded()
        if self._url is None:
            return None
        elif isinstance(self._url, str):
            return self._url
        else:
            return self._url(self)

    @property
    def jrl(self) -> Optional[str]:
        return None

    @property
    def active_for_pathnames(self) -> Sequence[str]:
        if self._active_for_pathnames is None:
            pathname = str(urlparse(self.url).path)
            return (pathname,)
        else:
            return self._active_for_pathnames

    @property
    def active_for_exec_names(self) -> Sequence[str]:
        if self._active_for_exec_names is None:
            return ()
        return self._active_for_exec_names

    @property
    def is_accessible(self) -> bool:
        self._chek_binded()
        if isinstance(self._is_accessible, bool):
            return self._is_accessible
        return self._is_accessible(self)

    @property
    def title(self) -> str:
        self._chek_binded()
        if isinstance(self._title, str):
            return self._title
        return self._title(self)

    @property
    def description(self) -> Optional[str]:
        self._chek_binded()
        if self._description is None:
            return None
        elif isinstance(self._description, str):
            return self._description
        return self._description(self)

    @property
    def icon(self) -> Optional[str]:
        """Name of the icon if it is supported by JUI Style"""
        self._chek_binded()
        if self._icon is None:
            return None
        elif isinstance(self._icon, str):
            return self._icon
        return self._icon(self)

    @property
    def icon_html(self) -> Optional[str]:
        """
        Raw HTML/SVG of custom icon for using icons not directly supported by JUI Style

        Used only if icon is None
        """
        self._chek_binded()
        if self._icon_html is None:
            return None
        elif isinstance(self._icon_html, str):
            return self._icon_html
        return self._icon_html(self)


class ActionLink(Link):
    def __init__(
        self,
        to: Union[str, Callable[["jembe.Component"], "jembe.ComponentReference"]],
        title: Optional[Union[str, Callable[["Link"], str]]] = None,
        description: Optional[Union[str, Callable[["Link"], str]]] = None,
        icon: Optional[Union[str, Callable[["Link"], str]]] = None,
        icon_html: Optional[Union[str, Callable[["Link"], str]]] = None,
        active_for_pathnames: Optional[Sequence[str]] = None,
        active_for_exec_names: Optional[Sequence[str]] = None,
        action_params: Optional[dict] = None,
    ):
        self._to = to
        self._title = title
        self._description = description
        self._icon = icon
        self._icon_html = icon_html
        super().__init__(
            active_for_pathnames=active_for_pathnames,
            active_for_exec_names=active_for_exec_names,
        )
        self.action_params = action_params if action_params else dict()

    @property
    def to_full_name(self) -> str:
        if (
            isinstance(self._to, str)
            and not self._to.endswith("()")
            and self._to.startswith("/")
        ):
            return self._to
        raise ValueError(
            "Action Link must be binded in order to get destination full_name"
        )

    @property
    def is_internal(self) -> bool:
        return True

    @property
    def url(self) -> Optional[str]:
        return self._component_reference.url

    @property
    def jrl(self) -> Optional[str]:
        return self._component_reference.jrl

    @property
    def active_for_pathnames(self) -> Sequence[str]:
        if self._active_for_pathnames is None:
            return ()
        return self._active_for_pathnames

    @property
    def active_for_exec_names(self) -> Sequence[str]:
        if self._active_for_exec_names is None:
            return (self._component_reference.exec_name,)
        else:
            return self._active_for_exec_names

    @property
    def is_accessible(self) -> bool:
        return self._component_reference.is_accessible

    @property
    def title(self) -> str:
        if isinstance(self._title, str):
            return self._title
        self._chek_binded()
        if self._title is None:
            return self._component_reference.component_instance.title
        return self._title(self)

    @property
    def description(self) -> Optional[str]:
        if self._description is None:
            return None
        elif isinstance(self._description, str):
            return self._description
        self._chek_binded()
        return self._description(self)

    @property
    def icon(self) -> Optional[str]:
        """Name of the icon if it is supported by JUI Style"""
        if self._icon is None:
            return None
        elif isinstance(self._icon, str):
            return self._icon
        self._chek_binded()
        return self._icon(self)

    @property
    def icon_html(self) -> Optional[str]:
        """
        Raw HTML/SVG of custom icon for using icons not directly supported by JUI Style

        Used only if icon is None
        """
        if self._icon_html is None:
            return None
        elif isinstance(self._icon_html, str):
            return self._icon_html
        self._chek_binded()
        return self._icon_html(self)

    @cached_property
    def _component_reference(self) -> "jembe.ComponentReference":
        self._chek_binded()
        to_component: Callable[["jembe.Component"], "jembe.ComponentReference"] = (
            self._str_to_component_reference_lambda(self._to)
            if isinstance(self._to, str)
            else self._to
        )
        return to_component(self.binded_to)  # type: ignore

    def _str_to_component_reference_lambda(
        self, to_str: str
    ) -> Callable[["jembe.Component"], "jembe.ComponentReference"]:
        if to_str.endswith("()"):
            if "/" in to_str:
                raise ValueError(
                    "Action call shortcut cann't be used on subcomponents."
                )
            return lambda component: component.component().call(
                to_str[:-2], **self.action_params
            )
        else:
            return lambda component: component.component(to_str, **self.action_params)


@dataclass
class Menu:
    items: Sequence[Union["Link", "Menu"]] = field(default_factory=list)
    title: Optional[Union[str, Callable[["Menu"], str]]] = None
    description: Optional[Union[str, Callable[["Menu"], str]]] = None
    icon: Optional[Union[str, Callable[["Menu"], str]]] = None
    icon_html: Optional[Union[str, Callable[["Menu"], str]]] = None
    params: Dict[str, Any] = field(default_factory=dict)

    id: str = field(default="", init=False)
    binded: bool = field(default=False, init=False)

    def __post_init__(self):
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
        binded_menu.items = [item.bind_to(component) for item in self.items]
        binded_menu.binded = True
        return binded_menu

    @cached_property
    def is_accessible(self) -> bool:
        if not self.binded:
            raise ValueError("Menu must be binded to component!")
        for item in self.items:
            if item.is_accessible:
                return True
        return False

    @property
    def is_menu(self) -> bool:
        return True


class CMenu(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/menu.html"
        TEMPLATE_VARIANTS = ("page_main", "page_system")

        def __init__(
            self,
            menu: Optional[Union["Menu", Sequence[Union["Link", "Menu"]]]] = None,
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = False,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            self.menu: "Menu" = (
                Menu()
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    def display(self) -> "jembe.DisplayResponse":
        self.menu = self._config.menu.bind_to(self)
        return super().display()
