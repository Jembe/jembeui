from typing import TYPE_CHECKING, Optional
from babel.core import get_locale_identifier

from flask_babel import get_locale
from .exceptions import JembeUIError
from .lib import (
    Link,
    ActionLink,
    URLLink,
    Menu,
    Breadcrumb,
    BreadcrumbList,
    Form,
    JembeFileField,
    JembeImageField,
)
from .components import (
    Component,
    CPage,
    CMenu,
    CBreadcrumb,
    CListRecords,
    CForm,
    CUpdateRecord,
    CCreateRecord,
    CViewRecord,
    CDeleteRecord,
)
from .helpers import convert_py_date_format_to_js

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    from jembe import Jembe

__all__ = (
    "JembeUI",
    "Link",
    "ActionLink",
    "URLLink",
    "Menu",
    "Breadcrumb",
    "BreadcrumbList",
    "Form",
    "JembeFileField",
    "JembeImageField",
    "Component",
    "CPage",
    "CMenu",
    "CBreadcrumb",
    "CListRecords",
    "CForm",
    "CUpdateRecord",
    "CCreateRecord",
    "CViewRecord",
    "CDeleteRecord",
)


class _JembeUIState:
    def __init__(self, jui: "JembeUI") -> None:
        self.jui = jui

    def do_init_jembe(self):
        self.jui.do_init_jembe()


class JembeUI:
    def __init__(
        self, jembe: Optional["Jembe"] = None, default_db: Optional["SQLAlchemy"] = None
    ) -> None:
        self.default_db = default_db
        if jembe is not None and jembe.flask is not None:
            self.init_jembe(jembe)

    def init_jembe(self, jembe: "Jembe", default_db: Optional["SQLAlchemy"] = None):

        self.__jembe = jembe
        if jembe.flask is not None:
            raise JembeUIError(
                "Jembe UI must be initialised before initialising jembe extension"
            )

        self.__jembe.extensions["jembeui"] = _JembeUIState(self)

        if default_db is not None:
            self.default_db = default_db

    def do_init_jembe(self):
        from .page import JembeUIPage

        self.__jembe.add_page(
            "jembeui", JembeUIPage
        )  # if removed jembeui templates will not load

        self.__jembe.flask.jinja_env.globals.update(
            {
                "jembeui_date_format_js": lambda usefor: convert_py_date_format_to_js(
                    get_locale().date_formats["medium"].pattern, usefor
                ),
                "jembeui_datetime_format_js": lambda usefor: convert_py_date_format_to_js(
                    get_locale()
                    .datetime_formats["full"]
                    .format(
                        get_locale().time_formats["full"].pattern,
                        get_locale().date_formats["full"].pattern,
                    ),
                    usefor,
                ),
                "jembeui_time_format_js": lambda usefor: convert_py_date_format_to_js(
                    get_locale().time_formats["medium"].pattern, usefor
                ),
                "get_locale_code": lambda separator="_": get_locale_identifier(
                    (
                        get_locale().language,
                        get_locale().territory,
                        get_locale().script,
                        get_locale().variant,
                    ),
                    separator,
                ).lower(),
            }
        )

    def set_default_db(self, default_db: "SQLAlchemy"):
        self.default_db = default_db
