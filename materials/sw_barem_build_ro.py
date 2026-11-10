# Builds the SW TCA grading rubric and answer key (RO, instructor only) as HTML for import into Google Docs.
import html
E = html.escape
out = []
def h(x): out.append('<h2>%s</h2>' % E(x))
def h3(x): out.append('<h3>%s</h3>' % E(x))
def p(x, raw=False): out.append('<p>%s</p>' % (x if raw else E(x)))
def ul(items): out.append('<ul>%s</ul>' % "".join("<li>%s</li>" % E(i) for i in items))
def table(head, rows, center_cols=(), size=10):
    th = "".join("<th>%s</th>" % E(x) for x in head)
    trs = "".join("<tr>%s</tr>" % "".join(("<td align=center>%s</td>" if i in center_cols else "<td>%s</td>") % (("<b>%s</b>" % E(str(c))) if i == 0 else E(str(c))) for i, c in enumerate(r)) for r in rows)
    out.append('<table class="s%d"><tr>%s</tr>%s</table><p></p>' % (size, th, trs))

out.append("""<html><head><meta charset="utf-8"><style>
body,p,li,td,th{font-family:'Times New Roman';font-size:12pt}
p{text-align:justify;margin:0 0 6pt 0}
h1{font-family:Aptos,Arial;font-size:20pt;color:#0F4761;font-weight:normal;text-align:center}
h2{font-family:Aptos,Arial;font-size:14pt;color:#0F4761;font-weight:normal;margin:16pt 0 6pt 0}
h3{font-family:Aptos,Arial;font-size:12pt;color:#156082;font-weight:normal;margin:12pt 0 4pt 0}
table{border-collapse:collapse;width:100%}
th{background:#000000;color:#FFFFFF;font-size:10pt;border:1px solid #000;padding:2pt 4pt}
td{font-size:10pt;border:1px solid #000;padding:2pt 4pt}
table.s9 td,table.s9 th{font-size:9pt}
</style></head><body>""")
out.append('<h1>SW TCA – barem și răspunsuri</h1>')
p("Document doar pentru profesor. Conține baremul pentru tema notată (varianta proprie, V1–V6), răspunsurile la exercițiile 1–7 din îndrumar, soluțiile de referință pentru fiecare variantă și greșelile frecvente. Soluțiile de referință au fost rulate în aplicație pe fiecare variantă.")

h("1. Baremul temei (10 puncte)")
table(["Criteriu", "Ce se verifică în raport", "Puncte"], [
    ["ISO 26262", "Răspunsul pentru ASIL B: statement ++, branch ++, MC/DC +", "0,5"],
    ["F1: teste din cerințe", "Câte un test pentru fiecare cerință SWR-F1-01…04, cu rezultat așteptat corect și cerința aleasă corect", "1,0"],
    ["F1: acoperire", "100% statement și 100% branch (inclusiv extended = false)", "0,5"],
    ["F1: observații", "Explică de ce 100% statement nu era suficient (if fără else, ramura false a lui extended)", "0,5"],
    ["F2: MC/DC", "100% MC/DC; perechea notată pentru fiecare condiție A–D; explicația perechii pentru C (masking)", "1,5"],
    ["F2: valori la limită", "Testele la limita variantei: minim, maxim, pasul exact și pasul + 1 (vezi secțiunea 3)", "1,0"],
    ["F3: valori la limită", "TEC 127/128, 255/256 și REC 127/128, cu rezultatele așteptate din cerințe", "1,0"],
    ["F3: greșeala găsită", "Testul care pică pentru greșeala variantei (vezi secțiunea 3)", "0,5"],
    ["F3: raport de defect", "Cerința încălcată, linia (38 sau 41), corecția în C și descrierea (obținut față de așteptat)", "1,0"],
    ["Integrare: acoperire", "100% funcții apelate și 100% apeluri executate (C1, C2, C3)", "0,5"],
    ["Integrare: justificare", "Liniile 67–68 (default): de ce nu pot fi atinse, de ce e acceptabil (cod defensiv, MISRA C), cum s-ar verifica (fault injection)", "0,5"],
    ["Trasabilitate și raport", "Fiecare test are cerința completată; raportul trimis complet; observațiile numesc tehnicile folosite (clase de echivalență, valori la limită)", "1,5"]], center_cols=(2,))
p("Total: 10 puncte. Raportul se generează din aplicație (tab-ul Raport) și conține toate elementele de mai sus.")

h("2. Greșeli frecvente (se depunctează)")
table(["Greșeala", "Cum se recunoaște", "Depunctare orientativă"], [
    ["Rezultatul așteptat copiat din rezultatul obținut", "Toate testele trec, inclusiv testul la limită care ar trebui să pice; rezultatul așteptat contrazice cerința", "tot punctajul pentru greșeala găsită și raportul de defect"],
    ["Teste fără cerință", "Coloana „Cerință” goală sau aleasă greșit", "0,1 pe test, maxim 0,5"],
    ["Teste doar pentru acoperire", "100% acoperire, dar fără valori la limită (de exemplu doar 300, 200, 0 la F3)", "punctajul pentru valorile la limită"],
    ["Corecția greșită", "Corecția schimbă alt operator sau constanta (de exemplu 256 în loc de >)", "0,5 din raportul de defect"],
    ["Justificare generică", "„Nu se poate testa” fără motiv", "0,25"],
    ["Linii de default șterse sau ignorate", "Propune eliminarea codului defensiv", "0,25"]])

h("3. Soluții de referință pe variante")
h3("3.1 Ce diferă între variante")
table(["Variantă", "Semnal F2", "SENSOR_MIN", "SENSOR_MAX", "SENSOR_MAX_STEP", "Greșeala din F3", "Testul care pică", "Corecția"], [
    ["V0 (demo)", "distanță longitudinală", "2", "2500", "80", "– (greșeala e în F1: id >= max_id)", "id = 0x7FF std. și 0x1FFFFFFF ext.: obținut false, așteptat true", "linia 14: if (id > max_id)"],
    ["V1", "distanță longitudinală", "2", "2500", "80", "linia 38: tec >= CAN_BUSOFF_LIMIT", "tec = 255, rec = 0: obținut BUS_OFF, așteptat ERROR_PASSIVE (SWR-F3-02)", "if (tec > CAN_BUSOFF_LIMIT)"],
    ["V2", "distanță longitudinală", "2", "2500", "80", "linia 41: tec >= CAN_PASSIVE_LIMIT", "tec = 127, rec = 0: obținut ERROR_PASSIVE, așteptat ERROR_ACTIVE (SWR-F3-03)", "(tec > CAN_PASSIVE_LIMIT)"],
    ["V3", "viteză relativă", "−1111", "556", "14", "linia 41: rec >= CAN_PASSIVE_LIMIT", "tec = 0, rec = 127: obținut ERROR_PASSIVE, așteptat ERROR_ACTIVE (SWR-F3-03)", "(rec > CAN_PASSIVE_LIMIT)"],
    ["V4", "viteză relativă", "−1111", "556", "14", "linia 38: tec >= CAN_BUSOFF_LIMIT", "tec = 255, rec = 0: obținut BUS_OFF, așteptat ERROR_PASSIVE (SWR-F3-02)", "if (tec > CAN_BUSOFF_LIMIT)"],
    ["V5", "distanță laterală", "−700", "700", "7", "linia 41: tec >= CAN_PASSIVE_LIMIT", "tec = 127, rec = 0: obținut ERROR_PASSIVE, așteptat ERROR_ACTIVE (SWR-F3-03)", "(tec > CAN_PASSIVE_LIMIT)"],
    ["V6", "distanță laterală", "−700", "700", "7", "linia 41: rec >= CAN_PASSIVE_LIMIT", "tec = 0, rec = 127: obținut ERROR_PASSIVE, așteptat ERROR_ACTIVE (SWR-F3-03)", "(rec > CAN_PASSIVE_LIMIT)"]], size=9)
p("F1 și integrarea sunt identice la toate variantele V1–V6 și nu au greșeală: soluția din îndrumar (secțiunile 9.2 pașii 1–2 și 9.5) este soluția de referință.")
h3("3.2 F3: setul de referință (același pentru toate variantele)")
table(["Test", "tec", "rec", "Așteptat", "Cerință", "Pică la"], [
    ["T1", "256", "0", "BUS_OFF", "SWR-F3-01", "–"], ["T2", "255", "0", "ERROR_PASSIVE", "SWR-F3-02", "V1, V4"], ["T3", "128", "0", "ERROR_PASSIVE", "SWR-F3-02", "–"],
    ["T4", "127", "0", "ERROR_ACTIVE", "SWR-F3-03", "V2, V5"], ["T5", "0", "128", "ERROR_PASSIVE", "SWR-F3-02", "–"], ["T6", "0", "127", "ERROR_ACTIVE", "SWR-F3-03", "V3, V6"]], center_cols=(1, 2))
p("Cu acest set, statement, branch și MC/DC sunt 100% la toate variantele, iar exact un test pică. Un student care a ajuns la 100% acoperire fără testul care pică nu a testat limita greșită.")
h3("3.3 F2: seturi de referință (5 teste MC/DC + 4 teste la limită)")
for name, rows in [("Distanță longitudinală (V0, V1, V2): min 2, max 2500, pas 80", [
        ["T1", "1000", "1050", "false", "true", "SWR-F2-04", "bază"], ["T2", "1000", "1100", "false", "false", "SWR-F2-04", "D (T1–T2)"], ["T3", "1000", "2000", "true", "true", "SWR-F2-03", "C (T2–T3)"],
        ["T4", "1", "0", "true", "false", "SWR-F2-01", "A (T1–T4)"], ["T5", "2501", "2500", "true", "false", "SWR-F2-02", "B (T1–T5)"], ["T6", "2", "2", "true", "true", "SWR-F2-01", "limită min"],
        ["T7", "2500", "2500", "false", "true", "SWR-F2-02", "limită max"], ["T8", "1080", "1000", "false", "true", "SWR-F2-04", "pas = 80"], ["T9", "1081", "1000", "false", "false", "SWR-F2-04", "pas = 81"]]),
    ("Viteză relativă (V3, V4): min −1111, max 556, pas 14", [
        ["T1", "0", "10", "false", "true", "SWR-F2-04", "bază"], ["T2", "0", "20", "false", "false", "SWR-F2-04", "D (T1–T2)"], ["T3", "0", "500", "true", "true", "SWR-F2-03", "C (T2–T3)"],
        ["T4", "−1112", "0", "true", "false", "SWR-F2-01", "A (T1–T4)"], ["T5", "557", "556", "true", "false", "SWR-F2-02", "B (T1–T5)"], ["T6", "−1111", "−1111", "true", "true", "SWR-F2-01", "limită min"],
        ["T7", "556", "556", "false", "true", "SWR-F2-02", "limită max"], ["T8", "14", "0", "false", "true", "SWR-F2-04", "pas = 14"], ["T9", "15", "0", "false", "false", "SWR-F2-04", "pas = 15"]]),
    ("Distanță laterală (V5, V6): min −700, max 700, pas 7", [
        ["T1", "0", "5", "false", "true", "SWR-F2-04", "bază"], ["T2", "0", "10", "false", "false", "SWR-F2-04", "D (T1–T2)"], ["T3", "0", "600", "true", "true", "SWR-F2-03", "C (T2–T3)"],
        ["T4", "−701", "0", "true", "false", "SWR-F2-01", "A (T1–T4)"], ["T5", "701", "700", "true", "false", "SWR-F2-02", "B (T1–T5)"], ["T6", "−700", "−700", "true", "true", "SWR-F2-01", "limită min"],
        ["T7", "700", "700", "false", "true", "SWR-F2-02", "limită max"], ["T8", "7", "0", "false", "true", "SWR-F2-04", "pas = 7"], ["T9", "8", "0", "false", "false", "SWR-F2-04", "pas = 8"]])]:
    h3(name)
    table(["Test", "value", "previous", "first_sample", "Așteptat", "Cerință", "Rol"], rows, center_cols=(1, 2, 3, 4), size=9)
p("Toate seturile au fost rulate în aplicație: 100% statement, branch și MC/DC, toate testele trec (F2 nu are greșeală la nicio variantă). Alte seturi sunt corecte dacă fiecare condiție are o pereche validă și limitele variantei sunt testate.")
h3("3.4 Justificarea de referință pentru integrare")
p("Liniile 67–68 (default) nu pot fi atinse prin teste: can_error_state() returnează numai ERROR_ACTIVE, ERROR_PASSIVE și BUS_OFF, toate tratate explicit. Codul este defensiv (MISRA C:2012 regula 16.4: orice switch are default) și tratează o valoare coruptă a lui state returnând RX_FAULT. Se poate verifica prin injectare de defecte (stub sau debugger care forțează state la o valoare invalidă). Acceptat ca neacoperit, cu justificare (ISO 26262-6, 9.4.4).")

h("4. Răspunsuri la exercițiile 1–7 (pe hârtie)")
h3("Exercițiul 1")
table(["Situație", "Tip", "Test de producție?"], [
    ["a) condensator cu valoare greșită pe 0,5% din plăci", "aleator (fabricație)", "da: ICT măsoară valoarea, dacă există acces; AOI nu, condensatorul nu are marcaj"],
    ["b) > în loc de >= în firmware", "sistematic (cod)", "nu: e în toate bucățile; se prinde la dezvoltare, cu teste la limită"],
    ["c) lipitură fisurată după 5 ani", "aleator (uzură)", "nu: apare în funcționare; se previne prin proiectare și teste de durabilitate"],
    ["d) cerință care nu spune ce se întâmplă la DLC = 0", "sistematic (cerință)", "nu: se găsește la analiza cerințelor sau la scrierea testelor"],
    ["e) tranzistor defect la temperatură mare", "aleator (hardware)", "în general nu; se tratează prin derating, diagnostic, mecanisme de siguranță"],
    ["f) funcție care nu tratează 65535", "sistematic (cod)", "nu: se găsește cu error guessing sau valori la limită ale tipului"]], size=9)
h3("Exercițiul 2")
p("Statement: 1 test ajunge, temp = 95 (rezultat 2): ambele if-uri sunt adevărate, deci se execută toate instrucțiunile. Branch: 2 teste, temp = 95 (rezultat 2) și temp = 20 (rezultat 0); fiecare decizie e o dată adevărată și o dată falsă. Observație pentru discuție: cazul 61…90 (rezultat 1) nu e testat deloc, deși acoperirea e 100%. Cerința l-ar fi impus, plus limitele 60/61 și 90/91.")
h3("Exercițiul 3")
p("(a = 1, b = 0) și (a = 0, b = 1): fiecare condiție e o dată adevărată și o dată falsă, deci condition coverage 100%, dar decizia e adevărată în ambele teste, deci ramura false nu se execută (branch 50%).")
h3("Exercițiul 4")
table(["Decizie", "Teste (N + 1)", "Perechi"], [
    ["a) (v >= 2) && (v <= 2500)", "TT → T (v = 100); FT → F (v = 1); TF → F (v = 3000)", "A: TT–FT; B: TT–TF"],
    ["b) a || b || c", "FFF → F; TFF → T; FTF → T; FFT → T", "a: FFF–TFF; b: FFF–FTF; c: FFF–FFT"],
    ["c) a && (b || c)", "TTF → T; FTF → F; TFF → F; TFT → T", "a: TTF–FTF; b: TTF–TFF; c: TFF–TFT"]], size=9)
h3("Exercițiul 5")
p("Clase: temperatură < −40 °C (defect), −40…125 °C (normal), > 125 °C (defect). Valori la limită: −41, −40, 125, 126. Minimul este 4 teste: valorile la limită acoperă deja cele trei clase. Error guessing: valorile extreme ale tipului citit și o citire constantă.")
h3("Exercițiul 6")
p("Linia 42 nu a fost executată: niciun test nu a dus în ERROR_PASSIVE. „branch 1 taken 0%” la linia 41: prima condiție (tec > 127) nu a fost niciodată adevărată. Teste de adăugat (SWR-F3-02): tec = 128, rec = 0 (ERROR_PASSIVE) și, pentru MC/DC pe B, tec = 0, rec = 128 (ERROR_PASSIVE); plus limitele 127 (ERROR_ACTIVE).")
h3("Exercițiul 7")
p("ASIL A: statement ++ (branch +, MC/DC +). ASIL D: branch ++ și MC/DC ++ (statement +, inclus în branch). Dacă la ASIL D MC/DC nu ajunge la 100%: se scriu teste suplimentare sau o justificare bazată pe alte metode (ISO 26262-6, 9.4.4), revizuită și verificată de evaluatorul de siguranță; lipsa justificării înseamnă acoperire insuficientă.")
out.append("</body></html>")
open("/tmp/claude-0/-home-claude/c5f6656f-76ce-5364-a995-5066a29cf46b/scratchpad/swguide/sw_barem_ro.html", "w").write("\n".join(out))
print("ok")
