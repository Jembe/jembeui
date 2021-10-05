from typing import TYPE_CHECKING, Optional, Callable, Union, Dict, Iterable, Tuple, Any
from sqlalchemy.orm.scoping import scoped_session
from ..component import Component
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ...lib import Form

if TYPE_CHECKING:
    import jembe
    import jembeui
    from flask_sqlalchemy import SQLAlchemy, Model

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
        record =  self._config.get_record_callback(self)
        print(self, record)
        return record

    @property
    def record(self) -> Union["Model", dict]:
        try:
            return self._record
        except AttributeError:
            self._record = self.get_record()
        return self._record

    @property
    def session(self) -> "scoped_session":
        return self._config.db.session


class CForm(CFormBase):
    class Config(CFormBase.Config):
        pass

    def __init__(self, form: Optional[Form] = None):
        if self.state.form is None:
            self.state.form = (
                self._config.form(data=self.record)
                if isinstance(self.record, dict)
                else self._config.form(obj=self.record)
            )

        self.state.form.mount(self)
        super().__init__()
