// HW TCA lab guide, in the style of the faculty's lab guides (short theory, then numbered exercises).
// Block types: h (section heading), p (paragraph), ex (exercise: heading + paragraphs/list), table, box (formula box), img, list, links
const APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/hw/";
const IMG = "/home/claude/sw-tca-lab/materials/img/";

const RULES = [
  ["PAS-SMD (R, C)", "Missing", 1, 3, 1, 5], ["PAS-SMD (R, C)", "Short", 5, 5, 1, 5], ["PAS-SMD (R, C)", "Open", 1, 5, 1, 5], ["PAS-SMD (R, C)", "Wrong value", 10, 10, 1, 5],
  ["DIODE (LED)", "Missing", 1, 3, 1, 5], ["DIODE (LED)", "Short", 5, 5, 1, 5], ["DIODE (LED)", "Open", 1, 5, 1, 5], ["DIODE (LED)", "Wrong value", 10, 10, 5, 10], ["DIODE (LED)", "Wrong polarity", 1, 10, 1, 5],
  ["IC-LEADED (U1)", "Missing", 1, 1, 1, 5], ["IC-LEADED (U1)", "Pin open", 1, 5, 1, 10], ["IC-LEADED (U1)", "Pin short", 1, 1, 1, 10], ["IC-LEADED (U1)", "Pin wrong functionality", 10, 10, 10, 10],
  ["CONN-THT (J1, J2, JP1)", "Missing", 1, 1, 1, 10], ["CONN-THT (J1, J2, JP1)", "Pin open", 10, 3, 1, 10], ["CONN-THT (J1, J2, JP1)", "Pin short", 10, 1, 1, 10],
  ["CONN-THT (J1, J2, JP1)", "Wrong value", 1, 10, 1, 5], ["CONN-THT (J1, J2, JP1)", "Short", 1, 10, 1, 5], ["CONN-THT (J1, J2, JP1)", "Open", 10, 3, 1, 5]
];
// AP: rows S band x O band, columns D 7-10, 5-6, 2-4, 1
const AP = [["9–10", "8–10", "H H H H"], ["9–10", "6–7", "H H H H"], ["9–10", "4–5", "H H H M"], ["9–10", "2–3", "H M L L"], ["9–10", "1", "L L L L"],
  ["7–8", "8–10", "H H H H"], ["7–8", "6–7", "H H H M"], ["7–8", "4–5", "H M M M"], ["7–8", "2–3", "M M L L"], ["7–8", "1", "L L L L"],
  ["4–6", "8–10", "H H M M"], ["4–6", "6–7", "M M M L"], ["4–6", "4–5", "M L L L"], ["4–6", "2–3", "L L L L"], ["4–6", "1", "L L L L"],
  ["2–3", "8–10", "M M L L"], ["2–3", "6–7", "L L L L"], ["2–3", "4–5", "L L L L"], ["2–3", "2–3", "L L L L"], ["2–3", "1", "L L L L"], ["1", "1–10", "L L L L"]];

module.exports = {
ro: {
  file: "HW_TCA_Laborator_RO.docx",
  title: "Analiza acoperirii testelor de producție (HW TCA)",
  blocks: [
    { t: "h", x: "Ce este analiza acoperirii testelor" },
    { t: "p", x: "După asamblare, o placă electronică trece prin mai multe etape de test: inspecție optică automată (AOI), inspecție cu raze X (AXI), test în circuit (ICT) și test funcțional (FT). Fiecare etapă vede alte tipuri de defecte. Analiza acoperirii testelor (Test Coverage Analysis, TCA) răspunde la întrebarea: dacă placa are un anumit defect de fabricație, îl prinde vreun test înainte să ajungă la client, și cât de sigur?" },
    { t: "p", x: "Un test trecut spune doar că proprietățile măsurate sunt în regulă. Dacă ICT măsoară un rezistor, știm că există, are valoarea corectă și nu este întrerupt sau scurtcircuitat; despre componentele pe care nu le-am măsurat nu știm nimic. De aceea analiza nu numără testele, ci ia fiecare mod de defectare posibil și îi dă o valoare de detecție pentru fiecare metodă de test." },
    { t: "p", x: "Metodele de test folosite în laborator sunt:" },
    { t: "table", w: [1300, 2900, 2700, 2700], head: ["Metodă", "Ce face", "Prinde bine", "Limitări"], rows: [
      ["AOI", "Camera compară placa cu imaginea de referință.", "componentă lipsă, polaritate, aliniere, punți de lipire vizibile", "nu vede lipiturile ascunse; nu citește valoarea componentelor nemarcate"],
      ["AXI", "Imagine cu raze X a lipiturilor.", "lipituri ascunse, scurtcircuite, calitatea lipiturii", "nu vede valoarea sau funcția componentei"],
      ["ICT", "Un fixture cu ace atinge test point-urile și măsoară componentele una câte una.", "valoare, scurtcircuit, întrerupere", "are nevoie de test point pe fiecare net al componentei"],
      ["FT", "Placa este alimentată și funcțiile sunt verificate prin conectori.", "funcția la viteza reală", "de multe ori nu arată care componentă este defectă"]] },
    { t: "ex", n: 1, x: ["Pentru fiecare defect de mai jos, spuneți ce metodă (AOI, AXI, ICT sau FT) îl poate prinde cel mai sigur și de ce:"],
      list: ["un rezistor SMD lipsă;", "un condensator SMD nemarcat, cu valoare greșită;", "un pin al unui conector THT neconectat, lipitura fiind pe fața BOTTOM;", "un driver CAN defect în interiorul transceiverului;", "o punte de lipire ascunsă sub capsula unui circuit integrat."] },

    { t: "h", x: "Modelul PCOLA/SOQ/FAM" },
    { t: "p", x: "Modelul PCOLA/SOQ, introdus de Hird, Parker și Follis (ITC 2002), descrie ce proprietăți verifică un test. Pentru componentă: P (presence, prezența), C (correctness, piesa corectă), O (orientation, polaritatea), L (live, piesa funcționează), A (alignment, alinierea pe pad-uri). Pentru conexiune: S (shorts, scurtcircuite), O (opens, întreruperi), Q (quality, calitatea lipiturii). iNEMI a adăugat partea funcțională, FAM: F (feature, funcția există), A (at-speed, la viteza reală), M (measurement, performanța măsurată)." },
    { t: "ex", n: 2, x: ["Încadrați fiecare defect din exercițiul 1 într-una dintre literele PCOLA, SOQ sau FAM."] },

    { t: "h", x: "Studiul de caz: modulul CAN al radarului frontal" },
    { t: "p", x: "Un radar frontal auto generic (ipoteza laboratorului: ASIL B) trimite lista de obiecte detectate pe CAN, la 500 kbit/s. Interfața CAN folosește un modul cu transceiverul MCP2551. Placa are 13 componente și nu are test point-uri. Componentele THT (J1, J2, JP1) au lipiturile pe fața BOTTOM, iar AOI inspectează inițial doar fața TOP." },
    { t: "table", w: [1500, 3500, 4600], head: ["Componentă", "Net-uri", "Rol"], rows: [
      ["J1", "VDD, TXD, RXD, GND", "conector spre senzor (alimentare și date de la microcontroler)"], ["U1", "TXD, GND, VDD, RXD, VREF (neconectat), CANL, CANH, RS", "transceiver CAN MCP2551 (SOIC-8)"],
      ["C3", "VDD – GND", "decuplarea alimentării"], ["R3", "RS – GND", "alege modul de lucru al lui U1"], ["R4 + JP1", "CANH – N_TERM – CANL", "terminația de 120 Ω, activată cu jumperul JP1"],
      ["R1 / C1", "CANH – N_F1 – GND", "filtru RC pe CANH (EMC)"], ["R2 / C2", "CANL – N_F2 – GND", "filtru RC pe CANL (EMC)"], ["J2", "CANH, CANL, GND", "conector spre bus-ul CAN"], ["LED1 + R5", "VDD – N_LED – GND", "indicator de alimentare"]] },
    { t: "img", f: "h0_schematic_ro.png", w: 15.5, cap: "Schema modulului, așa cum apare în aplicație (butonul SCHEMĂ)." },
    { t: "p", x: "Lucrați în aplicația web HW TCA Lab, în browser, fără instalare. Completați numele, grupa și codul de variantă primit (H1–H6) și apăsați Încarcă varianta. Placa și schema sunt interactive: când apăsați pe un pin (pad), aplicația desenează netul acelui pin, iar panoul Conexiuni arată unde merge semnalul, dacă netul ajunge la un conector și dacă are test point." },
    { t: "img", f: "h0_conn_ro.png", w: 11, cap: "Pinul 2 (CAN_L) al lui J2 selectat: linia albastră leagă toți pinii de pe netul CANL." },
    { t: "ex", n: 3, x: ["În aplicație, apăsați pe pinul 7 (CANH) al lui U1. Notați toate componentele de pe netul CANH, conectorul la care ajunge netul și dacă are test point. Repetați pentru pinul 8 (RS). Ce diferență observați între cele două net-uri, din punctul de vedere al testului funcțional?"] },

    { t: "h", x: "Severitatea (S)" },
    { t: "p", x: "Riscul fiecărui mod de defectare se descrie, după manualul AIAG-VDA FMEA (2019), prin trei note de la 1 la 10: severitatea S, ocurența O și detecția D. Severitatea se dă pe efect: cât de grav este efectul la client. În laborator, S rezultă din clasa de efect:" },
    { t: "table", w: [1100, 700, 7800], head: ["Clasă", "S", "Descriere"], rows: [
      ["E10", "10", "Afectează siguranța vehiculului, a ocupanților sau a altor participanți la trafic"], ["E9", "9", "Neconformitate cu reglementările (EMC: emisii sau imunitate)"],
      ["E8", "8", "Pierderea funcției principale (fără comunicație CAN sau fără funcționare)"], ["E7", "7", "Degradarea funcției principale (comunicație coruptă sau intermitentă)"],
      ["E6", "6", "Pierderea unei funcții secundare (indicatorul LED nu funcționează)"], ["E5", "5", "Degradarea unei funcții secundare (indicație LED greșită)"],
      ["E2", "2", "Efect ușor deranjant, fără efect funcțional sau EMC"], ["E1", "1", "Niciun efect perceptibil"]] },
    { t: "p", x: "Efectele care afectează doar filtrarea EMC primesc E9 (UNECE R10), chiar dacă funcția nu este afectată." },
    { t: "ex", n: 4, x: ["Stabiliți clasa de efect și severitatea pentru:"], list: ["LED-ul de alimentare nu se aprinde;", "lipsește filtrul RC de pe CANH;", "modulul nu comunică pe CAN;", "cadrele CAN ajung uneori corupte."] },
    { t: "ex", n: 5, x: ["În aplicație, alegeți clasa de efect pentru toate modurile de defectare din varianta voastră."] },

    { t: "h", x: "Ocurența (O)" },
    { t: "p", x: "Ocurența se dă pe cauză: cât de probabil apare defectul, ținând cont de prevenție. Pentru o tehnologie SMT matură, cu proces stabil, valoarea este de obicei mică." },
    { t: "table", w: [900, 8700], head: ["O", "Criteriu (rezumat AIAG-VDA)"], rows: [
      ["10", "Prima aplicare a unei tehnologii noi; fără experiență, standarde sau bune practici"], ["9", "Prima utilizare în firmă a unor inovații sau materiale noi"], ["8", "Inovații folosite într-o aplicație nouă; puține standarde aplicabile"],
      ["7", "Design nou pe tehnologie similară, aplicație nouă"], ["6", "Similar cu designuri anterioare, condiții de utilizare modificate"], ["5", "Modificări de detaliu pe un design dovedit; lecții învățate aplicate, dar nedovedite"],
      ["4", "Design aproape identic, expunere scurtă în teren"], ["3", "Modificări de detaliu pe un design cunoscut, cu experiență de test sau teren comparabilă"], ["2", "Design matur, aproape identic, cu expunere lungă în teren"], ["1", "Cauza e eliminată prin prevenție; nu e posibilă prin design"]] },
    { t: "ex", n: 6, x: ["În aplicație, alegeți O pentru fiecare mod. Folosiți aceeași logică pentru toate modurile și explicați-o în concluzia raportului."] },

    { t: "h", x: "Detecția la AOI, AXI și ICT" },
    { t: "p", x: "Detecția D spune cât de sigur prindem defectul înainte să plece placa: 1 înseamnă că metoda îl detectează mereu, 10 că nu îl putem detecta. Pentru AOI, AXI și ICT, aplicația calculează D din regulile de detecție de mai jos și afișează motivul. Valoarea ICT „cu TP” se folosește doar dacă toate net-urile componentei au test point." },
    { t: "table", w: [2500, 2300, 1100, 1100, 1300, 1300], head: ["Categorie", "Mod de defectare", "AOI", "AXI", "ICT cu TP", "ICT fără TP"], rows: RULES, small: true },
    { t: "p", x: "Două reguli suplimentare: C5 – la conectorii THT, defectele de lipire (pin open, pin short, open) sunt pe fața BOTTOM, pe care AOI nu o inspectează inițial, deci AOI = 10; dacă se activează AOI pe BOTTOM, devine 1. C7 – componentele marcate (R1–R5, U1) au valoarea scrisă pe capsulă, deci AOI prinde parțial o valoare greșită (D = 5)." },
    { t: "ex", n: 7, x: ["Fără aplicație, folosind tabelul și regulile C5 și C7, stabiliți D AOI, D AXI și D ICT (fără test point-uri) pentru:"], list: ["R1 short;", "J2, pinul 1 (CAN_H), pin open;", "U1, pinul 4 (RXD), pin open;", "R2 wrong value."] },
    { t: "ex", n: 8, x: ["În aplicație, verificați valorile AOI, AXI și ICT pentru modurile din varianta voastră. Alegeți două moduri și explicați, în cuvintele voastre, motivul afișat de aplicație."] },

    { t: "h", x: "Detecția la testul funcțional (FT)" },
    { t: "p", x: "Testul funcțional se face prin conectori, la 500 kbit/s, cu limitele de mai jos. Detecția FT o stabiliți voi: alegeți testul care se potrivește cu componenta și cu tipul defectului, sau NONE (D = 10), apoi alegeți D din scala de detecție și scrieți de ce. Un defect poate fi văzut de testul funcțional doar dacă netul lui ajunge, direct sau prin funcția modulului, la un pin de conector." },
    { t: "table", w: [700, 1700, 2600, 1800, 2800], head: ["Test", "Denumire", "Ce se măsoară", "Limite", "Ce poate prinde"], small: true, rows: [
      ["FT1", "Consum de curent", "IDD pe VDD (J1), în recesiv și dominant", "Recesiv ≤ 10 mA; dominant ≤ 75 mA", "Short pe C3, short / wrong polarity LED1, pin short U1 (VDD–GND), U1 missing, wrong functionality VDD"],
      ["FT2", "Indicator de alimentare", "LED1 aprins, verificat cu un senzor optic", "Aprins la VDD nominal", "LED1 open / missing / wrong polarity, R5 open / missing"],
      ["FT3", "Tensiuni pe bus în recesiv", "VCANH, VCANL fără sarcină, TXD = 1", "2,0 – 3,0 V", "Short R1/C1, R2/C2 (linie la GND), pin open / short U1 pe CANH / CANL"],
      ["FT4", "Tensiune diferențială în dominant", "VCANH – VCANL cu sarcină 40–60 Ω, TXD = 0", "1,5 – 3,0 V", "Driver defect (wrong functionality CANH / CANL), R3 wrong value (mod standby)"],
      ["FT5", "Loopback TXD → RXD", "Se comută TXD; RXD urmează starea bus-ului", "RXD = 0 în dominant, 1 în recesiv", "Pin open TXD / RXD pe U1 și J1, wrong functionality TXD / RXD, mod standby greșit (R3)"],
      ["FT6", "Rezistență de terminație", "CAN_H–CAN_L pe J2, cu JP1 montat și nemontat", "≈ 120 Ω cu JP1; ≥ 20 kΩ fără", "R4 open / missing / wrong value, JP1 missing / open / short"],
      ["FT7", "Transmisie CAN prin conectori", "Testerul trimite cadre pe TXD (J1); un nod de referință pe J2 le confirmă (ACK)", "Toate cadrele corecte, fără error frames", "Pin open / short pe J1 (VDD, TXD, GND) și J2 (CAN_H, CAN_L), U1 TXD / CANH / CANL / RS, R3 open / missing / wrong value, short R1/C1, R2/C2"],
      ["FT8", "Recepție CAN prin conectori", "Nodul de referință trimite cadre pe J2; testerul citește RXD pe J1", "Toate cadrele citite corect", "Pin open / short pe J1 (RXD) și J2 (CAN_H, CAN_L), U1 RXD / CANH / CANL, wrong functionality RXD"]] },
    { t: "p", x: "Analiza se face pe design, așa că folosim scala de detecție DFMEA (rezumat AIAG-VDA):" },
    { t: "table", w: [900, 8700], head: ["D", "Criteriu (rezumat AIAG-VDA)"], rows: [
      ["10", "Procedura de test nu e încă dezvoltată; metodă nedefinită"], ["9", "Metoda de test nu e concepută special pentru acest mod sau această cauză"], ["8", "Metodă de test nouă, nedovedită"],
      ["7", "Metodă dovedită, planificată târziu (pass / fail)"], ["6", "Metodă dovedită, planificată târziu (test până la defectare)"], ["5", "Metodă dovedită, planificată târziu (test de degradare)"],
      ["4", "Metodă dovedită, la timp înainte de lansare (pass / fail)"], ["3", "Metodă dovedită, la timp înainte de lansare (test până la defectare)"], ["2", "Metodă dovedită, la timp înainte de lansare (test de degradare)"],
      ["1", "Testele anterioare confirmă că defectul nu poate apărea, sau metoda îl detectează mereu"]] },
    { t: "ex", n: 9, x: ["În aplicație, pentru fiecare mod de defectare: apăsați pe pinul componentei și urmăriți netul în panoul Conexiuni, alegeți testul FT1–FT8 sau NONE, alegeți D FT din listă și scrieți justificarea. O valoare fără justificare nu se punctează."] },

    { t: "h", x: "Detecția combinată și prioritatea de acțiune (AP)" },
    { t: "p", x: "Toate testele rulează pe fiecare placă, așa că detecția combinată este minimul dintre valorile metodelor. Din S, O și D rezultă prioritatea de acțiune AP (H, M sau L), din tabelul AIAG-VDA. Nu folosim RPN = S × O × D: același RPN poate ascunde riscuri foarte diferite (Bowles, 2003)." },
    { t: "box", x: ["D = min(D AOI, D AXI, D ICT, D FT)", "AP = tabel AIAG-VDA (banda lui S, banda lui O, banda lui D)"] },
    { t: "table", w: [1200, 1200, 1800, 1800, 1800, 1800], head: ["S", "O", "D 7–10", "D 5–6", "D 2–4", "D 1"], rows: AP.map((r) => [r[0], r[1]].concat(r[2].split(" "))), small: true },
    { t: "p", x: "Avem următorul exemplu, din varianta demonstrativă H0 (o puteți încărca în aplicație cu codul H0): J2, pinul 2 (CAN_L), pin open. Lipitura este pe fața BOTTOM, deci AOI = 10 (C5). AXI = 3. ICT = 10, pentru că nu există test point pe CANL. Testul potrivit este FT7, dar cu CAN_L întrerupt comunicația poate funcționa încă pe distanță scurtă, deci FT7 nu prinde sigur defectul. Cu S = 8 (E8), O = 2 și D FT = 5: D = min(10, 3, 10, 5) = 3, iar AP = L. Dacă se activează AOI pe BOTTOM, AOI = 1 și D devine 1." },
    { t: "ex", n: 10, x: ["Calculați D și AP pentru:"], list: ["S = 8, O = 2; D AOI = 10, D AXI = 3, D ICT = 10, D FT = 5;", "S = 9, O = 4; D AOI = 5, D AXI = 5, D ICT = 5, D FT = 10;", "S = 7, O = 4; D AOI = 10, D AXI = 10, D ICT = 5, D FT = 10."] },
    { t: "ex", n: 11, x: ["Calculați RPN și AP pentru A: S = 9, O = 4, D = 3 și B: S = 3, O = 6, D = 6. Ce observați? Care risc ar trebui tratat primul?"] },

    { t: "h", x: "Îmbunătățiri" },
    { t: "p", x: "Pentru modurile cu AP H sau M se caută îmbunătățiri: test point-uri (ICT poate măsura componenta), AOI pe fața BOTTOM (lipiturile THT) sau teste FT noi (ce se măsoară, unde, ce limită). Fiecare îmbunătățire are un cost: un test point ocupă loc pe placă și un pin în fixture, un test nou adaugă timp de test. Se propune doar ce reduce un risc." },
    { t: "ex", n: 12, x: ["Pe ce net-uri trebuie adăugate test point-uri pentru ca ICT să poată măsura R1? Dar C2? Verificați răspunsul în aplicație, apăsând pe pinii componentelor."] },
    { t: "ex", n: 13, x: ["În aplicație, propuneți îmbunătățiri pentru modurile cu AP H sau M din varianta voastră. Notați, pentru fiecare, AP înainte și după îmbunătățire."] },

    { t: "h", x: "Riscul rezidual și raportul" },
    { t: "p", x: "Evaluarea riscului înseamnă identificare, analiză și evaluare (ISO 31000). Ce rămâne după îmbunătățiri este riscul rezidual: trebuie documentat, cu motivul pentru care rămâne și cu decizia luată (risc acceptat sau acțiune propusă)." },
    { t: "ex", n: 14, x: ["Pentru modurile care rămân H sau M după îmbunătățiri, completați în aplicație coloana „Evaluarea riscului rezidual”: alegeți risc acceptat sau acțiune propusă și scrieți de ce."] },
    { t: "ex", n: 15, x: ["În tab-ul Raport, scrieți propunerile de îmbunătățire și concluzia, verificați fișa generată și apăsați Trimite raportul. Dacă trimiterea nu este confirmată, descărcați raportul (.html) și păstrați-l."] },

    { t: "h", x: "Resurse" },
    { t: "links", items: [["Aplicația HW TCA Lab", APP], ["K. Hird, K. P. Parker, B. Follis, „Test Coverage: What Does It Mean When a Board Test Passes?”, ITC 2002", "https://doi.org/10.1109/TEST.2002.1041863"],
      ["J. B. Bowles, „An Assessment of RPN Prioritization in a Failure Modes Effects and Criticality Analysis”, RAMS 2003", "https://doi.org/10.1109/RAMS.2003.1182019"],
      ["Microchip, MCP2551 High-Speed CAN Transceiver (fișă tehnică)", "https://www.microchip.com/en-us/product/MCP2551"], ["AIAG & VDA, FMEA Handbook (2019)", "https://www.aiag.org"]] }
  ]
},
en: {
  file: "HW_TCA_Lab_EN.docx",
  title: "Production Test Coverage Analysis (HW TCA)",
  blocks: [
    { t: "h", x: "What test coverage analysis is" },
    { t: "p", x: "After assembly, a circuit board goes through several test stages: automated optical inspection (AOI), X-ray inspection (AXI), in-circuit test (ICT) and functional test (FT). Each stage sees different defect types. Test coverage analysis (TCA) answers the question: if the board has a given manufacturing defect, does any test catch it before it reaches the customer, and how reliably?" },
    { t: "p", x: "A passed test only says that the measured properties are fine. If ICT measures a resistor, we know it is present, has the right value and is neither open nor shorted; we know nothing about the components we did not measure. That is why the analysis does not count tests; it takes every possible failure mode and gives it a detection value for each test method." },
    { t: "p", x: "The test methods used in the lab are:" },
    { t: "table", w: [1300, 2900, 2700, 2700], head: ["Method", "What it does", "Good at", "Limitations"], rows: [
      ["AOI", "A camera compares the board with a reference image.", "missing part, polarity, alignment, visible solder bridges", "cannot see hidden joints; cannot read the value of unmarked parts"],
      ["AXI", "X-ray image of the solder joints.", "hidden joints, shorts, joint quality", "cannot see the value or function of a part"],
      ["ICT", "A bed-of-nails fixture contacts the test points and measures the parts one by one.", "value, short, open", "needs a test point on every net of the part"],
      ["FT", "The board is powered and its functions are checked through the connectors.", "function at real speed", "often cannot tell which part is faulty"]] },
    { t: "ex", n: 1, x: ["For each defect below, say which method (AOI, AXI, ICT or FT) catches it most reliably, and why:"],
      list: ["a missing SMD resistor;", "an unmarked SMD capacitor with the wrong value;", "an unconnected pin of a THT connector, soldered on the BOTTOM side;", "a faulty CAN driver inside the transceiver;", "a solder bridge hidden under an IC package."] },

    { t: "h", x: "The PCOLA/SOQ/FAM model" },
    { t: "p", x: "The PCOLA/SOQ model, introduced by Hird, Parker and Follis (ITC 2002), describes which properties a test verifies. For the component: P (presence), C (correctness, the right part), O (orientation, polarity), L (live, the part works), A (alignment on the pads). For the connection: S (shorts), O (opens), Q (quality of the joint). iNEMI added the functional part, FAM: F (feature, the function exists), A (at-speed), M (measurement, the measured performance)." },
    { t: "ex", n: 2, x: ["Assign each defect from exercise 1 to one of the PCOLA, SOQ or FAM letters."] },

    { t: "h", x: "The case study: the front radar's CAN module" },
    { t: "p", x: "A generic automotive front radar (lab assumption: ASIL B) sends its list of detected objects over CAN at 500 kbit/s. The CAN interface uses a module with the MCP2551 transceiver. The board has 13 components and no test points. The THT components (J1, J2, JP1) are soldered on the BOTTOM side, and AOI initially inspects only the TOP side." },
    { t: "table", w: [1500, 3500, 4600], head: ["Component", "Nets", "Role"], rows: [
      ["J1", "VDD, TXD, RXD, GND", "connector to the sensor (supply and data from the microcontroller)"], ["U1", "TXD, GND, VDD, RXD, VREF (not connected), CANL, CANH, RS", "MCP2551 CAN transceiver (SOIC-8)"],
      ["C3", "VDD – GND", "supply decoupling"], ["R3", "RS – GND", "selects the operating mode of U1"], ["R4 + JP1", "CANH – N_TERM – CANL", "120 Ω termination, enabled with jumper JP1"],
      ["R1 / C1", "CANH – N_F1 – GND", "RC filter on CANH (EMC)"], ["R2 / C2", "CANL – N_F2 – GND", "RC filter on CANL (EMC)"], ["J2", "CANH, CANL, GND", "connector to the CAN bus"], ["LED1 + R5", "VDD – N_LED – GND", "power indicator"]] },
    { t: "img", f: "h0_schematic_en.png", w: 15.5, cap: "The module schematic as shown in the app (SCHEMATIC button)." },
    { t: "p", x: "You work in the HW TCA Lab web app, in the browser, with nothing to install. Enter your name, group and the variant code you received (H1–H6) and click Load variant. The board and the schematic are interactive: when you click a pin (pad), the app draws that pin's net, and the Connections panel shows where the signal goes, whether the net reaches a connector and whether it has a test point." },
    { t: "img", f: "h0_conn_en.png", w: 11, cap: "Pin 2 (CAN_L) of J2 selected: the blue line joins all the pins on the CANL net." },
    { t: "ex", n: 3, x: ["In the app, click pin 7 (CANH) of U1. Write down all the components on the CANH net, the connector the net reaches and whether it has a test point. Repeat for pin 8 (RS). What difference do you see between the two nets, from the functional test's point of view?"] },

    { t: "h", x: "Severity (S)" },
    { t: "p", x: "Following the AIAG-VDA FMEA handbook (2019), the risk of each failure mode is described by three ratings from 1 to 10: severity S, occurrence O and detection D. Severity is rated on the effect: how serious the effect is for the customer. In the lab, S follows from the effect class:" },
    { t: "table", w: [1100, 700, 7800], head: ["Class", "S", "Description"], rows: [
      ["E10", "10", "Affects safe operation of the vehicle, occupants or other road users"], ["E9", "9", "Noncompliance with regulations (EMC: emissions or immunity)"],
      ["E8", "8", "Loss of the primary function (no CAN communication or no operation)"], ["E7", "7", "Degradation of the primary function (corrupted or intermittent communication)"],
      ["E6", "6", "Loss of a secondary function (the LED indicator does not work)"], ["E5", "5", "Degradation of a secondary function (wrong LED indication)"],
      ["E2", "2", "Slightly objectionable effect, no functional or EMC effect"], ["E1", "1", "No discernible effect"]] },
    { t: "p", x: "Effects that only reduce EMC filtering get E9 (UNECE R10), even if the function is not affected." },
    { t: "ex", n: 4, x: ["Choose the effect class and severity for:"], list: ["the power LED does not light;", "the RC filter on CANH is missing;", "the module does not communicate on CAN;", "CAN frames sometimes arrive corrupted."] },
    { t: "ex", n: 5, x: ["In the app, choose the effect class for all the failure modes of your variant."] },

    { t: "h", x: "Occurrence (O)" },
    { t: "p", x: "Occurrence is rated on the cause: how likely the defect is, given the prevention. For a mature SMT technology with a stable process the value is usually low." },
    { t: "table", w: [900, 8700], head: ["O", "Criterion (AIAG-VDA summary)"], rows: [
      ["10", "First application of new technology; no experience, standards or best practices"], ["9", "First use in the company of innovations or new materials"], ["8", "Innovations used in a new application; few applicable standards"],
      ["7", "New design on similar technology, new application"], ["6", "Similar to previous designs, changed duty cycle or conditions"], ["5", "Detail changes to a proven design; lessons learned applied but not proven"],
      ["4", "Almost identical design, short field exposure"], ["3", "Detail changes to a known design with comparable test or field experience"], ["2", "Almost identical mature design with long field exposure"], ["1", "Cause eliminated by prevention; not possible by design"]] },
    { t: "ex", n: 6, x: ["In the app, choose O for each mode. Use the same reasoning for all modes and explain it in the report's conclusion."] },

    { t: "h", x: "Detection at AOI, AXI and ICT" },
    { t: "p", x: "Detection D says how reliably we catch the defect before the board ships: 1 means the method always detects it, 10 that we cannot detect it. For AOI, AXI and ICT, the app calculates D from the detection rules below and shows the reason. The ICT “with TP” value applies only if all the nets of the part have a test point." },
    { t: "table", w: [2500, 2300, 1100, 1100, 1300, 1300], head: ["Category", "Failure mode", "AOI", "AXI", "ICT with TP", "ICT without TP"], rows: RULES, small: true },
    { t: "p", x: "Two additional rules: C5 – for the THT connectors, solder defects (pin open, pin short, open) are on the BOTTOM side, which AOI does not inspect at first, so AOI = 10; with AOI enabled on BOTTOM it becomes 1. C7 – marked parts (R1–R5, U1) have their value printed on the package, so AOI partly catches a wrong value (D = 5)." },
    { t: "ex", n: 7, x: ["Without the app, using the table and rules C5 and C7, find D AOI, D AXI and D ICT (without test points) for:"], list: ["R1 short;", "J2, pin 1 (CAN_H), pin open;", "U1, pin 4 (RXD), pin open;", "R2 wrong value."] },
    { t: "ex", n: 8, x: ["In the app, check the AOI, AXI and ICT values for the modes of your variant. Pick two modes and explain, in your own words, the reason the app shows."] },

    { t: "h", x: "Detection at the functional test (FT)" },
    { t: "p", x: "The functional test runs through the connectors at 500 kbit/s, with the limits below. You decide the FT detection yourselves: choose the test that matches the part and the defect type, or NONE (D = 10), then choose D from the detection scale and write why. The functional test can only see a defect if its net reaches a connector pin, directly or through the module's function." },
    { t: "table", w: [700, 1700, 2600, 1800, 2800], head: ["Test", "Name", "What is measured", "Limits", "What it can catch"], small: true, rows: [
      ["FT1", "Supply current", "IDD on VDD (J1), recessive and dominant", "Recessive ≤ 10 mA; dominant ≤ 75 mA", "C3 short, LED1 short / wrong polarity, U1 pin short (VDD–GND), U1 missing, VDD wrong functionality"],
      ["FT2", "Power indicator", "LED1 on, checked with an optical sensor", "On at nominal VDD", "LED1 open / missing / wrong polarity, R5 open / missing"],
      ["FT3", "Recessive bus voltages", "VCANH, VCANL without load, TXD = 1", "2.0 – 3.0 V", "R1/C1, R2/C2 short (line to GND), U1 pin open / short on CANH / CANL"],
      ["FT4", "Dominant differential voltage", "VCANH – VCANL with a 40–60 Ω load, TXD = 0", "1.5 – 3.0 V", "Faulty driver (CANH / CANL wrong functionality), R3 wrong value (standby mode)"],
      ["FT5", "Loopback TXD → RXD", "TXD is toggled; RXD follows the bus state", "RXD = 0 dominant, 1 recessive", "TXD / RXD pin open on U1 and J1, TXD / RXD wrong functionality, wrong standby mode (R3)"],
      ["FT6", "Termination resistance", "CAN_H–CAN_L on J2, with JP1 fitted and removed", "≈ 120 Ω with JP1; ≥ 20 kΩ without", "R4 open / missing / wrong value, JP1 missing / open / short"],
      ["FT7", "CAN transmission through the connectors", "The tester sends frames on TXD (J1); a reference node on J2 acknowledges them (ACK)", "All frames correct, no error frames", "Pin open / short on J1 (VDD, TXD, GND) and J2 (CAN_H, CAN_L), U1 TXD / CANH / CANL / RS, R3 open / missing / wrong value, R1/C1, R2/C2 short"],
      ["FT8", "CAN reception through the connectors", "The reference node sends frames on J2; the tester reads RXD on J1", "All frames read correctly", "Pin open / short on J1 (RXD) and J2 (CAN_H, CAN_L), U1 RXD / CANH / CANL, RXD wrong functionality"]] },
    { t: "p", x: "The analysis is done on the design, so we use the DFMEA detection scale (AIAG-VDA summary):" },
    { t: "table", w: [900, 8700], head: ["D", "Criterion (AIAG-VDA summary)"], rows: [
      ["10", "Test procedure not yet developed; method not defined"], ["9", "Test method not designed specifically for this mode or cause"], ["8", "New, unproven test method"],
      ["7", "Proven method, planned late (pass / fail)"], ["6", "Proven method, planned late (test-to-failure)"], ["5", "Proven method, planned late (degradation testing)"],
      ["4", "Proven method, in time before release (pass / fail)"], ["3", "Proven method, in time before release (test-to-failure)"], ["2", "Proven method, in time before release (degradation testing)"],
      ["1", "Prior testing confirms the failure cannot occur, or the method always detects it"]] },
    { t: "ex", n: 9, x: ["In the app, for each failure mode: click the pin of the part and follow its net in the Connections panel, choose test FT1–FT8 or NONE, choose D FT from the list and write the justification. A value without a justification earns no points."] },

    { t: "h", x: "Combined detection and action priority (AP)" },
    { t: "p", x: "All tests run on every board, so the combined detection is the minimum of the methods' values. S, O and D give the action priority AP (H, M or L) from the AIAG-VDA table. We do not use RPN = S × O × D: the same RPN can hide very different risks (Bowles, 2003)." },
    { t: "box", x: ["D = min(D AOI, D AXI, D ICT, D FT)", "AP = AIAG-VDA table (S band, O band, D band)"] },
    { t: "table", w: [1200, 1200, 1800, 1800, 1800, 1800], head: ["S", "O", "D 7–10", "D 5–6", "D 2–4", "D 1"], rows: AP.map((r) => [r[0], r[1]].concat(r[2].split(" "))), small: true },
    { t: "p", x: "Here is an example from the demo variant H0 (you can load it in the app with code H0): J2, pin 2 (CAN_L), pin open. The joint is on the BOTTOM side, so AOI = 10 (C5). AXI = 3. ICT = 10, because there is no test point on CANL. The matching test is FT7, but with CAN_L open communication may still work over a short distance, so FT7 does not surely catch the defect. With S = 8 (E8), O = 2 and D FT = 5: D = min(10, 3, 10, 5) = 3 and AP = L. With AOI enabled on BOTTOM, AOI = 1 and D becomes 1." },
    { t: "ex", n: 10, x: ["Calculate D and AP for:"], list: ["S = 8, O = 2; D AOI = 10, D AXI = 3, D ICT = 10, D FT = 5;", "S = 9, O = 4; D AOI = 5, D AXI = 5, D ICT = 5, D FT = 10;", "S = 7, O = 4; D AOI = 10, D AXI = 10, D ICT = 5, D FT = 10."] },
    { t: "ex", n: 11, x: ["Calculate RPN and AP for A: S = 9, O = 4, D = 3 and B: S = 3, O = 6, D = 6. What do you notice? Which risk should be treated first?"] },

    { t: "h", x: "Improvements" },
    { t: "p", x: "For the modes with AP H or M we look for improvements: test points (ICT can measure the part), AOI on the BOTTOM side (THT joints) or new FT tests (what is measured, where, which limit). Every improvement has a cost: a test point takes board space and a fixture pin, a new test adds test time. Propose only what reduces a risk." },
    { t: "ex", n: 12, x: ["On which nets must test points be added so that ICT can measure R1? And C2? Check your answer in the app by clicking the pins of the parts."] },
    { t: "ex", n: 13, x: ["In the app, propose improvements for the modes of your variant with AP H or M. For each, write down AP before and after the improvement."] },

    { t: "h", x: "Residual risk and the report" },
    { t: "p", x: "Risk assessment means identification, analysis and evaluation (ISO 31000). What remains after the improvements is the residual risk: it must be documented, with the reason it remains and the decision taken (risk accepted or action proposed)." },
    { t: "ex", n: 14, x: ["For the modes that stay H or M after the improvements, fill in the “Residual risk assessment” column in the app: choose risk accepted or action proposed and write why."] },
    { t: "ex", n: 15, x: ["In the Report tab, write your improvement proposals and conclusion, check the generated sheet and click Send report. If the submission is not confirmed, download the report (.html) and keep it."] },

    { t: "h", x: "Resources" },
    { t: "links", items: [["The HW TCA Lab app", APP], ["K. Hird, K. P. Parker, B. Follis, “Test Coverage: What Does It Mean When a Board Test Passes?”, ITC 2002", "https://doi.org/10.1109/TEST.2002.1041863"],
      ["J. B. Bowles, “An Assessment of RPN Prioritization in a Failure Modes Effects and Criticality Analysis”, RAMS 2003", "https://doi.org/10.1109/RAMS.2003.1182019"],
      ["Microchip, MCP2551 High-Speed CAN Transceiver (datasheet)", "https://www.microchip.com/en-us/product/MCP2551"], ["AIAG & VDA, FMEA Handbook (2019)", "https://www.aiag.org"]] }
  ]
},
IMG
};
