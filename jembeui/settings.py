from flask import current_app

__all__ = ("settings",)


class Settings:
    @property
    def default_style(self):
        return current_app.config.get("JEMBEUI_STYLE", "s0")

    @property
    def menu_widgets_variants_dirs(self):
        return current_app.config.get(
            "JEMBEUI_MENU_WIDGETS_VARIANTS_DIRS",
            ["jembeui/{style}/widgets/menu/"],
        )

    @property
    def link_widgets_variants_dirs(self):
        return current_app.config.get(
            "JEMBEUI_LINK_WIDGETS_VARIANTS_DIRS",
            ["jembeui/{style}/widgets/link/"],
        )

    @property
    def list_records_page_size(self):
        return current_app.config.get("JEMBEUI_LIST_RECORDS_PAGE_SIZE", 20)


settings = Settings()
