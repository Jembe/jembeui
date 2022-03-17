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
from .notice import CPageNotice
from .syserror import CPageSystemError
from .confirmation import CActionConfirmationDialog
from .update_indicatior import CPageUpdateIndicator
from .breadcrumb import Breadcrumb, CBreadcrumb
from ..menu import CMenu

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CPage",)


class CPage(Component):
    """Page with navigation and layoute"""

    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/page.html"

        def __init__(
            self,
            main_menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            system_menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            breadcrumbs: Optional[
                Union["jembeui.Breadcrumb", Sequence["jembeui.Breadcrumb"]]
            ] = None,
            enable_image_edit_support: bool = False,
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
            if "__title" not in components:
                components["__title"] = (
                    CPageTitle,
                    CPageTitle.Config(title=title if title else self.default_title),
                )
            if "__notifications" not in components:
                components["__notifications"] = CPageNotifications
            if "__notice" not in components:
                components["__notice"] = CPageNotice
            if "__syserror" not in components:
                components["__syserror"] = CPageSystemError
            if "__action_confirmation" not in components:
                components["__action_confirmation"] = CActionConfirmationDialog
            if "__update_indicator" not in components:
                components["__update_indicator"] = CPageUpdateIndicator
            if "__main_menu" not in components and main_menu is not None:
                components["__main_menu"] = (
                    CMenu,
                    CMenu.Config(
                        menu=main_menu,
                        template=CMenu.Config.template_variant("page_main"),
                    ),
                )
            if "__system_menu" not in components and system_menu is not None:
                components["__system_menu"] = (
                    CMenu,
                    CMenu.Config(
                        menu=system_menu,
                        template=CMenu.Config.template_variant("page_system"),
                    ),
                )
            if "__breadcrumb" not in components and breadcrumbs is not None:
                if isinstance(breadcrumbs, Breadcrumb):
                    breadcrumbs = [breadcrumbs]

                components["__breadcrumb"] = (
                    CBreadcrumb,
                    CBreadcrumb.Config(breadcrumbs=breadcrumbs),
                )

            # flags for css and js imports
            self.enable_image_edit_support = enable_image_edit_support
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

    def redisplay_navigation(self):
        self.emit("redisplay").to(("__main_menu", "__system_menu", "__braedcrumb"))
