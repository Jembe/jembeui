from typing import (
    Callable,
    ClassVar,
    Sequence,
    TYPE_CHECKING,
    Optional,
    Union,
    Dict,
    Any,
    ClassVar,
)
from markupsafe import Markup
from functools import cached_property
from dataclasses import dataclass, field
from uuid import uuid4
from flask import render_template

from ..exceptions import JembeUIError
from ..settings import settings
from ..helpers import get_widget_variants

if TYPE_CHECKING:
    import jembe
    import jembeui


@dataclass
class Menu:
    items: Sequence[Union["jembeui.Link", "jembeui.Menu"]] = field(default_factory=list)
    title: Optional[Union[str, Callable[["jembeui.Menu"], str]]] = None
    description: Optional[Union[str, Callable[["jembeui.Menu"], str]]] = None
    icon: Optional[Union[str, Callable[["jembeui.Menu"], str]]] = None
    icon_html: Optional[Union[str, Callable[["jembeui.Menu"], str]]] = None
    params: Dict[str, Any] = field(default_factory=dict)
    styling: Dict[str, Any] = field(default_factory=dict)

    id: str = field(default="", init=False)
    binded: bool = field(default=False, init=False)

    # template supoprted template variant calculated based on settings.menu_widgets_variants_dirs
    TEMPLATE_VARIANTS: ClassVar[dict]

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

    @property
    def template_variants(self) -> Dict[str, str]:
        try:
            return self.__class__.TEMPLATE_VARIANTS
        except AttributeError:
            self.__class__.TEMPLATE_VARIANTS = get_widget_variants(
                settings.menu_widgets_variants_dirs
            )
        return self.__class__.TEMPLATE_VARIANTS

    def as_html(self, variant: str = "default") -> str:
        if not self.binded:
            raise JembeUIError(
                "Menu must be binded to component in order to be rendered to html"
            )
        if "/" in variant or "." in variant:
            # variant is template name
            template = variant
        else:
            if variant not in self.template_variants.keys():
                raise JembeUIError(
                    "Menu variant '{}' does not exist! Valid variants are :{}".format(
                        variant, self.template_variants.keys()
                    )
                )
            template = self.template_variants[variant]
        context = {"menu": self}
        return Markup(render_template(template, **context))
