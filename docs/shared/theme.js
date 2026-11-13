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
  var ICON = { auto: "◐", light: "☀", dark: "☾" };
  function get() { try { var v = localStorage.getItem(KEY); return ORDER.indexOf(v) >= 0 ? v : "auto"; } catch (e) { return "auto"; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* storage unavailable */ } }
  function apply(v) {
    var r = document.documentElement;
    if (v === "auto") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", v);
  }
  apply(get());

  function label(btn) {
    var lang = (document.documentElement.lang || "ro").slice(0, 2); var T = TXT[lang] || TXT.ro; var v = get();
    btn.textContent = ICON[v] + " " + T.short[v];
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
