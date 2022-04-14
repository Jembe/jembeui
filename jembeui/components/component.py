from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
from flask import current_app
import jembe
from jembe import listener
from ..settings import settings
from ..helpers import get_component_template_variants
from ..exceptions import JembeUIError

if TYPE_CHECKING:
    import jembe


__all__ = ("Component",)


class Component(jembe.Component):
    """
    Base component for all Jembe UI components.
    """

    class Config(jembe.Component.Config):
        default_template_exp = "jembeui/{style}/components/component.html"
        default_template: str
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
            self._init_class_based_config()
            # regular config params
            self.title = title if title else self.default_title
            if template is None:
                template = ("", self.default_template)
            elif (
                isinstance(template, str)
                and template in self.TEMPLATE_VARIANTS.values()
            ):
                self.default_template = template
                template = ("", template)

            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        @classmethod
        def _init_class_based_config(cls):
            # Initialise default class level values here becouse we need app_context to do that
            if "default_template" not in cls.__dict__:
                cls.default_template = cls.default_template_exp.format(
                    style=settings.default_style
                )
            if "TEMPLATE_VARIANTS" not in cls.__dict__:
                cls.TEMPLATE_VARIANTS = get_component_template_variants(
                    cls.default_template
                )

        def default_title(self, component: "jembe.Component") -> str:
            return self.name.replace("_", " ").title()

        @classmethod
        def template_variant(cls, variant_name: str) -> str:
            """Returns template name for variant_name if exist"""
            cls._init_class_based_config()
            if variant_name in cls.TEMPLATE_VARIANTS:
                return cls.TEMPLATE_VARIANTS[variant_name]
            raise JembeUIError(
                "Template variant {} for {} does not exist".format(
                    variant_name, cls.default_template_exp
                )
            )

    _config: Config

    def init(self):
        self.update_ac()
        return super().init()

    @property
    def title(self) -> str:
        if "title" in self.state and self.state.title is not None:
            return self.state.title

        if isinstance(self._config.title, str):
            return self._config.title

        return self._config.title(self)

    @property
    def jui_style(self) -> str:
        """Adds current JembeUI style to template context

        Returns:
            str: JembeUI style configured by JEMBEUI_STYLE parameter in config.py
        """
        return settings.default_style

    # JembeUI helper methods
    def jui_set_page_title(self, title: Optional[str]):
        self.emit("setPageTitle", title=title)

    def jui_push_notification(self, message: str, level: str = "info"):
        self.emit("pushPageNotification", message=message, level=level)

    def jui_push_notice(self, message: str, title: Optional[str] = None):
        self.emit("pushPageNotice", message=message, title=title)

    def jui_confirm_action(
        self,
        action_name: str,
        title: str,
        question: str = "",
        action_params: Optional[dict] = None,
        confirm_title: str = "OK",
        danger: bool = False,
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
                confirm_title=confirm_title,
                danger=danger,
            ),
        )

    @listener(event="actionConfirmed")
    def jui_on_action_confirmed(self, event: "jembe.Event"):
        if hasattr(self, event.action_name):
            return getattr(self, event.action_name)(**event.action_params)

    @listener(event="redisplay")
    def jui_on_redisplay(self, event: "jembe.Event"):
        return True

    @listener(event="update_ac")
    def jui_on_update_ac(self, event: "jembe.Event"):
        avaiable = self.ac_check()
        try:
            self.update_ac()
        except Exception:
            self.ac_deny()
            if current_app.debug or current_app.testing:
                current_app.logger.warning(
                    "Exception in {}.update_ac. Access to compomonent {} is denied. "
                    "(exceptation trackback below)".format(
                        self.__class__.__name__, self.exec_name
                    )
                )
                import traceback

                traceback.print_exc()
        return avaiable != self.ac_check() and avaiable == False

    def update_ac(self):
        pass

    def hydrate(self):
        pass

    def display(self) -> "jembe.DisplayResponse":
        self.hydrate()
        return super().display()
