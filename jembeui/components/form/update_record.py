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
from markupsafe import Markup
from flask_sqlalchemy import Model
from flask_babel import lazy_gettext as _

from .form import CForm, WDB
from ...includes.link import Link
from ...includes.form import Form

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    import jembe
    import jembeui

__all__ = ("CUpdateRecord",)


class CUpdateRecord(CForm):
    """Displayes form that updates a record

    Functionalites over CForm:

    - implemnts modified fields property and is_from_modified
    """

    class Config(CForm.Config):
        """Configures Update Record component"""

        def __init__(
            self,
            form: Type["jembeui.Form"],
            get_record: Optional[
                Callable[["jembeui.CForm"], Union["Model", dict]]
            ] = None,
            get_record_version: Optional[Callable[[Union["Model", dict]], str]] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            grab_focus: bool = True,
            confirm_cancel: bool = True,
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            form_state_name: str = "form",
            submit_title: Union[str, Callable[["jembeui.CForm"], str]] = _("Save"),
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
            self.get_record_version = get_record_version

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
        self,
        record_id: int,
        form: Optional[Form] = None,
        modified_fields: Tuple[str, ...] = (),
        record_version: Optional[str] = None,
        _record: Optional[Union[Model, dict]] = None,
        wdb: Optional[WDB] = None,
    ):
        if _record is not None and (
            _record["id"] == record_id
            if isinstance(_record, dict)
            else _record.id == record_id
        ):
            self.record = _record
        if record_version is None:
            self.state.record_version = self.record_version
        super().__init__()

    @property
    def record_version(self) -> str:
        """Record version is used as protectio of multiple simultanus updates by different users/sessions"""
        record = self.record
        if self._config.get_record_version is not None:
            return self._config.get_record_version(record)

        if isinstance(record, dict):
            return str(record.get("version", 0))
        else:
            return str(getattr(record, "version", 0))

    def before_form_submit(self) -> None:
        # check if record is modified by other user/session/request in meantime
        if self.state.record_version != self.record_version:
            self.jui.push_page_message(
                _("Can't save the changes!"),
                Markup(
                    _(
                        "<div class='prose'>"
                        "<p>Saving your changes will erase changes already made by another user.</p>"
                        "<p><strong>Cancel the update and start again.</strong></p>"
                        "</div>"
                    )
                ),
                "error",
            )
            raise ValueError(
                _("Concurrent update detected. Can't save changes!")
            )
        return super().before_form_submit()

    def push_page_alert_on_form_submit(self):
        self.jui.push_page_alert(_("{} updated.").format(self.title), "success")
