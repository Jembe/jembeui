from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
from jembe.component_config import listener
from ..settings import settings
from ..helpers import get_component_template_variants
import jembe

if TYPE_CHECKING:
    from jembe import Event, DisplayResponse


__all__ = ("Component",)


class Component(jembe.Component):
    """
    Base component for all Jembe UI components.
    """

    class Config(jembe.Component.Config):
        default_template: str
        default_template_exp = "jembeui/{style}/components/component.html"
        TEMPLATE_VARIANTS: Dict[str, str]

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
            self.title = title if title else self.default_title
            # calculate default template and add it to template
            self.default_template = (
                self.default_template
                if hasattr(self, "default_template")
                else self.default_template_exp.format(style=settings.default_style)
            )
            self.__class__.TEMPLATE_VARIANTS = get_component_template_variants(
                self.default_template
            )
            if template is None:
                template = ("", self.default_template)
            elif isinstance(template, str):
                original_template = template
                # if template is one of the variants threat it as default template
                if template in self.TEMPLATE_VARIANTS:
                    template = (
                        "",
                        self.TEMPLATE_VARIANTS[template],
                        self.default_template,
                    )
                    self.default_template = self.TEMPLATE_VARIANTS[original_template]
                elif template in self.TEMPLATE_VARIANTS.values():
                    template = ("", template, self.default_template)
                    self.default_template = original_template

            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        def default_title(self, component: "jembe.Component") -> str:
            return self.name.replace("_", " ").title()

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

    def jui_confirm_action(
        self,
        action_name: str,
        title: str,
        question: str = "",
        action_params: Optional[dict] = None,
    ):
        from .page.confirmation import Confirmation

        if action_params is None:
            action_params = dict(confirmed=True)

        self.emit(
            "requestActionConfirmation",
            confirmation=Confirmation(
                title=title,
                question=question,
                action_name=action_name,
                action_params=action_params,
            ),
        )

    @listener(event="actionConfirmed")
    def jui_on_action_confirmed(self, event: "Event"):
        if hasattr(self, event.action_name):
            return getattr(self, event.action_name)(**event.action_params)

    def hydrate(self):
        pass

    def display(self) -> "DisplayResponse":
        self.hydrate()
        return super().display()
