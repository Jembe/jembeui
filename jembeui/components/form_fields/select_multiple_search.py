from typing import TYPE_CHECKING, Union, Callable, Tuple, Optional, Dict, Iterable, List

from ...components import Component
from ...exceptions import JembeUIError
from jembe import action

if TYPE_CHECKING:
    import jembe
    import jembeui
    import sqlalchemy as sa


__all__ = ("CSelectMultipleSearch",)


class CSelectMultipleSearch(Component):
    class Config(Component.Config):
        default_template_exp = (
            "jembeui/{style}/components/form_fields/select_multiple_search.html"
        )

        def __init__(
            self,
            field_name: str,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )
            self.field_name = field_name

    _confing: Config

    def __init__(
        self,
        search: str = "",
        selected: Tuple[str, ...] = (),
        is_disabled: bool = False,
        _form: Optional["jembeui.Form"] = None,
    ):
        if _form is not None:
            self._form = _form
            self._cform = _form.cform
            self._field = getattr(_form, self._config.field_name)
        else:
            raise JembeUIError(
                "SelectMultipeSearch Component must have _form parameter injected"
            )
        super().__init__()

    @property
    def form(self) -> "jembeui.Form":
        return self._form

    @property
    def cform(self) -> "jembeui.CForm":
        return self._cform

    @property
    def field(self) -> "jembeui.SelectMultipleField":
        return self._field

    @property
    def all_choices_ids(self) -> list:
        return self.field._all_choices_ids()

    @property
    def selected_choices(self) -> List[Tuple[str, str]]:
        return self.field._get_selected_choices(self.state.selected)

    @property
    def all_choices(self) -> list:
        return self.field._all_choices()

    @property
    def choices(self) -> List[tuple]:
        return self.field._get_choices(self.state.search, self.state.selected)
