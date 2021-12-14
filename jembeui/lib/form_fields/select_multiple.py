from typing import TYPE_CHECKING, Union, Callable, List, Tuple, Dict, Optional

from jembeui.exceptions import JembeUIError
from .jui_field import JUIFieldMixin
import wtforms


if TYPE_CHECKING:
    import jembe
    import jembeui
    import sqlalchemy as sa


__all__ = ("SelectMultipleField",)


class SelectMultipleField(JUIFieldMixin, wtforms.Field):
    """
    Field used to select multiple values that supports:
    - Searching from list
    - Display list of values as table
    - Viewing selected values
    - Updateing selected values
    - Creating new values in list

    List of values is displayed and searched within jembe component that
    is integrated in this field.
    Viewing, Updating and Creating values are supported by association
    of respectiv CViewRecord, CUpdateRecord and CCreateRecord jembe UI components
    """

    def __init__(
        self,
        label=None,
        validators=None,
        choices: Union[
            None,
            Callable[
                ["jembeui.SelectMultipleField", "jembeui.CForm", str],
                Union["sa.orm.Query", list],
            ],
        ] = None,
        selected_choices: Union[
            None,
            Callable[
                ["jembeui.SelectMultipleField", "jembeui.CForm", list],
                Union["sa.orm.Query", list],
            ],
        ] = None,
        coerce=int,
        filters=tuple(),
        description="",
        id=None,
        default=None,
        widget=None,
        render_kw=None,
        _form=None,
        _name=None,
        _prefix="",
        _translations=None,
        _meta=None,
    ):
        super().__init__(
            label=label,
            validators=validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget,
            render_kw=render_kw,
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            _translations=_translations,
            _meta=_meta,
        )
        self.coerce = coerce
        if choices is None:
            raise JembeUIError(
                "SelectMultipleField must have choices defined with"
                " Callable[['SelectMultipleField', 'jembeui.CForm', str], Union['sa.orm.Query', list]] "
            )
        self.choices: Callable[
            ["SelectMultipleField", "jembeui.CForm", str],
            Union["sa.orm.Query", list],
        ] = choices
        self.selected_choices = selected_choices

    def process_data(self, value):
        try:
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        try:
            self.data = list(self.coerce(x) for x in valuelist)
        except ValueError:
            raise ValueError(
                self.gettext(
                    "Invalid choice(s): one or more data inputs could not be coerced"
                )
            )

    def _all_choices_ids(self) -> list:
        temp_data = self.data
        self.data = None
        ids = []
        for choice in self.choices(self, self.cform, ""):
            ids.append(self.coerce(getattr(choice, "id", choice[0])))
        self.data = temp_data
        return ids

    def _all_choices(self) -> list:
        temp_data = self.data
        self.data = None
        choices = []
        for choice in self.choices(self, self.cform, ""):
            choices.append(
                (
                    self.coerce(getattr(choice, "id", choice[0])),
                    getattr(choice, "title", choice[1]),
                )
            )
        self.data = temp_data
        return choices

    def _get_selected_choices(
        self, selected_ids: Optional[list] = None
    ) -> List[Tuple[str, str]]:
        """
        Returns list of (id, title) of choices that are selected.

        if selected_choices function is provided it will use it otherwise
        it will get all choices and filter it by its id
        """
        data = selected_ids if selected_ids is not None else self.data
        if not data:
            return []
        if self.selected_choices:
            return [
                (getattr(choice, "id", choice[0]), getattr(choice, "title", choice[1]))
                for choice in self.selected_choices(self, self.cform, data)
            ]
        temp_data = self.data
        self.data = None
        select_choices = [
            (
                self.coerce(getattr(choice, "id", choice[0])),
                getattr(choice, "title", choice[1]),
            )
            for choice in self.choices(self, self.cform, "")
            if getattr(choice, "id", choice[0]) in data
        ]
        self.data = temp_data
        return select_choices

    def pre_validate(self, form):
        if self.data:
            values = self._all_choices_ids()
            for d in self.data:
                if d not in values:
                    raise ValueError(
                        self.gettext("'%(value)s' is not a valid choice for this field")
                        % dict(value=d)
                    )

    def jui_get_components(self) -> Dict[str, "jembe.ComponentRef"]:
        from ...components.form_fields import CSelectMultipleSearch

        return {
            self.jui_component_name("search"): (
                CSelectMultipleSearch,
                CSelectMultipleSearch.Config(
                    field_name=self.short_name, changes_url=False
                ),
            )
        }
