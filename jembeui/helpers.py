from jembeui.exceptions import JembeUIError
from typing import Optional
from typing import TYPE_CHECKING, Optional
from flask import current_app

if TYPE_CHECKING:
    from jembeui import JembeUI

__all__ = ("get_jembeui",)


def get_jembeui() -> "JembeUI":
    jembeui_state = current_app.extensions.get("jembeui", None)
    if jembeui_state is None:
        raise JembeUIError("JembeUI is not initialised")
    return jembeui_state.jui
