from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
import jembe as jmb
import os.path
from flask import current_app
from jembe.component_config import listener

if TYPE_CHECKING:
    from jembe import Event


__all__ = ("Component",)


class Component(jmb.Component):
    """
    Base component for all Jembe UI components.
    """

    class Config(jmb.Component.Config):
        default_template: str
        default_template_exp = "jembeui/{style}/components/component.html"
        TEMPLATE_VARIANTS: Tuple[str, ...] = ()

        @classmethod
        def template_variant(cls, variant):
            if variant not in cls.TEMPLATE_VARIANTS:
                raise ValueError(
                    "Invalid template variant '{}'. Valid variatns are: {}".format(
                        variant, cls.TEMPLATE_VARIANTS
                    )
                )
            dte_split = cls.default_template_exp.split(".")
            dte_split[-2] = dte_split[-2] + "__" + "{variant}"
            variant_template_exp = ".".join(dte_split)
            return variant_template_exp.format(
                style=current_app.config.get("JEMBEUI_STYLE", "s0"), variant=variant
            )

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
            elif isinstance(template, str):
                # if template is one of the variants threat it as default template
                for variant in self.TEMPLATE_VARIANTS:
                    if self.template_variant(variant) == template:
                        tvar = template
                        template = ("", template, self.default_template)
                        self.default_template = tvar
                        break
                    if template == variant:
                        tvar = self.template_variant(variant)
                        template = ("", tvar, self.default_template)
                        self.default_template = tvar
                        break

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
