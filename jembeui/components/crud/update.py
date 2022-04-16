from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    Callable,
    Iterable,
    Tuple,
    Dict,
    Sequence,
)
from flask_sqlalchemy import Model, SQLAlchemy
from .form import CForm
from ...lib import Form, Menu, ActionLink

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CUpdateRecord",)


class CUpdateRecord(CForm):
    class Config(CForm.Config):
        # default_template_exp = "jembeui/{style}/components/crud/update.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembeui.CFormBase"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            grab_focus_on_display: bool = True,
            cancel_needs_confirmation: bool = True,
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
                menu = Menu(
                    [
                        ActionLink("submit()", "Save", styling=("primary",)),
                        ActionLink("cancel()", "Cancel"),
                    ]
                )
            super().__init__(
                form,
                get_record=get_record,
                menu=menu,
                redisplay_on_submit=redisplay_on_submit,
                redisplay_on_cancel=redisplay_on_cancel,
                grab_focus_on_display=grab_focus_on_display,
                cancel_needs_confirmation=cancel_needs_confirmation,
                db=db,
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    def __init__(
        self,
        id: int,
        form: Optional[Form] = None,
        modified_fields: Tuple[str, ...] = (),
        _record: Optional[Union[Model, dict]] = None,
    ):
        if _record is not None and (
            _record["id"] == id if isinstance(_record, dict) else _record.id == id
        ):
            self.record = _record
            # insp = sa.inspect(_record)
            # if insp.presistent or insp.pending:
            #     self._record = _record
        super().__init__(form=form)

    @property
    def is_form_modified(self) -> bool:
        return len(self.state.modified_fields) > 0

    @property
    def modified_form_fields(self) -> Optional[Sequence[str]]:
        return self.state.modified_fields

    def on_submit_success(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        self.state.modified_fields = ()
        return super().on_submit_success(submited_record)

    def on_cancel(self) -> Optional[bool]:
        self.state.modified_fields = ()
        return super().on_cancel()

    def push_notification_on_invalid_form(self):
        self.jui_push_notification("Form is invalid", "warn")

    def push_notification_on_submit(self):
        self.jui_push_notification("{} updated.".format(self.title), "success")
