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
