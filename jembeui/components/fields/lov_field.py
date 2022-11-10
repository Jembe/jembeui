from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple, Union, Any
import sqlalchemy as sa
from jembe import listener
from jembeui import Component, JembeUIError

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CLovField",)


class CLovField(Component):
    """Component that actualy displayes and handles all logic for List of Values form field"""

    class Config(Component.Config):
        def __init__(
            self,
            field_name: str,
            choices: Callable[
                ["jembeui.LovField", "jembeui.CForm", str],
                Union["sa.orm.Query", list],
            ],
            get_choice_id: Callable[[Any], str],
            get_choice_title: Callable[[str], str],
            choice_columns: Dict[str, Callable[[Any], Any]],
            no_records_found_message: str,
            coerce=int,
            cview: Optional["jembe.ComponentRef"] = None,
            cupdate: Optional["jembe.ComponentRef"] = None,
            ccreate: Optional["jembe.ComponentRef"] = None,
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
        ):
            self.field_name = field_name
            self.choices = choices
            self.get_choice_id = get_choice_id
            self.get_choice_title = get_choice_title
            self.choice_columns = choice_columns

            self.coerce = coerce

            self.no_records_found_message = no_records_found_message

            components = {}
            if cview:
                components["view"] = cview
            if cupdate:
                components["update"] = cupdate
            if ccreate:
                components["create"] = ccreate

            super().__init__(
                title=title,
                components=components,
                template="jembeui/components/fields/lov_field.html",
                changes_url=False,
            )

    _config: Config

    def __init__(
        self,
        selected: Optional[str] = None,
        search: Optional[str] = None,
        is_disabled: bool = False,
        _form: Optional["jembeui.Form"] = None,
    ):
        if _form is None:
            raise JembeUIError("CLovField must have _form parameter injected")
        self._form = _form

        super().__init__()

    @property
    def form(self) -> "jembeui.Form":
        return self._form

    @property
    def cform(self) -> "jembeui.CForm":
        return self._form.cform

    @property
    def field(self) -> "jembeui.LovField":
        return getattr(self._form, self._config.field_name)

    @property
    def field_style(self) -> "jembeui.Form.FieldStyle":
        return self._form.get_form_style().field_style(self._config.field_name)

    @property
    def input_placeholder(self) -> Optional[str]:
        return (
            None
            if not self.field.render_kw
            else self.field.render_kw.get("placeholder", None)
        )

    @property
    def selected_title(self) -> Optional[str]:
        """Returns title of selected record"""
        if self.state.selected is None:
            return None
        return self._config.get_choice_title(
            self._get_choice_by_id(self.state.selected)
        )

    @property
    def is_open(self) -> bool:
        return self.state.search is not None

    @property
    def has_create(self) -> bool:
        return "create" in self._config.components

    @property
    def has_view(self) -> bool:
        return "view" in self._config.components

    @property
    def has_update(self) -> bool:
        return "update" in self._config.components

    @property
    def choices(self) -> List[Tuple[str, list]]:
        if self.state.search is None:
            return []

        result = []
        for c in self._config.choices(self.field, self.cform, self.state.search):
            result.append(
                (
                    self._config.get_choice_id(c),
                    [
                        transform(c)
                        for _, transform in self._config.choice_columns.items()
                    ],
                )
            )
        return result

    def _get_choice_by_id(self, choice_id: str) -> Any:
        """Returns selected choice by its id"""
        cid = self._config.coerce(choice_id)

        choices_result = self._config.choices(self.field, self.cform, "")
        if isinstance(choices_result, sa.orm.Query):
            return choices_result.filter(
                self._get_query_id_column(choices_result) == cid
            ).one()
        else:
            return next(
                choice
                for choice in choices_result
                if self._config.get_choice_id(choice) == choice_id
            )

    def _get_query_id_column(self, query: "sa.orm.Query"):
        id_column = next(
            (cd["expr"] for cd in query.column_descriptions if cd["name"] == "id"),
            None,
        )
        if id_column is None:
            id_column = query.column_descriptions[0]["expr"]
        return id_column
    
    @listener(event="cancel", source=("view", "update", "create"))
    def on_child_cancel(self, event: "jembe.Event"):
        self.remove_component(event.source_name)

    @listener(event="submit", source=("update", "create"))
    def on_child_submit(self, event: "jembe.Event"):
        if event.source_name == "update":
            if not event.source._config.redisplay_on_submit:
                self.remove_component(event.source_name)
        elif event.source_name == "create":
            self.remove_component(event.source_name)
            self.state.selected = str(event.source.record.id)
            self.emit(
                "update_form_field",
                name=self._config.field_name,
                value=self.state.selected,
            ).to("..")
        return True

    @listener(event="_display", source=("view", "update", "create"))
    def on_display_subcomponent(self, event: "jembe.Event"):
        self.state.search = None
        for cname in ("view", "update", "create"):
            if cname != event.source_name and cname in self._config.components:
                self.remove_component(cname)
