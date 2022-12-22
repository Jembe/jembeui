from markupsafe import Markup
from flask import render_template_string
from wtforms.widgets import html_params
import wtforms as wtf

__all__ = ("TipTapField", "TipTapWidget")


class TipTapWidget:
    """
    Div container for tip tap field

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    validation_attrs = ["required", "maxlength", "minlength"]

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "placeholder" in kwargs:
            del kwargs["placeholder"]
        is_disabled = False
        if "disabled" in kwargs:
            if kwargs["disabled"] != False:
                is_disabled = True
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)

        html = ""
        if not is_disabled:
            html += """<div class="w-full"><div class="w-full border rounded-b-none border-base-300 rounded-box btn-group opacity-60">
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleHeading({ level: 1 }).run()" jmb:class="{ 'btn-active': TipTap.get($self).isActive('heading', { level: 2 }) }" title="Heading 1">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M13 20h-2v-7H4v7H2V4h2v7h7V4h2v16zm8-12v12h-2v-9.796l-2 .536V8.67L19.5 8H21z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleHeading({ level: 2 }).run()" jmb:class="{ 'btn-active': TipTap.get($self).isActive('heading', { level: 3 }) }" title="Heading 2">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M4 4v7h7V4h2v16h-2v-7H4v7H2V4h2zm14.5 4c2.071 0 3.75 1.679 3.75 3.75 0 .857-.288 1.648-.772 2.28l-.148.18L18.034 18H22v2h-7v-1.556l4.82-5.546c.268-.307.43-.709.43-1.148 0-.966-.784-1.75-1.75-1.75-.918 0-1.671.707-1.744 1.606l-.006.144h-2C14.75 9.679 16.429 8 18.5 8z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleBold().run()"  jmb:class="{ 'btn-active': TipTap.get($self).isActive('bold') }" title="Bold">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M8 11h4.5a2.5 2.5 0 1 0 0-5H8v5zm10 4.5a4.5 4.5 0 0 1-4.5 4.5H6V4h6.5a4.5 4.5 0 0 1 3.256 7.606A4.498 4.498 0 0 1 18 15.5zM8 13v5h5.5a2.5 2.5 0 1 0 0-5H8z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleItalic().run()"  jmb:class="{ 'btn-active': TipTap.get($self).isActive('italic') }" title="Italic">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M15 20H7v-2h2.927l2.116-12H9V4h8v2h-2.927l-2.116 12H15z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleBulletList().run()" jmb:class="{ 'btn-active': TipTap.get($self).isActive('bulletList') }" title="Bullet List">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M8 4h13v2H8V4zM4.5 6.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm0 7a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm0 6.9a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM8 11h13v2H8v-2zm0 7h13v2H8v-2z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleOrderedList().run()" jmb:class="{ 'btn-active': TipTap.get($self).isActive('orderedList') }" title="Ordered List">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M8 4h13v2H8V4zM5 3v3h1v1H3V6h1V4H3V3h2zM3 14v-2.5h2V11H3v-1h3v2.5H4v.5h2v1H3zm2 5.5H3v-1h2V18H3v-1h3v4H3v-1h2v-.5zM8 11h13v2H8v-2zm0 7h13v2H8v-2z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleBlockquote().run()" jmb:class="{ 'btn-active': TipTap.get($self).isActive('blockquote') }" title="Blockquote">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M19.417 6.679C20.447 7.773 21 9 21 10.989c0 3.5-2.457 6.637-6.03 8.188l-.893-1.378c3.335-1.804 3.987-4.145 4.247-5.621-.537.278-1.24.375-1.929.311-1.804-.167-3.226-1.648-3.226-3.489a3.5 3.5 0 0 1 3.5-3.5c1.073 0 2.099.49 2.748 1.179zm-10 0C10.447 7.773 11 9 11 10.989c0 3.5-2.457 6.637-6.03 8.188l-.893-1.378c3.335-1.804 3.987-4.145 4.247-5.621-.537.278-1.24.375-1.929.311C4.591 12.322 3.17 10.841 3.17 9a3.5 3.5 0 0 1 3.5-3.5c1.073 0 2.099.49 2.748 1.179z"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().unsetAllMarks().clearNodes().run()" title="Clear Formating">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M12.651 14.065L11.605 20H9.574l1.35-7.661-7.41-7.41L4.93 3.515 20.485 19.07l-1.414 1.414-6.42-6.42zm-.878-6.535l.27-1.53h-1.8l-2-2H20v2h-5.927L13.5 9.257 11.773 7.53z" fill="current"/></svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().undo().run()" title="Undo"> 
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
      </svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().redo().run()" title="Redo">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 15l6-6m0 0l-6-6m6 6H9a6 6 0 000 12h3" />
      </svg>
    </button>
    <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleHighlight().run()" title="Markiraj">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentCollor"><path fill="none" d="M0 0h24v24H0z"/><path d="M15.243 4.515l-6.738 6.737-.707 2.121-1.04 1.041 2.828 2.829 1.04-1.041 2.122-.707 6.737-6.738-4.242-4.242zm6.364 3.535a1 1 0 0 1 0 1.414l-7.779 7.779-2.12.707-1.415 1.414a1 1 0 0 1-1.414 0l-4.243-4.243a1 1 0 0 1 0-1.414l1.414-1.414.707-2.121 7.779-7.779a1 1 0 0 1 1.414 0l5.657 5.657zm-6.364-.707l1.414 1.414-4.95 4.95-1.414-1.414 4.95-4.95zM4.283 16.89l2.828 2.829-1.414 1.414-4.243-1.414 2.828-2.829z"/></svg>
    </button>
  </div>
  """
        else:
            html += '<div class="w-full">'

        html += (
            """<div jmb-cloak """
            """jmb-on:ready="$self._editor = TipTap.start($self, {})" """
            """jmb-on-remove="if ($self._tiptap){{$self._editor.destroy()}}" {}>{}</div></div>""".format(
                "true" if is_disabled else "false",
                html_params(name=field.name, **kwargs),
                field._value(),
            )
        )
        return Markup(html)


class TipTapField(wtf.StringField):
    """Transforms file input value to and form Jembe File instance"""

    widget = TipTapWidget()


# H3
# <button class="btn btn-square btn-ghost btn-sm" tabindex="-1" jmb-on:click="TipTap.get($self).chain().focus().toggleHeading({ level: 3 }).run()" jmb:class="{ 'btn-active': TipTap.get($self).isActive('heading', { level: 4 }) }" title="Heading 3">
#   <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24" width="24" height="24" stroke-width="0.1" stroke="currentColor"><path d="M22 8l-.002 2-2.505 2.883c1.59.435 2.757 1.89 2.757 3.617 0 2.071-1.679 3.75-3.75 3.75-1.826 0-3.347-1.305-3.682-3.033l1.964-.382c.156.806.866 1.415 1.718 1.415.966 0 1.75-.784 1.75-1.75s-.784-1.75-1.75-1.75c-.286 0-.556.069-.794.19l-1.307-1.547L19.35 10H15V8h7zM4 4v7h7V4h2v16h-2v-7H4v7H2V4h2z" fill="current"/></svg>
# </button>
