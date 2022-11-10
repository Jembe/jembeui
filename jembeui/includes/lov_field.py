from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union
import sqlalchemy as sa
import wtforms as wtf
from flask_babel import lazy_gettext as _
from jembeui import JembeUIError
from .field import FieldMixin

if TYPE_CHECKING:
    import jembeui
    import jembe

__all__ = ("LovField",)


class LovField(FieldMixin, wtf.Field):
    """Field displaying selectable, editable, extendable List of Values

    Usefull for:

    - chosing from existing records when there are to many records for simple select;
    - when you need to search record to select by multiple columns
    - when you need to view record details before chosing it
    - when you need to add new record in place or modify existing ones
    """

    def __init__(
        self,
        label=None,
        validators=None,
        choices: Optional[
            Callable[
                ["jembeui.LovField", "jembeui.CForm", str],
                Union["sa.orm.Query", list],
            ]
        ] = None,
        get_choice_id: Callable[[Any], str] = lambda choice: str(
            getattr(choice, "id", choice[0])
        ),
        get_choice_title: Callable[[Any], str] = lambda choice: str(
            getattr(choice, "title", choice[1])
        ),
        choice_columns: Optional[Dict[str, Callable[[Any], Any]]] = None,
        no_records_found_message:str = _("No records found"),
        cview: Optional["jembe.ComponentRef"] = None,
        cupdate: Optional["jembe.ComponentRef"] = None,
        ccreate: Optional["jembe.ComponentRef"] = None,
        coerce=int,
        filters=(),
        description="",
        id=None,
        default=None,
        widget=None,
        render_kw=None,
        name=None,
        _form=None,
        _prefix="",
        _translations=None,
        _meta=None,
    ):
        super().__init__(
            label,
            validators,
            filters,
            description,
            id,
            default,
            widget,
            render_kw,
            name,
            _form,
            _prefix,
            _translations,
            _meta,
        )
        self._coerce = coerce

        if choices is None:
            raise JembeUIError(
                "LovField must have choices defined with"
                " Callable[['LovField', 'jembeui.CForm', str], Union['sa.orm.Query', list]] "
            )
        self._choices: Callable[
            ["LovField", "jembeui.CForm", str],
            Union["sa.orm.Query", list],
        ] = choices

        self._no_records_found_message = no_records_found_message

        self._get_choice_id = get_choice_id
        self._get_choice_title = get_choice_title

        if choice_columns is None:
            choice_columns = {
                "title": lambda choice: getattr(choice, "title", choice[1])
            }
        self._choice_columns = choice_columns

        self._cview = cview
        self._cupdate = cupdate
        self._ccreate = ccreate

    @property
    def choices(self):
        return [
            self._get_choice_id(choice) for choice in self._choices(self, self.form, "")
        ]

    def process_data(self, value):
        if value is None:
            self.data = None
        else:
            try:
                self.data = self._coerce(value)
            except (ValueError, TypeError):
                self.data = None

    def process_formdata(self, valuelist):
        try:
            if valuelist:
                self.data = self._coerce(valuelist[0])
            else:
                self.data = None
        except ValueError:
            raise ValueError(
                self.gettext("Invalid choice(s): data input could not be coerced")
            )

    def pre_validate(self, form):
        if self.data:
            valid_choices = {
                self._get_choice_id(choice) for choice in self._choices(self, form, "")
            }
            if str(self.data) not in valid_choices:
                raise ValueError(
                    self.gettext("Invalid value '{}' selected").format(self.data)
                )

    def get_jembeui_components(self) -> Dict[str, "jembe.ComponentRef"]:
        from jembeui.components.fields import CLovField

        return {
            "lov": (
                CLovField,
                CLovField.Config(
                    title=str(self.label),
                    field_name=self.short_name,
                    choices=self._choices,
                    get_choice_id=self._get_choice_id,
                    get_choice_title=self._get_choice_title,
                    choice_columns=self._choice_columns,
                    coerce=self._coerce,
                    no_records_found_message=self._no_records_found_message,
                    cview=self._cview,
                    cupdate=self._cupdate,
                    ccreate=self._ccreate,
                ),
            )
        }
