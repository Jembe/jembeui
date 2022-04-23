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
import sqlalchemy as sa
from flask_sqlalchemy import Model
from flask import current_app
from jembe import NotFound, listener, action

from ..component import Component
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ...lib import Form, Menu, JUIFieldMixin

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = (
    "CFormBase",
    "CForm",
)


class CFormBase(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/crud/form.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembeui.CFormBase"], Union["Model", dict]]
            ] = None,
            grab_focus_on_display: bool = True,
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
            self.grab_focus_on_display = grab_focus_on_display
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
                    submited_record_id = submited_record.get("id", None)
                else:
                    submited_record_id = getattr(submited_record, "id", None)

                self.emit(
                    "submit",
                    record=submited_record,
                    record_id=submited_record_id,
                )
                return self.on_submit_success(submited_record)
            except Exception as error:
                self.on_submit_exception(error)
                if current_app.debug or current_app.testing:
                    import traceback

                    traceback.print_exc()
        else:
            self.on_invalid_form()
        if not isinstance(self.record, dict):
            self.session.rollback()
        return True

    def on_submit_success(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        self.push_notification_on_submit()
        return None

    def on_submit_exception(self, error: Exception):
        if isinstance(error, sa.exc.SQLAlchemyError):
            self.jui_push_notification(
                str(getattr(error, "orig", error))
                if isinstance(error, sa.exc.SQLAlchemyError)
                else str(error),
                "error",
            )
        elif isinstance(error, ValueError):
            self.jui_push_notification(str(error), "warn")
        else:
            self.jui_push_notification(str(error), "error")

    def on_invalid_form(self):
        self.push_notification_on_invalid_form()

    @action
    def cancel(self, confirmed: bool = False):
        if self.form.is_disabled:
            self.emit(
                "cancel",
                id=self.record.get("id", None)
                if isinstance(self.record, dict)
                else getattr(self.record, "id", None),
                record=self.record,
            )
        # update and create
        if confirmed or not self.is_form_modified:
            self.form.cancel(self.record)
            redisplay = self.on_cancel()
            self.emit(
                "cancel",
                record=self.record,
                record_id=self.record.get("id", None)
                if isinstance(self.record, dict)
                else getattr(self.record, "id", None),
            )
            return redisplay
        else:
            self.jui_confirm_action(
                "cancel", "Unsaved changes", self.create_cancel_confirmation_question()
            )

    def on_cancel(self) -> Optional[bool]:
        self.push_notification_on_cancel()
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

    def push_notification_on_submit(self):
        pass

    def push_notification_on_cancel(self):
        pass

    def push_notification_on_invalid_form(self):
        pass

    def create_cancel_confirmation_question(self) -> str:
        return "Unsaved changes in will be lost!"


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
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            grab_focus_on_display: bool = False,
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
            self.redisplay_on_submit = redisplay_on_submit
            self.redisplay_on_cancel = redisplay_on_cancel
            self.cancel_needs_confirmation = cancel_needs_confirmation

            self.menu: "jembeui.Menu" = (
                Menu()
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            super().__init__(
                form,
                get_record=get_record,
                grab_focus_on_display=grab_focus_on_display,
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
        super().__init__()

    def init(self):
        super().init()
        # form must be mounted in init to clean up files in temp
        self.form

    @property
    def form(self) -> "Form":
        if self.state.form is None:
            self.state.form = (
                self._config.form(data=self.record)
                if isinstance(self.record, dict)
                else self._config.form(obj=self.record)
            )
        if not self.state.form.is_mounted:
            self.state.form.mount(self, "form")
        return self.state.form

    @form.setter
    def form(self, form: Optional["Form"]):
        self.state.form = form

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()

    def on_submit_success(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        super().on_submit_success(submited_record)

        if self._config.redisplay_on_submit:
            # repopulate form from database
            self.state.form = None
        return self._config.redisplay_on_submit

    @action
    def cancel(self, confirmed: bool = False):
        return super().cancel(
            confirmed if self._config.cancel_needs_confirmation else True
        )

    def on_cancel(self) -> Optional[bool]:
        super().on_cancel()

        if self._config.redisplay_on_cancel:
            # repopulate form from database
            self.state.form = None
        return self._config.redisplay_on_cancel
