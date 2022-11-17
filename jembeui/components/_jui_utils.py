from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    import jembeui

__all__ = ("JuiUtils",)


class JuiUtils:
    """Helper methods for working with JembeUi page events"""

    def __init__(self, component: "jembeui.Component") -> None:
        self._component = component

    def push_page_message(self, title: str, message: str, variant: str = ""):
        """
        - title (Optional[str], optional): Title of the message box. Defaults to None.
        - message (Optional[str], optional): Actual message. Defaults to None.
        - mvariant (Optional[str], optional): Color varinat (error, warning, primary, etc.). Defaults to None.
        """
        self._component.emit(
            "pushPageMessage", title=title, message=message, variant=variant
        )

    def push_page_alert(self, message: str, level: str = "base"):
        from .page.alerts import CPageAlerts

        if level not in CPageAlerts.LEVELS:
            raise ValueError(
                f"Invalid alert level {level}. Valid levels are: {CPageAlerts.LEVELS}"
            )
        self._component.emit("pushPageAlert", message=message, level=level)

    def push_page_head_tag(self, tag: str, content: str):
        from .page.head_tag import CPageHeadTag

        if tag not in CPageHeadTag.TYPES:
            raise ValueError(f"Unsupported head type '{type}'!")
        self._component.emit("pushPageHeadTag", htype=tag, content=content)

    def push_page_title(self, title: str):
        from .page.head_tag import CPageHeadTag

        self.push_page_head_tag(CPageHeadTag.TITLE, title)

    def push_page_description(self, description: str):
        from .page.head_tag import CPageHeadTag

        self.push_page_head_tag(CPageHeadTag.DESCRIPTION, description)

    def reset_page_head_tags(self, tags: Dict[str, str]):
        self._component.emit("resetPageHeadTags", tags=tags)

    def ask_for_action_confirmation(
        self,
        action_name: str,
        title: str,
        question: str = "",
        action_params: Optional[dict] = None,
        confirmation_title: str = "Ok",
        is_danger: bool = False,
        danger_confirmation_phrase: Optional[str] = None,
    ):
        from .page.action_confirmation import Confirmation

        if action_params is None:
            action_params = dict(confirmed=True)

        self._component.emit(
            "askForActionConfirmation",
            confirmation=Confirmation(
                title=title,
                question=question,
                action_name=action_name,
                action_params=action_params,
                confirmation_title=confirmation_title,
                is_danger=is_danger,
                danger_confirmation_phrase=danger_confirmation_phrase,
            ),
        )

    def redisplay(self, *component_names):
        """Emit redisplay to named child components cousing them to redisplay itself
        if they already exist on the page"""
        if component_names:
            self._component.emit("redisplay").to(component_names)
        else:
            self._component.emit("redisplay")
