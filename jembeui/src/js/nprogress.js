import NProgress from "nprogress";

// Configure NProgress bar
NProgress.configure({ showSpinner: false });
function registerNProgressBar() {
  let requestsInProgress = 0;
  updateProgressBar = () => {
    if (requestsInProgress > 0) {
      NProgress.start();
    } else {
      NProgress.done();
    }
  };

  window.addEventListener("jembeStartUpdatePage", () => {
    requestsInProgress += 1;
    updateProgressBar();
  });
  window.addEventListener("jembeUpdatePage", (event) => {
    if (event.detail.isXUpdate) {
      requestsInProgress -= 1;
    }
    updateProgressBar();
  });
  window.addEventListener("jembeUpdatePageError", () => {
    requestsInProgress -= 1;
    updateProgressBar();
  });
}

registerNProgressBar();