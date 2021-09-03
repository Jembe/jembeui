from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    Callable,
    Iterable,
    Dict,
    Tuple,
    Any,
)
from datetime import date, datetime
from functools import partial
from math import ceil
from .component import Component
from jembeui.helpers import get_jembeui
from jembeui.settings import settings
from jembeui.exceptions import JembeUIError

if TYPE_CHECKING:
    import jembe
    from flask_sqlalchemy import SQLAlchemy
    import sqlalchemy as sa

__all__ = ("CListRecords",)


def default_field_value(component: "jembe.Component", record, field_name: str) -> str:
    fnames = field_name.split("__")
    value = record[fnames.pop(0)]
    while len(fnames) > 0:
        value = getattr(value, fnames.pop(0))
    if isinstance(value, date):
        return str(value) # TODO
    elif isinstance(value, datetime):
        return str(value) # TODO
    elif isinstance(value, bool):
        return str(value) # TODO
    else:
        return str(value)  # type: ignore


class CListRecords(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/list_records.html"
        # TEMPLATE_VARIANTS = ()
        default_field_value = default_field_value

        def __init__(
            self,
            query: "sa.orm.Query",
            fields: Optional[Dict[str, str]] = None,
            field_values: Optional[
                Dict[str, Callable[["Component", Any, str], str]]
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
            # use @property self.db to get db so that
            # defult db can be useds when self._db is None
            self._db = db
            self.page_size = (
                page_size if page_size > 0 else settings.list_records_page_size
            )
            self.fields = (
                fields
                if fields is not None
                else {
                    ca["name"]: ca["name"].replace("_", " ")
                    for ca in self.query.column_descriptions
                }
            )
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

            if url_query_params is None:
                url_query_params = dict()
            if "page" not in url_query_params.values():
                url_query_params["p"] = "page"
            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        @property
        def db(self) -> "SQLAlchemy":
            if self._db is not None:
                return self._db
            self._db = get_jembeui().default_db
            if self._db is None:
                raise JembeUIError(
                    "Either 'db' for CListRecords.Config or default_db"
                    " on JembeUI instance must be set"
                )
            return self._db

    _config: "Config"

    def __init__(self, page: int = 0, page_size: int = 0):
        if page_size < 1:
            self.state.page_size = self._config.page_size
        super().__init__()

    def display(self):
        self.records = self._config.query.with_session(
            self._config.db.session()
        ).only_return_tuples(True)


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
            for field_name, field_value in
            self._config.field_values.items()
        }

        return super().display()
