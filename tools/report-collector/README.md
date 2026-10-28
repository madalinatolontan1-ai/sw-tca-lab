# Colectarea automată a rapoartelor

Aplicațiile de laborator (HW TCA, SW TCA, FMEA) trimit raportul fiecărui student la un script Google Apps Script. Scriptul:

- salvează raportul HTML în Google Drive, în `Rapoarte laboratoare/<laborator>`;
- adaugă un rând în foaia de calcul, în tab-ul laboratorului: momentul primirii, nume, grupă, variantă, un rezumat și linkul spre raport.

Un student poate trimite raportul de mai multe ori. Toate trimiterile se păstrează, iar ultima contează.

## Configurare (o singură dată, cam 5 minute)

1. Deschide foaia de calcul **Rapoarte laboratoare – colectare automată** din Google Drive.
2. Din meniu alege **Extensii → Apps Script**.
3. Șterge codul din editor, lipește conținutul fișierului [`Code.gs`](Code.gs) și salvează (Ctrl+S).
4. În bara de sus, din lista de funcții, alege **setup** și apasă **Rulează**. Google cere permisiuni pentru Drive și Sheets:
   1. Alege contul tău.
   2. Dacă apare „Google hasn't verified this app”, apasă **Advanced → Go to … (unsafe)**. E scriptul tău, rulat în contul tău.
   3. Apasă **Allow**.

   Rularea creează tab-urile HW TCA, SW TCA și FMEA și folderul din Drive.
5. Alege **Implementează → Implementare nouă**:
   1. La tip, alege **Aplicație web**.
   2. La **Execută ca**, alege **Eu**.
   3. La **Cine are acces**, alege **Oricine**.
   4. Apasă **Implementează** și copiază URL-ul care se termină în `/exec`.
6. Pune URL-ul în `docs/report-config.js`, la `window.LAB_REPORT_ENDPOINT`. Din acel moment, în tab-ul Raport al fiecărei aplicații apare butonul **Trimite raportul**.

Verificare: dacă deschizi URL-ul `/exec` în browser, trebuie să vezi `{"ok":true,...}`.

## Modificări ulterioare ale scriptului

După orice modificare în `Code.gs`:

1. Alege **Implementează → Gestionează implementările**.
2. Apasă pe creion (editare) și alege **Versiune nouă**.
3. Apasă **Implementează**.

URL-ul rămâne același.

## Limitări

- Oricine are URL-ul poate trimite date. URL-ul apare în codul public al paginii, deci numele de pe raport nu e verificat. Pentru laborator e de obicei suficient.
- Rapoartele conțin numele și grupa studenților. Ele ajung în Drive-ul tău și sunt vizibile doar pentru tine, cât timp nu partajezi folderul sau foaia.
