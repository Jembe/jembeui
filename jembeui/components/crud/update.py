from jembeui.lib.link import ActionLink
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
import sqlalchemy as sa
from flask_sqlalchemy import Model
from jembe import action
from .form import CForm
from ...lib import Form, Menu, Link, ActionLink

if TYPE_CHECKING:
    import jembe

__all__ = ("CUpdateRecord",)


def default_on_submit(c: "CUpdateRecord", r: Union["Model", str]):
    c.jui_push_notification("Saved sucessefuly", "success")


def default_on_invalid_form(c: "CUpdateRecord"):
    # TODO chek are they errors not associated with field and display it
    c.jui_push_notification("Form is invalid", "warn")


def default_on_submit_exception(c: "CUpdateRecord", error: "Exception"):
    if isinstance(error, sa.exc.SQLAlchemyError):
        c.jui_push_notification(
            str(getattr(error, "orig", error))
            if isinstance(error, sa.exc.SQLAlchemyError)
            else str(error),
            "error",
        )
    else:
        c.jui_push_notification(str(error), "error")


class CUpdateRecord(CForm):
    class Config(CForm.Config):
        default_template_exp = "jembeui/{style}/components/crud/update.html"

        def __init__(
            self,
            form: "Form",
            get_record: Optional[
                Callable[["CUpdateRecord"], Union["Model", dict]]
            ] = None,
            redisplay_on_submit: bool = False,
            menu: Optional[Union["Menu", Sequence[Union["Link", "Menu"]]]] = None,
            on_submit: Optional[
                Callable[["CUpdateRecord", Union["Model", dict]], None]
            ] = default_on_submit,
            on_invalid_form: Optional[
                Callable[["CUpdateRecord"], None]
            ] = default_on_invalid_form,
            on_submit_exception: Optional[
                Callable[["CUpdateRecord", "Exception"], None]
            ] = default_on_submit_exception,
            on_cancel: Optional[Callable[["CUpdateRecord"], None]] = None,
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
            self.redisplay_on_submit = redisplay_on_submit
            self.menu: "Menu" = (
                Menu(
                    [
                        ActionLink("submit()", "Save", styling=dict(primary=True)),
                        ActionLink("cancel()", "Cancel"),
                    ]
                )
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            self.on_submit = on_submit
            self.on_invalid_form = on_invalid_form
            self.on_submit_exception = on_submit_exception
            self.on_cancel = on_cancel
            super().__init__(
                form,
                get_record=get_record,
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
        is_modified: bool = False,
        _record: Optional[Union[Model, dict]] = None,
    ):
        if _record is not None and (
            _record["id"] == id if isinstance(_record, dict) else _record.id == id
        ):
            self._record = _record
        super().__init__(form=form)

    @action
    def submit(self) -> Optional[bool]:
        self.mount()
        if self.state.form.validate():
            try:
                submited_record = self.state.form.submit(self.record)
                self.session.commit()
                self.emit(
                    "submit",
                    record=submited_record,
                    record_id=submited_record["id"]
                    if isinstance(submited_record, dict)
                    else submited_record.id,
                )
                if self._config.on_submit:
                    self._config.on_submit(self, submited_record)
                return self._config.redisplay_on_submit
            except Exception as error:
                if self._config.on_submit_exception:
                    self._config.on_submit_exception(self, error)
        else:
            if self._config.on_invalid_form:
                self._config.on_invalid_form(self)
        self.session.rollback()
        return True

    @action
    def cancel(self, confirmed: bool = False):
        if confirmed or not self.state.is_modified:
            if self._config.on_cancel:
                self._config.on_cancel(self)
            self.emit(
                "cancel",
                record=self.record,
                record_id=self.record["id"]
                if isinstance(self.record, dict)
                else self.record.id,
            )
        else:
            self.jui_confirm_action(
                "cancel",
                "Unsaved changes",
                "You have unsaved changes in {} that will be lost.".format(self.title),
            )

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()
