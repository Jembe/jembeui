from typing import (
    Callable,
    Iterable,
    Sequence,
    TYPE_CHECKING,
    Optional,
    Tuple,
    Union,
    Dict,
)

from .component import Component
from ..lib import Menu, Link

if TYPE_CHECKING:
    import jembe

__all__ = ("CMenu",)


class CMenu(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/menu.html"

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
