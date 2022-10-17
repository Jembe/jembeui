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
from .form_adaptable import CFormAdaptable

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    import jembe
    import jembeui

__all__ = ("CViewRecordAdaptable",)


class CViewRecordAdaptable(CFormAdaptable):
    """Displayes Form that shows read only record from database"""

    # class Config(CFormAdaptable.Config):
    #     """Configures View Record component

    #     # TODO  copy from CFormAdaptable and add new stuff
    #     """

    #     def __init__(
    #         self,
    #         form: Type["jembeui.Form"],
    #         get_record: Optional[Callable[["jembeui.CFormAdaptable"], Union["Model", dict]]] = None,
    #         menu: Optional[
    #             Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
    #         ] = None,
    #         form_state_name: str = "form",
    #         db: Optional["SQLAlchemy"] = None,
    #         title: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
    #         template: Optional[Union[str, Iterable[str]]] = None,
    #         components: Optional[Dict[str, "jembe.ComponentRef"]] = None,
    #         inject_into_components: Optional[
    #             Callable[["jembe.Component", "jembe.ComponentConfig"], dict]
    #         ] = None,
    #         redisplay: Tuple["jembe.RedisplayFlag", ...] = (),
    #         changes_url: bool = True,
    #         url_query_params: Optional[Dict[str, str]] = None,
    #     ):
    #         super().__init__(
    #             form=form,
    #             get_record=get_record,
    #             menu=[] if menu is None else menu,
    #             form_state_name=form_state_name,
    #             db=db,
    #             title=title,
    #             template=template,
    #             components=components,
    #             inject_into_components=inject_into_components,
    #             redisplay=redisplay,
    #             changes_url=changes_url,
    #             url_query_params=url_query_params,
    #         )

    # _config: Config

    def __init__(self, record_id: int, _record: Optional[Union[Model, dict]] = None):

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
