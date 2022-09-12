from jembe import config
from ..component import Component

__all__ = ("CPageSystemError",)


@config(Component.Config(changes_url=False, title="System Error"))
class CPageSystemError(Component):
    """Display modal when system error occure usualy when server is unavaiable"""

    class Config(Component.Config):
        default_template = "jembeui/components/page/system_error.html"

    _config: Config
