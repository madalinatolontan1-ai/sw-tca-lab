/* Sends a finished lab report to the instructor's collector (Google Apps Script web app).
   The endpoint is set in report-config.js; without it the send box is not shown. */
(function () {
  "use strict";
  var TXT = {
    ro: { title: "Trimite raportul profesorului", hint: "Raportul ajunge direct la profesor. Poți retrimite oricând; se păstrează toate trimiterile, iar ultima contează.",
      send: "Trimite raportul", sending: "Se trimite…", ok: "Raport trimis", okAt: "Trimis la {t}.", fail: "Trimiterea nu a mers. Verifică conexiunea și încearcă din nou; dacă tot nu merge, descarcă raportul și trimite-l separat.",
      need: "Completează numele, grupa și varianta înainte de trimitere.",
      consent: "Prin completarea și trimiterea acestui raport, declar că sunt de acord cu folosirea datelor din acesta pentru studiu de caz. Numele tău nu va fi folosit nicăieri; se folosesc doar rezultatele din aplicație.", unconf: "Raportul a plecat, dar serverul nu a confirmat primirea. Descarcă raportul și păstrează-l până confirmă profesorul.", last: "Ultima trimitere: {t}." },
    en: { title: "Send the report to your instructor", hint: "The report goes straight to your instructor. You can send it again at any time; every submission is kept and the last one counts.",
      send: "Send report", sending: "Sending…", ok: "Report sent", okAt: "Sent at {t}.", fail: "Sending did not work. Check your connection and try again; if it still fails, download the report and send it separately.",
      need: "Fill in your name, group and variant before sending.",
      consent: "By completing and sending this report, I agree that the data in it may be used for a case study. Your name will not be used anywhere; only the results from the app are used.", unconf: "The report was sent but the server did not confirm receipt. Download the report and keep it until your instructor confirms.", last: "Last sent: {t}." }
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
      '<p style="font-size:0.85rem;margin:0;padding:6px 10px;border:1px solid var(--line);border-radius:var(--radius)">' + esc(T.consent) + "</p>" +
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
        askFeedback(opts.lab, opts.lang);
      };
      var fail = function (why) { st.style.color = "var(--bad)"; st.textContent = T.fail + (why ? " [" + why + "]" : ""); btn.disabled = false; };
      /* text/plain body keeps it a simple CORS request (no preflight), which Apps Script accepts */
      fetch(ep, { method: "POST", body: body, redirect: "follow" })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) done(j.received); else fail(j && j.error); })
        .catch(function () {
          /* the response could not be read: retry without reading it */
          fetch(ep, { method: "POST", mode: "no-cors", body: body }).then(function () { st.style.color = "var(--warn)"; st.textContent = T.unconf; btn.disabled = false; askFeedback(opts.lab, opts.lang); }, fail);
        });
    });
  }

  /* ---------------------------------------------------------------- anonymous feedback
     Shown once per lab and browser, after the report is sent. No name, group or variant is sent with it;
     the collector stores only the date and shuffles the rows. */
  var FB = {
    ro: { title: "Părerea ta despre aplicație", intro: "5 întrebări, complet anonime: nu se trimite numele, grupa sau varianta. Răspunsurile ne ajută să îmbunătățim laboratorul.",
      scale: ["Dezacord total", "Dezacord", "Neutru", "Acord", "Acord total"],
      q: ["Funcțiile aplicației mi-au acoperit nevoile pentru acest exercițiu.",
        "Aplicația este ușor de folosit.",
        "Am înțeles de unde vine fiecare valoare din analiză (tabele, reguli, explicații).",
        "Acum aș putea face singur această analiză pe un alt produs.",
        "Exercițiul mi s-a părut util, ținând cont că această analiză se folosește în industrie."],
      comment: "Ce ai schimba sau ce ți-a lipsit? (opțional)", send: "Trimite", later: "Nu acum", need: "Răspunde la toate cele 5 întrebări.", thanks: "Mulțumim!", fail: "Nu s-a putut trimite. Încearcă din nou." },
    en: { title: "Your opinion about the app", intro: "5 questions, fully anonymous: no name, group or variant is sent. Your answers help us improve the lab.",
      scale: ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
      q: ["The app's features met my needs for this exercise.",
        "The app is easy to use.",
        "I understood where every value in the analysis comes from (tables, rules, explanations).",
        "I could now do this analysis on my own for another product.",
        "I found the exercise useful, given that this analysis is used in industry."],
      comment: "What would you change or what was missing? (optional)", send: "Send", later: "Not now", need: "Answer all 5 questions.", thanks: "Thank you!", fail: "Could not send. Try again." }
  };
  function fbDone(lab) { try { return !!localStorage.getItem("labfeedback-" + lab); } catch (e) { return false; } }
  function fbMark(lab) { try { localStorage.setItem("labfeedback-" + lab, "1"); } catch (e) { /* storage unavailable */ } }
  function askFeedback(lab, lang) {
    var ep = window.LAB_REPORT_ENDPOINT;
    if (!ep || fbDone(lab) || document.getElementById("fbDlg")) return;
    var T = FB[lang] || FB.ro;
    if (!document.getElementById("fbCss")) {
      var css = document.createElement("style"); css.id = "fbCss";
      css.textContent = "#fbDlg{border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);color:var(--ink);padding:20px;max-width:640px;width:calc(100% - 32px)}" +
        "#fbDlg::backdrop{background:rgba(0,0,0,.45)}#fbDlg h3{margin:0 0 6px}#fbDlg .fbq{margin:14px 0 0}#fbDlg .fbq p{margin:0 0 6px;font-weight:600;font-size:.92rem}" +
        "#fbDlg .fbs{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}#fbDlg .fbs label{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.72rem;text-align:center;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:6px 2px;cursor:pointer}" +
        "#fbDlg .fbs label:has(input:checked){border-color:var(--accent);color:var(--ink)}#fbDlg textarea{width:100%;min-height:70px;margin-top:6px;box-sizing:border-box;font:inherit;padding:6px;border:1px solid var(--line);border-radius:6px;background:var(--bg,transparent);color:inherit}" +
        "#fbDlg .fbb{display:flex;gap:8px;justify-content:flex-end;align-items:center;margin-top:16px}#fbDlg .fbmsg{margin-right:auto;font-size:.85rem}";
      document.head.appendChild(css);
    }
    var d = document.createElement("dialog"); d.id = "fbDlg"; d.setAttribute("aria-labelledby", "fbTitle");
    d.innerHTML = '<h3 id="fbTitle">' + esc(T.title) + '</h3><p class="muted" style="margin:0;font-size:.88rem">' + esc(T.intro) + "</p>" +
      T.q.map(function (q, i) {
        return '<fieldset class="fbq" style="border:0;padding:0"><p>' + (i + 1) + ". " + esc(q) + '</p><div class="fbs">' +
          T.scale.map(function (s, j) { return '<label><input type="radio" name="fb' + i + '" value="' + (j + 1) + '"><b>' + (j + 1) + "</b>" + esc(s) + "</label>"; }).join("") + "</div></fieldset>";
      }).join("") +
      '<div class="fbq"><p>' + esc(T.comment) + '</p><textarea maxlength="1000" data-fbc></textarea></div>' +
      '<div class="fbb"><span class="fbmsg" role="status"></span><button type="button" class="btn" data-later>' + esc(T.later) + '</button><button type="button" class="btn primary" data-fbsend>' + esc(T.send) + "</button></div>";
    document.body.appendChild(d);
    var close = function () { try { d.close(); } catch (e) { /* ignore */ } d.remove(); };
    d.querySelector("[data-later]").addEventListener("click", close);
    d.addEventListener("cancel", function () { d.remove(); });
    var msg = d.querySelector(".fbmsg"), sb = d.querySelector("[data-fbsend]");
    sb.addEventListener("click", function () {
      var a = T.q.map(function (q, i) { var x = d.querySelector('input[name="fb' + i + '"]:checked'); return x ? +x.value : 0; });
      if (a.indexOf(0) >= 0) { msg.textContent = T.need; msg.style.color = "var(--bad)"; return; }
      sb.disabled = true; msg.textContent = "…"; msg.style.color = "";
      var body = JSON.stringify({ kind: "feedback", lab: lab, lang: lang, answers: a, comment: d.querySelector("[data-fbc]").value });
      var ok = function () { fbMark(lab); msg.style.color = "var(--ok)"; msg.textContent = T.thanks; setTimeout(close, 1200); };
      fetch(ep, { method: "POST", body: body, redirect: "follow" }).then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) ok(); else { sb.disabled = false; msg.style.color = "var(--bad)"; msg.textContent = T.fail; } })
        .catch(function () { fetch(ep, { method: "POST", mode: "no-cors", body: body }).then(ok, function () { sb.disabled = false; msg.style.color = "var(--bad)"; msg.textContent = T.fail; }); });
    });
    if (d.showModal) d.showModal(); else d.setAttribute("open", "");
  }
  window.LabReport = { mount: mount, askFeedback: askFeedback };
})();
