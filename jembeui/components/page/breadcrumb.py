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
from ..component import Component

if TYPE_CHECKING:
    import jembe
    from jembeui import Menu


__all__ = ("Bradcrumb", "CBreadcrumb")


class Breadcrumb:
    title: str
    is_link: bool = True
    is_factory: bool = False
    exec_name: str
    grouped_exec_names: List[str]

    @classmethod
    def group(cls, title: str, *exec_names: str) -> "Breadcrumb":
        raise NotImplementedError()

    @classmethod
    def from_menu(cls, menu: "Menu") -> Sequence["Breadcrumb"]:
        raise NotImplementedError()

    @classmethod
    def factory_ref(cls, name:str)-> "Breadcrumb":
        """
        Mark breadcrumb as factory reference.
        Used to signal parent component to replace this reference
        with actual breadcrumbs dynamicaly generated.

        Usefull to signal Page component to import main_menu 
        components into Breadcrumbs
        """
        raise NotImplementedError()


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
            breadcrums: Sequence[Breadcrumb],
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
            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        pass
