from jembe import config
from ..component import Component

__all__ = ("CPageHeadTag",)


@config(Component.Config(changes_url=False))
class CPageHeadTag(Component):
    """Display HTML header tag"""

    TITLE = "title"
    DESCRIPTION = "description"
    KEYWORDS = "keywords"
    AUTHOR = "author"
    OG_TYPE = "og_type"
    OG_TITLE = "og_title"
    OG_DESCRIPTION = "og_description"
    OG_URL = "og_url"
    OG_IMAGE = "og_image"
    OG_SITE_NAME = "og_site_name"
    TWITTER_TITLE = "twitter_title"
    TWITTER_TYPE = "twitter_type"
    TWITTER_URL = "twitter_url"
    TWITTER_IMAGE = "twitter_image"
    TWITTER_IMAGE_ALT = "twitter_image_alt"
    TWITTER_CARD = "twitter_card"
    TWITTER_SITE = "twitter_site"
    FB_APP_ID = "fb_app_id"
    TYPES = [
        TITLE,
        DESCRIPTION,
        KEYWORDS,
        AUTHOR,
        OG_TYPE,
        OG_TITLE,
        OG_DESCRIPTION,
        OG_URL,
        OG_IMAGE,
        OG_SITE_NAME,
        TWITTER_TITLE,
        TWITTER_TYPE,
        TWITTER_URL,
        TWITTER_IMAGE,
        TWITTER_IMAGE_ALT,
        TWITTER_CARD,
        TWITTER_SITE,
        FB_APP_ID,
    ]

    class Config(Component.Config):
        default_template: str = "/jembeui/components/page/head_tag.html"

    _config: Config

    def __init__(self, htype: str = "title", content: str = ""):
        if htype not in self.TYPES:
            raise ValueError(f"Unsupported head type '{type}'!")
        # self.key = htype
        super().__init__()
