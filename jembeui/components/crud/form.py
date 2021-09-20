from typing import TYPE_CHECKING, Optional, Callable, Union, Dict, Iterable, Tuple, Any
from jembe import run_only_once
from sqlalchemy.orm.scoping import scoped_session
from ..component import Component
from ...helpers import get_jembeui
from ...exceptions import JembeUIError
from ...lib import Form

if TYPE_CHECKING:
    import jembe
    from jembe import DisplayResponse
    from flask_sqlalchemy import SQLAlchemy, Model

__all__ = ("CForm",)


class CForm(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/crud/form.html"

        def __init__(
            self,
            form: "Form",
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

    def __init__(self, form: Optional[Form] = None):
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

    @run_only_once
    def mount(self):
        if self.state.form is None:
            self.state.form = (
                self._config.form(data=self.record)
                if isinstance(self.record, dict)
                else self._config.form(obj=self.record)
            )

        self.state.form.mount(self)

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
        return self._record

    def display(self) -> "DisplayResponse":
        self.mount()
        return super().display()

    @property
    def session(self) -> "scoped_session":
        return self._config.db.session

    # def do_submit_form(self)->Tuple[bool,Optional[str]]:
    #     """
    #         Returns (true, None) if submit is sucessfull
    #         Otherwise returns (False, "Error message") when submit is
    #         unsucessfull
    #     """
    #     raise NotImplementedError()
    #     self.mount()
    #     if self.state.form.validate():
    #         self.state.form.submit(self.record)
    #     return (False, None)

    # def do_cancel_form(self):
    #     self.mount()
    #     self.state.form.cancel(self.record)
    #     raise NotImplementedError()
