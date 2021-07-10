from typing import (
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
from jembe import JembeInitParamSupport, listener
from ..component import Component

if TYPE_CHECKING:
    import jembe
    from jembeui import Menu


__all__ = ("Bradcrumb", "BreadcrumbGroup", "breadcrums_from_menu", "CBreadcrumb")


def _get_default_breadcrumb_title(component: "jembe.Component") -> str:
    """Returns default breadcrum title for the component"""
    if isinstance(component, Component):
        return component.title
    return component._config.name


class Breadcrumb:
    def __init__(
        self,
        component_full_name: str,
        title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
    ) -> None:
        self._title: Union[str, Callable[["jembe.Component"], str]] = (
            title if title is not None else _get_default_breadcrumb_title
        )
        self.full_name = component_full_name

        self._binded_to: Optional["jembe.Component"] = None
        super().__init__()

    def bind_to(self, component: "jembe.Component") -> "Breadcrumb":
        bc = Breadcrumb(self.full_name, self._title)
        bc._binded_to = component
        return bc

    @property
    def title(self) -> str:
        if self._binded_to is None:
            raise ValueError(
                "Breadcrumb must be binded to component before accessing its title"
            )
        if isinstance(self._title, str):
            return self._title
        return self._title(self.bind_to)

    @property
    def url(self) -> str:
        if self._binded_to is None:
            raise ValueError(
                "Breadcrumb must be binded to component before accessing its url"
            )

        return self._binded_to.url

    @property
    def jrl(self) -> str:
        if self._binded_to is None:
            raise ValueError(
                "Breadcrumb must be binded to component before accessing its jrl"
            )
        return self._binded_to.jrl

    @property
    def bclink(self) -> "BreadcrumbLink":
        return BreadcrumbLink(
            self.full_name,
            self.title,
            self.url,
            self.jrl
        )


class BreadcrumbGroup:
    def __init__(self, title: str, *full_names: str):
        self.title = title
        self.full_names: List[str] = list(full_names)

        super().__init__()


def breadcrumbs_from_menu(
    cls, menu: "Menu"
) -> Sequence[Union["Breadcrumb", "BreadcrumbGroup"]]:
    raise NotImplementedError()


class BreadcrumbLink(JembeInitParamSupport):
    """Represents rendered breadcrumb link, (resolved breacrumb class instance)"""
    def __init__(self, full_name: str, title: str, url: str, jrl: str) -> None:
        self.full_name = full_name
        self.title = title
        self.url = url
        self.jrl = jrl


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
            breadcrums: Sequence[Union["Breadcrumb", "BreadcrumbGroup"]],
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

    def __init__(self, bcs: Tuple[BreadcrumbLink, ...] = ()):
        super().__init__()

    @listener(event="_display")
    def on_component_display(self, event: "jembe.Event"):
        # update self.state.bcs remove all bcs after event.source_full_name
        # TODO check if event.source_full_name exist in self._config.breadcrumbs if so:
        bcs_new = []
        new_bc = BreadcrumbLink(event.source_full_name) # look at _config.breadcrumbs and get new_bc 
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
        elif len(bcs_new)>0 and self._is_parent(bcs_new[-1].full_name, new_bc.full_name):
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
