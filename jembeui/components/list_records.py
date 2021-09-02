from typing import TYPE_CHECKING, Optional, Union, Callable, Iterable, Tuple, Dict
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


class CListRecords(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/list_records.html"
        # TEMPLATE_VARIANTS = ()
        def __init__(
            self,
            query: "sa.orm.Query",
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

            self.query = query
            self._db = db
            self.page_size = (
                page_size if page_size > 0 else settings.list_records_page_size
            )

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
        self.records = self._config.query.with_session(self._config.db.session())

        # columns
        self.columns = [cd.get("name", None) for cd in self.records.column_descriptions]

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


        return super().display()
