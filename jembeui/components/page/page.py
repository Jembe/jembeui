from typing import Callable, Dict, Iterable, Optional, TYPE_CHECKING, Tuple, Union
from ..component import Component
from .title import CPageTitle
from .notifications import CPageNotifications
from .syserror import CPageSystemError

if TYPE_CHECKING:
    import jembe as jmb

__all__ = ("CPageBase", "CPage")


class CPageBase(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/page_base.html"
        default_title = "JembeUI Page"

        def __init__(
            self,
            title: Optional[Union[str, Callable[["jmb.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jmb.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jmb.Component", "jmb.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jmb.RedisplayFlag", ...] = (),
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
    pass
