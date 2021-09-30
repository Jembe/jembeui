from jembe.component_config import config
from ..component import Component

__all__ = ("CPageSystemError",)


@config(Component.Config(changes_url=False, title="System Error"))
class CPageSystemError(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/system_error.html"

    _config: Config
