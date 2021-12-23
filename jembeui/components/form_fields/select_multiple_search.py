from typing import TYPE_CHECKING, Union, Callable, Tuple, Optional, Dict, Iterable, List

from jembe import listener
from ...components import Component
from ...exceptions import JembeUIError

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
            view_component: Optional["jembe.ComponentReference"] = None,
            update_component: Optional["jembe.ComponentReference"] = None,
            create_component: Optional["jembe.ComponentReference"] = None,
            display_update_link: bool = True,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            if components is None:
                components = dict()
            if view_component:
                components["view"] = view_component
            if update_component:
                components["update"] = update_component
            if create_component:
                components["create"] = create_component

            self.display_update_link = display_update_link
            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )
            self.field_name = field_name

    _config: Config

    def __init__(
        self,
        selected: Tuple[str, ...] = (),
        search: Optional[str] = None,
        is_disabled: bool = False,
        _form: Optional["jembeui.Form"] = None,
    ):
        if _form is None:
            raise JembeUIError(
                "SelectMultipeSearch Component must have _form parameter injected"
            )
        self._form = _form
        super().__init__()

    @property
    def form(self) -> "jembeui.Form":
        return self._form

    @property
    def cform(self) -> "jembeui.CForm":
        return self._form.cform

    @property
    def field(self) -> "jembeui.SelectMultipleField":
        return getattr(self._form, self._config.field_name)

    @property
    def selected_choices(self) -> List[Tuple[str, str]]:
        return self.field._get_selected_choices(self.state.selected)

    @property
    def choices(self) -> List[tuple]:
        if self.state.search is not None:
            return self.field._get_choices(self.state.search, self.state.selected)
        else:
            return []

    @property
    def choices_count(self) -> int:
        all_choices_result = self.field._get_all_choices_result()
        if isinstance(all_choices_result, list):
            return len(all_choices_result)
        else:
            return all_choices_result.count()

    @property
    def has_view_component(self) -> bool:
        return "view" in self._config.components

    @property
    def has_update_component(self) -> bool:
        return "update" in self._config.components

    @property
    def has_create_component(self) -> bool:
        return "create" in self._config.components

    @listener(event="cancel", source=("view", "update", "create"))
    def on_cancel(self, event: "jembe.Event"):
        self.remove_component(event.source_name)
        if not self._config.display_update_link and event.source_name == "update":
            self.display_component("view", id=event.source.state.id)

    @listener(event="submit", source=("update", "create"))
    def on_submit(self, event: "jembe.Event"):
        if event.source_name == "update":
            if not event.source._config.redisplay_on_submit:
                self.remove_component(event.source_name)
                if self.has_view_component and not self._config.display_update_link:
                    self.display_component("view", id=event.source.state.id)
        elif event.source_name == "create":
            self.remove_component(event.source_name)
            if self.has_view_component:
                self.display_component("view", id=event.source.record.id)
            self.state.selected = self.state.selected + (event.source.record.id,)
            self.emit(
                "update_form_field",
                name=self._config.field_name,
                value=self.state.selected,
            ).to("..")
        return True

    @listener(event="_display", source=("view", "update", "create"))
    def on_display_subcomponent(self, event: "jembe.Event"):
        for cname in ("view", "update", "create"):
            if cname != event.source_name and cname in self._config.components:
                self.remove_component(cname)
