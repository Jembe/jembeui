from flask import current_app

__all__ = ("settings",)


class Settings:
    @property
    def supported_locales(self):
        return current_app.config.get("JEMBEUI_SUPPORTED_LOCALES", [])


settings = Settings()
