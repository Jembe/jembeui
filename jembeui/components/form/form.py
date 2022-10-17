from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from ...includes.field import FieldMixin
from .form_base import CFormBase

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy, Model

__all__ = ("CForm",)


class CForm(CFormBase):
    """Component capable of initialising and displaying jembeui.Form

    Supports addvanced jembeu Fields (jembeu.FieldMixin) that can register
    subcomponents to form.
    Doesn't suport changin jembeui.Form class in runtime.

    - Form instance is acuired by component using self.form property.
    - CForm does not support changig form class
    """

    class Config(CFormBase.Config):
        """Configure options for Form Component:

        - form: Form class to be used. Required.
        - get_record: Callable to get record that should be displayed in form. Optional.
        - grab_focus: Instruct form to grab focus when displayed for the first time on
            page. Default is True.
        - redisplay_on_submit: Should component redisplay it self on successfull submit.
            Default is False.
        - redisplay_on_cancel: should component redisplay it self on successfull cancel.
            Default is False.
        - confirm_cancel: Should we ask user to confirm cancel when the form is changed. Default is True.
        - db: Sqlalchemy database for saving modified record when record is
            instance of Model, if None default db configured for JembeUI is used. Default is None,
        """

        def __init__(
            self,
            form: Type["jembeui.Form"],
            get_record: Optional[
                Callable[["jembeui.CForm"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            grab_focus: bool = True,
            confirm_cancel: bool = True,
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            form_state_name: str = "form",
            db: Optional["SQLAlchemy"] = None,
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
            self.form = form

            # Add components defined by jembeui.FiledMixin
            if components is None:
                components = {}
            # get fields from from and add for subcomponents defined by fields
            # this is the reason why form can't be dynamic
            for field in self.form():
                if isinstance(field, FieldMixin):
                    components.update(field.get_jembeui_components())

            super().__init__(
                get_record,
                menu,
                grab_focus,
                confirm_cancel,
                redisplay_on_submit,
                redisplay_on_cancel,
                form_state_name,
                db,
                title,
                template,
                components,
                inject_into_components,
                redisplay,
                changes_url,
                url_query_params,
            )

    _config: Config

    def inject_into(self, cconfig: "jembe.ComponentConfig") -> Dict[str, Any]:
        """Injects "_form" init parameter into subcomponents registred by form fields

        Subcomponent of field can accept this init parameter to
        gain access of parent form when needed
        """
        if cconfig.name.startswith("form_field__"):
            return {"_from": self.form}
        return {}

    def get_form_type(self) -> Type["jembeui.Form"]:
        """Return subclass of jembeui.Form which instance will be displayed"""
        return self._config.form

    def validate_form_instance(self, form: "jembeui.Form"):
        """Validates if form instance can be used inside component

        - no need to check for fields that extends FieldMixin
        """
