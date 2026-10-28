/* Sends a finished lab report to the instructor's collector (Google Apps Script web app).
   The endpoint is set in report-config.js; without it the send box is not shown. */
(function () {
  "use strict";
  var TXT = {
    ro: { title: "Trimite raportul profesorului", hint: "Raportul ajunge direct la profesor. Poți retrimite oricând; se păstrează toate trimiterile, iar ultima contează.",
      send: "Trimite raportul", sending: "Se trimite…", ok: "Raport trimis", okAt: "Trimis la {t}.", fail: "Trimiterea nu a mers. Verifică conexiunea și încearcă din nou; dacă tot nu merge, descarcă raportul și trimite-l separat.",
      need: "Completează numele, grupa și varianta înainte de trimitere.", last: "Ultima trimitere: {t}." },
    en: { title: "Send the report to your instructor", hint: "The report goes straight to your instructor. You can send it again at any time; every submission is kept and the last one counts.",
      send: "Send report", sending: "Sending…", ok: "Report sent", okAt: "Sent at {t}.", fail: "Sending did not work. Check your connection and try again; if it still fails, download the report and send it separately.",
      need: "Fill in your name, group and variant before sending.", last: "Last sent: {t}." }
  };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function getLast(lab) { try { return localStorage.getItem("labreport-sent-" + lab) || ""; } catch (e) { return ""; } }
  function setLast(lab, v) { try { localStorage.setItem("labreport-sent-" + lab, v); } catch (e) { /* storage unavailable */ } }

  /* opts: { lab, lang, getPayload: () => ({ name, group, variant, summary, html, text }) } */
  function mount(box, opts) {
    var ep = window.LAB_REPORT_ENDPOINT;
    if (!box || !ep) return;
    var T = TXT[opts.lang] || TXT.ro;
    var last = getLast(opts.lab);
    box.innerHTML = '<div class="panel stack" style="border-left:3px solid var(--accent)"><h3>' + esc(T.title) + '</h3><p class="muted" style="font-size:0.9rem">' + esc(T.hint) + "</p>" +
      '<div class="row"><button class="btn primary" type="button" data-send>' + esc(T.send) + '</button><span data-status class="muted" style="font-size:0.9rem" role="status">' +
      (last ? esc(T.last.replace("{t}", last)) : "") + "</span></div></div>";
    var btn = box.querySelector("[data-send]"), st = box.querySelector("[data-status]");
    btn.addEventListener("click", function () {
      var p = opts.getPayload();
      if (!String(p.name || "").trim() || !String(p.group || "").trim() || !String(p.variant || "").trim()) { st.textContent = T.need; st.style.color = "var(--bad)"; return; }
      btn.disabled = true; st.style.color = ""; st.textContent = T.sending;
      var body = JSON.stringify({ lab: opts.lab, lang: opts.lang, name: p.name, group: p.group, variant: p.variant, summary: p.summary || "", html: p.html, text: p.text || "" });
      var done = function (when) {
        var tstamp = when || new Date().toLocaleString(opts.lang === "en" ? "en-GB" : "ro-RO");
        setLast(opts.lab, tstamp); st.style.color = "var(--ok)"; st.textContent = T.ok + ". " + T.okAt.replace("{t}", tstamp); btn.disabled = false;
      };
      var fail = function () { st.style.color = "var(--bad)"; st.textContent = T.fail; btn.disabled = false; };
      /* text/plain body keeps it a simple CORS request (no preflight), which Apps Script accepts */
      fetch(ep, { method: "POST", body: body, redirect: "follow" })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) done(j.received); else fail(); })
        .catch(function () {
          /* the response could not be read: retry without reading it */
          fetch(ep, { method: "POST", mode: "no-cors", body: body }).then(function () { done(); }, fail);
        });
    });
  }
  window.LabReport = { mount: mount };
})();
