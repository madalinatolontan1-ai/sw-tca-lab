# Builds the SW TCA instructor explainer (RO): what the app does, why each test is written, how to read the results.
import html
E = html.escape
OUT = "/tmp/claude-0/-home-claude/c5f6656f-76ce-5364-a995-5066a29cf46b/scratchpad/swguide/sw_explainer_ro.html"
out = []
def h(x): out.append('<h2>%s</h2>' % E(x))
def h3(x): out.append('<h3>%s</h3>' % E(x))
def p(x): out.append('<p>%s</p>' % E(x))
def ul(items): out.append('<ul>%s</ul>' % "".join("<li>%s</li>" % E(i) for i in items))
def ol(items): out.append('<ol>%s</ol>' % "".join("<li>%s</li>" % E(i) for i in items))
def table(head, rows, size=10, center=()):
    th = "".join("<th>%s</th>" % E(x) for x in head)
    trs = "".join("<tr>%s</tr>" % "".join(("<td align=center>%s</td>" if i in center else "<td>%s</td>") % (("<b>%s</b>" % E(str(c))) if i == 0 else E(str(c))) for i, c in enumerate(r)) for r in rows)
    out.append('<table class="s%d"><tr>%s</tr>%s</table><p></p>' % (size, th, trs))
def code(lines):
    out.append('<table style="border-collapse:collapse;width:100%%;border:1px solid #000">%s</table><p></p>' % "".join(
        '<tr><td style="width:5%%;text-align:right;color:#999;font-family:\'Courier New\';font-size:9pt;padding:1pt 4pt;border:none">%s</td><td style="font-family:\'Courier New\';font-size:10pt;padding:1pt 4pt;border:none">%s</td></tr>' % (n, E(l).replace(" ", "&nbsp;")) for n, l in lines))

out.append("""<html><head><meta charset="utf-8"><style>
body,p,li,td,th{font-family:'Times New Roman';font-size:12pt}
p{text-align:justify;margin:0 0 6pt 0}
li{text-align:justify;margin:0 0 3pt 0}
h1{font-family:Aptos,Arial;font-size:20pt;color:#0F4761;font-weight:normal;text-align:center}
h2{font-family:Aptos,Arial;font-size:14pt;color:#0F4761;font-weight:normal;margin:16pt 0 6pt 0}
h3{font-family:Aptos,Arial;font-size:12pt;color:#156082;font-weight:normal;margin:12pt 0 4pt 0}
table{border-collapse:collapse;width:100%}
th{background:#000000;color:#FFFFFF;font-size:10pt;border:1px solid #000;padding:2pt 4pt}
td{font-size:10pt;border:1px solid #000;padding:2pt 4pt}
table.s9 td,table.s9 th{font-size:9pt}
</style></head><body>""")
out.append('<h1>SW TCA – ce facem în aplicație și de ce</h1>')
p("Document pentru profesor. Explică, pas cu pas, ce face aplicația SW TCA Lab, de unde vine fiecare test din varianta V0 și ce trebuie să observe studenții după fiecare rulare. Baremul spune ce rezultate sunt corecte; documentul acesta spune de ce.")

h("1. Ideea, legată de HW TCA")
p("La HW TCA aveați un mod de defectare (de exemplu R1 lipsă) și vă întrebați ce mașină de test îl prinde. La SW TCA, „mașina de test” este testul pe care îl scrieți voi: apelați funcția cu niște valori și verificați dacă răspunsul ei este cel cerut de specificație. Este exact ce face un test funcțional (FT): aplicați o intrare, măsurați ieșirea, o comparați cu limita. Diferența este că aici „limita” este cerința.")
p("Acoperirea este o a doua întrebare, separată: prin ce linii de cod au trecut testele? O linie prin care nu a trecut niciun test este ca fața BOTTOM la AOI fără BOTTOM activ: dacă este o greșeală acolo, nu o vede nimeni. De aceea ținta este ca testele să treacă prin tot codul, iar ce nu poate fi atins se justifică (ca riscul rezidual de la HW).")
table(["La HW TCA", "La SW TCA"], [
    ["Mod de defectare (R1 lipsă)", "Cerință (cadrul cu DLC > 8 se respinge)"],
    ["Mașina de test (AOI, ICT, FT)", "Testul scris de student: intrări + rezultat așteptat"],
    ["D: cât de sigur prinde testul defectul", "PASS / FAIL: codul face sau nu ce spune cerința"],
    ["Ce zone ale plăcii vede fiecare test", "Acoperirea: ce linii și ce decizii au fost parcurse"],
    ["Risc rezidual documentat", "Justificarea codului care nu poate fi atins"]])

h("2. Ce se întâmplă când apăsați „Rulează testele”")
ol(["Aplicația ia fiecare rând din tabelul de teste.", "Rulează funcția cu intrările din rând, exact cum ar fi apelată în C.",
    "În timp ce rulează, notează fiecare linie prin care trece și, la fiecare if, dacă a fost adevărat sau fals.",
    "Compară rezultatul obținut cu rezultatul așteptat scris de student: dacă sunt egale, PASS; altfel, FAIL.",
    "Adună notițele de la toate testele și calculează procentele: statement (linii parcurse), decizii (if-uri văzute și adevărate, și false), MC/DC (condiții care și-au demonstrat efectul), cerințe testate (cerințe care au cel puțin un test)."])
p("Două lucruri sunt independente și trebuie explicate separat studenților. PASS / FAIL spune dacă codul are o greșeală pentru valorile încercate. Acoperirea spune cât de mult din cod au încercat testele. Un test poate trece și totuși să nu acopere mare lucru; testele pot acoperi tot codul și totuși unul să pice. Exact a doua situație apare în varianta V0.")
p("Rezultatul așteptat îl scrie studentul, din cerință. Aplicația nu îl ghicește. Dacă studentul copiază în rezultatul așteptat ce a obținut, toate testele trec și greșeala nu mai poate fi găsită; de aceea baremul depunctează această greșeală.")

h("3. Cum se transformă o cerință într-un test")
p("Fiecare cerință este o frază de tipul „dacă intrarea este X, funcția trebuie să răspundă Y”. Testul alege o valoare X și scrie Y ca rezultat așteptat. Pentru valorile la limită se aleg exact pragul din cerință și vecinul lui.")
h3("F1 – can_frame_is_valid (este cadrul CAN valid?)")
p("Un cadru CAN are un identificator (id) și o lungime a datelor (DLC, câți octeți are mesajul, maxim 8). Identificatorul are 11 biți la cadrul standard (maxim 0x7FF) și 29 de biți la cel extins (maxim 0x1FFFFFFF). 0x înseamnă că numărul este scris în hexazecimal.")
table(["Cerință", "Ce spune, în română", "Test care rezultă", "Rezultat așteptat"], [
    ["SWR-F1-01", "Un cadru cu DLC mai mare decât 8 se respinge.", "dlc = 9 (oricare id valid)", "false"],
    ["SWR-F1-02", "La cadrul standard, un identificator mai mare decât 0x7FF se respinge.", "id = 0x800, extended = false", "false"],
    ["SWR-F1-03", "La cadrul extins, un identificator mai mare decât 0x1FFFFFFF se respinge.", "id = 0x20000000, extended = true", "false"],
    ["SWR-F1-04", "Orice cadru care nu e respins de regulile de mai sus se acceptă.", "id = 0x100, dlc = 8; și limitele 0x7FF (standard), 0x1FFFFFFF (extins)", "true"]], size=9)
h3("F2 – sensor_value_plausible (este valoarea radarului credibilă?) – pe V0, distanța longitudinală")
p("Radarul trimite la fiecare 72 ms distanța până la obiect, în pași de 0,1 m (valoarea 1000 înseamnă 100,0 m). Valoarea este credibilă dacă este în domeniul radarului (0,2 … 250 m) și, dacă obiectul era deja urmărit, nu a sărit mai mult de 8,0 m față de măsurarea anterioară (un obiect nu se poate apropia cu mai mult de 400 km/h). La prima detecție a unui obiect (first_sample = true) nu există o valoare anterioară, deci saltul nu contează.")
table(["Cerință", "Ce spune, în română", "Test care rezultă", "Rezultat așteptat"], [
    ["SWR-F2-01", "O distanță sub 2 (0,2 m) se respinge.", "value = 1 (limita: value = 2 se acceptă)", "false (2 → true)"],
    ["SWR-F2-02", "O distanță peste 2500 (250,0 m) se respinge.", "value = 2501 (limita: 2500 se acceptă)", "false (2500 → true)"],
    ["SWR-F2-03", "La prima detecție, orice valoare din domeniu se acceptă.", "first_sample = true, salt mare (1000 față de 2000)", "true"],
    ["SWR-F2-04", "La ciclurile următoare, valoarea se acceptă doar dacă saltul este cel mult 80 (8,0 m).", "first_sample = false, salt 50 (true), 100 (false); limitele 80 (true) și 81 (false)", "vezi coloana anterioară"]], size=9)
h3("F3 – can_error_state (în ce stare este controlerul CAN?)")
p("Controlerul CAN numără erorile: TEC la transmisie, REC la recepție. Standardul CAN spune: cât timp ambele sunt cel mult 127, nodul este ERROR_ACTIVE (normal); dacă unul depășește 127, devine ERROR_PASSIVE (mai prudent); dacă TEC depășește 255, devine BUS_OFF (se deconectează de pe magistrală).")
table(["Cerință", "Ce spune, în română", "Test care rezultă", "Rezultat așteptat"], [
    ["SWR-F3-01", "BUS_OFF când TEC > 255.", "tec = 256 (limita: 255 nu e bus-off)", "BUS_OFF"],
    ["SWR-F3-02", "Altfel, ERROR_PASSIVE când TEC sau REC > 127.", "tec = 128 sau 255; rec = 128", "ERROR_PASSIVE"],
    ["SWR-F3-03", "În rest, ERROR_ACTIVE.", "tec = 127, rec = 0; tec = 0, rec = 127", "ERROR_ACTIVE"]], size=9)
h3("Integrare – can_rx_handler (ce facem cu un cadru primit?)")
table(["Cerință", "Ce spune, în română", "Test care rezultă", "Rezultat așteptat"], [
    ["SWR-INT-01", "Dacă controlerul este BUS_OFF, cadrul se aruncă.", "tec = 300", "RX_BUS_OFF"],
    ["SWR-INT-02", "Altfel, cadrul se acceptă doar dacă este valid (F1) și valoarea e credibilă (F2).", "cadru valid, valoare în domeniu, tec = rec = 0", "RX_ACCEPTED"],
    ["SWR-INT-03", "Un cadru neacceptat întoarce RX_REJECTED.", "dlc = 9; sau value = 3000", "RX_REJECTED"]], size=9)

h("4. Varianta V0, pas cu pas")
h3("F1 – de ce statement nu ajunge și cum se găsește greșeala")
code([(6, "uint32_t max_id = CAN_STD_ID_MAX;     /* 0x7FF */"), (8, "if (extended) {"), (9, "    max_id = CAN_EXT_ID_MAX;           /* 0x1FFFFFFF */"), (10, "}"),
      (11, "if (dlc > CAN_MAX_DLC) {              /* 8 */"), (12, "    return false;"), (13, "}"), (14, "if (id >= max_id) {                   /* greșeala din V0 */"),
      (15, "    return false;"), (16, "}"), (17, "return true;")])
table(["Pas", "Teste în tabel", "Ce arată aplicația", "Ce trebuie să înțeleagă studentul"], [
    ["1", "T1 (exemplul): id 0x100, dlc 9, extended true → false", "statement 63%, decizii 33%; liniile 14, 15, 17 neexecutate", "Testul iese la linia 12 (return), deci restul codului nu rulează. Un test parcurge un singur drum."],
    ["2", "+ T2: 0x20000000, 8, true → false (SWR-F1-03); T3: 0x100, 8, true → true (SWR-F1-04)", "statement 100%; decizii 83%; „linia 8: false”; SWR-F1-02 fără test", "Toate liniile au rulat, dar if (extended) nu a fost niciodată fals: cadrul standard nu a fost testat. Ramura falsă nu are linii proprii, deci statement nu o vede."],
    ["3", "+ T4: 0x800, 8, false → false (SWR-F1-02)", "toate metricile 100%, toate testele PASS", "Pare terminat. Nu este: niciun test nu a încercat exact valoarea maximă permisă."],
    ["4", "+ T5: 0x7FF, 8, false → true; T6: 0x1FFFFFFF, 8, true → true (SWR-F1-04)", "T5 și T6 FAIL (obținut false)", "SWR-F1-02 respinge doar ce e MAI MARE decât 0x7FF, deci 0x7FF trebuie acceptat. Codul îl respinge: la linia 14 scrie >= în loc de >. Acoperirea era deja 100%; doar testul la limită, luat din cerință, a găsit greșeala."]], size=9)
p("Raportul de defect: testul T5; linia 14; corecția if (id > max_id); descrierea: „SWR-F1-02 respinge doar identificatorii mai mari decât 0x7FF, deci 0x7FF trebuie acceptat (SWR-F1-04). Obținut false, așteptat true.”")
h3("F2 – ce este MC/DC, pe un exemplu concret")
p("Decizia de la linia 28 este: (value >= 2) && (value <= 2500) && (first_sample || delta <= 80). În cuvinte: valoarea este în domeniu ȘI (este prima detecție SAU saltul este mic). Are patru condiții: A = nu e prea aproape, B = nu e prea departe, C = e prima detecție, D = saltul e mic.")
p("MC/DC cere să arătăm, pentru fiecare condiție, că ea singură poate schimba răspunsul. Metoda: pornim de la un test în care răspunsul este „acceptat” și stricăm, pe rând, câte o condiție.")
table(["Test", "value / previous / first_sample", "A B C D", "Rezultat", "Ce demonstrează"], [
    ["T1", "1000 / 1050 / false", "1 1 0 1", "true", "cazul de bază: obiect urmărit, salt de 5 m"],
    ["T2", "1000 / 1100 / false", "1 1 0 0", "false", "D: același obiect, salt de 10 m → respins. Diferă doar D (pereche T1–T2)."],
    ["T3", "1000 / 2000 / true", "1 1 1 –", "true", "C: același salt mare, dar e prima detecție → acceptat (pereche T2–T3). D nu mai e evaluat (–), deci nu contează."],
    ["T4", "1 / 0 / true", "0 – – –", "false", "A: prea aproape → respins (pereche T1–T4)."],
    ["T5", "2501 / 2500 / true", "1 0 – –", "false", "B: prea departe → respins (pereche T1–T5)."]], size=9)
p("Liniuța „–” înseamnă că acea condiție nici nu a fost calculată: în C, && se oprește la primul fals, iar || la primul adevărat. Apoi se adaugă limitele din cerințe: 2 (acceptat), 2500 (acceptat), salt 80 (acceptat), salt 81 (respins). La V0, F2 nu are greșeală: toate trec.")
h3("F3 – testele la limită")
p("Se scriu șase teste: 256 (BUS_OFF), 255 (ERROR_PASSIVE), 128 (ERROR_PASSIVE), 127 (ERROR_ACTIVE) pentru TEC, și 128 (ERROR_PASSIVE), 127 (ERROR_ACTIVE) pentru REC. La V0 toate trec. Acasă, fiecare variantă are un >= în loc de > într-una din cele trei comparații; testul de pe limita greșită (255 sau 127) pică. Asta trebuie să găsească studentul.")
h3("Integrare – funcții, apeluri și codul care nu poate fi atins")
p("can_rx_handler întreabă întâi starea controlerului (apelul C1, la F3), apoi verifică cadrul (C2, la F1) și valoarea (C3, la F2). Patru teste parcurg toate drumurile: un cadru bun (RX_ACCEPTED, trec prin C1, C2, C3), același cadru cu tec = 300 (RX_BUS_OFF), un cadru cu dlc = 9 (RX_REJECTED, C3 nu se mai apelează) și o valoare de 3000 (RX_REJECTED). Rezultat: funcții 100%, apeluri 100%, dar statement 82% și decizii 80%.")
p("Liniile 67–68 (cazul default al switch-ului) nu pot fi atinse: F3 întoarce doar trei stări și toate sunt tratate. Codul există pentru siguranță (dacă memoria s-ar corupe) și pentru că regulile de codare MISRA C cer un default la orice switch. Nu se șterge; se justifică: de ce nu poate fi atins, de ce e acceptabil, cum s-ar putea verifica (forțând o valoare invalidă cu un debugger, adică injectarea unui defect). Este echivalentul riscului rezidual de la HW TCA.")

h("5. Ce e diferit acasă")
ul(["F1 și integrarea sunt la fel ca pe V0, dar F1 nu mai are greșeală: testele la limită trec.",
    "F2 verifică alt semnal (distanță, viteză relativă sau distanță laterală), cu alte limite; metoda este aceeași.",
    "Greșeala plantată este în F3; testul la limită care pică o arată.",
    "Soluțiile de referință pentru fiecare variantă sunt în barem, secțiunea 3."])

h("6. Întrebări pe care le pot pune studenții")
table(["Întrebare", "Răspuns"], [
    ["Ce scriu la rezultatul așteptat?", "Ce spune cerința pentru valorile alese. Nu ce dă codul."],
    ["Toate testele mele trec, dar acoperirea e mică. E bine?", "Nu: au rămas linii sau decizii netestate. Listele de sub procente spun ce lipsește."],
    ["Am 100% peste tot și un test pică. Am greșit testul?", "Verificați rezultatul așteptat față de cerință. Dacă e corect, ați găsit o greșeală în cod: completați raportul de defect."],
    ["De ce nu pot acoperi liniile 67–68?", "Nu există intrare care să ajungă acolo. Se justifică, nu se testează."],
    ["Ce înseamnă „linia 8: false”?", "Decizia de la linia 8 nu a fost niciodată falsă: lipsește un test cu condiția falsă."],
    ["Ce înseamnă „–” în tabelul MC/DC?", "Condiția nu a fost calculată, pentru că rezultatul era deja sigur."],
    ["Ce e 0x?", "Prefixul numerelor scrise în hexazecimal: 0x7FF = 2047."],
    ["Câte teste trebuie?", "Cât să acopere toate cerințele, toate liniile, toate deciziile (și condițiile, la MC/DC) și toate limitele. Pe V0: 6 la F1, 9 la F2, 6 la F3, 4 la integrare."]], size=9)
out.append("</body></html>")
open(OUT, "w").write("\n".join(out))
print(len("\n".join(out)))
