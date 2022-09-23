from typing import TYPE_CHECKING, Any, Optional, Dict
from dataclasses import dataclass, asdict
from uuid import uuid4
from flask import current_app
from jembe import JembeInitParamSupport, listener, config
from ..component import Component

if TYPE_CHECKING:
    import jembe

__all__ = ("CPageAlerts",)


@dataclass
class Alert(JembeInitParamSupport):
    message: str
    level: str = "base"

    def __post_init__(self):
        if self.level not in CPageAlerts.LEVELS:
            current_app.logger.warning(
                f"Alert level '{self.level}' is not valid. "
                f"Valid levels are: {CPageAlerts.LEVELS}"
            )
            self.level = "error"

    @classmethod
    def dump_init_param(cls, value: "Alert") -> Any:
        return asdict(value)

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return (
            Alert(
                message=value.get("message"),
                level=value.get("level"),
            )
            if value is not None and bool(value)
            else None
        )


@config(Component.Config(changes_url=False))
class CPageAlerts(Component):
    """Display page allerts at the bottom of the page

    listen for pushPageAlert event containg:

    - level (info, success, warn, error): message severety level
    - message: text to be displayed to user
    """

    class Config(Component.Config):
        default_template = "jembeui/components/page/alerts.html"

    _config: Config

    BASE = "base"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    LEVELS = [BASE, INFO, WARNING, ERROR, SUCCESS]

    def __init__(self, alerts: Dict[str, Optional[Alert]] = {}):
        """Adds alerts state param

        Args:
            alerts (Dict[str, Optional[Alert]], optional): List of alerts to be displayed. Defaults to {}.
        """
        if not alerts:
            self.state.alerts = {}
        else:
            # remove alert id where alert[id] is None
            self.state.alerts = {
                uid: alrt for uid, alrt in alerts.items() if alrt is not None
            }
        super().__init__()

    @listener(event="pushPageAlert")
    def on_push_page_alert(self, event: "jembe.Event"):
        """on event pushPageAlert display new alert"""
        level = event.params.get("level", self.INFO)
        message = event.params.get(
            "message", "Developer forgot to specify alert message."
        )
        self.state.alerts[str(uuid4())] = Alert(level=level, message=message)
