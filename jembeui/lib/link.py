from typing import (
    Callable,
    Sequence,
    TYPE_CHECKING,
    Optional,
    Tuple,
    Union,
    Dict,
    Any,
)
from markupsafe import Markup
from abc import ABC, abstractmethod
from functools import cached_property
from copy import copy
from urllib.parse import urlparse
from jembe import ComponentReference
from flask import render_template

from ..exceptions import JembeUIError
from ..settings import settings
from ..helpers import get_widget_variants

if TYPE_CHECKING:
    import jembe

__all__ = ("Link", "URLLink", "ActionLink",)


class Link(ABC):
    TEMPLATE_VARIANTS: Dict[str, str]

    def __init__(
        self,
        active_for_pathnames: Optional[Sequence[str]] = None,
        active_for_exec_names: Optional[Sequence[str]] = None,
        styling: Optional[Dict[str, Any]] = None,
    ):
        self.params: dict = dict()
        self._binded_to: Optional["jembe.Component"] = None

        self._active_for_pathnames: Optional[Tuple[str, ...]] = (
            tuple(active_for_pathnames) if active_for_pathnames is not None else None
        )
        self._active_for_exec_names: Optional[Tuple[str, ...]] = (
            tuple(active_for_exec_names) if active_for_exec_names is not None else None
        )
        self.styling = styling if styling else dict()

    @property
    @abstractmethod
    def is_internal(self) -> bool:
        """True if link is to Jembe Component and/or Action"""
        raise NotImplementedError()

    def bind_to(self, component: "jembe.Component") -> "Link":
        blink = copy(self)
        blink._binded_to = component
        return blink

    @property
    def binded(self) -> bool:
        return self._binded_to is not None

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

    @property
    def template_variants(self) -> Dict[str, str]:
        try:
            return self.__class__.TEMPLATE_VARIANTS
        except AttributeError:
            self.__class__.TEMPLATE_VARIANTS = get_widget_variants(
                settings.link_widgets_variants_dirs
            )
        return self.__class__.TEMPLATE_VARIANTS

    def as_html(self, variant: str = "href", html_attrs: Optional[dict] = None) -> str:
        if "/" in variant:
            # variant is template name
            template = variant
        else:
            if variant not in self.template_variants.keys():
                raise JembeUIError(
                    "Link variant '{}' does not exist! Valid variants are :{}".format(
                        variant, self.template_variants.keys()
                    )
                )
            template = self.template_variants[variant]

        html_attrs = dict() if html_attrs is None else html_attrs
        context = {"link": self, "attrs": html_attrs}
        return Markup(render_template(template, **context))

    def as_href(self, html_attrs: Optional[dict] = None) -> str:
        """Renders link as simple regular <a href></a> link"""
        if not self.is_accessible:
            return ""
        return self.as_html(html_attrs=html_attrs)

    def as_button(
        self, html_attrs: Optional[dict] = None, show_disabled: bool = False
    ) -> str:
        """Renders link as simple regular <button></button>"""
        if not self.is_accessible and not show_disabled:
            return ""
        html_attrs = dict() if html_attrs is None else html_attrs
        if show_disabled:
            html_attrs["disabled"] = True
        return self.as_html("button", html_attrs=html_attrs)


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
        styling: Optional[Dict[str, Any]] = None,
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
            styling=styling,
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
        to: Union[
            str,
            "jembe.ComponentReference",
            Callable[["jembe.Component"], "jembe.ComponentReference"],
        ],
        title: Optional[Union[str, Callable[["Link"], str]]] = None,
        description: Optional[Union[str, Callable[["Link"], str]]] = None,
        icon: Optional[Union[str, Callable[["Link"], str]]] = None,
        icon_html: Optional[Union[str, Callable[["Link"], str]]] = None,
        styling: Optional[Dict[str, Any]] = None,
        active_for_pathnames: Optional[Sequence[str]] = None,
        active_for_exec_names: Optional[Sequence[str]] = None,
        params: Optional[dict] = None,
    ):
        self._to = to
        self._title = title
        self._description = description
        self._icon = icon
        self._icon_html = icon_html
        super().__init__(
            active_for_pathnames=active_for_pathnames,
            active_for_exec_names=active_for_exec_names,
            styling=styling,
        )
        self.params = params if params else dict()

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
        if isinstance(self._to, str):
            return self._str_to_component_reference_lambda(self._to)(self._binded_to)
        elif isinstance(self._to, ComponentReference):
            return self._to
        else:
            return self._to(self._binded_to)

    def _str_to_component_reference_lambda(
        self, to_str: str
    ) -> Callable[["jembe.Component"], "jembe.ComponentReference"]:
        if to_str.endswith("()"):
            if "/" in to_str:
                raise ValueError(
                    "Action call shortcut cann't be used on subcomponents."
                )
            return lambda component: component.component().call(
                to_str[:-2], **self.params
            )
        else:
            return lambda component: component.component(to_str, **self.params)