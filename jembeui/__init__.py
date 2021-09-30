from typing import TYPE_CHECKING, Optional

from .exceptions import JembeUIError
from .lib import (
    Link,
    ActionLink,
    URLLink,
    Menu,
    Breadcrumb,
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


class JembeUI:
    def __init__(
        self, jembe: Optional["Jembe"] = None, default_db: Optional["SQLAlchemy"] = None
    ) -> None:
        self.default_db = default_db
        if jembe is not None and jembe.flask is not None:
            self.init_app(jembe)

    def init_app(self, jembe: "Jembe", default_db: Optional["SQLAlchemy"] = None):
        from .page import JembeUIPage

        self.__jembe = jembe
        if jembe.flask is not None:
            raise JembeUIError(
                "Jembe UI must be initialised before initialising jembe extension"
            )

        self.__jembe.extensions["jembeui"] = _JembeUIState(self)

        if default_db is not None:
            self.default_db = default_db

        jembe.add_page(
            "jembeui", JembeUIPage
        )  # if removed jembeui templates will not load

    def set_default_db(self, default_db: "SQLAlchemy"):
        self.default_db = default_db
