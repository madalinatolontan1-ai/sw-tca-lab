# Builds the HW TCA lab guide as HTML (for import into Google Docs). usage: python3 build.py ro|en
import sys, html
from data import *
from texts import T

lang = sys.argv[1]
t = T[lang]
E = html.escape


def table(header, rows, widths=None, bold_first=False):
    th = "".join('<th bgcolor="#E3F4F1">%s</th>' % E(str(h)) for h in header)
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            v = E(str(c))
            if bold_first and i == 0:
                v = "<b>%s</b>" % v
            tds.append('<td>%s</td>' % v)
        trs.append("<tr>%s</tr>" % "".join(tds))
    return '<table border="1" cellpadding="4" cellspacing="0" width="100%%"><tr>%s</tr>%s</table>' % (th, "".join(trs))


def img(name, width=620, cap=None):
    s = '<p style="text-align:center"><img src="%s%s_%s.png" width="%d"></p>' % (IMG, name, lang, width)
    if cap:
        s += '<p style="text-align:center"><i>%s</i></p>' % E(cap)
    return s


def para(x):
    return "<p>%s</p>" % x


def ul(items, ordered=False):
    tag = "ol" if ordered else "ul"
    return "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % i for i in items), tag)


out = ['<html><head><meta charset="utf-8"></head><body style="font-family:Calibri">']
out.append("<h1>%s</h1>" % E(t["title"]))
out.append(para("<i>%s</i>" % E(t["subtitle"])))

for sec in t["sections"]:
    kind = sec[0]
    if kind == "h2":
        out.append("<h2>%s</h2>" % E(sec[1]))
    elif kind == "h3":
        out.append("<h3>%s</h3>" % E(sec[1]))
    elif kind == "p":
        out.append(para(sec[1]))
    elif kind == "ul":
        out.append(ul(sec[1]))
    elif kind == "ol":
        out.append(ul(sec[1], True))
    elif kind == "img":
        out.append(img(sec[1], sec[2], sec[3] if len(sec) > 3 else None))
    elif kind == "table":
        out.append(table(sec[1], sec[2], bold_first=True))
    elif kind == "components":
        out.append(table(t["compHead"], COMPONENTS[lang], bold_first=True))
    elif kind == "rules":
        out.append(table(t["rulesHead"], RULES))
    elif kind == "severity":
        out.append(table(t["sevHead"], SEVERITY[lang], bold_first=True))
    elif kind == "sevscale":
        out.append(table(t["scaleHead"], [(10 - i, x) for i, x in enumerate(SEV_SCALE[lang])], bold_first=True))
    elif kind == "occ":
        out.append(table(t["scaleHead"], [(10 - i, x) for i, x in enumerate(OCC[lang])], bold_first=True))
    elif kind == "ft":
        out.append(table(t["ftHead"], FT[lang], bold_first=True))
    elif kind == "ap":
        rows = []
        for sb, ob in AP.items():
            for o, v in ob.items():
                rows.append((sb, o) + tuple(v))
        out.append(table(t["apHead"], rows))
    elif kind == "h0":
        out.append(table(t["h0Head"], [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], "%s / %d" % (r[8], r[9]), r[10], r[11]) for r in H0], bold_first=True))
    elif kind == "h0after":
        out.append(table(t["h0AfterHead"], [(r[0], r[1], r[10], r[11], r[12], r[13]) for r in H0], bold_first=True))
    elif kind == "refs":
        out.append(ul([E(x) for x in sec[1]], True))
out.append("</body></html>")
open("guide_%s.html" % lang, "w").write("\n".join(out))
print("ok", len("\n".join(out)))
