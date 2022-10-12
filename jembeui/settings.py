from flask import current_app

__all__ = ("settings",)


class Settings:
    """Define JembeUI settings default values and gets config from app.config"""

    @property
    def supported_locales(self):
        """Locales supported"""
        return current_app.config.get("JEMBEUI_SUPPORTED_LOCALES", []) 

    @property
    def list_records_page_size(self):
        """Default page size for CList component"""
        return current_app.config.get("JEMBEUI_LIST_RECORDS_PAGE_SIZE", 20)

settings = Settings()
