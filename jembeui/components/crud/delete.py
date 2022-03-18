from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    Callable,
    Iterable,
    Tuple,
    Dict,
)
import sqlalchemy as sa
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm.scoping import scoped_session
from flask import current_app
from jembe import action, NotFound
from ..component import Component
from ...helpers import get_jembeui
from ...exceptions import JembeUIError

if TYPE_CHECKING:
    import jembeui
    import jembe

__all__ = ("CDeleteRecord",)


class CDeleteRecord(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/crud/delete.html"

        def __init__(
            self,
            get_record: Optional[
                Callable[["jembeui.CDeleteRecord"], Union["Model", dict]]
            ] = None,
            db: Optional["SQLAlchemy"] = None,
            title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
            changes_url: bool = False,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
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

    def __init__(
        self,
        id: int,
        _record: Optional[Union[Model, dict]] = None,
    ):
        if _record is not None and (
            _record["id"] == id if isinstance(_record, dict) else _record.id == id
        ):
            self._record = _record
        super().__init__()

    @action
    def submit(self) -> Optional[bool]:
        try:
            self.session.delete(self.record)
            self.session.commit()
            self.emit(
                "submit",
                record=self.record,
                record_id=(
                    self.record.get("id", None)
                    if isinstance(self.record, dict)
                    else getattr(self.record, "id", None)
                ),
            )
            return self.on_submit_success()
        except Exception as error:
            self.on_submit_exception(error)
            if current_app.debug or current_app.testing:
                import traceback

                traceback.print_exc()
        self.session.rollback()
        return True

    def on_submit_success(self):
        self.push_notification_on_submit()
        return None

    def on_submit_exception(self, error: Exception):
        if isinstance(error, sa.exc.SQLAlchemyError):
            self.jui_push_notification(
                str(getattr(error, "orig", error))
                if isinstance(error, sa.exc.SQLAlchemyError)
                else str(error),
                "error",
            )
        elif isinstance(error, ValueError):
            self.jui_push_notification(str(error), "warn")
        else:
            self.jui_push_notification(str(error), "error")

    @action
    def cancel(self):
        self.on_cancel()
        self.emit(
            "cancel",
            record=self.record,
            record_id=(
                self.record.get("id", None)
                if isinstance(self.record, dict)
                else getattr(self.record, "id", None)
            ),
        )

    def on_cancel(self) -> Optional[bool]:
        self.push_notification_on_cancel()
        return None

    def push_notification_on_submit(self):
        self.jui_push_notification("{} deleted.".format(self.title), "success")

    def push_notification_on_cancel(self):
        pass

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
