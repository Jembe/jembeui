from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Sequence,
    Set,
    Callable,
    Dict,
    Iterable,
    Optional,
    Tuple,
    Union,
)
from uuid import uuid3, NAMESPACE_DNS
from dataclasses import dataclass, field
from jembe import JembeInitParamSupport, listener
from ..component import Component
from ..menu import ActionLink, Menu

if TYPE_CHECKING:
    import jembe
    from jembeui import Link


__all__ = (
    "Breadcrumb",
    "CBreadcrumb",
)


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

        self._parent: Optional[Breadcrumb] = None
        self._all_parents_ids: Set[str] = set()
        self._all_childrens_ids: Set[str] = set()

        self.id: str = self._calc_id()

        if children is not None:
            self.children = children

        if self.component_full_name is None and not isinstance(self.title, str):
            raise ValueError(
                "Breadcrumb without component_full_name, can't have callable title!"
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
    def children(self) -> Sequence["Breadcrumb"]:
        return self._children

    @children.setter
    def children(self, children: Sequence["Breadcrumb"]):
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

    def get_item(
        self,
        from_component: "jembe.Component",
        to_component: Optional["jembe.Component"] = None,
    ) -> "BreadcrumbItem":
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
    ) -> Sequence["Breadcrumb"]:
        if menu is None:
            return list()
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
            return [home]

    @classmethod
    def _from_menu_item(cls, menu_item: Union[Menu, "Link"]) -> Sequence["Breadcrumb"]:
        if isinstance(menu_item, Menu):
            menu = menu_item
            parent_bc: Optional["Breadcrumb"] = (
                Breadcrumb(title=menu.title)
                if menu.title is not None and isinstance(menu.title, str)
                else None
            )
            children: List["Breadcrumb"] = list()
            for mi in menu.items:
                children.extend(cls._from_menu_item(mi))
            if parent_bc:
                parent_bc.children = children
                return [parent_bc]
            else:
                return children
        elif isinstance(menu_item, ActionLink):
            # TODO remove this tight dependency
            if not isinstance(menu_item._to, str) or menu_item._to.endswith("()"):
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
            return [
                Breadcrumb(
                    component_full_name=menu_item._to,
                    component_init_params=menu_item.action_params,
                    title=title,
                )
            ]
        else:
            # ignore URL links
            return []

    def find_by_component(self, component_full_name: str) -> "Breadcrumb":
        """
        Returns first breadcrumb in hiearachy with matching component_full_name

        Raises ValueError if matching breadcrumb does not exist.
        """
        # TODO
        raise NotImplementedError()

    def find_by_title(self, title: str) -> "Breadcrumb":
        """
        Returns first breadcrumb in hiearachy with matching title and component_full_name is None.

        Raises ValueError if matching breadcrumb does not exist.
        """
        # TODO
        raise NotImplementedError()


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
            breadcrumbs: Sequence["Breadcrumb"],
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
            self.breadcrumbs = breadcrumbs
            self.breadcrumbs_flat: Dict[str, Breadcrumb] = self._flatten_breadcrumbs(
                breadcrumbs
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

        def _flatten_breadcrumbs(
            self,
            breadcrumbs: Sequence[Breadcrumb],
        ) -> Dict[str, Breadcrumb]:
            flatten: Dict[str, Breadcrumb] = dict()
            for bc in breadcrumbs:
                flatten[bc.id] = bc
                flatten.update(self._flatten_breadcrumbs(bc.children))
            return flatten

        def is_parent_breadcrumbitem(
            self, bitem1: BreadcrumbItem, bitem2: BreadcrumbItem
        ) -> bool:
            """Returns true if bitem1 is parent of bitem2"""
            return self.is_parent_breadcrumb(
                self.breadcrumbs_flat[bitem1.id],
                self.breadcrumbs_flat[bitem2.id],
            )

        def is_parent_breadcrumb(self, b1: Breadcrumb, b2: Breadcrumb) -> bool:
            """Returns true if b1 is parent of b2"""
            if b2.parent is None:
                return False
            if b2.parent.id == b1.id:
                return True
            return self.is_parent_breadcrumb(b1, b2.parent)

    _config: Config

    def __init__(self, bitems: Tuple[BreadcrumbItem, ...] = ()):
        super().__init__()

    @listener(event="_display")
    def on_component_display(self, event: "jembe.Event"):
        if event.source_full_name not in self._config.breadcrumbs_mapping:
            # component that has been displayed does not have associated breadcrumb
            return

        new_bitem = self._config.breadcrumbs_mapping[event.source_full_name].get_item(
            self, event.source
        )
        new_bitem.fresh = True
        bitems_new: List[BreadcrumbItem] = []

        if len(self.state.bitems) == 0:
            bitems_new = [new_bitem]
        elif self._config.is_parent_breadcrumbitem(new_bitem, self.state.bitems[0]):
            # first item in bitems is child of new_bitem
            bitems_new = [new_bitem]
            bitems_new.extend(
                [
                    bi
                    for bi in self.state.bitems
                    if self._config.breadcrumbs_flat[bi.id].is_link
                ]
            )
        elif self._config.is_parent_breadcrumbitem(self.state.bitems[-1], new_bitem):
            # last item in bitems is parent of new_bitem
            bitems_new.extend(
                [
                    bi
                    for bi in self.state.bitems
                    if self._config.breadcrumbs_flat[bi.id].is_link
                ]
            )
            bitems_new.append(new_bitem)
        else:
            # find index of same item in bitems
            same_index: Optional[int] = None
            parent_index: Optional[int] = None
            last_fresh_index: Optional[int] = None
            for index, bi in enumerate(self.state.bitems):
                if bi.id == new_bitem.id:
                    same_index = index
                elif self._config.is_parent_breadcrumbitem(bi, new_bitem):
                    parent_index = index
                if bi.fresh:
                    last_fresh_index = index

            if same_index is not None:
                # replace same element and add all elements after it which
                # are fresh or behind the fresh ones
                bitems_new.extend(
                    [
                        bi
                        for bi in self.state.bitems[:same_index]
                        if self._config.breadcrumbs_flat[bi.id].is_link
                    ]
                )
                bitems_new.append(new_bitem)
                if last_fresh_index is not None:
                    bitems_new.extend(
                        [
                            bi
                            for bi in self.state.bitems[
                                same_index + 1 : last_fresh_index + 1
                            ]
                            if self._config.breadcrumbs_flat[bi.id].is_link
                        ]
                    )
            elif parent_index is not None:
                # add new bitem after its parent and dich all other that
                # was prevously after the parent
                bitems_new.extend(
                    [
                        bi
                        for bi in self.state.bitems[: parent_index + 1]
                        if self._config.breadcrumbs_flat[bi.id].is_link
                    ]
                )
                bitems_new.append(new_bitem)
            else:
                # new bitem is out of existing breadcrumb context/tree
                if last_fresh_index is not None:
                    # dich new one if there are fresh ones in existing breadcrumb
                    bitems_new = [
                        bi
                        for bi in self.state.bitems
                        if self._config.breadcrumbs_flat[bi.id].is_link
                    ]
                else:
                    # start new breadcrumb if old one does not have fresh ones
                    bitems_new = [new_bitem]

        # add non link breadcrumbs (up to max tree consecutive non link)
        bitems_new_ext: List[BreadcrumbItem] = list()
        for bitem in bitems_new:
            bdef = self._config.breadcrumbs_flat[bitem.id]
            if bdef.parent and not bdef.parent.is_link:
                # support nesting non link breadcrumb witout recursion
                # (bad programing but i dont care)
                non_links = []
                non_links.append(bdef.parent.get_item(self))
                if bdef.parent.parent and not bdef.parent.parent.is_link:
                    non_links.append(bdef.parent.parent.get_item(self))
                    if (
                        bdef.parent.parent.parent
                        and not bdef.parent.parent.parent.is_link
                    ):
                        non_links.append(bdef.parent.parent.parent.get_item(self))
                bitems_new_ext.extend(reversed(non_links))
            bitems_new_ext.append(bitem)
        self.state.bitems = tuple(bitems_new_ext)
