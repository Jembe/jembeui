window.addEventListener(
  'jembeUpdatePage',
  function (event) {
    if (event.detail.isXUpdate) {
      for ([cname, cdom] of Object.entries(event.detail.components)) {
        window.jembeClient.walkComponent(cdom, jembeui_s2_init_mui)
      }

    } else {
      window.jembeClient.walkDocument(jembeui_s2_init_mui)
    }
  }
)

function jembeui_s2_init_mui(el) {
  if (el.classList.contains('mdc-snackbar')) {
    // Snackbar
    el._mdcSnackbar = mdc.snackbar.MDCSnackbar.attachTo(el);
    // el._mdcSnackbar.timeoutMs = -1;
    // el._mdcSnackbar.open();
  } else if (el.classList.contains('mdc-banner')) {
    // Banner
    el._mdcBanner = mdc.banner.MDCBanner.attachTo(el);
    // el._mdcBanner.open();
  } else if (el.classList.contains('mdc-button') && el._mdcRipple === undefined) {
    // Button Ripple
    el._mdcRipple = mdc.ripple.MDCRipple.attachTo(el);
  } else if (el.classList.contains('mdc-dialog')) {
    // Dialog
    el._mdcDialog = mdc.dialog.MDCDialog.attachTo(el);
    if (el.classList.contains('scrim-click-disabled')) {
      el._mdcDialog.scrimClickAction = '';
    }
    // el._mdcDialog.listen('MDCDialog:opened', () => {
    //   el._mdcDialog.layout();
    // });
  } else if (el.classList.contains('mdc-linear-progress')) {
    // linear progress bar
    el._mdcProgress = mdc.linearProgress.MDCLinearProgress.attachTo(el);
  }

}