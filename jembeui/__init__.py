from typing import TYPE_CHECKING, Optional
from babel.core import get_locale_identifier

from flask import session, request
import flask_babel
from flask_babel import get_locale

from .exceptions import JembeUIError
from .sqlalchemy import SaFile

from .includes.link import Link
from .includes.menu import Menu
from .includes.field import FieldMixin
from .includes.file_field import FileField
from .includes.lov_field import LovField
from .includes.tiptap_field import TipTapField
from .includes.form import Form, TrailFormConfig
from .components import (
    Component,
    CPage,
    CForm,
    WDB,
    CCreateRecord,
    CViewRecord,
    CUpdateRecord,
    # ComponentWithMenu,
    # CMenu,
    # CBreadcrumb,
    CList,
    CListRecords,
    # CDeleteRecord,
)
from .helpers import convert_py_date_format_to_js, camel_to_snake, create_thumbnail

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    from jembe import Jembe

__all__ = (
    "JembeUI",
    "Link",
    "Menu",
    "Form",
    "TrailFormConfig",
    "CForm",
    "WDB",
    "CCreateRecord",
    "CViewRecord",
    "CUpdateRecord",
    "IsDataclass",
    # "Breadcrumb",
    # "BreadcrumbList",
    # "Form",
    "SaFile",
    "FieldMixin",
    "FileField",
    # "ImageField",
    "LovField",
    "TipTapField",
    "Component",
    # "ComponentWithMenu",
    "CPage",
    # "CMenu",
    # "CBreadcrumb",
    "CList",
    "CListRecords",
    # "CForm",
    # "CDeleteRecord",
    "create_thumbnail",
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
                "Jembe UI must be initialised before initialising jembe extension!"
            )

        self.__jembe.extensions["jembeui"] = _JembeUIState(self)

        if default_db is not None:
            self.default_db = default_db

    def do_init_jembe(self):
        from .page import JembeUIPage

        if "babel" not in self.__jembe.flask.extensions:
            raise JembeUIError(
                "FlaskBabel extension must be initialised before initialising Jembe with JembeUI extension!"
            )

        self.__jembe.add_page(
            "jembeui", JembeUIPage
        )  # if removed jembeui templates will not load

        def get_locale_code(separator="-"):
            locale = get_locale()
            return get_locale_identifier(
                (
                    locale.language,
                    locale.territory,
                    locale.script,
                    locale.variant,
                ),
                separator,
            ).lower()

        # jembetimezone support
        @self.__jembe.flask.before_request
        def update_user_timezone_and_locale():
            if "jembeuiTimezone" in request.cookies and request.cookies.get(
                "jembeuiTimezone"
            ) != session.get("jembeui_timezone", None):
                session["jembeui_timezone"] = request.cookies["jembeuiTimezone"]
                flask_babel.refresh()

            if "jembeuiLocaleCode" in request.cookies and request.cookies.get(
                "jembeuiLocaleCode"
            ) != session.get("jembeui_locale_code", None):
                from jembeui.settings import settings

                lc = request.cookies["jembeuiLocaleCode"]
                if lc in settings.supported_locales:
                    session["jembeui_locale_code"] = lc
                    flask_babel.refresh()

        @self.__jembe.flask.after_request
        def set_locale_cookie(response):
            response.set_cookie("jembeuiLocaleCode", get_locale_code("_"))
            return response

        babel = self.__jembe.flask.extensions["babel"]

        @babel.timezoneselector
        def get_user_timezone():
            if "jembeuiTimezone" in request.cookies and request.cookies.get(
                "jembeuiTimezone"
            ) != session.get("jembeui_timezone", None):
                session["jembeui_timezone"] = request.cookies["jembeuiTimezone"]
            return session.get("jembeui_timezone", None)

        @babel.localeselector
        def get_user_locale():
            from jembeui.settings import settings

            if "jembeuiLocaleCode" in request.cookies and request.cookies.get(
                "jembeuiLocalCode"
            ) != session.get("jembeui_local_code", None):
                lc = request.cookies["jembeuiLocaleCode"]
                if lc in settings.supported_locales:
                    session["jembeui_locale_code"] = lc
            if "jembeui_locale_code" not in session:
                session["jembeui_locale_code"] = (
                    settings.supported_locales[0]
                    if settings.supported_locales
                    else "en"
                )
            return session["jembeui_locale_code"]

        self.__jembe.flask.jinja_env.globals.update(
            {
                "jembeui_get_js_date_format": lambda usefor: convert_py_date_format_to_js(
                    get_locale().date_formats["medium"].pattern, usefor
                ),
                "jembeui_get_js_datetime_format": lambda usefor: convert_py_date_format_to_js(
                    get_locale()
                    .datetime_formats["medium"]
                    .format(
                        get_locale().time_formats["medium"].pattern,
                        get_locale().date_formats["medium"].pattern,
                    ),
                    usefor,
                ),
                "jembeui_get_js_time_format": lambda usefor: convert_py_date_format_to_js(
                    get_locale().time_formats["medium"].pattern, usefor
                ),
                "jembeui_get_locale_code": lambda separator="_": get_locale_code(
                    separator
                ),
                "jembeui_get_timezone": lambda: session.get("jembeui_timezone", None),
            }
        )
        self.__jembe.flask.jinja_env.filters.update(
            {"jembeui_camel_to_snake": camel_to_snake}
        )

    def set_default_db(self, default_db: "SQLAlchemy"):
        self.default_db = default_db
