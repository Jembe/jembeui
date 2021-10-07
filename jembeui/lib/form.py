from typing import TYPE_CHECKING, Any, Dict, Optional, List, Union
from datetime import date, datetime
from abc import ABCMeta
from markupsafe import Markup
import wtforms as wtf
from flask import render_template
from jembe import JembeInitParamSupport
from ..helpers import get_widget_variants, camel_to_snake
from ..settings import settings
from ..exceptions import JembeUIError

if TYPE_CHECKING:
    import jembeui
    import wtforms
    from flask_sqlalchemy import Model

__all__ = ("Form",)


class FormMeta(wtf.form.FormMeta, ABCMeta):
    pass


class Form(JembeInitParamSupport, wtf.Form, metaclass=FormMeta):
    """
    Form should be used together with CForm component and its variants
    CEdit, CCreate, CView to represent actual form.

    Form:
    - must be mounted by CForm component before being processed (displayed, etc).
    - renters itself inside CForm component template
    - CForm should call Form methods submit and cancel when user executes those
      actions on CForm
    """

    TEMPLATE_VARIANTS: dict
    TEMPLATE_VARIANTS_CACHE: dict
    DEFAULT_TEMPLATE: Union[str, List[str]]
    FIELD_TEMPLATES_CACHE: dict
    FIELD_TEMPLATES_VARIANTS_CACHE: dict

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
        self.cform: "jembeui.CForm"

        super().__init__(
            formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs
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

    def mount(self, cform: "jembeui.CForm") -> "jembeui.Form":
        """
        Mount is called by CFrom before form is displayed or before
        form needs aditional processing
        """
        self.cform = cform
        if "RENDER_KW" not in self.__class__.__dict__:
            self.__class__.RENDER_KW = dict()
            for field in self:
                self.RENDER_KW[field.name] = {}
                if field.render_kw:
                    self.RENDER_KW[field.name] = field.render_kw.copy()
                    field.render_kw = {
                        k: v
                        for k, v in field.render_kw.items()
                        if not k.endswith("+") and not k.startswith("_")
                    }
        return self

    def submit(self, record: Union["Model", dict]) -> Union["Model", dict]:
        # TODO
        if isinstance(record, dict):
            raise JembeUIError(
                "You must provide submit logic for form when record is dict by overriding 'submit' method"
            )
            # return record
        else:
            self.populate_obj(record)
            self.cform.session.add(record)
            return record

    def cancel(self, record: Union["Model", dict]):
        # TODO
        pass

    def set_disabled(self, *fields: "wtforms.Field"):
        for field in fields:
            self._field_setdefault(field, "disabled", True)

    def as_html(self, _variant_or_template_name: Optional[str] = None) -> str:
        template = self._jui_template(_variant_or_template_name)
        context = self.cform._get_default_template_context()
        return Markup(render_template(template, **context))

    def field_as_html(
        self,
        field: Union[str, "wtforms.Field"],
        _variant_or_template_name: Optional[str] = None,
        **render_kw
    ) -> str:
        template = self._jui_field_template(field, _variant_or_template_name)
        context = self.cform._get_default_template_context()
        if "form_field" in context:
            raise JembeUIError(
                "form_field var already exist in CForm context and "
                "Form.field_as_html can't be used"
            )
        form_field = getattr(self, field) if isinstance(field, str) else field
        context["form_field"] = form_field

        _render_kw = self.__join_kw(self.RENDER_KW[form_field.name], render_kw)
        if self.is_disabled:
            _render_kw["disabled"] = True

        context["raw_render_kw"] = _render_kw
        return Markup(render_template(template, **context))

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
                        elif isinstance(w, list):
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

    def resolve_kw(self, render_kw: dict, defaults_kw: Optional[dict] = None) -> dict:
        if defaults_kw:
            import pprint

            pprint.pprint(render_kw)
            pprint.pprint(defaults_kw)
            pprint.pprint(self.__join_kw(render_kw, defaults_kw, True))
            pprint.pprint(
                self.__resolve_kw(self.__join_kw(render_kw, defaults_kw, True))
            )
            print("---------------------------------")
            return self.__resolve_kw(self.__join_kw(render_kw, defaults_kw, True))
        else:
            return self.__resolve_kw(render_kw)

    def attr_kw(self, kw: dict) -> dict:
        return {
            k: v
            for k, v in kw.items()
            if not k.startswith("_") and not k.endswith("+") and isinstance(v, str)
        }

    def _jui_template(
        self, variant_or_template_name: Optional[str] = None
    ) -> Union[str, List[str]]:
        if "DEFAULT_TEMPLATE" not in self.__class__.__dict__:
            self.__class__.DEFAULT_TEMPLATE = [
                t.format(style=settings.default_style)
                for t in [
                    *self.__jui_my_default_template(),
                    self.__jui_get_template_variant(),
                ]
            ]
        if variant_or_template_name is None:
            return self.DEFAULT_TEMPLATE
        else:
            if "." in variant_or_template_name or "/" in variant_or_template_name:
                return variant_or_template_name.format(style=settings.default_style)
            if "TEMPLATE_VARIANTS_CACHE" not in self.__class__.__dict__:
                self.__class__.TEMPLATE_VARIANTS_CACHE = dict()
            try:
                return self.__class__.TEMPLATE_VARIANTS_CACHE[variant_or_template_name]
            except KeyError:
                pass
            self.__class__.TEMPLATE_VARIANTS_CACHE[variant_or_template_name] = [
                t.format(style=settings.default_style)
                for t in [
                    *self.__jui_my_default_template(variant_or_template_name),
                    self.__jui_get_template_variant(variant_or_template_name),
                    *self.__jui_my_default_template(),
                    self.__jui_get_template_variant(),
                ]
            ]
            return self.TEMPLATE_VARIANTS_CACHE[variant_or_template_name]

    def _jui_field_template(
        self,
        field: Union[str, "wtforms.Field"],
        variant_or_template_name: Optional[str] = None,
    ) -> Union[str, List[str]]:
        if variant_or_template_name and (
            "." in variant_or_template_name or "/" in variant_or_template_name
        ):
            return variant_or_template_name.format(style=settings.default_style)
        if "FIELD_TEMPLATES_CACHE" not in self.__class__.__dict__:
            self.__class__.FIELD_TEMPLATES_CACHE = dict()
        if "FIELD_TEMPLATES_VARIANTS_CACHE" not in self.__class__.__dict__:
            self.__class__.FIELD_TEMPLATES_VARIANTS_CACHE = dict()
        field_class_name = (
            getattr(self, field).__class__.__name__
            if isinstance(field, str)
            else field.__class__.__name__
        )
        try:
            if variant_or_template_name:
                return self.FIELD_TEMPLATES_VARIANTS_CACHE[field_class_name][
                    variant_or_template_name
                ]
            else:
                return self.FIELD_TEMPLATES_CACHE[field_class_name]
        except KeyError:
            pass
        if field_class_name not in self.FIELD_TEMPLATES_CACHE:
            self.__class__.FIELD_TEMPLATES_CACHE[field_class_name] = [
                *[
                    "{}/{}/{}.html".format(
                        d.strip("/"),
                        camel_to_snake(self.__class__.__name__),
                        camel_to_snake(field if isinstance(field, str) else field.name),
                    ).format(style=settings.default_style)
                    for d in settings.forms_template_dirs
                ],
                *[
                    t.format(style=settings.default_style)
                    for t in [
                        "/".join(
                            (
                                d.strip("/"),
                                "{}.html".format(camel_to_snake(field_class_name)),
                            )
                        )
                        for d in settings.form_fields_template_dirs
                    ]
                ],
                *[
                    t.format(style=settings.default_style)
                    for t in [
                        "/".join(
                            (
                                d.strip("/"),
                                "default.html",
                            )
                        )
                        for d in settings.form_fields_template_dirs
                    ]
                ],
            ]
        if field_class_name not in self.FIELD_TEMPLATES_VARIANTS_CACHE:
            self.__class__.FIELD_TEMPLATES_VARIANTS_CACHE[field_class_name] = dict()
        if (
            variant_or_template_name
            not in self.FIELD_TEMPLATES_VARIANTS_CACHE[field_class_name]
        ):
            self.__class__.FIELD_TEMPLATES_VARIANTS_CACHE[field_class_name][
                variant_or_template_name
            ] = [
                *[
                    t.format(style=settings.default_style)
                    for t in [
                        "/".join((d, "{}.html".format(variant_or_template_name)))
                        for d in settings.form_fields_template_dirs
                    ]
                ],
                *self.FIELD_TEMPLATES_CACHE[field_class_name],
            ]
        if variant_or_template_name:
            return self.FIELD_TEMPLATES_VARIANTS_CACHE[field_class_name][
                variant_or_template_name
            ]
        else:
            return self.FIELD_TEMPLATES_CACHE[field_class_name]

    @property
    def __jui_template_variants(self) -> Dict[str, str]:
        if "TEMPLATE_VARIANTS" in self.__class__.__dict__:
            return self.__class__.TEMPLATE_VARIANTS
        self.__class__.TEMPLATE_VARIANTS = get_widget_variants(
            settings.form_widgets_variants_dirs
        )
        return self.__class__.TEMPLATE_VARIANTS

    def __jui_get_template_variant(self, variant: str = "default") -> str:
        try:
            return self.__jui_template_variants[variant]
        except KeyError:
            raise JembeUIError(
                "Form variant '{}' does not exist! Valid variants are: {}".format(
                    variant, list(self.TEMPLATE_VARIANTS.keys())
                )
            )

    def __jui_my_default_template(self, variant: str = "") -> List[str]:
        return [
            "/".join(
                (
                    d.strip("/"),
                    "{name}{variant}.html".format(
                        name=camel_to_snake(self.__class__.__name__),
                        variant="__{}".format(variant) if variant else "",
                    ),
                )
            )
            for d in settings.forms_template_dirs
        ]

    def _field_setdefault(
        self, field: "wtforms.Field", param_name: str, value: Any
    ) -> Any:
        if field.render_kw is None:
            field.render_kw = dict()
        return field.render_kw.setdefault(param_name, value)
