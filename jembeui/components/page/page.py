from typing import TYPE_CHECKING, Callable, Iterable, Optional, Union, Dict, Tuple
from jembe import listener
from ..component import Component
from .alerts import CPageAlerts
from .message import CPageMessage
from .system_error import CPageSystemError
from .head_tag import CPageHeadTag
from .action_confirmation import CPageActionConfirmation


if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CPage",)


class CPage(Component):
    """Default Page/Root Component

    Provide basic functionalities excapted for every application including:

    -  HTML HEAD tags display and update with (page_head_tag=CPageHeadTag).
        Including title and description;
    -  action progress bar;
    -  alerts (toasts) with (page_alerts=CPageAlerts);
    -  messages with (page_messages=CPageMessage);
    -  system errors with (page_system_error=CPageSystemError);
    """

    class Config(Component.Config):
        default_template: str = "/jembeui/components/page.html"

        def __init__(
            self,
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            # Add default page components
            efective_components = dict(
                page_head_tag=CPageHeadTag,
                page_alerts=CPageAlerts,
                page_message=CPageMessage,
                page_system_error=CPageSystemError,
                page_action_confirmation=CPageActionConfirmation,
            )
            if components:
                efective_components.update(components)
            super().__init__(
                title,
                template,
                efective_components,
                inject_into_components,
                redisplay,
                changes_url,
                url_query_params,
            )

    _config: Config

    def __init__(self, head_tags: Dict[str, str] = {}):
        """_summary_

        Args:
            head_tags (Dict[str, str], optional): Configure title and meta tags in HTML>HEAD.
                Exp: {"title":"My Project", "description":"..."}. Defaults to {}.
        """
        if head_tags == {}:
            self.state.head_tags = dict()

        super().__init__()

        # add title tag if does not exist
        if CPageHeadTag.TITLE not in self.state.head_tags:
            self.state.head_tags[CPageHeadTag.TITLE] = self.title
        self._head_tags_level: Dict[str, int] = dict()

    # listener for updating HTML tags in HEAD
    @listener(event="pushPageHeadTag")
    def on_push_page_head_tag(self, event: "jembe.Event"):
        """Update values of Head Tags

        Event Args:

            htype (str): value from CPageHeadTag.TYPES defines tag type
            content (str): content of the tag. Setting None for content will remove tag
        """
        self._update_head_tag(
            event.params.get("htype", None),
            event.params.get("content", None),
            event.source._config.hiearchy_level,
        )
        return False

    @listener(event="resetPageHeadTags")
    def on_resetPageHeadTags(self, event: "jembe.Event"):
        """Remove all current head tags and sets new values

        Event Args:
            tags (Dict[str,str]):Dict of new tags to set
        """
        level = event.source._config.hiearchy_level

        # create new tags
        new_tags: Dict[str, str] = event.params.get("tags", dict())
        if CPageHeadTag.TITLE not in new_tags:
            new_tags[CPageHeadTag.TITLE] = self.title

        new_tags = {k: v for k, v in new_tags.items() if k in CPageHeadTag.TYPES}

        # remove tag components
        for htype in self.state.head_tags.keys():
            if htype not in new_tags and level >= self._head_tags_level.get(htype, 0):
                self.remove_component("page_head_tag", htype)
                del self.state.head_tags[htype]
                self._head_tags_level[htype] = level

        for htype, content in new_tags.items():
            if level >= self._head_tags_level.get(htype, 0):
                self._update_head_tag(htype, content, level)

        return False

    def display(self) -> "jembe.DisplayResponse":
        for htype, content in self.state.head_tags.items():
            self.display_component("page_head_tag", htype, htype=htype, content=content)
        return super().display()

    def _update_head_tag(self, htype: str, content: str, level: int):
        """Update head tag if request is made from higher level than existin tag

        Using level, components deeper in hiearchy have priority on setting head tags.
        """
        if htype in CPageHeadTag.TYPES:
            if level >= self._head_tags_level.get(htype, 0):
                self._head_tags_level[htype] = level
                if content is None:
                    del self.state.head_tags[htype]
                    self.remove_component("page_head_tag", htype)
                else:
                    self.state.head_tags[htype] = content
                    self.display_component(
                        "page_head_tag", htype, htype=htype, content=content
                    )
                self._head_tags_level[htype] = level
