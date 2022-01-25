from typing import Optional, Tuple
from jembe import File
from .file import FileField
from PIL import Image, ImageOps
from ...helpers import create_thumbnail


__all__ = ("ImageField",)


class ImageField(FileField):
    def __init__(
        self,
        label=None,
        validators=None,
        thumbnail_size=(300, 300),
        enable_screenshot: bool = False,
        enable_image_edit: bool = False,
        filters=(),
        description="",
        id=None,
        default=None,
        widget=None,
        render_kw=None,
        name=None,
        _form=None,
        _prefix="",
        _translations=None,
        _meta=None,
    ):
        super().__init__(
            label,
            validators,
            filters,
            description,
            id,
            default,
            widget,
            render_kw,
            name,
            _form,
            _prefix,
            _translations,
            _meta,
        )
        self.thumbnail_size = thumbnail_size
        self.enable_screenshot = enable_screenshot
        self.enable_image_edit = enable_image_edit

    def thumbnail(self, size: Optional[Tuple[int, int]] = None) -> Optional["File"]:
        thumbnail_size = size if size else self.thumbnail_size
        if self.data:
            return create_thumbnail(self.data, thumbnail_size)
        return None
