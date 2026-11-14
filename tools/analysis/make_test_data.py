#!/usr/bin/env python3
"""Synthetic reports in the collector's format, to try analyze.py before real data exists.
Usage: python3 make_test_data.py OUT_DIR   (writes OUT_DIR/reports/... and OUT_DIR/Rapoarte_laboratoare.xlsx)"""
import json
import random
import sys
from pathlib import Path

from openpyxl import Workbook

R = random.Random(7)
NAMES = ["Popescu Ana", "Ionescu Mihai", "Georgescu Ioana", "Stan Radu", "Dumitru Elena", "Matei Andrei", "Constantin Maria",
         "Marin Vlad", "Tudor Irina", "Barbu Paul", "Nistor Alina", "Ilie Sorin"]
HW = {"H1": [2, 14, 30, 31, 54, 73], "H2": [0, 21, 23, 33, 34, 75]}
FTS = ["FT1", "FT2", "FT4", "FT5", "FT6", "FT7", "none"]
AP = lambda s, o, d: "H" if s >= 9 and o >= 4 else "H" if s * o * d >= 200 else "M" if s * o * d >= 60 else "L"


def quiz(skip=False, base=2):
    if skip:
        return {"skipped": True}
    c = [R.random() < base / 5 for _ in range(5)]
    return {"t": "2026-11-20T10:00:00Z", "sec": R.randint(40, 200), "answers": [R.randint(0, 3) for _ in range(5)], "correct": c, "score": sum(c), "of": 5}


def hw_state(variant, key=False, noise=1.0):
    rows = []
    for i in HW[variant]:
        s = 8 if i % 3 else 6; o = 2; ft = R.choice([1, 5, 10]); d = min(ft, R.choice([1, 3, 5, 10]))
        if not key:
            s += R.choice([0, 0, 0, -2]) if R.random() < noise else 0
            o += R.choice([0, 0, 2]) if R.random() < noise else 0
        ap = AP(s, o, d)
        rows.append({"idx": i, "ref": "C%d" % (i % 4 + 1), "pin": "–", "mode": "Missing", "cls": "E%d" % s, "s": s, "o": o, "aoi": 1, "axi": 3, "ict": 5,
                     "fttest": R.choice(FTS), "ft": ft, "ftj": R.choice(["testul vede efectul", "FT7 comunicația cade", ""]), "nfttest": "", "nft": None,
                     "d": d, "ap": ap, "ap0": ap, "rad": "acc" if ap != "L" else "", "raw": "AOI nu vede" if ap != "L" else "", "ra": "acceptat" if ap != "L" else "", "checks": []})
    steps = [{"n": str(k), "status": R.choice(["done", "done", "part"]), "detail": ""} for k in range(1, 9)]
    return {"variant": variant, "lang": "ro", "aoiBottom": False, "tps": [], "newTests": [], "concl": {"o": "tabel P2", "impr": "TP pe RXD", "lim": ""},
            "rows": rows, "checksOpen": R.randint(0, 3), "steps": steps}


def sw_state(variant):
    ex = {k: {"stmt": [R.randint(8, 12), 12], "dec": [R.randint(4, 6), 6], "mcdc": [R.randint(2, 4), 4], "req": [R.randint(3, 5), 5], "notes": R.choice(["", "BVA la 127"])}
          for k in ("f1", "f2", "f3", "int")}
    return {"variant": variant, "lang": "ro", "asil": {"stmt": "++", "branch": R.choice(["++", "+"]), "mcdc": R.choice(["+", "++"])},
            "bug": {"test": "T6", "line": "54", "fix": "if (rec > CAN_PASSIVE_LIMIT)", "desc": "pragul greșit", "fixCheck": {"parsed": True, "total": 7, "pass": R.choice([5, 7]), "spec": R.random() < 0.7}},
            "just": "ASIL B cere ramuri", "concl": {"cov": "100% instrucțiuni", "lim": ""}, "ex": ex,
            "steps": [{"n": str(k), "status": R.choice(["done", "part"]), "detail": ""} for k in range(1, 6)]}


def fmea_state(variant):
    def side(tag):
        pairs = []
        for m in range(3):
            s = R.choice([7, 8]); o = R.choice([2, 4]); d = R.choice([3, 5, 7])
            pairs.append({"mode": "%s mod %d" % (tag, m), "cause": "cauza %d" % m, "effects": ["efect"], "s": s, "o": o, "d": d,
                          "ap0": AP(s, o, d), "ap1": "", "apX": "", "fin": AP(s, o, d), "failOpen": False})
        risk = {"m%d|c%d" % (m, m): {"xt": R.choice(["", "test nou pe CAN"]), "resid": R.choice(["", "acceptat"])} for m in range(3)}
        return {"fns": [], "fails": [], "links": [], "risk": risk, "pairs": pairs, "checksErr": 0, "checksWarn": 1}
    return {"variant": variant, "lang": "ro", "hw": side("HW"), "sw": side("SW"), "concl": {"dec": "AP H pe TXD", "act": "test", "lim": ""},
            "steps": [{"n": str(k), "status": R.choice(["done", "part"]), "detail": ""} for k in range(1, 8)]}


def write(out, lab, folder, group, variant, name, stamp, state, quizd, first):
    work = {"start": "2026-11-20T10:00:00Z", "activeSec": R.randint(1800, 6000), "edits": {}, "editCount": R.randint(40, 200),
            "pastes": [{"f": "ftj", "n": R.randint(10, 300), "t": "x"} for _ in range(R.randint(0, 3))]}
    data = {"lab": lab, "variant": variant, "receivedAt": "x", "v": 1, "sentAt": "x", "state": state, "work": work,
            "firstReportView": {"t": "x", "state": first}, "quiz": quizd}
    fn = "_".join([lab, group, variant, name.replace(" ", "_"), stamp]) + ".json"
    (out / folder).mkdir(parents=True, exist_ok=True)
    (out / folder / fn).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def main(out):
    out = Path(out); rep = out / "reports"
    for lab, folder, mk, vs in (("HW-TCA", "HW TCA", hw_state, ["H1", "H2"]), ("SW-TCA", "SW TCA", sw_state, ["V1", "V3"]), ("FMEA", "FMEA", fmea_state, ["F1", "F2"])):
        for v in vs:
            st = mk(v, key=True) if lab == "HW-TCA" else mk(v)
            write(rep, lab, folder, "", v, "Profu", "2026-11-14_14-36-08", st, {}, st)
        for k, name in enumerate(NAMES):
            v = vs[k % 2]
            first = mk(v) if lab != "HW-TCA" else hw_state(v, noise=1.0)
            final = mk(v) if lab != "HW-TCA" else hw_state(v, noise=0.4)
            q = {"pre": quiz(skip=(k == 3), base=2), "post": quiz(base=3.6)}
            write(rep, lab, folder, "4.1", v, name, "2026-11-20_11-0%d-00" % (k % 10), first, q, first)
            if k % 4 == 0:  # a second, later report
                write(rep, lab, folder, "4.1", v, name, "2026-11-20_12-0%d-00" % (k % 10), final, q, first)
        write(rep, lab, folder, "4.1", vs[0][0] + "0", "Demo Student", "2026-11-20_09-00-00", mk(vs[0]) if lab != "HW-TCA" else hw_state("H1"), {}, None)
    wb = Workbook(); ws = wb.active; ws.title = "HW TCA"
    s = wb.create_sheet("Feedback SUS")
    s.append(["Data", "Laborator", "Limba", "SUS1", "SUS2", "SUS3", "SUS4", "SUS5", "SUS6", "SUS7", "SUS8", "SUS9", "SUS10", "Scor SUS",
              "Q11 proveniența valorilor", "Q12 aș face singur analiza", "Q13 util pentru industrie", "Comentariu"])
    for lab in ("HW TCA", "SW TCA", "FMEA"):
        for _ in range(10):
            good = R.random() < 0.7
            a = [min(5, max(1, (4 if i % 2 == 0 else 2) + R.choice([-1, 0, 0, 1]) * (1 if good else 2))) for i in range(10)]
            s.append(["2026-11-20", lab, "ro"] + a + [None, R.randint(3, 5), R.randint(2, 5), R.randint(3, 5), ""])
    wb.save(out / "Rapoarte_laboratoare.xlsx")
    print("written to", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "testdata")
