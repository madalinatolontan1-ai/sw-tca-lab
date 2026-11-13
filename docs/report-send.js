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
      var p0 = opts.getPayload();
      if (!String(p0.name || "").trim() || !String(p0.variant || "").trim()) { st.textContent = T.need; st.style.color = "var(--bad)"; return; }
      /* the final knowledge test comes once, before the first sending of an own (non-demo) variant */
      if (!opts.demo && !quizGet(opts.lab).post && QUIZ[opts.lab]) { showQuiz(opts.lab, opts.lang, "post", send); return; }
      send();
    });
    function send() {
      var p = opts.getPayload();
      btn.disabled = true; st.style.color = ""; st.textContent = T.sending;
      var body = JSON.stringify({ lab: opts.lab, lang: opts.lang, name: p.name, group: p.group, variant: p.variant, summary: p.summary || "", html: p.html, text: p.text || "",
        data: { v: 1, sentAt: new Date().toISOString(), state: p.data || null, work: trackGet(opts.lab), firstReportView: snapGet(opts.lab), quiz: quizGet(opts.lab) } });
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
    }
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
      var el = e.target; if (!el || !/^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName) || el.closest(".labdlg")) return;
      var w = get(), k = fieldKey(el); w.edits[k] = (w.edits[k] || 0) + 1; w.editCount++; writeJ(tkKey(lab), w);
    }, true);
    document.addEventListener("paste", function (e) {
      var el = e.target; if (!el || !/^(INPUT|TEXTAREA)$/.test(el.tagName) || el.closest(".labdlg")) return;
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
  function resetWork(lab) { try { localStorage.removeItem(tkKey(lab)); localStorage.removeItem(snKey(lab)); localStorage.removeItem(qzKey(lab)); } catch (e) { /* storage unavailable */ } }

  /* ---------------------------------------------------------------- dialogs (feedback, knowledge test) */
  function dlgCss() {
    if (document.getElementById("labDlgCss")) return;
    var css = document.createElement("style"); css.id = "labDlgCss";
    css.textContent = ".labdlg{border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);color:var(--ink);padding:20px;max-width:680px;width:calc(100% - 32px);max-height:calc(100vh - 32px);overflow:auto}" +
      ".labdlg::backdrop{background:rgba(0,0,0,.45)}.labdlg h3{margin:0 0 6px}.labdlg .fbq{margin:14px 0 0}.labdlg .fbq p{margin:0 0 6px;font-weight:600;font-size:.92rem}" +
      ".labdlg .fbs{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}.labdlg .fbs label{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.72rem;text-align:center;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:6px 2px;cursor:pointer}" +
      ".labdlg .fbs label:has(input:checked),.labdlg .qzo label:has(input:checked){border-color:var(--accent);color:var(--ink)}.labdlg textarea{width:100%;min-height:70px;margin-top:6px;box-sizing:border-box;font:inherit;padding:6px;border:1px solid var(--line);border-radius:6px;background:var(--bg,transparent);color:inherit}" +
      ".labdlg .qzo{display:grid;gap:4px}.labdlg .qzo label{display:flex;gap:8px;align-items:flex-start;font-size:.86rem;border:1px solid var(--line);border-radius:6px;padding:6px 8px;cursor:pointer}" +
      ".labdlg .fbb{display:flex;gap:8px;justify-content:flex-end;align-items:center;margin-top:16px}.labdlg .fbmsg{margin-right:auto;font-size:.85rem}";
    document.head.appendChild(css);
  }

  /* ---------------------------------------------------------------- knowledge test (pre / post)
     5 multiple-choice items per lab. Pre: when the student loads an own variant for the first time (after the
     lecture and the worked example); post: before the first sending of the report, same items with the options
     in another order. Not graded; the answers go with the report (study data). Option ids a-d are canonical,
     "c" marks the correct one, so the order on screen does not matter for scoring. */
  var QZT = {
    ro: { pre: "Test inițial · 5 întrebări", post: "Test final · 5 întrebări", introPre: "Înainte să începi lucrul pe varianta ta. Nu se notează; ne arată ce ai reținut din prezentare și din exemplu. Alege un singur răspuns la fiecare întrebare.",
      introPost: "Aceleași întrebări ca la început, după lucrul în laborator. Nu se notează; răspunsurile pleacă împreună cu raportul.", send: "Trimite răspunsurile", skip: "Sar peste", need: "Răspunde la toate cele 5 întrebări sau apasă „Sar peste”." },
    en: { pre: "Initial test · 5 questions", post: "Final test · 5 questions", introPre: "Before you start on your variant. Not graded; it shows what you kept from the lecture and the example. Choose one answer per question.",
      introPost: "The same questions as at the start, after the lab work. Not graded; the answers go with your report.", send: "Send answers", skip: "Skip", need: "Answer all 5 questions or click “Skip”." }
  };
  var QUIZ = {
    "HW-TCA": [
      { q: { ro: "Un rezistor trece testul ICT. Ce știm sigur?", en: "A resistor passes the ICT test. What do we know for sure?" }, c: "b", o: {
        a: { ro: "Placa nu are niciun defect.", en: "The board has no defect." },
        b: { ro: "Rezistorul există, are valoarea corectă și nu e întrerupt sau în scurtcircuit.", en: "The resistor is present, has the right value and is neither open nor shorted." },
        c: { ro: "Toate componentele de pe același net sunt corecte.", en: "All parts on the same net are correct." },
        d: { ro: "Testul funcțional va trece sigur.", en: "The functional test will surely pass." } } },
      { q: { ro: "Pentru un defect, aplicația dă D AOI = 10, D AXI = 3, D ICT = 5, iar tu alegi D FT = 5. Toate testele rulează pe fiecare placă. Ce D intră în calculul AP?",
          en: "For a defect, the app gives D AOI = 10, D AXI = 3, D ICT = 5, and you choose D FT = 5. Every test runs on every board. Which D goes into the AP?" }, c: "b", o: {
        a: { ro: "5,75 (media celor patru)", en: "5.75 (the average of the four)" },
        b: { ro: "3 (cea mai mică valoare: metoda care prinde defectul cel mai sigur)", en: "3 (the lowest value: the method that catches the defect most reliably)" },
        c: { ro: "10 (cea mai mare valoare)", en: "10 (the highest value)" },
        d: { ro: "5 (doar D-ul testului funcțional)", en: "5 (only the D of the functional test)" } } },
      { q: { ro: "În HW TCA, de ce depinde ocurența (O) a unui defect de fabricație?", en: "In HW TCA, what does the occurrence (O) of a manufacturing defect depend on?" }, c: "c", o: {
        a: { ro: "De cât de grav e efectul la client", en: "How severe the effect is for the customer" },
        b: { ro: "De câte teste prind defectul", en: "How many tests catch the defect" },
        c: { ro: "De tipul și eficiența controlului de prevenție din linia de producție (tabelul P2)", en: "The type and effectiveness of the prevention control on the production line (table P2)" },
        d: { ro: "De numărul de componente de pe placă", en: "The number of parts on the board" } } },
      { q: { ro: "Lipiturile unui conector THT sunt pe fața BOTTOM, iar AOI inspectează doar fața TOP. Ce scade D AOI pentru un pin întrerupt al conectorului?", en: "A THT connector is soldered on the BOTTOM side and AOI inspects only the TOP side. What lowers D AOI for an open pin of the connector?" }, c: "a", o: {
        a: { ro: "Activarea inspecției AOI pe fața BOTTOM", en: "Enabling AOI inspection on the BOTTOM side" },
        b: { ro: "Un test point pe netul pinului", en: "A test point on the pin's net" },
        c: { ro: "Un O mai mic", en: "A lower O" },
        d: { ro: "Schimbarea clasei de efect", en: "Changing the effect class" } } },
      { q: { ro: "Un mod are S = 8, O = 4 și D = 1. Ce AP dă tabelul AIAG-VDA?", en: "A mode has S = 8, O = 4 and D = 1. Which AP does the AIAG-VDA table give?" }, c: "c", o: {
        a: { ro: "L", en: "L" }, b: { ro: "H", en: "H" }, c: { ro: "M", en: "M" }, d: { ro: "Nu se poate stabili fără RPN", en: "It cannot be set without the RPN" } } }
    ],
    "SW-TCA": [
      { q: { ro: "Ce înseamnă acoperire 100% statement?", en: "What does 100% statement coverage mean?" }, c: "a", o: {
        a: { ro: "Fiecare instrucțiune a fost executată cel puțin o dată de teste.", en: "Every statement was executed at least once by the tests." },
        b: { ro: "Codul nu mai are defecte.", en: "The code has no more defects." },
        c: { ro: "Fiecare decizie a luat atât valoarea true, cât și false.", en: "Every decision took both the true and the false outcome." },
        d: { ro: "Fiecare cerință are cel puțin un test.", en: "Every requirement has at least one test." } } },
      { q: { ro: "Pentru decizia if (A && B), ce cere MC/DC?", en: "For the decision if (A && B), what does MC/DC require?" }, c: "b", o: {
        a: { ro: "Un singur test cu A și B adevărate", en: "A single test with A and B true" },
        b: { ro: "Pentru fiecare condiție, o pereche de teste în care doar ea se schimbă și rezultatul deciziei se schimbă", en: "For each condition, a pair of tests where only that condition changes and the decision outcome changes" },
        c: { ro: "Obligatoriu toate cele 4 combinații de valori", en: "All 4 value combinations, always" },
        d: { ro: "Doar ca decizia să ia true și false", en: "Only that the decision takes true and false" } } },
      { q: { ro: "Cerința: „valorile peste 50 se resping”. Ce pereche de teste verifică limita (BVA)?", en: "Requirement: “values above 50 are rejected”. Which pair of tests checks the limit (BVA)?" }, c: "c", o: {
        a: { ro: "0 și 100", en: "0 and 100" }, b: { ro: "25 și 75", en: "25 and 75" }, c: { ro: "50 și 51", en: "50 and 51" }, d: { ro: "49 și 100", en: "49 and 100" } } },
      { q: { ro: "Cerința cere respingerea valorilor de la 50 inclusiv, dar codul are if (x > 50). Ce test găsește defectul?", en: "The requirement says values from 50 inclusive are rejected, but the code has if (x > 50). Which test finds the defect?" }, c: "b", o: {
        a: { ro: "x = 100", en: "x = 100" }, b: { ro: "x = 50", en: "x = 50" }, c: { ro: "x = 0", en: "x = 0" },
        d: { ro: "Orice set de teste cu acoperire 100% branch", en: "Any test set with 100% branch coverage" } } },
      { q: { ro: "Ce cere ISO 26262-6 pentru codul care rămâne neacoperit la testarea unității software?", en: "What does ISO 26262-6 ask for code that stays uncovered in software unit testing?" }, c: "d", o: {
        a: { ro: "Nimic, dacă acoperirea trece de 80%", en: "Nothing, if coverage is above 80%" },
        b: { ro: "Ștergerea codului neacoperit", en: "Deleting the uncovered code" },
        c: { ro: "Nimic la ASIL B; acoperirea e opțională", en: "Nothing at ASIL B; coverage is optional" },
        d: { ro: "Teste suplimentare sau o justificare a acoperirii insuficiente", en: "Additional tests or a rationale for the insufficient coverage" } } }
    ],
    "FMEA": [
      { q: { ro: "Cum se citește un lanț de defectare în DFMEA?", en: "How is a failure chain read in a DFMEA?" }, c: "a", o: {
        a: { ro: "Cauză → mod → efect, pe niveluri vecine ale structurii", en: "Cause → mode → effect, on neighbouring levels of the structure" },
        b: { ro: "Efect → cauză → mod, pe același nivel", en: "Effect → cause → mode, on the same level" },
        c: { ro: "Mod → test → efect", en: "Mode → test → effect" },
        d: { ro: "Doar mod → efect; cauza nu face parte din lanț", en: "Only mode → effect; the cause is not part of the chain" } } },
      { q: { ro: "Pe ce se dă severitatea (S)?", en: "What is severity (S) rated on?" }, c: "b", o: {
        a: { ro: "Pe cauză", en: "On the cause" }, b: { ro: "Pe efect: pentru mod se ia cel mai grav efect legat de el", en: "On the effect: a mode takes its most severe linked effect" },
        c: { ro: "Pe controlul de detecție", en: "On the detection control" }, d: { ro: "Pe cât de des apare defectul", en: "On how often the failure occurs" } } },
      { q: { ro: "O acțiune de prevenție (tip P) schimbă în primul rând:", en: "A prevention action (type P) mainly changes:" }, c: "c", o: {
        a: { ro: "S", en: "S" }, b: { ro: "D", en: "D" }, c: { ro: "O", en: "O" }, d: { ro: "Nimic, până la testare", en: "Nothing until testing" } } },
      { q: { ro: "De ce folosește AIAG-VDA prioritatea de acțiune (AP) în loc de RPN = S × O × D?", en: "Why does AIAG-VDA use the action priority (AP) instead of RPN = S × O × D?" }, c: "d", o: {
        a: { ro: "Pentru că AP e mai ușor de calculat", en: "Because the AP is easier to compute" },
        b: { ro: "Pentru că RPN nu folosește severitatea", en: "Because the RPN does not use severity" },
        c: { ro: "Pentru că AP ignoră detecția", en: "Because the AP ignores detection" },
        d: { ro: "Pentru că același RPN poate ascunde riscuri foarte diferite; AP dă prioritate severității", en: "Because the same RPN can hide very different risks; the AP gives priority to severity" } } },
      { q: { ro: "Testul care verifică o acțiune iese FAIL. Ce urmează?", en: "The test that checks an action comes out FAIL. What comes next?" }, c: "b", o: {
        a: { ro: "Acțiunea e închisă cu succes.", en: "The action is closed successfully." },
        b: { ro: "Defectul e confirmat: se adaugă o acțiune de proiectare (P) și se reevaluează O și D.", en: "The defect is confirmed: a design action (P) is added and O and D are re-rated." },
        c: { ro: "Se șterge cauza din analiză.", en: "The cause is deleted from the analysis." },
        d: { ro: "AP devine automat L.", en: "The AP becomes L automatically." } } }
    ]
  };
  function qzKey(lab) { return "labquiz-" + lab; }
  function quizGet(lab) { return readJ(qzKey(lab)) || {}; }
  function showQuiz(lab, lang, phase, after) {
    var Q = QUIZ[lab], T = QZT[lang] || QZT.ro;
    if (!Q) { if (after) after(); return; }
    dlgCss();
    var d = document.createElement("dialog"); d.className = "labdlg"; d.id = "qzDlg"; d.setAttribute("aria-labelledby", "qzTitle");
    var ids = ["a", "b", "c", "d"];
    var order = function (i) { return phase === "post" ? ids.slice((i % 3) + 1).concat(ids.slice(0, (i % 3) + 1)) : ids; };  /* post: options rotated */
    d.innerHTML = '<h3 id="qzTitle">' + esc(T[phase]) + '</h3><p class="muted" style="margin:0;font-size:.88rem">' + esc(phase === "pre" ? T.introPre : T.introPost) + "</p>" +
      Q.map(function (it, i) {
        return '<fieldset class="fbq" style="border:0;padding:0"><p>' + (i + 1) + ". " + esc(it.q[lang] || it.q.ro) + '</p><div class="qzo">' +
          order(i).map(function (k) { return '<label><input type="radio" name="qz' + i + '" value="' + k + '"><span>' + esc(it.o[k][lang] || it.o[k].ro) + "</span></label>"; }).join("") + "</div></fieldset>";
      }).join("") +
      '<div class="fbb"><span class="fbmsg" role="status"></span><button type="button" class="btn" data-qzskip>' + esc(T.skip) + '</button><button type="button" class="btn primary" data-qzsend>' + esc(T.send) + "</button></div>";
    document.body.appendChild(d);
    var t0 = Date.now();
    var finish = function (rec) {
      var all = quizGet(lab); all[phase] = rec; writeJ(qzKey(lab), all);
      try { d.close(); } catch (e) { /* ignore */ } d.remove();
      if (after) after();
    };
    d.querySelector("[data-qzskip]").addEventListener("click", function () { finish({ t: new Date().toISOString(), skipped: true }); });
    d.addEventListener("cancel", function (e) { e.preventDefault(); });
    d.querySelector("[data-qzsend]").addEventListener("click", function () {
      var a = Q.map(function (it, i) { var x = d.querySelector('input[name="qz' + i + '"]:checked'); return x ? x.value : ""; });
      if (a.indexOf("") >= 0) { var m = d.querySelector(".fbmsg"); m.textContent = T.need; m.style.color = "var(--bad)"; return; }
      var ok = a.map(function (x, i) { return x === Q[i].c; });
      finish({ t: new Date().toISOString(), sec: Math.round((Date.now() - t0) / 1000), answers: a, correct: ok, score: ok.filter(Boolean).length, of: Q.length });
    });
    if (d.showModal) d.showModal(); else d.setAttribute("open", "");
  }
  /* apps call this when an own variant is shown; it asks once per lab and browser (until "Start over") */
  function preTest(lab, lang) {
    if (!window.LAB_REPORT_ENDPOINT || !QUIZ[lab] || quizGet(lab).pre || document.querySelector(".labdlg")) return;
    showQuiz(lab, lang, "pre", null);
  }

  /* ---------------------------------------------------------------- steps of the analysis
     apps pass [{ n: "1", name: "...", status: "done" | "part" | "todo" | "na" | "auto", detail: "..." }] */
  var STT = {
    ro: { title: "Pașii analizei", step: "Pasul", what: "Ce se cere", st: "Stare", done: "complet", part: "parțial", todo: "necompletat", na: "nu e cazul", auto: "calculat de aplicație" },
    en: { title: "Steps of the analysis", step: "Step", what: "What is required", st: "Status", done: "complete", part: "partial", todo: "not done", na: "not applicable", auto: "computed by the app" }
  };
  var STC = { done: "#1D7F54", part: "#B7791F", todo: "#B83434", na: "#5B6578", auto: "#5B6578" };  /* report (light, static) */
  var STV = { done: "var(--ok)", part: "var(--warn)", todo: "var(--bad)", na: "var(--muted)", auto: "var(--muted)" };  /* app (follows the theme) */
  var STI = { done: "✓", part: "◐", todo: "○", na: "–", auto: "⚙" };
  function stepsHtml(list, lang, forReport) {
    var T = STT[lang] || STT.ro;
    var head = forReport ? "<h2>" + esc(T.title) + "</h2>" : '<h3>' + esc(T.title) + "</h3>";
    var rows = list.map(function (x) {
      return "<tr><td style=\"white-space:nowrap;font-weight:600\">" + esc(T.step) + " " + esc(x.n) + "</td><td>" + esc(x.name) + (x.detail ? '<br><span style="font-size:.85em;opacity:.8">' + esc(x.detail) + "</span>" : "") +
        '</td><td style="white-space:nowrap;color:' + (forReport ? STC : STV)[x.status] + ';font-weight:600">' + STI[x.status] + " " + esc(T[x.status]) + "</td></tr>";
    }).join("");
    var tbl = '<table class="' + (forReport ? "r" : "mini") + '" style="width:100%;border-collapse:collapse"><thead><tr><th style="text-align:left">' + esc(T.step) + '</th><th style="text-align:left">' + esc(T.what) + '</th><th style="text-align:left">' + esc(T.st) + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
    return forReport ? head + tbl : '<div class="panel stack">' + head + '<div class="tablewrap">' + tbl + "</div></div>";
  }
  function stepsText(list, lang) {
    var T = STT[lang] || STT.ro;
    return [T.title + ":"].concat(list.map(function (x) { return "  " + T.step + " " + x.n + ". " + x.name + ": " + T[x.status] + (x.detail ? " (" + x.detail + ")" : ""); })).join("\n");
  }
  /* compact strip for the work view: one chip per step, the name in the tooltip */
  function stepsBar(list, lang) {
    var T = STT[lang] || STT.ro;
    return '<div class="stepbar" style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px"><span class="label">' + esc(T.title) + "</span>" + list.map(function (x) {
      return '<span title="' + esc(x.name + " · " + T[x.status] + (x.detail ? " · " + x.detail : "")) + '" style="font-size:.8rem;font-weight:600;padding:2px 8px;border-radius:999px;border:1px solid ' + STV[x.status] + ";color:" + STV[x.status] + '">' +
        esc(x.n) + " " + STI[x.status] + "</span>";
    }).join("") + "</div>";
  }
  /* a step is done when n of n is complete, partial when some, not done when none; total 0 → not applicable */
  function stepStatus(have, total) { return total === 0 ? "na" : have >= total ? "done" : have > 0 ? "part" : "todo"; }

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
    if (!ep || fbDone(lab) || document.querySelector(".labdlg")) return;
    var T = FB[lang] || FB.ro;
    dlgCss();
    var d = document.createElement("dialog"); d.id = "fbDlg"; d.className = "labdlg"; d.setAttribute("aria-labelledby", "fbTitle");
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
  window.LabReport = { mount: mount, askFeedback: askFeedback, track: track, snapshot: snapshot, resetWork: resetWork, preTest: preTest, stepsHtml: stepsHtml, stepsText: stepsText, stepsBar: stepsBar, stepStatus: stepStatus };
})();
