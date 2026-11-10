# Builds the SW TCA lab guide (RO) as HTML for import into Google Docs, in the structure of the HW TCA guide:
# short theory blocks, each followed by an exercise (verbal or in the app), homework, resources.
import html
E = html.escape
IMG = "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/b3c1781/materials/sw_deck_src/img/"
APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/sw/"
REPO = "https://github.com/madalinatolontan1-ai/sw-tca-lab"
OUT = "/tmp/claude-0/-home-claude/c5f6656f-76ce-5364-a995-5066a29cf46b/scratchpad/swguide/sw_guide_ro_v3.html"
out = []
def h(x): out.append('<h2>%s</h2>' % E(x))
def ex(n, kind, x=None):
    out.append('<h3>Exercițiul %s (%s)</h3>' % (n, kind)); [p(t) for t in ([x] if isinstance(x, str) else (x or []))]
def p(x, raw=False): out.append('<p>%s</p>' % (x if raw else E(x)))
def ol(items, kind="a"): out.append('<ol type="%s">%s</ol>' % (kind, "".join("<li>%s</li>" % E(i) for i in items)))
def table(head, rows, center_cols=(), first_bold=True, size=10):
    th = "".join("<th>%s</th>" % E(x) for x in head)
    trs = "".join("<tr>%s</tr>" % "".join(("<td align=center>%s</td>" if i in center_cols else "<td>%s</td>") % (("<b>%s</b>" % E(str(c))) if (first_bold and i == 0) else E(str(c))) for i, c in enumerate(r)) for r in rows)
    out.append('<table class="s%d"><tr>%s</tr>%s</table><p></p>' % (size, th, trs))
def code(lines):
    out.append('<table style="border-collapse:collapse;width:100%%;border:1px solid #000">%s</table><p></p>' % "".join(
        '<tr><td style="width:5%%;text-align:right;color:#999;font-family:\'Courier New\';font-size:9pt;padding:1pt 4pt;border:none">%d</td><td style="font-family:\'Courier New\';font-size:10pt;font-weight:bold;color:#1A7F37;padding:1pt 4pt;border:none">%s</td></tr>' % (i + 1, E(l).replace(" ", "&nbsp;")) for i, l in enumerate(lines)))
def img(f, w, cap):
    out.append('<p style="text-align:center;text-indent:0"><img src="%s%s" width="%d"></p><p style="text-align:center;text-indent:0;font-size:10pt"><i>%s</i></p>' % (IMG, f, w, E(cap)))

out.append("""<html><head><meta charset="utf-8"><style>
body,p,li,td,th{font-family:'Times New Roman';font-size:12pt}
p{text-align:justify;text-indent:1.25cm;margin:0 0 6pt 0}
li{text-align:justify}
h1{font-family:Aptos,Arial;font-size:20pt;color:#0F4761;font-weight:normal;text-align:center}
h2{font-family:Aptos,Arial;font-size:14pt;color:#0F4761;font-weight:normal;margin:16pt 0 6pt 0}
h3{font-family:Aptos,Arial;font-size:12pt;color:#156082;font-weight:normal;margin:12pt 0 4pt 0}
table{border-collapse:collapse;width:100%}
th{background:#000000;color:#FFFFFF;font-size:10pt;border:1px solid #000;padding:2pt 4pt}
td{font-size:10pt;border:1px solid #000;padding:2pt 4pt}
table.s9 td,table.s9 th{font-size:9pt}
</style></head><body>""")
out.append('<h1>Analiza acoperirii testelor software (SW TCA)</h1>')

h("Ce este analiza SW TCA?")
p("La HW TCA, placa este proiectată corect, dar fiecare bucată fabricată poate ieși cu propriul defect (o componentă lipsă, o lipitură deschisă), de aceea fiecare placă trece prin testele de producție. Software-ul nu se fabrică bucată cu bucată: toate modulele livrate conțin exact același program. Dacă un programator a scris >= în loc de >, greșeala există în toate modulele, din prima zi. ISO 26262 numește aceste greșeli defecte sistematice; pentru software, toate defectele sunt sistematice.")
p("Un defect software nu poate fi prins în producție, pentru că toate bucățile sunt identice. Codul se verifică o dată, la dezvoltare, și din nou la fiecare modificare (testare de regresie). Software Test Coverage Analysis (SW TCA) răspunde la întrebarea: cât de complet au exercitat testele codul și cerințele? A rămas vreo linie pe care niciun test nu a executat-o? Dacă da, orice greșeală din ea ajunge sigur la client.")
p("Ținta este 100%. Ce nu poate fi acoperit prin teste se justifică în scris: de ce nu poate fi atins și de ce este acceptabil. Este echivalentul riscului rezidual de la HW TCA.")
p("Acoperirea se măsoară cu metrici. Cele folosite în laborator sunt:")
table(["Metrică", "Ce verifică", "Prinde bine", "Limitări"], [
    ["Statement coverage", "Fiecare instrucțiune a fost executată cel puțin o dată.", "cod niciodată executat (un return, o ramură cu instrucțiuni)", "nu vede ramura falsă a unui if fără else"],
    ["Branch coverage", "Fiecare decizie (if, switch) a fost și adevărată, și falsă.", "cazuri netestate ale unei decizii", "nu vede condițiile din interiorul unei decizii cu && sau ||"],
    ["MC/DC", "Fiecare condiție dintr-o decizie schimbă, singură, rezultatul.", "condiții fără efect sau scrise greșit", "nu alege valorile la limită"],
    ["Function / call coverage", "Fiecare funcție a fost apelată; fiecare loc de apel a fost executat.", "funcții sau apeluri netestate la integrare", "nu spune nimic despre interiorul funcției"]])
p("Niciuna dintre metrici nu spune dacă rezultatul este corect. Asta o face doar rezultatul așteptat al testului, luat din cerință.")
ex(1, "verbal", "Pentru fiecare problemă de mai jos, spuneți ce metrică o scoate la iveală, sau dacă niciuna nu o poate vedea:")
ol(["un return pe care niciun test nu l-a executat;", "un if fără else, testat doar cu condiția adevărată;",
    "o condiție dintr-o decizie cu ||, care nu a schimbat niciodată rezultatul;", "o funcție pe care niciun test de integrare nu o apelează;",
    "o comparație scrisă >= în loc de >, testată doar cu valori departe de limită."])

h("Ce cer standardele")
p("Standardul de siguranță funcțională pentru autovehicule, ISO 26262 (ediția 2018), partea 6, recomandă metricile în funcție de ASIL (Automotive Safety Integrity Level, de la A la D, D fiind cel mai strict). ++ înseamnă puternic recomandat (în practică obligatoriu; dacă nu se aplică, se scrie o justificare), + înseamnă recomandat.")
table(["Metrică", "ASIL A", "ASIL B", "ASIL C", "ASIL D"], [
    ["Statement coverage (unitate, tabelul 9)", "++", "++", "+", "+"], ["Branch coverage (unitate, tabelul 9)", "+", "++", "++", "++"],
    ["MC/DC (unitate, tabelul 9)", "+", "+", "+", "++"], ["Function coverage (integrare, tabelul 12)", "+", "+", "++", "++"],
    ["Call coverage (integrare, tabelul 12)", "+", "+", "++", "++"]], center_cols=(1, 2, 3, 4))
p("Dacă acoperirea nu este suficientă, standardul cere teste suplimentare sau o justificare (clauza 9.4.4). Testele se scriu pornind de la cerințe, iar Automotive SPICE, modelul cu care producătorii auto își evaluează furnizorii, cere ca fiecare test să fie legat de cerința pe care o verifică.")
ex(2, "verbal", "Radarul din laborator este ASIL B. Ce metrici sunt ++ la ASIL B? Dar la ASIL A și la ASIL D? De ce scade statement coverage la + la ASIL C și D? Ce se întâmplă dacă, la ASIL D, MC/DC nu ajunge la 100%?")

h("Studiul de caz: firmware-ul nodului CAN al radarului frontal")
p("Lucrăm pe același radar frontal auto generic ca la HW TCA (ipoteza laboratorului: ASIL B), care trimite lista de obiecte detectate pe CAN, la 500 kbit/s, la fiecare ciclu de măsurare (aproximativ 72 ms). Firmware-ul nodului CAN are patru funcții C. Codul a fost scris pentru laborator, după regulile reale: limitele CAN vin din standardul ISO 11898-1, iar domeniile senzorului sunt valori tipice pentru un radar auto de lungă distanță. În aplicație vedeți, pentru fiecare valoare, de unde vine.")
table(["Funcție", "Ce face", "Intrări", "Ieșire", "Cerințe"], [
    ["F1 can_frame_is_valid", "Verifică dacă un cadru CAN este valid: DLC cel mult 8 și identificatorul în domeniul de 11 biți (standard) sau 29 de biți (extins).", "id, dlc, extended", "true / false", "SWR-F1-01…04"],
    ["F2 sensor_value_plausible", "Verifică dacă valoarea radarului este în domeniu și nu sare prea mult față de ciclul anterior.", "value, previous, first_sample", "true / false", "SWR-F2-01…04"],
    ["F3 can_error_state", "Stabilește starea controlerului CAN din contoarele de erori TEC și REC.", "tec, rec", "ERROR_ACTIVE / ERROR_PASSIVE / BUS_OFF", "SWR-F3-01…03"],
    ["can_rx_handler (integrare)", "Primește un cadru și le apelează pe F3, F1 și F2.", "cadru, context senzor, tec, rec", "RX_ACCEPTED / RX_REJECTED / RX_BUS_OFF", "SWR-INT-01…03"]], size=9)
p('Mod de lucru: lucrați în aplicația web SW TCA Lab (<a href="%s">%s</a>), în browser, fără instalare. Completați numele, grupa și codul de variantă și apăsați „Încarcă varianta”. La laborator lucrați pe varianta demonstrativă V0. Acasă, pentru notare, faceți aceeași analiză pe varianta voastră (V1–V6), după cum scrie la tema de la final. Fiecare tab (F1, F2, F3, Integrare) are cerințele, codul și tabelul de teste. Scrieți testele (intrările, rezultatul așteptat din cerință și cerința verificată) și apăsați „Rulează testele”. Codul se colorează ca un raport de acoperire: numărul de lângă linie arată de câte ori a rulat, ##### înseamnă linie neexecutată, iar etichetele T și F arată dacă decizia a fost adevărată, respectiv falsă. Sub procente, listele „Instrucțiuni neexecutate”, „Rezultate de decizie lipsă” și „Cerințe fără test” vă spun ce test mai lipsește.' % (APP, APP), raw=True)
img("d_f1b_code.png", 520, "F1 pe V0, după trei teste: eticheta F roșie de la linia 8 arată că decizia nu a fost niciodată falsă.")
ex(3, "în aplicație", "Încărcați varianta V0. În F1 și F2, numărați deciziile și condițiile din cod și spuneți ce cerință implementează fiecare decizie.")

h("Statement coverage și branch coverage")
p("Un test parcurge un singur drum prin funcție. În F3, fiecare return este capătul unui drum diferit, deci pentru 100% statement coverage trebuie cel puțin trei teste:")
code(["if (tec > CAN_BUSOFF_LIMIT) {                    /* 255 */", "    return CAN_STATE_BUS_OFF;", "}",
      "if ((tec > CAN_PASSIVE_LIMIT) || (rec > CAN_PASSIVE_LIMIT)) {  /* 127 */", "    return CAN_STATE_ERROR_PASSIVE;", "}", "return CAN_STATE_ERROR_ACTIVE;"])
table(["Test", "tec", "rec", "Rezultat", "Ce acoperă"], [["T1", "300", "0", "BUS_OFF", "linia 2"], ["T2", "200", "0", "ERROR_PASSIVE", "linia 5"], ["T3", "0", "0", "ERROR_ACTIVE", "linia 7"]], center_cols=(1, 2))
p("Branch coverage cere ca fiecare decizie să fie o dată adevărată și o dată falsă. În F1, if (extended) { max_id = …; } nu are else. Dacă toate testele au extended = true, toate instrucțiunile se execută (100% statement), dar cadrul standard nu a fost testat deloc: ramura falsă nu are nicio instrucțiune proprie, așa că statement coverage nu o vede. De aceea branch coverage include statement coverage, dar nu și invers.")
ex(4, "verbal", "Pentru funcția de mai jos, câte teste trebuie, minim, pentru 100% statement coverage? Dar pentru 100% branch coverage? Ce valori ale lui temp alegeți? Ce caz rămâne netestat, chiar cu 100% branch?")
code(["int fan_level(int16_t temp)", "{", "    int level = 0;", "    if (temp > 60) {", "        level = 1;", "    }", "    if (temp > 90) {", "        level = 2;", "    }", "    return level;", "}"])
ex(5, "în aplicație", "Pe V0, în tab-ul F1, răspundeți la întrebarea despre ISO 26262. Scrieți câte un test pentru cerințele SWR-F1-01, SWR-F1-03 și SWR-F1-04, toate cu extended = true, și rulați: urmăriți statement și branch. Adăugați apoi testul care lipsește (lista „Rezultate de decizie lipsă”) și spuneți ce cerință acoperă. Notați în observații de ce 100% statement nu era suficient.")

h("MC/DC")
p("O decizie poate avea mai multe condiții legate prin && sau ||. Decizia de la linia 4 din F3 are două: A = (tec > 127) și B = (rec > 127). Branch coverage se uită doar la rezultatul deciziei: cu testele T2 și T3, B nu a fost niciodată adevărat, iar o greșeală în B (de exemplu rec > 1270) ar trece neobservată. MC/DC cere ca fiecare condiție să arate că, singură, schimbă rezultatul: pentru fiecare condiție există o pereche de teste în care se schimbă doar ea, iar rezultatul se schimbă și el.")
table(["Test", "tec", "rec", "A", "B", "A || B"], [["T3", "0", "0", "fals", "fals", "fals"], ["T2", "200", "0", "adevărat", "fals", "adevărat"], ["T4", "0", "200", "fals", "adevărat", "adevărat"]], center_cols=(1, 2, 3, 4, 5))
p("Perechea T3–T2 arată A, perechea T3–T4 arată B. Pentru N condiții sunt suficiente de obicei N + 1 teste, în loc de toate cele 2^N combinații. La ȘI (&&) porniți de la cazul „toate adevărate” și faceți, pe rând, câte o condiție falsă; la SAU (||) porniți de la „toate false” și faceți câte una adevărată. În C, && și || se opresc când rezultatul este sigur (evaluare scurtcircuitată): în tabelul de adevăr din aplicație, o condiție neevaluată apare cu „–”, iar perechea este valabilă și dacă diferă doar condiții neevaluate (masking MC/DC).")
img("d_f2_tt.png", 330, "Tabelul de adevăr MC/DC pentru F2 pe V0 și perechea care demonstrează fiecare condiție.")
ex(6, "verbal", "Pentru fiecare decizie, spuneți combinațiile de adevărat și fals pentru MC/DC (N + 1 teste) și perechea care demonstrează fiecare condiție:")
ol(["if ((v >= 2) && (v <= 2500))", "if (a || b || c)", "if (a && (b || c))"])
ex(7, "în aplicație", "Pe V0, în tab-ul F2, obțineți 100% MC/DC cu cel mult 5 teste. Decizia este A && B && (C || D): A și B verifică domeniul, C este prima detecție a obiectului, D verifică saltul față de ciclul anterior. Notați perechea care demonstrează fiecare condiție și explicați perechea pentru C.")

h("Cum se scriu testele și de ce 100% nu înseamnă fără greșeli")
p("Testele se scriu din cerințe, nu din cod (ISO 26262-6, tabelul 8). Tehnicile sunt:")
table(["Tehnică", "Ce faceți", "Exemplu pe F3 (bus-off când TEC > 255)"], [
    ["Analiza cerințelor", "Cel puțin un test pe fiecare cerință; rezultatul așteptat vine din cerință.", "tec = 300 → BUS_OFF"],
    ["Clase de echivalență", "Împărțiți domeniul în grupuri tratate la fel și luați câte o valoare din fiecare.", "TEC 0…127, 128…255, 256…65535"],
    ["Valori la limită", "Testați limita și vecinul ei: aici stau greșelile de tip > în loc de >=.", "TEC 127 / 128 și 255 / 256; REC 127 / 128"],
    ["Ghicirea erorilor", "Valori alese din experiență.", "0, 65535, diferență exact zero"]])
p("Acoperirea arată că o linie a rulat, nu că a dat rezultatul corect. Puteți trece prin toate ramurile cu valori „de mijloc” și să nu atingeți niciodată limita greșită. Ordinea corectă este: teste din cerințe, apoi acoperirea, apoi golurile.")
p("Avem următorul exemplu, din varianta V0 (îl refaceți la exercițiul 9). Cu patru teste, F1 are 100% statement, branch, MC/DC și cerințe, iar toate testele trec. Cerința SWR-F1-02 spune că se respinge un identificator mai mare decât 0x7FF, deci 0x7FF însuși trebuie acceptat. Testul cu id = 0x7FF, cadru standard, pică: funcția returnează false. La linia 14 scrie id >= max_id în loc de id > max_id. Raportul de defect arată așa:")
table(["Test care pică", "Linia", "Corecția", "Descriere"], [["T5: id = 0x7FF, dlc = 8, extended = false", "14", "if (id > max_id) {", "SWR-F1-02 respinge doar identificatorii mai mari decât 0x7FF, deci 0x7FF trebuie acceptat (SWR-F1-04). Obținut false, așteptat true. Comparația >= respinge și valoarea maximă validă."]], size=9)
ex(8, "verbal", "Cerința: „Senzorul de temperatură este în defect dacă temperatura citită este sub −40 °C sau peste 125 °C.” Ce clase de echivalență și ce valori la limită testați? Care este numărul minim de teste?")
ex(9, "în aplicație", "Pe V0, în tab-ul F1, adăugați testele la limită pentru cadrul standard și cel extins (0x7FF și 0x1FFFFFFF). Care test pică? Completați raportul de defect: testul, linia, corecția și descrierea (cerința, rezultatul obținut, rezultatul așteptat).")
ex(10, "în aplicație", "Pe V0, în tab-ul F3, scrieți testele din cerințele SWR-F3, cu toate valorile la limită (TEC 127 / 128 și 255 / 256, REC 127 / 128). Ce acoperire obțineți? Pică vreun test? Acasă, greșeala variantei voastre este în F3.")

h("Integrarea și codul care nu poate fi atins")
p("La integrare, funcția can_rx_handler le apelează pe celelalte trei. Aici se urmăresc function coverage (fiecare funcție apelată) și call coverage (fiecare loc de apel executat). Ce rămâne neacoperit se analizează: lipsește un test, lipsește o cerință, sau codul nu poate fi atins. Codul care nu poate fi atins nu se șterge dacă are un rol (de exemplu cod defensiv, cerut de regulile de codare MISRA C), ci se justifică: de ce nu poate fi atins, de ce este acceptabil și cum s-ar putea verifica totuși (de exemplu prin injectarea unui defect).")
ex(11, "verbal", "În aplicație, la F3, după testele (tec = 300, rec = 0), (0, 0) și (10, 5), linia 42 apare cu ##### și lista „Rezultate de decizie lipsă” arată „linia 41: true”. Ce înseamnă? Ce teste adăugați și din ce cerință? Gândiți-vă și la MC/DC.")
ex(12, "în aplicație", "Pe V0, în tab-ul Integrare, obțineți 100% funcții apelate și 100% apeluri executate. Care linii rămân neacoperite și de ce? Scrieți justificarea în câmpul „Justificarea codului neacoperit”.")

h("Temă pentru acasă (pentru notare)")
p("Acasă faceți analiza completă pe varianta voastră. Pașii sunt cei pe care i-ați făcut la laborator pe V0:")
ol(["în aplicație apăsați „Începe de la zero”, apoi încărcați varianta voastră (V1–V6), cu numele și grupa;",
    "refaceți exercițiile 5, 7, 9, 10 și 12 pe varianta voastră (atenție: la F2 limitele semnalului sunt altele decât la V0);",
    "la F3, testul la limită care pică vă arată greșeala variantei: completați raportul de defect;",
    "în fiecare tab, notați în observații tehnicile folosite (clase de echivalență, valori la limită) și concluzia;",
    "în tab-ul Raport, verificați raportul și trimiteți-l. Dacă trimiterea nu este confirmată, descărcați raportul (.html) și păstrați-l."], kind="1")

h("Resurse")
for t, u in [("Aplicația SW TCA Lab", APP), ("Repository-ul laboratorului (codul, demonstrația cu gcov în Codespaces)", REPO),
             ("K. J. Hayhurst, D. S. Veerhusen, J. J. Chilenski, L. K. Rierson, „A Practical Tutorial on Modified Condition/Decision Coverage”, NASA/TM-2001-210876, 2001", "https://shemesh.larc.nasa.gov/fm/papers/Hayhurst-2001-tm210876-MCDC.pdf"),
             ("ISO 26262-6:2018, Road vehicles — Functional safety — Part 6: Product development at the software level (prin biblioteca universității)", "https://www.iso.org/standard/68388.html")]:
    p('<a href="%s">%s</a>' % (u, E(t)), raw=True)
out.append("</body></html>")
open(OUT, "w").write("\n".join(out))
print(len("\n".join(out)))
