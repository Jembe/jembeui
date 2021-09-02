from jembeui.exceptions import JembeUIError
from typing import TYPE_CHECKING, Optional

from .components import (
    Component,
    CPage,
    CMenu,
    Link,
    ActionLink,
    URLLink,
    Menu,
    Breadcrumb,
    CBreadcrumb,
)
from flask import current_app

if TYPE_CHECKING:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

__all__ = (
    "JembeUI",
    "Component",
    "CPage",
    "CMenu",
    "Link",
    "ActionLink",
    "URLLink",
    "Menu",
    "Breadcrumb",
    "CBreadcrumb",
)


class _JembeUIState:
    def __init__(self, jui: "JembeUI") -> None:
        self.jui = jui


class JembeUI:
    def __init__(
        self, app: Optional["Flask"] = None, default_db: Optional["SQLAlchemy"] = None
    ) -> None:
        self.app = app
        self.default_db = default_db
        if app is not None:
            self.init_app(app)

    def init_app(self, app: "Flask", default_db: Optional["SQLAlchemy"] = None):
        from .page import JembeUIPage

        jembe_state = current_app.extensions.get("jembe", None)
        if jembe_state is None:
            raise JembeUIError(
                "Jembe extension must be initialised before initialising JembeUI"
            )
        self.app = app
        self.app.extensions["jembeui"] = _JembeUIState(self)

        if default_db is not None:
            self.default_db = default_db

        jembe_state.jembe.add_page("jembeui", JembeUIPage)

    def set_default_db(self, default_db: "SQLAlchemy"):
        self.default_db = default_db
