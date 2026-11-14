# Analiza rapoartelor (pseudonimizată)

`analyze.py` citește rapoartele trimise din cele trei aplicații și produce două fișiere Excel fără nume:

- `analiza_laboratoare.xlsx`, cu foile:
  - Rezumat;
  - Trimiteri: timp activ, modificări, lipiri, pași;
  - Test inițial-final: Wilcoxon, r, câștig Hake;
  - Test pe întrebări;
  - SUS: medie, AS, alfa Cronbach, Q11–Q13;
  - Prima vedere vs final;
  - Acord cu cheia: acord exact, ±1, kappa Cohen simplu și ponderat;
  - Acord pe student.
- `evaluatori_raspunsuri.xlsx`: toate răspunsurile scrise (justificări, risc rezidual, incident, concluzii), în ordine aleatoare, cu coloanele R1, R2 și R3 pentru cei trei evaluatori și rubrica 0–2.

Tabelul cod–nume (`--codes`) e singurul fișier cu nume. Se păstrează separat de date și nu se trimite nimănui.

## Pași

1. În Drive, descarcă folderul **Rapoarte laboratoare** (click dreapta → Descărcare) și dezarhivează-l.
2. Descarcă spreadsheet-ul **Rapoarte laboratoare** ca .xlsx (Fișier → Descărcați → Microsoft Excel). Din el se citește doar tab-ul „Feedback SUS”.
3. Opțional, dacă un student își retrage acordul, creează `retrase.txt`, cu un nume pe linie.
4. Rulează:

```
python3 analyze.py --reports "Rapoarte laboratoare" --sheet "Rapoarte laboratoare.xlsx" \
  --codes privat/coduri.csv --withdrawn retrase.txt \
  --out analiza_laboratoare.xlsx --raters evaluatori_raspunsuri.xlsx
```

Necesită Python 3.9+ cu `numpy`, `scipy` și `openpyxl` (`pip install numpy scipy openpyxl`).

## Reguli

- **Identitatea studentului:** numele din numele fișierului plus grupa. Ordinea cuvintelor, majusculele și diacriticele nu contează.
- **Cheia:** rapoartele trimise ca **PROF** sau **Profu** sunt cheia pentru laboratorul și varianta lor și nu intră în analiză.
- **Excluderi:** variantele demo H0, V0 și F0 nu intră în analiză.
- **Mai multe trimiteri:** se analizează ultimul raport al fiecărui student pe fiecare laborator. Numărul de trimiteri apare în foaia „Trimiteri”.
- **Coduri stabile:** la o nouă rulare, cu același `coduri.csv`, codurile vechi rămân aceleași, iar studenții noi primesc coduri noi, în ordine aleatoare.

## Probă fără date reale

```
python3 make_test_data.py testdata
python3 analyze.py --reports testdata/reports --sheet testdata/Rapoarte_laboratoare.xlsx --codes testdata/coduri.csv --out testdata/analiza.xlsx --raters testdata/evaluatori.xlsx
```
