from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    Optional,
    Tuple,
    Union,
    Sequence,
)
from ..component import Component
from .title import CPageTitle
from .notifications import CPageNotifications
from .syserror import CPageSystemError
from .confirmation import CActionConfirmationDialog
from .update_indicatior import CPageUpdateIndicator
from ..menu import CMenu

if TYPE_CHECKING:
    import jembe
    from ..menu import Menu, Link

__all__ = ("CPageBase", "CPage")


class CPageBase(Component):
    """Page Base classes for displaying empty page without navigation and layout"""

    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/page_base.html"
        default_title = "JembeUI Page"

        def __init__(
            self,
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
            components = components if components is not None else dict()
            if "_title" not in components:
                components["_title"] = (
                    CPageTitle,
                    CPageTitle.Config(title=title if title else self.default_title),
                )
            if "_notifications" not in components:
                components["_notifications"] = CPageNotifications
            if "_syserror" not in components:
                components["_syserror"] = CPageSystemError
            if "_action_confirmation" not in components:
                components["_action_confirmation"] = CActionConfirmationDialog
            if "_update_indicator" not in components:
                components["_update_indicator"] = CPageUpdateIndicator

            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )


class CPage(CPageBase):
    """Page with navigation and layoute"""

    class Config(CPageBase.Config):
        default_template_exp = "jembeui/{style}/components/page/page.html"

        def __init__(
            self,
            main_menu: Optional[Union["Menu", Sequence[Union["Link", "Menu"]]]] = None,
            system_menu: Optional[
                Union["Menu", Sequence[Union["Link", "Menu"]]]
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
            components = components if components is not None else dict()
            if "_main_menu" not in components:
                components["_main_menu"] = (
                    CMenu,
                    CMenu.Config(
                        menu=main_menu, template=CMenu.Config.template_variant("page_main")
                    ),
                )
            if "_system_menu" not in components:
                components["_system_menu"] = (
                    CMenu,
                    CMenu.Config(
                        menu=system_menu,
                        template=CMenu.Config.template_variant("page_system"),
                    ),
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
