from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
import jembe as jmb
from flask import current_app


__all__ = ("Component",)


class Component(jmb.Component):
    """
    Base component for all Jembe UI components.
    """

    class Config(jmb.Component.Config):
        default_template_exp = "jembeui/{style}/components/component.html"
        default_template: str

        default_title = "Jembe Component"

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
            self.title = title if title else self.default_title
            # calculate default template and add it to template
            self.default_template = (
                self.default_template
                if hasattr(self, "default_template")
                else self.default_template_exp.format(
                    style=current_app.config.get("JEMBEUI_STYLE", "s0")
                )
            )
            if template is None:
                template = ("", self.default_template)

            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    @property
    def title(self) -> str:
        if isinstance(self._config.title, str):
            return self._config.title
        return self._config.title(self)

    # JembeUI helper methods
    def jui_set_page_title(self, title: Optional[str]):
        self.emit("setPageTitle", title=title)

    def jui_push_notification(self, message: str, level: str = "info"):
        self.emit("pushPageNotification", message=message, level=level)
