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
    TEMPLATE: Union[str, Iterable[str]]

    def __init__(
        self,
        formdata=None,
        obj=None,
        prefix="",
        data=None,
        meta=None,
        readonly: bool = False,
        template: Optional[str] = None,
        **kwargs
    ):
        self.is_readonly = readonly
        self._readonly_fields: List["Field"] = []
        self.cform: "CForm"

        self.template = (
            template
            if template
            else self.default_template_exp.format(style=settings.default_style)
        )
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

    def submit(self, record: Union["Model",dict]) -> Union["Model",dict]:
        # TODO
        if isinstance(record,dict):
            raise NotImplementedError()
            # return record
        else:
            self.populate_obj(record)
            self.cform.session.add(record)
            return record

    def cancel(self, record: Union["Model",dict]):
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

    @property
    def _jui_template_variants(self) -> Dict[str, str]:
        try:
            return self.__class__.TEMPLATE_VARIANTS
        except AttributeError:
            self.__class__.TEMPLATE_VARIANTS = get_widget_variants(
                settings.form_widgets_variants_dirs
            )
        return self.__class__.TEMPLATE_VARIANTS

    def as_html(self, variant: Optional[str] = None) -> str:
        if not hasattr(self, "cform"):
            raise JembeUIError("Form must be mounted in order to be rendered as html")
        template = self._jui_get_template(variant)
        context = {"form": self}
        return Markup(render_template(template, **context))

    def _jui_get_template(
        self, variant_or_template_name: Optional[str] = None
    ) -> Union[str, List[str]]:
        if "TEMPLATE" not in self.__class__.__dict__:
            self.__class__.TEMPLATE = [
                self._jui_my_default_template(),
                self._jui_get_template_variant(),
            ]
        if variant_or_template_name is None:
            return [t.format(style=settings.default_style) for t in self.TEMPLATE]
        else:
            if "." in variant_or_template_name or "/" in variant_or_template_name:
                return variant_or_template_name.format(style=settings.default_style)
            else:
                return [
                    t.format(style=settings.default_style)
                    for t in [
                        self._jui_my_default_template(variant_or_template_name),
                        self._jui_get_template_variant(variant_or_template_name),
                        self._jui_my_default_template(),
                        self._jui_get_template_variant(),
                    ]
                ]

    def _jui_get_template_variant(self, variant: str = "default") -> str:
        try:
            return self._jui_template_variants[variant]
        except KeyError:
            raise JembeUIError(
                "Form variant '{}' does not exist! Valid variants are :{}".format(
                    variant, self.template_variants.keys()
                )
            )

    def _jui_my_default_template(self, variant: str = "") -> str:
        return "/".join(
            [
                settings.forms_template_dir.strip("/"),
                "{name}{variant}.html".format(
                    name=camel_to_snake(self.__class__.name),
                    variant="__{}".format(variant) if variant else "",
                ),
            ]
        )
