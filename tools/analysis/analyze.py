#!/usr/bin/env python3
"""Pseudonymised analysis of the lab reports (HW TCA, SW TCA, FMEA).

Inputs
  --reports DIR   the "Rapoarte laboratoare" folder downloaded from Drive (any depth; only *.json files are read)
  --sheet XLSX    optional: the "Rapoarte laboratoare" spreadsheet downloaded as .xlsx (tab "Feedback SUS")
  --codes CSV     the private name -> code table; created on the first run, reused and extended later
  --withdrawn TXT optional: one name per line; these students are left out (consent withdrawn)
  --out XLSX      the analysis workbook (codes only, no names)
  --raters XLSX   the rater workbook for the written answers (codes only, random order)

Rules
  * the student is identified by the name in the file name (word order and case do not matter) and the group;
  * reports of PROF / PROFU are the answer key for their lab and variant and are not analysed as students;
  * the demo variants (H0, V0, F0) are left out;
  * the last report of each student and lab is analysed; the number of reports is kept.

Nothing in the outputs except --codes contains a name. Keep the codes file apart from the data.
"""
import argparse
import csv
import json
import math
import random
import re
import secrets
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from scipy import stats

LABS = ["HW-TCA", "SW-TCA", "FMEA"]
KEY_NAMES = {"prof", "profu"}
DEMO = {"H0", "V0", "F0"}
QUIZ_OF = 5
FNAME = re.compile(r"^(HW-TCA|SW-TCA|FMEA)_(.*?)_([HVF]\d+)_(.+)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})$")
SUS_LABS = {"HW TCA": "HW-TCA", "SW TCA": "SW-TCA", "FMEA": "FMEA"}


# ---------------------------------------------------------------- identity and pseudonyms
def norm_name(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return " ".join(sorted(t for t in re.split(r"[^a-z0-9]+", s) if t))


def load_codes(path):
    codes = {}
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                codes[(row["key"], row["group"])] = row["code"]
    return codes


def save_codes(path, codes, names):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "key", "group", "name_as_written"])
        for (key, group), code in sorted(codes.items(), key=lambda x: x[1]):
            w.writerow([code, key, group, names.get((key, group), "")])


def assign_codes(codes, ids):
    """New students get the next free codes in random order, so the codes say nothing about the names."""
    new = [i for i in sorted(ids) if i not in codes]
    random.Random(secrets.randbits(64)).shuffle(new)
    used = {int(c[1:]) for c in codes.values() if re.fullmatch(r"S\d+", c)}
    n = max(used, default=0)
    for i in new:
        n += 1
        codes[i] = "S%03d" % n
    return codes


# ---------------------------------------------------------------- reading the reports
def read_reports(root, withdrawn):
    subs, keys, skipped = [], defaultdict(list), defaultdict(int)
    for p in sorted(root.rglob("*.json")):
        m = FNAME.match(p.stem)
        if not m:
            skipped["file name not recognised"] += 1
            continue
        lab, group, variant, name, day, time = m.groups()
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            skipped["unreadable JSON"] += 1
            continue
        key = norm_name(name)
        rec = {"lab": lab, "group": group, "variant": variant, "name": name.replace("_", " "), "key": key,
               "stamp": day + "_" + time, "data": data, "file": p.name}
        if key.replace(" ", "") in KEY_NAMES:
            keys[(lab, variant)].append(rec)
        elif variant in DEMO:
            skipped["demo variant (H0/V0/F0)"] += 1
        elif key in withdrawn:
            skipped["withdrawn"] += 1
        else:
            subs.append(rec)
    keys = {k: max(v, key=lambda r: r["stamp"]) for k, v in keys.items()}
    return subs, keys, skipped


def last_per_student(subs):
    by = defaultdict(list)
    for r in subs:
        by[(r["key"], r["group"], r["lab"])].append(r)
    out = []
    for v in by.values():
        v.sort(key=lambda r: r["stamp"])
        last = dict(v[-1])
        last["n_reports"] = len(v)
        last["first_stamp"] = v[0]["stamp"]
        out.append(last)
    return out


# ---------------------------------------------------------------- statistics
def cohen_kappa(a, b, weights=None):
    """Cohen's kappa for two raters; weights None (nominal) or 'linear' (ordinal, numeric categories)."""
    pairs = [(x, y) for x, y in zip(a, b) if x not in (None, "") and y not in (None, "")]
    if len(pairs) < 2:
        return None
    cats = sorted({x for p in pairs for x in p}, key=lambda c: (str(type(c)), c))
    k = len(cats)
    if k < 2:
        return 1.0
    ix = {c: i for i, c in enumerate(cats)}
    m = np.zeros((k, k))
    for x, y in pairs:
        m[ix[x], ix[y]] += 1
    m /= m.sum()
    if weights == "linear":
        vals = np.array([float(c) for c in cats])
        span = vals.max() - vals.min()
        w = 1 - np.abs(vals[:, None] - vals[None, :]) / span
    else:
        w = np.eye(k)
    po = (w * m).sum()
    pe = (w * np.outer(m.sum(1), m.sum(0))).sum()
    return None if pe == 1 else float((po - pe) / (1 - pe))


def cronbach_alpha(rows):
    x = np.array(rows, dtype=float)
    if x.shape[0] < 2 or x.shape[1] < 2:
        return None
    item_var = x.var(axis=0, ddof=1).sum()
    total_var = x.sum(axis=1).var(ddof=1)
    return None if total_var == 0 else float(x.shape[1] / (x.shape[1] - 1) * (1 - item_var / total_var))


def wilcoxon(pre, post):
    d = [b - a for a, b in zip(pre, post)]
    nz = [x for x in d if x != 0]
    if len(nz) < 2:
        return None, None, None
    res = stats.wilcoxon(post, pre, zero_method="wilcox", method="approx")
    z = getattr(res, "zstatistic", None)
    if z is None:
        z = stats.norm.isf(res.pvalue / 2) * (1 if sum(nz) > 0 else -1)
    return float(res.statistic), float(res.pvalue), float(abs(z) / math.sqrt(len(nz)))


def mean_sd(v):
    v = [x for x in v if x is not None]
    if not v:
        return None, None
    return float(np.mean(v)), (float(np.std(v, ddof=1)) if len(v) > 1 else None)


# ---------------------------------------------------------------- per lab helpers
def steps_done(state):
    st = (state or {}).get("steps") or []
    return sum(1 for s in st if s.get("status") in ("done", "auto", "na")), len(st)


def quiz_score(q):
    if not isinstance(q, dict) or q.get("skipped") or not isinstance(q.get("score"), (int, float)):
        return None
    return q["score"]


def hw_rows(state):
    return {r["idx"]: r for r in (state or {}).get("rows", [])}


def fmea_pairs(state):
    out = {}
    for side in ("hw", "sw"):
        for p in ((state or {}).get(side) or {}).get("pairs", []):
            k = (side, norm_text(p.get("mode")), norm_text(p.get("cause")))
            out[k] = p
    return out


def norm_text(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))


def match_fmea(st, key):
    """Pairs of (student pair, key pair): same side, mode and cause; if not, same side and cause."""
    kp = fmea_pairs(key)
    by_cause = defaultdict(list)
    for k, v in kp.items():
        by_cause[(k[0], k[2])].append(v)
    out, used = [], set()
    for k, p in fmea_pairs(st).items():
        if k in kp:
            out.append((p, kp[k])); used.add(k)
        elif len(by_cause.get((k[0], k[2]), [])) == 1:
            out.append((p, by_cause[(k[0], k[2])][0]))
    return out, len(kp)


# ---------------------------------------------------------------- workbook helpers
HEAD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="E8EEF6")
NOTE = Font(italic=True, color="555555")


def sheet(wb, title, header, rows, note=None, widths=None):
    ws = wb.create_sheet(title)
    r0 = 1
    if note:
        ws.cell(1, 1, note).font = NOTE
        r0 = 3
    for j, h in enumerate(header, 1):
        c = ws.cell(r0, j, h)
        c.font, c.fill = HEAD, HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                v = None
            c = ws.cell(i, j, round(v, 3) if isinstance(v, float) else v)
            if isinstance(v, str) and len(v) > 40:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = ws.cell(r0 + 1, 1)
    for j, h in enumerate(header, 1):
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(h, max(10, min(18, len(str(h)) + 2)))
    return ws


# ---------------------------------------------------------------- analyses
def an_submissions(last, codes):
    rows = []
    for r in sorted(last, key=lambda r: (r["lab"], codes[(r["key"], r["group"])])):
        d = r["data"]; w = d.get("work") or {}; st = d.get("state") or {}
        q = d.get("quiz") or {}
        done, n = steps_done(st)
        fdone, fn = steps_done((d.get("firstReportView") or {}).get("state"))
        pastes = w.get("pastes") or []
        rows.append([codes[(r["key"], r["group"])], r["lab"], r["variant"], r["n_reports"], r["first_stamp"], r["stamp"],
                     round((w.get("activeSec") or 0) / 60, 1) if w else None, w.get("editCount"), len(pastes),
                     sum(int(p.get("n", 0) or 0) for p in pastes if isinstance(p, dict)),
                     quiz_score(q.get("pre")), quiz_score(q.get("post")),
                     "%d/%d" % (fdone, fn) if fn else None, "%d/%d" % (done, n) if n else None,
                     st.get("checksOpen")])
    return ["Cod", "Lab", "Varianta", "Rapoarte trimise", "Primul raport", "Ultimul raport", "Timp activ (min)", "Modificări",
            "Lipiri", "Caractere lipite", "Test inițial", "Test final", "Pași la prima vedere a raportului", "Pași în raportul final",
            "Verificări deschise (HW)"], rows


def an_quiz(last):
    rows, items = [], []
    for lab in LABS:
        pre, post = [], []
        per_q = defaultdict(lambda: [[], []])
        for r in last:
            if r["lab"] != lab:
                continue
            q = (r["data"].get("quiz") or {})
            a, b = quiz_score(q.get("pre")), quiz_score(q.get("post"))
            for k, which in ((0, "pre"), (1, "post")):
                c = (q.get(which) or {}).get("correct")
                if isinstance(c, list):
                    for i, ok in enumerate(c):
                        per_q[i][k].append(1 if ok else 0)
            if a is not None and b is not None:
                pre.append(a); post.append(b)
        n = len(pre)
        if n:
            mpre, spre = mean_sd(pre); mpost, spost = mean_sd(post)
            W, p, r_eff = wilcoxon(pre, post)
            g_class = (mpost - mpre) / (QUIZ_OF - mpre) if mpre < QUIZ_OF else None
            gi = [(b - a) / (QUIZ_OF - a) for a, b in zip(pre, post) if a < QUIZ_OF]
            rows.append([lab, n, mpre, spre, mpost, spost, float(np.median(pre)), float(np.median(post)), W, p, r_eff,
                         g_class, float(np.mean(gi)) if gi else None])
        else:
            rows.append([lab, 0] + [None] * 11)
        for i in sorted(per_q):
            a, b = per_q[i]
            items.append([lab, "Q%d" % (i + 1), len(a), np.mean(a) if a else None, len(b), np.mean(b) if b else None])
    head = ["Lab", "N (pre și post)", "Media inițial", "AS inițial", "Media final", "AS final", "Mediana inițial", "Mediana final",
            "Wilcoxon W", "p", "r (efect)", "Câștig Hake <g> (clasă)", "Câștig Hake g (media individuală)"]
    return head, rows, ["Lab", "Întrebare", "N inițial", "Proporție corectă inițial", "N final", "Proporție corectă final"], items


def an_sus(path):
    if not path or not path.exists():
        return None
    wb = load_workbook(path, data_only=True)
    if "Feedback SUS" not in wb.sheetnames:
        return None
    ws = wb["Feedback SUS"]
    vals = list(ws.iter_rows(values_only=True))
    head = [str(h or "") for h in vals[0]]
    col = {h: i for i, h in enumerate(head)}
    by = defaultdict(list)
    for row in vals[1:]:
        if not row or row[col["Laborator"]] is None:
            continue
        try:
            a = [int(row[col["SUS%d" % i]]) for i in range(1, 11)]
            extra = [int(row[col[h]]) for h in head if h.startswith(("Q11", "Q12", "Q13"))]
        except (TypeError, ValueError, KeyError):
            continue
        lab = SUS_LABS.get(str(row[col["Laborator"]]), str(row[col["Laborator"]]))
        by[lab].append((a, extra))
    out = []
    for lab in LABS + sorted(set(by) - set(LABS)):
        v = by.get(lab, [])
        if not v:
            out.append([lab, 0] + [None] * 9)
            continue
        rec = [[(x - 1) if i % 2 == 0 else (5 - x) for i, x in enumerate(a)] for a, _ in v]
        sus = [sum(r) * 2.5 for r in rec]
        m, s = mean_sd(sus)
        ex = np.array([e for _, e in v if len(e) == 3], dtype=float)
        exm = [float(ex[:, i].mean()) if len(ex) else None for i in range(3)]
        out.append([lab, len(v), m, s, float(np.median(sus)), min(sus), max(sus), cronbach_alpha(rec)] + exm)
    return ["Lab", "N", "SUS media", "SUS AS", "SUS mediana", "Min", "Max", "Alfa Cronbach (10 itemi)",
            "Q11 proveniența valorilor (medie 1-5)", "Q12 aș face singur analiza", "Q13 util pentru industrie"], out


def an_first_final(last, codes):
    rows = []
    for r in last:
        d = r["data"]; first = (d.get("firstReportView") or {}).get("state"); final = d.get("state")
        if not first or not final:
            continue
        fd, n = steps_done(first); ld, _ = steps_done(final)
        changed, total = None, None
        if r["lab"] == "HW-TCA":
            a, b = hw_rows(first), hw_rows(final)
            total = len(b)
            changed = sum(1 for i in b if any((a.get(i) or {}).get(f) != b[i].get(f) for f in ("s", "o", "ft", "ap")))
        elif r["lab"] == "FMEA":
            a, b = fmea_pairs(first), fmea_pairs(final)
            total = len(b)
            changed = sum(1 for k in b if k not in a or any(a[k].get(f) != b[k].get(f) for f in ("s", "o", "d", "fin")))
        rows.append([codes[(r["key"], r["group"])], r["lab"], r["variant"], fd, ld, n, ld - fd, changed, total,
                     first.get("checksOpen"), final.get("checksOpen")])
    head = ["Cod", "Lab", "Varianta", "Pași la prima vedere", "Pași final", "Pași total", "Pași câștigați după verificări",
            "Rânduri schimbate (S/O/D/AP)", "Rânduri", "Verificări deschise la prima vedere (HW)", "Verificări deschise final (HW)"]
    return head, sorted(rows, key=lambda x: (x[1], x[0]))


def an_agreement(last, keys, codes):
    """Student values against the PROF key of the same variant."""
    pool = defaultdict(lambda: ([], []))
    detail = []
    missing_keys = set()
    for r in last:
        key = keys.get((r["lab"], r["variant"]))
        if not key:
            missing_keys.add((r["lab"], r["variant"]))
            continue
        st, ks = r["data"].get("state") or {}, key["data"].get("state") or {}
        code = codes[(r["key"], r["group"])]
        if r["lab"] == "HW-TCA":
            a, b = hw_rows(st), hw_rows(ks)
            pairs = [(a[i], b[i]) for i in b if i in a]
            fields = (("s", "S"), ("o", "O"), ("ft", "D FT"), ("d", "D"), ("ap", "AP"), ("ap0", "AP fără îmbun."))
        elif r["lab"] == "FMEA":
            pairs, nkey = match_fmea(st, ks)
            fields = (("s", "S"), ("o", "O"), ("d", "D"), ("ap0", "AP inițial"), ("fin", "AP final"))
        else:
            pairs, fields = [], ()
            for k, ex in (st.get("ex") or {}).items():
                kx = (ks.get("ex") or {}).get(k) or {}
                for f in ("stmt", "dec", "mcdc", "req"):
                    v, kv = ex.get(f), kx.get(f)
                    pv = round(100 * v[0] / v[1]) if isinstance(v, list) and len(v) == 2 and v[1] else None
                    pk = round(100 * kv[0] / kv[1]) if isinstance(kv, list) and len(kv) == 2 and kv[1] else None
                    pool[("SW-TCA", "%s %s (%%)" % (k, f))][0].append(pv)
                    pool[("SW-TCA", "%s %s (%%)" % (k, f))][1].append(pk)
            for f in ("stmt", "branch", "mcdc"):
                pool[("SW-TCA", "ASIL: cerința " + f)][0].append((st.get("asil") or {}).get(f) or None)
                pool[("SW-TCA", "ASIL: cerința " + f)][1].append((ks.get("asil") or {}).get(f) or None)
            fc = ((st.get("bug") or {}).get("fixCheck") or {})
            detail.append([code, "SW-TCA", r["variant"], "corectura trece retestul",
                           None if not fc.get("parsed") else int(fc.get("pass", 0) == fc.get("total")), fc.get("spec"), None, None])
            continue
        n_ex = n_pm1 = 0
        for f, label in fields:
            sv = [p[0].get(f) or None for p in pairs]; kv = [p[1].get(f) or None for p in pairs]
            pool[(r["lab"], label)][0].extend(sv); pool[(r["lab"], label)][1].extend(kv)
            both = [(x, y) for x, y in zip(sv, kv) if x is not None and y is not None]
            ex = sum(1 for x, y in both if x == y)
            pm = sum(1 for x, y in both if isinstance(x, (int, float)) and isinstance(y, (int, float)) and abs(x - y) <= 1) if f not in ("ap", "ap0", "fin") else None
            detail.append([code, r["lab"], r["variant"], label, len(both), ex / len(both) if both else None,
                           (pm / len(both)) if (pm is not None and both) else None,
                           (len(pairs) / nkey) if r["lab"] == "FMEA" and nkey else None])
    summary = []
    for (lab, label), (s, k) in sorted(pool.items()):
        both = [(x, y) for x, y in zip(s, k) if x is not None and y is not None]
        if not both:
            summary.append([lab, label, 0, None, None, None, None])
            continue
        num = all(isinstance(x, (int, float)) and isinstance(y, (int, float)) for x, y in both)
        ex = sum(1 for x, y in both if x == y) / len(both)
        pm = sum(1 for x, y in both if abs(x - y) <= 1) / len(both) if num and "%" not in label else None
        xs, ys = [x for x, _ in both], [y for _, y in both]
        kap = cohen_kappa(xs, ys) if "%" not in label else None
        wk = cohen_kappa(xs, ys, "linear") if num and "%" not in label else None
        if label.startswith("AP"):
            order = {"L": 1, "M": 2, "H": 3}
            wk = cohen_kappa([order.get(x) for x in xs], [order.get(y) for y in ys], "linear")
        summary.append([lab, label, len(both), ex, pm, kap, wk])
    head_s = ["Lab", "Câmp", "N perechi", "Acord exact", "Acord ±1", "Kappa Cohen", "Kappa ponderat liniar"]
    head_d = ["Cod", "Lab", "Varianta", "Câmp", "N", "Acord exact", "Acord ±1", "Perechi mod-cauză găsite din cheie (FMEA)"]
    return head_s, summary, head_d, detail, sorted(missing_keys)


def rater_items(last, codes, seed):
    """Every written answer as one item, in random order, with empty columns for three raters."""
    items = []
    for r in last:
        st = r["data"].get("state") or {}
        code = codes[(r["key"], r["group"])]
        add = lambda what, txt: items.append([code, r["lab"], r["variant"], what, str(txt).strip()]) if str(txt or "").strip() else None
        if r["lab"] == "HW-TCA":
            for row in st.get("rows", []):
                ref = "%s %s %s" % (row.get("ref"), "" if row.get("pin") == "–" else row.get("pin"), row.get("mode"))
                add("Justificare FT · %s · test %s, D %s" % (ref, row.get("fttest"), row.get("ft")), row.get("ftj"))
                if row.get("rad"):
                    add("Risc rezidual · %s · AP %s · %s · de ce rămâne" % (ref, row.get("ap"), row.get("rad")), row.get("raw"))
                    add("Risc rezidual · %s · AP %s · %s · ce se face" % (ref, row.get("ap"), row.get("rad")), row.get("ra"))
        elif r["lab"] == "SW-TCA":
            add("Justificarea ASIL / acoperire", st.get("just"))
            b = st.get("bug") or {}
            add("Raport de incident · test %s, linia %s · descriere" % (b.get("test"), b.get("line")), b.get("desc"))
            add("Raport de incident · corectura", b.get("fix"))
            for k, ex in (st.get("ex") or {}).items():
                add("Note %s" % k, ex.get("notes"))
        else:
            for side in ("hw", "sw"):
                for k, rk in ((st.get(side) or {}).get("risk") or {}).items():
                    add("%s · risc %s · acțiune suplimentară" % (side.upper(), k), rk.get("xt"))
                    add("%s · risc %s · risc rezidual" % (side.upper(), k), rk.get("resid"))
        for k, v in (st.get("concl") or {}).items():
            add("Concluzie · " + k, v)
    random.Random(seed).shuffle(items)
    return [["Item %04d" % (i + 1)] + it for i, it in enumerate(items)]


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reports", type=Path, required=True)
    ap.add_argument("--sheet", type=Path)
    ap.add_argument("--codes", type=Path, required=True)
    ap.add_argument("--withdrawn", type=Path)
    ap.add_argument("--out", type=Path, default=Path("analiza_laboratoare.xlsx"))
    ap.add_argument("--raters", type=Path, default=Path("evaluatori_raspunsuri.xlsx"))
    ap.add_argument("--seed", type=int, default=2027, help="order of the rater items")
    a = ap.parse_args(argv)

    withdrawn = set()
    if a.withdrawn and a.withdrawn.exists():
        withdrawn = {norm_name(x) for x in a.withdrawn.read_text(encoding="utf-8").splitlines() if x.strip()}
    subs, keys, skipped = read_reports(a.reports, withdrawn)
    last = last_per_student(subs)
    codes = assign_codes(load_codes(a.codes), {(r["key"], r["group"]) for r in last})
    names = {(r["key"], r["group"]): r["name"] for r in subs}
    save_codes(a.codes, codes, names)

    wb = Workbook(); wb.remove(wb.active)
    info = [["Rapoarte de studenți citite", len(subs)], ["Studenți × laborator (ultimul raport)", len(last)],
            ["Chei PROF găsite", ", ".join("%s %s" % k for k in sorted(keys)) or "niciuna"]] + \
           [["Lăsate deoparte: " + k, v] for k, v in sorted(skipped.items())] + \
           [["Studenți pe laborator: " + lab, sum(1 for r in last if r["lab"] == lab)] for lab in LABS]
    sheet(wb, "Rezumat", ["Ce", "Valoare"], info, note="Date pseudonimizate: fiecare student are un cod (S001…). Tabelul cod–nume e păstrat separat.",
          widths={"Ce": 46, "Valoare": 40})
    h, rows = an_submissions(last, codes)
    sheet(wb, "Trimiteri", h, rows)
    hq, rq, hi, ri = an_quiz(last)
    sheet(wb, "Test inițial-final", hq, rq, note="Doar studenții cu ambele teste (fără „sărit”). Scor din %d. Câștig Hake: (final − inițial) / (%d − inițial)." % (QUIZ_OF, QUIZ_OF))
    sheet(wb, "Test pe întrebări", hi, ri)
    sus = an_sus(a.sheet)
    if sus:
        sheet(wb, "SUS", sus[0], sus[1], note="Itemii impari: scor − 1; pari: 5 − scor; suma × 2,5. Alfa pe itemii recodificați.")
    h, rows = an_first_final(last, codes)
    sheet(wb, "Prima vedere vs final", h, rows, note="Prima vedere = copia luată când studentul deschide prima dată tab-ul Raport, înainte să vadă verificările.")
    hs, rs, hd, rd, mk = an_agreement(last, keys, codes)
    sheet(wb, "Acord cu cheia", hs, rs, note="Cheia = raportul PROF pe aceeași variantă." +
          (" Fără cheie: " + ", ".join("%s %s" % k for k in mk) if mk else ""), widths={"Câmp": 30})
    sheet(wb, "Acord pe student", hd, rd, widths={"Câmp": 30})
    a.out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(a.out)

    items = rater_items(last, codes, a.seed)
    rb = Workbook(); rb.remove(rb.active)
    rub = [["2", "corect și justificat cu referire la tabele, reguli sau schemă"], ["1", "parțial corect sau justificare generică"],
           ["0", "greșit, lipsă sau fără legătură"]]
    sheet(rb, "Instrucțiuni", ["Scor", "Criteriu"], rub, note="Fiecare evaluator completează doar coloana lui (R1, R2 sau R3), fără să vadă scorurile celorlalți.",
          widths={"Criteriu": 70})
    sheet(rb, "Răspunsuri", ["Item", "Cod", "Lab", "Varianta", "Ce", "Text", "R1", "R2", "R3"], items,
          widths={"Ce": 40, "Text": 70, "R1": 6, "R2": 6, "R3": 6})
    a.raters.parent.mkdir(parents=True, exist_ok=True)
    rb.save(a.raters)

    print("students x lab:", len(last), "| keys:", len(keys), "| skipped:", dict(skipped))
    print("analysis ->", a.out); print("raters   ->", a.raters, "(%d items)" % len(items)); print("codes    ->", a.codes, "(PRIVATE)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
