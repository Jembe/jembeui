from typing import Dict, TYPE_CHECKING, Optional
from ...exceptions import JembeUIError

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("JUIFieldMixin",)


class JUIFieldMixin:
    """
    Adds jembe components support to form field so that component
    can be registred by field itself.

    Subcomponent will be registred with field name as prefix to avoid
    colision of component names
    """

    _cform: "jembeui.CForm"

    @property
    def cform(self) -> "jembeui.CForm":
        try:
            return self._cform
        except AttributeError:
            raise JembeUIError(
                "Field is not mounted by its form and cform attribute is not avaiable!"
            )

    @property
    def form(self) -> "jembeui.FormBase":
        try:
            return self._form
        except AttributeError:
            raise JembeUIError(
                "Field is not mounted by its form and cform attribute is not avaiable!"
            )

    def jui_mount(self, form: "jembeui.FormBase"):
        self._form = form
        self._cform = form.cform

    def jui_component_name(self, name: str) -> str:
        return "{}__{}__{}".format(
            "form",
            self.short_name,  # type:ignore
            name,
        )

    def jui_get_components(self) -> Dict[str, "jembe.ComponentRef"]:
        return dict()

    def jui_component(
        self, _component_name: str, **kwargs
    ) -> "jembe.ComponentReference":
        """Renders component by its name set by field without using field name prefix."""
        return self.cform._jinja2_component(
            self.jui_component_name(_component_name), **kwargs
        )

    def jui_component_placeholder(self, _component_name: str, **kwargs):
        """Renders component placeholder by its name set by field without using field name prefix."""
        return self.cform._jinja2_placeholder(
            self.jui_component_name(_component_name), **kwargs
        )
