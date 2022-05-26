from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field, asdict

from ..component import Component
from jembe import config, listener, action, JembeInitParamSupport

if TYPE_CHECKING:
    import jembe


__all__ = "CActionConfirmationDialog"


@dataclass
class Confirmation(JembeInitParamSupport):
    title: str
    question: str
    action_name: str
    action_params: dict = field(default_factory=dict)
    confirm_title: str = "OK"
    danger: bool = False
    danger_confirm_text: Optional[str] = None

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
                confirm_title=value.get("confirm_title"),
                danger=value.get("danger"),
                danger_confirm_text=value.get("danger_confirm_text"),
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
    def on_request_confirmation(self, event: "jembe.Event"):
        self.state.confirmation = event.confirmation
        self.state.source = event.source_exec_name

    @action
    def confirm(self, danger_confirm_text: Optional[str] = None):
        if (
            self.state.confirmation.danger_confirm_text is not None
            and danger_confirm_text != self.state.confirmation.danger_confirm_text
        ):
            self.jui_push_notification("Invalid text entered for action confirmation!", "warn")
        else:
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
