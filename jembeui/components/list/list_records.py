from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Optional, Sequence, Tuple, Union
from datetime import datetime, date, time, timedelta
from markupsafe import Markup
import sqlalchemy as sa
from flask_babel import format_date, format_datetime, format_time, format_timedelta, lazy_gettext as _
from flask import render_template
from jembeui.includes.menu import Menu
from .list import CList


if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CListRecords",)

def default_field_value(component: "jembe.Component", record, field_name: str) -> str:
    """Default handler for displaying data inside the table"""
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
        return Markup(
            render_template(
                "jembeui/s0/widgets/table_boolean_field.html", value=value
            )
        )
    else:
        return str(value) if value is not None else ""  # type: ignore

class CListRecords(CList):
    """Display list of records from SQLAlchemy query as HTML table"""

    class Config(CList.Config):
        """Configure how to Display list of records from sqlalchemy

        Args:
            fields (Dict[str,str]): name of the field and its title
            field_values(Dict[str,Callable]): callable to get value of the field from query
            record_menu: callable that returns menu for current record
        """
        default_template: str = "/jembeui/components/list/table.html"
        default_field_value = default_field_value

        def __init__(
            self,
            query: Union["sa.orm.Query", Callable[["jembeui.CList"], "sa.orm.Query"]],
            fields: Optional[Dict[str, str]] = None,
            field_values: Optional[
                Dict[str, Callable[["jembeui.Component", Any, str], str]]
            ] = None,
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
            record_menu: Optional[
                Callable[
                    ["jembeui.Component", Any],
                    Union[
                        "jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]
                    ],
                ]
            ] = None,
            no_data_message: str = _("No data found"),
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
            # field names
            self.fields = fields if fields is not None else dict()
            self.fields = {k: v if v is not None else k for k, v in self.fields.items()}
            if isinstance(query, sa.orm.Query) and not self.fields:
                self.fields = {
                    ca["name"]: ca["name"].replace("_", " ")
                    for ca in query.column_descriptions
                }

            # field values
            self.field_values = field_values if field_values is not None else dict()
            for field_name in self.fields.keys():
                if field_name not in self.field_values:
                    self.field_values[field_name] = self.__class__.default_field_value

            # order by
            order_by = {k:v for k, v in self.fields.items()}
            if order_by_exp is not None:
                for ordr, exp in order_by_exp.items():
                    if exp is None and ordr in order_by:
                        del order_by[ordr]

            # record menu
            self.record_menu = record_menu

            self.no_data_message = no_data_message
            super().__init__(
                query,
                order_by=order_by,
                order_by_exp=order_by_exp,
                search_filter=search_filter,
                choice_filters=choice_filters,
                menu=menu,
                page_size=page_size,
                db=db,
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: "Config"

    def hydrate(self):
        super().hydrate()

        # initialise field renderes
        self.field_values = {
            field_name: partial(field_value, self)
            for field_name, field_value in self._config.field_values.items()
        }

        # record menu
        self.get_record_menu = self._get_record_menu

    def _get_record_menu(self, record) -> Optional["jembeui.Menu"]:
        """Method to be called on each record in template to get its action menu"""
        if self._config.record_menu is None:
            return None
        raw_menu = self._config.record_menu(self, record)
        menu = raw_menu if isinstance(raw_menu, Menu) else Menu(raw_menu)
        return menu.bind_to(self)