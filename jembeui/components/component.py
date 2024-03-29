from typing import Callable, Dict, Iterable, Optional, Tuple, Union
from flask import current_app
import jembe
from jembe import listener
from ._jui_utils import JuiUtils
from ..helpers import get_component_template_variants, create_thumbnail
from ..exceptions import JembeUIError


__all__ = ("Component",)


class Component(jembe.Component):
    """
    Base component for all Jembe UI components.
    """

    class Config(jembe.Component.Config):
        """Adds support for title and template variants"""

        default_template: str = "jembeui/components/component.html"
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
            self.title = title if title is not None else self.default_title
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
            # Initialise default class level values here because we need app_context to do that
            if "default_template" not in cls.__dict__:
                if cls.default_template:
                    # copy defalult template to class property
                    cls.default_template = cls.default_template
                else:
                    raise JembeUIError(
                        f"Default_template class propert must be set for JembeUI components: {cls}"
                    )
            if "TEMPLATE_VARIANTS" not in cls.__dict__:
                cls.TEMPLATE_VARIANTS = get_component_template_variants(
                    cls.default_template
                )

        def default_title(self, component: "jembe.Component") -> str:
            """Get default component title"""
            return self.name.replace("_", " ").title()

        @classmethod
        def template_variant(cls, variant_name: str) -> str:
            """Returns template name for variant_name if exist"""
            cls._init_class_based_config()
            if variant_name in cls.TEMPLATE_VARIANTS:
                return cls.TEMPLATE_VARIANTS[variant_name]
            raise JembeUIError(
                f"Template variant '{variant_name}' for '{cls.default_template}' does not exist"
            )

        @property
        def default_template_names(self) -> Tuple[str, ...]:
            """REturns names of default templates"""
            # use fullname to generate default tempalte name
            tname = f"{self.full_name.strip('/')}.html"
            templates = [tname, f"pages/{tname}"]

            # if component is in components package use it to generate default
            # template by package name
            for mro in self._component_class.__mro__:
                packages = mro.__module__.split(".")
                if len(packages) > 1 and packages[0] not in ("jembe", "jembeui"):
                    try:
                        components_index = packages.index("components")
                        if len(packages) > 1 and packages[-1] == packages[-2]:
                            templates.append(
                                f"{'/'.join(packages[components_index:-1])}.html"
                            )
                        else:
                            templates.append(
                                f"{'/'.join(packages[components_index:])}.html"
                            )
                    except ValueError:
                        pass

            # return template names
            return tuple(templates)

    _config: Config

    def init(self):
        self.update_ac()
        return super().init()

    @property
    def title(self) -> str:
        """Component title"""
        if "title" in self.state and self.state.title is not None:
            return self.state.title

        if callable(self._config.title):
            return self._config.title(self)

        return self._config.title

    _jui_utils: JuiUtils

    @property
    def jui(self) -> JuiUtils:
        """JembeUi Component Utils instance"""
        try:
            return self._jui_utils
        except AttributeError:
            self._jui_utils = JuiUtils(self)
            return self._jui_utils

    @listener(event="userHasConfirmedTheAction")
    def jui_user_has_confirmed_the_action(self, event: "jembe.Event"):
        if hasattr(self, event.action_name):
            return getattr(self, event.action_name)(**event.action_params)

    @listener(event="redisplay")
    def jui_on_redisplay(self, event: "jembe.Event"):
        if event.params.get("update_ac", False) == True:
            try:
                self.update_ac()
            except Exception:
                self.ac_deny()
                if current_app.debug or current_app.testing:
                    current_app.logger.warning(
                        f"Exception in {self.__class__.__name__}.update_ac. Access to compomonent {self.exec_name} is denied. "
                        "(exceptation trackback below)"
                    )
                    import traceback

                    traceback.print_exc()
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
                    f"Exception in {self.__class__.__name__}.update_ac. Access to compomonent {self.exec_name} is denied. "
                    "(exceptation trackback below)"
                )
                import traceback

                traceback.print_exc()
        return avaiable != self.ac_check() and avaiable is False

    def update_ac(self):
        pass

    def hydrate(self):
        """Hydrate is called by display
        to allow separtaion of control logic/calculations and display logic
        useful when extending class behavior"""

    def display(self) -> "jembe.DisplayResponse":
        self.hydrate()
        # Add create_thumbnail function in template context
        self.create_thumbnail = create_thumbnail
        return super().display()
