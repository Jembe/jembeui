from typing import (
    TYPE_CHECKING,
    Optional,
    Callable,
    Union,
    Sequence,
    Iterable,
    Dict,
    Tuple,
)
from flask_babel import lazy_gettext as _
from .form import CForm
from ...includes.link import Link
from ...includes.form import Form

if TYPE_CHECKING:
    from flask_sqlalchemy import Model, SQLAlchemy
    import jembe
    import jembeui
__all__ = ("CCreateRecord",)


class CCreateRecord(CForm):
    """Displayes form that creates new record

    - implemnts modified fields property and is_from_modified
    - add default menu
    """

    class Config(CForm.Config):
        def __init__(
            self,
            form: "jembeui.Form",
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
            if menu is None:
                menu = [
                    Link("submit()", _("Save"), style="btn-primary", as_button=True),
                    Link("cancel()", _("Cancel"), style="btn-ghost", as_button=True),
                ]
            super().__init__(
                form,
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

    def __init__(
        self, form: Optional[Form] = None, modified_fields: Tuple[str, ...] = ()
    ):
        super().__init__()

    @property
    def modified_form_fields(self) -> Optional[Sequence[str]]:
        return self.state.modified_fields

    def on_form_submited(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        self.state.modified_fields = ()
        return super().on_form_submited(submited_record)

    def on_form_canceled(self) -> Optional[bool]:
        self.state.modified_fields = ()
        return super().on_form_canceled()

    def push_page_alert_on_form_submit(self):
        self.jui.push_page_alert(_("{} created.").format(self.title), "success")

    def push_page_alert_on_form_invalid(self):
        self.jui.push_page_alert(_("Form is invalid"), "warning")
