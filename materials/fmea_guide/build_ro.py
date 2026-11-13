"""FMEA lab guide (RO), DFMEA HW + SW, in the style of the HW TCA exercise guide.
Writes fmea_guide_ro.html, uploaded to Drive as a Google Doc."""
import html, json, os
SHA = os.environ.get("IMG_SHA", "main")
IMG = "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/%s/docs/guide-img/fmea/" % SHA
APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/fmea/"
e = html.escape
out = []
def h1(t): out.append("<h1>%s</h1>" % e(t))
def h2(t): out.append("<h2>%s</h2>" % e(t))
def h3(t): out.append("<h3>%s</h3>" % e(t))
def p(t, raw=False): out.append("<p>%s</p>" % (t if raw else e(t)))
def ol(items): out.append("<ol>" + "".join("<li>%s</li>" % e(i) for i in items) + "</ol>")
def ul(items): out.append("<ul>" + "".join("<li>%s</li>" % e(i) for i in items) + "</ul>")
def table(rows, bold_first_col=True):
    s = "<table border='1' style='border-collapse:collapse'>"
    for i, r in enumerate(rows):
        s += "<tr>" + "".join(("<td><b>%s</b></td>" if (i == 0 or (bold_first_col and j == 0)) else "<td>%s</td>") % e(str(c)) for j, c in enumerate(r)) + "</tr>"
    out.append(s + "</table>")
def fig(name, cap, w=600):
    out.append("<p style='text-align:center'><img src='%s%s' width='%d'></p>" % (IMG, name, w))
    out.append("<p style='text-align:center'><i>%s</i></p>" % e(cap))

h1("Analiza modurilor de defectare și a efectelor (FMEA): DFMEA hardware și software")

h2("Ce este FMEA?")
p("FMEA (Failure Mode and Effects Analysis) este o analiză de risc făcută înainte ca defectul să existe. Echipa ia fiecare element al produsului, scrie ce trebuie să facă (funcțiile), se întreabă cum poate să nu facă asta (modurile de defectare), ce se întâmplă atunci (efectele) și de ce s-ar putea întâmpla (cauzele). Pentru fiecare lanț efect – mod – cauză evaluează riscul și decide ce face ca riscul să scadă. FMEA este preventivă: valoarea ei e mare la început, când o schimbare costă puțin, și scade cu fiecare fază în care defectul rămâne negăsit.")
p("Există trei tipuri de FMEA în manualul AIAG-VDA (2019), folosit în industria auto:")
table([["Tip", "Ce analizează", "Exemplu pe modulul CAN"],
       ["DFMEA (de design)", "Designul produsului: schema, componentele alese, layout-ul, codul, cerințele", "R4 ales cu putere nominală prea mică; SENSOR_MAX scris în altă unitate"],
       ["PFMEA (de proces)", "Procesul de fabricație și asamblare", "C2 lipsă după montaj; lipitură rece la J2 (laboratorul TCA HW)"],
       ["FMEA-MSR", "Monitorizarea și răspunsul sistemului în funcționare, în vehicul", "Radarul detectează bus-off și raportează defectul către ECU-ul ADAS"]])
p("În acest laborator facem DFMEA pe nodul CAN al radarului frontal, pe două părți ale lui: un semnal hardware și o funcție software. Metoda este aceeași pentru amândouă. Diferă doar cauzele: la hardware ele țin de alegerea și dimensionarea componentelor, de schemă și de layout; la software toate cauzele sunt sistematice (cerințe, constante, logică, tipuri de date, interfețe), pentru că software-ul nu se uzează și nu se fabrică bucată cu bucată.")
h3("De ce se face, când și pe ce")
ul(["De ce: ca defectele să fie găsite și eliminate în design, nu la client. Un defect găsit în teren costă mult mai mult decât unul găsit la design (rechemări, garanții, răspundere juridică).",
    "Când: DFMEA începe odată cu designul (concept, schemă, arhitectura software) și se actualizează la fiecare schimbare; este un document viu. PFMEA începe când se proiectează linia de fabricație.",
    "Pe ce: pe sistem (radarul), pe subsisteme și componente (nodul CAN, transceiverul, filtrele), pe software (funcțiile) și pe procesul de fabricație.",
    "Cine: o echipă, nu o persoană: proiectant HW, dezvoltator SW, inginer de test și validare, inginer de siguranță funcțională, inginer de calitate. În laborator, voi jucați toate aceste roluri."])
h3("Standarde, legi și industrii")
table([["Domeniu", "Ce cere FMEA"],
       ["Auto", "Manualul AIAG-VDA FMEA (2019) și SAE J1739 (2021) descriu metoda. IATF 16949 cere analiza riscului de design (DFMEA) printre ieșirile designului și PFMEA printre ieșirile procesului. ISO 26262-9 (clauza 8) cere analize de siguranță, iar FMEA este analiza inductivă folosită cel mai des."],
       ["General", "IEC 60812:2018 descrie FMEA și FMECA pentru orice industrie."],
       ["Aeronautică", "SAE ARP4761A (2023) pentru evaluarea siguranței; SAE AS13004 pentru PFMEA și planul de control."],
       ["Medical", "ISO 14971 pentru managementul riscului dispozitivelor medicale; FMEA este una dintre tehnicile folosite."],
       ["Feroviar", "EN 50126 (RAMS), cu FMEA ca analiză de bază."],
       ["Telecom", "Nu există un standard FMEA dedicat. TL 9000 este sistemul de management al calității pentru sectorul ICT; pentru analiză se folosesc IEC 60812 și, pentru fiabilitate, Telcordia SR-332."]])
p("Ce se întâmplă dacă FMEA nu se face: la auditul IATF 16949 lipsa ei este o neconformitate, iar furnizorul poate pierde certificarea și clientul. Dacă defectul ajunge în teren, urmează rechemări și răspunderea pentru produse defecte; noua directivă europeană privind răspunderea pentru produse (UE 2024/2853) include explicit și software-ul.")
h3("Exercițiul 1 (verbal)")
p("Pentru fiecare situație, spuneți dacă este o cauză de DFMEA sau de PFMEA și de ce:")
ol(["R4 a fost ales cu o putere nominală prea mică pentru starea dominantă;",
    "R4 lipsește de pe placă după montaj;",
    "SENSOR_MAX a fost scris în grade, iar restul codului lucrează în zecimi de grad;",
    "lipitura unui pin al lui J2 este rece;",
    "cerința pentru prima detecție a unui obiect lipsește din specificația software."])

h2("Cei 7 pași ai metodei AIAG-VDA")
table([["Pas", "Ce faceți", "În aplicație"],
       ["1. Planificare", "Scopul, momentul, echipa, sarcinile și instrumentele (cei 5T)", "Pasul 1 · Planificare"],
       ["2. Analiza structurii", "Arborele de structură: N1 efect (radarul), N2 elementul analizat, N3 categoriile de cauze", "Tab-urile HW și SW, pașii 2–3"],
       ["3. Analiza funcțiilor", "Funcțiile fiecărui element: verb + obiect + condiție măsurabilă", "Pașii 2–3"],
       ["4. Analiza defectărilor", "Efecte, moduri de defectare și cauze, legate în rețeaua de defectare", "Pasul 4"],
       ["5. Analiza riscului", "Controale de prevenție și detecție; S, O, D; prioritatea de acțiune AP", "Pașii 5–6"],
       ["6. Optimizare", "Acțiuni pentru AP H și M, cu responsabil și termen; O și D noi", "Pașii 5–6"],
       ["7. Documentare", "Raportul cu rezultatele", "Pasul 7 · Raport"]])
h3("Exercițiul 2 (verbal)")
p("Încărcați în aplicație varianta demo F0 și citiți cei 5T din Pasul 1. Ce intră în analiză și ce nu? De ce procesul de fabricație nu face parte din DFMEA?")

h2("Studiul de caz și aplicația")
p("Lucrăm pe același radar frontal auto generic ca la laboratoarele TCA (ipoteza laboratorului: ASIL B), care trimite lista de obiecte detectate pe CAN, la 500 kbit/s, la aproximativ 72 ms. Nodul CAN are partea hardware din laboratorul TCA HW (modulul cu transceiverul MCP2551) și partea software din laboratorul TCA SW (funcțiile de recepție).")
p("Mod de lucru: lucrați în aplicația web <a href='%s'>FMEA Lab</a>, în browser, fără instalare. Completați numele și codul de variantă și apăsați „Încarcă varianta”. La laborator lucrați pe varianta demo F0, împreună cu cadrul didactic: filtrele RC de pe CANH / CANL (HW) și verificarea de plauzibilitate a unghiului azimut, funcția sensor_value_plausible() (SW). Acasă faceți aceeași analiză pe varianta voastră (F1–F6) și trimiteți raportul. Aplicația are un tab pentru analiza HW, unul pentru analiza SW și tab-ul Raport. Fiecare analiză are trei etape: pașii 2–3 (structură și funcții), pasul 4 (rețeaua de defectare) și pașii 5–6 (risc și optimizare). La fiecare etapă găsiți „Context”, „Cum se face” (cu exemplul pe F0) și tabelele AIAG-VDA de referință. Lucrul se salvează în browserul folosit." % APP, raw=True)
p("Simplificare de laborator: alegeți o singură funcție pe element, cel mult 3 moduri de defectare, 3 efecte și 2 cauze pe mod. Aplicația vă avertizează când treceți de aceste limite, dar nu vă blochează. În industrie, analiza acoperă toate funcțiile și toate defectările; aici urmărim cum le evaluați, nu o analiză completă.")

h2("Structura și funcțiile (pașii 2–3)")
p("Arborele de structură are trei niveluri. N1 este nivelul efectului: radarul, văzut din vehicul. N2 este elementul analizat: semnalul hardware sau funcția software din varianta voastră; aici apar modurile de defectare. N3 este nivelul cauzei: categoriile de cauze de design.")
table([["Nivel", "Analiza HW", "Analiza SW"],
       ["N1 (efect)", "Radarul frontal (ASIL B)", "Radarul frontal (ASIL B)"],
       ["N2 (mod)", "Semnalul din variantă (ex.: filtrele RC de pe CANH / CANL)", "Funcția din variantă (ex.: sensor_value_plausible() pentru unghiul azimut)"],
       ["N3 (cauză)", "Alegerea componentelor, Dimensionarea componentelor, Definiția semnalului, Schema electrică, Layout PCB", "Cerințele software (SWR), Constante și parametri (#define), Logica de decizie, Tipuri de date și domenii de valori, Interfața (apeluri, valori returnate)"]])
p("O funcție bună are verb, obiect și o condiție măsurabilă, de exemplu „Asigură 120 Ω ±1 % între CANH și CANL la capătul bus-ului”. Funcțiile de la N2 le scrieți pornind de la cerințele afișate (HWR pentru hardware, SWR pentru software). Lista de sugestii din aplicație este comună pentru toate nivelurile: decideți voi unde se potrivește fiecare funcție.")
h3("Exercițiul 3 (pe hârtie)")
p("Indicatorul de alimentare LED1 + R5 nu apare în nicio variantă. Scrieți o funcție pentru el la N2, cu o condiție măsurabilă, și o funcție pentru categoria „Dimensionarea componentelor” de la N3.")
h3("Exercițiul 4 (în aplicație)")
p("Pe F0, în tab-ul HW, scrieți câte o funcție pentru N1, N2 și pentru categoria „Dimensionarea componentelor”. Apoi faceți același lucru în tab-ul SW, cu categoria „Constante și parametri (#define)”. Urmăriți exemplul din „Cum se face”.")
fig("hw_s23c.png", "F0, analiza HW: arborele de structură, funcția categoriei „Dimensionarea componentelor” și placa cu semnalul analizat.")

h2("Rețeaua de defectare (pasul 4)")
p("Defectările sunt negarea funcțiilor: funcția lipsește, este parțială, intermitentă, nedorită sau în afara limitelor. La N1 scrieți efectele (ce simte vehiculul sau ECU-ul ADAS), la N2 modurile de defectare ale elementului, la N3 cauzele. Apoi legați fiecare mod de cel puțin un efect și de cel puțin o cauză. Severitatea se dă pe efect, iar modul preia severitatea maximă a efectelor legate de el.")
p("Pe fiecare cauză alegeți vinovatul: la HW, componenta (cele de pe semnal sunt evidențiate pe placă și în schemă); la SW, cerința, dacă este o cauză din categoria cerințelor. Atenție la nivel: „C2 are toleranță prea mare” este o cauză (N3), nu un mod; modul este ce face filtrul greșit (asimetrie între CANH și CANL).")
h3("Exercițiul 5 (pe hârtie)")
p("Pentru funcția scrisă la exercițiul 3, scrieți un lanț complet: efectul la N1, cu S din tabelul de mai jos, modul de defectare la N2, o cauză la N3, categoria ei și componenta vinovată.")
table([["S", "Criteriu (tabelul D1, rezumat)"],
       ["10", "Afectează siguranța vehiculului sau sănătatea persoanelor"], ["9", "Neconformitate cu reglementările"],
       ["8", "Pierderea unei funcții principale a vehiculului"], ["7", "Degradarea unei funcții principale a vehiculului"],
       ["6", "Pierderea unei funcții secundare a vehiculului"], ["5", "Degradarea unei funcții secundare a vehiculului"],
       ["4", "Aspect, sunet sau vibrații foarte deranjante"], ["3", "Aspect, sunet sau vibrații moderat deranjante"],
       ["2", "Aspect, sunet sau vibrații ușor deranjante"], ["1", "Niciun efect perceptibil"]])
h3("Exercițiul 6 (în aplicație)")
p("Pe F0 construiți rețeaua de defectare din „Cum se face”. HW: efectul „Emisii electromagnetice peste limitele reglementate (EMC)”, S 9; modul „Asimetrie între filtrele de pe CANH și CANL”; cauza „Toleranță prea mare pentru funcție”, la „Dimensionarea componentelor”, vinovat C2. SW: efectul „Un obiect real nu e raportat (detecție ratată, frânare lipsă)”, S 8, la nivel de senzor; modul „Respinge o valoare validă”; cauza „Unitate de măsură greșită a constantei”, la „Constante și parametri (#define)”: SENSOR_MAX scris în grade (60) în loc de zecimi de grad (600), deci obiectele de peste 6° sunt respinse.")
fig("hw_s4c.png", "F0, analiza HW: efect – mod – cauză, cu vinovatul C2 ales pe cauză.")
fig("sw_s4c.png", "F0, analiza SW: lanțul pentru constanta SENSOR_MAX scrisă în altă unitate.")

h2("Analiza riscului (pasul 5)")
p("Pentru fiecare legătură mod – cauză adăugați controalele existente și evaluați riscul:")
ul(["S vine din efectele legate de mod (maximul), din tabelul D1.",
    "O se dă pe cauză, ținând cont de controalele de prevenție (ce împiedică apariția cauzei: calcule, reguli de design, review, componente aprobate, reguli de codare), din tabelul D2. Atenție: la TCA HW ați folosit tabelul P2 al FMEA de proces; în DFMEA se folosește D2, al designului.",
    "D se dă pe controalele de detecție (testul sau analiza care găsește cauza sau modul înainte de lansare), din tabelul D3. D depinde de cât de dovedită este metoda și de cât de devreme se face: un test bun, făcut după lansarea sculelor, are tot D 5–7.",
    "AP (prioritatea de acțiune) rezultă din S, O și D, din tabelul AP: H înseamnă acțiune necesară, M acțiune recomandată, L acțiune opțională. Nu folosim RPN = S × O × D."])
table([["O", "Criteriu (tabelul D2, rezumat)", "D", "Criteriu (tabelul D3, rezumat)"],
       ["10", "Tehnologie nouă, fără experiență și fără prevenție", "10", "Nu există încă procedură de test"],
       ["9", "Prima utilizare în firmă, inovații noi, fără validare", "9", "Testul nu vizează modul de defectare sau cauza"],
       ["8", "Inovații noi într-o aplicație nouă, fără validare", "8", "Metodă de test nouă, nedovedită"],
       ["7", "Design nou pe tehnologie similară, prevenție limitată", "7", "Test dovedit, făcut târziu, pass / fail"],
       ["6", "Design similar, condiții de funcționare schimbate, prevenție parțială", "6", "Test dovedit, făcut târziu, test până la defectare"],
       ["5", "Modificări de detaliu, tehnologie dovedită, lecții învățate aplicate", "5", "Test dovedit, făcut târziu, test de degradare"],
       ["4", "Design aproape identic, respectă standardele și bunele practici", "4", "Test dovedit, făcut la timp, pass / fail"],
       ["3", "Design cunoscut, testat în condiții comparabile", "3", "Test dovedit, făcut la timp, test până la defectare"],
       ["2", "Design matur, expunere lungă în teren", "2", "Test dovedit, făcut la timp, test de degradare"],
       ["1", "Cauza nu este posibilă prin design", "1", "Detectează sigur sau cauza nu poate apărea"]], bold_first_col=False)
p("Tabelul AP (AIAG-VDA), pe benzi de S, O și D:")
AP = {"9-10": {"8-10": "HHHH", "6-7": "HHHH", "4-5": "HHHM", "2-3": "HMLL", "1": "LLLL"},
      "7-8": {"8-10": "HHHH", "6-7": "HHHM", "4-5": "HMMM", "2-3": "MMLL", "1": "LLLL"},
      "4-6": {"8-10": "HHMM", "6-7": "MMML", "4-5": "MLLL", "2-3": "LLLL", "1": "LLLL"},
      "2-3": {"8-10": "MMLL", "6-7": "LLLL", "4-5": "LLLL", "2-3": "LLLL", "1": "LLLL"}}
rows = [["S", "O", "D 7–10", "D 5–6", "D 2–4", "D 1"]]
for sb in ["9-10", "7-8", "4-6", "2-3"]:
    for ob in ["8-10", "6-7", "4-5", "2-3", "1"]:
        rows.append([sb.replace("-", "–"), ob.replace("-", "–")] + list(AP[sb][ob]))
rows.append(["1", "1–10", "L", "L", "L", "L"])
table(rows)
h3("Exercițiul 7 (pe hârtie)")
p("Citiți AP din tabel pentru rândurile de mai jos. Pentru fiecare rând H sau M, spuneți ce ați schimba întâi: prevenția (O) sau detecția (D)?")
table([["Rând", "S", "O", "D", "AP"], ["a", "9", "4", "7", ""], ["b", "9", "2", "4", ""], ["c", "8", "4", "3", ""], ["d", "6", "5", "2", ""]])
h3("Exercițiul 8 (în aplicație)")
p("Pe F0, la pașii 5–6, completați starea inițială. HW: prevenție „Calculul filtrului RC” și „Componente din lista aprobată”, O 4; detecție „Test EMC (emisii și imunitate)”, la validarea designului, după lansarea sculelor, D 7. SW: prevenție „Review de cod față de specificația senzorului”, O 4; detecție „Testare pe cerințe (requirements-based)” și „Teste la limite (boundary values)”, D 3. Ce AP iese în fiecare caz și de ce testul EMC are D 7, deși este o metodă dovedită?")

h2("Optimizarea (pasul 6)")
p("Unde AP este H sau M propuneți acțiuni, în starea revizuită. O acțiune are tip, text, responsabil, termen și stare. Tipul P (prevenție) schimbă designul și scade O; tipul D (detecție) adaugă sau mută un test și scade D. După acțiuni evaluați O nou și D nou; AP-ul revizuit arată dacă riscul a scăzut.")
ul(["Când o acțiune este finalizată, îi alegeți rezultatul: PASS sau FAIL.",
    "FAIL înseamnă că testul a găsit defectul: detecția a funcționat, dar defectul există. Adăugați o acțiune corectivă de design (P) și reevaluați O. Doar un test mai bun nu coboară riscul.",
    "Dacă după revizie riscul rămâne H sau M, propuneți o acțiune suplimentară (P, care scade O, sau D, care scade D) și justificați riscul rezidual. La S 9 cu O 4–5, D 2–4 lasă AP H: practic, numai prevenția coboară riscul."])
h3("Exercițiul 9 (în aplicație)")
p("Pe F0 propuneți acțiunile. HW: [P] „Analiza toleranțelor pe perechea C1 / C2 (C0G, 1 %)” și [D] „Test EMC de pre-conformitate pe prototip, înainte de lansarea sculelor”, cu O nou 2 și D nou 4. SW: [P] „Constante generate automat din specificația senzorului”, cu O nou 2. Ce AP obțineți? Apoi, pe HW, marcați testul de pre-conformitate ca finalizat, cu rezultatul FAIL: ce vă cere aplicația și de ce?")
fig("hw_s56c.png", "F0, analiza HW: starea inițială (AP H) și starea revizuită, cu o acțiune P și una D (AP L).")
fig("sw_s56c.png", "F0, analiza SW: starea inițială (AP M) și acțiunea P care coboară O (AP L).")

h2("Legătura cu testarea")
p("FMEA și testarea lucrează împreună. Controalele de detecție din DFMEA sunt, de fapt, testele din planul de verificare și validare a designului: testul EMC, măsurătorile pe prototip, testele software pe cerințe. Când un test iese FAIL, rezultatul se întoarce în FMEA. Laboratoarele precedente acoperă partea de test a acelorași elemente:")
ul(["TCA HW: aceleași componente, dar cauzele sunt de fabricație (PFMEA), iar întrebarea este dacă AOI, AXI, ICT și FT prind defectul înainte să plece placa.",
    "TCA SW: arată cât de complete sunt testele software folosite ca detecție în DFMEA SW. Un D mic pe „Testare pe cerințe” are sens doar dacă testele acoperă codul și limitele."])
h3("Exercițiul 10 (verbal)")
p("Cauza din demo-ul SW este SENSOR_MAX = 60 în loc de 600. Ce test din laboratorul TCA SW ar fi găsit-o: ce valori ale unghiului alegeți, ce rezultat așteptat și din ce cerință? De ce D este 3 și nu 1?")

h2("Temă pentru acasă (raportul)")
p("Acasă faceți analiza pe varianta voastră, pentru semnalul HW și pentru funcția SW. Pașii sunt cei de la laborator, pe F0:")
ol(["în aplicație apăsați „Începe de la zero”, apoi încărcați varianta voastră (F1–F6), cu numele;",
    "pentru HW și pentru SW: refaceți exercițiile 4, 6, 8 și 9 (o funcție pe element, cel mult 3 moduri, 3 efecte și 2 cauze pe mod);",
    "la fiecare cauză alegeți vinovatul (componenta la HW, cerința la cauzele SW din categoria cerințelor);",
    "pentru AP H sau M propuneți acțiuni cu responsabil și termen și evaluați O și D noi; dacă riscul rămâne H sau M, propuneți acțiunea suplimentară și justificați riscul rezidual;",
    "scrieți concluziile, verificați lista „Verificări” din fiecare analiză, apoi, în tab-ul Raport, apăsați „Trimite raportul”. Prin trimitere sunteți de acord ca datele din raport să fie folosite pentru un studiu de caz; numele vostru nu se folosește nicăieri, doar rezultatele din aplicație. După trimitere apare un chestionar anonim de 5 întrebări despre aplicație și exercițiu; îl puteți completa sau închide cu „Nu acum”. Dacă trimiterea nu este confirmată, descărcați raportul (.html) și păstrați-l."])

h2("Resurse")
out.append("<ul><li><a href='%s'>Aplicația FMEA Lab</a></li>" % APP +
           "<li>AIAG & VDA, FMEA Handbook, ed. 1, 2019 (tabelele D1, D2, D3 și AP).</li>"
           "<li>SAE J1739:2021, Potential Failure Mode and Effects Analysis (FMEA).</li>"
           "<li>IEC 60812:2018, Failure modes and effects analysis (FMEA and FMECA).</li>"
           "<li>ISO 26262-9:2018, Road vehicles — Functional safety — Part 9 (clauza 8, analize de siguranță); IATF 16949:2016.</li>"
           "<li><a href='https://www.microchip.com/en-us/product/MCP2551'>Microchip, MCP2551 High-Speed CAN Transceiver (fișă tehnică)</a></li></ul>")

doc = "<html><head><meta charset='utf-8'></head><body>" + "\n".join(out) + "</body></html>"
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fmea_guide_ro.html"), "w", encoding="utf-8").write(doc)
print(len(doc))
