from typing import (
    TYPE_CHECKING,
    Optional,
    Callable,
    Sequence,
    Union,
    Dict,
    Iterable,
    Tuple,
    Any,
)
from jembe import NotFound, listener, action
from flask_sqlalchemy import Model
import sqlalchemy as sa

from ..component import Component
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ...lib import Form, Menu, JUIFieldMixin

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CFormBase", "CForm", "cformbase_default_on_submit_exception")


def cformbase_default_on_submit_exception(c: "jembeui.CFormBase", error: "Exception"):
    if isinstance(error, sa.exc.SQLAlchemyError):
        c.jui_push_notification(
            str(getattr(error, "orig", error))
            if isinstance(error, sa.exc.SQLAlchemyError)
            else str(error),
            "error",
        )
    else:
        c.jui_push_notification(str(error), "error")


class CFormBase(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/crud/form.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembeui.CFormBase"], Union["Model", dict]]
            ] = None,
            on_submit_success: Optional[
                Callable[
                    ["jembeui.CFormBase", Optional[Union["Model", dict]]],
                    Optional[bool],
                ]
            ] = None,
            on_invalid_form: Optional[Callable[["jembeui.CFormBase"], None]] = None,
            on_submit_exception: Optional[
                Callable[["jembeui.CFormBase", "Exception"], None]
            ] = cformbase_default_on_submit_exception,
            on_cancel: Optional[Callable[["jembeui.CFormBase"], Optional[bool]]] = None,
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
            self.get_record = get_record
            self.on_submit_success = on_submit_success
            self.on_invalid_form = on_invalid_form
            self.on_submit_exception = on_submit_exception
            self.on_cancel = on_cancel
            # defult db can be useds when db is None
            if db is not None:
                self.db: "SQLAlchemy" = db
            else:
                self.db = get_jembeui().default_db
                if self.db is None:
                    raise JembeUIError(
                        "Either 'db' for CListRecords.Config or default_db"
                        " on JembeUI instance must be set"
                    )

            # Add components defined by JUIFormFields
            if components is None:
                components = {}
            for field in self.form():
                if isinstance(field, JUIFieldMixin):
                    components.update(field.jui_get_components())

            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    def inject_into(self, cconfig: "jembe.ComponentConfig") -> Dict[str, Any]:
        # inject _form into subcomponents injected by JUIField
        if cconfig.name.startswith("form_field__"):
            return {"_form": self.form}
        return {}

    def __init__(self):
        self._record: Union["Model", dict]
        super().__init__()

    @classmethod
    def load_init_param(
        cls, config: "jembe.ComponentConfig", name: str, value: Any
    ) -> Any:
        # if not overriden it fill use jembeui.lib.form.Form.load_init_param
        if name == "form":
            return config.form.load_init_param(value)
        return super().load_init_param(config, name, value)

    def get_record(self) -> Union["Model", dict]:
        if self._config.get_record is None:
            raise JembeUIError(
                "You need to implement get_record method or to add config parameter get_record to component: {}".format(
                    self._config.full_name
                )
            )
        return self._config.get_record(self)

    @property
    def record(self) -> Union["Model", dict]:
        try:
            return self._record
        except AttributeError:
            self._record = self.get_record()

        if self._record is None:
            raise NotFound()
        return self._record

    @record.setter
    def record(self, value: Union["Model", dict]):
        self._record = value

    @property
    def form(self) -> "Form":
        """Returns form instance"""
        try:
            return self._form
        except AttributeError:
            raise NotImplementedError()

    @form.setter
    def form(self, form: "Form"):
        self._form = form

    @property
    def is_form_modified(self) -> bool:
        """Should return true when form is modified by user and not submited"""
        return False if self.form.is_disabled else True

    @property
    def modified_form_fields(self) -> Optional[Sequence[str]]:
        """Should return list of modified fields or None if component doesn' track modified fields"""
        return None

    @property
    def session(self) -> "sa.orm.scoping.scoped_session":
        return self._config.db.session

    @listener(event="update_form_field")
    def on_update_form_field(self, event: "jembe.Event"):
        if not self.form.is_disabled:
            field = getattr(self.form, event.params["name"])
            field.data = event.params["value"]

    @action
    def submit(self):
        if self.form.is_disabled:
            raise JembeUIError("Can't submit disabled form")

        if self.form.validate():
            try:
                submited_record = self.form.submit(self.record)

                if submited_record is None:
                    submited_record_id = None
                elif isinstance(submited_record, dict):
                    submited_record_id = submited_record["id"]
                else:
                    submited_record_id = submited_record.id

                self.emit(
                    "submit",
                    record=submited_record,
                    record_id=submited_record_id,
                )
                return self.on_submit_success(submited_record)
            except Exception as error:
                self.on_submit_exception(error)
        else:
            if self._config.on_invalid_form:
                self._config.on_invalid_form(self)
        if not isinstance(self.record, dict):
            self.session.rollback()
        return True

    def on_submit_success(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        if self._config.on_submit_success:
            return self._config.on_submit_success(self, submited_record)
        return None

    def on_submit_exception(self, error: Exception):
        if self._config.on_submit_exception:
            self._config.on_submit_exception(self, error)

    def on_invalid_form(self):
        if self._config.on_invalid_form:
            self._config.on_invalid_form(self)

    @action
    def cancel(self, confirmed: bool = False):
        if self.form.is_disabled:
            self.emit(
                "cancel",
                id=self.record["id"]
                if isinstance(self.record, dict)
                else self.record.id,
                record=self.record,
            )
        # update and create
        if confirmed or not self.is_form_modified:
            self.form.cancel(self.record)
            redisplay = self.on_cancel()
            self.emit(
                "cancel",
                record=self.record,
                record_id=self.record["id"]
                if isinstance(self.record, dict)
                else self.record.id,
            )
            return redisplay
        else:
            self.jui_confirm_action(
                "cancel",
                "Unsaved changes",
                "You have unsaved changes in {} that will be lost.".format(self.title),
            )

    def on_cancel(self) -> Optional[bool]:
        if self._config.on_cancel:
            return self._config.on_cancel(self)
        return None

    @action
    def validate(self, only_modified_fields: bool = False):
        """
        Validates form without submiting it.

        if only_modified_fields is True then validate only modified fields not the whole
        form
        """
        if self.form.is_disabled:
            raise JembeUIError("Can't validate disabled form")

        is_valid = True
        if only_modified_fields and self.modified_form_fields is not None:
            for field_name in self.modified_form_fields:
                is_valid = is_valid and getattr(self.form, field_name).validate(
                    self.form
                )
        else:
            is_valid = self.form.validate()
        if not is_valid:
            self.on_invalid_form()
        return True


class CForm(CFormBase):
    class Config(CFormBase.Config):
        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembeui.CFormBase"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            on_submit_success: Optional[
                Callable[["jembeui.CFormBase", Union["Model", dict]], Optional[bool]]
            ] = None,
            on_invalid_form: Optional[Callable[["jembeui.CFormBase"], None]] = None,
            on_submit_exception: Optional[
                Callable[["jembeui.CFormBase", "Exception"], None]
            ] = cformbase_default_on_submit_exception,
            on_cancel: Optional[Callable[["jembeui.CFormBase"], Optional[bool]]] = None,
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
            self.menu: "jembeui.Menu" = (
                Menu()
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            super().__init__(
                form,
                get_record=get_record,
                on_submit_success=on_submit_success,
                on_invalid_form=on_invalid_form,
                on_submit_exception=on_submit_exception,
                on_cancel=on_cancel,
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

    def __init__(self, form: Optional[Form] = None):
        if self.state.form is None:
            self.state.form = (
                self._config.form(data=self.record)
                if isinstance(self.record, dict)
                else self._config.form(obj=self.record)
            )

        self.state.form.mount(self, "form")
        self.form = self.state.form
        super().__init__()

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()
