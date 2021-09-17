from typing import TYPE_CHECKING
from ..component import Component

if TYPE_CHECKING:
    import jembe

__all__ = ("CForm",)


class CForm(Component):
    class Config(Component.Config):
        pass
