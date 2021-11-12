from jembe import File
import wtforms


__all__ = ("FileField",)


class FileField(wtforms.FileField):
    # usefull to recognise jembeui FileField when
    # rendering multiple fields in loop inside jinja2 template
    is_jembeui_file_field = True

    def process_data(self, value):
        if value is None:
            self.data = None
        elif isinstance(value, File):
            self.data = value
        else:
            self.data = File.load_init_param(value)
