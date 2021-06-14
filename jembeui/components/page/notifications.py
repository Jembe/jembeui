from typing import Dict, Optional, TYPE_CHECKING, Any
from dataclasses import dataclass, asdict
from uuid import uuid1

from ..component import Component
from jembe import config, listener, JembeInitParamSupport
from flask import current_app

if TYPE_CHECKING:
    from jembe import Event


__all__ = "CPageNotifications"


@dataclass
class PageNotification(JembeInitParamSupport):
    message: str
    level: str = "info"

    def __post_init__(self):
        if self.level not in ("info", "success", "warn", "error"):
            current_app.logger.warning(
                "PageNotification level '{}' is not valid. Valid levels are: info, success, warn and error".format(
                    self.level
                )
            )
            self.level = "error"

    @classmethod
    def dump_init_param(cls, value: "PageNotification") -> Any:
        # called to menu 
        return asdict(value)

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return (
            PageNotification(
                message=value.get("message"),
                level=value.get("level"),
            )
            if value is not None and bool(value)
            else None
        )

@config(Component.Config(changes_url=False))
class CPageNotifications(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/notifications.html"

    def __init__(
        self, notifications: Optional[Dict[str, PageNotification]] = None
    ) -> None:
        if notifications is not None:
            # remove notifications id where notification[id] == None
            self.state.notifications = {
                id: n for id, n in notifications.items() if n is not None 
            }
        else:
            self.state.notifications = dict()

        super().__init__()

    @listener(event="pushPageNotification")
    def on_push_notification(self, event: "Event"):
        level = event.params.get("level")
        message = event.params.get("message")
        notification = PageNotification(
            message=message if message is not None else "Undefined message",
            level=level if level is not None else "info",
        )
        self.state.notifications[str(uuid1())] = notification
