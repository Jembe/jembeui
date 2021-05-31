from typing import TYPE_CHECKING, Optional
from jembe.component_config import config
from ..component import Component
from jembe import listener
from flask import current_app

if TYPE_CHECKING:
    from jembe import Event

__all__ = ("CPageTitle",)


@config(Component.Config(changes_url=False))
class CPageTitle(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/title.html"

    def __init__(self, title: Optional[str] = None):
        super().__init__()

    @property
    def title(self) -> str:
        if self.state.title is None:
            return super().title
        return self.state.title

    @listener(event="setPageTitle")
    def on_set_page_title(self, event: "Event"):
        try:
            self.state.title = event.params["title"]
        except Exception as e:
            current_app.logger.warning(
                "setPageTitle event must have 'title' param set! ({event})".format(
                    event=event,
                )
            )
