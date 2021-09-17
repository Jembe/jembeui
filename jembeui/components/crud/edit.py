from typing import TYPE_CHECKING, Optional, Union, Callable, Iterable, Tuple, Dict
from .form import CForm
from jembe import action
import sqlalchemy as sa

if TYPE_CHECKING:
    import jembe
    from ...lib import Form
    from flask_sqlalchemy import Model, SQLAlchemy

__all__ = ("CEdit",)


class CEditRecord(CForm):
    class Config(CForm.Config):
        def __init__(
            self,
            form: "Form",
            get_record: Optional[
                Callable[["jembe.Component"], Union["Model", dict]]
            ] = None,
            redisplay_on_submit: bool = False,
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
        form: Optional["Form"] = None,
        is_modified: bool = False,
        _record: Optional[Union["Model", dict]] = None,
    ):
        if _record is not None and (
            _record["id"] == id if isinstance(_record, dict) else _record.id == id
        ):
            self._record = _record
        super().__init__(form=form)

    @action
    def submit(self) -> Optional[bool]:
        self.mount()
        if self.state.form.validate():
            try:
                submited_record = self.state.form.submit(self.record)
                self.session.commit()
                self.emit(
                    "submit",
                    record=submited_record,
                    record_id=submited_record["id"]
                    if isinstance(submited_record, dict)
                    else submited_record.id,
                )
                # TODO info notification if needed formated as needed
            except (sa.exc.SQLAlchemyError) as error:
                # TODO error notificationself.
                pass
        self.session.roolback()
        return True
