from ..component import Component
from jembe import config


__all__ = ("CPageUpdateIndicator",)


@config(Component.Config(changes_url=False))
class CPageUpdateIndicator(Component):
    class Config(Component.Config):
        default_template_exp = "jembeui/{style}/components/page/update_indicator.html"
