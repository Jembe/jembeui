from typing import (
    TYPE_CHECKING,
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
from .form import CForm, WDB

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    import jembe
    import jembeui

__all__ = ("CViewRecord",)


class CViewRecord(CForm):
    """Displayes Form that shows read only record from database"""

    class Config(CForm.Config):
        """Configures View Record component

        Removes menu
        """

        def __init__(
            self,
            form: Type["jembeui.Form"],
            get_record: Optional[
                Callable[["jembeui.CForm"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = [],
            grab_focus: bool = False,
            confirm_cancel: bool = False,
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
            super().__init__(
                form,
                get_record,
                menu,
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

        def get_trail_form_component(self, tfc: "jembeui.TrailFormConfig") -> "jembe.ComponentRef":
            from .trail_form import CTrailViewForm

            return (
                CTrailViewForm,
                CTrailViewForm.Config(
                    form=tfc.form,
                    trail_form_dataclass=tfc.dataclass
                ),
            )

    _config: Config

    def __init__(
        self,
        record_id: int,
        _record: Optional[Union[Model, dict]] = None,
        wdb: Optional[WDB] = None
    ):
        if _record is not None and (
            _record["id"] == record_id
            if isinstance(_record, dict)
            else _record.id == record_id
        ):
            self.record = _record

        self.form = (
            self._config.form(data=self.record, disabled=True)
            if isinstance(self.record, dict)
            else self._config.form(obj=self.record, disabled=True)
        )
        self.form.mount(self)
        super().__init__()
