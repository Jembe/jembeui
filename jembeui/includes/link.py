from typing import TYPE_CHECKING, Any, Callable, List, Optional, Sequence, Union, Dict
from functools import cached_property
from copy import copy
from dataclasses import dataclass
from markupsafe import Markup
from flask import render_template
from jembe import ComponentReference, ComponentConfig
from ..exceptions import JembeUIError

if TYPE_CHECKING:

    import jembe
    import jembeui

__all__ = ("Link",)


class Link:
    """Link to url or Jembe action used inside menus capable of displaying itself as HTML element"""

    LINK_TEMPLATE: List[str] = ["/jembeui/includes/link.html"]

    @dataclass
    class Style:
        """
        - classes: list of classes to add
        - full_classes: should the default classes be replaced
        - as_button: display as button instenad of href
        - title_hidden: don't show title only show icon if present,
            if icon is not present ignore this config
        """

        classes: Optional[str] = None
        full_classes: bool = False
        as_button: bool = False
        title_hidden: bool = False

    @dataclass
    class Icon:
        """
        - name: name of the icon to display
        - icon_set: name of the icon set to use from heroicons (outline, solid, mini)
        - classes: classes to add
        - full_classes: should the default classes be replaced
        - display_last: when true display icon after title
        """

        name: str
        icon_set: str = "outline"
        classes: Optional[str] = None
        full_classes: bool = False
        display_last: bool = False

    def __init__(
        self,
        to: Union[
            str,
            "jembe.ComponentReference",
            Callable[["jembe.Component"], "jembe.ComponentReference"],
        ],
        title: Optional[
            Union[
                str,
                Callable[["jembe.Component"], str],
            ]
        ] = None,
        description: Optional[Union[str, Callable[["jembe.Component"], str]]] = None,
        icon: Optional[
            Union[
                str,
                "jembe.Link.Icon",
                Callable[["jembe.Component"], Union[str, "jembe.Link.Icon"]],
            ]
        ] = None,
        style: Optional[
            Union[
                str,
                "jembe.Link.Style",
                Callable[["jembe.Component"], Union[str, "jembe.Link.Style"]],
            ]
        ] = None,
        active_for_path_names: Optional[Sequence[str]] = None,
        active_for_exec_names: Optional[Sequence[str]] = None,
        params: Optional[Dict[str, Any]] = None,
        is_accessible: Optional[
            Union[bool, Callable[["jembe.Component"], bool]]
        ] = None,
        as_button: bool = False,
    ):
        """Creates url or action/component link that can render itself as HTML

        Link element must be binded to its component before it can be used 
        in jinja2 template

        Args:
            to (Union[ str, &quot;jembe.ComponentReference&quot;, 
                Callable[[&quot;jembe.Component&quot;], 
                &quot;jembe.ComponentReference&quot;], ]):
                Determine what should help when user clicks the link. It can be:

                - URL address,
                    - starting with http:// or https:// are full urls
                - JRL (Jembe js code to invoce actions):
                    - component full names starting with  /
                    - relative child components names
                    - action name ending with (); params are passed with params attribute
                    - custom javascript prefixed with JRL: 
            title (Optional[ Union[ str, Callable[[&quot;jembe.Component&quot;], str], ] ], optional):
                Title of the link. Defaults to None.
            description (Optional[Union[str, Callable[[&quot;jembe.Component&quot;], str]]], optional):
                Link description (usualy used as title tag on html or a) Defaults to None.
            icon (Optional[ Union[ str, Icon], Callable[[&quot;jembe.Component&quot;], Union[str, Icon]]], ] ], optional):
                Icon name from heroicons set or dataclass with following params: name, icon_set, classes. Defaults to None.
            active_for_path_names (Optional[Sequence[str]], optional):
                List of url paths where link should be rendered as "active". Defaults to None.
            active_for_exec_names (Optional[Sequence[str]], optional):
                List of exec_names that should render link as "active" if they are present on the page. Defaults to None.
            params (Optional[Dict[str, Any]], optional):
                Parameters for action when action is called by its name in 'to' argument. Defaults to None.
            is_accessible (Optional[ Union[bool, Callable[[&quot;jembe.Component&quot;], bool]] ], optional):
                Defines if link is accessible to user or not. For action or component links this will be set
                regarding to component/action aviability to current user. Defaults to None.
        """
        self._to = to
        self._title = title
        self._description = description
        self._icon = icon
        self._style = style
        self._active_for_path_names = active_for_path_names
        self._active_for_exec_names = active_for_exec_names
        self._params = {} if params is None else params
        self._is_accessible = is_accessible
        self._as_button = as_button

        self.is_external = isinstance(self._to, str) and (
            self._to.startswith("https://") or self._to.startswith("http://")
        )

        self._component: Optional["jembe.Component"] = None
        self._calling_action = False

    def bind_to(self, component: "jembe.Component") -> "jembeui.Link":
        if self.is_binded:
            raise JembeUIError("Link is already binded! Link can't be binded twice")
        binded_link: "jembeui.Link" = copy(self)
        binded_link._component = component
        return binded_link

    @property
    def component(self) -> "jembe.Component":
        if self._component is None:
            raise JembeUIError("Link is not binded to component")
        return self._component

    @property
    def is_binded(self) -> bool:
        return self._component is not None

    @property
    def url(self) -> Optional[str]:
        if self.is_external:
            if not self.is_binded:
                raise ValueError("Link must be binded to component")
            return self._to  # type:ignore
        elif isinstance(self._to, str) and self._to.startswith("JRL:"):
            return '#'
        else:
            return self._component_reference.url

    @property
    def jrl(self) -> Optional[str]:
        if self.is_external:
            return None
        elif isinstance(self._to, str) and self._to.startswith("JRL:"):
            return self._to[4:]
        else:
            return self._component_reference.jrl

    @property
    def is_accessible(self) -> bool:
        """Check if link is accessible by current user"""
        if self.is_external:
            if not self.is_binded:
                raise ValueError("Link must be binded to component")
            if isinstance(self._is_accessible, bool):
                return self._is_accessible
            elif self._is_accessible is None:
                return True
            else:
                return self._is_accessible(self._component)
        else:
            return self._component_reference.is_accessible

    @cached_property
    def _component_reference(self) -> "jembe.ComponentReference":
        if not self.is_binded:
            raise ValueError("Link must be binded to component")
        if self.is_external:
            raise ValueError("Component reference doesn't exist for external links")
        if isinstance(self._to, str):
            return self._str_to_component_reference_lambda(self._to)(self._component)
        elif isinstance(self._to, ComponentReference):
            return self._to
        else:
            return self._to(self._component)

    def _str_to_component_reference_lambda(
        self, to_str: str
    ) -> Callable[["jembe.Component"], "jembe.ComponentReference"]:
        if to_str.endswith("()"):
            if "/" in to_str:
                raise ValueError(
                    "Action call shortcut cann't be used on subcomponents."
                )
            self._calling_action = True
            return lambda component: component.component().call(
                to_str[:-2], **self._params
            )
        else:
            return lambda component: component.component(to_str, **self._params)

    def render(self) -> str:
        if not self.is_binded:
            raise ValueError("Link is not binded to component")
        if not self.is_accessible:
            return ""
        context: dict = dict(
            is_external=self.is_external,
            url=self.url,
            jrl=self.jrl,
            title=self.title,
            description=self.description,
            icon=self.icon,
            style=self.style,
            active_for_path_names=self.active_for_path_names,
            active_for_exec_names=self.active_for_exec_names,
            is_accessible=self.is_accessible,
        )
        return Markup(render_template(self.LINK_TEMPLATE, **context))  # type:ignore

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.render()

    @property
    def title(self) -> Optional[str]:
        if not self.is_binded:
            raise ValueError("Link must be binded to component")
        if self._title is None:
            if self.is_external:
                return "Unknown link" if self.icon is None else None
            else:
                if self.icon is not None and self.style.title_hidden:
                    return None

                cr = self._component_reference
                if cr.action != ComponentConfig.DEFAULT_DISPLAY_ACTION:
                    return cr.action.title()
                else:
                    return cr.component_instance.title
        elif isinstance(self._title, str):
            return self._title
        else:
            # callable
            title = self._title(self._component)
            if title is None and self.icon is None:
                return "Unknown link"
            return title

    @property
    def description(self) -> Optional[str]:
        if not self.is_binded:
            raise ValueError("Link must be binded to component")

        return (
            self._description
            if self._description is None or isinstance(self._description, str)
            else self._description(self._component)
        )

    @property
    def icon(self) -> Optional["jembeui.Link.Icon"]:
        if not self.is_binded:
            raise ValueError("Link must be binded to component")

        if self._icon is None:
            return None
        elif isinstance(self._icon, str):
            split = self._icon.split(" ", 2)
            return self.Icon(
                name=split[0], classes=split[1] if len(split) == 2 else None
            )
        elif isinstance(self._icon, self.Icon):
            return self._icon
        else:
            # callable
            icon = self._icon(self._component)
            return icon if isinstance(icon, self.Icon) else self.Icon(name=icon)

    @property
    def style(self) -> "jembeui.Link.Style":
        if not self.is_binded:
            raise ValueError("Link must be binded to component")
        style: "jembeui.Link.Style"
        if self._style is None:
            style = self.Style(as_button=self._as_button)
        elif isinstance(self._style, str):
            style = self.Style(classes=self._style, as_button=self._as_button)
        elif isinstance(self._style, self.Style):
            style = self._style
            if self._as_button:
                style.as_button = True
        else:
            # callable
            res = self._style(self._component)
            style = (
                res
                if isinstance(res, self.Style)
                else self.Style(classes=res, as_button=self._as_button)
            )
            if self._as_button:
                style.as_button = True
        if self.icon is None:
            style.title_hidden = False
        elif (
            isinstance(self._style, str)
            and self._title is None
            and ("btn-circle" in self._style or "btn-square" in self._style)
        ):
            style.title_hidden = True
        return style

    @property
    def active_for_path_names(self) -> Sequence[str]:
        if self._active_for_path_names is not None:
            return self._active_for_path_names
        else:
            return ()

    @property
    def active_for_exec_names(self) -> Sequence[str]:
        if self._active_for_exec_names is not None:
            return self._active_for_exec_names
        else:
            if (
                not self.is_external
                and self._active_for_path_names is None
                and self._active_for_exec_names is None
                and not self._calling_action 
            ):
                return (self._component_reference.exec_name,)
            return ()

    @property
    def is_link(self):
        return True

    def __copy__(self) -> "jembeui.Link":
        link = Link(
            to=self._to,
            title=self._title,
            description=self._description,
            icon=copy(self._icon),
            style=copy(self._style),
            active_for_path_names=(
                tuple(k for k in self._active_for_path_names)
                if isinstance(self._active_for_path_names, (list, tuple))
                else self._active_for_path_names
            ),
            active_for_exec_names=(
                tuple(k for k in self._active_for_exec_names)
                if isinstance(self._active_for_exec_names, (list, tuple))
                else self._active_for_exec_names
            ),
            params=(
                {k: v for k, v in self._params.items()}
                if isinstance(self._params, dict)
                else self._params
            ),
            is_accessible=self._is_accessible,
            as_button=self._as_button,
        )

        link.is_external = self.is_external
        link._component = None

        return link
