// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        this
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"8Ue9r":[function(require,module,exports) {
"use strict";
var global = arguments[3];
var HMR_HOST = null;
var HMR_PORT = 43123;
var HMR_SECURE = false;
var HMR_ENV_HASH = "d6ea1d42532a7575";
module.bundle.HMR_BUNDLE_ID = "e01c7e82c185049c";
/* global HMR_HOST, HMR_PORT, HMR_ENV_HASH, HMR_SECURE, chrome, browser, globalThis, __parcel__import__, __parcel__importScripts__, ServiceWorkerGlobalScope */ /*::
import type {
  HMRAsset,
  HMRMessage,
} from '@parcel/reporter-dev-server/src/HMRServer.js';
interface ParcelRequire {
  (string): mixed;
  cache: {|[string]: ParcelModule|};
  hotData: mixed;
  Module: any;
  parent: ?ParcelRequire;
  isParcelRequire: true;
  modules: {|[string]: [Function, {|[string]: string|}]|};
  HMR_BUNDLE_ID: string;
  root: ParcelRequire;
}
interface ParcelModule {
  hot: {|
    data: mixed,
    accept(cb: (Function) => void): void,
    dispose(cb: (mixed) => void): void,
    // accept(deps: Array<string> | string, cb: (Function) => void): void,
    // decline(): void,
    _acceptCallbacks: Array<(Function) => void>,
    _disposeCallbacks: Array<(mixed) => void>,
  |};
}
interface ExtensionContext {
  runtime: {|
    reload(): void,
    getURL(url: string): string;
    getManifest(): {manifest_version: number, ...};
  |};
}
declare var module: {bundle: ParcelRequire, ...};
declare var HMR_HOST: string;
declare var HMR_PORT: string;
declare var HMR_ENV_HASH: string;
declare var HMR_SECURE: boolean;
declare var chrome: ExtensionContext;
declare var browser: ExtensionContext;
declare var __parcel__import__: (string) => Promise<void>;
declare var __parcel__importScripts__: (string) => Promise<void>;
declare var globalThis: typeof self;
declare var ServiceWorkerGlobalScope: Object;
*/ var OVERLAY_ID = "__parcel__error__overlay__";
var OldModule = module.bundle.Module;
function Module(moduleName) {
    OldModule.call(this, moduleName);
    this.hot = {
        data: module.bundle.hotData,
        _acceptCallbacks: [],
        _disposeCallbacks: [],
        accept: function(fn) {
            this._acceptCallbacks.push(fn || function() {});
        },
        dispose: function(fn) {
            this._disposeCallbacks.push(fn);
        }
    };
    module.bundle.hotData = undefined;
}
module.bundle.Module = Module;
var checkedAssets, acceptedAssets, assetsToAccept /*: Array<[ParcelRequire, string]> */ ;
function getHostname() {
    return HMR_HOST || (location.protocol.indexOf("http") === 0 ? location.hostname : "localhost");
}
function getPort() {
    return HMR_PORT || location.port;
} // eslint-disable-next-line no-redeclare
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== "undefined") {
    var hostname = getHostname();
    var port = getPort();
    var protocol = HMR_SECURE || location.protocol == "https:" && !/localhost|127.0.0.1|0.0.0.0/.test(hostname) ? "wss" : "ws";
    var ws = new WebSocket(protocol + "://" + hostname + (port ? ":" + port : "") + "/"); // Web extension context
    var extCtx = typeof chrome === "undefined" ? typeof browser === "undefined" ? null : browser : chrome; // Safari doesn't support sourceURL in error stacks.
    // eval may also be disabled via CSP, so do a quick check.
    var supportsSourceURL = false;
    try {
        (0, eval)('throw new Error("test"); //# sourceURL=test.js');
    } catch (err) {
        supportsSourceURL = err.stack.includes("test.js");
    } // $FlowFixMe
    ws.onmessage = async function(event) {
        checkedAssets = {} /*: {|[string]: boolean|} */ ;
        acceptedAssets = {} /*: {|[string]: boolean|} */ ;
        assetsToAccept = [];
        var data = JSON.parse(event.data);
        if (data.type === "update") {
            // Remove error overlay if there is one
            if (typeof document !== "undefined") removeErrorOverlay();
            let assets = data.assets.filter((asset)=>asset.envHash === HMR_ENV_HASH); // Handle HMR Update
            let handled = assets.every((asset)=>{
                return asset.type === "css" || asset.type === "js" && hmrAcceptCheck(module.bundle.root, asset.id, asset.depsByBundle);
            });
            if (handled) {
                console.clear(); // Dispatch custom event so other runtimes (e.g React Refresh) are aware.
                if (typeof window !== "undefined" && typeof CustomEvent !== "undefined") window.dispatchEvent(new CustomEvent("parcelhmraccept"));
                await hmrApplyUpdates(assets);
                for(var i = 0; i < assetsToAccept.length; i++){
                    var id = assetsToAccept[i][1];
                    if (!acceptedAssets[id]) hmrAcceptRun(assetsToAccept[i][0], id);
                }
            } else fullReload();
        }
        if (data.type === "error") {
            // Log parcel errors to console
            for (let ansiDiagnostic of data.diagnostics.ansi){
                let stack = ansiDiagnostic.codeframe ? ansiDiagnostic.codeframe : ansiDiagnostic.stack;
                console.error("\uD83D\uDEA8 [parcel]: " + ansiDiagnostic.message + "\n" + stack + "\n\n" + ansiDiagnostic.hints.join("\n"));
            }
            if (typeof document !== "undefined") {
                // Render the fancy html overlay
                removeErrorOverlay();
                var overlay = createErrorOverlay(data.diagnostics.html); // $FlowFixMe
                document.body.appendChild(overlay);
            }
        }
    };
    ws.onerror = function(e) {
        console.error(e.message);
    };
    ws.onclose = function() {
        console.warn("[parcel] \uD83D\uDEA8 Connection to the HMR server was lost");
    };
}
function removeErrorOverlay() {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
        overlay.remove();
        console.log("[parcel] ✨ Error resolved");
    }
}
function createErrorOverlay(diagnostics) {
    var overlay = document.createElement("div");
    overlay.id = OVERLAY_ID;
    let errorHTML = '<div style="background: black; opacity: 0.85; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; font-family: Menlo, Consolas, monospace; z-index: 9999;">';
    for (let diagnostic of diagnostics){
        let stack = diagnostic.frames.length ? diagnostic.frames.reduce((p, frame)=>{
            return `${p}
<a href="/__parcel_launch_editor?file=${encodeURIComponent(frame.location)}" style="text-decoration: underline; color: #888" onclick="fetch(this.href); return false">${frame.location}</a>
${frame.code}`;
        }, "") : diagnostic.stack;
        errorHTML += `
      <div>
        <div style="font-size: 18px; font-weight: bold; margin-top: 20px;">
          🚨 ${diagnostic.message}
        </div>
        <pre>${stack}</pre>
        <div>
          ${diagnostic.hints.map((hint)=>"<div>\uD83D\uDCA1 " + hint + "</div>").join("")}
        </div>
        ${diagnostic.documentation ? `<div>📝 <a style="color: violet" href="${diagnostic.documentation}" target="_blank">Learn more</a></div>` : ""}
      </div>
    `;
    }
    errorHTML += "</div>";
    overlay.innerHTML = errorHTML;
    return overlay;
}
function fullReload() {
    if ("reload" in location) location.reload();
    else if (extCtx && extCtx.runtime && extCtx.runtime.reload) extCtx.runtime.reload();
}
function getParents(bundle, id) /*: Array<[ParcelRequire, string]> */ {
    var modules = bundle.modules;
    if (!modules) return [];
    var parents = [];
    var k, d, dep;
    for(k in modules)for(d in modules[k][1]){
        dep = modules[k][1][d];
        if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) parents.push([
            bundle,
            k
        ]);
    }
    if (bundle.parent) parents = parents.concat(getParents(bundle.parent, id));
    return parents;
}
function updateLink(link) {
    var newLink = link.cloneNode();
    newLink.onload = function() {
        if (link.parentNode !== null) // $FlowFixMe
        link.parentNode.removeChild(link);
    };
    newLink.setAttribute("href", link.getAttribute("href").split("?")[0] + "?" + Date.now()); // $FlowFixMe
    link.parentNode.insertBefore(newLink, link.nextSibling);
}
var cssTimeout = null;
function reloadCSS() {
    if (cssTimeout) return;
    cssTimeout = setTimeout(function() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for(var i = 0; i < links.length; i++){
            // $FlowFixMe[incompatible-type]
            var href = links[i].getAttribute("href");
            var hostname = getHostname();
            var servedFromHMRServer = hostname === "localhost" ? new RegExp("^(https?:\\/\\/(0.0.0.0|127.0.0.1)|localhost):" + getPort()).test(href) : href.indexOf(hostname + ":" + getPort());
            var absolute = /^https?:\/\//i.test(href) && href.indexOf(location.origin) !== 0 && !servedFromHMRServer;
            if (!absolute) updateLink(links[i]);
        }
        cssTimeout = null;
    }, 50);
}
function hmrDownload(asset) {
    if (asset.type === "js") {
        if (typeof document !== "undefined") {
            let script = document.createElement("script");
            script.src = asset.url + "?t=" + Date.now();
            if (asset.outputFormat === "esmodule") script.type = "module";
            return new Promise((resolve, reject)=>{
                var _document$head;
                script.onload = ()=>resolve(script);
                script.onerror = reject;
                (_document$head = document.head) === null || _document$head === void 0 || _document$head.appendChild(script);
            });
        } else if (typeof importScripts === "function") {
            // Worker scripts
            if (asset.outputFormat === "esmodule") return import(asset.url + "?t=" + Date.now());
            else return new Promise((resolve, reject)=>{
                try {
                    importScripts(asset.url + "?t=" + Date.now());
                    resolve();
                } catch (err) {
                    reject(err);
                }
            });
        }
    }
}
async function hmrApplyUpdates(assets) {
    global.parcelHotUpdate = Object.create(null);
    let scriptsToRemove;
    try {
        // If sourceURL comments aren't supported in eval, we need to load
        // the update from the dev server over HTTP so that stack traces
        // are correct in errors/logs. This is much slower than eval, so
        // we only do it if needed (currently just Safari).
        // https://bugs.webkit.org/show_bug.cgi?id=137297
        // This path is also taken if a CSP disallows eval.
        if (!supportsSourceURL) {
            let promises = assets.map((asset)=>{
                var _hmrDownload;
                return (_hmrDownload = hmrDownload(asset)) === null || _hmrDownload === void 0 ? void 0 : _hmrDownload.catch((err)=>{
                    // Web extension bugfix for Chromium
                    // https://bugs.chromium.org/p/chromium/issues/detail?id=1255412#c12
                    if (extCtx && extCtx.runtime && extCtx.runtime.getManifest().manifest_version == 3) {
                        if (typeof ServiceWorkerGlobalScope != "undefined" && global instanceof ServiceWorkerGlobalScope) {
                            extCtx.runtime.reload();
                            return;
                        }
                        asset.url = extCtx.runtime.getURL("/__parcel_hmr_proxy__?url=" + encodeURIComponent(asset.url + "?t=" + Date.now()));
                        return hmrDownload(asset);
                    }
                    throw err;
                });
            });
            scriptsToRemove = await Promise.all(promises);
        }
        assets.forEach(function(asset) {
            hmrApply(module.bundle.root, asset);
        });
    } finally{
        delete global.parcelHotUpdate;
        if (scriptsToRemove) scriptsToRemove.forEach((script)=>{
            if (script) {
                var _document$head2;
                (_document$head2 = document.head) === null || _document$head2 === void 0 || _document$head2.removeChild(script);
            }
        });
    }
}
function hmrApply(bundle, asset) {
    var modules = bundle.modules;
    if (!modules) return;
    if (asset.type === "css") reloadCSS();
    else if (asset.type === "js") {
        let deps = asset.depsByBundle[bundle.HMR_BUNDLE_ID];
        if (deps) {
            if (modules[asset.id]) {
                // Remove dependencies that are removed and will become orphaned.
                // This is necessary so that if the asset is added back again, the cache is gone, and we prevent a full page reload.
                let oldDeps = modules[asset.id][1];
                for(let dep in oldDeps)if (!deps[dep] || deps[dep] !== oldDeps[dep]) {
                    let id = oldDeps[dep];
                    let parents = getParents(module.bundle.root, id);
                    if (parents.length === 1) hmrDelete(module.bundle.root, id);
                }
            }
            if (supportsSourceURL) // Global eval. We would use `new Function` here but browser
            // support for source maps is better with eval.
            (0, eval)(asset.output);
             // $FlowFixMe
            let fn = global.parcelHotUpdate[asset.id];
            modules[asset.id] = [
                fn,
                deps
            ];
        } else if (bundle.parent) hmrApply(bundle.parent, asset);
    }
}
function hmrDelete(bundle, id) {
    let modules = bundle.modules;
    if (!modules) return;
    if (modules[id]) {
        // Collect dependencies that will become orphaned when this module is deleted.
        let deps = modules[id][1];
        let orphans = [];
        for(let dep in deps){
            let parents = getParents(module.bundle.root, deps[dep]);
            if (parents.length === 1) orphans.push(deps[dep]);
        } // Delete the module. This must be done before deleting dependencies in case of circular dependencies.
        delete modules[id];
        delete bundle.cache[id]; // Now delete the orphans.
        orphans.forEach((id)=>{
            hmrDelete(module.bundle.root, id);
        });
    } else if (bundle.parent) hmrDelete(bundle.parent, id);
}
function hmrAcceptCheck(bundle, id, depsByBundle) {
    if (hmrAcceptCheckOne(bundle, id, depsByBundle)) return true;
     // Traverse parents breadth first. All possible ancestries must accept the HMR update, or we'll reload.
    let parents = getParents(module.bundle.root, id);
    let accepted = false;
    while(parents.length > 0){
        let v = parents.shift();
        let a = hmrAcceptCheckOne(v[0], v[1], null);
        if (a) // If this parent accepts, stop traversing upward, but still consider siblings.
        accepted = true;
        else {
            // Otherwise, queue the parents in the next level upward.
            let p = getParents(module.bundle.root, v[1]);
            if (p.length === 0) {
                // If there are no parents, then we've reached an entry without accepting. Reload.
                accepted = false;
                break;
            }
            parents.push(...p);
        }
    }
    return accepted;
}
function hmrAcceptCheckOne(bundle, id, depsByBundle) {
    var modules = bundle.modules;
    if (!modules) return;
    if (depsByBundle && !depsByBundle[bundle.HMR_BUNDLE_ID]) {
        // If we reached the root bundle without finding where the asset should go,
        // there's nothing to do. Mark as "accepted" so we don't reload the page.
        if (!bundle.parent) return true;
        return hmrAcceptCheck(bundle.parent, id, depsByBundle);
    }
    if (checkedAssets[id]) return true;
    checkedAssets[id] = true;
    var cached = bundle.cache[id];
    assetsToAccept.push([
        bundle,
        id
    ]);
    if (!cached || cached.hot && cached.hot._acceptCallbacks.length) return true;
}
function hmrAcceptRun(bundle, id) {
    var cached = bundle.cache[id];
    bundle.hotData = {};
    if (cached && cached.hot) cached.hot.data = bundle.hotData;
    if (cached && cached.hot && cached.hot._disposeCallbacks.length) cached.hot._disposeCallbacks.forEach(function(cb) {
        cb(bundle.hotData);
    });
    delete bundle.cache[id];
    bundle(id);
    cached = bundle.cache[id];
    if (cached && cached.hot && cached.hot._acceptCallbacks.length) cached.hot._acceptCallbacks.forEach(function(cb) {
        var assetsToAlsoAccept = cb(function() {
            return getParents(module.bundle.root, id);
        });
        if (assetsToAlsoAccept && assetsToAccept.length) // $FlowFixMe[method-unbinding]
        assetsToAccept.push.apply(assetsToAccept, assetsToAlsoAccept);
    });
    acceptedAssets[id] = true;
}

},{}],"idS3Y":[function(require,module,exports) {
var _i18N = require("./i18n");
var _nprogress = require("./nprogress");
var _vanillajsDatepicker = require("vanillajs-datepicker");
var _lov = require("./lov");
window.Datepicker = (0, _vanillajsDatepicker.Datepicker);
window.juiLov = (0, _lov.Lov);

},{"./i18n":"6CuKp","./nprogress":"9pg8g","vanillajs-datepicker":"4sPNn","./lov":"ayviZ"}],"6CuKp":[function(require,module,exports) {
function setJembeuiTimezoneCookie(timezone) {
    if (timezone !== undefined && timezone !== null) document.cookie = `jembeuiTimezone=${timezone};`;
    else {
        const timezoneCookie = document.cookie.split("; ").find((item)=>item.trim().startsWith("jembeuiTimezone="));
        const currentTimezone = timezoneCookie !== undefined ? timezoneCookie.trim().split("=")[1] : null;
        timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        if (currentTimezone !== timezone) document.cookie = `jembeuiTimezone=${timezone};`;
    }
}
function setJembeuiLocaleCookie(localeCode) {
    if (localeCode !== undefined && localeCode !== null) document.cookie = `jembeuiLocaleCode=${localeCode};`;
}
setJembeuiTimezoneCookie();

},{}],"9pg8g":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
var _nprogress = require("nprogress");
var _nprogressDefault = parcelHelpers.interopDefault(_nprogress);
// Configure NProgress bar
(0, _nprogressDefault.default).configure({
    showSpinner: false
});
function registerNProgressBar() {
    let requestsInProgress = 0;
    updateProgressBar = ()=>{
        if (requestsInProgress > 0) (0, _nprogressDefault.default).start();
        else (0, _nprogressDefault.default).done();
    };
    window.addEventListener("jembeStartUpdatePage", ()=>{
        requestsInProgress += 1;
        updateProgressBar();
    });
    window.addEventListener("jembeUpdatePage", (event)=>{
        if (event.detail.isXUpdate) requestsInProgress -= 1;
        updateProgressBar();
    });
    window.addEventListener("jembeUpdatePageError", ()=>{
        requestsInProgress -= 1;
        updateProgressBar();
    });
}
registerNProgressBar();

},{"nprogress":"1tCWG","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"1tCWG":[function(require,module,exports) {
(function(root, factory) {
    if (typeof define === "function" && define.amd) define(factory);
    else module.exports = factory();
})(this, function() {
    var NProgress = {};
    NProgress.version = "0.2.0";
    var Settings = NProgress.settings = {
        minimum: 0.08,
        easing: "ease",
        positionUsing: "",
        speed: 200,
        trickle: true,
        trickleRate: 0.02,
        trickleSpeed: 800,
        showSpinner: true,
        barSelector: '[role="bar"]',
        spinnerSelector: '[role="spinner"]',
        parent: "body",
        template: '<div class="bar" role="bar"><div class="peg"></div></div><div class="spinner" role="spinner"><div class="spinner-icon"></div></div>'
    };
    /**
   * Updates configuration.
   *
   *     NProgress.configure({
   *       minimum: 0.1
   *     });
   */ NProgress.configure = function(options) {
        var key, value;
        for(key in options){
            value = options[key];
            if (value !== undefined && options.hasOwnProperty(key)) Settings[key] = value;
        }
        return this;
    };
    /**
   * Last number.
   */ NProgress.status = null;
    /**
   * Sets the progress bar status, where `n` is a number from `0.0` to `1.0`.
   *
   *     NProgress.set(0.4);
   *     NProgress.set(1.0);
   */ NProgress.set = function(n) {
        var started = NProgress.isStarted();
        n = clamp(n, Settings.minimum, 1);
        NProgress.status = n === 1 ? null : n;
        var progress = NProgress.render(!started), bar = progress.querySelector(Settings.barSelector), speed = Settings.speed, ease = Settings.easing;
        progress.offsetWidth; /* Repaint */ 
        queue(function(next) {
            // Set positionUsing if it hasn't already been set
            if (Settings.positionUsing === "") Settings.positionUsing = NProgress.getPositioningCSS();
            // Add transition
            css(bar, barPositionCSS(n, speed, ease));
            if (n === 1) {
                // Fade out
                css(progress, {
                    transition: "none",
                    opacity: 1
                });
                progress.offsetWidth; /* Repaint */ 
                setTimeout(function() {
                    css(progress, {
                        transition: "all " + speed + "ms linear",
                        opacity: 0
                    });
                    setTimeout(function() {
                        NProgress.remove();
                        next();
                    }, speed);
                }, speed);
            } else setTimeout(next, speed);
        });
        return this;
    };
    NProgress.isStarted = function() {
        return typeof NProgress.status === "number";
    };
    /**
   * Shows the progress bar.
   * This is the same as setting the status to 0%, except that it doesn't go backwards.
   *
   *     NProgress.start();
   *
   */ NProgress.start = function() {
        if (!NProgress.status) NProgress.set(0);
        var work = function() {
            setTimeout(function() {
                if (!NProgress.status) return;
                NProgress.trickle();
                work();
            }, Settings.trickleSpeed);
        };
        if (Settings.trickle) work();
        return this;
    };
    /**
   * Hides the progress bar.
   * This is the *sort of* the same as setting the status to 100%, with the
   * difference being `done()` makes some placebo effect of some realistic motion.
   *
   *     NProgress.done();
   *
   * If `true` is passed, it will show the progress bar even if its hidden.
   *
   *     NProgress.done(true);
   */ NProgress.done = function(force) {
        if (!force && !NProgress.status) return this;
        return NProgress.inc(0.3 + 0.5 * Math.random()).set(1);
    };
    /**
   * Increments by a random amount.
   */ NProgress.inc = function(amount) {
        var n = NProgress.status;
        if (!n) return NProgress.start();
        else {
            if (typeof amount !== "number") amount = (1 - n) * clamp(Math.random() * n, 0.1, 0.95);
            n = clamp(n + amount, 0, 0.994);
            return NProgress.set(n);
        }
    };
    NProgress.trickle = function() {
        return NProgress.inc(Math.random() * Settings.trickleRate);
    };
    /**
   * Waits for all supplied jQuery promises and
   * increases the progress as the promises resolve.
   *
   * @param $promise jQUery Promise
   */ (function() {
        var initial = 0, current = 0;
        NProgress.promise = function($promise) {
            if (!$promise || $promise.state() === "resolved") return this;
            if (current === 0) NProgress.start();
            initial++;
            current++;
            $promise.always(function() {
                current--;
                if (current === 0) {
                    initial = 0;
                    NProgress.done();
                } else NProgress.set((initial - current) / initial);
            });
            return this;
        };
    })();
    /**
   * (Internal) renders the progress bar markup based on the `template`
   * setting.
   */ NProgress.render = function(fromStart) {
        if (NProgress.isRendered()) return document.getElementById("nprogress");
        addClass(document.documentElement, "nprogress-busy");
        var progress = document.createElement("div");
        progress.id = "nprogress";
        progress.innerHTML = Settings.template;
        var bar = progress.querySelector(Settings.barSelector), perc = fromStart ? "-100" : toBarPerc(NProgress.status || 0), parent = document.querySelector(Settings.parent), spinner;
        css(bar, {
            transition: "all 0 linear",
            transform: "translate3d(" + perc + "%,0,0)"
        });
        if (!Settings.showSpinner) {
            spinner = progress.querySelector(Settings.spinnerSelector);
            spinner && removeElement(spinner);
        }
        if (parent != document.body) addClass(parent, "nprogress-custom-parent");
        parent.appendChild(progress);
        return progress;
    };
    /**
   * Removes the element. Opposite of render().
   */ NProgress.remove = function() {
        removeClass(document.documentElement, "nprogress-busy");
        removeClass(document.querySelector(Settings.parent), "nprogress-custom-parent");
        var progress = document.getElementById("nprogress");
        progress && removeElement(progress);
    };
    /**
   * Checks if the progress bar is rendered.
   */ NProgress.isRendered = function() {
        return !!document.getElementById("nprogress");
    };
    /**
   * Determine which positioning CSS rule to use.
   */ NProgress.getPositioningCSS = function() {
        // Sniff on document.body.style
        var bodyStyle = document.body.style;
        // Sniff prefixes
        var vendorPrefix = "WebkitTransform" in bodyStyle ? "Webkit" : "MozTransform" in bodyStyle ? "Moz" : "msTransform" in bodyStyle ? "ms" : "OTransform" in bodyStyle ? "O" : "";
        if (vendorPrefix + "Perspective" in bodyStyle) // Modern browsers with 3D support, e.g. Webkit, IE10
        return "translate3d";
        else if (vendorPrefix + "Transform" in bodyStyle) // Browsers without 3D support, e.g. IE9
        return "translate";
        else // Browsers without translate() support, e.g. IE7-8
        return "margin";
    };
    /**
   * Helpers
   */ function clamp(n, min, max) {
        if (n < min) return min;
        if (n > max) return max;
        return n;
    }
    /**
   * (Internal) converts a percentage (`0..1`) to a bar translateX
   * percentage (`-100%..0%`).
   */ function toBarPerc(n) {
        return (-1 + n) * 100;
    }
    /**
   * (Internal) returns the correct CSS for changing the bar's
   * position given an n percentage, and speed and ease from Settings
   */ function barPositionCSS(n, speed, ease) {
        var barCSS;
        if (Settings.positionUsing === "translate3d") barCSS = {
            transform: "translate3d(" + toBarPerc(n) + "%,0,0)"
        };
        else if (Settings.positionUsing === "translate") barCSS = {
            transform: "translate(" + toBarPerc(n) + "%,0)"
        };
        else barCSS = {
            "margin-left": toBarPerc(n) + "%"
        };
        barCSS.transition = "all " + speed + "ms " + ease;
        return barCSS;
    }
    /**
   * (Internal) Queues a function to be executed.
   */ var queue = function() {
        var pending = [];
        function next() {
            var fn = pending.shift();
            if (fn) fn(next);
        }
        return function(fn) {
            pending.push(fn);
            if (pending.length == 1) next();
        };
    }();
    /**
   * (Internal) Applies css properties to an element, similar to the jQuery 
   * css method.
   *
   * While this helper does assist with vendor prefixed property names, it 
   * does not perform any manipulation of values prior to setting styles.
   */ var css = function() {
        var cssPrefixes = [
            "Webkit",
            "O",
            "Moz",
            "ms"
        ], cssProps = {};
        function camelCase(string) {
            return string.replace(/^-ms-/, "ms-").replace(/-([\da-z])/gi, function(match, letter) {
                return letter.toUpperCase();
            });
        }
        function getVendorProp(name) {
            var style = document.body.style;
            if (name in style) return name;
            var i = cssPrefixes.length, capName = name.charAt(0).toUpperCase() + name.slice(1), vendorName;
            while(i--){
                vendorName = cssPrefixes[i] + capName;
                if (vendorName in style) return vendorName;
            }
            return name;
        }
        function getStyleProp(name) {
            name = camelCase(name);
            return cssProps[name] || (cssProps[name] = getVendorProp(name));
        }
        function applyCss(element, prop, value) {
            prop = getStyleProp(prop);
            element.style[prop] = value;
        }
        return function(element, properties) {
            var args = arguments, prop, value;
            if (args.length == 2) for(prop in properties){
                value = properties[prop];
                if (value !== undefined && properties.hasOwnProperty(prop)) applyCss(element, prop, value);
            }
            else applyCss(element, args[1], args[2]);
        };
    }();
    /**
   * (Internal) Determines if an element or space separated list of class names contains a class name.
   */ function hasClass(element, name) {
        var list = typeof element == "string" ? element : classList(element);
        return list.indexOf(" " + name + " ") >= 0;
    }
    /**
   * (Internal) Adds a class to an element.
   */ function addClass(element, name) {
        var oldList = classList(element), newList = oldList + name;
        if (hasClass(oldList, name)) return;
        // Trim the opening space.
        element.className = newList.substring(1);
    }
    /**
   * (Internal) Removes a class from an element.
   */ function removeClass(element, name) {
        var oldList = classList(element), newList;
        if (!hasClass(element, name)) return;
        // Replace the class name.
        newList = oldList.replace(" " + name + " ", " ");
        // Trim the opening and closing spaces.
        element.className = newList.substring(1, newList.length - 1);
    }
    /**
   * (Internal) Gets a space separated list of the class names on the element. 
   * The list is wrapped with a single space on each end to facilitate finding 
   * matches within the list.
   */ function classList(element) {
        return (" " + (element.className || "") + " ").replace(/\s+/gi, " ");
    }
    /**
   * (Internal) Removes an element from the DOM.
   */ function removeElement(element) {
        element && element.parentNode && element.parentNode.removeChild(element);
    }
    return NProgress;
});

},{}],"gkKU3":[function(require,module,exports) {
exports.interopDefault = function(a) {
    return a && a.__esModule ? a : {
        default: a
    };
};
exports.defineInteropFlag = function(a) {
    Object.defineProperty(a, "__esModule", {
        value: true
    });
};
exports.exportAll = function(source, dest) {
    Object.keys(source).forEach(function(key) {
        if (key === "default" || key === "__esModule" || dest.hasOwnProperty(key)) return;
        Object.defineProperty(dest, key, {
            enumerable: true,
            get: function() {
                return source[key];
            }
        });
    });
    return dest;
};
exports.export = function(dest, destName, get) {
    Object.defineProperty(dest, destName, {
        enumerable: true,
        get: get
    });
};

},{}],"4sPNn":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "Datepicker", ()=>(0, _datepickerJsDefault.default));
parcelHelpers.export(exports, "DateRangePicker", ()=>(0, _dateRangePickerJsDefault.default));
var _datepickerJs = require("./Datepicker.js");
var _datepickerJsDefault = parcelHelpers.interopDefault(_datepickerJs);
var _dateRangePickerJs = require("./DateRangePicker.js");
var _dateRangePickerJsDefault = parcelHelpers.interopDefault(_dateRangePickerJs);

},{"./Datepicker.js":"eHHLj","./DateRangePicker.js":"eY7zY","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"eHHLj":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("./lib/utils.js");
var _dateJs = require("./lib/date.js");
var _dateFormatJs = require("./lib/date-format.js");
var _domJs = require("./lib/dom.js");
var _eventJs = require("./lib/event.js");
var _baseLocalesJs = require("./i18n/base-locales.js");
var _defaultOptionsJs = require("./options/defaultOptions.js");
var _defaultOptionsJsDefault = parcelHelpers.interopDefault(_defaultOptionsJs);
var _processOptionsJs = require("./options/processOptions.js");
var _processOptionsJsDefault = parcelHelpers.interopDefault(_processOptionsJs);
var _pickerJs = require("./picker/Picker.js");
var _pickerJsDefault = parcelHelpers.interopDefault(_pickerJs);
var _functionsJs = require("./events/functions.js");
var _inputFieldListenersJs = require("./events/inputFieldListeners.js");
var _otherListenersJs = require("./events/otherListeners.js");
function stringifyDates(dates, config) {
    return dates.map((dt)=>(0, _dateFormatJs.formatDate)(dt, config.format, config.locale)).join(config.dateDelimiter);
}
// parse input dates and create an array of time values for selection
// returns undefined if there are no valid dates in inputDates
// when origDates (current selection) is passed, the function works to mix
// the input dates into the current selection
function processInputDates(datepicker, inputDates, clear = false) {
    // const {config, dates: origDates, rangepicker} = datepicker;
    const { config , dates: origDates , rangeSideIndex  } = datepicker;
    if (inputDates.length === 0) // empty input is considered valid unless origiDates is passed
    return clear ? [] : undefined;
    // const rangeEnd = rangepicker && datepicker === rangepicker.datepickers[1];
    let newDates = inputDates.reduce((dates, dt)=>{
        let date = (0, _dateFormatJs.parseDate)(dt, config.format, config.locale);
        if (date === undefined) return dates;
        // adjust to 1st of the month/Jan 1st of the year
        // or to the last day of the monh/Dec 31st of the year if the datepicker
        // is the range-end picker of a rangepicker
        date = (0, _dateJs.regularizeDate)(date, config.pickLevel, rangeSideIndex);
        if ((0, _utilsJs.isInRange)(date, config.minDate, config.maxDate) && !dates.includes(date) && !config.datesDisabled.includes(date) && (config.pickLevel > 0 || !config.daysOfWeekDisabled.includes(new Date(date).getDay()))) dates.push(date);
        return dates;
    }, []);
    if (newDates.length === 0) return;
    if (config.multidate && !clear) // get the synmetric difference between origDates and newDates
    newDates = newDates.reduce((dates, date)=>{
        if (!origDates.includes(date)) dates.push(date);
        return dates;
    }, origDates.filter((date)=>!newDates.includes(date)));
    // do length check always because user can input multiple dates regardless of the mode
    return config.maxNumberOfDates && newDates.length > config.maxNumberOfDates ? newDates.slice(config.maxNumberOfDates * -1) : newDates;
}
// refresh the UI elements
// modes: 1: input only, 2, picker only, 3 both
function refreshUI(datepicker, mode = 3, quickRender = true) {
    const { config , picker , inputField  } = datepicker;
    if (mode & 2) {
        const newView = picker.active ? config.pickLevel : config.startView;
        picker.update().changeView(newView).render(quickRender);
    }
    if (mode & 1 && inputField) inputField.value = stringifyDates(datepicker.dates, config);
}
function setDate(datepicker, inputDates, options) {
    let { clear , render , autohide , revert  } = options;
    if (render === undefined) render = true;
    if (!render) autohide = false;
    else if (autohide === undefined) autohide = datepicker.config.autohide;
    const newDates = processInputDates(datepicker, inputDates, clear);
    if (!newDates && !revert) return;
    if (newDates && newDates.toString() !== datepicker.dates.toString()) {
        datepicker.dates = newDates;
        refreshUI(datepicker, render ? 3 : 1);
        (0, _functionsJs.triggerDatepickerEvent)(datepicker, "changeDate");
    } else refreshUI(datepicker, 1);
    if (autohide) datepicker.hide();
}
class Datepicker {
    /**
   * Create a date picker
   * @param  {Element} element - element to bind a date picker
   * @param  {Object} [options] - config options
   * @param  {DateRangePicker} [rangepicker] - DateRangePicker instance the
   * date picker belongs to. Use this only when creating date picker as a part
   * of date range picker
   */ constructor(element, options = {}, rangepicker){
        element.datepicker = this;
        this.element = element;
        const config = this.config = Object.assign({
            buttonClass: options.buttonClass && String(options.buttonClass) || "button",
            container: null,
            defaultViewDate: (0, _dateJs.today)(),
            maxDate: undefined,
            minDate: undefined
        }, (0, _processOptionsJsDefault.default)((0, _defaultOptionsJsDefault.default), this));
        // configure by type
        const inline = this.inline = element.tagName !== "INPUT";
        let inputField;
        if (inline) config.container = element;
        else {
            if (options.container) // omit string type check because it doesn't guarantee to avoid errors
            // (invalid selector string causes abend with sytax error)
            config.container = options.container instanceof HTMLElement ? options.container : document.querySelector(options.container);
            inputField = this.inputField = element;
            inputField.classList.add("datepicker-input");
        }
        if (rangepicker) {
            // check validiry
            const index = rangepicker.inputs.indexOf(inputField);
            const datepickers = rangepicker.datepickers;
            if (index < 0 || index > 1 || !Array.isArray(datepickers)) throw Error("Invalid rangepicker object.");
            // attach itaelf to the rangepicker here so that processInputDates() can
            // determine if this is the range-end picker of the rangepicker while
            // setting inital values when pickLevel > 0
            datepickers[index] = this;
            // add getter for rangepicker
            Object.defineProperty(this, "rangepicker", {
                get () {
                    return rangepicker;
                }
            });
            Object.defineProperty(this, "rangeSideIndex", {
                get () {
                    return index;
                }
            });
        }
        // set up config
        this._options = options;
        Object.assign(config, (0, _processOptionsJsDefault.default)(options, this));
        // set initial dates
        let initialDates;
        if (inline) {
            initialDates = (0, _utilsJs.stringToArray)(element.dataset.date, config.dateDelimiter);
            delete element.dataset.date;
        } else initialDates = (0, _utilsJs.stringToArray)(inputField.value, config.dateDelimiter);
        this.dates = [];
        // process initial value
        const inputDateValues = processInputDates(this, initialDates);
        if (inputDateValues && inputDateValues.length > 0) this.dates = inputDateValues;
        if (inputField) inputField.value = stringifyDates(this.dates, config);
        const picker = this.picker = new (0, _pickerJsDefault.default)(this);
        if (inline) this.show();
        else {
            // set up event listeners in other modes
            const onMousedownDocument = (0, _otherListenersJs.onClickOutside).bind(null, this);
            const listeners = [
                [
                    inputField,
                    "keydown",
                    (0, _inputFieldListenersJs.onKeydown).bind(null, this)
                ],
                [
                    inputField,
                    "focus",
                    (0, _inputFieldListenersJs.onFocus).bind(null, this)
                ],
                [
                    inputField,
                    "mousedown",
                    (0, _inputFieldListenersJs.onMousedown).bind(null, this)
                ],
                [
                    inputField,
                    "click",
                    (0, _inputFieldListenersJs.onClickInput).bind(null, this)
                ],
                [
                    inputField,
                    "paste",
                    (0, _inputFieldListenersJs.onPaste).bind(null, this)
                ],
                [
                    document,
                    "mousedown",
                    onMousedownDocument
                ],
                [
                    document,
                    "touchstart",
                    onMousedownDocument
                ],
                [
                    window,
                    "resize",
                    picker.place.bind(picker)
                ]
            ];
            (0, _eventJs.registerListeners)(this, listeners);
        }
    }
    /**
   * Format Date object or time value in given format and language
   * @param  {Date|Number} date - date or time value to format
   * @param  {String|Object} format - format string or object that contains
   * toDisplay() custom formatter, whose signature is
   * - args:
   *   - date: {Date} - Date instance of the date passed to the method
   *   - format: {Object} - the format object passed to the method
   *   - locale: {Object} - locale for the language specified by `lang`
   * - return:
   *     {String} formatted date
   * @param  {String} [lang=en] - language code for the locale to use
   * @return {String} formatted date
   */ static formatDate(date, format, lang) {
        return (0, _dateFormatJs.formatDate)(date, format, lang && (0, _baseLocalesJs.locales)[lang] || (0, _baseLocalesJs.locales).en);
    }
    /**
   * Parse date string
   * @param  {String|Date|Number} dateStr - date string, Date object or time
   * value to parse
   * @param  {String|Object} format - format string or object that contains
   * toValue() custom parser, whose signature is
   * - args:
   *   - dateStr: {String|Date|Number} - the dateStr passed to the method
   *   - format: {Object} - the format object passed to the method
   *   - locale: {Object} - locale for the language specified by `lang`
   * - return:
   *     {Date|Number} parsed date or its time value
   * @param  {String} [lang=en] - language code for the locale to use
   * @return {Number} time value of parsed date
   */ static parseDate(dateStr, format, lang) {
        return (0, _dateFormatJs.parseDate)(dateStr, format, lang && (0, _baseLocalesJs.locales)[lang] || (0, _baseLocalesJs.locales).en);
    }
    /**
   * @type {Object} - Installed locales in `[languageCode]: localeObject` format
   * en`:_English (US)_ is pre-installed.
   */ static get locales() {
        return 0, _baseLocalesJs.locales;
    }
    /**
   * @type {Boolean} - Whether the picker element is shown. `true` whne shown
   */ get active() {
        return !!(this.picker && this.picker.active);
    }
    /**
   * @type {HTMLDivElement} - DOM object of picker element
   */ get pickerElement() {
        return this.picker ? this.picker.element : undefined;
    }
    /**
   * Set new values to the config options
   * @param {Object} options - config options to update
   */ setOptions(options) {
        const picker = this.picker;
        const newOptions = (0, _processOptionsJsDefault.default)(options, this);
        Object.assign(this._options, options);
        Object.assign(this.config, newOptions);
        picker.setOptions(newOptions);
        refreshUI(this, 3);
    }
    /**
   * Show the picker element
   */ show() {
        if (this.inputField) {
            if (this.inputField.disabled) return;
            if (!(0, _domJs.isActiveElement)(this.inputField) && !this.config.disableTouchKeyboard) {
                this._showing = true;
                this.inputField.focus();
                delete this._showing;
            }
        }
        this.picker.show();
    }
    /**
   * Hide the picker element
   * Not available on inline picker
   */ hide() {
        if (this.inline) return;
        this.picker.hide();
        this.picker.update().changeView(this.config.startView).render();
    }
    /**
   * Destroy the Datepicker instance
   * @return {Detepicker} - the instance destroyed
   */ destroy() {
        this.hide();
        (0, _eventJs.unregisterListeners)(this);
        this.picker.detach();
        if (!this.inline) this.inputField.classList.remove("datepicker-input");
        delete this.element.datepicker;
        return this;
    }
    /**
   * Get the selected date(s)
   *
   * The method returns a Date object of selected date by default, and returns
   * an array of selected dates in multidate mode. If format string is passed,
   * it returns date string(s) formatted in given format.
   *
   * @param  {String} [format] - Format string to stringify the date(s)
   * @return {Date|String|Date[]|String[]} - selected date(s), or if none is
   * selected, empty array in multidate mode and untitled in sigledate mode
   */ getDate(format) {
        const callback = format ? (date)=>(0, _dateFormatJs.formatDate)(date, format, this.config.locale) : (date)=>new Date(date);
        if (this.config.multidate) return this.dates.map(callback);
        if (this.dates.length > 0) return callback(this.dates[0]);
    }
    /**
   * Set selected date(s)
   *
   * In multidate mode, you can pass multiple dates as a series of arguments
   * or an array. (Since each date is parsed individually, the type of the
   * dates doesn't have to be the same.)
   * The given dates are used to toggle the select status of each date. The
   * number of selected dates is kept from exceeding the length set to
   * maxNumberOfDates.
   *
   * With clear: true option, the method can be used to clear the selection
   * and to replace the selection instead of toggling in multidate mode.
   * If the option is passed with no date arguments or an empty dates array,
   * it works as "clear" (clear the selection then set nothing), and if the
   * option is passed with new dates to select, it works as "replace" (clear
   * the selection then set the given dates)
   *
   * When render: false option is used, the method omits re-rendering the
   * picker element. In this case, you need to call refresh() method later in
   * order for the picker element to reflect the changes. The input field is
   * refreshed always regardless of this option.
   *
   * When invalid (unparsable, repeated, disabled or out-of-range) dates are
   * passed, the method ignores them and applies only valid ones. In the case
   * that all the given dates are invalid, which is distinguished from passing
   * no dates, the method considers it as an error and leaves the selection
   * untouched. (The input field also remains untouched unless revert: true
   * option is used.)
   *
   * @param {...(Date|Number|String)|Array} [dates] - Date strings, Date
   * objects, time values or mix of those for new selection
   * @param {Object} [options] - function options
   * - clear: {boolean} - Whether to clear the existing selection
   *     defualt: false
   * - render: {boolean} - Whether to re-render the picker element
   *     default: true
   * - autohide: {boolean} - Whether to hide the picker element after re-render
   *     Ignored when used with render: false
   *     default: config.autohide
   * - revert: {boolean} - Whether to refresh the input field when all the
   *     passed dates are invalid
   *     default: false
   */ setDate(...args) {
        const dates = [
            ...args
        ];
        const opts = {};
        const lastArg = (0, _utilsJs.lastItemOf)(args);
        if (typeof lastArg === "object" && !Array.isArray(lastArg) && !(lastArg instanceof Date) && lastArg) Object.assign(opts, dates.pop());
        const inputDates = Array.isArray(dates[0]) ? dates[0] : dates;
        setDate(this, inputDates, opts);
    }
    /**
   * Update the selected date(s) with input field's value
   * Not available on inline picker
   *
   * The input field will be refreshed with properly formatted date string.
   *
   * In the case that all the entered dates are invalid (unparsable, repeated,
   * disabled or out-of-range), whixh is distinguished from empty input field,
   * the method leaves the input field untouched as well as the selection by
   * default. If revert: true option is used in this case, the input field is
   * refreshed with the existing selection.
   *
   * @param  {Object} [options] - function options
   * - autohide: {boolean} - whether to hide the picker element after refresh
   *     default: false
   * - revert: {boolean} - Whether to refresh the input field when all the
   *     passed dates are invalid
   *     default: false
   */ update(options) {
        if (this.inline) return;
        const opts = Object.assign(options || {}, {
            clear: true,
            render: true
        });
        const inputDates = (0, _utilsJs.stringToArray)(this.inputField.value, this.config.dateDelimiter);
        setDate(this, inputDates, opts);
    }
    /**
   * Refresh the picker element and the associated input field
   * @param {String} [target] - target item when refreshing one item only
   * 'picker' or 'input'
   * @param {Boolean} [forceRender] - whether to re-render the picker element
   * regardless of its state instead of optimized refresh
   */ refresh(target, forceRender = false) {
        if (target && typeof target !== "string") {
            forceRender = target;
            target = undefined;
        }
        let mode;
        if (target === "picker") mode = 2;
        else if (target === "input") mode = 1;
        else mode = 3;
        refreshUI(this, mode, !forceRender);
    }
    /**
   * Enter edit mode
   * Not available on inline picker or when the picker element is hidden
   */ enterEditMode() {
        if (this.inline || !this.picker.active || this.editMode) return;
        this.editMode = true;
        this.inputField.classList.add("in-edit");
    }
    /**
   * Exit from edit mode
   * Not available on inline picker
   * @param  {Object} [options] - function options
   * - update: {boolean} - whether to call update() after exiting
   *     If false, input field is revert to the existing selection
   *     default: false
   */ exitEditMode(options) {
        if (this.inline || !this.editMode) return;
        const opts = Object.assign({
            update: false
        }, options);
        delete this.editMode;
        this.inputField.classList.remove("in-edit");
        if (opts.update) this.update(opts);
    }
}
exports.default = Datepicker;

},{"./lib/utils.js":"7MDex","./lib/date.js":"1PD5J","./lib/date-format.js":"kp7fb","./lib/dom.js":"wtAuE","./lib/event.js":"3Mw9Z","./i18n/base-locales.js":"bop0d","./options/defaultOptions.js":"fzk7Q","./options/processOptions.js":"30IQF","./picker/Picker.js":"e44C2","./events/functions.js":"8gUhk","./events/inputFieldListeners.js":"9slyU","./events/otherListeners.js":"33DOL","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"7MDex":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "hasProperty", ()=>hasProperty);
parcelHelpers.export(exports, "lastItemOf", ()=>lastItemOf);
// push only the items not included in the array
parcelHelpers.export(exports, "pushUnique", ()=>pushUnique);
parcelHelpers.export(exports, "stringToArray", ()=>stringToArray);
parcelHelpers.export(exports, "isInRange", ()=>isInRange);
parcelHelpers.export(exports, "limitToRange", ()=>limitToRange);
parcelHelpers.export(exports, "createTagRepeat", ()=>createTagRepeat);
// Remove the spacing surrounding tags for HTML parser not to create text nodes
// before/after elements
parcelHelpers.export(exports, "optimizeTemplateHTML", ()=>optimizeTemplateHTML);
function hasProperty(obj, prop) {
    return Object.prototype.hasOwnProperty.call(obj, prop);
}
function lastItemOf(arr) {
    return arr[arr.length - 1];
}
function pushUnique(arr, ...items) {
    items.forEach((item)=>{
        if (arr.includes(item)) return;
        arr.push(item);
    });
    return arr;
}
function stringToArray(str, separator) {
    // convert empty string to an empty array
    return str ? str.split(separator) : [];
}
function isInRange(testVal, min, max) {
    const minOK = min === undefined || testVal >= min;
    const maxOK = max === undefined || testVal <= max;
    return minOK && maxOK;
}
function limitToRange(val, min, max) {
    if (val < min) return min;
    if (val > max) return max;
    return val;
}
function createTagRepeat(tagName, repeat, attributes = {}, index = 0, html = "") {
    const openTagSrc = Object.keys(attributes).reduce((src, attr)=>{
        let val = attributes[attr];
        if (typeof val === "function") val = val(index);
        return `${src} ${attr}="${val}"`;
    }, tagName);
    html += `<${openTagSrc}></${tagName}>`;
    const next = index + 1;
    return next < repeat ? createTagRepeat(tagName, repeat, attributes, next, html) : html;
}
function optimizeTemplateHTML(html) {
    return html.replace(/>\s+/g, ">").replace(/\s+</, "<");
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"1PD5J":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "stripTime", ()=>stripTime);
parcelHelpers.export(exports, "today", ()=>today);
// Get the time value of the start of given date or year, month and day
parcelHelpers.export(exports, "dateValue", ()=>dateValue);
parcelHelpers.export(exports, "addDays", ()=>addDays);
parcelHelpers.export(exports, "addWeeks", ()=>addWeeks);
parcelHelpers.export(exports, "addMonths", ()=>addMonths);
parcelHelpers.export(exports, "addYears", ()=>addYears);
// Get the date of the specified day of the week of given base date
parcelHelpers.export(exports, "dayOfTheWeekOf", ()=>dayOfTheWeekOf);
// Get the ISO week of a date
parcelHelpers.export(exports, "getWeek", ()=>getWeek);
// Get the start year of the period of years that includes given date
// years: length of the year period
parcelHelpers.export(exports, "startOfYearPeriod", ()=>startOfYearPeriod);
// Convert date to the first/last date of the month/year of the date
parcelHelpers.export(exports, "regularizeDate", ()=>regularizeDate);
function stripTime(timeValue) {
    return new Date(timeValue).setHours(0, 0, 0, 0);
}
function today() {
    return new Date().setHours(0, 0, 0, 0);
}
function dateValue(...args) {
    switch(args.length){
        case 0:
            return today();
        case 1:
            return stripTime(args[0]);
    }
    // use setFullYear() to keep 2-digit year from being mapped to 1900-1999
    const newDate = new Date(0);
    newDate.setFullYear(...args);
    return newDate.setHours(0, 0, 0, 0);
}
function addDays(date, amount) {
    const newDate = new Date(date);
    return newDate.setDate(newDate.getDate() + amount);
}
function addWeeks(date, amount) {
    return addDays(date, amount * 7);
}
function addMonths(date, amount) {
    // If the day of the date is not in the new month, the last day of the new
    // month will be returned. e.g. Jan 31 + 1 month → Feb 28 (not Mar 03)
    const newDate = new Date(date);
    const monthsToSet = newDate.getMonth() + amount;
    let expectedMonth = monthsToSet % 12;
    if (expectedMonth < 0) expectedMonth += 12;
    const time = newDate.setMonth(monthsToSet);
    return newDate.getMonth() !== expectedMonth ? newDate.setDate(0) : time;
}
function addYears(date, amount) {
    // If the date is Feb 29 and the new year is not a leap year, Feb 28 of the
    // new year will be returned.
    const newDate = new Date(date);
    const expectedMonth = newDate.getMonth();
    const time = newDate.setFullYear(newDate.getFullYear() + amount);
    return expectedMonth === 1 && newDate.getMonth() === 2 ? newDate.setDate(0) : time;
}
// Calculate the distance bettwen 2 days of the week
function dayDiff(day, from) {
    return (day - from + 7) % 7;
}
function dayOfTheWeekOf(baseDate, dayOfWeek, weekStart = 0) {
    const baseDay = new Date(baseDate).getDay();
    return addDays(baseDate, dayDiff(dayOfWeek, weekStart) - dayDiff(baseDay, weekStart));
}
function getWeek(date) {
    // start of ISO week is Monday
    const thuOfTheWeek = dayOfTheWeekOf(date, 4, 1);
    // 1st week == the week where the 4th of January is in
    const firstThu = dayOfTheWeekOf(new Date(thuOfTheWeek).setMonth(0, 4), 4, 1);
    return Math.round((thuOfTheWeek - firstThu) / 604800000) + 1;
}
function startOfYearPeriod(date, years) {
    /* @see https://en.wikipedia.org/wiki/Year_zero#ISO_8601 */ const year = new Date(date).getFullYear();
    return Math.floor(year / years) * years;
}
function regularizeDate(date, timeSpan, useLastDate) {
    if (timeSpan !== 1 && timeSpan !== 2) return date;
    const newDate = new Date(date);
    if (timeSpan === 1) useLastDate ? newDate.setMonth(newDate.getMonth() + 1, 0) : newDate.setDate(1);
    else useLastDate ? newDate.setFullYear(newDate.getFullYear() + 1, 0, 0) : newDate.setMonth(0, 1);
    return newDate.setHours(0, 0, 0, 0);
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"kp7fb":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "reFormatTokens", ()=>reFormatTokens);
parcelHelpers.export(exports, "reNonDateParts", ()=>reNonDateParts);
parcelHelpers.export(exports, "parseDate", ()=>parseDate);
parcelHelpers.export(exports, "formatDate", ()=>formatDate);
var _dateJs = require("./date.js");
var _utilsJs = require("./utils.js");
const reFormatTokens = /dd?|DD?|mm?|MM?|yy?(?:yy)?/;
const reNonDateParts = /[\s!-/:-@[-`{-~年月日]+/;
// cache for persed formats
let knownFormats = {};
// parse funtions for date parts
const parseFns = {
    y (date, year) {
        return new Date(date).setFullYear(parseInt(year, 10));
    },
    m (date, month, locale) {
        const newDate = new Date(date);
        let monthIndex = parseInt(month, 10) - 1;
        if (isNaN(monthIndex)) {
            if (!month) return NaN;
            const monthName = month.toLowerCase();
            const compareNames = (name)=>name.toLowerCase().startsWith(monthName);
            // compare with both short and full names because some locales have periods
            // in the short names (not equal to the first X letters of the full names)
            monthIndex = locale.monthsShort.findIndex(compareNames);
            if (monthIndex < 0) monthIndex = locale.months.findIndex(compareNames);
            if (monthIndex < 0) return NaN;
        }
        newDate.setMonth(monthIndex);
        return newDate.getMonth() !== normalizeMonth(monthIndex) ? newDate.setDate(0) : newDate.getTime();
    },
    d (date, day) {
        return new Date(date).setDate(parseInt(day, 10));
    }
};
// format functions for date parts
const formatFns = {
    d (date) {
        return date.getDate();
    },
    dd (date) {
        return padZero(date.getDate(), 2);
    },
    D (date, locale) {
        return locale.daysShort[date.getDay()];
    },
    DD (date, locale) {
        return locale.days[date.getDay()];
    },
    m (date) {
        return date.getMonth() + 1;
    },
    mm (date) {
        return padZero(date.getMonth() + 1, 2);
    },
    M (date, locale) {
        return locale.monthsShort[date.getMonth()];
    },
    MM (date, locale) {
        return locale.months[date.getMonth()];
    },
    y (date) {
        return date.getFullYear();
    },
    yy (date) {
        return padZero(date.getFullYear(), 2).slice(-2);
    },
    yyyy (date) {
        return padZero(date.getFullYear(), 4);
    }
};
// get month index in normal range (0 - 11) from any number
function normalizeMonth(monthIndex) {
    return monthIndex > -1 ? monthIndex % 12 : normalizeMonth(monthIndex + 12);
}
function padZero(num, length) {
    return num.toString().padStart(length, "0");
}
function parseFormatString(format) {
    if (typeof format !== "string") throw new Error("Invalid date format.");
    if (format in knownFormats) return knownFormats[format];
    // sprit the format string into parts and seprators
    const separators = format.split(reFormatTokens);
    const parts = format.match(new RegExp(reFormatTokens, "g"));
    if (separators.length === 0 || !parts) throw new Error("Invalid date format.");
    // collect format functions used in the format
    const partFormatters = parts.map((token)=>formatFns[token]);
    // collect parse function keys used in the format
    // iterate over parseFns' keys in order to keep the order of the keys.
    const partParserKeys = Object.keys(parseFns).reduce((keys, key)=>{
        const token = parts.find((part)=>part[0] !== "D" && part[0].toLowerCase() === key);
        if (token) keys.push(key);
        return keys;
    }, []);
    return knownFormats[format] = {
        parser (dateStr, locale) {
            const dateParts = dateStr.split(reNonDateParts).reduce((dtParts, part, index)=>{
                if (part.length > 0 && parts[index]) {
                    const token = parts[index][0];
                    if (token === "M") dtParts.m = part;
                    else if (token !== "D") dtParts[token] = part;
                }
                return dtParts;
            }, {});
            // iterate over partParserkeys so that the parsing is made in the oder
            // of year, month and day to prevent the day parser from correcting last
            // day of month wrongly
            return partParserKeys.reduce((origDate, key)=>{
                const newDate = parseFns[key](origDate, dateParts[key], locale);
                // ingnore the part failed to parse
                return isNaN(newDate) ? origDate : newDate;
            }, (0, _dateJs.today)());
        },
        formatter (date, locale) {
            let dateStr = partFormatters.reduce((str, fn, index)=>{
                return str += `${separators[index]}${fn(date, locale)}`;
            }, "");
            // separators' length is always parts' length + 1,
            return dateStr += (0, _utilsJs.lastItemOf)(separators);
        }
    };
}
function parseDate(dateStr, format, locale) {
    if (dateStr instanceof Date || typeof dateStr === "number") {
        const date = (0, _dateJs.stripTime)(dateStr);
        return isNaN(date) ? undefined : date;
    }
    if (!dateStr) return undefined;
    if (dateStr === "today") return (0, _dateJs.today)();
    if (format && format.toValue) {
        const date1 = format.toValue(dateStr, format, locale);
        return isNaN(date1) ? undefined : (0, _dateJs.stripTime)(date1);
    }
    return parseFormatString(format).parser(dateStr, locale);
}
function formatDate(date, format, locale) {
    if (isNaN(date) || !date && date !== 0) return "";
    const dateObj = typeof date === "number" ? new Date(date) : date;
    if (format.toDisplay) return format.toDisplay(dateObj, format, locale);
    return parseFormatString(format).formatter(dateObj, locale);
}

},{"./date.js":"1PD5J","./utils.js":"7MDex","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"wtAuE":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "parseHTML", ()=>parseHTML);
parcelHelpers.export(exports, "getParent", ()=>getParent);
parcelHelpers.export(exports, "isActiveElement", ()=>isActiveElement);
// equivalent to jQuery's :visble
parcelHelpers.export(exports, "isVisible", ()=>isVisible);
parcelHelpers.export(exports, "hideElement", ()=>hideElement);
parcelHelpers.export(exports, "showElement", ()=>showElement);
parcelHelpers.export(exports, "emptyChildNodes", ()=>emptyChildNodes);
parcelHelpers.export(exports, "replaceChildNodes", ()=>replaceChildNodes);
const range = document.createRange();
function parseHTML(html) {
    return range.createContextualFragment(html);
}
function getParent(el) {
    return el.parentElement || (el.parentNode instanceof ShadowRoot ? el.parentNode.host : undefined);
}
function isActiveElement(el) {
    return el.getRootNode().activeElement === el;
}
function isVisible(el) {
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
}
function hideElement(el) {
    if (el.style.display === "none") return;
    // back up the existing display setting in data-style-display
    if (el.style.display) el.dataset.styleDisplay = el.style.display;
    el.style.display = "none";
}
function showElement(el) {
    if (el.style.display !== "none") return;
    if (el.dataset.styleDisplay) {
        // restore backed-up dispay property
        el.style.display = el.dataset.styleDisplay;
        delete el.dataset.styleDisplay;
    } else el.style.display = "";
}
function emptyChildNodes(el) {
    if (el.firstChild) {
        el.removeChild(el.firstChild);
        emptyChildNodes(el);
    }
}
function replaceChildNodes(el, newChildNodes) {
    emptyChildNodes(el);
    if (newChildNodes instanceof DocumentFragment) el.appendChild(newChildNodes);
    else if (typeof newChildNodes === "string") el.appendChild(parseHTML(newChildNodes));
    else if (typeof newChildNodes.forEach === "function") newChildNodes.forEach((node)=>{
        el.appendChild(node);
    });
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"3Mw9Z":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
// Register event listeners to a key object
// listeners: array of listener definitions;
//   - each definition must be a flat array of event target and the arguments
//     used to call addEventListener() on the target
parcelHelpers.export(exports, "registerListeners", ()=>registerListeners);
parcelHelpers.export(exports, "unregisterListeners", ()=>unregisterListeners);
// Search for the actual target of a delegated event
parcelHelpers.export(exports, "findElementInEventPath", ()=>findElementInEventPath);
const listenerRegistry = new WeakMap();
const { addEventListener , removeEventListener  } = EventTarget.prototype;
function registerListeners(keyObj, listeners) {
    let registered = listenerRegistry.get(keyObj);
    if (!registered) {
        registered = [];
        listenerRegistry.set(keyObj, registered);
    }
    listeners.forEach((listener)=>{
        addEventListener.call(...listener);
        registered.push(listener);
    });
}
function unregisterListeners(keyObj) {
    let listeners = listenerRegistry.get(keyObj);
    if (!listeners) return;
    listeners.forEach((listener)=>{
        removeEventListener.call(...listener);
    });
    listenerRegistry.delete(keyObj);
}
// Event.composedPath() polyfill for Edge
// based on https://gist.github.com/kleinfreund/e9787d73776c0e3750dcfcdc89f100ec
if (!Event.prototype.composedPath) {
    const getComposedPath = (node, path = [])=>{
        path.push(node);
        let parent;
        if (node.parentNode) parent = node.parentNode;
        else if (node.host) parent = node.host;
        else if (node.defaultView) parent = node.defaultView;
        return parent ? getComposedPath(parent, path) : path;
    };
    Event.prototype.composedPath = function() {
        return getComposedPath(this.target);
    };
}
function findFromPath(path, criteria, currentTarget) {
    const [node, ...rest] = path;
    if (criteria(node)) return node;
    if (node === currentTarget || node.tagName === "HTML" || rest.length === 0) // stop when reaching currentTarget or <html>
    return;
    return findFromPath(rest, criteria, currentTarget);
}
function findElementInEventPath(ev, selector) {
    const criteria = typeof selector === "function" ? selector : (el)=>el instanceof Element && el.matches(selector);
    return findFromPath(ev.composedPath(), criteria, ev.currentTarget);
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"bop0d":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "locales", ()=>locales);
const locales = {
    en: {
        days: [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ],
        daysShort: [
            "Sun",
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat"
        ],
        daysMin: [
            "Su",
            "Mo",
            "Tu",
            "We",
            "Th",
            "Fr",
            "Sa"
        ],
        months: [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ],
        monthsShort: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ],
        today: "Today",
        clear: "Clear",
        titleFormat: "MM y"
    }
};

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"fzk7Q":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
// config options updatable by setOptions() and their default values
const defaultOptions = {
    autohide: false,
    beforeShowDay: null,
    beforeShowDecade: null,
    beforeShowMonth: null,
    beforeShowYear: null,
    calendarWeeks: false,
    clearBtn: false,
    dateDelimiter: ",",
    datesDisabled: [],
    daysOfWeekDisabled: [],
    daysOfWeekHighlighted: [],
    defaultViewDate: undefined,
    disableTouchKeyboard: false,
    format: "mm/dd/yyyy",
    language: "en",
    maxDate: null,
    maxNumberOfDates: 1,
    maxView: 3,
    minDate: null,
    nextArrow: "\xbb",
    orientation: "auto",
    pickLevel: 0,
    prevArrow: "\xab",
    showDaysOfWeek: true,
    showOnClick: true,
    showOnFocus: true,
    startView: 0,
    title: "",
    todayBtn: false,
    todayBtnMode: 0,
    todayHighlight: false,
    updateOnBlur: true,
    weekStart: 0
};
exports.default = defaultOptions;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"30IQF":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../lib/utils.js");
var _dateJs = require("../lib/date.js");
var _dateFormatJs = require("../lib/date-format.js");
var _domJs = require("../lib/dom.js");
var _defaultOptionsJs = require("./defaultOptions.js");
var _defaultOptionsJsDefault = parcelHelpers.interopDefault(_defaultOptionsJs);
const { language: defaultLang , format: defaultFormat , weekStart: defaultWeekStart ,  } = (0, _defaultOptionsJsDefault.default);
// Reducer function to filter out invalid day-of-week from the input
function sanitizeDOW(dow, day) {
    return dow.length < 6 && day >= 0 && day < 7 ? (0, _utilsJs.pushUnique)(dow, day) : dow;
}
function calcEndOfWeek(startOfWeek) {
    return (startOfWeek + 6) % 7;
}
// validate input date. if invalid, fallback to the original value
function validateDate(value, format, locale, origValue) {
    const date = (0, _dateFormatJs.parseDate)(value, format, locale);
    return date !== undefined ? date : origValue;
}
// Validate viewId. if invalid, fallback to the original value
function validateViewId(value, origValue, max = 3) {
    const viewId = parseInt(value, 10);
    return viewId >= 0 && viewId <= max ? viewId : origValue;
}
function processOptions(options, datepicker) {
    const inOpts = Object.assign({}, options);
    const config = {};
    const locales = datepicker.constructor.locales;
    const rangeSideIndex = datepicker.rangeSideIndex;
    let { format , language , locale , maxDate , maxView , minDate , pickLevel , startView , weekStart ,  } = datepicker.config || {};
    if (inOpts.language) {
        let lang;
        if (inOpts.language !== language) {
            if (locales[inOpts.language]) lang = inOpts.language;
            else {
                // Check if langauge + region tag can fallback to the one without
                // region (e.g. fr-CA → fr)
                lang = inOpts.language.split("-")[0];
                if (locales[lang] === undefined) lang = false;
            }
        }
        delete inOpts.language;
        if (lang) {
            language = config.language = lang;
            // update locale as well when updating language
            const origLocale = locale || locales[defaultLang];
            // use default language's properties for the fallback
            locale = Object.assign({
                format: defaultFormat,
                weekStart: defaultWeekStart
            }, locales[defaultLang]);
            if (language !== defaultLang) Object.assign(locale, locales[language]);
            config.locale = locale;
            // if format and/or weekStart are the same as old locale's defaults,
            // update them to new locale's defaults
            if (format === origLocale.format) format = config.format = locale.format;
            if (weekStart === origLocale.weekStart) {
                weekStart = config.weekStart = locale.weekStart;
                config.weekEnd = calcEndOfWeek(locale.weekStart);
            }
        }
    }
    if (inOpts.format) {
        const hasToDisplay = typeof inOpts.format.toDisplay === "function";
        const hasToValue = typeof inOpts.format.toValue === "function";
        const validFormatString = (0, _dateFormatJs.reFormatTokens).test(inOpts.format);
        if (hasToDisplay && hasToValue || validFormatString) format = config.format = inOpts.format;
        delete inOpts.format;
    }
    //*** pick level ***//
    let newPickLevel = pickLevel;
    if (inOpts.pickLevel !== undefined) {
        newPickLevel = validateViewId(inOpts.pickLevel, 2);
        delete inOpts.pickLevel;
    }
    if (newPickLevel !== pickLevel) {
        if (newPickLevel > pickLevel) {
            // complement current minDate/madDate so that the existing range will be
            // expanded to fit the new level later
            if (inOpts.minDate === undefined) inOpts.minDate = minDate;
            if (inOpts.maxDate === undefined) inOpts.maxDate = maxDate;
        }
        // complement datesDisabled so that it will be reset later
        if (!inOpts.datesDisabled) inOpts.datesDisabled = [];
        pickLevel = config.pickLevel = newPickLevel;
    }
    //*** dates ***//
    // while min and maxDate for "no limit" in the options are better to be null
    // (especially when updating), the ones in the config have to be undefined
    // because null is treated as 0 (= unix epoch) when comparing with time value
    let minDt = minDate;
    let maxDt = maxDate;
    if (inOpts.minDate !== undefined) {
        const defaultMinDt = (0, _dateJs.dateValue)(0, 0, 1);
        minDt = inOpts.minDate === null ? defaultMinDt // set 0000-01-01 to prevent negative values for year
         : validateDate(inOpts.minDate, format, locale, minDt);
        if (minDt !== defaultMinDt) minDt = (0, _dateJs.regularizeDate)(minDt, pickLevel, false);
        delete inOpts.minDate;
    }
    if (inOpts.maxDate !== undefined) {
        maxDt = inOpts.maxDate === null ? undefined : validateDate(inOpts.maxDate, format, locale, maxDt);
        if (maxDt !== undefined) maxDt = (0, _dateJs.regularizeDate)(maxDt, pickLevel, true);
        delete inOpts.maxDate;
    }
    if (maxDt < minDt) {
        minDate = config.minDate = maxDt;
        maxDate = config.maxDate = minDt;
    } else {
        if (minDate !== minDt) minDate = config.minDate = minDt;
        if (maxDate !== maxDt) maxDate = config.maxDate = maxDt;
    }
    if (inOpts.datesDisabled) {
        config.datesDisabled = inOpts.datesDisabled.reduce((dates, dt)=>{
            const date = (0, _dateFormatJs.parseDate)(dt, format, locale);
            return date !== undefined ? (0, _utilsJs.pushUnique)(dates, (0, _dateJs.regularizeDate)(date, pickLevel, rangeSideIndex)) : dates;
        }, []);
        delete inOpts.datesDisabled;
    }
    if (inOpts.defaultViewDate !== undefined) {
        const viewDate = (0, _dateFormatJs.parseDate)(inOpts.defaultViewDate, format, locale);
        if (viewDate !== undefined) config.defaultViewDate = viewDate;
        delete inOpts.defaultViewDate;
    }
    //*** days of week ***//
    if (inOpts.weekStart !== undefined) {
        const wkStart = Number(inOpts.weekStart) % 7;
        if (!isNaN(wkStart)) {
            weekStart = config.weekStart = wkStart;
            config.weekEnd = calcEndOfWeek(wkStart);
        }
        delete inOpts.weekStart;
    }
    if (inOpts.daysOfWeekDisabled) {
        config.daysOfWeekDisabled = inOpts.daysOfWeekDisabled.reduce(sanitizeDOW, []);
        delete inOpts.daysOfWeekDisabled;
    }
    if (inOpts.daysOfWeekHighlighted) {
        config.daysOfWeekHighlighted = inOpts.daysOfWeekHighlighted.reduce(sanitizeDOW, []);
        delete inOpts.daysOfWeekHighlighted;
    }
    //*** multi date ***//
    if (inOpts.maxNumberOfDates !== undefined) {
        const maxNumberOfDates = parseInt(inOpts.maxNumberOfDates, 10);
        if (maxNumberOfDates >= 0) {
            config.maxNumberOfDates = maxNumberOfDates;
            config.multidate = maxNumberOfDates !== 1;
        }
        delete inOpts.maxNumberOfDates;
    }
    if (inOpts.dateDelimiter) {
        config.dateDelimiter = String(inOpts.dateDelimiter);
        delete inOpts.dateDelimiter;
    }
    //*** view ***//
    let newMaxView = maxView;
    if (inOpts.maxView !== undefined) {
        newMaxView = validateViewId(inOpts.maxView, maxView);
        delete inOpts.maxView;
    }
    // ensure max view >= pick level
    newMaxView = pickLevel > newMaxView ? pickLevel : newMaxView;
    if (newMaxView !== maxView) maxView = config.maxView = newMaxView;
    let newStartView = startView;
    if (inOpts.startView !== undefined) {
        newStartView = validateViewId(inOpts.startView, newStartView);
        delete inOpts.startView;
    }
    // ensure pick level <= start view <= max view
    if (newStartView < pickLevel) newStartView = pickLevel;
    else if (newStartView > maxView) newStartView = maxView;
    if (newStartView !== startView) config.startView = newStartView;
    //*** template ***//
    if (inOpts.prevArrow) {
        const prevArrow = (0, _domJs.parseHTML)(inOpts.prevArrow);
        if (prevArrow.childNodes.length > 0) config.prevArrow = prevArrow.childNodes;
        delete inOpts.prevArrow;
    }
    if (inOpts.nextArrow) {
        const nextArrow = (0, _domJs.parseHTML)(inOpts.nextArrow);
        if (nextArrow.childNodes.length > 0) config.nextArrow = nextArrow.childNodes;
        delete inOpts.nextArrow;
    }
    //*** misc ***//
    if (inOpts.disableTouchKeyboard !== undefined) {
        config.disableTouchKeyboard = "ontouchstart" in document && !!inOpts.disableTouchKeyboard;
        delete inOpts.disableTouchKeyboard;
    }
    if (inOpts.orientation) {
        const orientation = inOpts.orientation.toLowerCase().split(/\s+/g);
        config.orientation = {
            x: orientation.find((x)=>x === "left" || x === "right") || "auto",
            y: orientation.find((y)=>y === "top" || y === "bottom") || "auto"
        };
        delete inOpts.orientation;
    }
    if (inOpts.todayBtnMode !== undefined) {
        switch(inOpts.todayBtnMode){
            case 0:
            case 1:
                config.todayBtnMode = inOpts.todayBtnMode;
        }
        delete inOpts.todayBtnMode;
    }
    //*** copy the rest ***//
    Object.keys(inOpts).forEach((key)=>{
        if (inOpts[key] !== undefined && (0, _utilsJs.hasProperty)((0, _defaultOptionsJsDefault.default), key)) config[key] = inOpts[key];
    });
    return config;
}
exports.default = processOptions;

},{"../lib/utils.js":"7MDex","../lib/date.js":"1PD5J","../lib/date-format.js":"kp7fb","../lib/dom.js":"wtAuE","./defaultOptions.js":"fzk7Q","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"e44C2":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../lib/utils.js");
var _dateJs = require("../lib/date.js");
var _domJs = require("../lib/dom.js");
var _eventJs = require("../lib/event.js");
var _pickerTemplateJs = require("./templates/pickerTemplate.js");
var _pickerTemplateJsDefault = parcelHelpers.interopDefault(_pickerTemplateJs);
var _daysViewJs = require("./views/DaysView.js");
var _daysViewJsDefault = parcelHelpers.interopDefault(_daysViewJs);
var _monthsViewJs = require("./views/MonthsView.js");
var _monthsViewJsDefault = parcelHelpers.interopDefault(_monthsViewJs);
var _yearsViewJs = require("./views/YearsView.js");
var _yearsViewJsDefault = parcelHelpers.interopDefault(_yearsViewJs);
var _functionsJs = require("../events/functions.js");
var _pickerListenersJs = require("../events/pickerListeners.js");
const orientClasses = [
    "left",
    "top",
    "right",
    "bottom"
].reduce((obj, key)=>{
    obj[key] = `datepicker-orient-${key}`;
    return obj;
}, {});
const toPx = (num)=>num ? `${num}px` : num;
function processPickerOptions(picker, options) {
    if (options.title !== undefined) {
        if (options.title) {
            picker.controls.title.textContent = options.title;
            (0, _domJs.showElement)(picker.controls.title);
        } else {
            picker.controls.title.textContent = "";
            (0, _domJs.hideElement)(picker.controls.title);
        }
    }
    if (options.prevArrow) {
        const prevBtn = picker.controls.prevBtn;
        (0, _domJs.emptyChildNodes)(prevBtn);
        options.prevArrow.forEach((node)=>{
            prevBtn.appendChild(node.cloneNode(true));
        });
    }
    if (options.nextArrow) {
        const nextBtn = picker.controls.nextBtn;
        (0, _domJs.emptyChildNodes)(nextBtn);
        options.nextArrow.forEach((node)=>{
            nextBtn.appendChild(node.cloneNode(true));
        });
    }
    if (options.locale) {
        picker.controls.todayBtn.textContent = options.locale.today;
        picker.controls.clearBtn.textContent = options.locale.clear;
    }
    if (options.todayBtn !== undefined) {
        if (options.todayBtn) (0, _domJs.showElement)(picker.controls.todayBtn);
        else (0, _domJs.hideElement)(picker.controls.todayBtn);
    }
    if ((0, _utilsJs.hasProperty)(options, "minDate") || (0, _utilsJs.hasProperty)(options, "maxDate")) {
        const { minDate , maxDate  } = picker.datepicker.config;
        picker.controls.todayBtn.disabled = !(0, _utilsJs.isInRange)((0, _dateJs.today)(), minDate, maxDate);
    }
    if (options.clearBtn !== undefined) {
        if (options.clearBtn) (0, _domJs.showElement)(picker.controls.clearBtn);
        else (0, _domJs.hideElement)(picker.controls.clearBtn);
    }
}
// Compute view date to reset, which will be...
// - the last item of the selected dates or defaultViewDate if no selection
// - limitted to minDate or maxDate if it exceeds the range
function computeResetViewDate(datepicker) {
    const { dates , config  } = datepicker;
    const viewDate = dates.length > 0 ? (0, _utilsJs.lastItemOf)(dates) : config.defaultViewDate;
    return (0, _utilsJs.limitToRange)(viewDate, config.minDate, config.maxDate);
}
// Change current view's view date
function setViewDate(picker, newDate) {
    const oldViewDate = new Date(picker.viewDate);
    const newViewDate = new Date(newDate);
    const { id , year , first , last  } = picker.currentView;
    const viewYear = newViewDate.getFullYear();
    picker.viewDate = newDate;
    if (viewYear !== oldViewDate.getFullYear()) (0, _functionsJs.triggerDatepickerEvent)(picker.datepicker, "changeYear");
    if (newViewDate.getMonth() !== oldViewDate.getMonth()) (0, _functionsJs.triggerDatepickerEvent)(picker.datepicker, "changeMonth");
    // return whether the new date is in different period on time from the one
    // displayed in the current view
    // when true, the view needs to be re-rendered on the next UI refresh.
    switch(id){
        case 0:
            return newDate < first || newDate > last;
        case 1:
            return viewYear !== year;
        default:
            return viewYear < first || viewYear > last;
    }
}
function getTextDirection(el) {
    return window.getComputedStyle(el).direction;
}
// find the closet scrollable ancestor elemnt under the body
function findScrollParents(el) {
    const parent = (0, _domJs.getParent)(el);
    if (parent === document.body || !parent) return;
    // checking overflow only is enough because computed overflow cannot be
    // visible or a combination of visible and other when either axis is set
    // to other than visible.
    // (Setting one axis to other than 'visible' while the other is 'visible'
    // results in the other axis turning to 'auto')
    return window.getComputedStyle(parent).overflow !== "visible" ? parent : findScrollParents(parent);
}
class Picker {
    constructor(datepicker){
        const { config  } = this.datepicker = datepicker;
        const template = (0, _pickerTemplateJsDefault.default).replace(/%buttonClass%/g, config.buttonClass);
        const element = this.element = (0, _domJs.parseHTML)(template).firstChild;
        const [header, main, footer] = element.firstChild.children;
        const title = header.firstElementChild;
        const [prevBtn, viewSwitch, nextBtn] = header.lastElementChild.children;
        const [todayBtn, clearBtn] = footer.firstChild.children;
        const controls = {
            title,
            prevBtn,
            viewSwitch,
            nextBtn,
            todayBtn,
            clearBtn
        };
        this.main = main;
        this.controls = controls;
        const elementClass = datepicker.inline ? "inline" : "dropdown";
        element.classList.add(`datepicker-${elementClass}`);
        processPickerOptions(this, config);
        this.viewDate = computeResetViewDate(datepicker);
        // set up event listeners
        (0, _eventJs.registerListeners)(datepicker, [
            [
                element,
                "mousedown",
                (0, _pickerListenersJs.onMousedownPicker)
            ],
            [
                main,
                "click",
                (0, _pickerListenersJs.onClickView).bind(null, datepicker)
            ],
            [
                controls.viewSwitch,
                "click",
                (0, _pickerListenersJs.onClickViewSwitch).bind(null, datepicker)
            ],
            [
                controls.prevBtn,
                "click",
                (0, _pickerListenersJs.onClickPrevBtn).bind(null, datepicker)
            ],
            [
                controls.nextBtn,
                "click",
                (0, _pickerListenersJs.onClickNextBtn).bind(null, datepicker)
            ],
            [
                controls.todayBtn,
                "click",
                (0, _pickerListenersJs.onClickTodayBtn).bind(null, datepicker)
            ],
            [
                controls.clearBtn,
                "click",
                (0, _pickerListenersJs.onClickClearBtn).bind(null, datepicker)
            ], 
        ]);
        // set up views
        this.views = [
            new (0, _daysViewJsDefault.default)(this),
            new (0, _monthsViewJsDefault.default)(this),
            new (0, _yearsViewJsDefault.default)(this, {
                id: 2,
                name: "years",
                cellClass: "year",
                step: 1
            }),
            new (0, _yearsViewJsDefault.default)(this, {
                id: 3,
                name: "decades",
                cellClass: "decade",
                step: 10
            }), 
        ];
        this.currentView = this.views[config.startView];
        this.currentView.render();
        this.main.appendChild(this.currentView.element);
        if (config.container) config.container.appendChild(this.element);
        else datepicker.inputField.after(this.element);
    }
    setOptions(options) {
        processPickerOptions(this, options);
        this.views.forEach((view)=>{
            view.init(options, false);
        });
        this.currentView.render();
    }
    detach() {
        this.element.remove();
    }
    show() {
        if (this.active) return;
        const { datepicker , element  } = this;
        if (datepicker.inline) element.classList.add("active");
        else {
            // ensure picker's direction matches input's
            const inputDirection = getTextDirection(datepicker.inputField);
            if (inputDirection !== getTextDirection((0, _domJs.getParent)(element))) element.dir = inputDirection;
            else if (element.dir) element.removeAttribute("dir");
            element.style.visiblity = "hidden";
            element.classList.add("active");
            this.place();
            element.style.visiblity = "";
            if (datepicker.config.disableTouchKeyboard) datepicker.inputField.blur();
        }
        this.active = true;
        (0, _functionsJs.triggerDatepickerEvent)(datepicker, "show");
    }
    hide() {
        if (!this.active) return;
        this.datepicker.exitEditMode();
        this.element.classList.remove("active");
        this.active = false;
        (0, _functionsJs.triggerDatepickerEvent)(this.datepicker, "hide");
    }
    place() {
        const { classList , offsetParent , style  } = this.element;
        const { config , inputField  } = this.datepicker;
        const { width: calendarWidth , height: calendarHeight ,  } = this.element.getBoundingClientRect();
        const { left: inputLeft , top: inputTop , right: inputRight , bottom: inputBottom , width: inputWidth , height: inputHeight  } = inputField.getBoundingClientRect();
        let { x: orientX , y: orientY  } = config.orientation;
        let left = inputLeft;
        let top = inputTop;
        // caliculate offsetLeft/Top of inputField
        if (offsetParent === document.body || !offsetParent) {
            left += window.scrollX;
            top += window.scrollY;
        } else {
            const offsetParentRect = offsetParent.getBoundingClientRect();
            left -= offsetParentRect.left - offsetParent.scrollLeft;
            top -= offsetParentRect.top - offsetParent.scrollTop;
        }
        // caliculate the boundaries of the visible area that contains inputField
        const scrollParent = findScrollParents(inputField);
        let scrollAreaLeft = 0;
        let scrollAreaTop = 0;
        let { clientWidth: scrollAreaRight , clientHeight: scrollAreaBottom ,  } = document.documentElement;
        if (scrollParent) {
            const scrollParentRect = scrollParent.getBoundingClientRect();
            if (scrollParentRect.top > 0) scrollAreaTop = scrollParentRect.top;
            if (scrollParentRect.left > 0) scrollAreaLeft = scrollParentRect.left;
            if (scrollParentRect.right < scrollAreaRight) scrollAreaRight = scrollParentRect.right;
            if (scrollParentRect.bottom < scrollAreaBottom) scrollAreaBottom = scrollParentRect.bottom;
        }
        // determine the horizontal orientation and left position
        let adjustment = 0;
        if (orientX === "auto") {
            if (inputLeft < scrollAreaLeft) {
                orientX = "left";
                adjustment = scrollAreaLeft - inputLeft;
            } else if (inputLeft + calendarWidth > scrollAreaRight) {
                orientX = "right";
                if (scrollAreaRight < inputRight) adjustment = scrollAreaRight - inputRight;
            } else if (getTextDirection(inputField) === "rtl") orientX = inputRight - calendarWidth < scrollAreaLeft ? "left" : "right";
            else orientX = "left";
        }
        if (orientX === "right") left += inputWidth - calendarWidth;
        left += adjustment;
        // determine the vertical orientation and top position
        if (orientY === "auto") {
            if (inputTop - calendarHeight > scrollAreaTop) orientY = inputBottom + calendarHeight > scrollAreaBottom ? "top" : "bottom";
            else orientY = "bottom";
        }
        if (orientY === "top") top -= calendarHeight;
        else top += inputHeight;
        classList.remove(...Object.values(orientClasses));
        classList.add(orientClasses[orientX], orientClasses[orientY]);
        style.left = toPx(left);
        style.top = toPx(top);
    }
    setViewSwitchLabel(labelText) {
        this.controls.viewSwitch.textContent = labelText;
    }
    setPrevBtnDisabled(disabled) {
        this.controls.prevBtn.disabled = disabled;
    }
    setNextBtnDisabled(disabled) {
        this.controls.nextBtn.disabled = disabled;
    }
    changeView(viewId) {
        const oldView = this.currentView;
        const newView = this.views[viewId];
        if (newView.id !== oldView.id) {
            this.currentView = newView;
            this._renderMethod = "render";
            (0, _functionsJs.triggerDatepickerEvent)(this.datepicker, "changeView");
            this.main.replaceChild(newView.element, oldView.element);
        }
        return this;
    }
    // Change the focused date (view date)
    changeFocus(newViewDate) {
        this._renderMethod = setViewDate(this, newViewDate) ? "render" : "refreshFocus";
        this.views.forEach((view)=>{
            view.updateFocus();
        });
        return this;
    }
    // Apply the change of the selected dates
    update() {
        const newViewDate = computeResetViewDate(this.datepicker);
        this._renderMethod = setViewDate(this, newViewDate) ? "render" : "refresh";
        this.views.forEach((view)=>{
            view.updateFocus();
            view.updateSelection();
        });
        return this;
    }
    // Refresh the picker UI
    render(quickRender = true) {
        const renderMethod = quickRender && this._renderMethod || "render";
        delete this._renderMethod;
        this.currentView[renderMethod]();
    }
}
exports.default = Picker;

},{"../lib/utils.js":"7MDex","../lib/date.js":"1PD5J","../lib/dom.js":"wtAuE","../lib/event.js":"3Mw9Z","./templates/pickerTemplate.js":"f2wKj","./views/DaysView.js":"kbIqA","./views/MonthsView.js":"7U3nG","./views/YearsView.js":"bOhGK","../events/functions.js":"8gUhk","../events/pickerListeners.js":"5P9Sl","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"f2wKj":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
const pickerTemplate = (0, _utilsJs.optimizeTemplateHTML)(`<div class="datepicker">
  <div class="datepicker-picker">
    <div class="datepicker-header">
      <div class="datepicker-title"></div>
      <div class="datepicker-controls">
        <button type="button" class="%buttonClass% prev-btn"></button>
        <button type="button" class="%buttonClass% view-switch"></button>
        <button type="button" class="%buttonClass% next-btn"></button>
      </div>
    </div>
    <div class="datepicker-main"></div>
    <div class="datepicker-footer">
      <div class="datepicker-controls">
        <button type="button" class="%buttonClass% today-btn"></button>
        <button type="button" class="%buttonClass% clear-btn"></button>
      </div>
    </div>
  </div>
</div>`);
exports.default = pickerTemplate;

},{"../../lib/utils.js":"7MDex","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"kbIqA":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
var _dateJs = require("../../lib/date.js");
var _dateFormatJs = require("../../lib/date-format.js");
var _domJs = require("../../lib/dom.js");
var _daysTemplateJs = require("../templates/daysTemplate.js");
var _daysTemplateJsDefault = parcelHelpers.interopDefault(_daysTemplateJs);
var _calendarWeeksTemplateJs = require("../templates/calendarWeeksTemplate.js");
var _calendarWeeksTemplateJsDefault = parcelHelpers.interopDefault(_calendarWeeksTemplateJs);
var _viewJs = require("./View.js");
var _viewJsDefault = parcelHelpers.interopDefault(_viewJs);
class DaysView extends (0, _viewJsDefault.default) {
    constructor(picker){
        super(picker, {
            id: 0,
            name: "days",
            cellClass: "day"
        });
    }
    init(options, onConstruction = true) {
        if (onConstruction) {
            const inner = (0, _domJs.parseHTML)((0, _daysTemplateJsDefault.default)).firstChild;
            this.dow = inner.firstChild;
            this.grid = inner.lastChild;
            this.element.appendChild(inner);
        }
        super.init(options);
    }
    setOptions(options) {
        let updateDOW;
        if ((0, _utilsJs.hasProperty)(options, "minDate")) this.minDate = options.minDate;
        if ((0, _utilsJs.hasProperty)(options, "maxDate")) this.maxDate = options.maxDate;
        if (options.datesDisabled) this.datesDisabled = options.datesDisabled;
        if (options.daysOfWeekDisabled) {
            this.daysOfWeekDisabled = options.daysOfWeekDisabled;
            updateDOW = true;
        }
        if (options.daysOfWeekHighlighted) this.daysOfWeekHighlighted = options.daysOfWeekHighlighted;
        if (options.todayHighlight !== undefined) this.todayHighlight = options.todayHighlight;
        if (options.weekStart !== undefined) {
            this.weekStart = options.weekStart;
            this.weekEnd = options.weekEnd;
            updateDOW = true;
        }
        if (options.locale) {
            const locale = this.locale = options.locale;
            this.dayNames = locale.daysMin;
            this.switchLabelFormat = locale.titleFormat;
            updateDOW = true;
        }
        if (options.beforeShowDay !== undefined) this.beforeShow = typeof options.beforeShowDay === "function" ? options.beforeShowDay : undefined;
        if (options.calendarWeeks !== undefined) {
            if (options.calendarWeeks && !this.calendarWeeks) {
                const weeksElem = (0, _domJs.parseHTML)((0, _calendarWeeksTemplateJsDefault.default)).firstChild;
                this.calendarWeeks = {
                    element: weeksElem,
                    dow: weeksElem.firstChild,
                    weeks: weeksElem.lastChild
                };
                this.element.insertBefore(weeksElem, this.element.firstChild);
            } else if (this.calendarWeeks && !options.calendarWeeks) {
                this.element.removeChild(this.calendarWeeks.element);
                this.calendarWeeks = null;
            }
        }
        if (options.showDaysOfWeek !== undefined) {
            if (options.showDaysOfWeek) {
                (0, _domJs.showElement)(this.dow);
                if (this.calendarWeeks) (0, _domJs.showElement)(this.calendarWeeks.dow);
            } else {
                (0, _domJs.hideElement)(this.dow);
                if (this.calendarWeeks) (0, _domJs.hideElement)(this.calendarWeeks.dow);
            }
        }
        // update days-of-week when locale, daysOfweekDisabled or weekStart is changed
        if (updateDOW) Array.from(this.dow.children).forEach((el, index)=>{
            const dow = (this.weekStart + index) % 7;
            el.textContent = this.dayNames[dow];
            el.className = this.daysOfWeekDisabled.includes(dow) ? "dow disabled" : "dow";
        });
    }
    // Apply update on the focused date to view's settings
    updateFocus() {
        const viewDate = new Date(this.picker.viewDate);
        const viewYear = viewDate.getFullYear();
        const viewMonth = viewDate.getMonth();
        const firstOfMonth = (0, _dateJs.dateValue)(viewYear, viewMonth, 1);
        const start = (0, _dateJs.dayOfTheWeekOf)(firstOfMonth, this.weekStart, this.weekStart);
        this.first = firstOfMonth;
        this.last = (0, _dateJs.dateValue)(viewYear, viewMonth + 1, 0);
        this.start = start;
        this.focused = this.picker.viewDate;
    }
    // Apply update on the selected dates to view's settings
    updateSelection() {
        const { dates , rangepicker  } = this.picker.datepicker;
        this.selected = dates;
        if (rangepicker) this.range = rangepicker.dates;
    }
    // Update the entire view UI
    render() {
        // update today marker on ever render
        this.today = this.todayHighlight ? (0, _dateJs.today)() : undefined;
        // refresh disabled dates on every render in order to clear the ones added
        // by beforeShow hook at previous render
        this.disabled = [
            ...this.datesDisabled
        ];
        const switchLabel = (0, _dateFormatJs.formatDate)(this.focused, this.switchLabelFormat, this.locale);
        this.picker.setViewSwitchLabel(switchLabel);
        this.picker.setPrevBtnDisabled(this.first <= this.minDate);
        this.picker.setNextBtnDisabled(this.last >= this.maxDate);
        if (this.calendarWeeks) {
            // start of the UTC week (Monday) of the 1st of the month
            const startOfWeek = (0, _dateJs.dayOfTheWeekOf)(this.first, 1, 1);
            Array.from(this.calendarWeeks.weeks.children).forEach((el, index)=>{
                el.textContent = (0, _dateJs.getWeek)((0, _dateJs.addWeeks)(startOfWeek, index));
            });
        }
        Array.from(this.grid.children).forEach((el, index)=>{
            const classList = el.classList;
            const current = (0, _dateJs.addDays)(this.start, index);
            const date = new Date(current);
            const day = date.getDay();
            el.className = `datepicker-cell ${this.cellClass}`;
            el.dataset.date = current;
            el.textContent = date.getDate();
            if (current < this.first) classList.add("prev");
            else if (current > this.last) classList.add("next");
            if (this.today === current) classList.add("today");
            if (current < this.minDate || current > this.maxDate || this.disabled.includes(current)) classList.add("disabled");
            if (this.daysOfWeekDisabled.includes(day)) {
                classList.add("disabled");
                (0, _utilsJs.pushUnique)(this.disabled, current);
            }
            if (this.daysOfWeekHighlighted.includes(day)) classList.add("highlighted");
            if (this.range) {
                const [rangeStart, rangeEnd] = this.range;
                if (current > rangeStart && current < rangeEnd) classList.add("range");
                if (current === rangeStart) classList.add("range-start");
                if (current === rangeEnd) classList.add("range-end");
            }
            if (this.selected.includes(current)) classList.add("selected");
            if (current === this.focused) classList.add("focused");
            if (this.beforeShow) this.performBeforeHook(el, current, current);
        });
    }
    // Update the view UI by applying the changes of selected and focused items
    refresh() {
        const [rangeStart, rangeEnd] = this.range || [];
        this.grid.querySelectorAll(".range, .range-start, .range-end, .selected, .focused").forEach((el)=>{
            el.classList.remove("range", "range-start", "range-end", "selected", "focused");
        });
        Array.from(this.grid.children).forEach((el)=>{
            const current = Number(el.dataset.date);
            const classList = el.classList;
            if (current > rangeStart && current < rangeEnd) classList.add("range");
            if (current === rangeStart) classList.add("range-start");
            if (current === rangeEnd) classList.add("range-end");
            if (this.selected.includes(current)) classList.add("selected");
            if (current === this.focused) classList.add("focused");
        });
    }
    // Update the view UI by applying the change of focused item
    refreshFocus() {
        const index = Math.round((this.focused - this.start) / 86400000);
        this.grid.querySelectorAll(".focused").forEach((el)=>{
            el.classList.remove("focused");
        });
        this.grid.children[index].classList.add("focused");
    }
}
exports.default = DaysView;

},{"../../lib/utils.js":"7MDex","../../lib/date.js":"1PD5J","../../lib/date-format.js":"kp7fb","../../lib/dom.js":"wtAuE","../templates/daysTemplate.js":"9Uldk","../templates/calendarWeeksTemplate.js":"5I6Tc","./View.js":"8Gh24","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"9Uldk":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
const daysTemplate = (0, _utilsJs.optimizeTemplateHTML)(`<div class="days">
  <div class="days-of-week">${(0, _utilsJs.createTagRepeat)("span", 7, {
    class: "dow"
})}</div>
  <div class="datepicker-grid">${(0, _utilsJs.createTagRepeat)("span", 42)}</div>
</div>`);
exports.default = daysTemplate;

},{"../../lib/utils.js":"7MDex","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"5I6Tc":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
const calendarWeeksTemplate = (0, _utilsJs.optimizeTemplateHTML)(`<div class="calendar-weeks">
  <div class="days-of-week"><span class="dow"></span></div>
  <div class="weeks">${(0, _utilsJs.createTagRepeat)("span", 6, {
    class: "week"
})}</div>
</div>`);
exports.default = calendarWeeksTemplate;

},{"../../lib/utils.js":"7MDex","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"8Gh24":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
var _domJs = require("../../lib/dom.js");
class View {
    constructor(picker, config){
        Object.assign(this, config, {
            picker,
            element: (0, _domJs.parseHTML)(`<div class="datepicker-view"></div>`).firstChild,
            selected: []
        });
        this.init(this.picker.datepicker.config);
    }
    init(options) {
        if (options.pickLevel !== undefined) this.isMinView = this.id === options.pickLevel;
        this.setOptions(options);
        this.updateFocus();
        this.updateSelection();
    }
    // Execute beforeShow() callback and apply the result to the element
    // args:
    // - current - current value on the iteration on view rendering
    // - timeValue - time value of the date to pass to beforeShow()
    performBeforeHook(el, current, timeValue) {
        let result = this.beforeShow(new Date(timeValue));
        switch(typeof result){
            case "boolean":
                result = {
                    enabled: result
                };
                break;
            case "string":
                result = {
                    classes: result
                };
        }
        if (result) {
            if (result.enabled === false) {
                el.classList.add("disabled");
                (0, _utilsJs.pushUnique)(this.disabled, current);
            }
            if (result.classes) {
                const extraClasses = result.classes.split(/\s+/);
                el.classList.add(...extraClasses);
                if (extraClasses.includes("disabled")) (0, _utilsJs.pushUnique)(this.disabled, current);
            }
            if (result.content) (0, _domJs.replaceChildNodes)(el, result.content);
        }
    }
}
exports.default = View;

},{"../../lib/utils.js":"7MDex","../../lib/dom.js":"wtAuE","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"7U3nG":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
var _dateJs = require("../../lib/date.js");
var _domJs = require("../../lib/dom.js");
var _viewJs = require("./View.js");
var _viewJsDefault = parcelHelpers.interopDefault(_viewJs);
function computeMonthRange(range, thisYear) {
    if (!range || !range[0] || !range[1]) return;
    const [[startY, startM], [endY, endM]] = range;
    if (startY > thisYear || endY < thisYear) return;
    return [
        startY === thisYear ? startM : -1,
        endY === thisYear ? endM : 12, 
    ];
}
class MonthsView extends (0, _viewJsDefault.default) {
    constructor(picker){
        super(picker, {
            id: 1,
            name: "months",
            cellClass: "month"
        });
    }
    init(options, onConstruction = true) {
        if (onConstruction) {
            this.grid = this.element;
            this.element.classList.add("months", "datepicker-grid");
            this.grid.appendChild((0, _domJs.parseHTML)((0, _utilsJs.createTagRepeat)("span", 12, {
                "data-month": (ix)=>ix
            })));
        }
        super.init(options);
    }
    setOptions(options) {
        if (options.locale) this.monthNames = options.locale.monthsShort;
        if ((0, _utilsJs.hasProperty)(options, "minDate")) {
            if (options.minDate === undefined) this.minYear = this.minMonth = this.minDate = undefined;
            else {
                const minDateObj = new Date(options.minDate);
                this.minYear = minDateObj.getFullYear();
                this.minMonth = minDateObj.getMonth();
                this.minDate = minDateObj.setDate(1);
            }
        }
        if ((0, _utilsJs.hasProperty)(options, "maxDate")) {
            if (options.maxDate === undefined) this.maxYear = this.maxMonth = this.maxDate = undefined;
            else {
                const maxDateObj = new Date(options.maxDate);
                this.maxYear = maxDateObj.getFullYear();
                this.maxMonth = maxDateObj.getMonth();
                this.maxDate = (0, _dateJs.dateValue)(this.maxYear, this.maxMonth + 1, 0);
            }
        }
        if (this.isMinView) {
            if (options.datesDisabled) this.datesDisabled = options.datesDisabled;
        } else this.datesDisabled = [];
        if (options.beforeShowMonth !== undefined) this.beforeShow = typeof options.beforeShowMonth === "function" ? options.beforeShowMonth : undefined;
    }
    // Update view's settings to reflect the viewDate set on the picker
    updateFocus() {
        const viewDate = new Date(this.picker.viewDate);
        this.year = viewDate.getFullYear();
        this.focused = viewDate.getMonth();
    }
    // Update view's settings to reflect the selected dates
    updateSelection() {
        const { dates , rangepicker  } = this.picker.datepicker;
        this.selected = dates.reduce((selected, timeValue)=>{
            const date = new Date(timeValue);
            const year = date.getFullYear();
            const month = date.getMonth();
            if (selected[year] === undefined) selected[year] = [
                month
            ];
            else (0, _utilsJs.pushUnique)(selected[year], month);
            return selected;
        }, {});
        if (rangepicker && rangepicker.dates) this.range = rangepicker.dates.map((timeValue)=>{
            const date = new Date(timeValue);
            return isNaN(date) ? undefined : [
                date.getFullYear(),
                date.getMonth()
            ];
        });
    }
    // Update the entire view UI
    render() {
        // refresh disabled months on every render in order to clear the ones added
        // by beforeShow hook at previous render
        // this.disabled = [...this.datesDisabled];
        this.disabled = this.datesDisabled.reduce((arr, disabled)=>{
            const dt = new Date(disabled);
            if (this.year === dt.getFullYear()) arr.push(dt.getMonth());
            return arr;
        }, []);
        this.picker.setViewSwitchLabel(this.year);
        this.picker.setPrevBtnDisabled(this.year <= this.minYear);
        this.picker.setNextBtnDisabled(this.year >= this.maxYear);
        const selected = this.selected[this.year] || [];
        const yrOutOfRange = this.year < this.minYear || this.year > this.maxYear;
        const isMinYear = this.year === this.minYear;
        const isMaxYear = this.year === this.maxYear;
        const range = computeMonthRange(this.range, this.year);
        Array.from(this.grid.children).forEach((el, index)=>{
            const classList = el.classList;
            const date = (0, _dateJs.dateValue)(this.year, index, 1);
            el.className = `datepicker-cell ${this.cellClass}`;
            if (this.isMinView) el.dataset.date = date;
            // reset text on every render to clear the custom content set
            // by beforeShow hook at previous render
            el.textContent = this.monthNames[index];
            if (yrOutOfRange || isMinYear && index < this.minMonth || isMaxYear && index > this.maxMonth || this.disabled.includes(index)) classList.add("disabled");
            if (range) {
                const [rangeStart, rangeEnd] = range;
                if (index > rangeStart && index < rangeEnd) classList.add("range");
                if (index === rangeStart) classList.add("range-start");
                if (index === rangeEnd) classList.add("range-end");
            }
            if (selected.includes(index)) classList.add("selected");
            if (index === this.focused) classList.add("focused");
            if (this.beforeShow) this.performBeforeHook(el, index, date);
        });
    }
    // Update the view UI by applying the changes of selected and focused items
    refresh() {
        const selected = this.selected[this.year] || [];
        const [rangeStart, rangeEnd] = computeMonthRange(this.range, this.year) || [];
        this.grid.querySelectorAll(".range, .range-start, .range-end, .selected, .focused").forEach((el)=>{
            el.classList.remove("range", "range-start", "range-end", "selected", "focused");
        });
        Array.from(this.grid.children).forEach((el, index)=>{
            const classList = el.classList;
            if (index > rangeStart && index < rangeEnd) classList.add("range");
            if (index === rangeStart) classList.add("range-start");
            if (index === rangeEnd) classList.add("range-end");
            if (selected.includes(index)) classList.add("selected");
            if (index === this.focused) classList.add("focused");
        });
    }
    // Update the view UI by applying the change of focused item
    refreshFocus() {
        this.grid.querySelectorAll(".focused").forEach((el)=>{
            el.classList.remove("focused");
        });
        this.grid.children[this.focused].classList.add("focused");
    }
}
exports.default = MonthsView;

},{"../../lib/utils.js":"7MDex","../../lib/date.js":"1PD5J","../../lib/dom.js":"wtAuE","./View.js":"8Gh24","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"bOhGK":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _utilsJs = require("../../lib/utils.js");
var _dateJs = require("../../lib/date.js");
var _domJs = require("../../lib/dom.js");
var _viewJs = require("./View.js");
var _viewJsDefault = parcelHelpers.interopDefault(_viewJs);
function toTitleCase(word) {
    return [
        ...word
    ].reduce((str, ch, ix)=>str += ix ? ch : ch.toUpperCase(), "");
}
class YearsView extends (0, _viewJsDefault.default) {
    constructor(picker, config){
        super(picker, config);
    }
    init(options, onConstruction = true) {
        if (onConstruction) {
            this.navStep = this.step * 10;
            this.beforeShowOption = `beforeShow${toTitleCase(this.cellClass)}`;
            this.grid = this.element;
            this.element.classList.add(this.name, "datepicker-grid");
            this.grid.appendChild((0, _domJs.parseHTML)((0, _utilsJs.createTagRepeat)("span", 12)));
        }
        super.init(options);
    }
    setOptions(options) {
        if ((0, _utilsJs.hasProperty)(options, "minDate")) {
            if (options.minDate === undefined) this.minYear = this.minDate = undefined;
            else {
                this.minYear = (0, _dateJs.startOfYearPeriod)(options.minDate, this.step);
                this.minDate = (0, _dateJs.dateValue)(this.minYear, 0, 1);
            }
        }
        if ((0, _utilsJs.hasProperty)(options, "maxDate")) {
            if (options.maxDate === undefined) this.maxYear = this.maxDate = undefined;
            else {
                this.maxYear = (0, _dateJs.startOfYearPeriod)(options.maxDate, this.step);
                this.maxDate = (0, _dateJs.dateValue)(this.maxYear, 11, 31);
            }
        }
        if (this.isMinView) {
            if (options.datesDisabled) this.datesDisabled = options.datesDisabled;
        } else this.datesDisabled = [];
        if (options[this.beforeShowOption] !== undefined) {
            const beforeShow = options[this.beforeShowOption];
            this.beforeShow = typeof beforeShow === "function" ? beforeShow : undefined;
        }
    }
    // Update view's settings to reflect the viewDate set on the picker
    updateFocus() {
        const viewDate = new Date(this.picker.viewDate);
        const first = (0, _dateJs.startOfYearPeriod)(viewDate, this.navStep);
        const last = first + 9 * this.step;
        this.first = first;
        this.last = last;
        this.start = first - this.step;
        this.focused = (0, _dateJs.startOfYearPeriod)(viewDate, this.step);
    }
    // Update view's settings to reflect the selected dates
    updateSelection() {
        const { dates , rangepicker  } = this.picker.datepicker;
        this.selected = dates.reduce((years, timeValue)=>{
            return (0, _utilsJs.pushUnique)(years, (0, _dateJs.startOfYearPeriod)(timeValue, this.step));
        }, []);
        if (rangepicker && rangepicker.dates) this.range = rangepicker.dates.map((timeValue)=>{
            if (timeValue !== undefined) return (0, _dateJs.startOfYearPeriod)(timeValue, this.step);
        });
    }
    // Update the entire view UI
    render() {
        // refresh disabled years on every render in order to clear the ones added
        // by beforeShow hook at previous render
        // this.disabled = [...this.datesDisabled];
        this.disabled = this.datesDisabled.map((disabled)=>new Date(disabled).getFullYear());
        this.picker.setViewSwitchLabel(`${this.first}-${this.last}`);
        this.picker.setPrevBtnDisabled(this.first <= this.minYear);
        this.picker.setNextBtnDisabled(this.last >= this.maxYear);
        Array.from(this.grid.children).forEach((el, index)=>{
            const classList = el.classList;
            const current = this.start + index * this.step;
            const date = (0, _dateJs.dateValue)(current, 0, 1);
            el.className = `datepicker-cell ${this.cellClass}`;
            if (this.isMinView) el.dataset.date = date;
            el.textContent = el.dataset.year = current;
            if (index === 0) classList.add("prev");
            else if (index === 11) classList.add("next");
            if (current < this.minYear || current > this.maxYear || this.disabled.includes(current)) classList.add("disabled");
            if (this.range) {
                const [rangeStart, rangeEnd] = this.range;
                if (current > rangeStart && current < rangeEnd) classList.add("range");
                if (current === rangeStart) classList.add("range-start");
                if (current === rangeEnd) classList.add("range-end");
            }
            if (this.selected.includes(current)) classList.add("selected");
            if (current === this.focused) classList.add("focused");
            if (this.beforeShow) this.performBeforeHook(el, current, date);
        });
    }
    // Update the view UI by applying the changes of selected and focused items
    refresh() {
        const [rangeStart, rangeEnd] = this.range || [];
        this.grid.querySelectorAll(".range, .range-start, .range-end, .selected, .focused").forEach((el)=>{
            el.classList.remove("range", "range-start", "range-end", "selected", "focused");
        });
        Array.from(this.grid.children).forEach((el)=>{
            const current = Number(el.textContent);
            const classList = el.classList;
            if (current > rangeStart && current < rangeEnd) classList.add("range");
            if (current === rangeStart) classList.add("range-start");
            if (current === rangeEnd) classList.add("range-end");
            if (this.selected.includes(current)) classList.add("selected");
            if (current === this.focused) classList.add("focused");
        });
    }
    // Update the view UI by applying the change of focused item
    refreshFocus() {
        const index = Math.round((this.focused - this.start) / this.step);
        this.grid.querySelectorAll(".focused").forEach((el)=>{
            el.classList.remove("focused");
        });
        this.grid.children[index].classList.add("focused");
    }
}
exports.default = YearsView;

},{"../../lib/utils.js":"7MDex","../../lib/date.js":"1PD5J","../../lib/dom.js":"wtAuE","./View.js":"8Gh24","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"8gUhk":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "triggerDatepickerEvent", ()=>triggerDatepickerEvent);
// direction: -1 (to previous), 1 (to next)
parcelHelpers.export(exports, "goToPrevOrNext", ()=>goToPrevOrNext);
parcelHelpers.export(exports, "switchView", ()=>switchView);
parcelHelpers.export(exports, "unfocus", ()=>unfocus);
var _utilsJs = require("../lib/utils.js");
var _dateJs = require("../lib/date.js");
function triggerDatepickerEvent(datepicker, type) {
    const detail = {
        date: datepicker.getDate(),
        viewDate: new Date(datepicker.picker.viewDate),
        viewId: datepicker.picker.currentView.id,
        datepicker
    };
    datepicker.element.dispatchEvent(new CustomEvent(type, {
        detail
    }));
}
function goToPrevOrNext(datepicker, direction) {
    const { minDate , maxDate  } = datepicker.config;
    const { currentView , viewDate  } = datepicker.picker;
    let newViewDate;
    switch(currentView.id){
        case 0:
            newViewDate = (0, _dateJs.addMonths)(viewDate, direction);
            break;
        case 1:
            newViewDate = (0, _dateJs.addYears)(viewDate, direction);
            break;
        default:
            newViewDate = (0, _dateJs.addYears)(viewDate, direction * currentView.navStep);
    }
    newViewDate = (0, _utilsJs.limitToRange)(newViewDate, minDate, maxDate);
    datepicker.picker.changeFocus(newViewDate).render();
}
function switchView(datepicker) {
    const viewId = datepicker.picker.currentView.id;
    if (viewId === datepicker.config.maxView) return;
    datepicker.picker.changeView(viewId + 1).render();
}
function unfocus(datepicker) {
    if (datepicker.config.updateOnBlur) datepicker.update({
        revert: true
    });
    else datepicker.refresh("input");
    datepicker.hide();
}

},{"../lib/utils.js":"7MDex","../lib/date.js":"1PD5J","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"5P9Sl":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "onClickTodayBtn", ()=>onClickTodayBtn);
parcelHelpers.export(exports, "onClickClearBtn", ()=>onClickClearBtn);
parcelHelpers.export(exports, "onClickViewSwitch", ()=>onClickViewSwitch);
parcelHelpers.export(exports, "onClickPrevBtn", ()=>onClickPrevBtn);
parcelHelpers.export(exports, "onClickNextBtn", ()=>onClickNextBtn);
// For the picker's main block to delegete the events from `datepicker-cell`s
parcelHelpers.export(exports, "onClickView", ()=>onClickView);
parcelHelpers.export(exports, "onMousedownPicker", ()=>onMousedownPicker);
var _dateJs = require("../lib/date.js");
var _eventJs = require("../lib/event.js");
var _functionsJs = require("./functions.js");
function goToSelectedMonthOrYear(datepicker, selection) {
    const picker = datepicker.picker;
    const viewDate = new Date(picker.viewDate);
    const viewId = picker.currentView.id;
    const newDate = viewId === 1 ? (0, _dateJs.addMonths)(viewDate, selection - viewDate.getMonth()) : (0, _dateJs.addYears)(viewDate, selection - viewDate.getFullYear());
    picker.changeFocus(newDate).changeView(viewId - 1).render();
}
function onClickTodayBtn(datepicker) {
    const picker = datepicker.picker;
    const currentDate = (0, _dateJs.today)();
    if (datepicker.config.todayBtnMode === 1) {
        if (datepicker.config.autohide) {
            datepicker.setDate(currentDate);
            return;
        }
        datepicker.setDate(currentDate, {
            render: false
        });
        picker.update();
    }
    if (picker.viewDate !== currentDate) picker.changeFocus(currentDate);
    picker.changeView(0).render();
}
function onClickClearBtn(datepicker) {
    datepicker.setDate({
        clear: true
    });
}
function onClickViewSwitch(datepicker) {
    (0, _functionsJs.switchView)(datepicker);
}
function onClickPrevBtn(datepicker) {
    (0, _functionsJs.goToPrevOrNext)(datepicker, -1);
}
function onClickNextBtn(datepicker) {
    (0, _functionsJs.goToPrevOrNext)(datepicker, 1);
}
function onClickView(datepicker, ev) {
    const target = (0, _eventJs.findElementInEventPath)(ev, ".datepicker-cell");
    if (!target || target.classList.contains("disabled")) return;
    const { id , isMinView  } = datepicker.picker.currentView;
    if (isMinView) datepicker.setDate(Number(target.dataset.date));
    else if (id === 1) goToSelectedMonthOrYear(datepicker, Number(target.dataset.month));
    else goToSelectedMonthOrYear(datepicker, Number(target.dataset.year));
}
function onMousedownPicker(ev) {
    ev.preventDefault();
}

},{"../lib/date.js":"1PD5J","../lib/event.js":"3Mw9Z","./functions.js":"8gUhk","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"9slyU":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "onKeydown", ()=>onKeydown);
parcelHelpers.export(exports, "onFocus", ()=>onFocus);
// for the prevention for entering edit mode while getting focus on click
parcelHelpers.export(exports, "onMousedown", ()=>onMousedown);
parcelHelpers.export(exports, "onClickInput", ()=>onClickInput);
parcelHelpers.export(exports, "onPaste", ()=>onPaste);
var _utilsJs = require("../lib/utils.js");
var _domJs = require("../lib/dom.js");
var _dateJs = require("../lib/date.js");
var _functionsJs = require("./functions.js");
// Find the closest date that doesn't meet the condition for unavailable date
// Returns undefined if no available date is found
// addFn: function to calculate the next date
//   - args: time value, amount
// increase: amount to pass to addFn
// testFn: function to test the unavailablity of the date
//   - args: time value; retun: true if unavailable
function findNextAvailableOne(date, addFn, increase, testFn, min, max) {
    if (!(0, _utilsJs.isInRange)(date, min, max)) return;
    if (testFn(date)) {
        const newDate = addFn(date, increase);
        return findNextAvailableOne(newDate, addFn, increase, testFn, min, max);
    }
    return date;
}
// direction: -1 (left/up), 1 (right/down)
// vertical: true for up/down, false for left/right
function moveByArrowKey(datepicker, ev, direction, vertical) {
    const picker = datepicker.picker;
    const currentView = picker.currentView;
    const step = currentView.step || 1;
    let viewDate = picker.viewDate;
    let addFn;
    let testFn;
    switch(currentView.id){
        case 0:
            if (vertical) viewDate = (0, _dateJs.addDays)(viewDate, direction * 7);
            else if (ev.ctrlKey || ev.metaKey) viewDate = (0, _dateJs.addYears)(viewDate, direction);
            else viewDate = (0, _dateJs.addDays)(viewDate, direction);
            addFn = (0, _dateJs.addDays);
            testFn = (date)=>currentView.disabled.includes(date);
            break;
        case 1:
            viewDate = (0, _dateJs.addMonths)(viewDate, vertical ? direction * 4 : direction);
            addFn = (0, _dateJs.addMonths);
            testFn = (date)=>{
                const dt = new Date(date);
                const { year , disabled  } = currentView;
                return dt.getFullYear() === year && disabled.includes(dt.getMonth());
            };
            break;
        default:
            viewDate = (0, _dateJs.addYears)(viewDate, direction * (vertical ? 4 : 1) * step);
            addFn = (0, _dateJs.addYears);
            testFn = (date)=>currentView.disabled.includes((0, _dateJs.startOfYearPeriod)(date, step));
    }
    viewDate = findNextAvailableOne(viewDate, addFn, direction < 0 ? -step : step, testFn, currentView.minDate, currentView.maxDate);
    if (viewDate !== undefined) picker.changeFocus(viewDate).render();
}
function onKeydown(datepicker, ev) {
    const key = ev.key;
    if (key === "Tab") {
        (0, _functionsJs.unfocus)(datepicker);
        return;
    }
    const picker = datepicker.picker;
    const { id , isMinView  } = picker.currentView;
    if (!picker.active) {
        if (key === "ArrowDown") picker.show();
        else {
            if (key === "Enter") datepicker.update();
            else if (key === "Escape") picker.show();
            return;
        }
    } else if (datepicker.editMode) {
        if (key === "Enter") datepicker.exitEditMode({
            update: true,
            autohide: datepicker.config.autohide
        });
        else if (key === "Escape") picker.hide();
        return;
    } else {
        if (key === "ArrowLeft") {
            if (ev.ctrlKey || ev.metaKey) (0, _functionsJs.goToPrevOrNext)(datepicker, -1);
            else if (ev.shiftKey) {
                datepicker.enterEditMode();
                return;
            } else moveByArrowKey(datepicker, ev, -1, false);
        } else if (key === "ArrowRight") {
            if (ev.ctrlKey || ev.metaKey) (0, _functionsJs.goToPrevOrNext)(datepicker, 1);
            else if (ev.shiftKey) {
                datepicker.enterEditMode();
                return;
            } else moveByArrowKey(datepicker, ev, 1, false);
        } else if (key === "ArrowUp") {
            if (ev.ctrlKey || ev.metaKey) (0, _functionsJs.switchView)(datepicker);
            else if (ev.shiftKey) {
                datepicker.enterEditMode();
                return;
            } else moveByArrowKey(datepicker, ev, -1, true);
        } else if (key === "ArrowDown") {
            if (ev.shiftKey && !ev.ctrlKey && !ev.metaKey) {
                datepicker.enterEditMode();
                return;
            }
            moveByArrowKey(datepicker, ev, 1, true);
        } else if (key === "Enter") {
            if (isMinView) {
                datepicker.setDate(picker.viewDate);
                return;
            }
            picker.changeView(id - 1).render();
        } else {
            if (key === "Escape") picker.hide();
            else if (key === "Backspace" || key === "Delete" || key.length === 1 && !ev.ctrlKey && !ev.metaKey) datepicker.enterEditMode();
            return;
        }
    }
    ev.preventDefault();
}
function onFocus(datepicker) {
    if (datepicker.config.showOnFocus && !datepicker._showing) datepicker.show();
}
function onMousedown(datepicker, ev) {
    const el = ev.target;
    if (datepicker.picker.active || datepicker.config.showOnClick) {
        el._active = (0, _domJs.isActiveElement)(el);
        el._clicking = setTimeout(()=>{
            delete el._active;
            delete el._clicking;
        }, 2000);
    }
}
function onClickInput(datepicker, ev) {
    const el = ev.target;
    if (!el._clicking) return;
    clearTimeout(el._clicking);
    delete el._clicking;
    if (el._active) datepicker.enterEditMode();
    delete el._active;
    if (datepicker.config.showOnClick) datepicker.show();
}
function onPaste(datepicker, ev) {
    if (ev.clipboardData.types.includes("text/plain")) datepicker.enterEditMode();
}

},{"../lib/utils.js":"7MDex","../lib/dom.js":"wtAuE","../lib/date.js":"1PD5J","./functions.js":"8gUhk","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"33DOL":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
// for the `document` to delegate the events from outside the picker/input field
parcelHelpers.export(exports, "onClickOutside", ()=>onClickOutside);
var _domJs = require("../lib/dom.js");
var _eventJs = require("../lib/event.js");
var _functionsJs = require("./functions.js");
function onClickOutside(datepicker, ev) {
    const { element , picker  } = datepicker;
    // check both picker's and input's activeness to make updateOnBlur work in
    // the cases where...
    // - picker is hidden by ESC key press → input stays focused
    // - input is unfocused by closing mobile keyboard → piker is kept shown
    if (!picker.active && !(0, _domJs.isActiveElement)(element)) return;
    const pickerElem = picker.element;
    if ((0, _eventJs.findElementInEventPath)(ev, (el)=>el === element || el === pickerElem)) return;
    (0, _functionsJs.unfocus)(datepicker);
}

},{"../lib/dom.js":"wtAuE","../lib/event.js":"3Mw9Z","./functions.js":"8gUhk","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"eY7zY":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _eventJs = require("./lib/event.js");
var _dateFormatJs = require("./lib/date-format.js");
var _datepickerJs = require("./Datepicker.js");
var _datepickerJsDefault = parcelHelpers.interopDefault(_datepickerJs);
// filter out the config options inapproprite to pass to Datepicker
function filterOptions(options) {
    const newOpts = Object.assign({}, options);
    delete newOpts.inputs;
    delete newOpts.allowOneSidedRange;
    delete newOpts.maxNumberOfDates; // to ensure each datepicker handles a single date
    return newOpts;
}
function setupDatepicker(rangepicker, changeDateListener, el, options) {
    (0, _eventJs.registerListeners)(rangepicker, [
        [
            el,
            "changeDate",
            changeDateListener
        ], 
    ]);
    new (0, _datepickerJsDefault.default)(el, options, rangepicker);
}
function onChangeDate(rangepicker, ev) {
    // to prevent both datepickers trigger the other side's update each other
    if (rangepicker._updating) return;
    rangepicker._updating = true;
    const target = ev.target;
    if (target.datepicker === undefined) return;
    const datepickers = rangepicker.datepickers;
    const setDateOptions = {
        render: false
    };
    const changedSide = rangepicker.inputs.indexOf(target);
    const otherSide = changedSide === 0 ? 1 : 0;
    const changedDate = datepickers[changedSide].dates[0];
    const otherDate = datepickers[otherSide].dates[0];
    if (changedDate !== undefined && otherDate !== undefined) {
        // if the start of the range > the end, swap them
        if (changedSide === 0 && changedDate > otherDate) {
            datepickers[0].setDate(otherDate, setDateOptions);
            datepickers[1].setDate(changedDate, setDateOptions);
        } else if (changedSide === 1 && changedDate < otherDate) {
            datepickers[0].setDate(changedDate, setDateOptions);
            datepickers[1].setDate(otherDate, setDateOptions);
        }
    } else if (!rangepicker.allowOneSidedRange) // to prevent the range from becoming one-sided, copy changed side's
    // selection (no matter if it's empty) to the other side
    {
        if (changedDate !== undefined || otherDate !== undefined) {
            setDateOptions.clear = true;
            datepickers[otherSide].setDate(datepickers[changedSide].dates, setDateOptions);
        }
    }
    datepickers[0].picker.update().render();
    datepickers[1].picker.update().render();
    delete rangepicker._updating;
}
class DateRangePicker {
    /**
   * Create a date range picker
   * @param  {Element} element - element to bind a date range picker
   * @param  {Object} [options] - config options
   */ constructor(element, options = {}){
        const inputs = Array.isArray(options.inputs) ? options.inputs : Array.from(element.querySelectorAll("input"));
        if (inputs.length < 2) return;
        element.rangepicker = this;
        this.element = element;
        this.inputs = inputs.slice(0, 2);
        this.allowOneSidedRange = !!options.allowOneSidedRange;
        const changeDateListener = onChangeDate.bind(null, this);
        const cleanOptions = filterOptions(options);
        // in order for initial date setup to work right when pcicLvel > 0,
        // let Datepicker constructor add the instance to the rangepicker
        const datepickers = [];
        Object.defineProperty(this, "datepickers", {
            get () {
                return datepickers;
            }
        });
        setupDatepicker(this, changeDateListener, this.inputs[0], cleanOptions);
        setupDatepicker(this, changeDateListener, this.inputs[1], cleanOptions);
        Object.freeze(datepickers);
        // normalize the range if inital dates are given
        if (datepickers[0].dates.length > 0) onChangeDate(this, {
            target: this.inputs[0]
        });
        else if (datepickers[1].dates.length > 0) onChangeDate(this, {
            target: this.inputs[1]
        });
    }
    /**
   * @type {Array} - selected date of the linked date pickers
   */ get dates() {
        return this.datepickers.length === 2 ? [
            this.datepickers[0].dates[0],
            this.datepickers[1].dates[0], 
        ] : undefined;
    }
    /**
   * Set new values to the config options
   * @param {Object} options - config options to update
   */ setOptions(options) {
        this.allowOneSidedRange = !!options.allowOneSidedRange;
        const cleanOptions = filterOptions(options);
        this.datepickers[0].setOptions(cleanOptions);
        this.datepickers[1].setOptions(cleanOptions);
    }
    /**
   * Destroy the DateRangePicker instance
   * @return {DateRangePicker} - the instance destroyed
   */ destroy() {
        this.datepickers[0].destroy();
        this.datepickers[1].destroy();
        (0, _eventJs.unregisterListeners)(this);
        delete this.element.rangepicker;
    }
    /**
   * Get the start and end dates of the date range
   *
   * The method returns Date objects by default. If format string is passed,
   * it returns date strings formatted in given format.
   * The result array always contains 2 items (start date/end date) and
   * undefined is used for unselected side. (e.g. If none is selected,
   * the result will be [undefined, undefined]. If only the end date is set
   * when allowOneSidedRange config option is true, [undefined, endDate] will
   * be returned.)
   *
   * @param  {String} [format] - Format string to stringify the dates
   * @return {Array} - Start and end dates
   */ getDates(format) {
        const callback = format ? (date)=>(0, _dateFormatJs.formatDate)(date, format, this.datepickers[0].config.locale) : (date)=>new Date(date);
        return this.dates.map((date)=>date === undefined ? date : callback(date));
    }
    /**
   * Set the start and end dates of the date range
   *
   * The method calls datepicker.setDate() internally using each of the
   * arguments in start→end order.
   *
   * When a clear: true option object is passed instead of a date, the method
   * clears the date.
   *
   * If an invalid date, the same date as the current one or an option object
   * without clear: true is passed, the method considers that argument as an
   * "ineffective" argument because calling datepicker.setDate() with those
   * values makes no changes to the date selection.
   *
   * When the allowOneSidedRange config option is false, passing {clear: true}
   * to clear the range works only when it is done to the last effective
   * argument (in other words, passed to rangeEnd or to rangeStart along with
   * ineffective rangeEnd). This is because when the date range is changed,
   * it gets normalized based on the last change at the end of the changing
   * process.
   *
   * @param {Date|Number|String|Object} rangeStart - Start date of the range
   * or {clear: true} to clear the date
   * @param {Date|Number|String|Object} rangeEnd - End date of the range
   * or {clear: true} to clear the date
   */ setDates(rangeStart, rangeEnd) {
        const [datepicker0, datepicker1] = this.datepickers;
        const origDates = this.dates;
        // If range normalization runs on every change, we can't set a new range
        // that starts after the end of the current range correctly because the
        // normalization process swaps start↔︎end right after setting the new start
        // date. To prevent this, the normalization process needs to run once after
        // both of the new dates are set.
        this._updating = true;
        datepicker0.setDate(rangeStart);
        datepicker1.setDate(rangeEnd);
        delete this._updating;
        if (datepicker1.dates[0] !== origDates[1]) onChangeDate(this, {
            target: this.inputs[1]
        });
        else if (datepicker0.dates[0] !== origDates[0]) onChangeDate(this, {
            target: this.inputs[0]
        });
    }
}
exports.default = DateRangePicker;

},{"./lib/event.js":"3Mw9Z","./lib/date-format.js":"kp7fb","./Datepicker.js":"eHHLj","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"ayviZ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "Lov", ()=>Lov);
const Lov = {
    closeListbox: ($context)=>{
        let focused = $context.$local.focusedOptionId !== null;
        $context.$local.focusedOptionId = null;
        $context.search = null;
        if (focused) $context.$el.querySelector("[jmb-ref=button]").focus();
    },
    toggleListboxVisibility: ($context)=>{
        if ($context.search !== null) return juiLov.closeListbox($context);
        $context.search = String("");
        $context.$local.focusedOptionId = null;
    },
    selectOption: function($context, $dispatch) {
        let focusedId = $context.$local.focusedOptionId;
        $context.$local.focusedOptionId = null;
        $context.selected = focusedId !== null && focusedId !== "" ? String(focusedId) : null;
        $context.search = null;
        $dispatch("select-option-changed", {
            selected: $context.selected
        });
    },
    focusNext: function($context) {
        if ($context.$local.focusedOptionId === null) nextOption = $context.$el.querySelector("[option-id]");
        else {
            selOption = $context.$el.querySelector("[option-id='" + $context.$local.focusedOptionId + "']");
            nextOption = selOption !== null ? selOption.nextElementSibling : null;
            if (nextOption === null) nextOption = $context.$el.querySelector("[option-id]");
        }
        if (nextOption === null) return;
        $context.$local.focusedOptionId = nextOption.getAttribute("option-id");
        nextOption.scrollIntoViewIfNeeded();
    },
    focusPrev: function($context) {
        if ($context.$local.focusedOptionId === null) prevOption = $context.$el.querySelector("[option-id]:last-of-type");
        else {
            selOption = $context.$el.querySelector("[option-id='" + $context.$local.focusedOptionId + "']");
            prevOption = selOption !== null ? selOption.previousElementSibling : null;
            if (prevOption === null) prevOption = $context.$el.querySelector("[option-id]:last-of-type");
        }
        if (prevOption === null) return;
        $context.$local.focusedOptionId = prevOption.getAttribute("option-id");
        prevOption.scrollIntoViewIfNeeded();
    }
};

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}]},["8Ue9r","idS3Y"], "idS3Y", "parcelRequire94c2")

//# sourceMappingURL=jembeui.js.map
