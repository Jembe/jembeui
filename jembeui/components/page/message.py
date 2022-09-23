from typing import TYPE_CHECKING, Optional
from jembe import config, listener, action
from ..component import Component


if TYPE_CHECKING:
    import jembe

__all__ = ("CPageMessage",)


@config(Component.Config(changes_url=False))
class CPageMessage(Component):
    """Displays message to user that he needs to confirm

    listen to pushPageMessage event with parameters:

    - title: title
    - message: textual message to be displayed to user
    """

    class Config(Component.Config):
        default_template = "jembeui/components/page/message.html"

    _config: Config

    def __init__(self, title: Optional[str] = None, message: Optional[str] = None):
        """Defines component state params

        title (Optional[str], optional): Title of the message box. Defaults to None.
        message (Optional[str], optional): Actual message. Defaults to None.

        when title and message are None message box is hidden
        """
        super().__init__()

    @listener(event="pushPageMessage")
    def on_push_message(self, event: "jembe.Event"):
        """Display message on pushPageMessage event"""
        self.state.title = event.params.get("title", "Message")
        self.state.message = event.params.get("message", "")

    @action
    def cancel(self):
        """Close the message box and remove message"""
        self.state.message = None
        self.state.title = None
