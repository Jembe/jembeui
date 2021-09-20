from typing import TYPE_CHECKING, List, Dict
import re
from flask import current_app
from jembe import get_jembe
from .exceptions import JembeUIError
from .settings import settings

if TYPE_CHECKING:
    from jembeui import JembeUI

__all__ = (
    "get_jembeui",
    "get_widget_variants",
    "get_component_template_variants",
    "camel_to_snake",
)


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


def get_component_template_variants(template_name: str) -> Dict[str, str]:
    """
    returns dict[  variant_name: template_path]
    where variant_name is part of template name after __ (double underscore)
    and before .html extension
    """
    template_variants = dict()
    tname_start = template_name.split(".")[0]
    reexp = re.compile("{}__([^\.]+)\.[^\.]+".format(tname_start))
    for tname in current_app.jinja_env.list_templates():
        variant_match = reexp.match(tname)
        if variant_match is not None:
            template_variants[variant_match[1]] = tname
    return template_variants


_re_cts_1 = re.compile("(.)([A-Z][a-z]+)")
_re_cts_2 = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(name: str) -> str:
    global _re_cts_1, _re_cts_2
    name = _re_cts_1.sub(r"\1_\2", name)
    return _re_cts_2.sub(r"\1_\2", name).lower()
