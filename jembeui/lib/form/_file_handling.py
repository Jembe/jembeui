from typing import TYPE_CHECKING, Optional, Union
import jembeui

if TYPE_CHECKING:
    from flask_sqlalchemy import Model

all = ("SupportFileHandlingMixin",)


class SupportFileHandlingMixin:
    """Add support for default file upload handling when form is changed, canceled and submited"""

    def mount(
        self, cform: "jembeui.CForm", form_state_name: Optional[str] = None
    ) -> "jembeui.Form":
        for field in self:  # type:ignore
            if isinstance(field, jembeui.FileField):
                if field.data and field.data.is_just_uploaded():
                    # if file is just uploaded and it is valid file
                    # move it to temp storage
                    # otherwise remove file from disk and set it to None
                    if field.validate(self):
                        field.data.move_to_temp()
                    else:
                        field.data.remove()
                        field.data = None
                # remove previous field value (file) if file is in temp storage
                # when changing upload file without submit
                # to remove changed file from disk
                if form_state_name and cform.previous_state:
                    previous_form_field = getattr(
                        cform.previous_state[form_state_name], field.name
                    )
                    if (
                        previous_form_field
                        and previous_form_field.data
                        and previous_form_field.data.in_temp_storage()
                        and previous_form_field.data != field.data
                    ):
                        previous_form_field.data.remove()
        return super().mount(cform)  # type:ignore

    def cancel(self, record: Union["Model", dict]) -> Optional[bool]:
        state_changed = False
        for field in self:  # type:ignore
            if isinstance(field, jembeui.FileField):
                # if file field is changed before canceling form
                # remove new file from server
                record_field = (
                    record[field.name]
                    if isinstance(record, dict)
                    else getattr(record, field.name)
                )
                if field.data and (
                    field.data.in_temp_storage() or field.data != record_field
                ):
                    field.data.remove()
                    field.data = None
                    state_changed = True
        super().cancel(record)  # type:ignore
        return False if state_changed else None

    def submit(self, record: Union["Model", dict]) -> Union["Model", dict]:
        for field in self:  # type:ignore
            if isinstance(field, jembeui.FileField):
                if field.data and field.data.in_temp_storage():
                    # move photo in public storage for permanent keep
                    field.data.move_to_public()
                if record:
                    if isinstance(record, dict):
                        if record[field.name] and record[field.name] != field.data:
                            # delete old photo when it's replaced with new one
                            record[field.name].remove()
                            record[field.name] = None
                    else:
                        record_field = getattr(record, field.name)
                        if record_field and record_field != field.data:
                            # delete old photo when it's replaced with new one
                            record_field.remove()
                            record_field = None
        return super().submit(record)  # type:ignore
