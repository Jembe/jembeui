from jembeui.exceptions import JembeUIError
from typing import TYPE_CHECKING, List, Dict
from flask import current_app
from .settings import settings
from jembe import get_jembe

if TYPE_CHECKING:
    from jembeui import JembeUI

__all__ = ("get_jembeui", "get_widget_variants")


def get_jembeui() -> "JembeUI":
    jembe = get_jembe()
    jembeui_state = jembe.extensions.get("jembeui", None)
    if jembeui_state is None:
        raise JembeUIError("JembeUI is not initialised")
    return jembeui_state.jui


def get_widget_variants(templates_dir_list: List[str]) -> Dict[str, str]:
    """
    returns dict[  variant_name: template_path]
    where variant_name is template name without .html extension
    for all templates found in templates_dir_lists
    """
    template_variants = dict()
    for tname in current_app.jinja_env.list_templates():
        for tdir in templates_dir_list:
            tdir = tdir.format(style=settings.default_style)
            tdir = tdir if tdir.endswith("/") else tdir + "/"
            if tname.startswith(tdir):
                vname = tname[len(tdir) :].strip("/")
                if "/" not in vname:
                    template_variants[".".join(vname.split(".")[:-1])] = tname
    return template_variants
