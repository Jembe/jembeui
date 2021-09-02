from flask import current_app

__all__ = ("settings",)


class Settings:
    @property
    def default_style(self):
        return current_app.config.get("JEMBEUI_STYLE", "s0")

    @property
    def list_records_page_size(self):
        return current_app.config.get("JEMBEUI_LIST_RECORDS_PAGE_SIZE", 20)


settings = Settings()
