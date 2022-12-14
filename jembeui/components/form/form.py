from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)
from dataclasses import asdict, is_dataclass
import sqlalchemy as sa
from uuid import uuid1

from flask_sqlalchemy import Model
from flask_babel import lazy_gettext as _
from flask import current_app
from jembe.common import dataclass_from_dict
from jembe import NotFound, listener, action, IsDataclass
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ..component import Component
from ...includes.form import Form
from ...includes.menu import Menu

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CForm", "WDB")

WDB = Dict[str, List[Tuple[str, IsDataclass]]]


class CForm(Component):
    """Component capable of initialising and displaying jembeui.Form"""

    class Config(Component.Config):
        """Configure options for Form Component:
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
            form: Type["jembeui.Form"],
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
            # _is_trail_form: bool = False,
            # _trail_form_dataclass: Optional[IsDataclass] = None,
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

            # Add components defined by jembeui.FiledMixin
            if components is None:
                components = {}
            # get fields from from and add for subcomponents defined by fields
            # this is the reason why form can't be dynamic
            components.update(self.form().get_jembeui_components())

            # Lead form
            self.is_lead_form = hasattr(form, "__trail_forms__")
            self.trail_forms_config = {}
            if self.is_lead_form:
                # Add trail form config and compoents

                self.trail_forms_config = {
                    form.get_trail_form_component_name(name): tfc
                    for name, tfc in form.__trail_forms__.items()
                }

                for name, tfc in self.trail_forms_config.items():
                    if name not in components:
                        components[name] = self.get_trail_form_component(tfc)

            # Use default db when db is None
            if db is not None:
                self.db: "SQLAlchemy" = db
            else:
                self.db = get_jembeui().default_db
                if self.db is None:
                    raise JembeUIError(
                        "Configure 'default_db' for JembeUI or 'db' Component.Config parameter"
                    )

            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        def get_trail_form_component(
            self, tfc: "jembeui.TrailFormConfig"
        ) -> "jembe.ComponentRef":
            from .trail_form import CTrailUpdateForm

            return (
                CTrailUpdateForm,
                CTrailUpdateForm.Config(
                    form=tfc.form,
                    trail_form_dataclass=tfc.dataclass,
                    changes_url=False,
                ),
            )

    _config: Config

    _record: Union["Model", dict]

    def __init__(self, wdb: Optional[WDB] = None):
        super().__init__()

    def init(self):
        if self._config.is_lead_form:
            if "wdb" not in self.state:
                raise JembeUIError(
                    f"wdb state parameter must be configured for lead form {self._config.full_name}."
                )
            if self.state.wdb is None:
                # Initialise WDB Working data on client
                self.state.wdb = self._create_wdb()
        return super().init()

    @classmethod
    def load_init_param(
        cls, config: "jembe.ComponentConfig", name: str, value: Any
    ) -> Any:
        """Load 'form'/_config.form_state_name state param using form specific load"""
        if name == config.form_state_name:
            return config.form.load_init_param(value)
        elif name == "wdb" and config.is_lead_form:
            if value is None:
                return None
            return {
                tfcname: [
                    (
                        uid,
                        dataclass_from_dict(
                            config.trail_forms_config[tfcname].dataclass, r
                        ),
                    )
                    for uid, r in record_list
                ]
                for tfcname, record_list in value.items()
            }

        return super().load_init_param(config, name, value)

    def inject_into(self, cconfig: "jembe.ComponentConfig") -> Dict[str, Any]:
        """Injects "_form" init parameter into subcomponents registred by form fields

        Subcomponent of field can accept this init parameter to
        gain access of parent form when needed
        """
        if cconfig.name.startswith("form__"):
            return {
                "record_id": self.record.get("id", None)
                if isinstance(self.record, dict)
                else getattr(self.record, "id", None),
                "_record": self.record,
                "_form": self._get_form(),
            }
        return {}

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
        """Returns mounted form instance"""
        form = self._get_form()
        if not form.is_mounted:
            form.mount(self)
        return form

    @form.setter
    def form(self, form: "Form"):
        if self._config.form_state_name in self.state.keys():
            self.state.form = form
        else:
            self._form = form

    def _get_form(self) -> "Form":
        """Returns form instance not mounted, usefull when injecting into sub componentds

        - Form instance is saved and retrived from state if 'form' state exist.
        - Form instance is created and cached localy when 'form' state does not exist."""

        def get_form_init_params():
            if isinstance(self.record, dict):
                return {"data": self.record}
            elif is_dataclass(self.record):
                return {"data": asdict(self.record)}
            else:
                return {"obj": self.record}

        form_type = self._config.form

        if self._config.form_state_name in self.state.keys():
            if self.state.form is None:
                self.state.form = form_type(**get_form_init_params(), cform=self)
            else:
                self.state.form.attach_to(self)
            return self.state.form
        else:
            if not hasattr(self, "_form"):
                self._form = form_type(**get_form_init_params(), cform=self)
            else:
                self._form.attach_to(self)
            return self._form

    @property
    def is_form_modified(self) -> bool:
        """Should return True when form is modified by user and not submited"""
        if self.form.get_form_style().disabled or not self.modified_form_fields:
            return False
        if len(self.modified_form_fields) > 0:
            return True
        return False

    @property
    def modified_form_fields(self) -> Optional[Sequence[str]]:
        """Should return list of modified fields or None if component doesn' track modified fields"""
        if "modified_fields" in self.state:
            return self.state.modified_fields
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
                self.before_form_submit()
                # submit wdb if exist
                if self._config.is_lead_form:
                    for cname, tfc in self._config.trail_forms_config.items():
                        tfc.submit_records(
                            self, [rec for _, rec in self.state.wdb.get(cname, [])]
                        )
                    self.state.wdb = None

                # submit form
                submited_record = self.call_form_submit(self.record)

                # commit database session
                if not isinstance(self.record, dict) and not is_dataclass(self.record):
                    self.session.commit()

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
                # Submit is unsuccessfull
                if not isinstance(self.record, dict) and not is_dataclass(self.record):
                    self.session.rollback()

                self.on_form_submit_exception(error)
        else:
            self.on_form_invalid()

        if current_app.debug or current_app.testing:
            print("Validation Errors: ", self.form.errors)

        return True

    def call_form_submit(
        self, record: Union["Model", dict]
    ) -> Optional[Union["Model", dict]]:
        """Etract actual call to form submit from submit acction for easy overriden and changing behaviors"""
        return self.form.submit(self.record)

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
            # wdb support
            if self._config.is_lead_form:
                self.state.wdb = None
            return redisplay
        else:
            self.jui.ask_for_action_confirmation(
                "cancel",
                _("Unsaved changes"),
                self.get_confirm_cancel_question(),
                is_danger=True,
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

    def before_form_submit(self) -> None:
        """Hook called before form submit but after form is validated"""

    def on_form_submited(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        """Hook called when the from is successfully submited and session is commited

        Returns True, False or None to identify should form redisplay itself.

        Defaults calls self.push_page_alert_on_form_submit and
        returns value defined by _config.redisplay_on_submit"""

        if "modified_fields" in self.state:
            self.state.modified_fields = ()

        self.push_page_alert_on_form_submit()

        if self._config.redisplay_on_submit and isinstance(submited_record, Model):
            # reset form state to get data from database on redisplay
            setattr(self.state, self._config.form_state_name, None)

        return self._config.redisplay_on_submit

    def on_form_canceled(self) -> Optional[bool]:
        """Hook called when the form is canceled.

        Default calls self.push_page_alert_on_form_cancel, and returns
        _config.redisplay_on_cancel"""

        if "modified_fields" in self.state:
            self.state.modified_fields = ()

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
        return _("Unsaved changes will be lost?")

    def hydrate(self):
        """Binds menu from _config if it's configured"""
        self.menu = (
            self._config.menu.bind_to(self) if self._config.menu is not None else None
        )

    # WDB specific methods
    def _create_wdb(self) -> WDB:
        """Creates WDB using _config.trails_forms_config"""
        if not self._config.is_lead_form:
            return {}
        wdb: WDB = {}
        for component_name, tfc in self._config.trail_forms_config.items():
            wdb[component_name] = [
                (uuid1().hex, tfc.model_to_dataclass(record))
                for record in tfc.get_records(self)
            ]
        return wdb

    @action
    def add_wdb_record(self, tfc_name: str, to_end=False):
        """Add wdb_record to wdb and also new trail form to handle it"""
        if not self._config.is_lead_form:
            return None
        if tfc_name not in self._config.trail_forms_config.keys():
            return None

        tfc = self._config.trail_forms_config[tfc_name]

        if tfc.create_record is None:
            raise ValueError("TrailFormConfig.create_record is not defined")
        new_record = tfc.model_to_dataclass(tfc.create_record(self))

        # self.state.wdb[tfc_name].append(new_record)
        if to_end:
            self.state.wdb[tfc_name].append((uuid1().hex, new_record))
        else:
            self.state.wdb[tfc_name] = [(uuid1().hex, new_record)] + self.state.wdb[
                tfc_name
            ]

    @action
    def remove_wdb_record(self, tfcname: str, uid: str):
        """Removes record from wDB"""
        position, record_uid, record = next(
            (
                (idx, rec[0], rec[1])
                for idx, rec in enumerate(self.state.wdb.get(tfcname, []))
                if rec[0] == uid
            ),
            (None, None, None),
        )
        if (
            position is None
            or position < 0
            or position >= len(self.state.wdb.get(tfcname, []))
        ):
            return

        tfc = self._config.trail_forms_config[tfcname]
        if tfc.delete_record is not None:
            if tfc.delete_record(self, record) == True:
                del self.state.wdb[tfcname][position]
        else:
            del self.state.wdb[tfcname][position]

    @listener(event="updateWDB", source="./*.*")
    def on_update_wdb(self, event: "jembe.Event"):
        """Updates wdb by receiving trail form event"""
        if event.source_name in self._config.trail_forms_config:
            tfcname = event.source_name
            operation = event.params.get("operation", "update")
            record = event.params.get("record")
            uid = event.params.get("uid")
            position = next(
                (
                    idx
                    for idx, rec in enumerate(self.state.wdb.get(tfcname, []))
                    if rec[0] == uid
                ),
                None,
            )
            if (
                position is None
                or position < 0
                or position >= len(self.state.wdb.get(tfcname, []))
            ):
                return
            if operation == "update":
                self.state.wdb[tfcname][position] = (uid, record)
            elif operation == "delete":
                del self.state.wdb[tfcname][position]
            return True
