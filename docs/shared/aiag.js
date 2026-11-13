/* AIAG-VDA FMEA Handbook (1st edition, 2019) rating tables, as used in the labs (shared by the HW TCA and FMEA apps).
   S: DFMEA severity (product general evaluation criteria, table D1).
   O: DFMEA occurrence (occurrence potential for the product, table D2).
   D: DFMEA detection (detection potential for the validation of the product design, table D3).
   O_P: PFMEA occurrence (table P2, occurrence potential for the process), used by HW TCA for manufacturing defects.
   Romanian translation of the English criteria; the English text is the handbook wording. */
(function () {
  "use strict";
  const L = (ro, en) => ({ ro: ro, en: en });
  const S = [
    [10, L("Foarte mare", "Very high"), L("Afectează funcționarea în siguranță a vehiculului și/sau a altor vehicule, sănătatea șoferului, a pasagerilor, a altor participanți la trafic sau a pietonilor.", "Affects safe operation of the vehicle and/or other vehicles, the health of driver or passenger(s) or road users or pedestrians.")],
    [9, L("Foarte mare", "Very high"), L("Neconformitate cu reglementările.", "Noncompliance with regulations.")],
    [8, L("Mare", "High"), L("Pierderea unei funcții principale a vehiculului, necesară pentru condusul normal pe durata de viață estimată.", "Loss of primary vehicle function necessary for normal driving during expected service life.")],
    [7, L("Mare", "High"), L("Degradarea unei funcții principale a vehiculului, necesară pentru condusul normal pe durata de viață estimată.", "Degradation of primary vehicle function necessary for normal driving during expected service life.")],
    [6, L("Moderată", "Moderate"), L("Pierderea unei funcții secundare a vehiculului.", "Loss of secondary vehicle function.")],
    [5, L("Moderată", "Moderate"), L("Degradarea unei funcții secundare a vehiculului.", "Degradation of secondary vehicle function.")],
    [4, L("Moderată", "Moderate"), L("Aspect, sunet, vibrații, asperitate sau haptică foarte deranjante.", "Very objectionable appearance, sound, vibration, harshness, or haptics.")],
    [3, L("Mică", "Low"), L("Aspect, sunet, vibrații, asperitate sau haptică moderat deranjante.", "Moderately objectionable appearance, sound, vibration, harshness, or haptics.")],
    [2, L("Mică", "Low"), L("Aspect, sunet, vibrații, asperitate sau haptică ușor deranjante.", "Slightly objectionable appearance, sound, vibration, harshness, or haptics.")],
    [1, L("Foarte mică", "Very low"), L("Niciun efect perceptibil.", "No discernible effect.")]
  ];
  const O = [
    [10, L("Extrem de mare", "Extremely high"),
      L("Prima aplicare a unei tehnologii noi, oriunde, fără experiență de funcționare și/sau în condiții de funcționare necontrolate. Fără experiență de verificare și/sau validare a produsului.",
        "First application of new technology anywhere without operating experience and/or under uncontrolled operating conditions. No product verification and/or validation experience."),
      L("Standardele nu există, iar bunele practici nu au fost încă stabilite. Controalele de prevenție nu pot prezice performanța în teren sau nu există.",
        "Standards do not exist and best practices have not yet been determined. Prevention controls not able to predict field performance or do not exist.")],
    [9, L("Foarte mare", "Very high"),
      L("Prima utilizare în firmă a unui design cu inovații tehnice sau materiale noi. Aplicație nouă sau schimbare a ciclului de funcționare / a condițiilor de funcționare. Fără experiență de verificare și/sau validare a produsului.",
        "First use of design with technical innovations or materials within the company. New application or change in duty cycle / operating conditions. No product verification and/or validation experience."),
      L("Controalele de prevenție nu sunt orientate spre a identifica performanța față de cerințe specifice.", "Prevention controls not targeted to identify performance to specific requirements.")],
    [8, L("Foarte mare", "Very high"),
      L("Prima utilizare a unui design cu inovații tehnice sau materiale noi într-o aplicație nouă. Aplicație nouă sau schimbare a ciclului de funcționare / a condițiilor de funcționare. Fără experiență de verificare și/sau validare a produsului.",
        "First use of design with technical innovations or materials on a new application. New application or change in duty cycle / operating conditions. No product verification and/or validation experience."),
      L("Puține standarde și bune practici existente, neaplicabile direct acestui design. Controalele de prevenție nu sunt un indicator fiabil al performanței în teren.",
        "Few existing standards and best practices, not directly applicable for this design. Prevention controls not a reliable indicator of field performance.")],
    [7, L("Mare", "High"),
      L("Design nou, bazat pe tehnologie și materiale similare. Aplicație nouă sau schimbare a ciclului de funcționare / a condițiilor de funcționare. Fără experiență de verificare și/sau validare a produsului.",
        "New design based on similar technology and materials. New application or change in duty cycle / operating conditions. No product verification and/or validation experience."),
      L("Standardele, bunele practici și regulile de design se aplică designului de bază, dar nu și inovațiilor. Controalele de prevenție dau o indicație limitată a performanței.",
        "Standards, best practices, and design rules apply to the baseline design, but not the innovations. Prevention controls provide limited indication of performance.")],
    [6, L("Mare", "High"),
      L("Similar cu designuri anterioare, folosind tehnologie și materiale existente. Aplicație similară, cu schimbări ale ciclului de funcționare sau ale condițiilor de funcționare. Experiență anterioară de test sau din teren.",
        "Similar to previous designs, using existing technology and materials. Similar application, with changes in duty cycle or operating conditions. Previous testing or field experience."),
      L("Există standarde și reguli de design, dar nu sunt suficiente pentru a asigura că nu va apărea cauza defectării. Controalele de prevenție oferă o anumită capacitate de a preveni cauza.",
        "Standards and design rules exist but are insufficient to ensure that the failure cause will not occur. Prevention controls provide some ability to prevent a failure cause.")],
    [5, L("Moderată", "Moderate"),
      L("Modificări de detaliu ale unui design anterior, folosind tehnologie și materiale dovedite. Aplicație, ciclu de funcționare sau condiții de funcționare similare. Experiență anterioară de test sau din teren, ori design nou cu o anumită experiență de test legată de defectare.",
        "Detail changes to previous design, using proven technology and materials. Similar application, duty cycle or operating conditions. Previous testing or field experience, or new design with some test experience related to the failure."),
      L("Designul ține cont de lecțiile învățate din designuri anterioare. Bunele practici au fost reevaluate pentru acest design, dar nu au fost încă dovedite. Controalele de prevenție pot găsi deficiențe ale produsului legate de cauză și dau o anumită indicație a performanței.",
        "Design addresses lessons learned from previous designs. Best Practices re-evaluated for this design but have not yet been proven. Prevention controls capable of finding deficiencies in the product related to the failure cause and provide some indication of performance.")],
    [4, L("Moderată", "Moderate"),
      L("Design aproape identic, cu expunere scurtă în teren. Aplicație similară, cu schimbări minore ale ciclului de funcționare sau ale condițiilor de funcționare. Experiență anterioară de test sau din teren.",
        "Almost identical design with short-term field exposure. Similar application, with minor change in duty cycle or operating conditions. Previous testing or field experience."),
      L("Designul predecesor și modificările pentru noul design respectă bunele practici, standardele și specificațiile. Controalele de prevenție pot găsi deficiențe ale produsului legate de cauză și indică o probabilă conformitate a designului.",
        "Predecessor design and changes for new design conform to best practices, standards, and specifications. Prevention controls capable of finding deficiencies in the product related to the failure cause and indicate likely design conformance.")],
    [3, L("Mică", "Low"),
      L("Modificări de detaliu ale unui design cunoscut (aceeași aplicație, cu schimbări minore ale ciclului sau condițiilor de funcționare) și experiență de test sau din teren în condiții comparabile, ori design nou cu procedură de test finalizată cu succes.",
        "Detail changes to known design (same application, with minor change in duty cycle or operating conditions) and testing or field experience under comparable operating conditions, or new design with successfully completed test procedure."),
      L("Designul este de așteptat să respecte standardele și bunele practici, ținând cont de lecțiile învățate. Controalele de prevenție pot găsi deficiențe ale produsului legate de cauză și prezic conformitatea designului de producție.",
        "Design expected to conform to Standards and Best Practices, considering Lessons Learned from previous designs. Prevention controls capable of finding deficiencies in the product related to the failure cause and predict conformance of production design.")],
    [2, L("Foarte mică", "Very low"),
      L("Design matur, aproape identic, cu expunere lungă în teren. Aceeași aplicație, cu ciclu și condiții de funcționare comparabile. Experiență de test sau din teren în condiții de funcționare comparabile.",
        "Almost identical mature design with long term field exposure. Same application, with comparable duty cycle and operating conditions. Testing or field experience under comparable operating conditions."),
      L("Designul este de așteptat să respecte standardele și bunele practici, ținând cont de lecțiile învățate, cu o marjă de încredere semnificativă. Controalele de prevenție pot găsi deficiențe ale produsului legate de cauză și indică încredere în conformitatea designului.",
        "Design expected to conform to standards and best practices, considering Lessons Learned from previous designs, with significant margin of confidence. Prevention controls capable of finding deficiencies in the product related to the failure cause and indicate confidence in design conformance.")],
    [1, L("Extrem de mică", "Extremely low"), L("Defectarea este eliminată prin controale de prevenție, iar cauza nu este posibilă prin design.", "Failure eliminated through preventive control and failure cause is not possible by design."), L("", "")]
  ];
  const O_NOTE = L("Experiența produsului: istoricul utilizării produsului în firmă (noutatea designului, a aplicației sau a cazului de utilizare); rezultatele controalelor de detecție deja făcute dau experiență cu designul. Controale de prevenție: bune practici de design, reguli de design, standarde ale firmei, lecții învățate, standarde industriale, specificații de material, reglementări și eficiența instrumentelor analitice de prevenție (CAE, modelare matematică, simulări, analiza toleranțelor, marje de siguranță). O 10, 9, 8, 7 pot scădea pe baza activităților de validare a produsului.",
    "Product Experience: history of product usage within the company (novelty of design, application or use case); results of already completed detection controls provide experience with the design. Prevention Controls: use of best practices for product design, design rules, company standards, lessons learned, industry standards, material specifications, government regulations and effectiveness of prevention oriented analytical tools including computer aided engineering, math modeling, simulation studies, tolerance stacks and design safety margins. O 10, 9, 8, 7 can drop based on product validation activities.");
  const MAT_LATE = L("Metodă de test dovedită pentru verificarea funcționalității sau validarea performanței, calității, fiabilității și durabilității; planificată târziu în ciclul de dezvoltare, astfel încât defectele găsite la test pot întârzia producția pentru re-proiectare și/sau re-sculare.",
    "Proven test method for verification of functionality or validation of performance, quality, reliability, and durability; planned timing is later in the product development cycle such that test failures may result in production delays for re-design and/or re-tooling.");
  const MAT_OK = L("Metodă de test dovedită pentru verificarea funcționalității sau validarea performanței, calității, fiabilității și durabilității; planificată suficient de devreme pentru a modifica sculele de producție înainte de lansarea în producție.",
    "Proven test method for verification of functionality or validation of performance, quality, reliability, and durability; planned timing is sufficient to modify production tools before release for production.");
  const ALL3 = L("Pass-Fail, test până la defectare, test de degradare", "Pass-Fail, Test-to-Fail, Degradation Testing");
  const D = [
    [10, L("Foarte mică", "Very low"), L("Procedura de test nu este încă dezvoltată.", "Test procedure yet to be developed."), L("Metoda de test nu este definită", "Test method not defined")],
    [9, L("Foarte mică", "Very low"), L("Metoda de test nu este concepută special pentru a detecta modul de defectare sau cauza.", "Test method not designed specifically to detect failure mode or cause."), ALL3],
    [8, L("Mică", "Low"), L("Metodă de test nouă, nedovedită.", "New test method; not proven."), ALL3],
    [7, L("Mică", "Low"), MAT_LATE, L("Pass-Fail", "Pass-Fail Testing")],
    [6, L("Moderată", "Moderate"), MAT_LATE, L("Test până la defectare", "Test-to-Failure")],
    [5, L("Moderată", "Moderate"), MAT_LATE, L("Test de degradare", "Degradation Testing")],
    [4, L("Mare", "High"), MAT_OK, L("Pass-Fail", "Pass-Fail Testing")],
    [3, L("Mare", "High"), MAT_OK, L("Test până la defectare", "Test-to-Failure")],
    [2, L("Mare", "High"), MAT_OK, L("Test de degradare", "Degradation Testing")],
    [1, L("Foarte mare", "Very high"), L("Testele anterioare au confirmat că modul de defectare sau cauza nu poate apărea, sau metodele de detecție s-au dovedit că detectează întotdeauna modul de defectare sau cauza.", "Prior testing confirmed that failure mode or cause cannot occur, or detection methods proven to always detect the failure mode or failure cause."), L("", "")]
  ];
  const OP = [
    [10, L("Extrem de mare", "Extremely high"), L("Niciunul", "None"), L("Nu există controale de prevenție.", "No prevention controls.")],
    [9, L("Foarte mare", "Very high"), L("Comportamental", "Behavioral"), L("Controalele de prevenție au un efect mic în prevenirea cauzei.", "Prevention controls will have little effect in preventing failure cause.")],
    [8, L("Foarte mare", "Very high"), L("Comportamental", "Behavioral"), L("Controalele de prevenție au un efect mic în prevenirea cauzei.", "Prevention controls will have little effect in preventing failure cause.")],
    [7, L("Mare", "High"), L("Comportamental sau tehnic", "Behavioral or Technical"), L("Controalele de prevenție sunt oarecum eficiente în prevenirea cauzei.", "Prevention controls somewhat effective in preventing failure cause.")],
    [6, L("Mare", "High"), L("Comportamental sau tehnic", "Behavioral or Technical"), L("Controalele de prevenție sunt oarecum eficiente în prevenirea cauzei.", "Prevention controls somewhat effective in preventing failure cause.")],
    [5, L("Moderată", "Moderate"), L("Comportamental sau tehnic", "Behavioral or Technical"), L("Controalele de prevenție sunt eficiente în prevenirea cauzei.", "Prevention controls are effective in preventing failure cause.")],
    [4, L("Moderată", "Moderate"), L("Comportamental sau tehnic", "Behavioral or Technical"), L("Controalele de prevenție sunt eficiente în prevenirea cauzei.", "Prevention controls are effective in preventing failure cause.")],
    [3, L("Mică", "Low"), L("Bune practici: comportamental sau tehnic", "Best Practices: Behavioral or Technical"), L("Controalele de prevenție sunt foarte eficiente în prevenirea cauzei.", "Prevention controls are highly effective in preventing failure cause.")],
    [2, L("Foarte mică", "Very low"), L("Bune practici: comportamental sau tehnic", "Best Practices: Behavioral or Technical"), L("Controalele de prevenție sunt foarte eficiente în prevenirea cauzei.", "Prevention controls are highly effective in preventing failure cause.")],
    [1, L("Extrem de mică", "Extremely low"), L("Tehnic", "Technical"), L("Controalele de prevenție sunt extrem de eficiente: cauza nu poate apărea datorită designului (de exemplu geometria piesei) sau procesului (de exemplu designul dispozitivului de fixare sau al sculei). Intenția controalelor de prevenție: modul de defectare nu poate fi produs fizic de cauză.",
      "Prevention controls are extremely effective in preventing failure cause from occurring due to design (e.g. part geometry) or process (e.g. fixture or tooling design). Intent of prevention controls - Failure Mode cannot be physically produced due to the Failure Cause.")]
  ];
  const OP_NOTE = L("Eficiența controalelor de prevenție: controalele sunt tehnice (se bazează pe mașini, durata de viață a sculei, materialul sculei etc.), bune practici (dispozitive de fixare, designul sculei, proceduri de calibrare, verificarea error-proofing, mentenanță preventivă, instrucțiuni de lucru, fișe SPC, monitorizarea procesului, designul produsului etc.) sau comportamentale (operatori certificați sau necertificați, meseriași calificați, șefi de echipă etc.). O este o evaluare calitativă predictivă, făcută la momentul analizei; la controale multiple se alege valoarea care reflectă cel mai bine robustețea controlului.",
    "Prevention Control Effectiveness: consider if prevention controls are technical (rely on machines, tool life, tool material, etc.), or use best practices (fixtures, tool design, calibration procedures, error-proofing verification, preventive maintenance, work instructions, statistical process control charting, process monitoring, product design, etc.) or behavioral (rely on certified or non-certified operators, skilled trades, team leaders, etc.). Occurrence is a predictive qualitative rating made at the time of evaluation; for prevention controls with multiple ratings, use the rating that best reflects the robustness of the control.");
  /* Action Priority table, AIAG-VDA (same for DFMEA and PFMEA); columns D 7-10, 5-6, 2-4, 1 */
  const AP = {
    "9-10": { "8-10": "HHHH", "6-7": "HHHH", "4-5": "HHHM", "2-3": "HMLL", "1": "LLLL" },
    "7-8":  { "8-10": "HHHH", "6-7": "HHHM", "4-5": "HMMM", "2-3": "MMLL", "1": "LLLL" },
    "4-6":  { "8-10": "HHMM", "6-7": "MMML", "4-5": "MLLL", "2-3": "LLLL", "1": "LLLL" },
    "2-3":  { "8-10": "MMLL", "6-7": "LLLL", "4-5": "LLLL", "2-3": "LLLL", "1": "LLLL" },
    "1":    { "8-10": "LLLL", "6-7": "LLLL", "4-5": "LLLL", "2-3": "LLLL", "1": "LLLL" }
  };
  function apOf(s, o, d) {
    if (!s || !o || !d) return null;
    const sb = s >= 9 ? "9-10" : s >= 7 ? "7-8" : s >= 4 ? "4-6" : s >= 2 ? "2-3" : "1";
    const ob = o >= 8 ? "8-10" : o >= 6 ? "6-7" : o >= 4 ? "4-5" : o >= 2 ? "2-3" : "1";
    const di = d >= 7 ? 0 : d >= 5 ? 1 : d >= 2 ? 2 : 3;
    return AP[sb][ob][di];
  }
  /* HTML tables for the reference panels; lang "ro" / "en", esc = HTML escape */
  const H = { ro: { s: "Efect", crit: "Criteriu", pred: "Predicția apariției cauzei", ctl: "Controale de prevenție", type: "Tip de control", ab: "Capacitate de detecție", mat: "Maturitatea metodei de detecție", opp: "Oportunitatea de detecție" },
    en: { s: "Effect", crit: "Criteria", pred: "Prediction of failure cause occurring", ctl: "Prevention controls", type: "Type of control", ab: "Ability to detect", mat: "Detection method maturity", opp: "Opportunity for detection" } };
  function table(kind, lang, esc) {
    const h = H[lang] || H.ro, tr = (x) => esc(x[lang] || x.ro);
    const row = (cells) => "<tr>" + cells.map((c, i) => (i === 0 ? '<td class="c">' + c + "</td>" : "<td>" + c + "</td>")).join("") + "</tr>";
    if (kind === "S") return '<table class="mini aiag"><tr><th>S</th><th>' + h.s + "</th><th>" + h.crit + "</th></tr>" + S.map((x) => row([x[0], tr(x[1]), tr(x[2])])).join("") + "</table>";
    if (kind === "O") return '<table class="mini aiag"><tr><th>O</th><th>' + h.pred + "</th><th>" + h.crit + "</th></tr>" + O.map((x) => row([x[0], tr(x[1]), tr(x[2]) + (x[3][lang] ? '<br><span class="muted">' + tr(x[3]) + "</span>" : "")])).join("") + "</table>" +
      '<p class="muted aiagnote">' + tr(O_NOTE) + "</p>";
    if (kind === "D") return '<table class="mini aiag"><tr><th>D</th><th>' + h.ab + "</th><th>" + h.mat + "</th><th>" + h.opp + "</th></tr>" + D.map((x) => row([x[0], tr(x[1]), tr(x[2]), tr(x[3])])).join("") + "</table>";
    if (kind === "OP") return '<table class="mini aiag"><tr><th>O</th><th>' + h.pred + "</th><th>" + h.type + "</th><th>" + h.ctl + "</th></tr>" + OP.map((x) => row([x[0], tr(x[1]), tr(x[2]), tr(x[3])])).join("") + "</table>" +
      '<p class="muted aiagnote">' + tr(OP_NOTE) + "</p>";
    if (kind === "AP") {
      /* one small O x D matrix per severity band, side by side: wide and short instead of 30 rows */
      return '<div class="apgrid">' + ["9-10", "7-8", "4-6", "2-3", "1"].map((sb) => '<table class="mini apm"><tr><th colspan="5" class="c">S ' + sb + "</th></tr>" +
        '<tr><th></th><th class="c">D 7–10</th><th class="c">D 5–6</th><th class="c">D 2–4</th><th class="c">D 1</th></tr>' +
        ["8-10", "6-7", "4-5", "2-3", "1"].map((ob) => '<tr><th class="c">O ' + ob + "</th>" +
          AP[sb][ob].split("").map((a) => '<td class="c"><span class="ap ' + a + '">' + a + "</span></td>").join("") + "</tr>").join("") + "</table>").join("") + "</div>";
    }
    return "";
  }
  /* short option labels for the selects (one line); the full handbook text stays in the reference tables and in the option tooltip */
  const SH = {
    S: { 10: L("Afectează siguranța vehiculului sau sănătatea persoanelor", "Affects safe vehicle operation or people's health"),
      9: L("Neconformitate cu reglementările", "Noncompliance with regulations"),
      8: L("Pierderea unei funcții principale a vehiculului", "Loss of a primary vehicle function"),
      7: L("Degradarea unei funcții principale a vehiculului", "Degradation of a primary vehicle function"),
      6: L("Pierderea unei funcții secundare a vehiculului", "Loss of a secondary vehicle function"),
      5: L("Degradarea unei funcții secundare a vehiculului", "Degradation of a secondary vehicle function"),
      4: L("Aspect, sunet sau vibrații foarte deranjante", "Very objectionable appearance, sound or vibration"),
      3: L("Aspect, sunet sau vibrații moderat deranjante", "Moderately objectionable appearance, sound or vibration"),
      2: L("Aspect, sunet sau vibrații ușor deranjante", "Slightly objectionable appearance, sound or vibration"),
      1: L("Niciun efect perceptibil", "No discernible effect") },
    O: { 10: L("tehnologie nouă, fără experiență și fără prevenție", "new technology, no experience, no prevention"),
      9: L("prima utilizare în firmă, inovații noi, fără validare", "first use in the company, new innovations, no validation"),
      8: L("inovații noi într-o aplicație nouă, fără validare", "new innovations in a new application, no validation"),
      7: L("design nou pe tehnologie similară, prevenție limitată", "new design on similar technology, limited prevention"),
      6: L("design similar, condiții de funcționare schimbate, prevenție parțială", "similar design, changed operating conditions, some prevention"),
      5: L("modificări de detaliu, tehnologie dovedită, lecții învățate aplicate", "detail changes, proven technology, lessons learned applied"),
      4: L("design aproape identic, respectă standardele și bunele practici", "almost identical design, conforms to standards and best practices"),
      3: L("design cunoscut, testat în condiții comparabile", "known design, tested under comparable conditions"),
      2: L("design matur, expunere lungă în teren", "mature design, long field exposure"),
      1: L("cauza nu este posibilă prin design", "the cause is not possible by design") },
    D: { 10: L("nu există încă procedură de test", "no test procedure yet"),
      9: L("testul nu vizează modul de defectare sau cauza", "the test does not target the failure mode or cause"),
      8: L("metodă de test nouă, nedovedită", "new, unproven test method"),
      7: L("test dovedit, făcut târziu, pass / fail", "proven test, done late, pass / fail"),
      6: L("test dovedit, făcut târziu, test până la defectare", "proven test, done late, test-to-failure"),
      5: L("test dovedit, făcut târziu, test de degradare", "proven test, done late, degradation test"),
      4: L("test dovedit, făcut la timp, pass / fail", "proven test, done in time, pass / fail"),
      3: L("test dovedit, făcut la timp, test până la defectare", "proven test, done in time, test-to-failure"),
      2: L("test dovedit, făcut la timp, test de degradare", "proven test, done in time, degradation test"),
      1: L("detectează sigur sau cauza nu poate apărea", "always detects, or the cause cannot occur") }
  };
  const tl = (x, lang) => x[lang] || x.ro;
  /* each option: [value, short label, full handbook text for the tooltip] */
  const short = {
    S: (lang) => S.map((x) => [x[0], x[0] + " · " + tl(SH.S[x[0]], lang), tl(x[2], lang)]),
    O: (lang) => O.map((x) => [x[0], x[0] + " · " + tl(x[1], lang) + " · " + tl(SH.O[x[0]], lang), tl(x[2], lang)]),
    D: (lang) => D.map((x) => [x[0], x[0] + " · " + tl(x[1], lang) + " · " + tl(SH.D[x[0]], lang), tl(x[2], lang) + (x[3][lang] ? " (" + tl(x[3], lang) + ")" : "")]),
    OP: (lang) => OP.map((x) => [x[0], x[0] + " · " + tl(x[2], lang) + " · " + tl(x[3], lang), tl(x[3], lang)])
  };
  window.AIAG = { S: S, O: O, D: D, OP: OP, O_NOTE: O_NOTE, OP_NOTE: OP_NOTE, AP: AP, apOf: apOf, table: table, options: short };
})();
