from typing import (
    TYPE_CHECKING,
    Optional,
    Callable,
    Sequence,
    Union,
    Dict,
    Iterable,
    Tuple,
    Any,
)
from jembe import NotFound, listener
from sqlalchemy.orm.scoping import scoped_session
from flask_sqlalchemy import Model

from ..component import Component
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ...lib import Form, Menu, JUIFieldMixin

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy

__all__ = ("CFormBase", "CForm")


class CFormBase(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/crud/form.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembe.Component"], Union["Model", dict]]
            ] = None,
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
            self.form = form
            self.get_record_callback = get_record
            # defult db can be useds when db is None
            if db is not None:
                self.db: "SQLAlchemy" = db
            else:
                self.db = get_jembeui().default_db
                if self.db is None:
                    raise JembeUIError(
                        "Either 'db' for CListRecords.Config or default_db"
                        " on JembeUI instance must be set"
                    )
            if components is None:
                components = {}
            for field in self.form():
                if isinstance(field, JUIFieldMixin):
                    components.update(field.jui_get_components())

            super().__init__(
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    def __init__(self):
        self._record: Union["Model", dict]
        super().__init__()

    @classmethod
    def load_init_param(
        cls, config: "jembe.ComponentConfig", name: str, value: Any
    ) -> Any:
        # if not overriden it fill use jembeui.lib.form.Form.load_init_param
        if name == "form":
            return config.form.load_init_param(value)
        return super().load_init_param(config, name, value)

    def get_record(self) -> Union["Model", dict]:
        if self._config.get_record_callback is None:
            raise JembeUIError(
                "You need to implement get_record method or to add config parameter get_record to component: {}".format(
                    self._config.full_name
                )
            )
        return self._config.get_record_callback(self)

    @property
    def record(self) -> Union["Model", dict]:
        try:
            return self._record
        except AttributeError:
            self._record = self.get_record()

        if self._record is None:
            raise NotFound()
        return self._record

    @property
    def session(self) -> "scoped_session":
        return self._config.db.session


class CForm(CFormBase):
    class Config(CFormBase.Config):
        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembe.Component"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
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
                db=db,
                title=title,
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        pass

    def inject_into(self, cconfig: "jembe.ComponentConfig") -> Dict[str, Any]:
        return {
            "_form": self.state.form,
        }

    def __init__(self, form: Optional[Form] = None):
        if self.state.form is None:
            self.state.form = (
                self._config.form(data=self.record)
                if isinstance(self.record, dict)
                else self._config.form(obj=self.record)
            )

        self.state.form.mount(self, "form")
        super().__init__()

    def hydrate(self):
        self.menu = self._config.menu.bind_to(self)
        return super().hydrate()

    @listener(event="update_form_field")
    def on_update_form_field(self, event: "jembe.Event"):
        field = getattr(self.state.form, event.params["name"])
        field.data = event.params["value"]
