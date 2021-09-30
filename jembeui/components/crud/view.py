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
from jembe import action
from flask_sqlalchemy import Model, SQLAlchemy
from .form import CFormBase
from ...lib import Form, Menu, Link


if TYPE_CHECKING:
    import jembe

__all__ = ("CViewRecord",)


class CViewRecord(CFormBase):
    class Config(CFormBase.Config):
        default_template_exp = "jembeui/{style}/components/crud/view.html"

        def __init__(
            self,
            form: "Form",
            get_record: Optional[
                Callable[["CViewRecord"], Union["Model", dict]]
            ] = None,
            menu: Optional[Union["Menu", Sequence[Union["Link", "Menu"]]]] = None,
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
            self.menu: "Menu" = (
                Menu()
                if menu is None
                else (Menu(menu) if not isinstance(menu, Menu) else menu)
            )
            super().__init__(
                form,
                get_record=get_record,
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
            self._record = _record
        self.form: Form = (
            self._config.form(data=self.record)
            if isinstance(self.record, dict)
            else self._config.form(obj=self.record)
        )
        self.form.set_readonly_all()
        self.form.mount(self)
        super().__init__()

    @action
    def cancel(self):
        self.emit("cancel", id=self.record.id, record=self.record)

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()
