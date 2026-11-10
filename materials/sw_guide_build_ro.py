# Builds the SW TCA lab guide (RO) as HTML for import into Google Docs (same style as the HW TCA guide).
import html
E = html.escape
IMG = "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/faee707/materials/img/sw/"
APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/sw/"
REPO = "https://github.com/madalinatolontan1-ai/sw-tca-lab"
out = []
def h(x): out.append('<h2>%s</h2>' % E(x))
def h3(x): out.append('<h3>%s</h3>' % E(x))
def ex(n, x=None): out.append('<h3>Exercițiul %s</h3>' % n); [p(t) for t in ([x] if isinstance(x, str) else (x or []))]
def p(x, raw=False): out.append('<p>%s</p>' % (x if raw else E(x)))
def pn(x, raw=False): out.append('<p class="n">%s</p>' % (x if raw else E(x)))
def ul(items, raw=False): out.append('<ul>%s</ul>' % "".join("<li>%s</li>" % (i if raw else E(i)) for i in items))
def ol(items, kind="a", raw=False): out.append('<ol type="%s">%s</ol>' % (kind, "".join("<li>%s</li>" % (i if raw else E(i)) for i in items)))
def table(head, rows, center_cols=(), first_bold=True, size=10, raw=False):
    th = "".join("<th>%s</th>" % E(x) for x in head)
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            v = str(c) if raw else E(str(c)); v = "<b>%s</b>" % v if (first_bold and i == 0) else v
            tds.append(("<td align=center>%s</td>" if i in center_cols else "<td>%s</td>") % v)
        trs.append("<tr>%s</tr>" % "".join(tds))
    out.append('<table class="s%d"><tr>%s</tr>%s</table><p></p>' % (size, th, "".join(trs)))
def code(lines):
    out.append('<table style="border-collapse:collapse;width:100%%;border:1px solid #000">%s</table><p></p>' % "".join(
        '<tr><td style="width:5%%;text-align:right;color:#999;font-family:\'Courier New\';font-size:9pt;padding:1pt 4pt;border:none">%s</td><td style="font-family:\'Courier New\';font-size:10pt;color:#1A3F7F;padding:1pt 4pt;border:none;white-space:pre">%s</td></tr>' % (n, E(l).replace(" ", "&nbsp;")) for n, l in lines))
def img(f, w, cap):
    out.append('<p style="text-align:center;text-indent:0"><img src="%s%s" width="%d"></p><p style="text-align:center;text-indent:0;font-size:10pt"><i>%s</i></p>' % (IMG, f, w, E(cap)))
def note(x): out.append('<p class="note">%s</p>' % E(x))

out.append("""<html><head><meta charset="utf-8"><style>
body,p,li,td,th{font-family:'Times New Roman';font-size:12pt}
p{text-align:justify;text-indent:1.25cm;margin:0 0 6pt 0}
p.n{text-indent:0}
p.note{text-indent:0;font-size:11pt;background:#EEF3F8;border-left:3px solid #156082;padding:4pt 6pt}
li{text-align:justify;margin:0 0 3pt 0}
h1{font-family:Aptos,Arial;font-size:20pt;color:#0F4761;font-weight:normal;text-align:center}
h2{font-family:Aptos,Arial;font-size:14pt;color:#0F4761;font-weight:normal;margin:16pt 0 6pt 0}
h3{font-family:Aptos,Arial;font-size:12pt;color:#156082;font-weight:normal;margin:12pt 0 4pt 0}
table{border-collapse:collapse;width:100%}
th{background:#000000;color:#FFFFFF;font-size:10pt;border:1px solid #000;padding:2pt 4pt}
td{font-size:10pt;border:1px solid #000;padding:2pt 4pt}
table.s9 td,table.s9 th{font-size:9pt}
</style></head><body>""")
out.append('<h1>Analiza acoperirii testelor software (SW TCA)</h1>')

# ---------------------------------------------------------------- 1
h("1. Scopul laboratorului")
p("În acest laborator veți analiza cât de complet au fost testate funcțiile software ale unui modul auto: nodul CAN al unui radar frontal. Veți lucra exact ca un inginer de verificare software din industria auto: scrieți teste pornind de la cerințe, le rulați, măsurați ce parte din cod au exercitat testele și decideți ce faceți cu ce a rămas netestat.")
p("La finalul laboratorului veți ști:")
ul(["de ce testarea software se face diferit față de testarea hardware și ce înseamnă un defect sistematic;",
    "ce cer standardele din industria auto (ISO 26262-6 și Automotive SPICE) despre testele software și acoperirea lor;",
    "ce măsoară acoperirea de instrucțiuni (statement), de decizii (branch), MC/DC, acoperirea funcțiilor și a apelurilor;",
    "cum se scriu teste pornind de la cerințe, cu clase de echivalență și valori la limită;",
    "cum se citește un raport de acoperire și ce faceți cu codul rămas neacoperit;",
    "de ce 100% acoperire nu înseamnă cod fără greșeli."])
p("Nu aveți nevoie de experiență în industria auto. Este suficient să știți să citiți cod C: o instrucțiune if, operatorii && și ||, comparațiile. Tot contextul (ce este un cadru CAN, ce face radarul, de unde vin valorile) este explicat în acest îndrumar.")

# ---------------------------------------------------------------- 2
h("2. De ce software-ul se testează altfel decât hardware-ul")
p("La laboratorul de HW TCA ați analizat o placă electronică. Placa este proiectată corect, dar fiecare exemplar fabricat poate avea propriul defect: o componentă lipsă, o lipitură deschisă, un scurtcircuit. Aceste defecte apar întâmplător, pe unele bucăți, și de aceea fiecare placă trece prin teste de producție (AOI, AXI, ICT, FT). Întrebarea de la HW TCA a fost: pentru fiecare mod de defectare, ce test din producție îl detectează?")
p("Software-ul nu se fabrică bucată cu bucată. Toate cele 100.000 de module livrate conțin exact același program, bit cu bit. Codul nu se uzează și nu „iese” cu un defect pe o anumită bucată. Dacă un programator a scris > în loc de >=, greșeala există în toate modulele, din prima zi. Standardul ISO 26262 numește aceste greșeli defecte sistematice (systematic faults): erori introduse la specificare, proiectare sau scriere a codului. Pentru software, ISO 26262 tratează toate defectele ca sistematice; defectele aleatoare (random hardware faults) există doar la hardware.")
p("Consecința practică: un defect software nu poate fi prins în producție, pentru că toate bucățile sunt identice. Singura apărare este verificarea făcută o singură dată, la dezvoltare (plus repetarea testelor la fiecare modificare a codului, numită testare de regresie). De aceea întrebarea se schimbă: nu mai întrebăm „ce test prinde defectul pe această bucată?”, ci „cât de complet am testat codul? A rămas vreo parte din cod pe care niciun test nu a executat-o?”. Dacă o linie de cod nu a fost executată de niciun test, orice greșeală din ea ajunge sigur la client.")
table(["Aspect", "HW TCA (laboratorul anterior)", "SW TCA (acest laborator)"], [
    ["Tipul defectului", "Aleator, de fabricație (lipitură, componentă greșită, scurtcircuit)", "Sistematic (greșeală de specificare, proiectare sau cod)"],
    ["Unde există defectul", "Doar pe unele exemplare", "Identic în toate exemplarele"],
    ["Când se testează", "Fiecare placă, în producție", "O dată pe versiune de software, la dezvoltare, plus regresie"],
    ["Întrebarea analizei", "Ce test de producție detectează fiecare mod de defectare?", "Ce cerințe și ce părți din cod au fost exercitate de teste?"],
    ["Unitatea analizată", "Mod de defectare × componentă × test", "Cerință, instrucțiune, decizie, condiție, funcție, apel"],
    ["Rezultatul unui gol", "Defect scăpat în producție, pe o parte din bucăți", "Cod netestat, cu un posibil defect în toate bucățile"],
    ["Standard de referință", "AIAG-VDA FMEA, practici IPC, ISO 26262-5", "ISO 26262-6, Automotive SPICE (SWE.4–SWE.6)"]])

# ---------------------------------------------------------------- 3
h("3. Unde intră testarea: modelul V")
p("În industria auto, dezvoltarea software urmează modelul V. Pe ramura din stânga se scrie ce trebuie construit (cerințe, arhitectură, proiectare detaliată și cod). Pe ramura din dreapta, fiecărui nivel din stânga îi corespunde un nivel de verificare. Tabelul arată nivelurile software și locul lor în standarde.")
table(["Ce construim (stânga)", "Cum verificăm (dreapta)", "ISO 26262-6:2018", "Automotive SPICE"], [
    ["Cerințe software", "Testarea software-ului integrat (testare de calificare)", "Clauza 11", "SWE.6"],
    ["Arhitectura software", "Testarea integrării software", "Clauza 10", "SWE.5"],
    ["Proiectarea detaliată a unităților și codul", "Verificarea unităților (teste unitare, analiză statică, review)", "Clauza 9", "SWE.4"]])
p("Acoperirea structurală (cât din cod a fost executat) se măsoară la nivel de unitate (clauza 9: instrucțiuni, decizii, MC/DC) și la nivel de integrare (clauza 10: funcții și apeluri). La nivelurile superioare se urmărește acoperirea cerințelor: fiecare cerință are cel puțin un test. În laborator veți lucra la ambele niveluri de jos: funcțiile F1, F2, F3 sunt unități, iar funcția can_rx_handler este nivelul de integrare.")
h3("Vocabular minim")
table(["Termen (RO / EN)", "Ce înseamnă"], [
    ["Cerință / requirement", "O afirmație verificabilă despre comportament. Exemplu: „Funcția raportează BUS_OFF când TEC > 255.” Fiecare cerință are un identificator (de exemplu SWR-F3-01)."],
    ["Caz de test / test case", "Intrări + rezultatul așteptat + cerința verificată. Exemplu: tec = 256, rec = 0, se așteaptă BUS_OFF, verifică SWR-F3-01."],
    ["Oracol de test / test oracle", "Sursa care spune care este rezultatul corect. De obicei este cerința. Un test fără rezultat așteptat nu verifică nimic."],
    ["Verdict", "PASS dacă rezultatul obținut este egal cu cel așteptat, FAIL altfel."],
    ["Trasabilitate / traceability", "Legătura cerință ↔ test ↔ rezultat, în ambele sensuri. În aplicație, coloana „Cerință” din tabelul de teste face această legătură."],
    ["Unitate / unit", "Cea mai mică parte de software testată separat; în C, de obicei o funcție."],
    ["Testare de regresie", "Rularea din nou a tuturor testelor după o modificare a codului."],
    ["Acoperire / coverage", "Procentul din cod (sau din cerințe) exercitat de teste."]])

# ---------------------------------------------------------------- 4
h("4. Regulile reale: ce cer standardele")
p("Standardul de siguranță funcțională pentru autovehicule este ISO 26262 (ediția a doua, 2018). Partea 6 tratează software-ul. Standardul nu impune o singură metodă, ci dă tabele cu metode recomandate în funcție de ASIL (Automotive Safety Integrity Level, de la A, cel mai puțin strict, la D, cel mai strict). Semnele din tabele înseamnă: ++ puternic recomandat, + recomandat, o fără recomandare. În practică, o metodă marcată ++ se aplică întotdeauna; dacă nu se aplică, trebuie scrisă o justificare, pe care evaluatorul de siguranță o verifică.")
note("Sursa valorilor: ISO 26262 este un standard cu plată. Valorile din tabelele de mai jos sunt preluate din reproducerile publicate de producătorii de unelte de test (Vector, LDRA, Parasoft, Verifysoft, MathWorks) și au fost verificate încrucișat. Textul original se găsește prin biblioteca universității.")
h3("4.1 Cum se obțin cazurile de test (ISO 26262-6, tabelul 8)")
table(["Metodă de derivare a testelor", "ASIL A", "ASIL B", "ASIL C", "ASIL D"], [
    ["Analiza cerințelor", "++", "++", "++", "++"],
    ["Generarea și analiza claselor de echivalență", "+", "++", "++", "++"],
    ["Analiza valorilor la limită", "+", "++", "++", "++"],
    ["Ghicirea erorilor din experiență (error guessing)", "+", "+", "+", "+"]], center_cols=(1, 2, 3, 4))
p("Primul rând este cel mai important: testele se scriu pornind de la cerințe, nu de la cod. La ASIL B, clasele de echivalență și valorile la limită sunt și ele ++. Secțiunea 6 explică fiecare metodă.")
h3("4.2 Acoperirea structurală la nivel de unitate (tabelul 9)")
table(["Metrica", "ASIL A", "ASIL B", "ASIL C", "ASIL D"], [
    ["Statement coverage (acoperirea instrucțiunilor)", "++", "++", "+", "+"],
    ["Branch coverage (acoperirea deciziilor)", "+", "++", "++", "++"],
    ["MC/DC (Modified Condition/Decision Coverage)", "+", "+", "+", "++"]], center_cols=(1, 2, 3, 4))
p("Pentru radarul din laborator (ASIL B), statement și branch sunt ++, iar MC/DC este +. De aceea laboratorul cere 100% statement și branch, iar MC/DC îl faceți ca pas suplimentar, cel cerut la ASIL D (frânare, direcție). La ASIL C și D, statement coverage scade la +, nu pentru că ar conta mai puțin, ci pentru că este inclus automat în branch coverage: dacă ați trecut prin toate ramurile, ați executat toate instrucțiunile.")
h3("4.3 Acoperirea la nivel de integrare (tabelul 12)")
table(["Metrica", "ASIL A", "ASIL B", "ASIL C", "ASIL D"], [
    ["Function coverage (acoperirea funcțiilor)", "+", "+", "++", "++"],
    ["Call coverage (acoperirea apelurilor)", "+", "+", "++", "++"]], center_cols=(1, 2, 3, 4))
h3("4.4 Ce faceți când acoperirea nu este completă (clauza 9.4.4)")
p("Standardul spune că acoperirea se măsoară ca să se evalueze cât de complete sunt testele. Dacă acoperirea obținută nu este suficientă, se specifică teste suplimentare sau se scrie o justificare bazată pe alte metode. Notele standardului precizează că lipsa unei ținte de acoperire, sau o țintă mică fără justificare, este considerată insuficientă. Analiza acoperirii poate scoate la iveală teste lipsă, cerințe incomplete, cod mort (care nu poate fi executat niciodată), cod dezactivat sau funcționalitate nedorită.")
p("Standardul nu impune un procent. În practică, în industria auto se cere 100% pentru metricile ++, iar fiecare linie rămasă neacoperită are o justificare scrisă, revizuită și aprobată. Exact asta veți face în exercițiul de integrare.")
h3("4.5 Automotive SPICE")
p("Automotive SPICE (ASPICE, versiunea 4.0 din 2023) nu este un standard de siguranță, ci un model de evaluare a proceselor, folosit de producătorii auto pentru a-și evalua furnizorii. Procesele SWE.4 (verificarea unităților), SWE.5 (verificarea componentelor și a integrării) și SWE.6 (verificarea software-ului) cer ca testele să aibă criterii PASS/FAIL, să fie legate de cerințe în ambele sensuri (trasabilitate bidirecțională), să existe o strategie de regresie și ca rezultatele să fie rezumate și comunicate. Un evaluator ASPICE alege o cerință la întâmplare și urmărește drumul până la test și la rezultat. De aceea fiecare test din aplicație are coloana „Cerință”.")
h3("4.6 Unelte de test și calificarea lor")
p("Unealta care măsoară acoperirea poate greși: dacă raportează o ramură ca executată când nu a fost, cod netestat ajunge în producție. ISO 26262-8 (clauza 11) cere clasificarea uneltelor după impact și după probabilitatea de a detecta o greșeală a uneltei (Tool Confidence Level, TCL1–TCL3) și, unde este cazul, calificarea lor. În industrie se folosesc unelte comerciale cu kit de calificare (VectorCAST, Tessy, LDRA, Cantata, Testwell CTC++, Parasoft C/C++test). În laborator folosim unelte gratuite: gcov și gcovr (din compilatorul GCC; de la GCC 14 măsoară și MC/DC) și aplicația SW TCA Lab. Sunt foarte bune pentru învățare, dar într-un proiect real ASIL B ar avea nevoie de o argumentare de calificare.")
h3("4.7 Ce se întâmplă în alte industrii")
table(["Standard", "Domeniu", "Ce cere"], [
    ["ISO 26262-6:2018", "Auto", "Metode recomandate în funcție de ASIL (tabelele 8, 9, 12); fără procent impus, dar cu justificare pentru fiecare gol"],
    ["DO-178C (2011)", "Aviație civilă", "Obiective obligatorii, 100%: nivelul A cere MC/DC, nivelul B decizii, nivelul C instrucțiuni. MC/DC a apărut în aviație (DO-178B, 1992) și a fost preluat de industria auto"],
    ["IEC 61508-3:2010", "Industrie", "Standardul-mamă din care s-a derivat ISO 26262; tabele similare pe nivelurile SIL 1–4"],
    ["EN 50128 / EN 50716", "Feroviar", "Acoperire de instrucțiuni, ramuri și condiții compuse, în funcție de SIL"],
    ["IEC 62304", "Dispozitive medicale", "Nu impune o metrică anume; cere criterii de acceptare pentru unități"],
    ["Telecomunicații (ETSI, 3GPP, TL 9000)", "Telecom", "Nu am găsit un standard care să ceară acoperirea codului. ETSI și 3GPP definesc teste de conformitate de tip cutie neagră (verifică protocolul, nu codul), iar TL 9000 este un sistem de management al calității. În telecom, acoperirea codului este o practică internă a companiilor, nu o cerință normativă."]])
h3("4.8 De ce contează: un exemplu real")
p("În 2009–2011, Toyota a avut rechemări în service pentru accelerarea neintenționată a unor vehicule. NASA, la cererea autorității americane NHTSA, a analizat software-ul de control al clapetei de accelerație și nu a găsit un defect electronic care să explice incidentele, dar nici nu a putut exclude software-ul. În procesul Bookout v. Toyota (2013), expertul reclamanților a descris un cod greu de testat: zeci de mii de abateri de la regulile de codare MISRA C, funcții prea complexe pentru a fi testate complet, variabile globale neprotejate. Juriul a decis împotriva Toyota. Cazul nu dovedește că un anumit bug a cauzat accidentele, dar arată ce se întâmplă când nu există dovezi că software-ul a fost verificat sistematic: producătorul nu poate demonstra că produsul este sigur.")

# ---------------------------------------------------------------- 5
h("5. Metricile de acoperire")
p("Explicăm metricile pe funcția F3 din laborator, care decide starea de eroare a controlerului CAN pe baza celor două contoare de erori: TEC (transmit error counter, erori la transmisie) și REC (receive error counter, erori la recepție). Regulile vin din standardul CAN, ISO 11898-1: un nod este error active cât timp ambele contoare sunt cel mult 127, devine error passive când TEC sau REC depășește 127 și devine bus-off (se deconectează de la magistrală) când TEC depășește 255.")
code([(35, "/* F3 - ASIL B */"), (36, "can_err_state_t can_error_state(uint16_t tec, uint16_t rec)"), (37, "{"),
      (38, "    if (tec > CAN_BUSOFF_LIMIT) {                 /* 255 */"), (39, "        return CAN_STATE_BUS_OFF;"), (40, "    }"),
      (41, "    if ((tec > CAN_PASSIVE_LIMIT) || (rec > CAN_PASSIVE_LIMIT)) {   /* 127 */"),
      (42, "        return CAN_STATE_ERROR_PASSIVE;"), (43, "    }"), (44, "    return CAN_STATE_ERROR_ACTIVE;"), (45, "}")])
p("Câteva cuvinte pe care le folosim în continuare. O decizie este o expresie care alege drumul programului (de exemplu condiția unui if). O condiție este o parte a unei decizii care nu mai conține && sau ||. Decizia de la linia 41 are două condiții: A = (tec > 127) și B = (rec > 127).")
h3("5.1 Statement coverage (acoperirea instrucțiunilor)")
p("Întrebarea: a fost executată fiecare instrucțiune cel puțin o dată? Un test parcurge un singur drum prin funcție. Fiecare return este capătul unui drum diferit, deci pentru F3 aveți nevoie de cel puțin trei teste:")
table(["Test", "tec", "rec", "Rezultat", "Ce acoperă"], [
    ["T1", "300", "0", "BUS_OFF", "linia 39"], ["T2", "200", "0", "ERROR_PASSIVE", "linia 42"], ["T3", "0", "0", "ERROR_ACTIVE", "linia 44"]], center_cols=(1, 2))
p("Cu aceste trei teste, statement coverage este 100%. Un singur test (de exemplu tec = 300) nu ajunge: funcția iese la linia 39 și restul codului nu se mai execută.")
h3("5.2 Branch coverage (acoperirea deciziilor)")
p("Întrebarea: fiecare decizie a fost cel puțin o dată adevărată (true) și cel puțin o dată falsă (false)? Pentru F3, testele T1–T3 îndeplinesc și această condiție: decizia de la linia 38 este true în T1 și false în T2 și T3; decizia de la linia 41 este true în T2 și false în T3.")
p("Atenție însă la funcția F1 din laborator. Acolo, if (extended) { max_id = …; } nu are ramură else. Dacă toate testele au extended = true, toate instrucțiunile sunt executate (100% statement), dar decizia nu a fost niciodată falsă, deci cazul cadrelor standard nu a fost testat deloc. Ramura false a unui if fără else nu are nicio instrucțiune proprie, așa că statement coverage nu o poate vedea. Branch coverage o vede. De aceea branch coverage include statement coverage, dar nu și invers.")
h3("5.3 Condition coverage (acoperirea condițiilor) și capcana ei")
p("Branch coverage se uită doar la rezultatul deciziei, nu și la condițiile din interior. În T2 (tec = 200), decizia de la linia 41 este adevărată datorită lui A; condiția B nu a fost niciodată adevărată. Dacă programatorul ar fi scris greșit rec > 1270, testele ar trece în continuare. Condition coverage cere ca fiecare condiție să fie o dată adevărată și o dată falsă.")
p("Capcana: pentru A || B, testele (A = adevărat, B = fals) și (A = fals, B = adevărat) dau 100% condition coverage, dar decizia este adevărată de ambele ori, deci ramura false nu a fost executată. Condition coverage nu include branch coverage.")
h3("5.4 MC/DC (Modified Condition/Decision Coverage)")
p("MC/DC le cere pe amândouă și încă ceva: fiecare condiție trebuie să arate că, singură, schimbă rezultatul deciziei. Pentru fiecare condiție căutați o pereche de teste în care se schimbă doar acea condiție, iar rezultatul deciziei se schimbă și el. Pentru A || B de la linia 41:")
table(["Test", "tec", "rec", "A (tec > 127)", "B (rec > 127)", "A || B"], [
    ["T3", "0", "0", "fals", "fals", "fals"], ["T2", "200", "0", "adevărat", "fals", "adevărat"], ["T4", "0", "200", "fals", "adevărat", "adevărat"]], center_cols=(1, 2, 3, 4, 5))
ul(["perechea T3–T2: se schimbă doar A, rezultatul trece din fals în adevărat, deci A contează;",
    "perechea T3–T4: se schimbă doar B, rezultatul trece din fals în adevărat, deci B contează."])
p("Trei teste pentru două condiții. Regula generală: MC/DC se atinge de obicei cu N + 1 teste pentru N condiții, în loc de 2^N (toate combinațiile). La 4 condiții sunt 5 teste în loc de 16; la 10 condiții, 11 în loc de 1024. De aceea MC/DC este folosit în industrie: este riguros, dar realizabil. Testul T4 este exact cel care prinde greșeala rec > 1270 ratată de branch coverage.")
p("O regulă ușor de ținut minte: la ȘI (&&) porniți de la cazul „toate adevărate” și faceți, pe rând, câte o condiție falsă; la SAU (||) porniți de la „toate false” și faceți, pe rând, câte o condiție adevărată.")
p("Un detaliu de limbaj C: la A || B, dacă A este adevărat, B nici nu mai este evaluat (evaluare scurtcircuitată, short-circuit). La A && B, dacă A este fals, B nu mai este evaluat. În tabelele de adevăr din aplicație, o condiție neevaluată apare cu „–”. Uneltele moderne (GCC 14, aplicația din laborator) folosesc varianta masking MC/DC, acceptată în aviație și în auto: o pereche este valabilă și dacă alte condiții diferă, cu condiția ca acele condiții să nu fi influențat rezultatul (de exemplu, nu au fost evaluate).")
h3("5.5 Function coverage și call coverage")
p("La nivel de integrare, function coverage întreabă dacă fiecare funcție a fost apelată măcar o dată, iar call coverage dacă fiecare loc din cod de unde se apelează o funcție a fost executat. Ele pot diferi: dacă o funcție este apelată din trei locuri și testele trec doar prin unul, function coverage este 100%, iar call coverage 33%.")
h3("5.6 Ierarhia metricilor")
p("Pentru cod structurat: MC/DC include branch coverage, care include statement coverage. Condition coverage singură nu include branch coverage. Path coverage (toate drumurile posibile) și multiple condition coverage (toate cele 2^N combinații) sunt și mai stricte, dar practic imposibil de atins pe cod real, așa că ISO 26262 nu le cere.")
h3("5.7 Cel mai important lucru: 100% acoperire nu înseamnă cod fără greșeli")
p("Acoperirea măsoară cât de complet au fost exercitate testele, nu cât de corect este codul. Trei motive:")
ol(["Acoperirea arată că o linie a rulat, nu că a dat rezultatul corect. Un test fără rezultat așteptat corect acoperă cod, dar nu verifică nimic.",
    "Contează valorile alese, nu doar drumul parcurs. Puteți trece prin toate ramurile cu valori „de mijloc” și să nu atingeți niciodată limita la care este greșeala.",
    "Codul care lipsește nu are acoperire. Dacă o cerință nu a fost implementată deloc, nu există nicio linie neacoperită care să vă alerteze. Acest gol îl găsește doar acoperirea cerințelor."], kind="1")
p("Exemplu: dacă la linia 38 programatorul scrie tec >= 255 în loc de tec > 255, testele T1–T4 obțin în continuare 100% statement, branch și MC/DC și toate trec. Greșeala apare doar cu un test exact la limită, tec = 255, pentru care cerința spune ERROR_PASSIVE, iar codul greșit dă BUS_OFF. Valoarea 255 nu v-o dă acoperirea, v-o dă cerința. De aici ordinea corectă de lucru: teste din cerințe, apoi măsurarea acoperirii, apoi analiza golurilor.")
h3("5.8 Cum se citește un raport gcov")
p("gcov este unealta de acoperire a compilatorului GCC; gcovr face din rezultatele lui un raport HTML. Pașii: compilați cu opțiunea --coverage (compilatorul adaugă în program contoare invizibile), rulați testele (fiecare linie și fiecare ramură își numără execuțiile), apoi gcov sau gcovr citește contoarele și scrie raportul. Mai jos este un raport real, pentru F3 rulată cu testele (300, 0), (0, 0) și (10, 5):")
code([("", "function can_error_state called 3 returned 100% blocks executed 86%"),
      ("", "        3:   38:    if (tec > CAN_BUSOFF_LIMIT) {"), ("", "        1:   39:        return CAN_STATE_BUS_OFF;"),
      ("", "        2:   41:    if ((tec > CAN_PASSIVE_LIMIT) || (rec > CAN_PASSIVE_LIMIT)) {"),
      ("", "branch  0 taken 100% (fallthrough)"), ("", "branch  1 taken 0%"), ("", "branch  2 taken 0% (fallthrough)"), ("", "branch  3 taken 100%"),
      ("", "    #####:   42:        return CAN_STATE_ERROR_PASSIVE;"), ("", "        2:   44:    return CAN_STATE_ERROR_ACTIVE;")])
ul(["numărul din stânga arată de câte ori a rulat linia;",
    "##### marchează o linie care nu a fost executată niciodată; pe ea o căutați prima;",
    "– marchează o linie fără cod executabil (acoladă, comentariu);",
    "branch N taken X arată, sub fiecare decizie, de câte ori a fost luată fiecare ieșire; 0% înseamnă o ramură neluată. La A || B compilatorul face două salturi (din cauza evaluării scurtcircuitate), de aceea apar 4 ramuri, nu 2;",
    "procentul pe fișier include toate funcțiile din fișier; când lucrați pe o funcție, uitați-vă la funcția respectivă."])
p("În acest raport, linia 42 nu a fost executată: niciun test nu a dus în starea ERROR_PASSIVE. Testul lipsă se scrie din cerința SWR-F3-02, de exemplu tec = 128, rec = 0.")

# ---------------------------------------------------------------- 6
h("6. Cum se scriu testele: tehnici de derivare")
p("Tabelul 8 din ISO 26262-6 enumeră patru tehnici. Le aplicăm pe cerința SWR-F3-01 („BUS_OFF când TEC > 255”) și SWR-F3-02 („ERROR_PASSIVE când TEC sau REC > 127”).")
h3("6.1 Analiza cerințelor")
p("Pentru fiecare cerință scrieți cel puțin un test care o verifică. Rezultatul așteptat îl luați din cerință, nu din cod. Dacă cerința nu spune clar ce trebuie să se întâmple, testul nu poate fi scris: ați găsit o problemă în cerință, nu în cod.")
h3("6.2 Clase de echivalență")
p("Împărțiți domeniul fiecărei intrări în grupuri pe care funcția ar trebui să le trateze la fel, și alegeți câte o valoare din fiecare grup. Pentru TEC: [0…127] → ERROR_ACTIVE (dacă și REC ≤ 127), [128…255] → ERROR_PASSIVE, [256…65535] → BUS_OFF. Pentru REC: [0…127] și [128…65535]. Includeți și clasele invalide, dacă există.")
h3("6.3 Valori la limită")
p("Greșelile se adună la limite: > în loc de >=, < în loc de <=, un indice cu unu mai mare. Pentru fiecare limită testați valoarea de pe limită și vecinul ei. Pentru F3: TEC = 127 și 128, TEC = 255 și 256, REC = 127 și 128. Testul cu TEC = 255 prinde imediat implementarea greșită tec >= 255.")
h3("6.4 Ghicirea erorilor (error guessing)")
p("Din experiență: valoarea 0, valoarea maximă a tipului (pentru uint16_t, 65535), valori negative la tipuri cu semn, depășiri aritmetice, o valoare care se repetă, o diferență exact zero.")
h3("6.5 Cum se documentează un test")
table(["Câmp", "Exemplu"], [
    ["Identificator", "T2"], ["Cerința verificată", "SWR-F3-02"], ["Tehnica", "Valori la limită (TEC = 255, imediat sub pragul de bus-off)"],
    ["Intrări", "tec = 255, rec = 0"], ["Rezultat așteptat (din cerință)", "ERROR_PASSIVE"], ["Rezultat obținut", "ce returnează codul"], ["Verdict", "PASS sau FAIL"]])
p("În aplicație, fiecare rând din tabelul „Teste” are exact aceste câmpuri, mai puțin tehnica, pe care o notați în observații.")

# ---------------------------------------------------------------- 7
h("7. Studiul de caz și de unde vine fiecare element")
h3("7.1 Sistemul")
p("Studiul de caz este același la toate laboratoarele (HW TCA, SW TCA, FMEA): nodul CAN al unui radar frontal. Radarul de referință este Continental ARS 408-21, un radar de 77 GHz care detectează obiectele din fața vehiculului și transmite, la fiecare ciclu de măsurare (aproximativ 72 ms), lista obiectelor pe magistrala CAN, la 500 kbit/s. Pentru fiecare obiect se transmit, printre altele, distanța longitudinală, distanța laterală și viteza relativă. Pe placă, transceiver-ul CAN este MCP2551, cel pe care l-ați analizat la HW TCA.")
p("Firmware-ul nodului primește cadre CAN, verifică dacă sunt valide (F1), verifică dacă valorile senzorului sunt plauzibile (F2), urmărește starea de eroare a controlerului CAN (F3) și decide ce face cu fiecare cadru primit (can_rx_handler, nivelul de integrare).")
h3("7.2 ASIL B")
p("Toate funcțiile au ASIL B, ca radarul. În realitate, ASIL-ul rezultă din analiza pericolelor și a riscurilor (HARA, ISO 26262-3) făcută pentru funcția vehiculului. Pentru laborator, ASIL B este o ipoteză de lucru realistă pentru un radar frontal folosit în funcții de asistență: o defectare poate duce la o reacție greșită a vehiculului, dar șoferul rămâne responsabil. ASIL D se folosește pentru funcții ca frânarea sau direcția, unde o defectare poate fi direct catastrofală.")
h3("7.3 Codul")
p("Codul (fișierul can_node.c) a fost scris pentru acest laborator. Firmware-ul real al unui radar este proprietar și nu poate fi folosit la curs. Funcțiile sunt simplificate, dar au forma unei unități software reale: o funcție, intrări de tipuri fixe (uint32_t, uint16_t, int16_t), constante cu nume, un singur punct de decizie pe fiecare regulă. Codul este public, în repository-ul laboratorului, împreună cu testele demonstrative pentru gcov.")
h3("7.4 De unde vine fiecare valoare")
table(["Element", "Valoare", "De unde vine"], [
    ["CAN_STD_ID_MAX", "0x7FF", "ISO 11898-1: cadrul standard are identificator de 11 biți, deci maxim 2^11 − 1 = 0x7FF."],
    ["CAN_EXT_ID_MAX", "0x1FFFFFFF", "ISO 11898-1: cadrul extins are identificator de 29 de biți, deci maxim 2^29 − 1."],
    ["CAN_MAX_DLC", "8", "ISO 11898-1, CAN clasic: un cadru are cel mult 8 octeți de date. Standardul permite codurile DLC 9–15, dar le tratează tot ca 8 octeți. Cerința SWR-F1-01 le respinge: este o verificare de robustețe aleasă de noi."],
    ["CAN_PASSIVE_LIMIT", "127", "ISO 11898-1, mecanismul de izolare a defectelor (fault confinement): error passive când TEC sau REC > 127."],
    ["CAN_BUSOFF_LIMIT", "255", "ISO 11898-1: bus-off când TEC > 255 (doar TEC, nu și REC)."],
    ["Distanța longitudinală", "0,2 … 250 m", "Fișa tehnică ARS 408-21: domeniul de măsurare far range, 0,20…250 m."],
    ["Viteza relativă", "−111,1 … +55,6 m/s", "Fișa tehnică ARS 408-21: −400 km/h … +200 km/h, convertit în m/s."],
    ["Distanța laterală", "−70 … +70 m", "Derivat: în near range radarul vede până la 70 m; un obiect nu poate fi mai departe lateral decât este de departe în total, deci |y| ≤ 70 m."],
    ["Ciclul de măsurare", "72 ms", "Fișa tehnică ARS 408-21: aproximativ 72 ms pentru măsurarea near și far."],
    ["Pas maxim, distanță", "8,0 m pe ciclu", "Derivat: viteza de apropiere maximă de 400 km/h = 111,1 m/s; în 72 ms obiectul se poate deplasa cel mult 111,1 × 0,072 = 8,0 m."],
    ["Pas maxim, viteză", "1,4 m/s pe ciclu", "Derivat: 1,4 m/s în 72 ms înseamnă o accelerație de 19,4 m/s², adică aproape 2 g, peste ce poate face un vehicul real."],
    ["Pas maxim, lateral", "0,7 m pe ciclu", "Derivat: 0,7 m în 72 ms înseamnă o viteză laterală de 9,7 m/s (35 km/h), peste o schimbare de bandă reală."],
    ["Unitatea 0,1 m și 0,1 m/s", "valori întregi", "Simplificare a laboratorului, ca valorile să fie numere întregi ușor de citit (2500 = 250,0 m). Mesajul CAN real al radarului folosește rezoluții de 0,2 m și 0,25 m/s."]], size=9)
h3("7.5 Cerințele")
p("Cerințele software (SWR-F1-01 … SWR-INT-03) au fost scrise pentru laborator pornind de la valorile din tabelul de mai sus. Sunt formulate în engleză, cum se lucrează în industrie: specificațiile, testele și rapoartele circulă între echipe din mai multe țări. Fiecare cerință are un identificator, ca testele să poată fi legate de ea.")
h3("7.6 Variantele și greșelile plantate")
p("Fiecare student primește o variantă. Variantele diferă în două locuri: semnalul radarului verificat de F2 (distanță longitudinală, viteză relativă sau distanță laterală) și locul în care am plantat o greșeală. Greșeala este de fiecare dată un operator > înlocuit cu >=, adică o greșeală de limită (off-by-one), cel mai frecvent tip de greșeală din codul de comparații. Am ales-o pentru că trece de toate metricile de acoperire și este prinsă doar de un test la limită, scris din cerință: exact lecția acestui laborator.")
table(["Variantă", "Semnal în F2", "Greșeala plantată", "Unde se folosește"], [
    ["V0", "distanță longitudinală", "F1: id >= max_id", "demo, rezolvată împreună la laborator"],
    ["V1", "distanță longitudinală", "F3: tec >= CAN_BUSOFF_LIMIT", "acasă, notată"],
    ["V2", "distanță longitudinală", "F3: tec >= CAN_PASSIVE_LIMIT", "acasă, notată"],
    ["V3", "viteză relativă", "F3: rec >= CAN_PASSIVE_LIMIT", "acasă, notată"],
    ["V4", "viteză relativă", "F3: tec >= CAN_BUSOFF_LIMIT", "acasă, notată"],
    ["V5", "distanță laterală", "F3: tec >= CAN_PASSIVE_LIMIT", "acasă, notată"],
    ["V6", "distanță laterală", "F3: rec >= CAN_PASSIVE_LIMIT", "acasă, notată"]], center_cols=(0,))
p("La V0 greșeala este în F1, iar la variantele de acasă în F3, așa că rezolvarea făcută împreună nu dă răspunsul temei. V0 are aceeași greșeală ca demonstrația gcov din curs (make report SET=f1_branch BUG=1), deci ce vedeți în terminal la curs este același lucru cu ce faceți în aplicație.")

# ---------------------------------------------------------------- 8
h("8. Aplicația SW TCA Lab")
p('Aplicația rulează în browser, fără instalare: <a href="%s">%s</a>. Ea imită o unealtă de acoperire de tip gcov: vedeți codul C al unei funcții, scrieți teste, apăsați „Rulează testele” și primiți verdictul fiecărui test, liniile și deciziile executate și procentele de acoperire. Codul afișat este același cu cel din repository; aplicația îl execută printr-o copie în JavaScript care numără execuțiile, cum face gcov.' % (APP, APP), raw=True)
h3("8.1 Pornirea")
p("În tab-ul Start introduceți numele, grupa și codul variantei (V0 la laborator, varianta voastră acasă), apoi „Încarcă varianta”. Lucrul se salvează în browserul folosit; dacă schimbați calculatorul, o luați de la capăt. Butonul RO/EN schimbă limba. Taburile sunt: F1 validare cadru, F2 plauzibilitate, F3 stare CAN, Integrare și Raport.")
img("sw_v0_start.png", 600, "Figura 1. Tab-ul F1 la început, pe varianta V0, cu testul-exemplu T1.")
h3("8.2 Zonele unui tab")
table(["Zona", "Ce conține și cum se citește"], [
    ["„Înainte de teste: ce cere ISO 26262-6 pentru ASIL B?” (doar la F1)", "Alegeți ++, + sau o pentru statement, branch și MC/DC. Răspunsul ajunge în raport. Răspunsul corect este în secțiunea 4.2."],
    ["Ce ai de făcut", "Pașii exercițiului pentru funcția respectivă."],
    ["Cerințe", "Specificația funcției. De aici scrieți testele și rezultatul așteptat."],
    ["Cod testat", "Codul C, adnotat ca un raport gcov. Numărul de lângă linie arată de câte ori a rulat; ##### și fundalul roșu înseamnă neexecutat; verde înseamnă executat; galben înseamnă decizie acoperită doar parțial. Etichetele T și F de lângă fiecare decizie sunt verzi dacă decizia a fost adevărată, respectiv falsă, cel puțin o dată, și roșii dacă nu. La switch apar etichete pentru fiecare caz."],
    ["Teste", "Tabelul în care adăugați teste: intrările, rezultatul așteptat și cerința verificată. După rulare apar rezultatul obținut și verdictul PASS / FAIL. Intrările în hexazecimal se scriu cu 0x."],
    ["Rezultatul rulării", "Procentele: statement, decizii (branch), MC/DC (condiții), cerințe testate; la integrare și funcții apelate, apeluri executate. Sub ele: instrucțiunile neexecutate, rezultatele de decizie lipsă (de exemplu „linia 8: false” înseamnă că decizia de la linia 8 nu a fost niciodată falsă), cerințele fără test și condițiile MC/DC nedemonstrate. Aceste liste vă spun exact ce test mai lipsește."],
    ["Tabelul de adevăr MC/DC", "Pentru deciziile cu mai multe condiții: fiecare test pe un rând, fiecare condiție pe o coloană (1 = adevărat, 0 = fals, – = neevaluată din cauza evaluării scurtcircuitate) și rezultatul deciziei. Sub tabel, fiecare condiție este „demonstrată prin perechea Tx–Ty” sau „nedemonstrată”."],
    ["Raport de defect (F3, și F1 la V0)", "Dacă un test pică: testul, linia suspectă, corecția propusă în C și descrierea (cerința, rezultatul obținut, rezultatul așteptat)."],
    ["Justificarea codului neacoperit (Integrare)", "Pentru fiecare linie care rămâne neacoperită: de ce nu poate fi atinsă și de ce este acceptabil."],
    ["Observații", "Text liber care ajunge în raport: tehnicile folosite, concluziile."]])
h3("8.3 Raportul")
p("Tab-ul Raport adună tot: datele voastre, răspunsul la întrebarea despre ISO 26262, testele, acoperirea, raportul de defect, justificările și observațiile. Raportul se descarcă (.html) sau se trimite direct, conform indicațiilor de la laborator. Acesta este documentul care se notează.")
h3("8.4 Aplicația și gcov")
p('Demonstrația din curs folosește uneltele reale, gcov și gcovr, pe același cod. O puteți rula și voi, gratuit, în browser: în repository-ul laboratorului (<a href="%s">%s</a>) apăsați Code → Codespaces → Create codespace on main, apoi în terminal make report SET=f1_statement, make report SET=f1_branch BUG=1 sau make report SET=f1_limits BUG=1, și make serve pentru raportul HTML. Comenzile sunt descrise în fișierul README.' % (REPO, REPO), raw=True)

# ---------------------------------------------------------------- 9
h("9. Exemplul rezolvat: varianta V0")
p("Această secțiune este rezolvarea completă a variantei V0, pe care o facem împreună la laborator. Urmăriți fiecare pas în aplicație, pe V0. Acasă refaceți aceiași pași pe varianta voastră.")
h3("9.1 Întrebarea despre ISO 26262")
p("La F1 alegeți: statement coverage ++, branch coverage ++, MC/DC +. Sursa: tabelul 9, coloana ASIL B (secțiunea 4.2).")
h3("9.2 F1: can_frame_is_valid")
p("Funcția verifică dacă un cadru CAN este valid: DLC cel mult 8 și identificatorul în domeniul tipului de cadru (standard sau extins). Pornim cu testul-exemplu T1 (DLC = 9, verifică SWR-F1-01) și rulăm: statement 63%, branch 33%. Lista „Instrucțiuni neexecutate” arată liniile 14, 15 și 17.")
pn("Pasul 1, 100% statement. Adăugăm câte un test pentru cerințele încă netestate:")
table(["Test", "id", "dlc", "extended", "Așteptat", "Cerință", "De ce"], [
    ["T2", "0x20000000", "8", "true", "false", "SWR-F1-03", "identificator peste maximul extins (clasă invalidă)"],
    ["T3", "0x100", "8", "true", "true", "SWR-F1-04", "cadru valid; DLC = 8 este exact limita"]], center_cols=(2, 3, 4))
img("sw_v0_f1_b.png", 600, "Figura 2. F1 cu T1–T3: 100% statement, dar decizia de la linia 8 nu a fost niciodată falsă.")
p("Rezultat: statement 100%, dar branch 83%. Lista „Rezultate de decizie lipsă” arată „linia 8: false”: toate testele au extended = true, deci cadrul standard nu a fost testat, iar cerința SWR-F1-02 nu are test. Aceasta este lecția exercițiului: 100% statement nu înseamnă că toate cazurile au fost testate.")
pn("Pasul 2, 100% branch. Adăugăm testul pentru cadrul standard:")
table(["Test", "id", "dlc", "extended", "Așteptat", "Cerință", "De ce"], [
    ["T4", "0x800", "8", "false", "false", "SWR-F1-02", "identificator standard imediat peste 0x7FF"]], center_cols=(2, 3, 4))
p("Acum statement, branch, MC/DC și cerințele sunt 100%, iar toate testele trec. Pare gata. Nu este.")
pn("Pasul 3, valorile la limită din cerințe. Cerința SWR-F1-02 spune că se respinge un identificator mai mare decât 0x7FF, deci 0x7FF însuși trebuie acceptat. La fel 0x1FFFFFFF pentru cadrul extins:")
table(["Test", "id", "dlc", "extended", "Așteptat", "Cerință", "Obținut"], [
    ["T5", "0x7FF", "8", "false", "true", "SWR-F1-04", "false → FAIL"],
    ["T6", "0x1FFFFFFF", "8", "true", "true", "SWR-F1-04", "false → FAIL"]], center_cols=(2, 3, 4))
img("sw_v0_f1_d.png", 600, "Figura 3. F1 cu testele la limită: acoperire 100% pe toate metricile, dar T5 și T6 pică.")
p("Am găsit greșeala plantată: la linia 14 scrie id >= max_id, deci identificatorul maxim valid este respins. Toate metricile erau deja 100% înainte de T5 și T6; doar testele la limită, scrise din cerință, au găsit-o. Raportul de defect:")
table(["Câmp", "Ce scriem"], [
    ["Testul care pică", "T5 (și T6)"], ["Linia suspectă", "14"], ["Corecția propusă", "if (id > max_id) {"],
    ["Descriere", "SWR-F1-02 cere respingerea identificatorilor mai mari decât 0x7FF, deci 0x7FF trebuie acceptat (SWR-F1-04). Pentru id = 0x7FF, cadru standard, funcția returnează false; se aștepta true. Comparația de la linia 14 folosește >= în loc de >, deci respinge și valoarea maximă validă. Aceeași greșeală apare la cadrul extins (T6, 0x1FFFFFFF)."]])
h3("9.3 F2: sensor_value_plausible")
p("Funcția verifică dacă o distanță măsurată de radar este plauzibilă: în domeniul 0,2…250 m și, dacă obiectul era deja urmărit, fără un salt mai mare de 8,0 m față de măsurarea anterioară. Decizia de la linia 28 are patru condiții:")
ul(["A: value >= SENSOR_MIN (2, adică 0,2 m)", "B: value <= SENSOR_MAX (2500, adică 250,0 m)", "C: first_sample (prima detecție a obiectului)", "D: delta <= SENSOR_MAX_STEP (80, adică 8,0 m)"])
p("Decizia este A && B && (C || D). Pentru MC/DC aveți nevoie de cel puțin N + 1 = 5 teste. Pornim de la cazul în care obiectul este urmărit și saltul este mic (rezultat adevărat) și schimbăm pe rând câte o condiție:")
table(["Test", "value", "previous", "first_sample", "Așteptat", "Cerință", "Ce demonstrează"], [
    ["T1", "1000", "1050", "false", "true", "SWR-F2-04", "cazul de bază: în domeniu, salt de 5,0 m"],
    ["T2", "1000", "1100", "false", "false", "SWR-F2-04", "D: salt de 10,0 m (perechea T1–T2)"],
    ["T3", "1000", "2000", "true", "true", "SWR-F2-03", "C: prima detecție acceptă orice salt (perechea T2–T3)"],
    ["T4", "1", "0", "true", "false", "SWR-F2-01", "A: sub 0,2 m (perechea T1–T4)"],
    ["T5", "2501", "2500", "true", "false", "SWR-F2-02", "B: peste 250,0 m (perechea T1–T5)"]], center_cols=(1, 2, 3, 4))
p("Observați perechea T2–T3 pentru C: în T3, D nu mai este evaluată (C este adevărat, deci C || D este adevărat fără D). Aceasta este situația din masking MC/DC: D diferă între cele două teste, dar nu influențează rezultatul, deci perechea este valabilă. Apoi adăugăm valorile la limită din cerințe: 2 (acceptat), 2500 (acceptat), un salt exact de 80 (acceptat) și unul de 81 (respins).")
table(["Test", "value", "previous", "first_sample", "Așteptat", "Cerință"], [
    ["T6", "2", "2", "true", "true", "SWR-F2-01"], ["T7", "2500", "2500", "false", "true", "SWR-F2-02"],
    ["T8", "1080", "1000", "false", "true", "SWR-F2-04"], ["T9", "1081", "1000", "false", "false", "SWR-F2-04"]], center_cols=(1, 2, 3, 4))
img("sw_v0_f2_full.png", 560, "Figura 4. F2 pe V0: tabelul de adevăr MC/DC și perechea care demonstrează fiecare condiție.")
p("Toate testele trec și toate metricile sunt 100%: la V0, F2 nu are greșeală.")
h3("9.4 F3: can_error_state")
p("Scriem testele strict din cerințele SWR-F3, cu valorile la limită din secțiunea 6.3:")
table(["Test", "tec", "rec", "Așteptat", "Cerință"], [
    ["T1", "256", "0", "BUS_OFF", "SWR-F3-01"], ["T2", "255", "0", "ERROR_PASSIVE", "SWR-F3-02"], ["T3", "128", "0", "ERROR_PASSIVE", "SWR-F3-02"],
    ["T4", "127", "0", "ERROR_ACTIVE", "SWR-F3-03"], ["T5", "0", "128", "ERROR_PASSIVE", "SWR-F3-02"], ["T6", "0", "127", "ERROR_ACTIVE", "SWR-F3-03"]], center_cols=(1, 2))
p("La V0 toate trec, cu 100% pe toate metricile. Acasă, aceleași teste vor face să pice unul dintre ele, pentru că greșeala variantei voastre este în F3. Testul care pică vă arată limita greșită.")
h3("9.5 Integrare: can_rx_handler")
p("Funcția primește un cadru CAN, contextul senzorului și contoarele de erori. Întâi întreabă starea controlerului (apelul C1, linia 52). Dacă starea este BUS_OFF, aruncă cadrul. Altfel verifică validitatea cadrului (apelul C2, linia 57) și, dacă este valid, plauzibilitatea valorii (apelul C3, linia 58). Patru teste acoperă toate funcțiile și toate apelurile:")
table(["Test", "Intrări relevante", "Așteptat", "Cerință", "Ce acoperă"], [
    ["I1", "cadru valid, value = 1000, previous = 1050, tec = rec = 0", "RX_ACCEPTED", "SWR-INT-02", "C1, C2, C3; drumul de acceptare"],
    ["I2", "același cadru, tec = 300", "RX_BUS_OFF", "SWR-INT-01", "ramura BUS_OFF a switch-ului"],
    ["I3", "dlc = 9", "RX_REJECTED", "SWR-INT-03", "cadru invalid; C3 nu se mai apelează"],
    ["I4", "value = 3000", "RX_REJECTED", "SWR-INT-03", "valoare neplauzibilă"]])
img("sw_v0_int.png", 600, "Figura 5. Integrarea pe V0: toate funcțiile și apelurile sunt acoperite, dar liniile 67–68 (default) rămân neexecutate.")
p("Funcții apelate 100%, apeluri executate 100%, dar statement 82% și branch 80%: liniile 67–68 (cazul default al switch-ului) nu pot fi executate. can_error_state() returnează doar cele trei stări tratate explicit, deci niciun test nu poate ajunge în default. Este cod defensiv, cerut de regulile de codare MISRA C (orice switch are un default), care protejează programul dacă variabila state ar fi coruptă în memorie. Justificarea, de exemplu:")
note("Liniile 67–68 (default) nu pot fi atinse prin teste: can_error_state() returnează numai ERROR_ACTIVE, ERROR_PASSIVE și BUS_OFF, toate tratate explicit. Codul este defensiv, cerut de MISRA C:2012 regula 16.4, și tratează o valoare coruptă a lui state (de exemplu o eroare de memorie) returnând RX_FAULT. Poate fi verificat prin injectare de defecte (fault injection): un test care forțează state la o valoare invalidă, posibil doar cu un stub sau un debugger. Codul este acceptat ca neacoperit, cu această justificare.")
h3("9.6 Raportul")
p("În tab-ul Raport verificați că apar testele, acoperirea, raportul de defect pentru F1 și justificarea pentru integrare. Pe V0 nu trimiteți raportul; este doar exercițiu.")

# ---------------------------------------------------------------- 10
h("10. Exerciții")
p("Exercițiile 1–7 se rezolvă pe hârtie și vă pregătesc pentru aplicație. Exercițiile 8–11 se fac în aplicație, pe V0, împreună la laborator (urmați secțiunea 9). Tema, pe varianta voastră, se predă și se notează.")
ex(1, "Pentru fiecare situație, spuneți dacă defectul este aleator (hardware) sau sistematic (software ori proiectare) și dacă poate fi detectat de un test de producție:")
ol(["un condensator montat cu valoare greșită pe 0,5% din plăci;", "o comparație scrisă > în loc de >= în firmware;",
    "o lipitură care se fisurează după 5 ani de vibrații;", "o cerință care uită să spună ce se întâmplă la DLC = 0;",
    "un tranzistor care se defectează la temperatură mare;", "o funcție care nu tratează valoarea 65535 a unui contor."])
ex(2, "Pentru funcția de mai jos, scrieți numărul minim de teste pentru 100% statement coverage, apoi pentru 100% branch coverage. Pentru fiecare test, dați valoarea lui temp și rezultatul.")
code([(1, "int fan_level(int16_t temp)"), (2, "{"), (3, "    int level = 0;"), (4, "    if (temp > 60) {"), (5, "        level = 1;"), (6, "    }"),
      (7, "    if (temp > 90) {"), (8, "        level = 2;"), (9, "    }"), (10, "    return level;"), (11, "}")])
ex(3, "Pentru decizia if ((a > 0) || (b > 0)), dați două teste care obțin 100% condition coverage, dar nu 100% branch coverage. Explicați de ce.")
ex(4, "Pentru fiecare decizie, scrieți combinațiile de adevărat/fals pentru MC/DC (N + 1 teste) și perechea care demonstrează fiecare condiție:")
ol(["if ((v >= 2) && (v <= 2500))", "if (a || b || c)", "if (a && (b || c))"])
ex(5, "Pentru cerința „Senzorul de temperatură este în defect dacă temperatura citită este sub −40 °C sau peste 125 °C”, scrieți clasele de echivalență și valorile la limită pe care le testați. Cât este minimul de teste?")
ex(6, "Citiți raportul gcov din secțiunea 5.8. Ce linie nu a fost executată? Ce înseamnă „branch 1 taken 0%” la linia 41? Ce test(e) adăugați și din ce cerință?")
ex(7, "Folosind tabelele din secțiunea 4, completați pentru ASIL A și pentru ASIL D: ce metrici de acoperire la nivel de unitate sunt ++? Ce se întâmplă dacă, la ASIL D, MC/DC nu ajunge la 100%?")
ex(8, "În aplicație, pe V0, tab-ul F1: răspundeți la întrebarea despre ISO 26262 și refaceți pașii 1–3 din secțiunea 9.2. În observații, scrieți de ce 100% statement nu era suficient și ce test a găsit greșeala. Completați raportul de defect.")
ex(9, "În aplicație, pe V0, tab-ul F2: obțineți 100% MC/DC cu cel mult 5 teste, apoi adăugați testele la limită. Pentru fiecare condiție notați perechea care o demonstrează. Explicați perechea pentru C (first_sample).")
ex(10, "În aplicație, pe V0, tab-ul F3: scrieți testele din cerințe, cu toate valorile la limită (127/128, 255/256 pentru TEC și 127/128 pentru REC). Ce acoperire obțineți? Pică vreun test?")
ex(11, "În aplicație, pe V0, tab-ul Integrare: obțineți 100% funcții și apeluri. Care linii rămân neacoperite și de ce? Scrieți justificarea.")
h3("Tema (se notează)")
p("Acasă, încărcați în aplicație varianta voastră (V1–V6) și refaceți exercițiile 8–11 pe ea:")
ol(["la F1: răspunsul despre ISO 26262, testele pentru toate cerințele, 100% statement și branch, observațiile;",
    "la F2: 100% MC/DC cu perechile notate, plus testele la limită pentru semnalul variantei voastre (atenție, limitele sunt altele decât la V0);",
    "la F3: testele din cerințe, cu toate valorile la limită; testul care pică și raportul de defect complet (cerința încălcată, linia, corecția în C, descrierea);",
    "la Integrare: 100% funcții și apeluri, justificarea codului neacoperit;",
    "în tab-ul Raport: verificați raportul și trimiteți-l (sau descărcați-l și predați-l, conform indicațiilor)."], kind="1")
p("Nota se acordă pe raport: corectitudinea testelor și a rezultatelor așteptate, legătura cu cerințele, acoperirea obținută, găsirea și descrierea greșelii, calitatea justificărilor și a observațiilor.")

# ---------------------------------------------------------------- 11
h("Anexa A. Glosar român / englez")
table(["Română", "English", "Explicație scurtă"], [
    ["acoperirea instrucțiunilor", "statement coverage", "fiecare instrucțiune executată cel puțin o dată"],
    ["acoperirea deciziilor", "branch / decision coverage", "fiecare decizie a fost și adevărată, și falsă"],
    ["acoperirea condițiilor", "condition coverage", "fiecare condiție a fost și adevărată, și falsă"],
    ["MC/DC", "Modified Condition/Decision Coverage", "fiecare condiție influențează singură rezultatul deciziei"],
    ["acoperirea funcțiilor", "function coverage", "fiecare funcție apelată cel puțin o dată"],
    ["acoperirea apelurilor", "call coverage", "fiecare loc de apel executat"],
    ["acoperirea cerințelor", "requirements coverage", "fiecare cerință are cel puțin un test"],
    ["caz de test", "test case", "intrări, rezultat așteptat, cerință"],
    ["oracol de test", "test oracle", "sursa rezultatului corect (de obicei cerința)"],
    ["trasabilitate bidirecțională", "bidirectional traceability", "legături cerință ↔ test ↔ rezultat"],
    ["clase de echivalență", "equivalence classes", "grupuri de intrări tratate la fel"],
    ["analiza valorilor la limită", "boundary value analysis", "teste pe limită și imediat lângă ea"],
    ["ghicirea erorilor", "error guessing", "teste alese din experiență"],
    ["injectarea de defecte", "fault injection", "defecte introduse intenționat pentru a verifica reacția"],
    ["cod mort", "dead code", "cod care nu poate fi executat niciodată (greșeală de proiectare)"],
    ["cod defensiv", "defensive code", "protecție pentru situații care nu ar trebui să apară"],
    ["defect sistematic", "systematic fault", "greșeală de proiectare, prezentă în toate exemplarele"],
    ["defect aleator hardware", "random hardware fault", "defectare întâmplătoare a unei componente"],
    ["evaluare scurtcircuitată", "short-circuit evaluation", "în C, && și || se opresc când rezultatul este cunoscut"]], size=9)
h("Anexa B. Bibliografie și resurse")
for t, u in [("Aplicația SW TCA Lab", APP), ("Repository-ul laboratorului (cod, teste demonstrative, Codespaces)", REPO),
             ("K. J. Hayhurst, D. S. Veerhusen, J. J. Chilenski, L. K. Rierson, „A Practical Tutorial on Modified Condition/Decision Coverage”, NASA/TM-2001-210876, 2001", "https://shemesh.larc.nasa.gov/fm/papers/Hayhurst-2001-tm210876-MCDC.pdf"),
             ("Vector, „Following the ISO 26262-6:2018 Guidelines with VectorCAST” (whitepaper)", "https://cdn.vector.com/cms/content/products/VectorCAST/Docs/Whitepapers/English/VectorCAST_Following_the_ISO26262-62018-Guidelines-with-VectorCAST.pdf"),
             ("LDRA, „Implementing ISO 26262 second edition” (whitepaper)", "https://ldra.com/wp-content/uploads/ldra/Implementing_ISO_26262_second_edition_white_paper.pdf"),
             ("VDA QMC, Automotive SPICE PAM 4.0", "https://vda-qmc.de/wp-content/uploads/2023/06/Automotive-SPICE-PAM-40-Gelbbandrelease.pdf"),
             ("ZVEI, „Best Practice Guideline: Software for Safety-Related Automotive Systems” (2025)", "https://www.zvei.org/fileadmin/user_upload/Presse_und_Medien/Publikationen/2025/Januar/Best_Practice_Guideline_Software_for_Safety-Related_Automotive_Systems/Best-Practice-Guideline-Software-for-Safety-Related-Automotive-Systems_final.pdf"),
             ("GCC, Instrumentation Options (-fcondition-coverage, MC/DC din GCC 14)", "https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html"),
             ("Continental / Aumovio, ARS 408-21 Long Range Radar (fișă tehnică)", "https://engineering-solutions.aumovio.com/wp-content/uploads/2025/10/121118_FS_ARS-408-21_EN_HS.pdf"),
             ("Texas Instruments, „Introduction to the Controller Area Network (CAN)”, SLOA101", "https://www.ti.com/lit/SLOA101"),
             ("P. Koopman, „A Case Study of Toyota Unintended Acceleration and Software Safety” (2014)", "https://betterembsw.blogspot.com/2014/09/a-case-study-of-toyota-unintended.html")]:
    p('<a href="%s">%s</a>' % (u, E(t)), raw=True)
p("Standarde (prin biblioteca universității): ISO 26262-6:2018 (clauzele 9–11), ISO 26262-8:2018 (clauza 11), ISO 11898-1 (CAN), MISRA C:2012, DO-178C, IEC 61508-3.")
out.append("</body></html>")
open("/tmp/claude-0/-home-claude/c5f6656f-76ce-5364-a995-5066a29cf46b/scratchpad/swguide/sw_guide_ro.html", "w").write("\n".join(out))
print(len("\n".join(out)))
