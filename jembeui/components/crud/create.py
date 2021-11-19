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
from flask_sqlalchemy import Model, SQLAlchemy
from jembe import action
from .form import CForm
from ...lib import Form, Menu, ActionLink

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CCreateRecord",)


def default_on_submit(c: "jembeui.CCreateRecord", r: Union["Model", str]):
    c.jui_push_notification("Created sucessefuly", "success")


def default_on_cancel(c: "jembeui.CUpdateRecord", r: Union["Model", str]):
    return c.state.form.cancel(r)


def default_on_invalid_form(c: "jembeui.CCreateRecord"):
    # TODO chek are they errors not associated with field and display it
    c.jui_push_notification("Form is invalid", "warn")


def default_on_submit_exception(c: "jembeui.CCreateRecord", error: "Exception"):
    if isinstance(error, sa.exc.SQLAlchemyError):
        c.jui_push_notification(
            str(getattr(error, "orig", error))
            if isinstance(error, sa.exc.SQLAlchemyError)
            else str(error),
            "error",
        )
    else:
        c.jui_push_notification(str(error), "error")


class CCreateRecord(CForm):
    class Config(CForm.Config):
        default_template_exp = "jembeui/{style}/components/crud/create.html"

        def __init__(
            self,
            form: "Form",
            get_record: Optional[
                Callable[["jembeui.CCreateRecord"], Union["Model", dict]]
            ] = None,
            redisplay_on_submit: bool = False,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            on_submit: Optional[
                Callable[["jembeui.CCreateRecord", Union["Model", dict]], None]
            ] = default_on_submit,
            on_invalid_form: Optional[
                Callable[["jembeui.CCreateRecord"], None]
            ] = default_on_invalid_form,
            on_submit_exception: Optional[
                Callable[["jembeui.CCreateRecord", "Exception"], None]
            ] = default_on_submit_exception,
            on_cancel: Optional[
                Callable[
                    ["jembeui.CCreateRecord", Union["Model", dict]], Optional[bool]
                ]
            ] = default_on_cancel,
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
            self.redisplay_on_submit = redisplay_on_submit
            if menu is None:
                menu = Menu(
                    [
                        ActionLink("submit()", "Save", styling=dict(primary=True)),
                        ActionLink("cancel()", "Cancel"),
                    ]
                )
            self.on_submit = on_submit
            self.on_invalid_form = on_invalid_form
            self.on_submit_exception = on_submit_exception
            self.on_cancel = on_cancel
            super().__init__(
                form,
                get_record=get_record,
                menu=menu,
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
        form: Optional[Form] = None,
        modified_fields: Tuple[str, ...] = (),
    ):
        super().__init__(form=form)

    @action
    def submit(self) -> Optional[bool]:
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
        if confirmed or not self.state.modified_fields:
            redisplay: Optional[bool] = None
            if self._config.on_cancel:
                redisplay = self._config.on_cancel(self, self.record)
            self.emit("cancel", record=self.record, record_id=None)
            return redisplay
        else:
            self.jui_confirm_action(
                "cancel",
                "Unsaved changes",
                "You have unsaved changes in {} that will be lost.".format(self.title),
            )

    @action
    def validate(self, only_modified_fields: bool = False):
        """
            Validates form without submiting it

            if only_modified_fields is True then validate only modified fields not the whole
            form
        """
        is_valid = True
        if only_modified_fields:
            for field_name in self.state.modified_fields:
                is_valid = getattr(self.state.form, field_name).validate(
                    self.state.form
                ) and is_valid
        else:
            is_valid = self.state.form.validate()
        if not is_valid and self._config.on_invalid_form:
            self._config.on_invalid_form(self)
        return True