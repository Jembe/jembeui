const Lov = {
  closeListbox: ($context) => {
    let focused = $context.$local.focusedOptionId !== null;
    $context.$local.focusedOptionId = null;
    $context.search = null;
    if (focused){
      $context.$el.querySelector("[jmb-ref=button]").focus();
    }
  },
  toggleListboxVisibility: ($context) => {
    if ($context.search !== null) return juiLov.closeListbox($context);
    $context.search = String("");
    $context.$local.focusedOptionId = null;
  },

  selectOption: function ($context, $dispatch) {
    let focusedId = $context.$local.focusedOptionId;
    $context.$local.focusedOptionId = null;
    $context.selected =
      focusedId !== null && focusedId !== "" ? String(focusedId) : null;
    $context.search = null;
    $dispatch("select-option-changed", { selected: $context.selected });
  },
  focusNext: function ($context) {
    if ($context.$local.focusedOptionId === null) {
      nextOption = $context.$el.querySelector("[option-id]");
    } else {
      selOption = $context.$el.querySelector(
        "[option-id='" + $context.$local.focusedOptionId + "']"
      );
      nextOption = selOption !== null ? selOption.nextElementSibling : null;
      if (nextOption === null) {
        nextOption = $context.$el.querySelector("[option-id]");
      }
    }
    if (nextOption === null) {
      return;
    }
    $context.$local.focusedOptionId = nextOption.getAttribute("option-id");
    nextOption.scrollIntoViewIfNeeded();
  },
  focusPrev: function ($context) {
    if ($context.$local.focusedOptionId === null) {
      prevOption = $context.$el.querySelector("[option-id]:last-of-type");
    } else {
      selOption = $context.$el.querySelector(
        "[option-id='" + $context.$local.focusedOptionId + "']"
      );
      prevOption = selOption !== null ? selOption.previousElementSibling : null;
      if (prevOption === null) {
        prevOption = $context.$el.querySelector("[option-id]:last-of-type");
      }
    }
    if (prevOption === null) {
      return;
    }
    $context.$local.focusedOptionId = prevOption.getAttribute("option-id");
    prevOption.scrollIntoViewIfNeeded();
  },
};

export { Lov };
