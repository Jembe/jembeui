from collections import namedtuple
from functools import cached_property
from math import ceil
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import sqlalchemy as sa
from jembe import action
from jembeui.includes.menu import Menu
from jembeui.helpers import get_jembeui
from jembeui.exceptions import JembeUIError
from jembeui.settings import settings
from ..component import Component

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CList",)


def default_order_by(
    query: "sa.orm.Query", column_name: str, desc: bool
) -> "sa.orm.Query":
    """Default logic that alters SqlAlchemy query in order to apply ordering used by CList"""
    if desc:
        return query.order_by(None).order_by(
            sa.desc(column_name.replace("__", ".")), *query._order_by_clauses
        )
    return query.order_by(None).order_by(
        column_name.replace("__", "."), *query._order_by_clauses
    )


class CList(Component):
    """Display paginable, orderable, searchable and filterable list from SQLAlchemy query.

    HTML for displaying records in the list must be provided by user in "content" block.
    Default templates for pagination, search and filtering are provided in "toolbar" block;
    """

    class Config(Component.Config):
        """Allow configuring of

        - query <sa.orm.Query>: for quering records
        - order_by: map order name to order title
        - order_by_exp: maps order name to callable that alerts sa.orm.Query
        - search_filter: callable that alters sa.orm.Query on search input
        - choice_filters: list of choice filtes to used
        - page_size: number of records displayed per page
        - menu <jembeui.Menu>: to be displayed with table"""

        default_template: str = "/jembeui/components/list/list.html"
        default_order_by = default_order_by

        def __init__(
            self,
            query: Union["sa.orm.Query", Callable[["jembeui.CList"], "sa.orm.Query"]],
            order_by: Optional[Dict[str, str]] = None,
            order_by_exp: Optional[
                Dict[
                    str, Optional[Callable[["sa.orm.Query", str, bool], "sa.orm.Query"]]
                ]
            ] = None,
            search_filter: Optional[
                Callable[["sa.orm.Query", str], "sa.orm.Query"]
            ] = None,
            choice_filters: Iterable["jembeui.CList.ChoiceFilter"] = (),
            page_size: int = 0,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
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
            """
            self.query = query

            # defult db can be useds when db is None
            if db is not None:
                self.db = db
            else:
                self.db = get_jembeui().default_db
                if self.db is None:
                    raise JembeUIError(
                        "Either 'db' for CList.Config or default_db"
                        " on JembeUI instance must be set"
                    )

            # page size
            self.page_size = (
                page_size if page_size > 0 else settings.list_records_page_size
            )

            # order by
            self.order_by = order_by if order_by is not None else dict()
            self.order_by_exp = order_by_exp if order_by_exp is not None else dict()
            for oname in self.order_by.keys():
                # add default order by expresion
                if oname not in self.order_by_exp:
                    self.order_by_exp[oname] = self.__class__.default_order_by

            # search filter
            self.search_filter = search_filter

            # choice filters
            self.choice_filters = {
                f"cf{index}": cf for index, cf in enumerate(choice_filters)
            }

            # menu
            self.menu: Optional["Menu"] = (
                None
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )

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
                title,
                template,
                components,
                inject_into_components,
                redisplay,
                changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    class ChoiceFilter:
        """Represents choice filter to be add to table with all it properties and logic"""

        ListChoiceType = namedtuple("ListChoiceType", ["title", "value_str", "value"])

        def __init__(
            self,
            expr: Callable[["sa.orm.Query", Iterable[Any]], "sa.orm.Query"],
            *choices: Union[Tuple[str, str], Tuple[str, str, Any]],
            dynamic_choices: Optional[
                Callable[
                    ["jembeui.CList"],
                    Iterable[Union[Tuple[str, str], Tuple[str, str, Any]]],
                ]
            ] = None,
            default_choices: Union[
                Iterable[str], Callable[["jembeui.CList"], Iterable[str]]
            ] = (),
            grouped: Optional[bool] = None,
            title: Optional[Union[str, Callable[["jembeui.CList"], str]]] = None,
            multiselect: bool = True,
        ) -> None:
            """
            expr - python function that accepts query and list of values and
                   returns new query with applied filter based on the choices in values
            choices - list of tuples with choice title and choice value
                      that user can select to filter list records
            grouped: Optional[bool]:
                - None default grouping under filtes
                - True custome group witho or without title
                - False switches in line without grouping
            """
            self.expr = expr
            self.choices: List[Tuple[str, str, Any]] = [
                self.ListChoiceType(
                    c[0], str(c[1]), c[2] if len(c) == 3 else c[1]  # type:ignore
                )
                for c in choices
            ]
            self.str_values: List[str]
            self._dynamic_choices = dynamic_choices
            self._check_for_duplicate_choices()
            self.is_grouped = grouped
            self.default_choices = default_choices
            if isinstance(self.default_choices, (list, tuple)):
                self.default_choices = tuple([str(v) for v in self.default_choices])
            self.title = title
            self.multiselect = multiselect

        def map_values(self, str_values: Iterable[str]) -> Iterable[Any]:
            """Map str values to actual valuse when passing to choicde expression"""
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
                    f"ListRecords.ChoiceFilter can't have duplicate values: {values}"
                )

        def mount(self, component: "jembe.Component") -> "jembeui.CList.ChoiceFilter":
            """Mount ChoiceFilter defintino to Component"""
            if (
                self._dynamic_choices
                or callable(self.title)
                or callable(self.default_choices)
            ):
                cfcopy = CList.ChoiceFilter(
                    self.expr,
                    *self.choices,
                    default_choices=(
                        tuple(str(v) for v in self.default_choices(component))
                        if callable(self.default_choices)
                        else self.default_choices
                    ),
                    grouped=self.is_grouped,
                    title=(
                        self.title(component) if callable(self.title) else self.title
                    ),
                    multiselect=self.multiselect,
                )
                cfcopy.choices.extend(
                    self.ListChoiceType(
                        c[0], str(c[1]), c[2] if len(c) == 3 else c[1]  # type:ignore
                    )
                    for c in self._dynamic_choices(component)  # type:ignore
                )
                cfcopy._check_for_duplicate_choices()
                return cfcopy
            return self

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
        """db session for easy access"""
        return self._config.db.session

    @action
    def jui_apply_choice_filter(self, filter_name, filter_value_str):
        """Action that applies choice filters to the query

        Action is called from template to update choice filters
        """
        # ignore when trying to modify undefined filter or when provided
        # value is not valid
        if (
            filter_name not in self.jui_choice_filters_config
            or filter_value_str
            not in self.jui_choice_filters_config[filter_name].str_values
        ):
            return

        # if self.state.choice_filters is None:
        #     self.state.choice_filters = dict()

        if (
            filter_name not in self.state.choice_filters
            or self.jui_choice_filters_config[filter_name].multiselect is False
        ):
            self.state.choice_filters[filter_name] = [filter_value_str]
        else:
            self.state.choice_filters[filter_name].append(filter_value_str)

        self.state.page = 0

    @action
    def jui_remove_choice_filter(self, filter_name, filter_value_str):
        """Remove filter from query"""
        # ignore when trying to remove undefined filter or when provided
        # value is not valid
        if (
            filter_name not in self.jui_choice_filters_config
            or filter_value_str
            not in self.jui_choice_filters_config[filter_name].str_values
        ):
            return

        # ignore when filter is not set
        if filter_name not in self.state.choice_filters:
            return
        if filter_value_str not in self.state.choice_filters[filter_name]:
            return

        # remove filter
        self.state.choice_filters[filter_name].remove(filter_value_str)
        if len(self.state.choice_filters[filter_name]) == 0:
            del self.state.choice_filters[filter_name]

        # if len(self.state.choice_filters) == 0:
        #     self.state.choice_filters = None

        self.state.page = 0

    @cached_property
    def jui_choice_filters_config(self):
        """Dictionary of filter name and filter configuration from _config"""
        return {
            name: cf.mount(self) for name, cf in self._config.choice_filters.items()
        }

    @cached_property
    def jui_pagination_steps(self) -> List[int]:
        """Returns list of page_steps to be used as alternative to default setting"""
        psize = self._config.page_size
        step = psize
        if step * 5 >= 100:
            # use arithemtic sequence
            steps = [psize * (i + 1) for i in range(100 // psize)]
        else:
            # use fibonacci sequence
            cstep = step
            steps = []
            while cstep <= 100:
                steps.append(cstep)
                cstep = cstep + cstep
        if psize // 2 >= 10:
            steps.insert(0, psize // 2)
        return steps

    def hydrate(self):
        """Prepare query and context variables for rendering list, search,filters and pagination"""
        # Enclosing in try-except in order to pinpoint error source file on error
        try:
            # When there is not choice filters set use default ones
            if self.state.choice_filters is None:
                # apply default filters
                self.state.choice_filters = {
                    name: list(cf.default_choices)
                    for name, cf in self.jui_choice_filters_config.items()
                }

            # Get sqlAlchemy query
            query = (
                self._config.query
                if isinstance(self._config.query, sa.orm.Query)
                else self._config.query(self)
            )
            # Check if query without choice and search filters is empty
            self.has_records = self.session.query(
                query.with_session(self.session()).order_by(None).exists()
            ).scalar()

            # assign db session to query and instruct query to always return tuples
            query = query.with_session(self.session()).only_return_tuples(True)

            # apply search filter
            if self._config.search_filter is not None and self.state.search:
                query = self._config.search_filter(query, self.state.search)

            # apply choice filters (and clean input)
            cleaned_choice_filters = dict()
            if self.state.choice_filters:
                for name in self.state.choice_filters.keys():
                    if (
                        name in self.jui_choice_filters_config.keys()
                        and self.state.choice_filters[name]
                    ):
                        cfilter = self.jui_choice_filters_config[name]
                        str_value = self.state.choice_filters[name]
                        query = cfilter.expr(query, cfilter.map_values(str_value))
                        try:
                            cleaned_choice_filters[name].append(str_value)
                            cleaned_choice_filters[name] = list(
                                set(cleaned_choice_filters[name])
                            )
                        except KeyError:
                            cleaned_choice_filters[name] = list(str_value)
            if len(cleaned_choice_filters) == 0:
                self.state.choice_filters = dict()
            else:
                self.state.choice_filters = cleaned_choice_filters

            # apply order by
            if self.state.order_by:
                fname = self.state.order_by.strip("-")
                is_desc = self.state.order_by.startswith("-")
                if fname in self._config.order_by.keys():
                    query = self._config.order_by_exp[fname](query, fname, is_desc)

            # apply pagination and get record and pages count
            self.total_records = query.count()
            self.total_pages = ceil(self.total_records / self.state.page_size)
            if self.state.page > self.total_pages - 1:
                self.state.page = self.total_pages - 1
            if self.state.page < 0:
                self.state.page = 0
            self.start_record_index = self.state.page * self.state.page_size
            self.end_record_index = self.start_record_index + self.state.page_size
            if self.end_record_index > self.total_records:
                self.end_record_index = self.total_records
            # get records to be displayed and associte with records (visible in template)
            self.records = query[self.start_record_index : self.end_record_index]

            # bind menu to component
            self.menu = self._config.menu.bind_to(self) if self._config.menu else None
        except Exception as err:
            err.args = (f"Exception in {self.__class__}",) + err.args
            raise err