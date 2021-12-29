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
import sqlalchemy as sa
from flask_sqlalchemy import Model, SQLAlchemy
from .form import CForm, cformbase_default_on_submit_exception
from ...lib import Form, Menu, ActionLink

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CCreateRecord",)


def default_on_submit(c: "jembeui.CCreateRecord", r: Union["Model", str]) -> Optional[bool]:
    c.jui_push_notification("Created sucessefuly", "success")
    return False


def default_on_invalid_form(c: "jembeui.CCreateRecord"):
    # TODO chek are they errors not associated with field and display it
    c.jui_push_notification("Form is invalid", "warn")


class CCreateRecord(CForm):
    class Config(CForm.Config):
        default_template_exp = "jembeui/{style}/components/crud/create.html"

        def __init__(
            self,
            form: "jembeui.Form",
            get_record: Optional[
                Callable[["jembeui.CFormBase"], Union["Model", dict]]
            ] = None,
            menu: Optional[
                Union["jembeui.Menu", Sequence[Union["jembeui.Link", "jembeui.Menu"]]]
            ] = None,
            on_submit: Optional[
                Callable[["jembeui.CFormBase", Union["Model", dict]], Optional[bool]]
            ] = default_on_submit,
            on_invalid_form: Optional[
                Callable[["jembeui.CFormBase"], None]
            ] = default_on_invalid_form,
            on_submit_exception: Optional[
                Callable[["jembeui.CFormBase", "Exception"], None]
            ] = cformbase_default_on_submit_exception,
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
            if menu is None:
                menu = Menu(
                    [
                        ActionLink("submit()", "Save", styling=dict(primary=True)),
                        ActionLink("cancel()", "Cancel"),
                    ]
                )
            super().__init__(
                form,
                get_record=get_record,
                menu=menu,
                on_submit=on_submit,
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
        form: Optional[Form] = None,
        modified_fields: Tuple[str, ...] = (),
    ):
        super().__init__(form=form)

    @property
    def is_form_modified(self) -> bool:
        return len(self.state.modified_fields) > 0

    @property
    def modified_form_fields(self) -> Optional[Sequence[str]]:
        return self.state.modified_fields
