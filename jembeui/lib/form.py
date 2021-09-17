from typing import TYPE_CHECKING, Any, Dict, Optional
from abc import ABCMeta
from markupsafe import Markup
from wtforms.form import Form, FormMeta
from flask import render_template
from jembe import JembeInitParamSupport
from ..helpers import get_widget_variants
from ..settings import settings
from ..exceptions import JembeUIError

if TYPE_CHECKING:
    from ..components import CForm
    from wtforms import Field
    from flask_sqlalchemy import Model

__all__ = ("JembeForm",)


class JembeFormMeta(FormMeta, ABCMeta):
    pass


class JembeForm(JembeInitParamSupport, Form, metaclass=JembeFormMeta):
    """
    JembeForm should be used together with CForm component and its variants
    CEdit, CCreate, CView to represent actual form.

    JembeForm:
    - must be mounted by CForm component before being processed (displayed, etc).
    - renters itself inside CForm component template
    - CForm should call JembeForm methods submit and cancel when user executes those
      actions on CForm
    """

    TEMPLATE_VARIANTS: dict

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

    def mount(self, cform: "CForm") -> "JembeForm":
        """
        Mount is called by CFrom before form is displayed or before
        form needs aditional processing
        """
        self.cform = cform
        return self

    def submit(self, record: Optional["Model"] = None) -> Optional["Model"]:
        # TODO
        if record is not None:
            self.populate_obj(record)
            self.cform.session.add(record)
            return record
        return None

    def cancel(self, record: Optional["Model"] = None):
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

    def set_readonly_all(self):
        self.set_readonly(*[field for field in self])

    @property
    def template_variants(self) -> Dict[str, str]:
        try:
            return self.__class__.TEMPLATE_VARIANTS
        except AttributeError:
            self.__class__.TEMPLATE_VARIANTS = get_widget_variants(
                settings.form_widgets_variants_dirs
            )
        return self.__class__.TEMPLATE_VARIANTS

    def as_html(self, variant: str = "default") -> str:
        if not hasattr(self,"cform"):
            raise JembeUIError(
                "Form must be mounted in order to be rendered as html"
            )
        if "/" in variant or "." in variant:
            # variant is template name
            template = variant
        else:
            if variant not in self.template_variants.keys():
                raise JembeUIError(
                    "Form variant '{}' does not exist! Valid variants are :{}".format(
                        variant, self.template_variants.keys()
                    )
                )
            template = self.template_variants[variant]
        context = {"form": self}
        return Markup(render_template(template, **context))