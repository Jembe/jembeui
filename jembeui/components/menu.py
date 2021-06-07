from typing import List, Sequence, TYPE_CHECKING, Optional, Tuple
from abc import ABC, abstractmethod
from copy import copy

from jembe.component import component
from .component import Component

__all__ = ("Link", "URLLink", "ActionLink", "Menu", "CMenu")


class Link(ABC):
    def __init__(
        self,
        active_for_pathnames: Sequence[str] = (),
        active_for_exec_names: Sequence[str] = (),
    ):
        self.callable_params: dict = dict()
        self.binded_to: Optional["Component"] = None

        self.extra_pathnames: Tuple[str, ...] = tuple(active_for_pathnames)
        self.extra_exec_names: Tuple[str, ...] = tuple(active_for_exec_names)

    @property
    @abstractmethod
    def is_internal(self) -> bool:
        """True if link is to Jembe Component and/or Action"""
        raise NotImplementedError()

    def bind_to(self, component: "Component") -> "Link":
        blink = copy(self)
        blink.binded_to = component
        return blink

    @property
    def binded(self) -> bool:
        return self.binded_to is not None

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
        link.callable_params = dict()
        for k, v in kwargs.items():
            link.callable_params[k] = v
        return link
