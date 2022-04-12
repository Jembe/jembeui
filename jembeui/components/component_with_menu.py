from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    Callable,
    Iterable,
    Tuple,
    Dict,
    Sequence,
)
from ..lib import Menu
from .component import Component


if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("ComponentWithMenu",)


class ComponentWithMenu(Component):
    class Config(Component.Config):
        def __init__(
            self,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            self.menu: "jembeui.Menu" = (
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

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()
