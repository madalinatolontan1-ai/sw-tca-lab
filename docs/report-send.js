/* Sends a finished lab report to the instructor's collector (Google Apps Script web app).
   The endpoint is set in report-config.js; without it the send box is not shown. */
(function () {
  "use strict";
  var TXT = {
    ro: { title: "Trimite raportul profesorului", hint: "Raportul ajunge direct la profesor. Poți retrimite oricând; se păstrează toate trimiterile, iar ultima contează.",
      send: "Trimite raportul", sending: "Se trimite…", ok: "Raport trimis", okAt: "Trimis la {t}.", fail: "Trimiterea nu a mers. Verifică conexiunea și încearcă din nou; dacă tot nu merge, descarcă raportul și trimite-l separat.",
      need: "Completează numele și varianta înainte de trimitere.",
      consent: "Prin trimiterea raportului cu acest buton ești de acord ca datele din el să fie folosite, pseudonimizat, într-un studiu despre aceste laboratoare: valorile și justificările din analiză și datele de lucru (timpul de lucru, numărul de modificări, textul lipit în câmpuri). Numele tău nu se folosește nicăieri. Dacă nu ești de acord, nu trimite raportul aici: descarcă-l și încarcă-l pe Campusul Virtual; prezența se acordă la fel.", unconf: "Raportul a plecat, dar serverul nu a confirmat primirea. Descarcă raportul și păstrează-l până confirmă profesorul.", last: "Ultima trimitere: {t}." },
    en: { title: "Send the report to your instructor", hint: "The report goes straight to your instructor. You can send it again at any time; every submission is kept and the last one counts.",
      send: "Send report", sending: "Sending…", ok: "Report sent", okAt: "Sent at {t}.", fail: "Sending did not work. Check your connection and try again; if it still fails, download the report and send it separately.",
      need: "Fill in your name and variant before sending.",
      consent: "By sending the report with this button you agree that its data may be used, pseudonymised, in a study about these labs: the values and justifications of your analysis and the work data (working time, number of changes, text pasted into fields). Your name is not used anywhere. If you do not agree, do not send the report here: download it and upload it to the Virtual Campus; attendance counts the same.", unconf: "The report was sent but the server did not confirm receipt. Download the report and keep it until your instructor confirms.", last: "Last sent: {t}." }
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
      if (!String(p.name || "").trim() || !String(p.variant || "").trim()) { st.textContent = T.need; st.style.color = "var(--bad)"; return; }
      btn.disabled = true; st.style.color = ""; st.textContent = T.sending;
      var body = JSON.stringify({ lab: opts.lab, lang: opts.lang, name: p.name, group: p.group, variant: p.variant, summary: p.summary || "", html: p.html, text: p.text || "",
        data: { v: 1, sentAt: new Date().toISOString(), state: p.data || null, work: trackGet(opts.lab), firstReportView: snapGet(opts.lab) } });
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

  /* ---------------------------------------------------------------- work data (sent with the report, for the study)
     start time, active time (a 15 s tick counts when the page is visible and the student did something in the last minute),
     committed edits per field, text pasted into fields (length only), and one copy of the analysis taken the first time
     the Report tab is opened, before the checks list is seen. Everything stays in this browser until the report is sent. */
  var TICK = 15, IDLE = 60000;
  function tkKey(lab) { return "labwork-" + lab; }
  function snKey(lab) { return "labfirst-" + lab; }
  function readJ(k) { try { var r = localStorage.getItem(k); return r ? JSON.parse(r) : null; } catch (e) { return null; } }
  function writeJ(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable or full */ } }
  function trackGet(lab) { return readJ(tkKey(lab)); }
  function snapGet(lab) { return readJ(snKey(lab)); }
  function fieldKey(el) {
    if (!el || !el.getAttribute) return "?";
    if (el.id) return "#" + el.id;
    var parts = [];
    for (var i = 0; i < el.attributes.length; i++) { var a = el.attributes[i]; if (a.name.indexOf("data-") === 0) parts.push(a.name.slice(5) + "=" + a.value); }
    return parts.length ? parts.join(",") : (el.name || el.tagName.toLowerCase());
  }
  var tracked = null;
  function track(lab) {
    if (tracked) return;
    tracked = lab;
    var last = Date.now();
    var get = function () { var w = trackGet(lab); if (!w) { w = { start: new Date().toISOString(), activeSec: 0, edits: {}, editCount: 0, pastes: [] }; } return w; };
    if (!trackGet(lab)) writeJ(tkKey(lab), get());
    var touch = function () { last = Date.now(); };
    ["pointerdown", "keydown", "wheel", "input"].forEach(function (ev) { document.addEventListener(ev, touch, { passive: true, capture: true }); });
    document.addEventListener("change", function (e) {
      var el = e.target; if (!el || !/^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName) || el.closest("#fbDlg")) return;
      var w = get(), k = fieldKey(el); w.edits[k] = (w.edits[k] || 0) + 1; w.editCount++; writeJ(tkKey(lab), w);
    }, true);
    document.addEventListener("paste", function (e) {
      var el = e.target; if (!el || !/^(INPUT|TEXTAREA)$/.test(el.tagName) || el.closest("#fbDlg")) return;
      var n = 0; try { n = (e.clipboardData || window.clipboardData).getData("text").length; } catch (x) { /* no access */ }
      var w = get(); if (w.pastes.length < 500) w.pastes.push({ f: fieldKey(el), n: n, t: new Date().toISOString() }); writeJ(tkKey(lab), w);
    }, true);
    setInterval(function () {
      if (document.visibilityState !== "visible" || Date.now() - last > IDLE) return;
      var w = get(); w.activeSec += TICK; writeJ(tkKey(lab), w);
    }, TICK * 1000);
  }
  /* call when the Report tab is shown; only the first call stores anything */
  function snapshot(lab, getData) {
    if (snapGet(lab)) return;
    var d = null; try { d = getData(); } catch (e) { /* keep null */ }
    writeJ(snKey(lab), { t: new Date().toISOString(), state: d });
  }
  /* "Start over" in the apps: forget the work data of the previous attempt */
  function resetWork(lab) { try { localStorage.removeItem(tkKey(lab)); localStorage.removeItem(snKey(lab)); } catch (e) { /* storage unavailable */ } }

  /* ---------------------------------------------------------------- anonymous feedback
     Shown once per lab and browser, after the report is sent. No name, group or variant is sent with it;
     the collector stores only the date and shuffles the rows. */
  /* items 1-10: System Usability Scale (Brooke, 1996), "system" → "app"; Romanian: translation by the authors.
     items 11-13: lab-specific statements, not part of the SUS score. Same 5-point scale for all. */
  var FB = {
    ro: { title: "Părerea ta despre aplicație", intro: "13 afirmații, complet anonime: nu se trimit numele sau varianta. Alege cât de mult ești de acord cu fiecare. Răspunsurile ne ajută să îmbunătățim laboratorul.",
      scale: ["Dezacord total", "Dezacord", "Neutru", "Acord", "Acord total"],
      q: ["Cred că mi-ar plăcea să folosesc frecvent această aplicație.",
        "Mi s-a părut că aplicația este inutil de complexă.",
        "Mi s-a părut că aplicația este ușor de folosit.",
        "Cred că aș avea nevoie de ajutorul unei persoane cu cunoștințe tehnice ca să pot folosi această aplicație.",
        "Mi s-a părut că funcțiile aplicației sunt bine integrate.",
        "Mi s-a părut că aplicația are prea multe inconsecvențe.",
        "Îmi imaginez că majoritatea oamenilor ar învăța foarte repede să folosească această aplicație.",
        "Mi s-a părut că aplicația este foarte greoaie de folosit.",
        "Am avut multă încredere în mine când am folosit aplicația.",
        "A trebuit să învăț multe lucruri înainte să mă pot descurca cu această aplicație.",
        "Am înțeles de unde vine fiecare valoare din analiză (tabele, reguli, explicații).",
        "Acum aș putea face singur această analiză pe un alt produs.",
        "Exercițiul mi s-a părut util, ținând cont că această analiză se folosește în industrie."],
      comment: "Ce ai schimba sau ce ți-a lipsit? (opțional)", send: "Trimite", later: "Nu acum", need: "Răspunde la toate cele 13 afirmații.", thanks: "Mulțumim!", fail: "Nu s-a putut trimite. Încearcă din nou." },
    en: { title: "Your opinion about the app", intro: "13 statements, fully anonymous: no name or variant is sent. Choose how much you agree with each. Your answers help us improve the lab.",
      scale: ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
      q: ["I think that I would like to use this app frequently.",
        "I found the app unnecessarily complex.",
        "I thought the app was easy to use.",
        "I think that I would need the support of a technical person to be able to use this app.",
        "I found the various functions in this app were well integrated.",
        "I thought there was too much inconsistency in this app.",
        "I would imagine that most people would learn to use this app very quickly.",
        "I found the app very cumbersome to use.",
        "I felt very confident using the app.",
        "I needed to learn a lot of things before I could get going with this app.",
        "I understood where every value in the analysis comes from (tables, rules, explanations).",
        "I could now do this analysis on my own for another product.",
        "I found the exercise useful, given that this analysis is used in industry."],
      comment: "What would you change or what was missing? (optional)", send: "Send", later: "Not now", need: "Answer all 13 statements.", thanks: "Thank you!", fail: "Could not send. Try again." }
  };
  function fbDone(lab) { try { return !!localStorage.getItem("labfeedback-" + lab); } catch (e) { return false; } }
  function fbMark(lab) { try { localStorage.setItem("labfeedback-" + lab, "1"); } catch (e) { /* storage unavailable */ } }
  function askFeedback(lab, lang) {
    var ep = window.LAB_REPORT_ENDPOINT;
    if (!ep || fbDone(lab) || document.getElementById("fbDlg")) return;
    var T = FB[lang] || FB.ro;
    if (!document.getElementById("fbCss")) {
      var css = document.createElement("style"); css.id = "fbCss";
      css.textContent = "#fbDlg{border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);color:var(--ink);padding:20px;max-width:640px;width:calc(100% - 32px);max-height:calc(100vh - 32px);overflow:auto}" +
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
      var body = JSON.stringify({ kind: "feedback", qv: 2, lab: lab, lang: lang, answers: a, comment: d.querySelector("[data-fbc]").value });
      var ok = function () { fbMark(lab); msg.style.color = "var(--ok)"; msg.textContent = T.thanks; setTimeout(close, 1200); };
      fetch(ep, { method: "POST", body: body, redirect: "follow" }).then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) ok(); else { sb.disabled = false; msg.style.color = "var(--bad)"; msg.textContent = T.fail; } })
        .catch(function () { fetch(ep, { method: "POST", mode: "no-cors", body: body }).then(ok, function () { sb.disabled = false; msg.style.color = "var(--bad)"; msg.textContent = T.fail; }); });
    });
    if (d.showModal) d.showModal(); else d.setAttribute("open", "");
  }
  window.LabReport = { mount: mount, askFeedback: askFeedback, track: track, snapshot: snapshot, resetWork: resetWork };
})();
