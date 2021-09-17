from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Sequence,
    Set,
    Callable,
    Optional,
    Union,
)
from uuid import uuid3, NAMESPACE_DNS
from dataclasses import dataclass, field
from jembe import JembeInitParamSupport
from .link import ActionLink
from .menu import Menu
from ..exceptions import JembeUIError

if TYPE_CHECKING:
    import jembe
    from jembeui import Link


__all__ = (
    "Breadcrumb",
    "BreadcrumbList",
    "BreadcrumbItem",
)


def _get_default_breadcrumb_title(component: "jembe.Component") -> str:
    """Returns default breadcrum title for the component"""
    from ..components import Component

    if isinstance(component, Component):
        return component.title
    return component._config.name


class BreadcrumbList(List["Breadcrumb"]):
    def insert_into(
        self, component_full_name: str, *breadcrumbs: "Breadcrumb"
    ) -> "BreadcrumbList":
        """
        Insert breadcrumbs into existing breadcrumb found inside this breacrumb list
        returns self

        if breadcrumb with component_full_name can't be found raise JembeUI Exception
        """
        # TODO

        breadcrumb = self._find_breadcrumb(
            self, lambda bc: bc.component_full_name == component_full_name
        )
        if breadcrumb is None:
            raise JembeUIError(
                "Cant find breadcrumb with component full name equal '{}'".format(
                    component_full_name
                )
            )
        breadcrumb.children = [*breadcrumb.children, *breadcrumbs]
        return self

    def insert_into_by_title(
        self, title: str, *breadcrumbs: "Breadcrumb"
    ) -> "BreadcrumbList":
        """
        Insert breadcrumbs into existing breadcrumb found inside this breacrumb list
        returns self
        Finds breadcrumb with equal title and where component_full_name is None

        if breadcrumb with title can't be found raise JembeUI Exception
        """
        breadcrumb = self._find_breadcrumb(
            self, lambda bc: bc.title == title and bc.component_full_name is None
        )
        if breadcrumb is None:
            raise JembeUIError(
                "Cant find breadcrumb with title equal '{}'".format(title)
            )
        breadcrumb.children = [*breadcrumb.children, *breadcrumbs]
        return self

    def _find_breadcrumb(
        self, breadcrumbs: List["Breadcrumb"], match: Callable[["Breadcrumb"], bool]
    ) -> Optional["Breadcrumb"]:
        for bc in breadcrumbs:
            if match(bc):
                return bc
            cmatch = self._find_breadcrumb(bc.children, match)
            if cmatch:
                return cmatch
        return None


class Breadcrumb:
    def __init__(
        self,
        component_full_name: Optional[str] = None,
        component_init_params: Optional[dict] = None,
        title: Union[str, Callable[["jembe.Component"], str]] = "",
        children: Optional[Sequence["Breadcrumb"]] = None,
    ) -> None:
        """
        When component_full_name and title are None then this breadcrumb should not be displayed
        becouse its main purpuse is to hold its children (act as container for other breadcrumbs)
        """
        self.component_full_name = component_full_name
        self.title = title
        if self.title == "" and self.component_full_name is not None:
            self.title = _get_default_breadcrumb_title
        self.component_init_params = component_init_params
        self._children: List["Breadcrumb"] = list()

        self._parent: Optional[Breadcrumb] = None
        self._all_parents_ids: Set[str] = set()
        self._all_childrens_ids: Set[str] = set()

        self.id: str = self._calc_id()

        if children is not None:
            self.children = list(children)

        if self.component_full_name is None and not isinstance(self.title, str):
            raise ValueError(
                "Breadcrumb without component_full_name, can't have callable title!"
            )
        if self.component_full_name is None and self.title is None:
            raise ValueError(
                "Breadcrumb must have either component_full_name or title set!"
            )

    def _calc_id(self) -> str:
        idstr = "{}:::{}:::{}:::{}".format(
            self.component_full_name,
            self.title if isinstance(self.title, str) else "",
            ",".join(self._all_parents_ids),
            ",".join(
                [
                    c.component_full_name
                    if c.component_full_name
                    else (c.title if isinstance(c.title, str) else "")
                    for c in self.children
                ]
            ),
        )
        return str(uuid3(NAMESPACE_DNS, idstr))

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
        self.id = self._calc_id()
        for c in self.children:
            c._update_all_parents_ids()

    @property
    def children(self) -> List["Breadcrumb"]:
        return self._children

    @children.setter
    def children(self, children: List["Breadcrumb"]):
        for c in children:
            c.parent = self

        self._children = list(children)

        self._update_all_childrens_ids()

    def _update_all_childrens_ids(self):
        self._all_childrens_ids = set()
        for c in self.children:
            self._all_childrens_ids = self._all_childrens_ids.union(
                c._all_childrens_ids
            )
            self._all_childrens_ids.add(c.id)

        if self.parent is not None:
            self.parent._update_all_childrens_ids()

    @property
    def is_link(self) -> bool:
        return self.component_full_name is not None

    def get_breadcrumb_item(
        self,
        from_component: "jembe.Component",
        to_component: Optional["jembe.Component"] = None,
    ) -> "BreadcrumbItem":
        """
        Returns instance of BreadcrumbItem with specific URL and/or JRL attributes,
        ready to be displayed.
        """
        if to_component and to_component._config.full_name == self.component_full_name:
            component_reference = from_component.component(
                self.component_full_name,
                **(
                    self.component_init_params
                    if self.component_init_params is not None
                    else dict()
                )
            )
            return BreadcrumbItem(
                self.id,
                self.title if isinstance(self.title, str) else self.title(to_component),
                component_reference.url,
                component_reference.jrl,
            )
        else:
            return BreadcrumbItem(
                self.id,
                self.title if isinstance(self.title, str) else self.title(to_component),
                None,
                None,
            )

    @classmethod
    def from_menu(
        cls,
        menu: Optional[Union["Menu", Sequence[Union["Link", "Menu"]]]],
        first_home: bool = False,
    ) -> "BreadcrumbList":
        """Generates Breadcrum configuration from Menu configuration"""
        if menu is None:
            return BreadcrumbList()
        menu_source: "Menu" = Menu(menu) if not isinstance(menu, Menu) else menu
        if not first_home:
            return cls._from_menu_item(menu_source)
        else:
            home_menu = menu_source.items[0]
            if not isinstance(home_menu, ActionLink):
                raise ValueError(
                    "First item in menu must be action link when using first_home=True"
                )
            home = cls._from_menu_item(home_menu)[0]
            children: List["Breadcrumb"] = list()
            for menu_item in menu_source.items[1:]:
                children.extend(cls._from_menu_item(menu_item))
            home.children = children
            return BreadcrumbList((home,))

    @classmethod
    def _from_menu_item(cls, menu_item: Union[Menu, "Link"]) -> "BreadcrumbList":
        if isinstance(menu_item, Menu):
            menu = menu_item
            parent_bc: Optional["Breadcrumb"] = (
                Breadcrumb(title=menu.title)
                if menu.title is not None and isinstance(menu.title, str)
                else None
            )
            children: "BreadcrumbList" = BreadcrumbList()
            for mi in menu.items:
                children.extend(cls._from_menu_item(mi))
            if parent_bc:
                parent_bc.children = children
                return BreadcrumbList((parent_bc,))
            else:
                return children
        elif isinstance(menu_item, ActionLink):
            try:
                to_full_name = menu_item.to_full_name
            except ValueError:
                raise ValueError(
                    "ActionLink {}: only component full_name is supported for "
                    "action_link 'to' parameter, when converting it to breadcrumb".format(
                        menu_item
                    )
                )
            try:
                title: Union[str, Callable[["jembe.Component"], str]] = menu_item.title
            except ValueError:
                title = lambda component: component.title
            return BreadcrumbList(
                (
                    Breadcrumb(
                        component_full_name=to_full_name,
                        component_init_params=menu_item.params,
                        title=title,
                    ),
                )
            )
        else:
            # ignore URL links
            return BreadcrumbList()


@dataclass
class BreadcrumbItem(JembeInitParamSupport):
    id: str
    title: str
    url: Optional[str]
    jrl: Optional[str]

    fresh: bool = field(init=False, default=False)

    @classmethod
    def dump_init_param(cls, value: "BreadcrumbItem") -> Any:
        return dict(
            id=value.id,
            title=value.title,
            url=value.url,
            jrl=value.jrl,
        )

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return BreadcrumbItem(
            id=value.get("id"),
            title=value.get("title"),
            url=value.get("url"),
            jrl=value.get("jrl"),
        )