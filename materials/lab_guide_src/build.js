// Builds the HW TCA lab guide (.docx) in the style of the faculty's lab guides. usage: node build.js ro|en
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, AlignmentType,
  ImageRun, ExternalHyperlink, LevelFormat, HeadingLevel, Footer, PageNumber } = require("docx");
const C = require("./content.js");
const lang = process.argv[2] || "ro";
const L = C[lang];

const BODY = "Times New Roman", HEAD = "Aptos", MONO = "Courier New", BLUE = "0F4761", HBLUE = "156082";
const PAGE_W = 11906, MARGIN = 1134, TEXT_W = PAGE_W - 2 * MARGIN; // A4, 2 cm margins
const INDENT = 709; // first-line indent, as in the model

const para = (text, opts = {}) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent: { firstLine: INDENT }, spacing: { after: 120, line: 276 }, ...opts,
  children: [new TextRun({ text, font: BODY, size: 24 })] });
const thin = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
/* shaded note with a bold question as its first sentence ("Which standard governs ...?") */
const note = (text) => { const k = text.indexOf("? ") + 1;
  return new Paragraph({ spacing: { before: 60, after: 160, line: 276 }, indent: { left: 180, right: 180 },
    shading: { type: ShadingType.CLEAR, fill: "E8F4F2", color: "auto" },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: "0F6E69", space: 8 } },
    children: [new TextRun({ text: text.slice(0, k), bold: true, font: BODY, size: 24 }), new TextRun({ text: text.slice(k), font: BODY, size: 24 })] }); };
const borders = { top: thin, bottom: thin, left: thin, right: thin };

function table(b) {
  const total = b.w.reduce((a, x) => a + x, 0);
  const w = b.w.map((x) => Math.round(x * TEXT_W / total));
  w[w.length - 1] += TEXT_W - w.reduce((a, x) => a + x, 0);
  const size = b.small ? 18 : 20;
  const cell = (txt, i, head) => new TableCell({ width: { size: w[i], type: WidthType.DXA }, borders,
    shading: head ? { fill: "000000", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ alignment: i === 0 || head ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({ text: String(txt), font: BODY, size, bold: head || i === 0, color: head ? "FFFFFF" : "000000" })] })] });
  return new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: w,
    rows: [new TableRow({ tableHeader: true, children: b.head.map((h, i) => cell(h, i, true)) })]
      .concat(b.rows.map((r) => new TableRow({ cantSplit: true, children: r.map((x, i) => cell(x, i, false)) }))) });
}
function box(lines) {
  // formula box, drawn like the code boxes of the model (bordered, monospace, numbered lines)
  const w = [450, TEXT_W - 450];
  return new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: w,
    borders: { top: thin, bottom: thin, left: thin, right: thin, insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" } },
    rows: lines.map((ln, k) => { const NO = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, tb = { top: k === 0 ? thin : NO, bottom: k === lines.length - 1 ? thin : NO };
      return new TableRow({ children: [
      new TableCell({ width: { size: w[0], type: WidthType.DXA }, borders: { ...tb, left: thin, right: NO },
        children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: String(k + 1), font: MONO, size: 18, color: "999999" })] })] }),
      new TableCell({ width: { size: w[1], type: WidthType.DXA }, borders: { ...tb, left: NO, right: thin },
        children: [new Paragraph({ children: [new TextRun({ text: ln, font: MONO, size: 20, bold: true, color: "1A7F37" })] })] })] }); }) });
}
function image(b) {
  const file = path.join(C.IMG, b.f), buf = fs.readFileSync(file);
  const wpx = buf.readUInt32BE(16), hpx = buf.readUInt32BE(20); // PNG header
  const widthPx = Math.round(b.w / 2.54 * 96), heightPx = Math.round(widthPx * hpx / wpx);
  return [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, children: [new ImageRun({ type: "png", data: buf, transformation: { width: widthPx, height: heightPx },
      altText: { title: b.cap, description: b.cap, name: b.f } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: b.cap, font: BODY, size: 20, italics: true })] })];
}

const out = [new Paragraph({ heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER, spacing: { before: 240, after: 360 }, children: [new TextRun({ text: L.title })] })];
const exWord = lang === "ro" ? "Exercițiul " : "Exercise ";
for (const b of L.blocks) {
  if (b.t === "h") out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: b.x })] }));
  else if (b.t === "p") out.push(para(b.x));
  else if (b.t === "note") out.push(note(b.x));
  else if (b.t === "table") { out.push(table(b)); out.push(new Paragraph({ spacing: { after: 120 }, children: [] })); }
  else if (b.t === "box") { out.push(box(b.x)); out.push(new Paragraph({ spacing: { after: 120 }, children: [] })); }
  else if (b.t === "img") out.push(...image(b));
  else if (b.t === "ex") {
    out.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: exWord + b.n })] }));
    b.x.forEach((x) => out.push(para(x)));
    (b.list || []).forEach((x) => out.push(new Paragraph({ numbering: { reference: "abc", level: 0, instance: b.n }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 60 },
      children: [new TextRun({ text: x, font: BODY, size: 24 })] })));
  } else if (b.t === "links") {
    b.items.forEach((it) => out.push(new Paragraph({ spacing: { after: 80 }, indent: { firstLine: INDENT },
      children: [new ExternalHyperlink({ link: it[1], children: [new TextRun({ text: it[0], font: BODY, size: 24, style: "Hyperlink" })] })] })));
  }
}

const doc = new Document({
  creator: "UPT ETC", title: L.title,
  styles: {
    default: { document: { run: { font: BODY, size: 24 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: HEAD, size: 40, color: BLUE }, paragraph: { spacing: { before: 240, after: 360 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: HEAD, size: 28, color: BLUE }, paragraph: { spacing: { before: 360, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: HEAD, size: 24, color: HBLUE }, paragraph: { spacing: { before: 240, after: 80 }, keepNext: true, outlineLevel: 1 } }
    ],
    characterStyles: [{ id: "Hyperlink", name: "Hyperlink", basedOn: "DefaultParagraphFont", run: { color: "467886", underline: { type: "single" } } }]
  },
  numbering: { config: [{ reference: "abc", levels: [{ level: 0, format: LevelFormat.LOWER_LETTER, text: "%1)", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1069, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 16838 }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: BODY, size: 18 })] })] }) },
    children: out
  }]
});
Packer.toBuffer(doc).then((buf) => { const f = path.join(__dirname, L.file); fs.writeFileSync(f, buf); console.log("written", f); });
