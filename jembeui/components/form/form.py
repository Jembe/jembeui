from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import sqlalchemy as sa

from flask_babel import lazy_gettext as _
from flask import current_app
from jembe import NotFound, listener, action
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ..component import Component
from ...includes.form import Form
from ...includes.field import FieldMixin
from ...includes.menu import Menu

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy, Model

__all__ = ("CForm",)


class CForm(Component):
    """Component capable of initialising and displaying jembeui.Form

    - Form instance is acuired by component using self.form property.
    - CForm does not support submiting or canceling form
    """

    class Config(Component.Config):
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

        default_template: str = "jembeui/components/form/form.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[Callable[["CForm"], Union["Model", dict]]] = None,
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
            self.get_record = get_record
            self.menu: Optional["jembeui.Menu"] = (
                None
                if menu is None
                else (
                    Menu(
                        menu,
                        style=Menu.Style(Menu.Style.DROPDOWNS, classes="gap-2"),
                    )
                    if not isinstance(menu, Menu)
                    else menu
                )
            )
            self.grab_focus = grab_focus
            self.confirm_cancel = confirm_cancel
            self.redisplay_on_submit = redisplay_on_submit
            self.redisplay_on_cancel = redisplay_on_cancel
            self.form_state_name = form_state_name

            # Use default db when db is None
            if db is not None:
                self.db: "SQLAlchemy" = db
            else:
                self.db = get_jembeui().default_db
                if self.db is None:
                    raise JembeUIError(
                        "Configure 'default_db' for JembeUI or 'db' Component.Config parameter"
                    )

            # Add components defined by jembeui.FiledMixin
            if components is None:
                components = {}
            # get fields from from and add for subcomponents defined by fields
            # this is the reason why form can't be dynamic
            for field in self.form():
                if isinstance(field, FieldMixin):
                    components.update(field.get_jembeui_components())

            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _class: Config

    _record: Union["Model", dict]

    def inject_into(self, cconfig: "jembe.ComponentConfig") -> Dict[str, Any]:
        """Injects "_form" init parameter into subcomponents registred by form fields

        Subcomponent of field can accept this init parameter to
        gain access of parent form when needed
        """
        if cconfig.name.startswith("form_field__"):
            return {"_from": self.form}
        return {}

    @classmethod
    def load_init_param(
        cls, config: "jembe.ComponentConfig", name: str, value: Any
    ) -> Any:
        """Load 'form'/_config.form_state_name state param using form specific load"""
        if name == config.form_state_name:
            return config.form.load_init_param(value)
        return super().load_init_param(config, name, value)

    def get_record(self) -> Union["Model", dict]:
        """Gets record to be displayed in Form

        By default it calls _config.get_record, but can be overriden
        if more control is need when getting the record completly ignoring
        _config.get_record"""
        if self._config.get_record is not None:
            return self._config.get_record(self)
        raise JembeUIError(
            f"{self.__class__}: "
            "Can get form original record."
            "Add 'get_record' callback in Config or override Form 'get_record' method."
        )

    @property
    def record(self) -> Union["Model", dict]:
        """Gets original record that will be displayed and modified in Form

        Record from self.get_record() is cached by this component instance.

        Raises:
        - NotFound: when self.get_record() returns None"""
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
        """Returns form instance

        - Form instance is saved and retrived from state if 'form' state exist.
        - Form instance is created and cached localy when 'form' state does not exist."""

        if self._config.form_state_name in self.state.keys():
            if self.state.form is None:
                self.state.form = (
                    self._config.form(data=self.record)
                    if isinstance(self.record, dict)
                    else self._config.form(obj=self.record)
                )
            if not self.state.form.is_mounted:
                self.state.form.mount(self, self._config.form_state_name)
            return self.state.form
        else:
            if not hasattr(self, "_form"):
                self._form = (
                    self._config.form(data=self.record)
                    if isinstance(self.record, dict)
                    else self._config.form(obj=self.record)
                )
            if not self._form.is_mounted:
                self._form.mount(self, self._config.form_state_name)
            return self._form

    @form.setter
    def form(self, form: "Form"):
        if self._config.form_state_name in self.state.keys():
            self.state.form = form
        else:
            self._form = form

    @property
    def is_form_modified(self) -> bool:
        """Should return True when form is modified by user and not submited"""
        if self.form.get_form_style().disabled or not self.modified_form_fields:
            return False
        if len(self.modified_form_fields) > 0:
            return True

    @property
    def modified_form_fields(self) -> Optional[Sequence[str]]:
        """Should return list of modified fields or None if component doesn' track modified fields"""
        return None

    @property
    def session(self) -> "sa.orm.scoping.scoped_session":
        """Returns SqlAlchemy session for easy quering the database in lambdas"""
        return self._config.db.session

    @listener(event="update_form_field")
    def on_update_form_field(self, event: "jembe.Event"):
        """Update form field using event listener

        Conviniet whay for updating when using field subcomponents"""
        if not self.form.get_form_style().disabled:
            field = getattr(self.form, event.params["name"])
            field.data = event.params["value"]

    @action
    def submit(self):
        """Submit form changes

        Checks if form is valid if soo calls self.form.submit() to
        submit form changes.

        if _config.redisplay_on_submit is True, component will
        redisplay itself after successfull submision.

        Emits "submit" when form is successfully submited"""

        if self.form.get_form_style().disabled:
            raise JembeUIError("Can't submit disabled form")

        if self.form.validate():
            try:
                # submit form
                submited_record = self.form.submit(self.record)

                # get submited record id
                if submited_record is None:
                    submited_record_id = None
                elif isinstance(submited_record, dict):
                    submited_record_id = submited_record.get("id", None)
                else:
                    submited_record_id = getattr(submited_record, "id", None)

                # emit submit event
                self.emit(
                    "submit", record=submited_record, record_id=submited_record_id
                )

                return self.on_form_submited(submited_record)
            except Exception as error:
                self.on_form_submit_exception(error)
        else:
            self.on_form_invalid()

        # Submit is unsuccessfull
        if not isinstance(self.record, dict):
            self.session.rollback()

        return True

    @action
    def cancel(self, confirmed: bool = False):
        """Cancel form changes

        Depending of _config.confirm_cancel ask user
        to confirm cancelation when form is changed.

        if _config.redisplay_on_cancel is True, component will
        redisplayit self after successfull cancelation.

        Emits "cancel" on successfull form cancelation"""

        # get record id
        record_id = (
            self.record.get("id", None)
            if isinstance(self.record, dict)
            else getattr(self.record, "id", None)
        )

        if self.form.get_form_style().disabled:
            self.emit("cancel", id=record_id, record=self.record)

        if (
            not self._config.confirm_cancel
            or not self.is_form_modified
            or (self._config.confirm_cancel and confirmed)
        ):
            self.form.cancel(self.record)
            redisplay = self.on_form_canceled()
            self.emit("cancel", record=self.record, record_id=record_id)
            return redisplay
        else:
            self.jui.ask_for_action_confirmation(
                "cancel", _("Unsaved changes"), self.get_confirm_cancel_question()
            )

    @action
    def validate(self, modified_fields_only: bool = False):
        """Validates form without submiting it.

        - modified_fields_only<bool>: When True, validate only modified filelds not
            the whole form. Default is False."""

        if self.form.get_form_style().disabled:
            raise JembeUIError("Can't validate disabled form")

        is_valid = True
        if modified_fields_only and self.modified_form_fields is not None:
            for field_name in self.modified_form_fields:
                is_valid = is_valid and getattr(self.form, field_name).validate(
                    self.form
                )
        else:
            is_valid = self.form.validate()

        if not is_valid:
            self.on_form_invalid()

        return True

    def on_form_invalid(self) -> None:
        """Hook called when the form is invalid

        Hook can be called during form submition or validation action.
        Defaults calls self.push_page_alert_on_form_invalid"""
        self.push_page_alert_on_form_invalid()

    def on_form_submited(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        """Hook called when the from is successfully submited

        Returns True, False or None to identify should form redisplay itself.

        Defaults calls self.push_page_alert_on_form_submit and
        returns value defined by _config.redisplay_on_submit"""

        self.push_page_alert_on_form_submit()

        if self._config.redisplay_on_submit:
            # reset form state to get data from database on redisplay
            setattr(self.state, self._config.form_state_name, None)

        return self._config.redisplay_on_submit

    def on_form_canceled(self) -> Optional[bool]:
        """Hook called when the form is canceled.

        Default calls self.push_page_alert_on_form_cancel, and returns
        _config.redisplay_on_cancel"""
        self.push_page_alert_on_form_cancel()
        return self._config.redisplay_on_cancel

    def on_form_submit_exception(self, error: Exception) -> None:
        """Hook called when exception is raised during submit"""
        if isinstance(error, sa.exc.SQLAlchemyError):
            self.jui.push_page_alert(str(getattr(error, "orig", error)), "error")
        elif isinstance(error, ValueError):
            self.jui.push_page_alert(str(error), "warning")
        else:
            self.jui.push_page_alert(str(error), "error")

        if current_app.debug or current_app.testing:
            import traceback

            traceback.print_exc()

    def push_page_alert_on_form_invalid(self):
        """Hook run during self.on_form_invalid to push page alerts"""

    def push_page_alert_on_form_cancel(self):
        """Hook run during self.on_form_cancel to push page alerts"""

    def push_page_alert_on_form_submit(self):
        """Hook run during self.on_form_submited to push page alerts"""

    def get_confirm_cancel_question(self) -> str:
        """Get question for cancel confirmation.

        Default is "Unsaved changes will be lost?"."""
        return "Unsaved changes will be lost?"

    def hydrate(self):
        """Binds menu from _config if it's configured"""
        self.menu = (
            self._config.menu.bind_to(self) if self._config.menu is not None else None
        )
