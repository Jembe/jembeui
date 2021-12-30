from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Sequence,
    Union,
    Callable,
    Iterable,
    Dict,
    Tuple,
    Any,
)
from collections import namedtuple
from datetime import date, datetime, time, timedelta
from functools import partial, cached_property
from math import ceil
from flask_babel import format_date, format_datetime, format_time, format_timedelta
from jembe import action
from .component import Component
from .menu import Menu
from jembeui.helpers import get_jembeui
from jembeui.settings import settings
from jembeui.exceptions import JembeUIError
import sqlalchemy as sa

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CListRecords",)


def default_field_value(component: "jembe.Component", record, field_name: str) -> str:
    fnames = field_name.split("__")
    value = record[fnames.pop(0)]
    while len(fnames) > 0:
        value = getattr(value, fnames.pop(0))
    if isinstance(value, datetime):
        return format_datetime(value)
    elif isinstance(value, date):
        return format_date(value)
    elif isinstance(value, time):
        return format_time(value)
    elif isinstance(value, timedelta):
        return format_timedelta(value)
    elif isinstance(value, bool):
        return str(value)  # TODO
    else:
        return str(value) if value is not None else ""  # type: ignore


def default_field_order_by(
    query: "sa.orm.Query", field_name: str, desc: bool
) -> "sa.orm.Query":
    if desc:
        return query.order_by(None).order_by(
            sa.desc(field_name.replace("__", ".")), *query._order_by_clauses
        )
    return query.order_by(None).order_by(
        field_name.replace("__", "."), *query._order_by_clauses
    )


class CListRecords(Component):
    class ChoiceFilter:
        ListChoiceType = namedtuple("ListChoiceType", ["title", "value_str", "value"])

        def __init__(
            self,
            expr: Callable[["sa.orm.Query", Iterable[Any]], "sa.orm.Query"],
            *choices: Union[Tuple[str, str], Tuple[str, str, Any]],
            grouped: bool = False,
            dynamic_choices: Optional[
                Callable[
                    ["jembe.Component"],
                    Iterable[Union[Tuple[str, str], Tuple[str, str, Any]]],
                ]
            ] = None
        ):
            """
            expr - python function that accepts query and list of values and
                   returns new query with applied filter based on the choices in values
            choices - list of tuples with choice title and choice value
                      that user can select to filter list records
            """
            self.expr = expr
            self.choices: List[Tuple[str, str, Any]] = [
                self.ListChoiceType(
                    c[0], c[1], c[2] if len(c) == 3 else c[1]  # type:ignore
                )
                for c in choices
            ]
            self.str_values: List[str]
            self._dynamic_choices = dynamic_choices
            self._check_for_duplicate_choices()
            self.is_grouped = grouped

        def map_values(self, str_values: Iterable[str]) -> Iterable[Any]:
            mapping = {c[1]: c[2] for c in self.choices}
            return tuple(mapping[v] for v in str_values if v in mapping.keys())

        def _check_for_duplicate_choices(self):
            # check for duplicates
            self.str_values = [c[1] for c in self.choices]
            values = [c[2] for c in self.choices]
            if len(self.str_values) != len(set(self.str_values)) or len(values) != len(
                set(values)
            ):
                raise JembeUIError(
                    "ListRecords.ChoiceFilter can't have duplicate values: {}".format(
                        values
                    )
                )

        def mount(
            self, component: "jembe.Component"
        ) -> "jembeui.CListRecords.ChoiceFilter":
            if self._dynamic_choices:
                cfcopy = CListRecords.ChoiceFilter(
                    self.expr, *self.choices, grouped=self.is_grouped
                )
                cfcopy.choices.extend(
                    self.ListChoiceType(
                        c[0], c[1], c[2] if len(c) == 3 else c[1]  # type:ignore
                    )
                    for c in self._dynamic_choices(component)  # type:ignore
                )
                cfcopy._check_for_duplicate_choices()
                return cfcopy
            return self

    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/list_records.html"
        default_field_value = default_field_value
        default_field_order_by = default_field_order_by

        def __init__(
            self,
            query: Union[
                "sa.orm.Query", Callable[["jembeui.CListRecords"], "sa.orm.Query"]
            ],
            fields: Optional[Dict[str, str]] = None,
            field_values: Optional[
                Dict[str, Callable[["jembeui.Component", Any, str], str]]
            ] = None,
            field_order_by: Optional[
                Dict[str, Callable[["sa.orm.Query", str, bool], "sa.orm.Query"]]
            ] = None,
            fields_styling: Optional[Dict[str, dict]] = None,
            search_filter: Optional[
                Callable[["sa.orm.Query", str], "sa.orm.Query"]
            ] = None,
            choice_filters: Iterable["jembeui.CListRecords.ChoiceFilter"] = (),
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            record_menu: Optional[
                Callable[
                    ["Component", Any],
                    Union[
                        "jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]
                    ],
                ]
            ] = None,
            page_size: int = 0,
            db: Optional["SQLAlchemy"] = None,
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            """
            query - sqlachemy query created with sa.Query
            fields - fields/columns to be displayed inside list/table.
                    key is access param name for record where '__' will be replaced with '.'
                    value is field title
            """

            self.query = query
            # defult db can be useds when db is None
            if db is not None:
                self.db = db
            else:
                self.db = get_jembeui().default_db
                if self.db is None:
                    raise JembeUIError(
                        "Either 'db' for CListRecords.Config or default_db"
                        " on JembeUI instance must be set"
                    )
            # page size
            self.page_size = (
                page_size if page_size > 0 else settings.list_records_page_size
            )
            # field names
            if isinstance(self.query, sa.orm.Query):
                self.fields = (
                    fields
                    if fields is not None
                    else {
                        ca["name"]: ca["name"].replace("_", " ")
                        for ca in self.query.column_descriptions
                    }
                )
            else:
                self.fields = fields if fields is not None else {}
            # field values
            self.field_values = (
                field_values
                if field_values is not None
                else {
                    field_name: self.__class__.default_field_value
                    for field_name in self.fields.keys()
                }
            )
            for field_name in self.fields.keys():
                if field_name not in self.field_values:
                    self.field_values[field_name] = self.__class__.default_field_value
            # field order by
            self.field_order_by = (
                field_order_by if field_order_by is not None else dict()
            )
            for field_name in self.fields.keys():
                if field_name not in self.field_order_by:
                    self.field_order_by[
                        field_name
                    ] = self.__class__.default_field_order_by

            # field stylings
            self.fields_styling = dict()
            fields_styling = fields_styling if fields_styling is not None else dict()
            for field_name in self.fields.keys():
                self.fields_styling[field_name] = fields_styling.get(field_name, dict())

            # search filter
            self.search_filter = search_filter

            # choice filters
            self.choice_filters = {
                "cf{}".format(index): cf for index, cf in enumerate(choice_filters)
            }
            # menu
            self.menu: "Menu" = (
                Menu()
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            # record menu
            self.record_menu = record_menu

            # query params
            if url_query_params is None:
                url_query_params = dict()
            if "page" not in url_query_params.values():
                url_query_params["p"] = "page"
            if "page_size" not in url_query_params.values():
                url_query_params["ps"] = "page_size"
            if "search" not in url_query_params.values():
                url_query_params["s"] = "search"
            if "choice_filters" not in url_query_params.values():
                url_query_params["cf"] = "choice_filters"
            if "order_by" not in url_query_params.values():
                url_query_params["ob"] = "order_by"

            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: "Config"

    def __init__(
        self,
        page: int = 0,
        page_size: int = 0,
        search: str = "",
        choice_filters: Optional[Dict[str, List[str]]] = None,
        order_by: Optional[str] = None,
    ):
        if page_size < 1:
            self.state.page_size = self._config.page_size
        super().__init__()

    @property
    def session(self) -> "sa.orm.scoping.scoped_session":
        return self._config.db.session

    @action
    def jui_apply_choice_filter(self, filter_name, filter_value):
        if (
            filter_name not in self.choice_filters_config
            or filter_value not in self.choice_filters_config[filter_name].str_values
        ):
            return
        if self.state.choice_filters is None:
            self.state.choice_filters = dict()

        if filter_name not in self.state.choice_filters:
            self.state.choice_filters[filter_name] = [filter_value]
        else:
            self.state.choice_filters[filter_name].append(filter_value)

        self.state.page = 0

    @action
    def jui_remove_choice_filter(self, filter_name, filter_value):
        if (
            filter_name not in self.choice_filters_config
            or filter_value not in self.choice_filters_config[filter_name].str_values
        ):
            return
        if filter_name not in self.state.choice_filters:
            return
        if filter_value not in self.state.choice_filters[filter_name]:
            return

        self.state.choice_filters[filter_name].remove(filter_value)
        if len(self.state.choice_filters[filter_name]) == 0:
            del self.state.choice_filters[filter_name]

        if len(self.state.choice_filters) == 0:
            self.state.choice_filters = None

        self.state.page = 0

    @cached_property
    def choice_filters_config(self):
        return {
            name: cf.mount(self) for name, cf in self._config.choice_filters.items()
        }

    def hydrate(self):
        query = (
            self._config.query
            if isinstance(self._config.query, sa.orm.Query)
            else self._config.query(self)
        )
        self.records = query.with_session(self.session()).only_return_tuples(
            True
        )

        # apply search filter
        if self._config.search_filter is not None and self.state.search:
            self.records = self._config.search_filter(self.records, self.state.search)

        # apply choice filters (and clean input)
        cleaned_choice_filters = dict()
        if self.state.choice_filters is not None:
            for name in self.state.choice_filters.keys():
                if name in self.choice_filters_config.keys():
                    cf = self.choice_filters_config[name]
                    str_value = self.state.choice_filters[name]
                    self.records = cf.expr(self.records, cf.map_values(str_value))
                    try:
                        cleaned_choice_filters[name].append(str_value)
                        cleaned_choice_filters[name] = list(
                            set(cleaned_choice_filters[name])
                        )
                    except KeyError:
                        cleaned_choice_filters[name] = list(str_value)
        if len(cleaned_choice_filters) == 0:
            self.state.choice_filters = None
        else:
            self.state.choice_filters = cleaned_choice_filters

        # apply order by
        if self.state.order_by:
            fname = self.state.order_by.strip("-")
            is_desc = self.state.order_by.startswith("-")
            if fname in self._config.fields.keys():
                self.records = self._config.field_order_by[fname](
                    self.records, fname, is_desc
                )

        # apply pagination
        self.total_records = self.records.count()
        self.total_pages = ceil(self.total_records / self.state.page_size)
        if self.state.page > self.total_pages - 1:
            self.state.page = self.total_pages - 1
        if self.state.page < 0:
            self.state.page = 0
        self.start_record_index = self.state.page * self.state.page_size
        self.end_record_index = self.start_record_index + self.state.page_size
        if self.end_record_index > self.total_records:
            self.end_record_index = self.total_records
        self.records = self.records[self.start_record_index : self.end_record_index]

        # initialise field renderes
        self.field_values = {
            field_name: partial(field_value, self)
            for field_name, field_value in self._config.field_values.items()
        }

        # menu
        self.menu = self._config.menu.bind_to(self)

        # record menu
        self.get_record_menu = self._get_record_menu

    def _get_record_menu(self, record) -> "jembeui.Menu":
        if self._config.record_menu is None:
            raise JembeUIError()
        raw_menu = self._config.record_menu(self, record)
        menu = raw_menu if isinstance(raw_menu, Menu) else Menu(raw_menu)
        return menu.bind_to(self)
