from typing import Optional, Tuple
from jembe import File
from .file import FileField
from PIL import Image, ImageOps


__all__ = ("ImageField",)


class ImageField(FileField):
    def __init__(
        self,
        label=None,
        validators=None,
        thumbnail_size=(300, 300),
        enable_screenshot: bool = False,
        # enable_image_edit: bool = False,
        # edit_on_change: bool = False,
        filters=tuple(),
        description="",
        id=None,
        default=None,
        widget=None,
        render_kw=None,
        _form=None,
        _name=None,
        _prefix="",
        _translations=None,
        _meta=None,
    ):
        super().__init__(
            label=label,
            validators=validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget,
            render_kw=render_kw,
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            _translations=_translations,
            _meta=_meta,
        )
        self.thumbnail_size = thumbnail_size
        self.enable_screenshot = enable_screenshot

    def thumbnail(self, size: Optional[Tuple[int, int]] = None) -> Optional["File"]:
        thumbnail_size = size if size else self.thumbnail_size
        if self.data:
            thumb = self.data.get_cache_version(
                "thumbnail_{}_{}.jpg".format(*thumbnail_size)
            )
            if not thumb.exists():
                try:
                    with Image.open(self.data.open(mode="rb")) as img:
                        img.verify()
                except Exception:
                    return None
                with Image.open(self.data.open(mode="rb")) as img:
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img = ImageOps.exif_transpose(img)
                    img.thumbnail(thumbnail_size, Image.BICUBIC)
                    with thumb.open("wb") as tfo:
                        img.save(tfo, "JPEG")
                        return thumb
            else:
                return thumb
        return None
