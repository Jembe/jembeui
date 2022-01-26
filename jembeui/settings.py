from flask import current_app

__all__ = ("settings",)


class Settings:
    @property
    def default_style(self):
        return current_app.config.get("JEMBEUI_STYLE", "s0")

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
            ["forms/", "{style}/forms/"],
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

    @property
    def default_currency(self):
        return current_app.config.get("JEMBEUI_DEFAULT_CURRENCY", "EUR")

    @property
    def supported_locales(self):
        return current_app.config.get("JEMBEUI_SUPPORTED_LOCALES", [])


settings = Settings()
