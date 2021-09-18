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
    def form_widgets_variants_dirs(self):
        return current_app.config.get(
            "JEMBEUI_FORM_WIDGETS_VARIANTS_DIRS",
            ["widgets/form/", "{style}/widgets/form/", "jembeui/{style}/widgets/form/"],
        )

    @property
    def forms_template_dirs(self):
        return current_app.config.get(
            "JEMBEUI_FORMS_TEMPLATE_DIRS",
            ["forms/","{style}/forms/"],
        )

    @property
    def form_fields_template_dirs(self):
        return current_app.config.get(
            "JEMBEUI_FORM_FIELDS_TEMPLATE_DIRS",
            [
                "widgets/form_fields",
                "{style}/widgets/form_fields/",
                "jembeui/{style}/widgets/form_fields/",
            ],
        )

    @property
    def list_records_page_size(self):
        return current_app.config.get("JEMBEUI_LIST_RECORDS_PAGE_SIZE", 20)


settings = Settings()
