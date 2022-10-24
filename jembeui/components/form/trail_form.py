from dataclasses import asdict
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)
from flask_sqlalchemy import Model
from jembe.common import dataclass_from_dict
from jembe import IsDataclass, NotFound, action
from jembeui.exceptions import JembeUIError
from ...includes.form import Form
from .form import CForm

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CTrailUpdateForm", "CTrailViewForm")


class CTrailFormBase(CForm):
    class Config(CForm.Config):
        default_template: str = "jembeui/components/form/trail_form.html"
        def __init__(
            self,
            form: Type["jembeui.Form"],
            trail_form_dataclass: Type[IsDataclass],
            grab_focus: bool = True,
            confirm_cancel: bool = True,
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            form_state_name: str = "form",
            db: Optional["SQLAlchemy"] = None,
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
            self.trail_form_dataclass = trail_form_dataclass
            self.is_trail_form = True
            super().__init__(
                form,
                None,
                [],
                grab_focus,
                confirm_cancel,
                redisplay_on_submit,
                redisplay_on_cancel,
                form_state_name,
                db,
                title,
                template,
                components,
                inject_into_components,
                redisplay,
                changes_url,
                url_query_params,
            )

    _conig: Config

    @classmethod
    def load_init_param(
        cls, config: "jembe.ComponentConfig", name: str, value: Any
    ) -> Any:
        if name == "record":
            if value is None:
                return None
            return dataclass_from_dict(config.trail_form_dataclass, value)  # TODO
        return super().load_init_param(config, name, value)

    @action
    def submit(self):
        """Submit form changes"""
        if self.form.get_form_style().disabled:
            raise JembeUIError("Can't submit disabled form")

        if self.form.validate():
            try:
                self.before_form_submit()

                # submit form
                submited_record = self.form.submit(self.record)
                self.record = submited_record

                # emit submit event
                self.emit(
                    "updateWDB",
                    operation="update",
                    record=submited_record,
                    uid=self.key,
                )

                return self.on_form_submited(submited_record)
            except Exception as error:
                self.on_form_submit_exception(error)
        else:
            self.on_form_invalid()

        return True


class CTrailUpdateForm(CTrailFormBase):
    def __init__(
        self,
        record: Optional[IsDataclass] = None,
        form: Optional[Form] = None,
        modified_fields: Tuple[str, ...] = (),
    ):
        if record is None:
            raise NotFound()
        self.record = self.state.record
        if self.previous_state and self.previous_state.record != self.state.record:
            del self.form
        super().__init__()

    def push_page_alert_on_form_submit(self):
        """No alert on submit"""

class CTrailViewForm(CTrailFormBase):
    class Config(CTrailFormBase.Config):
        def __init__(
            self,
            form: Type["jembeui.Form"],
            trail_form_dataclass: Type[IsDataclass],
            form_state_name: str = "form",
            db: Optional["SQLAlchemy"] = None,
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
            super().__init__(
                form,
                trail_form_dataclass,
                False,
                False,
                False,
                False,
                form_state_name,
                db,
                title,
                template,
                components,
                inject_into_components,
                redisplay,
                changes_url,
                url_query_params,
            )

    _config: Config

    def __init__(
        self,
        record: Optional[IsDataclass] = None,
    ):
        if record is None:
            raise NotFound()
        self.record = self.state.record
        self.form = self._config.form(data=asdict(self.record), disabled=True)
        super().__init__()
