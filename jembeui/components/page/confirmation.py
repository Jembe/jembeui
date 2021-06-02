from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field, asdict

from ..component import Component
from jembe import config, listener, action, JembeInitParamSupport

if TYPE_CHECKING:
    from jembe import Event


__all__ = "CActionConfirmationDialog"


@dataclass
class Confirmation(JembeInitParamSupport):
    title: str
    question: str
    action_name: str
    action_params: dict = field(default_factory=dict)

    @classmethod
    def dump_init_param(cls, value: "Confirmation") -> Any:
        return asdict(value)

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return (
            Confirmation(
                title=value.get("title"),
                question=value.get("question"),
                action_name=value.get("action_name"),
                action_params=value.get("action_params"),
            )
            if value is not None
            else None
        )


@config(Component.Config(changes_url=False))
class CActionConfirmationDialog(Component):
    class Config(Component.Config):
        default_template_exp = (
            "jembeui/{style}/components/page/action_confirmation_dialog.html"
        )

    def __init__(
        self, confirmation: Optional[Confirmation] = None, source: Optional[str] = None
    ):
        super().__init__()

    @listener(event="requestActionConfirmation")
    def on_request_confirmation(self, event: "Event"):
        self.state.confirmation = event.confirmation
        self.state.source = event.source_exec_name

    @action
    def confirm(self):
        self.emit(
            "actionConfirmed",
            action_name=self.state.confirmation.action_name,
            action_params=self.state.confirmation.action_params,
        ).to(self.state.source)
        self.state.confirmation = None
        self.state.source = None

    @action
    def cancel(self):
        self.state.confirmation = None
        self.state.source = None
