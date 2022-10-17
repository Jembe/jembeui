from typing import (
    TYPE_CHECKING,
    Optional,
    Callable,
    Type,
    Union,
    Sequence,
    Iterable,
    Dict,
    Tuple,
)
from flask_sqlalchemy import Model
from flask_babel import lazy_gettext as _
from .form_adaptable import CFormAdaptable
from ...includes.link import Link
from ...includes.form import Form

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    import jembe
    import jembeui

__all__ = ("CUpdateRecordAdaptable",)


class CUpdateRecordAdaptable(CFormAdaptable):
    """Displayes form that updates a record

    Functionalites over CForm:

    - implemnts modified fields property and is_from_modified
    """

    class Config(CFormAdaptable.Config):
        """Configures Update Record component"""

        def __init__(
            self,
            get_form: Callable[["jembeui.CFormAdaptable"], Type["jembeui.Form"]],
            get_record: Optional[
                Callable[["jembeui.CFormAdaptable"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            grab_focus: bool = True,
            confirm_cancel: bool = True,
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            form_state_name: str = "form",
            submit_title: Union[str, Callable[["jembeui.CFormAdaptable"], str]] = _("Save"),
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
            self.submit_title = submit_title
            if menu is None:
                menu = [
                    Link(
                        "submit()",
                        title=submit_title,
                        style="btn-primary",
                        as_button=True,
                    ),
                    Link("cancel()", _("Cancel"), style="btn-ghost", as_button=True),
                ]
            super().__init__(
                get_form,
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
        self,
        record_id: int,
        form: Optional[Form] = None,
        modified_fields: Tuple[str, ...] = (),
        _record: Optional[Union[Model, dict]] = None,
    ):
        if _record is not None and (
            _record["id"] == record_id
            if isinstance(_record, dict)
            else _record.id == record_id
        ):
            self.record = _record
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
        self.jui.push_page_alert(_("{} updated.").format(self.title), "success")
