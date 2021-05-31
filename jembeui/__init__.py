from typing import TYPE_CHECKING, Optional

from jinja2.loaders import ChoiceLoader, PackageLoader
from .components import Component, CPage, CPageBase

if TYPE_CHECKING:
    from flask import Flask

__all__ = (
    "JembeUI",
    "Component",
    "CPage",
    "CPageBase",
)


class JembeUI:
    def __init__(self, app: Optional["Flask"] = None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: "Flask"):
        from jembe.app import jembe
        from .page import JembeUIPage
        jembe.add_page("jembeui", JembeUIPage)
