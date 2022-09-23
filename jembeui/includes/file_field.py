from jembe import File
import wtforms as wtf


__all__ = ("FileField",)


class FileField(wtf.FileField):
    """Transforms file input value to and form Jembe File instance"""

    def process_data(self, value):
        if value is None:
            self.data = None
        elif isinstance(value, File):
            self.data = value
        else:
            self.data = File.load_init_param(value)

    # flag to quickly recognise JembeUI FileField in Jinja2 template
    is_jembeui_file_field = True
