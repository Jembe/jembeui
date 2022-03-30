from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Union
from copy import deepcopy
from datetime import date, datetime
from abc import ABCMeta
from markupsafe import Markup
import wtforms as wtf
from flask import render_template
from jembe import JembeInitParamSupport, ComponentPreviousStateUnavaiableError

from ...settings import settings
from ...exceptions import JembeUIError
from ..form_fields import JUIFieldMixin, FileField


if TYPE_CHECKING:
    import jembeui
    import wtforms
    from flask_sqlalchemy import Model

__all__ = (
    "Form",
    "FormBase",
)


class FormMeta(wtf.form.FormMeta, ABCMeta):
    pass


class FormBase(JembeInitParamSupport, wtf.Form, metaclass=FormMeta):
    """
    Form should be used together with CForm component and its variants
    CEdit, CCreate, CView to represent actual form.

    Form:
    - must be mounted by CForm component before being processed (displayed, etc).
    - renters itself inside CForm component template
    - CForm should call Form methods submit and cancel when user executes those
      actions on CForm
    """

    # full path name of template
    __template__: Union[str, Sequence[str]] = "jembeui/{style}/widgets/form.html"
    # __template__ = Form.template_variant("inline")
    __styling__: Sequence[str] = ()

    RENDER_KW: Dict[str, Dict[str, Any]]

    def __init__(
        self,
        formdata=None,
        obj=None,
        prefix="",
        data=None,
        meta=None,
        disabled: bool = False,
        **kwargs
    ):
        self.is_disabled = disabled
        self.is_mounted = False
        self.cform: "jembeui.CForm"
        super().__init__(
            formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs
        )
        # copy class var RENDER_KW to instance var RENDER_KW
        if "RENDER_KW" not in self.__class__.__dict__:
            self.__class__.RENDER_KW = dict()
            for field in self:
                self.__class__.RENDER_KW[field.name] = {}
                if field.render_kw:
                    self.__class__.RENDER_KW[field.name] = field.render_kw.copy()
                    field.render_kw = {
                        k: v
                        for k, v in field.render_kw.items()
                        if not k.endswith("+") and not k.startswith("_")
                    }
        self.RENDER_KW = deepcopy(self.__class__.RENDER_KW)

        # to change render_kw dynamicaly by subclasses we must
        # oweride render_kw of every field instance with fresh copy
        # otherwise changes to render_kw will be permanent
        for field in self:
            setattr(
                field,
                "render_kw",
                {
                    k: v
                    for k, v in field.render_kw.items()
                    if not k.endswith("+") and not k.startswith("_")
                }
                if field.render_kw
                else {},
            )

    @classmethod
    def dump_init_param(cls, value: Any) -> Any:
        def dump_param(field_name, value):
            if isinstance(value, JembeInitParamSupport):
                return value.dump_init_param(value)
            elif isinstance(value, (date, datetime)):
                return value.isoformat()
            return value

        return (
            {
                k: dump_param(k, v)
                for k, v in value.data.items()
                if getattr(getattr(cls, k, None), "render_kw", dict()).get(
                    "disabled", None
                )
                is None
            }
            if value is not None
            else dict()
        )

    @classmethod
    def load_init_param(cls, value: dict) -> Any:
        def load_param(field_name, value):
            fc = getattr(cls, field_name).field_class
            if issubclass(fc, wtf.DateField):
                return date.fromisoformat(value) if value is not None else None
            elif issubclass(fc, wtf.DateTimeField):
                return datetime.fromisoformat(value) if value is not None else None
            return value

        return cls(
            data={
                k: load_param(k, v)
                for k, v in value.items()
                if getattr(getattr(cls, k, None), "render_kw", dict()).get(
                    "disabled", None
                )
                is None
            }
        )

    def mount(
        self, cform: "jembeui.CForm", form_state_name: Optional[str] = None
    ) -> "jembeui.Form":
        """
        Mount is called by CFrom before form is displayed or before
        form needs aditional processing
        """
        if self.is_mounted and cform != self.cform:
            raise JembeUIError(
                "Form {} can't be mounted multiple times!".format(
                    self.__class__.__name__
                )
            )
        if not self.is_mounted:
            self.cform = cform

            # if field is Jembe UI Field call jembe ui mount
            # to associate form and form compoennt to field instance
            for field in self:
                if isinstance(field, JUIFieldMixin):
                    field.jui_mount(self)

            self.init()
            self.is_mounted = True
        return self

    def init(self):
        """Called only once when form instance is mounted/ready to be displayed/validated
        Place to alter form behavior"""
        pass

    def submit(self, record: Union["Model", dict]) -> Optional[Union["Model", dict]]:
        if isinstance(record, dict):
            # TODO
            raise JembeUIError(
                "You must provide submit logic for form when record is dict by overriding 'submit' method"
            )
            # return record
        else:
            self.populate_obj(record)
            self.cform.session.add(record)
            self.cform.session.commit()
            return record

    def cancel(self, record: Union["Model", dict]):
        pass

    def set_disabled(self, *fields: "wtforms.Field", disabled: bool = True):
        for field in fields:
            self.set_renderkw(field, "disabled", disabled)

    def as_html(self, _variant_or_template_name: Optional[str] = None) -> str:
        """Renders form using self.__template__ jinja2 template or specific template if provided in argument.

        Args:
            _variant_or_template_name (str, optional): Full path to template to be used or name of the template variant of default template. Defaults to None.

        Returns:
            str: rendered and marked as safe html string
        """
        _template = (
            [self.__template__]
            if isinstance(self.__template__, str)
            else list(self.__template__)
        )
        _variant = None
        if _variant_or_template_name is not None:
            if "." in _variant_or_template_name:
                # template name
                _template = [_variant_or_template_name] + _template
            else:
                # variant name
                _variant = _variant_or_template_name
        template = [tn.format(style=settings.default_style) for tn in _template]
        if _variant:
            template = [
                tn.replace(".html", "__{}.html".format(_variant)) for tn in template
            ]
        context = self.cform._get_default_template_context()
        return Markup(render_template(template, **context))

    def template_variant(self, variant_name: str):
        if isinstance(self.__template__, str):
            return [
                self.__template__.replace(".html", "__{}.html".format(variant_name))
            ]
        else:
            return [
                tn.replace(".html", "__{}.html".format(variant_name))
                for tn in self.__template__
            ]

    def __join_kw(self, kw1: dict, kw2: dict, as_defaults: bool = False) -> dict:
        result = kw1.copy()
        for k, w in kw2.items():
            if as_defaults and not k.endswith("+") and not isinstance(w, (list, dict)):
                k = "{}+".format(k)

            if not k.endswith("+") and not isinstance(w, (list, dict)):
                result[k] = w
            elif (
                as_defaults and k.strip("+") in kw1 and not isinstance(w, (list, dict))
            ):
                pass
            else:
                if isinstance(w, dict):
                    result[k] = (
                        w
                        if k not in result
                        else self.__join_kw(result[k], w, as_defaults)
                    )
                elif isinstance(w, list):
                    result[k] = w if k not in result else [*result[k], *w]
                else:  # str
                    result[k] = w if k not in result else " ".join((result[k], w))
        return result

    def __resolve_kw(self, kw: dict) -> dict:
        result: Dict[str, Any] = {}
        for k, w in kw.items():
            if k not in result:
                if k.endswith("+"):
                    kn = k.strip("+")
                    if kn in kw:
                        if isinstance(w, dict):
                            result[kn] = self.__resolve_kw(
                                self.__join_kw(result[kn], w)
                            )
                        elif isinstance(w, (list, tuple)):
                            result[kn] = [*result[kn], *w]
                        else:  # str
                            result[kn] = " ".join((result[kn], w))
                    else:
                        if isinstance(w, dict):
                            result[kn] = self.__resolve_kw(w)
                        else:
                            result[kn] = w
                else:
                    if isinstance(w, dict):
                        result[k] = self.__resolve_kw(w)
                    else:
                        result[k] = w
        return result

    def resolve_kw(
        self,
        render_kw: dict,
        additional_kw: Optional[dict] = None,
        additional_as_default: bool = True,
    ) -> dict:
        if additional_kw:
            return self.__resolve_kw(
                self.__join_kw(render_kw, additional_kw, additional_as_default)
            )
        else:
            return self.__resolve_kw(render_kw)

    def attr_kw(self, kw: dict) -> dict:
        return {
            k: v
            for k, v in kw.items()
            if not k.startswith("_")
            and not k.endswith("+")
            and isinstance(v, (str, int, bool))
        }

    def set_renderkw(self, field: "wtforms.Field", param_name: str, value: Any) -> Any:
        self.RENDER_KW[field.name][param_name] = value
        return value
        # return self.RENDER_KW[field.name].setdefault(param_name, value)
        # return field.render_kw.setdefault(param_name, value)


class Form(FormBase):
    """
    Adds support for default behavior for handling uploaded files in form
    when form is changed, canceled and submited.
    Olso adds instant validate and submit switches
    """

    # If __instant_validate__ is True, validate action will be called
    # after field value is changed by user
    __instant_validate__: bool = False
    # If __instant_submit__ is True, submit action will be called
    # after field value is changed by user
    __instant_submit__: bool = False
    # __instant_validate__ and __instant_submit__ functionality should be implemnted by
    # field templates

    def mount(
        self, cform: "jembeui.CForm", form_state_name: Optional[str] = None
    ) -> "jembeui.Form":
        if not self.is_mounted:
            for field in self:  # type:ignore
                if isinstance(field, FileField):
                    if field.data and field.data.is_just_uploaded():
                        # if file is just uploaded and it is valid file
                        # move it to temp storage
                        # otherwise remove file from disk and set it to None
                        if field.validate(self):
                            field.data.move_to_temp()
                        else:
                            field.data.remove()
                            field.data = None
                    # remove previous field value (file) if file is in temp storage
                    # when changing upload file without submit
                    # to remove changed file from disk
                    try:
                        if form_state_name and cform.previous_state:
                            previous_form_field = getattr(
                                cform.previous_state[form_state_name], field.name
                            )
                            if (
                                previous_form_field
                                and previous_form_field.data
                                and previous_form_field.data.in_temp_storage()
                                and previous_form_field.data != field.data
                            ):
                                previous_form_field.data.remove()
                    except ComponentPreviousStateUnavaiableError:
                        pass
        return super().mount(cform)  # type:ignore

    def cancel(self, record: Union["Model", dict]):
        for field in self:  # type:ignore
            if isinstance(field, FileField):
                # if file field is changed before canceling form
                # remove new file from server
                record_field = (
                    record.get(field.name, None)
                    if isinstance(record, dict)
                    else getattr(record, field.name, None)
                )
                if field.data and (
                    field.data.in_temp_storage() or field.data != record_field
                ):
                    field.data.remove()
                    field.data = None
        super().cancel(record)  # type:ignore

    def submit(self, record: Union["Model", dict]) -> Optional[Union["Model", dict]]:
        for field in self:  # type:ignore
            if isinstance(field, FileField):
                if field.data and field.data.in_temp_storage():
                    # move photo in public storage for permanent keep
                    field.data.move_to_public()
                if record:
                    if isinstance(record, dict):
                        if record[field.name] and record[field.name] != field.data:
                            # delete old file when it's replaced with new one
                            record[field.name].remove()
                            record[field.name] = None
                    else:
                        record_field = getattr(record, field.name)
                        if record_field and record_field != field.data:
                            # delete old file when it's replaced with new one
                            record_field.remove()
                            record_field = None
        return super().submit(record)  # type:ignore
