from typing import TYPE_CHECKING, Dict
from jembeui.exceptions import JembeUIError

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("FieldMixin",)


class FieldMixin:
    """
    Adds following functionalities to WTForm Fields:

    - Ability to register child component to parente JembeUI Component (multiselect, LOV, etc);
        - child components will be prefixed with field name to avoid component name colisions.
    - Ability to render registred child compnent in its template;
    - Access parent JembeUI CForm(Component) instance;
    - Access to parent WTForm instance;

    FieldMixin must be used inside CForm in order to provide additional functionalities
    """

    _cform: "jembeui.CBaseForm"
    _form: "jembeui.Form"

    @property
    def cform(self) -> "jembeui.CBaseForm":
        """Parent CForm component instance"""
        try:
            return self._cform
        except AttributeError as err:
            raise JembeUIError(
                "Field must be mounted to access parent form component!"
            ) from err

    @property
    def form(self) -> "jembeui.Form":
        """Parent Form instance"""
        try:
            return self._form
        except AttributeError as err:
            raise JembeUIError(
                "Field must be mounted to access its form instance!"
            ) from err

    def mount_jembeui_form(self, form: "jembeui.Form"):
        """Mounts field inside the Form"""
        if not form.is_mounted:
            raise JembeUIError("Can't mount form filed inside unmounted form!")
        self._form = form
        self._cform = form.cform

    def get_jembeui_component_name(self, name: str) -> str:
        """Returns name to be used by parent CForm component to register field subcomponent"""
        return f"form_field__{self.short_name}__{name}"  # type:ignore

    def get_jembeui_components(self) -> Dict[str, "jembe.ComponentRef"]:
        """Returns dict of components to be registred into form parent Component"""
        return {}

    def jembeui_component(
        self, _component_name: str, **kwargs
    ) -> "jembe.ComponentReference":
        """Renders component registred by the field inside template.

        - _component_name: name defined by field, without prefix add by CForm
        """
        return self.cform._jinja2_component(
            self.get_jembeui_component_name(_component_name), **kwargs
        )

    def jembeui_component_placeholder(self, _component_name: str, **kwargs) -> str:
        """Renders component placeholder registred by the field inside the template

        - _component_name: name defined by the field, without prefixes
        """
        return self.cform._jinja2_placeholder(
            self.get_jembeui_component_name(_component_name), **kwargs
        )
