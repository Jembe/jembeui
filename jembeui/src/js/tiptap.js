import { Editor } from "@tiptap/core";
import StarterKit from "@tiptap/starter-kit";

const TipTap = {
  start: function (el, is_disabled) {
    content = el.innerHTML;
    el.innerHTML = "";

    return new Editor({
      element: el,
      extensions: [StarterKit],
      editable: !is_disabled,

      editorProps: {
        attributes: {
          class: "prose prose-sm max-w-full focus:outline-none text-base-content",
        },
      },
      content: content,
      onBlur({ editor, event }) {
        const html = editor.getHTML();
        el.value = html;
        el.dispatchEvent(new Event("change", { detail: html }));
      },
    });
  },
  // get tiptap editor instance from button in toolboard
  get: function (el) {
    return el.parentElement.nextElementSibling._editor;
  },
};
export { TipTap };
