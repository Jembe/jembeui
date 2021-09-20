from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, List, Union
from abc import ABCMeta
from markupsafe import Markup
import wtforms as wtf
from flask import render_template
from jembe import JembeInitParamSupport
from ..helpers import get_widget_variants, camel_to_snake
from ..settings import settings
from ..exceptions import JembeUIError

if TYPE_CHECKING:
    from ..components import CForm
    from wtforms import Field
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

    def __init__(
        self,
        formdata=None,
        obj=None,
        prefix="",
        data=None,
        meta=None,
        readonly: bool = False,
        **kwargs
    ):
        self.is_readonly = readonly
        self._readonly_fields: List["Field"] = []
        self.cform: "CForm"

        super().__init__(
            formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs
        )

    @classmethod
    def dump_init_param(cls, value: Any) -> Any:
        return (
            {
                k: v.dump_init_param(v) if isinstance(v, JembeInitParamSupport) else v
                for k, v in value.data.items()
            }
            if value is not None
            else dict()
        )

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return cls(data=value)

    def mount(self, cform: "CForm") -> "Form":
        """
        Mount is called by CFrom before form is displayed or before
        form needs aditional processing
        """
        self.cform = cform
        if self.is_readonly:
            self.set_readonly_all()
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

    def _field_setdefault(self, field: "Field", param_name: str, value: Any) -> Any:
        if field.render_kw is None:
            field.render_kw = dict()
        return field.render_kw.setdefault(param_name, value)

    def set_readonly(self, *fields: "Field"):
        for field in fields:
            self._field_setdefault(field, "disabled", True)
            self._field_setdefault(field, "readonly", True)
            self._readonly_fields.append(field)

    def set_readonly_all(self):
        self.set_readonly(*[field for field in self])

    def as_html(self, variant_or_template_name: Optional[str] = None) -> str:
        template = self._jui_template(variant_or_template_name)
        context = self.cform._get_default_template_context()
        return Markup(render_template(template, **context))

    def field_as_html(
        self,
        field: Union[str, "wtf.Field"],
        variant_or_template_name: Optional[str] = None,
    ) -> str:
        template = self._jui_field_template(field, variant_or_template_name)
        context = self.cform._get_default_template_context()
        if "form_field" in context:
            raise JembeUIError(
                "form_field var already exist in CForm context and "
                "Form.field_as_html can't be used"
            )
        context["form_field"] = (
            getattr(self, field) if isinstance(field, str) else field
        )
        return Markup(render_template(template, **context))

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
        field: Union[str, "wtf.Field"],
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
        tdirs = ["widgets/form_fields/", *settings.form_fields_template_dirs]
        if field_class_name not in self.FIELD_TEMPLATES_CACHE:
            self.__class__.FIELD_TEMPLATES_CACHE[field_class_name] = [
                *[
                    "{}/{}/{}.html".format(
                        d,
                        camel_to_snake(self.__class__.name),
                        camel_to_snake(field_class_name),
                    )
                    for d in settings.forms_template_dirs
                ],
                *[
                    t.format(style=settings.default_style)
                    for t in [
                        "/".join(
                            [d, "{}.html".format(camel_to_snake(field_class_name))]
                        )
                        for d in [
                            "widgets/form_fields/",
                            *settings.form_fields_template_dirs,
                        ]
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
                        "/".join([d, "{}.html".format(variant_or_template_name)])
                        for d in tdirs
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
                "Form variant '{}' does not exist! Valid variants are :{}".format(
                    variant, self.template_variants.keys()
                )
            )

    def __jui_my_default_template(self, variant: str = "") -> List[str]:
        return [
            "/".join(
                [
                    d.strip("/"),
                    "{name}{variant}.html".format(
                        name=camel_to_snake(self.__class__.__name__),
                        variant="__{}".format(variant) if variant else "",
                    ),
                ]
            )
            for d in settings.forms_template_dirs
        ]
