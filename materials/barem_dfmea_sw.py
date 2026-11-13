"""DFMEA SW - grading rubric and model answers (teacher only, RO). Writes barem_dfmea_sw.html next to this file.
Same structure as the HW rubric; AP is computed with the AIAG-VDA table, and the expected AP is asserted."""
import html, os
E = html.escape
AP = {"9-10": {"8-10": "HHHH", "6-7": "HHHH", "4-5": "HHHM", "2-3": "HMLL", "1": "LLLL"},
      "7-8": {"8-10": "HHHH", "6-7": "HHHM", "4-5": "HMMM", "2-3": "MMLL", "1": "LLLL"},
      "4-6": {"8-10": "HHMM", "6-7": "MMML", "4-5": "MLLL", "2-3": "LLLL", "1": "LLLL"},
      "2-3": {"8-10": "MMLL", "6-7": "LLLL", "4-5": "LLLL", "2-3": "LLLL", "1": "LLLL"},
      "1": {"8-10": "LLLL", "6-7": "LLLL", "4-5": "LLLL", "2-3": "LLLL", "1": "LLLL"}}
def ap(s, o, d):
    sb = "9-10" if s >= 9 else "7-8" if s >= 7 else "4-6" if s >= 4 else "2-3" if s >= 2 else "1"
    ob = "8-10" if o >= 8 else "6-7" if o >= 6 else "4-5" if o >= 4 else "2-3" if o >= 2 else "1"
    di = 0 if d >= 7 else 1 if d >= 5 else 2 if d >= 2 else 3
    return AP[sb][ob][di]

# effects at N1 (sensor level, as in the SW demo) and their S
FE = {"lost": ("Un obiect real nu e raportat (detecție ratată, frânare lipsă)", 8, "pierderea funcției principale a senzorului"),
      "implaus": ("Date neplauzibile ajung la funcția ADAS", 8, "pierderea funcției principale: ADAS primește date în care nu se poate încrede"),
      "wrongval": ("Valori greșite raportate pentru obiecte (distanță, viteză, poziție)", 7, "degradarea funcției principale"),
      "dropped": ("Cadre valide sunt aruncate, iar datele radarului se pierd", 7, "degradarea funcției principale (pierderi intermitente)"),
      "busoff": ("Nodul continuă să transmită deși controllerul CAN e în bus-off", 8, "perturbă celelalte noduri de pe bus (ca la HW: S 8, se acceptă 9–10 cu argument)")}
N1P = "Folosește doar date valide și plauzibile pentru funcțiile ADAS"
N1B = "Nu perturbă comunicația celorlalte noduri de pe bus-ul CAN"
CATF = {"Cerințele software (SWR)": "Asigură definirea completă și corectă a cerințelor funcției",
        "Constante și parametri (#define)": "Asigură valori corecte ale limitelor (#define), conform specificației",
        "Constante și parametri (#define) ": "Asigură unitățile de măsură corecte ale constantelor",
        "Logica de decizie (condiții, operatori)": "Asigură operatorii de comparație corecți la limite",
        "Logica de decizie (condiții, operatori) ": "Asigură combinarea corectă a condițiilor (&&, ||)",
        "Tipuri de date și domenii de valori": "Asigură tipuri de date suficiente pentru domeniul valorilor (fără overflow)",
        "Tipuri de date și domenii de valori ": "Asigură conversii corecte între tipuri (signed / unsigned)",
        "Interfața (apeluri, valori returnate)": "Asigură apelarea corectă a funcțiilor (parametri, ordine)"}
# variant: (title, N1 fn, N2 fn, [(mode, [effects])], risk rows)
# risk row: (mode idx, category key, culprit, cause, PC, O, DC, D, expected AP, action or None, O', D', expected AP')
V = {}
V["F0"] = ("sensor_value_plausible() · unghiul azimut (demo)", N1P, "Respinge valorile din afara domeniului [MIN, MAX]",
  [("Respinge o valoare validă", ["lost"]), ("Decizie greșită la valorile limită", ["wrongval"])],
  [(0, "Constante și parametri (#define) ", "–", "Unitate de măsură greșită a constantei (SENSOR_MAX = 60, în grade, în loc de 600, în zecimi de grad)",
    "Review de cod față de specificația senzorului", 4, "Testare pe cerințe (requirements-based); teste la limite (boundary values), în testul unitar, înainte de lansare", 3, "M",
    "[P] Constante generate automat din specificația senzorului", 2, 3, "L"),
   (1, "Logica de decizie (condiții, operatori)", "–", "Operator de comparație greșit la limită (< în loc de <=)",
    "Reguli de codare MISRA C; review de cod", 4, "Teste la limite (boundary values): 600 / 601, −600 / −601", 3, "M",
    "[P] Șabloane de cod reutilizate, dovedite, pentru verificările de domeniu", 3, 3, "L")])
V["F1"] = ("can_error_state() (TEC / REC → stare CAN)", N1B, "Raportează BUS_OFF când TEC > 255",
  [("Nu raportează BUS_OFF", ["busoff"]), ("Raportează BUS_OFF prea devreme", ["dropped"])],
  [(0, "Logica de decizie (condiții, operatori)", "–", "Verificările în ordine inversă (error-passive înainte de bus-off)",
    "Review al arhitecturii / designului SW", 4, "Testare pe cerințe (requirements-based), test unitar", 4, "M",
    "[P] Programare defensivă: ordinea verificărilor luată direct din cerințe (SWR-F3-01 înaintea SWR-F3-02), verificată la review", 3, 4, "L"),
   (0, "Cerințele software (SWR)", "SWR-F3-02", "Cerință ambiguă sau incompletă (lipsește cazul limită): nu spune explicit că bus-off are prioritate",
    "Review al cerințelor", 5, "Test de integrare, târziu", 7, "H",
    "[P] Review al cerințelor cu checklist pentru ordinea și limitele condițiilor; cerința reformulată; [D] teste la limite din cerință (TEC 255 / 256), în testul unitar", 3, 3, "L"),
   (1, "Logica de decizie (condiții, operatori)", "–", "TEC comparat cu >= în loc de > la limita bus-off",
    "Reguli de codare MISRA C", 5, "Teste la limite (boundary values), în testul unitar", 3, "M",
    "[P] Șabloane de cod reutilizate, dovedite, pentru comparațiile cu praguri", 3, 3, "L")])
V["F2"] = ("sensor_value_plausible() · distanța longitudinală", N1P, "Respinge salturile mai mari decât pasul maxim între cicluri",
  [("Acceptă un salt mai mare decât pasul maxim", ["implaus"]), ("Respinge prima detecție a unui obiect", ["lost"])],
  [(0, "Logica de decizie (condiții, operatori)", "–", "Lipsește valoarea absolută a diferenței (salturile negative trec)",
    "Review de cod față de specificația senzorului", 4, "Testare pe cerințe (requirements-based), test unitar", 4, "M",
    "[P] Funcție comună abs_diff(), verificată și reutilizată", 2, 4, "L"),
   (0, "Tipuri de date și domenii de valori", "–", "Diferența calculată pe int16_t (overflow)",
    "Reguli de codare MISRA C", 3, "Analiză statică, la fiecare build", 4, "L", None, 0, 0, ""),
   (1, "Logica de decizie (condiții, operatori) ", "–", "first_sample combinat greșit cu verificarea pasului (&& în loc de ||)",
    "Review al arhitecturii / designului SW", 5, "Test de integrare, târziu", 7, "H",
    "[P] Decizia scrisă direct din SWR-F2-03 și SWR-F2-04, cu tabel de adevăr la review; [D] test unitar cu acoperire MC/DC (perechea pentru first_sample)", 3, 3, "L")])
V["F3"] = ("can_frame_is_valid() (validarea cadrului CAN)", N1P, "Respinge identificatorii în afara domeniului (standard / extins)",
  [("Respinge un cadru valid (identificator extins în domeniu)", ["dropped"]), ("Acceptă un identificator în afara domeniului", ["implaus"])],
  [(0, "Logica de decizie (condiții, operatori)", "–", "max_id nu se schimbă pentru cadrele extinse",
    "Șabloane de cod reutilizate, dovedite", 3, "Test unitar cu acoperire MC/DC", 3, "L", None, 0, 0, ""),
   (0, "Constante și parametri (#define)", "–", "CAN_EXT_ID_MAX definit pe 28 de biți în loc de 29",
    "Review de cod față de specificația senzorului", 4, "Test de integrare, târziu", 7, "H",
    "[D] Teste la limite pe cadrul extins (0x1FFFFFFF / 0x20000000) în testul unitar; [P] constante generate automat din ISO 11898-1", 2, 3, "L"),
   (1, "Constante și parametri (#define)", "–", "Valoare greșită a limitei în #define (CAN_STD_ID_MAX = 0xFFF)",
    "Trasabilitate cerințe → cod", 4, "Teste la limite (boundary values), în testul unitar", 3, "M",
    "[P] Constante generate automat din specificație", 2, 3, "L")])
V["F4"] = ("can_rx_handler() (integrarea)", N1P, "Acceptă doar cadrele valide și plauzibile",
  [("Acceptă un cadru invalid", ["implaus"]), ("Omite una dintre verificări (validitate sau plauzibilitate)", ["implaus"])],
  [(0, "Interfața (apeluri, valori returnate)", "–", "Parametri transmiși în ordine greșită (id și dlc inversate la can_frame_is_valid())",
    "Reguli de codare MISRA C", 4, "Test de integrare, înainte de lansare", 4, "M",
    "[P] Interfață cu un tip dedicat (struct can_frame) în loc de parametri de același tip", 2, 4, "L"),
   (0, "Interfața (apeluri, valori returnate)", "–", "Valoarea returnată de funcția apelată nu e verificată",
    "Review al arhitecturii / designului SW", 3, "Analiză statică, la fiecare build", 4, "L", None, 0, 0, ""),
   (1, "Interfața (apeluri, valori returnate)", "–", "Rezultatul sensor_value_plausible() ignorat",
    "Programare defensivă (ghid intern)", 4, "Test HIL (hardware-in-the-loop), la validare, târziu", 7, "H",
    "[D] Test de integrare cu function / call coverage 100 %; [P] review al designului cu lista apelurilor obligatorii", 3, 4, "L")])
V["F5"] = ("sensor_value_plausible() · viteza relativă", N1P, "Respinge valorile din afara domeniului [MIN, MAX]",
  [("Respinge o valoare validă", ["lost"]), ("Acceptă o valoare în afara domeniului", ["wrongval"])],
  [(0, "Tipuri de date și domenii de valori ", "–", "Conversie signed / unsigned greșită (SENSOR_MIN = −1111 comparat ca unsigned)",
    "Reguli de codare MISRA C", 4, "Teste la limite (boundary values), în testul unitar", 3, "M",
    "[P] Reguli MISRA C verificate automat la build (regulile de conversie)", 2, 3, "L"),
   (0, "Constante și parametri (#define)", "–", "SENSOR_MIN / SENSOR_MAX diferite de specificația senzorului",
    "Review de cod față de specificația senzorului", 4, "Test de integrare, târziu", 7, "H",
    "[P] Constante generate automat din specificație; [D] teste la limite (−1111 / −1112, 556 / 557) în testul unitar", 2, 3, "L"),
   (1, "Logica de decizie (condiții, operatori)", "–", "Operator de comparație greșit la limită (< în loc de <=)",
    "Șabloane de cod reutilizate, dovedite", 3, "Teste la limite (boundary values), în testul unitar", 3, "L", None, 0, 0, "")])
V["F6"] = ("sensor_value_plausible() · poziția laterală", N1P, "Respinge salturile mai mari decât pasul maxim între cicluri",
  [("Respinge o valoare validă", ["lost"]), ("Acceptă un salt mai mare decât pasul maxim", ["wrongval"])],
  [(0, "Cerințele software (SWR)", "SWR-F2-04", "Cerință greșită față de cerința de sistem (pasul de 0,7 m pe ciclu prea mic pentru o schimbare de bandă)",
    "Review al cerințelor", 5, "Test HIL (hardware-in-the-loop), la validare, târziu", 7, "H",
    "[P] Trasabilitate cerințe → cerințe de sistem, cu calculul pentru manevra de schimbare a benzii; [D] scenariu HIL de schimbare a benzii, devreme", 3, 4, "L"),
   (1, "Constante și parametri (#define)", "–", "Valoare greșită a limitei în #define (SENSOR_MAX_STEP = 70)",
    "Constante generate automat din specificația senzorului", 2, "Teste la limite (boundary values), în testul unitar", 3, "L", None, 0, 0, ""),
   (1, "Logica de decizie (condiții, operatori)", "–", "Lipsește valoarea absolută a diferenței (salturile negative trec)",
    "Review de cod față de specificația senzorului", 4, "Testare pe cerințe (requirements-based), test unitar", 4, "M",
    "[P] Funcție comună abs_diff(), verificată și reutilizată", 2, 4, "L")])

def tbl(head, rows):
    return "<table border='1' cellpadding='4' style='border-collapse:collapse'><tr>" + "".join("<th>" + E(h) + "</th>" for h in head) + "</tr>" + \
        "".join("<tr>" + "".join("<td>" + c + "</td>" for c in r) + "</tr>" for r in rows) + "</table>"

def smax(modes, i): return max(FE[e][1] for e in modes[i][1])
# check every expected AP against the table
for code, (t, n1, n2, modes, risk) in V.items():
    for r in risk:
        s = smax(modes, r[0])
        assert ap(s, r[5], r[7]) == r[8], (code, r[3], ap(s, r[5], r[7]))
        if r[9]: assert ap(s, r[10], r[11]) == r[12], (code, r[3], "rev", ap(s, r[10], r[11]))

h = ["<html><head><meta charset='utf-8'></head><body><h1>DFMEA SW – barem și răspunsuri model</h1>"]
h.append("<p>Document doar pentru profesor. Completează documentul „DFMEA HW – barem și răspunsuri model v2”: acolo e partea HW (5 puncte), aici partea SW (5 puncte), cu demo-ul F0 câmp cu câmp și câte o analiză model pentru funcția SW a fiecărei variante (F1–F6). Studenții nu sunt notați la laborator; baremul servește la analiza rapoartelor pentru studiul de caz și la corectarea cu al doilea evaluator. Modelele respectă simplificarea din laborator: o funcție pe element, cel mult 3 moduri, 3 efecte și 2 cauze pe mod. Nu există un singur răspuns corect: modelele arată nivelul așteptat. AP a fost calculat cu tabelul AIAG-VDA și verificat automat.</p>")
h.append("<h2>1. Ce se punctează (partea SW, 5 puncte; HW + SW = 10)</h2>")
h.append(tbl(["Criteriu", "Ce se verifică", "Puncte (din 5)"], [
    ["Structură și funcții", "O funcție pe element: N1 la nivelul radarului, N2 din cerințele SWR ale funcției, la N3 doar categoriile folosite; funcții cu condiție verificabilă", "1,0"],
    ["Rețeaua de defectare", "Moduri ca negare a funcției N2 (ce face funcția greșit, nu linia de cod); efectele la nivelul radarului; cauze în categoria potrivită (cerințe, constante, logică, tipuri, interfață); la cauzele din cerințe, cerința vinovată aleasă corect", "1,25"],
    ["S, O, D", "S din D1 pe efect (la nivel de senzor, cel mult 8 pentru efectele funcționale, ca în demo; 9–10 doar cu argument de nivel vehicul); O din D2 justificat prin prevenția SW; D din D3 justificat prin metodă și moment (testul unitar pe cerințe și la limite, înainte de lansare: D 3–4; test de integrare sau HIL târziu: D 7)", "1,25"],
    ["Optimizare", "Acțiuni la H și M, de tip P sau D, cu responsabil și termen; O' / D' realiste; la FAIL, acțiune corectivă P; acțiunea suplimentară cu tipul potrivit; risc rezidual justificat dacă rămâne H / M", "1,0"],
    ["Raport", "Verificările fără erori; concluzia leagă DFMEA SW de TCA SW (detecția = testele pe cerințe și la limite, acoperirea lor)", "0,5"]]))
h.append("<p>Limitele (o funcție pe element, 3 moduri, 3 efecte, 2 cauze pe mod) sunt avertismente în aplicație, nu se depunctează.</p>")
h.append("<h2>2. Greșeli frecvente</h2>")
h.append(tbl(["Greșeala", "Cum se recunoaște"], [
    ["Linia de cod ca mod", "„Operatorul >= în loc de >” scris ca mod la N2; modul este ce face funcția (raportează BUS_OFF prea devreme), operatorul e cauza"],
    ["Cauză în categoria greșită", "O constantă în altă unitate pusă la „Logica de decizie”; o cerință ambiguă pusă la „Constante”"],
    ["Cerința vinovată lipsă", "Cauză din categoria „Cerințele software” fără cerința bifată"],
    ["Defecte aleatoare în DFMEA SW", "„Bit flip în RAM”, „memorie coruptă”: sunt defecte hardware aleatoare (FMEDA, ISO 26262-5), nu cauze de design software"],
    ["O mic fără prevenție", "O 1–2 cu prevenția „niciuna” sau doar „MISRA C” pentru o greșeală pe care MISRA nu o prinde (unitatea unei constante)"],
    ["D mic pentru review sau teste târzii", "Code review sau HIL de validare cu D 1–2; review-ul nu e test, iar un test făcut după lansare are D 5–7"],
    ["D fără legătură cu TCA SW", "„Testare pe cerințe” cu D 2–3, deși testele nu acoperă limitele; concluzia nu menționează valorile la limită"],
    ["FAIL tratat doar prin detecție", "Testul la limită a ieșit FAIL, iar studentul scade doar D; defectul e confirmat, e nevoie de corecția codului sau a cerinței (P)"]]))
h.append("<h2>3. Efectele de la N1 și severitatea lor</h2>")
h.append(tbl(["Efect (N1)", "S", "Motiv (tabelul D1)"], [[E(v[0]), str(v[1]), E(v[2])] for v in FE.values()]))
h.append("<p>Convenția din laborator, ca la TCA: senzorul e analizat separat de vehicul, deci efectele funcționale au cel mult S 8. Dacă studentul argumentează efectul la nivel de vehicul (de exemplu „un obiect inexistent e raportat, frânare falsă”), se acceptă S 9–10.</p>")

def variant(code, demo, num):
    t, n1, n2, modes, risk = V[code]
    out = ["<h2>%s %s · %s</h2>" % (num, code, E(t))]
    out.append("<h3>Pașii 2–3: structură și funcții</h3>")
    cats = []
    for r in risk:
        if r[1] not in cats: cats.append(r[1])
    rows = [["N1 · Radar frontal (ASIL B)", E(n1)], ["N2 · " + E(t), E(n2)]] + [["N3 · " + E(c.strip()), E(CATF[c])] for c in cats]
    out.append(tbl(["Element", "Funcție"], rows))
    out.append("<h3>Pasul 4: rețeaua de defectare</h3>")
    nr = []
    for i, (m, effs) in enumerate(modes):
        causes = [r for r in risk if r[0] == i]
        nr.append(["<br>".join(E(FE[e][0]) + " (S " + str(FE[e][1]) + ")" for e in effs), E(m) + " (S max " + str(smax(modes, i)) + ")",
                   "<br>".join("<i>" + E(r[1].strip()) + "</i>: " + E(r[3]) + ("" if r[2] == "–" else " — cerința vinovată: <b>" + E(r[2]) + "</b>") for r in causes) or "–"])
    out.append(tbl(["Efecte (N1)", "Mod (N2)", "Cauze (N3)"], nr))
    out.append("<h3>Pașii 5–6: risc și optimizare</h3>")
    rr = []
    for r in risk:
        s = smax(modes, r[0])
        rev = (E(r[9]) + "<br>O' " + str(r[10]) + " · D' " + str(r[11]) + " → AP " + r[12]) if r[9] else "–"
        rr.append([E(modes[r[0]][0]) + " ← " + E(r[3]), str(s), E(r[4]), str(r[5]), E(r[6]), str(r[7]), r[8], rev])
    out.append(tbl(["Mod ← cauză", "S", "Prevenție (PC)", "O", "Detecție (DC)", "D", "AP", "Acțiuni (revizie) → AP"], rr))
    return "".join(out)

h.append("<h2>4. Demo F0 (SW) în aplicație: ce se scrie</h2>")
h.append("<p>Pe F0 se completează în clasă primul lanț (cel din „Cum se face”); al doilea e opțional, dacă rămâne timp. Acțiunile au tip, responsabil (ex.: dezvoltator SW, inginer de test SW) și termen.</p>")
h.append(variant("F0", True, "4.1"))
h.append("<p><b>De discutat la demo:</b></p><ul>"
  "<li>Legătura cu TCA SW: cu SENSOR_MAX = 60, testul la limită SWR-F2-02 (600 acceptat, 601 respins) pică imediat. De aceea D este 3: detecția există și se face la timp, în testul unitar.</li>"
  "<li>Scenariu FAIL: dacă testul la limită iese FAIL, defectul e confirmat. Acțiunea corectivă e P (corectarea constantei, apoi constante generate din specificație), iar O se reevaluează. Un test în plus nu coboară riscul.</li>"
  "<li>Diferența față de HW: la software nu există variație de la o piesă la alta; dacă greșeala e în cod, e în toate radarele. De aceea prevenția (O) contează la fel de mult ca detecția.</li></ul>")
for k, c in enumerate(["F1", "F2", "F3", "F4", "F5", "F6"]):
    h.append(variant(c, False, "5.%d" % (k + 1)))
h.append("<h2>6. Ce se acceptă ca alternativă</h2><ul>"
  "<li>Alt mod sau altă cauză decât cele din model, dacă lanțul efect – mod – cauză e coerent și cauza e de design software.</li>"
  "<li>O cu ±1 față de model, dacă prevenția aleasă justifică valoarea.</li>"
  "<li>D 4 în loc de 3 (aceeași bandă AP) pentru testele unitare pe cerințe; D 5–6 pentru teste făcute târziu, dacă studentul scrie momentul.</li>"
  "<li>S 9–10 la efectele care afectează frânarea, dacă studentul argumentează nivelul vehiculului.</li></ul>")
h.append("</body></html>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "barem_dfmea_sw.html"), "w", encoding="utf-8").write("".join(h))
print("ok", sum(len(v[4]) for v in V.values()), "rows")
