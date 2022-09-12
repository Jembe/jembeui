import os
from itertools import chain
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    import jembe


__all__ = "list_used_jembeui_templates",

def list_used_jembeui_templates(jmb: "jembe.Jembe") -> List[str]:
    """Create list of JembeUI templates used by the current application"""
    # Get JembeUi Template root
    import jembeui

    jui_template_root = os.path.join(jembeui.__path__[0], "templates")

    # Add macros and includes templates
    templates = [
        os.path.join(jui_template_root, "jembeui", "macros", "**", "*"),
        os.path.join(jui_template_root, "jembeui", "includes", "**", "*"),
    ]
    # list component config templates, transforme it to full path, and remove duplicates
    file_names = set(
        os.path.abspath(
            os.path.join(
                jui_template_root,
                template_name
                if not template_name.startswith("/")
                else template_name[1:],
            )
        )
        for template_name in chain(
            *[v.template for v in jmb.components_configs.values()]
        )
    )
    # extend content with template files that actualy exist
    templates.extend(fname for fname in sorted(file_names) if os.path.exists(fname))

    return templates
