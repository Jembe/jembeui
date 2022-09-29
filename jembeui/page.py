from jembe import Component, config

__all__ = ("JembeUIPage",)


@config(Component.Config(template="jembeui/jembeui.html"))
class JembeUIPage(Component):
    """Empty page for flask to load JembeUI static paths"""
