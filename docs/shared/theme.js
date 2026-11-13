/* Light / dark theme switch shared by the lab apps.
   Default "auto" follows the operating system (prefers-color-scheme); the choice is kept per browser.
   The apps' CSS already reads :root[data-theme="light" | "dark"]. Load this script in <head> to avoid a flash. */
(function () {
  "use strict";
  var KEY = "lab-theme";
  var ORDER = ["auto", "light", "dark"];
  var TXT = {
    ro: { auto: "Temă: automată (ca sistemul)", light: "Temă: luminoasă", dark: "Temă: întunecată", short: { auto: "Auto", light: "Luminos", dark: "Întunecat" } },
    en: { auto: "Theme: automatic (system)", light: "Theme: light", dark: "Theme: dark", short: { auto: "Auto", light: "Light", dark: "Dark" } }
  };
  var SVG = function (d) { return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="vertical-align:-2px;margin-right:5px">' + d + "</svg>"; };
  var ICON = { auto: SVG('<circle cx="12" cy="12" r="9"/><path d="M12 3v18" /><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/>'),
    light: SVG('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    dark: SVG('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>') };
  function get() { try { var v = localStorage.getItem(KEY); return ORDER.indexOf(v) >= 0 ? v : "auto"; } catch (e) { return "auto"; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* storage unavailable */ } }
  function apply(v) {
    var r = document.documentElement;
    if (v === "auto") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", v);
  }
  apply(get());

  function label(btn) {
    var lang = (document.documentElement.lang || "ro").slice(0, 2); var T = TXT[lang] || TXT.ro; var v = get();
    btn.innerHTML = ICON[v] + T.short[v];
    btn.title = T[v]; btn.setAttribute("aria-label", T[v]);
  }
  function mount() {
    var lang = document.querySelector(".lang"); if (!lang || document.getElementById("themeBtn")) return;
    var grp = document.createElement("div"); grp.className = "lang"; grp.setAttribute("role", "group");
    var btn = document.createElement("button"); btn.type = "button"; btn.id = "themeBtn"; btn.setAttribute("aria-pressed", "false");
    grp.appendChild(btn); lang.parentNode.insertBefore(grp, lang.nextSibling);
    label(btn);
    btn.addEventListener("click", function () { var v = ORDER[(ORDER.indexOf(get()) + 1) % ORDER.length]; set(v); apply(v); label(btn); });
    new MutationObserver(function () { label(btn); }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount); else mount();
})();
