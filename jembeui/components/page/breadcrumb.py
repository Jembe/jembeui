from typing import (
    Any,
    List,
    Sequence,
    Set,
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    Optional,
    Tuple,
    Union,
)
from uuid import uuid4
from dataclasses import asdict, dataclass, field
from jembe import JembeInitParamSupport, listener
from ..component import Component

if TYPE_CHECKING:
    import jembe
    from jembeui import Menu


__all__ = ("Bradcrumb", "CBreadcrumb")


def _get_default_breadcrumb_title(component: "jembe.Component") -> str:
    """Returns default breadcrum title for the component"""
    if isinstance(component, Component):
        return component.title
    return component._config.name


class Breadcrumb:
    def __init__(
        self,
        component_full_name: Optional[str] = None,
        component_init_params: Optional[dict] = None,
        title: Union[str, Callable[["jembe.Component"], str]] = "",
        children: Optional[Sequence["Breadcrumb"]] = None,
    ) -> None:
        self.component_full_name = component_full_name
        self.title = title
        if self.title == "" and self.component_full_name is not None:
            self.title = _get_default_breadcrumb_title
        self.component_init_params = component_init_params
        self._children: List["Breadcrumb"] = list()

        self.id = str(uuid4())
        self._parent: Optional[Breadcrumb] = None
        self._all_parents_ids: Set[str] = set()
        self._all_childrens_ids: Set[str] = set()

        if children is not None:
            self.children = children

        if self.component_full_name is None and not isinstance(self.title, str):
            raise ValueError(
                "Breadcrumb without component_full_name, can't have callable title!"
            )

    @property
    def parent(self) -> Optional["Breadcrumb"]:
        return self._parent

    @parent.setter
    def parent(self, parent: "Breadcrumb"):
        if self._parent is not None:
            # remove itself from parent breadcrumb
            self._parent.children = [
                c for c in self._parent.children if c.id != self.id
            ]
        self._parent = parent
        self._update_all_parents_ids()

    def _update_all_parents_ids(self):
        self._all_parents_ids = set(self.parent._all_parents_ids)
        self._all_parents_ids.add(self.parent.id)
        for c in self.children:
            c._update_all_parents_ids()

    @property
    def children(self) -> Sequence["Breadcrumb"]:
        return self._children

    @children.setter
    def children(self, children: Sequence["Breadcrumb"]):
        for c in children:
            c.parent = self

        self._update_all_childrens_ids()

    def _update_all_childrens_ids(self):
        self._all_childrens_ids = set()
        for c in self.children:
            self._all_childrens_ids = self._all_childrens_ids.union(
                c._all_childrens_ids
            )
            self._all_childrens_ids.add(c.id)

        self.parent._update_all_childrens_ids()

    @property
    def is_link(self) -> bool:
        return self.component_full_name is not None

    def get_item(
        self, component: Optional["jembe.Component"] = None
    ) -> "BreadcrumbItem":
        if component and component._config.full_name == self.component_full_name:
            component_reference = (
                component.component(".", **self.component_init_params)
                if self.component_init_params is not None
                else component.component_reset(".")
            )
            return BreadcrumbItem(
                self.id,
                self.title if isinstance(self.title, str) else self.title(component),
                component_reference.url,
                component_reference.jrl,
            )
        else:
            return BreadcrumbItem(
                self.id,
                self.title if isinstance(self.title, str) else self.title(component),
                None,
                None,
            )

    @classmethod
    def from_menu(cls, menu: Menu):
        raise NotImplementedError()


@dataclass
class BreadcrumbItem(JembeInitParamSupport):
    id: str
    title: str
    url: Optional[str]
    jrl: Optional[str]

    @classmethod
    def dump_init_param(cls, value: "BreadcrumbItem") -> Any:
        return asdict(value)

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return BreadcrumbItem(
            id=value.get("id"),
            title=value.get("title"),
            url=value.get("url"),
            jrl=value.get("jrl"),
        )


class CBreadcrumb(Component):
    """
    Displays breadcrumb current navigation postition based on deepest component displayed on the page
    that is registred as breadcrumb link.

    Bredcrumb can display components referenced by its full_name and passive text.
    Passive text is useful for grouping components links, for example "Settings" groupe without need
    to create Settings component and .
    """

    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/breadcrumb.html"
        # TEMPLATE_VARIANTS = ()

        def __init__(
            self,
            breadcrums: Sequence["Breadcrumb"],
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = False,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            self.breadcrumbs = breadcrums
            self.breadcrumbs_flat: Dict[str, Breadcrumb] = self._flatten_breadcrumbs(
                breadcrums
            )
            self.breadcrumbs_mapping: Dict[str, Breadcrumb] = {
                b.component_full_name: b
                for b in self.breadcrumbs_flat.values()
                if b.component_full_name is not None  # b.is_link
            }
            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        def _flatten_bradcrumbs(
            self,
            breadcrumbs: Sequence[Breadcrumb],
        ) -> Dict[str, Breadcrumb]:
            flatten: Dict[str, Breadcrumb] = dict()
            for b in breadcrumbs:
                flatten[b.id] = b
                flatten.update(self._flatten_bradcrumbs(b.children))
            return flatten

    _config: Config

    def __init__(self, bitems: Tuple[BreadcrumbItem, ...] = ()):
        super().__init__()

    @listener(event="_display")
    def on_component_display(self, event: "jembe.Event"):
        if event.source_full_name not in self._config.breadcrumbs_mapping:
            # component that has been displayed does not have associated breadcrumb
            return
        # update self.state.bitems remove all bitems after new_bitem
        # TODO incorporate non link breadcrumbitems
        #   - remove/ignore them complitrly when building bitems_new 
        #   - add them at the end when bitems_new is complitly formed
        new_bitem = self._config.breadcrumbs_mapping[event.source_full_name].get_item(
            event.source
        )
        bitems_new: List[BreadcrumbItem] = []
        resolved = False
        for bitem in self.state.bitems:
            if self._config.is_parent_breadcrumb(new_bitem, bitem):
                bitems_new.append(new_bitem)
                bitems_new.extend(self.state.bitems)
                resolved = True
                break
            elif new_bitem.id == bitem.id:
                bitems_new.append(new_bitem)
                resolved = True
                break
            elif self._config.is_parent_breadcrumb(bitem, new_bitem):
                bitems_new.append(bitem)
            else:
                bitems_new.append(new_bitem)
                resolved = True
                break

        if resolved:
            self.state.bitems = tuple(bitems_new)
        elif len(bitems_new) > 0 and self._config.is_parent_breadcrumb(
            bitems_new[-1], new_bitem
        ):
            bitems_new.append(new_bitem)
            self.state.bitems = tuple(bitems_new)
        else:
            self.state.bitems = tuple(bitems_new)

    # def display(self) -> "jembe.DisplayResponse":
    #     # init breadcrumbs based on self.state.bcs and add bradcrumb groups in it
    #     # bindit to components and add parent
    #     self.breadcrumbs: List[] = []
    #     return super().display()


# TODO separate breadcrumb config classes from actual breadcrumb items used inside running component
# Breadcrum component need to have just title:str and full_name nothing more or nothing less
# parent type navigation should be removed use regular list instead
#
