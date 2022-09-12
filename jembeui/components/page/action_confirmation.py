from typing import TYPE_CHECKING, Any, Optional
from dataclasses import dataclass, field, asdict

from ..component import Component
from jembe import config, listener, action, JembeInitParamSupport

if TYPE_CHECKING:
    import jembe


__all__ = ("CPageActionConfirmation",)


@dataclass
class Confirmation(JembeInitParamSupport):
    title: str
    question: str
    action_name: str
    action_params: dict = field(default_factory=dict)
    confirmation_title: str = "Ok"
    is_danger: bool = False
    # string that user should typein to confirm danger operation
    danger_confirmation_phrase: Optional[str] = None

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
                confirmation_title=value.get("confirmation_title"),
                is_danger=value.get("is_danger"),
            )
            if value is not None
            else None
        )


@config(Component.Config(changes_url=False))
class CPageActionConfirmation(Component):
    """Ask user to confirme action

    This is page component that opens modal with title
    and question for user.

    Becouse confirmation of action is common use case it is implemented
    on global component so we dont cluter subcomponent with logic for confirmation.

    Intented use of ActionConfirmation is to send it event with
    Confiramtion class where you specify question.
    Uppon user confirmation of action event will be emited that action is confirmed.
    """

    class Config(Component.Config):
        default_template = "/jembeui/components/page/action_confirmation.html"

    _config: Config

    def __init__(
        self,
        confirmation: Optional[Confirmation] = None,
        source: Optional[str] = None,
    ):
        super().__init__()

    @listener(event="askForActionConfirmation")
    def on_request_confirmation(self, event: "jembe.Event"):
        self.state.confirmation = (
            Confirmation(**event.confirmation)
            if isinstance(event.confirmation, dict)
            else event.confirmation
        )
        self.state.source = event.source_exec_name

    @action
    def confirm(self):
        self.emit(
            "userHasConfirmedTheAction",
            action_name=self.state.confirmation.action_name,
            action_params=self.state.confirmation.action_params,
        ).to(self.state.source)
        self.state.confirmation = None
        self.state.source = None

    @action
    def cancel(self):
        self.state.confirmation = None
        self.state.source = None
