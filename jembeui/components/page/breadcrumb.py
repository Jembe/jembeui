from typing import (
    Any,
    List,
    Sequence,
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
        self.children: List["Breadcrumb"] = (
            list(children) if children is not None else list()
        )

        self.id = str(uuid4())
        self._parent: Optional[Breadcrumb] = None
        self._all_parents_ids: List[str] = list()
        self._all_childrens_ids: List[str] = list()

        for c in self.children:
            c.parent = self
            self._all_childrens_ids.append(c.id)
            self._all_childrens_ids.extend(c._all_childrens_ids)

    @property
    def parent(self) -> Optional["Breadcrumb"]:
        return self._parent

    @parent.setter
    def parent(self, parent: "Breadcrumb"):
        self._parent = parent
        self._all_parents_ids = [*parent._all_parents_ids, parent.id]

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
                # self.parent.id if self.parent else None,
                # self._all_parents_ids,
                # self._all_childrens_ids,
            )
        else:
            return BreadcrumbItem(
                self.id,
                self.title if isinstance(self.title, str) else self.title(component),
                None,
                None,
                # self.parent.id if self.parent else None,
                # self._all_parents_ids,
                # self._all_childrens_ids,
            )


@dataclass
class BreadcrumbItem(JembeInitParamSupport):
    id: str
    title: str
    url: Optional[str]
    jrl: Optional[str]

    # parent_id: Optional[str]
    # all_parent_ids: List[str]
    # all_children_ids: List[str]

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

    Bredcrumb can display components referenced by its exec_names and passive text.
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
            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    def __init__(self, bc_items: Tuple[BreadcrumbItem, ...] = ()):
        super().__init__()

    @listener(event="_display")
    def on_component_display(self, event: "jembe.Event"):
        # update self.state.bcs remove all bcs after event.source_full_name
        # TODO check if event.source_full_name exist in self._config.breadcrumbs if so:
        bcs_new = []
        new_bc = BreadcrumbLink(
            event.source_full_name
        )  # look at _config.breadcrumbs and get new_bc
        resolved = False
        for bc in self.state.bcs:
            if self._is_parent(new_bc.full_name, bc.full_name):
                bcs_new.append(new_bc)
                bcs_new.extend(self.state.bcs)
                resolved = True
                break
            elif new_bc.full_name == bc.full_name:
                bcs_new.append(new_bc)
                resolved = True
                break
            elif self._is_parent(bc.full_name, new_bc.full_name):
                bcs_new.append(bc)
            else:
                bcs_new.append(new_bc)
                resolved = True
                break

        if resolved:
            self.state.bcs = tuple(bcs_new)
        elif len(bcs_new) > 0 and self._is_parent(
            bcs_new[-1].full_name, new_bc.full_name
        ):
            bcs_new.append(new_bc)
            self.state.bcs = tuple(bcs_new)
        else:
            self.state.bcs = [new_bc]

    def display(self) -> "jembe.DisplayResponse":
        # init breadcrumbs based on self.state.bcs and add bradcrumb groups in it
        # bindit to components and add parent
        self.breadcrumbs: List[Union[Breadcrumb, BreadcrumbGroup]] = []
        return super().display()


# TODO separate breadcrumb config classes from actual breadcrumb items used inside running component
# Breadcrum component need to have just title:str and full_name nothing more or nothing less
# parent type navigation should be removed use regular list instead
#
