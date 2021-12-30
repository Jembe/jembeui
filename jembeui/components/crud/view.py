from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    Callable,
    Iterable,
    Tuple,
    Dict,
    Sequence,
)
from flask_sqlalchemy import Model, SQLAlchemy
from .form import CFormBase
from ...lib import Menu


if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CViewRecord",)


class CViewRecord(CFormBase):
    class Config(CFormBase.Config):
        default_template_exp = "jembeui/{style}/components/crud/view.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembeui.CFormBase"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            on_submit_success: Optional[
                Callable[["jembeui.CFormBase", Union["Model", dict]], Optional[bool]]
            ] = None,
            on_invalid_form: Optional[Callable[["jembeui.CFormBase"], None]] = None,
            on_submit_exception: Optional[
                Callable[["jembeui.CFormBase", "Exception"], None]
            ] = None,
            on_cancel: Optional[Callable[["jembeui.CFormBase"], Optional[bool]]] = None,
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
            self.menu: "jembeui.Menu" = (
                Menu()
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            super().__init__(
                form,
                get_record=get_record,
                on_submit_success=on_submit_success,
                on_invalid_form=on_invalid_form,
                on_submit_exception=on_submit_exception,
                on_cancel=on_cancel,
                db=db,
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    def __init__(
        self,
        id: int,
        _record: Optional[Union[Model, dict]] = None,
    ):
        if _record is not None and (
            _record["id"] == id if isinstance(_record, dict) else _record.id == id
        ):
            self.record = _record
        self.form = (
            self._config.form(data=self.record, disabled=True)
            if isinstance(self.record, dict)
            else self._config.form(obj=self.record, disabled=True)
        )
        self.form.mount(self)
        super().__init__()

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()
