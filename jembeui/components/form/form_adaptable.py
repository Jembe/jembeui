from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from .form_base import CFormBase

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy, Model

__all__ = ("CFormAdaptable",)


class CFormAdaptable(CFormBase):
    """Component capable of initialising and displaying jembeui.Form

    Support changin jembeui.Form class in runtime.
    Doesn't supports addvanced jembeu Fields (jembeu.FieldMixin).
    subcomponents to form.
    """

    class Config(CFormBase.Config):
        """Configure options for Form Component:
        # TODO
        """

        def __init__(
            self,
            get_form: Callable[["jembeui.CFormAdaptable"], Type["jembeui.Form"]],
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
            self.get_form = get_form

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

    def get_form_type(self) -> Type["jembeui.Form"]:
        """Return subclass of jembeui.Form which instance will be displayed"""
        return self._config.get_form(self)
