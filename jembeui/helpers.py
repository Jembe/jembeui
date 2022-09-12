from typing import TYPE_CHECKING, List, Dict, Tuple
import re
from PIL import Image, ImageOps
from flask import current_app
from jembe import get_jembe
from .exceptions import JembeUIError

if TYPE_CHECKING:
    import jembe
    from jembeui import JembeUI

__all__ = (
    "get_jembeui",
    "get_widget_variants",
    "get_component_template_variants",
    "camel_to_snake",
    "convert_py_date_format_to_js",
    "create_thumbnail",
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
    reexp = re.compile(f"{tname_start}__([^\.]+)\.[^\.]+")
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


BABEL_DATETIME_FORMAT_TO_DATEPICKER_JS = {
    "dd": "dd",
    "d": "d",
    "EEEE": "DD",
    "EEE": "D",
    "MMMM": "MM",
    "MMM": "M",
    "MM": "mm",
    "M": "m",
    "y": "yyyy",
}


def convert_py_date_format_to_js(format_str, usefor: str = "datepicker"):
    """
    * Description: Convert a python format string to javascript format string
    * Example:     "%m/%d/%Y" to "MM/DD/YYYY"
    * @param:  formatStr is the python format string
    * @return: the javascript format string
    */
    """
    wordbook = {}
    if usefor == "datepicker":
        wordbook = BABEL_DATETIME_FORMAT_TO_DATEPICKER_JS
    for key in wordbook.keys():
        format_str = wordbook[key].join(format_str.split(key))
    return format_str


def create_thumbnail(
    image: "jembe.File", thumbnail_size: Tuple[int, int]
) -> "jembe.File":
    thumb = image.get_cache_version(f"thumbnail_{thumbnail_size[0]}_{thumbnail_size[1]}.jpg")
    if not thumb.exists():
        try:
            with Image.open(image.open(mode="rb")) as img:
                img.verify()
        except Exception:
            return None
        with Image.open(image.open(mode="rb")) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img = ImageOps.exif_transpose(img)
            img.thumbnail(thumbnail_size, Image.BICUBIC)
            with thumb.open("wb") as tfo:
                img.save(tfo, "JPEG")
                return thumb
    else:
        return thumb
