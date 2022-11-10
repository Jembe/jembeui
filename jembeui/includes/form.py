from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    Sequence,
    Type,
    Union,
    Dict,
)
from datetime import datetime, date
from copy import copy, deepcopy
from abc import ABCMeta
from dataclasses import dataclass, asdict
from markupsafe import Markup
import wtforms as wtf
from flask import render_template
from jembeui import JembeUIError
from jembe import JembeInitParamSupport, ComponentPreviousStateUnavaiableError
from .file_field import FileField
from .field import FieldMixin
from jembe import IsDataclass

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import Model

__all__ = ("Form", "TrailFormConfig")


@dataclass
class TrailFormConfig:
    title: str
    form: Type["jembeui.Form"]
    model: Type["Model"]
    relationship_name: Optional[str]
    dataclass: "jembe.IsDataclass"
    get_records: Callable[["jembeui.CForm"], List["Model"]]
    create_record: Optional[Callable[["jembeui.CForm"], "Model"]] = None
    submit_records: Optional[
        Callable[["jembeui.CForm", List["jembe.IsDataclass"]], None]
    ] = None
    model_to_dataclass: Callable[
        ["Model"], "jembe.IsDataclass"
    ] = lambda record: record.to_dataclass()

    def __post_init__(self):
        if self.submit_records is None and self.relationship_name is not None:
            self.submit_records = self.submit_records_default
        if self.submit_records is None and self.relationship_name is None:
            raise ValueError(
                "Please provide submit_records or relationship_name attribute"
            )
        if self.create_record is None:
            self.create_record = lambda c: self.model()

    def submit_records_default(self, c: "jembeui.CForm", records_dc: List[IsDataclass]):
        if self.relationship_name is None:
            raise ValueError("reltionship_name must be set")

        records = list(self.get_records(c))
        # update or delete existing records in database
        for record in records:
            record_dc = next((r for r in records_dc if r.id == record.id), None)
            if record_dc:
                # update record
                updated = False
                for k, v in asdict(record_dc).items():
                    if hasattr(record, k) and getattr(record, k) != v:
                        setattr(record, k, v)
                        updated = True
                if updated:
                    c.session.add(record)
            else:
                c.session.delete(record)
        # create new records in database
        for record_dc in records_dc:
            if record_dc.id is None:
                record = self.model()
                setattr(record, self.relationship_name, c.record)
                for k, v in asdict(record_dc).items():
                    if hasattr(record, k) and getattr(record, k) != v:
                        setattr(record, k, v)
                c.session.add(record)


class FormMeta(wtf.form.FormMeta, ABCMeta):
    """To avoid metaclass confilict for Form"""


class Form(JembeInitParamSupport, wtf.Form, metaclass=FormMeta):
    """Extends and adapts WTForm to be used by JembeUI.

    Following features are added:

    - Support for JembeUI form Fields that accepts Form instance
    - Form instance can access parent component
    - Support for working with SaFile fields
    - Support for cancel and submit actions with acces to parent component
    - support of submiting sqlalchemy records directly to DB

    - Form must be used together with jembeui.CForm component.
    - Form can render itself using __style__ class variable and render method

    TODO give beter explanation how form renders work using style
    """

    __trail_forms__: Dict[str, "jembeui.TrailFormConfig"]

    @dataclass
    class FieldStyle:
        """Defines how individual field should be displayed

        Args:
            disabled: Disable field. Default is False.
            template: Template to be used to render the field. If None
                    default template for specific field will be used. Can be list
                    of templates.
                    Template can ignore all other settings of the field style.
                    Default is None.
            is_compact: Display without label and description on top. Use placeholder as label. Default False
            field: set by JembeUI
            form_style: Parent form style. Set by JembeUI
        """

        disabled: bool = False

        is_compact: bool = False
        size: Optional[str] = None

        on_change_submit: Optional[bool] = None
        on_change_validate: Optional[bool] = None
        on_change_defer: Optional[bool] = None

        template: Optional[Union[str, Sequence[str]]] = None

        _field: Optional["wtf.Field"] = None
        _form_style: Optional["jembeui.Form.Style"] = None

        _base_class: str = "input"

        DEFAULT_TEMPLATE = "jembeui/includes/input.html"
        TEMPLATE_BY_CLASS_NAME = {
            # "HiddenField": "jembeui/includes/input_hidden.html",
            "DateField": "jembeui/includes/input_date.html",
            "LovField": "jembeui/includes/input_lov.html",
        }  # type:ignore

        def mount(
            self, field: "wtf.Field", form_style: "jembeui.Form.Style"
        ) -> "jembeui.Form.FieldStyle":
            """Mount instance of Style to specific field"""
            self._field = field
            self._form_style = form_style

            if (
                field.render_kw
                and "disabled" in field.render_kw
                and field.render_kw["disabled"]
            ):
                self.disabled = True

            # field size
            if self.size is None and self._form_style.fields_size is not None:
                self.size = self._form_style.fields_size

            # on change submit
            if self.on_change_submit is None:
                if self._form_style.on_change_submit is not None:
                    self.on_change_submit = self._form_style.on_change_submit
                else:
                    self.on_change_submit = False

            # on change validate
            if self.on_change_validate is None:
                if self._form_style.on_change_validate is not None:
                    self.on_change_validate = self._form_style.on_change_validate
                else:
                    self.on_change_validate = False

            # on change defer
            if self.on_change_defer is None:
                if self._form_style.on_change_defer is not None:
                    self.on_change_defer = self._form_style.on_change_defer
                else:
                    self.on_change_defer = True

            if self.template is None:
                self.template = self.TEMPLATE_BY_CLASS_NAME.get(
                    field.__class__.__name__, self.DEFAULT_TEMPLATE
                )

            # support select
            if self.field and isinstance(self.field.widget, wtf.widgets.Select):
                self._base_class = "select"

            return self

        def render(self) -> str:
            """Renders field as HTML"""
            if self._field is None or self._form_style is None:
                raise JembeUIError("Field is not mounted")
            if self._form_style.form is None:
                raise JembeUIError("Form is not mounted")
            ctx = {
                "field": self._field,
                "field_style": self,
                "form": self._form_style.form,
                "cform": self._form_style.form.cform,
            }
            return Markup(render_template(self.template, **ctx))  # type:ignore

        def __call__(self) -> str:
            """Renders field as HTML"""
            return self.render()

        @property
        def is_hidden_field(self) -> bool:
            """Returns True if field is hidden"""
            if self._field is None:
                raise JembeUIError("Field style is not mounted")
            return isinstance(self._field.widget, wtf.widgets.HiddenInput)

        @property
        def mark_if_optional(self) -> bool:
            """Put marking on optional fields"""
            if self._form_style is None:
                raise JembeUIError("Field style is not mounted")
            return self._form_style.mark_optional_fields

        @property
        def mark_if_required(self) -> bool:
            """Put marking on required fields"""
            if self._form_style is None:
                raise JembeUIError("Field style is not mounted")
            return self._form_style.mark_required_fields

        @property
        def form_style(self) -> Optional["jembeui.Form.Style"]:
            """REturn Form style of the Form to wich this field is attached to"""
            return self._form_style

        @property
        def field(self) -> Optional["wtf.Field"]:
            """Return Field to which tish field style is attached to"""
            return self._field

    @dataclass
    class Style:
        """Defines how form should be displayed.

        - classes: list of classes to add to the form container
        - disabled: Disable all fields in form. Default is False.
        - instant_validate: call validate imediatlly after field value is changed. Default is None
        - on_change_submit: call submited imediatlly after field value is changed. Default is None.
        - template: Default template to render the from. Can be list of
            template names.
            Templates can ignore all other settings of the form style.

        All functionalites except template must be implemented inside form and/or
        field templates.
        """

        disabled: bool = False
        classes: Optional[str] = None

        fields_size: Optional[str] = None
        fields: Optional[Dict[str, "jembeui.Form.FieldStyle"]] = None

        # instant_validate: bool = False
        on_change_submit: Optional[bool] = None
        on_change_validate: Optional[bool] = None
        on_change_defer: Optional[bool] = None

        template: Union[str, Sequence[str]] = "jembeui/includes/form.html"

        mark_optional_fields: bool = True
        mark_required_fields: bool = False

        _form: Optional["jembeui.Form"] = None

        def get_field_style(self, field: "wtf.Field") -> "jembeui.Form.FieldStyle":
            """Returns configured or default mounted field style and save it to self.fields"""

            if self.fields is None or field.name not in self.fields:
                field_style = Form.FieldStyle()
                if self.fields:
                    self.fields[field.name] = field_style
                else:
                    self.fields = {field.name: field_style}
            else:
                field_style = self.fields[field.name]
                if field_style.field == field:
                    return field_style

            field_style.mount(field, self)

            if self.disabled:
                field_style.disabled = True

            return field_style

        def field_style(self, field_name: str) -> "jembeui.Form.FieldStyle":
            """Return field style for field name"""
            if not self._form:
                raise ValueError("FormStyle is not mounted")

            if self.fields is None or field_name not in self.fields:
                field_style = Form.FieldStyle()
                if self.fields:
                    self.fields[field_name] = field_style
                else:
                    self.fields = {field_name: field_style}
            else:
                field_style = self.fields[field_name]
                if (
                    field_style.field is not None
                    and field_style.field.name == field_name
                ):
                    return field_style
            field = getattr(self._form, field_name)
            if field is None:
                raise ValueError(
                    f"field {field_name} does not exist in form {self._form}"
                )
            field_style.mount(field, self)

            if self.disabled:
                field_style.disabled = True

            return field_style

        def mount(self, form: "jembeui.Form") -> "jembeui.Form.Style":
            """Mount instance of Style to specific form"""
            self._form = form

            if self._form.is_disabled:
                self.disabled = True

            if (
                self._form
                and self._form.cform
                and getattr(self._form.cform._config, "is_trail_form", False)
            ):
                self.on_change_defer = True
                self.on_change_submit = True

            return self

        def field_styles(self):
            """Iterate over field styles for displaying purpose

            - if self.fields is defined respec order in it, and iterate only over
                fields in the self.fields
            - iterate over all fields as they are defined in form
            """
            for field in self._form:
                yield self.get_field_style(field)

        def updated_from_dict(self, **kwargs) -> "jembeui.Form.Style":
            """Create new style from this one where settings are updated form dict"""

            def update_ostr(k, check_value=lambda x: len(x) > 0):
                if k in kwargs and check_value(v := kwargs[k]):
                    if getattr(new_style, k) is None:
                        setattr(new_style, k, str(v))
                    else:
                        setattr(new_style, k, " ".join((getattr(new_style, k), str(v))))

            def update_bool(k, check_value=lambda x: True):
                if k in kwargs and check_value(v := kwargs[k]):
                    setattr(new_style, k, bool(v))

            new_style = copy(self)
            update_bool("disabled")
            update_ostr("classes")
            return new_style

        def render(self, **kwargs) -> str:
            """Renders form as HTML"""
            ctx = {
                "form": self._form,
                "form_style": self.updated_from_dict(**kwargs),
                "has_field": lambda field_name: (
                    field_name in self._form if self._form else False
                ),
                "field_style": lambda field_name: self.field_style(field_name),
                "component": self._form.cform._jinja2_component if self._form else None,
                "component_reset": self._form.cform._jinja2_component_reset
                if self._form
                else None,
                "placeholder": self._form.cform._jinja2_placeholder
                if self._form
                else None,
            }
            return Markup(render_template(self.template, **ctx))  # type:ignore

        def __call__(self, *args, **kwargs) -> str:
            """Renders form as HTML"""
            return self.render(**kwargs)

        @property
        def form(self) -> Optional["jembeui.Form"]:
            return self._form

    __style__: Style = Style()

    def __init__(
        self,
        formdata=None,
        obj=None,
        prefix="",
        data=None,
        meta=None,
        disabled: bool = False,
        **kwargs,
    ):
        self.cform: "jembeui.CForm"

        self.is_disabled = disabled

        self.is_mounted = False
        super().__init__(
            formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs
        )

    def mount(
        self, cform: "jembeui.CForm", form_state_name: Optional[str] = None
    ) -> "jembeui.Form":
        """Mounts Form inside jembeui.CForm component

        Args:
            cform (jembeui.CForm): CForm component that mounts the form
            form_state_name (Optional[str], optional): Name of state param
                of CForm comonent when form is defined as state param. Defaults to None.

        form_state_name is used to monitor if form field is changed between
        to consequent request. This is usefull to delete temporary uploaded files.
        """
        if self.is_mounted:
            if cform != self.cform:
                raise JembeUIError(
                    f"{self.__class__.__name__} can't be mounted multiple times!"
                )
            else:
                # No need to mounti it again
                return self

        self.cform = cform
        self.is_mounted = True

        for field in self:
            if isinstance(field, FieldMixin):
                field.mount_jembeui_form(self)
            if isinstance(field, FileField):
                if field.data and field.data.is_just_uploaded():
                    # File is just uploaded
                    if field.validate(self):
                        # File is valid:
                        # - Move it to temporary storage
                        field.data = field.data.move_to_temp()
                    else:
                        # File is not valid:
                        # - remove it from disk
                        # - set field data to None
                        field.data.remove()
                        field.data = None
                # Check if new file is uploaded and previous file
                # is in temporary storage
                try:
                    if form_state_name and cform.previous_state:
                        previous_field = getattr(
                            cform.previous_state[form_state_name], field.name
                        )
                        if (
                            previous_field
                            and previous_field.data
                            and previous_field.data.in_temp_storage()
                            and previous_field.data != field.data
                        ):
                            previous_field.data.remove()
                except ComponentPreviousStateUnavaiableError:
                    # ignore exception
                    pass

        self.init()

        return self

    @classmethod
    def dump_init_param(cls, value: Optional["jembeui.Form"]) -> Any:
        """Transform form into JSON ready object"""

        def dump_param(value):
            """Dumps form field to JSON ready object depending of field type"""
            if isinstance(value, JembeInitParamSupport):
                return value.dump_init_param(value)
            elif isinstance(value, (date, datetime)):
                return value.isoformat()
            return value

        if value is None:
            return dict()
        else:
            result = {k: dump_param(v) for k, v in value.data.items()}
            return result

    @classmethod
    def load_init_param(cls, value: dict) -> Any:
        """Reconstruct form from JSON ready object"""

        def load_param(field_name, value):
            """Reconstruct form field from JSON ready object"""
            field_class = getattr(cls, field_name).field_class
            if issubclass(field_class, wtf.DateField):
                return date.fromisoformat(value) if value is not None else None
            elif issubclass(field_class, wtf.DateTimeField):
                return datetime.fromisoformat(value) if value is not None else None
            return value

        return cls(data={k: load_param(k, v) for k, v in value.items()})

    def _is_field_permanently_disabled(self, field_name: str) -> bool:
        """Checks is field is permanently disabled by form or field style.

        Permanently disabled fields can't be update on client, thay are
        excluded from component state.
        """
        form_style = self.get_form_style()
        field = getattr(self, field_name)
        return (
            form_style.disabled
            or (field.render_kw and field.render_kw.get("disabled", False))
            or (
                form_style.fields is not None
                and field_name in form_style.fields
                and form_style.fields[field_name].disabled
            )
        )

    def populate_obj(self, obj):
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields.

        :note: This is a destructive operation; Any attribute with the same name
               as a field will be overridden. Use with caution.

        :note: Disabled field are not populated
        """
        for name, field in self._fields.items():
            if not self._is_field_permanently_disabled(name):
                field.populate_obj(obj, name)

    def init(self):
        """Lifecycle hook: Called once when form instance is mounted to CForm"""

    def submit(self, record: Union["Model", dict]) -> Optional[Union["Model", dict]]:
        """
        Lifecycle hook: Called when form is submited

        Default implementation of update and commit record in sqlalchemy when record is instance of Model
        """
        if isinstance(record, dict):
            raise JembeUIError(
                "Provide custom form.submit() implementation for record of dict type."
            )

        self.handle_files_on_submit(record)

        self.populate_obj(record)
        self.cform.session.add(record)
        # self.cform.session.commit()
        return record

    def cancel(self, record: Union["Model", dict]):
        """Lifecycle hook: Called when form is canceled"""
        self.handle_files_on_cancel(record)

    def handle_files_on_submit(self, record: Union["Model", dict]):
        """
        Handle moving uploaded files to default public storage on submit

        Moving files to protected or non default storages must be handled manualy
        before calling this method.
        """
        for field in self:
            if isinstance(field, FileField):
                if field.data and field.data.in_temp_storage():
                    field.data = field.data.move_to_public()
                if record:
                    if isinstance(record, dict):
                        if record[field.name] and record[field.name] != field.data:
                            # delete old file before it's replaced with the new one
                            record[field.name].remove()
                            record[field.name] = None
                        else:
                            file_in_record = getattr(record, field.name, None)
                            if file_in_record and file_in_record != field.data:
                                # delete old file
                                file_in_record.remove()
                                setattr(record, field.name, None)

    def handle_files_on_cancel(self, record: Union["Model", dict]):
        """Handle removing temporary files from server on form cancel"""
        # find File fields
        for field in self:
            if isinstance(field, FileField):
                # if file is changed remove new file from the server
                if field.data:
                    # get file in original record
                    if isinstance(record, dict):
                        file_in_record = record.get(field.name, None)
                    else:
                        file_in_record = record.getattr(record, field.name, None)

                    if field.data.in_temp_storage() or field.data != file_in_record:
                        field.data.remove()
                        field.data = None

    def get_form_style(self):
        """Returns editable copy of cls.__style__

        Subsequen calls will return the same copy of style,
        allowing user to update style only to this specific form instance
        """
        try:
            return self._instance_style
        except AttributeError:
            self._instance_style = deepcopy(self.__style__)
            self._instance_style.mount(self)
            return self._instance_style

    def get_jembeui_components(self) -> Dict[str, "jembe.ComponentRef"]:
        """Return subcomponents defined inside form that should be added
        to CForm compoennt

        By default returns components defined by jembe.FieldMixin fileds.
        Override method to add additional components
        """
        components = {}
        # add jembe field subcomponents
        # get fields from form dummy instance
        for field in self:
            if isinstance(field, FieldMixin):
                components.update(
                    {
                        field.get_jembeui_component_name(n): c
                        for n, c in field.get_jembeui_components().items()
                    }
                )

        return components

    @classmethod
    def get_trail_form_component_name(cls, trail_form_name: str) -> str:
        return f"form__{trail_form_name}"

    def __call__(self, **kwargs) -> str:
        """Renders form using style configuration"""
        return self.get_form_style().render(**kwargs)
