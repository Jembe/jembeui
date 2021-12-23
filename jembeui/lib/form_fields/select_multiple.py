from typing import TYPE_CHECKING, Union, Callable, List, Tuple, Dict, Optional

from jembeui.exceptions import JembeUIError
from .jui_field import JUIFieldMixin
import wtforms
from sqlalchemy.orm import Query


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

    widget = wtforms.widgets.HiddenInput

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
        view_component: Optional["jembe.ComponentReference"] = None,
        update_component: Optional["jembe.ComponentReference"] = None,
        create_component: Optional["jembe.ComponentReference"] = None,
        display_update_link: bool = True,
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
        self.view_component = view_component
        self.update_component = update_component
        self.create_component = create_component
        self.display_update_link = display_update_link

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

    def _get_all_choices_result(self) -> Union["sa.orm.Query", list]:
        temp_data = self.data
        self.data = None
        result = self.choices(self, self.cform, "")
        self.data = temp_data

        if isinstance(result, Query):
            result = result.limit(None)
        return result

    def _get_ids(self, choices_result: Union["sa.orm.Query", list]) -> list:
        return [
            self.coerce(getattr(choice, "id", choice[0])) for choice in choices_result
        ]

    def _get_id_column(self, query: "sa.orm.Query"):
        id_column = next(
            (cd["expr"] for cd in query.column_descriptions if cd["name"] == "id"),
            None,
        )
        if id_column is None:
            id_column = query.column_descriptions[0]["expr"]
        return id_column

    def _get_selected_choices(
        self, selected_ids: Optional[tuple] = None
    ) -> List[Tuple[str, str]]:
        """
        Returns list of (id, title) of choices that are selected.

        it will get all choices and filter it by its id
        """
        data = (
            [self.coerce(id) for id in selected_ids]
            if selected_ids is not None
            else self.data
        )
        if not data:
            return []

        all_choices_result = self._get_all_choices_result()
        if isinstance(all_choices_result, Query):
            return [
                (
                    self.coerce(getattr(choice, "id", choice[0])),
                    getattr(choice, "title", choice[1]),
                )
                for choice in all_choices_result.filter(
                    self._get_id_column(all_choices_result).in_(data)
                )
            ]
        else:
            return [
                (
                    self.coerce(getattr(choice, "id", choice[0])),
                    getattr(choice, "title", choice[1]),
                )
                for choice in all_choices_result
            ]

    def _get_choices(self, search: str, selected_ids: tuple) -> List[tuple]:
        temp_data = self.data
        self.data = [self.coerce(id) for id in selected_ids]
        choices = []
        for choice in self.choices(self, self.cform, search):
            choices.append(
                (
                    self.coerce(getattr(choice, "id", choice[0])),
                    getattr(choice, "title", choice[1]),
                )
            )
        self.data = temp_data
        return choices  # type:ignore

    def pre_validate(self, form):
        if self.data:
            choices_result = self._get_all_choices_result()
            if isinstance(choices_result, list):
                ids = self._get_ids(choices_result)
                for d in self.data:
                    if d not in ids:
                        raise ValueError(self.gettext("Invalid values selected"))
            else:
                if choices_result.filter(
                    self._get_id_column(choices_result).in_(self.data)
                ).count() != len(self.data):
                    raise ValueError(self.gettext("Invalid values selected"))

    def jui_get_components(self) -> Dict[str, "jembe.ComponentRef"]:
        from ...components.form_fields import CSelectMultipleSearch

        return {
            self.jui_component_name("search"): (
                CSelectMultipleSearch,
                CSelectMultipleSearch.Config(
                    field_name=self.short_name,
                    view_component=self.view_component,
                    update_component=self.update_component,
                    create_component=self.create_component,
                    display_update_link=self.display_update_link,
                    changes_url=False,
                ),
            )
        }
