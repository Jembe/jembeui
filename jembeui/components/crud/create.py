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
from .form import CForm
from ...lib import Form, Menu, ActionLink

if TYPE_CHECKING:
    import jembe
    import jembeui

__all__ = ("CCreateRecord",)


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
            redisplay_on_submit: bool = False,
            redisplay_on_cancel: bool = False,
            grab_focus_on_display: bool = True,
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
                redisplay_on_submit=redisplay_on_submit,
                redisplay_on_cancel=redisplay_on_cancel,
                grab_focus_on_display=grab_focus_on_display,
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

    def on_submit_success(
        self, submited_record: Optional[Union["Model", dict]]
    ) -> Optional[bool]:
        self.state.modified_fields = ()
        self.jui_push_notification("Created sucessefuly", "success")
        return super().on_submit_success(submited_record)

    def on_cancel(self) -> Optional[bool]:
        self.state.modified_fields = ()
        return super().on_cancel()

    def on_invalid_form(self):
        self.jui_push_notification("Form is invalid", "warn")
        return super().on_invalid_form()
