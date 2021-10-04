from typing import (
    TYPE_CHECKING,
    List,
    Sequence,
    Callable,
    Dict,
    Iterable,
    Optional,
    Tuple,
    Union,
)
from jembe import listener
from ..component import Component
from ...lib import Breadcrumb, BreadcrumbItem

if TYPE_CHECKING:
    import jembe
    import jembeui


__all__ = (
    "CBreadcrumb",
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

        def __init__(
            self,
            breadcrumbs: Sequence["jembeui.Breadcrumb"],
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
            breadcrumbs: Sequence["jembeui.Breadcrumb"],
        ) -> Dict[str, "jembeui.Breadcrumb"]:
            flatten: Dict[str, Breadcrumb] = dict()
            for bc in breadcrumbs:
                flatten[bc.id] = bc
                flatten.update(self._flatten_breadcrumbs(bc.children))
            return flatten

        def is_parent_breadcrumbitem(
            self, bitem1: BreadcrumbItem, bitem2: BreadcrumbItem
        ) -> bool:
            """Returns true if bitem1 is parent of bitem2"""
            try:
                return self.is_parent_breadcrumb(
                    self.breadcrumbs_flat[bitem1.id],
                    self.breadcrumbs_flat[bitem2.id],
                )
            except KeyError:
                return False

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

        new_bitem = self._config.breadcrumbs_mapping[
            event.source_full_name
        ].get_breadcrumb_item(self, event.source)
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
                non_links.append(bdef.parent.get_breadcrumb_item(self))
                if bdef.parent.parent and not bdef.parent.parent.is_link:
                    non_links.append(bdef.parent.parent.get_breadcrumb_item(self))
                    if (
                        bdef.parent.parent.parent
                        and not bdef.parent.parent.parent.is_link
                    ):
                        non_links.append(
                            bdef.parent.parent.parent.get_breadcrumb_item(self)
                        )
                bitems_new_ext.extend(reversed(non_links))
            bitems_new_ext.append(bitem)
        self.state.bitems = tuple(bitems_new_ext)
