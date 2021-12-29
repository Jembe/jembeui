from typing import Optional, TYPE_CHECKING
from ..component import Component
from jembe import config, listener, action

if TYPE_CHECKING:
    import jembe


__all__ = ("CPageNotice",)


@config(Component.Config(changes_url=False))
class CPageNotice(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/notice.html"

    _config: Config

    def __init__(self, title:Optional[str] = None, message: Optional[str] = None):
        super().__init__()

    @listener(event="pushPageNotice")
    def on_push_notice(self, event: "jembe.Event"):
        self.state.message = event.params.get("message")
        self.state.title = event.params.get("title")

    @action
    def cancel(self):
        self.state.message = None
        self.state.title = None
        return True
