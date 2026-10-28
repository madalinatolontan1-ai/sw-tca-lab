// Builds the HW TCA lecture deck (RO or EN) from content.<lang>.js
// usage: node build.js ro|en
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/9a6e3071-74e9-40e5-8194-05132a0f8286_2655cfc6-80ca-4a77-bfbd-d76bce1272d9/pptx/scripts/apply_theme.js");

const lang = process.argv[2] || "ro";
const K = require(path.join(__dirname, "content." + lang + ".js"));

const THEME = {
  name: "HW TCA Light",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2A37", lt1: "FFFFFF", dk2: "0B6E69", lt2: "E3F4F1",
    accent1: "0B6E69", accent2: "F2A93B", accent3: "3B82C4", accent4: "E46A5E", accent5: "7C9A3D", accent6: "8A6FD1",
    hlink: "3B82C4", folHlink: "6B7280"
  }
};
const HEX = { text: "1F2A37", muted: "5B6575", teal: "0B6E69", mint: "E3F4F1", mint2: "CDEBE5", amber: "F2A93B", amberT: "FFF4DE", sky: "3B82C4", skyT: "E5F0FA", coral: "E46A5E", coralT: "FCE9E7", ph: "F4F6F8", phLine: "9AA5B1", white: "FFFFFF" };

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = K.meta.title; pres.author = "Mădălina Tolontan"; pres.subject = K.meta.subject;

pres.defineSlideMaster({
  title: "TITLE_ONLY",
  background: { color: HEX.white },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.28, w: 9.0, h: 0.62, fontSize: 26, bold: true, color: HEX.teal, valign: "middle", margin: 0 }, text: "" } },
    { text: { text: K.meta.footer, options: { x: 0.5, y: 5.3, w: 6.5, h: 0.22, fontSize: 9, color: HEX.muted, margin: 0 } } }
  ],
  slideNumber: { x: 9.1, y: 5.28, w: 0.4, h: 0.25, fontSize: 9, color: HEX.muted, align: "right" }
});
pres.defineSlideMaster({ title: "COVER", background: { color: HEX.mint } });

let slideNo = 0;
function base(title) {
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText(title, { placeholder: "title" });
  slideNo++;
  return s;
}
function refs(s, r) {
  if (!r) return;
  s.addText(r, { x: 0.5, y: 5.0, w: 8.5, h: 0.26, fontSize: 10, color: HEX.muted, italic: true, margin: 0, isTextBox: true, objectName: "sources" });
}
function imgBox(s, x, y, w, h, label) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: HEX.ph }, line: { color: HEX.phLine, width: 1, dashType: "dash" }, objectName: "image placeholder" });
  s.addText(label, { x: x + 0.15, y: y + 0.1, w: w - 0.3, h: h - 0.2, fontSize: 12, color: HEX.muted, align: "center", valign: "middle", italic: true, isTextBox: true, objectName: "image placeholder label" });
}
function bullets(s, items, x, y, w, h, size) {
  const arr = items.map((it, i) => {
    const o = { bullet: { indent: 14 }, paraSpaceAfter: 6, breakLine: i < items.length - 1 };
    if (typeof it === "string") return { text: it, options: o };
    return [{ text: it[0], options: Object.assign({}, o, { bold: true, breakLine: false }) }, { text: it[1], options: { breakLine: i < items.length - 1 } }];
  }).flat();
  s.addText(arr, { x, y, w, h, fontSize: size || 15, color: HEX.text, valign: "top", margin: 0.05, isTextBox: true });
}
function card(s, x, y, w, h, head, body, fill, headColor, size) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: fill || HEX.mint }, line: { color: fill || HEX.mint, width: 0.5 } });
  s.addText([{ text: head, options: { bold: true, color: headColor || HEX.teal, fontSize: (size || 14) + 1, breakLine: true } }, { text: body, options: { color: HEX.text, fontSize: size || 14 } }],
    { x: x + 0.12, y: y + 0.08, w: w - 0.24, h: h - 0.16, valign: "top", margin: 0.02, paraSpaceAfter: 3, isTextBox: true });
}
function badge(s, x, y, txt, color) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.42, h: 0.42, fill: { color: color || HEX.amber }, line: { color: color || HEX.amber } });
  s.addText(txt, { x, y, w: 0.42, h: 0.42, fontSize: 13, bold: true, color: HEX.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
}

for (const sl of K.slides) {
  let s;
  switch (sl.type) {
    case "cover": {
      s = pres.addSlide({ masterName: "COVER" }); slideNo++;
      s.addShape(pres.shapes.OVAL, { x: 7.2, y: -1.0, w: 4.2, h: 4.2, fill: { color: HEX.mint2 }, line: { color: HEX.mint2 } });
      s.addShape(pres.shapes.OVAL, { x: 8.3, y: 3.6, w: 2.4, h: 2.4, fill: { color: HEX.amberT }, line: { color: HEX.amberT } });
      s.addText(sl.kicker, { x: 0.6, y: 0.9, w: 6.5, h: 0.4, fontSize: 14, bold: true, color: HEX.amber, charSpacing: 1, margin: 0, isTextBox: true });
      s.addText(sl.title, { x: 0.6, y: 1.35, w: 7.0, h: 1.5, fontSize: 38, bold: true, color: HEX.teal, valign: "top", margin: 0, isTextBox: true });
      s.addText(sl.subtitle, { x: 0.6, y: 2.95, w: 6.6, h: 0.9, fontSize: 17, color: HEX.text, valign: "top", margin: 0, isTextBox: true });
      s.addText(sl.byline, { x: 0.6, y: 4.5, w: 6.6, h: 0.6, fontSize: 12, color: HEX.muted, valign: "top", margin: 0, isTextBox: true });
      break;
    }
    case "agenda": {
      s = base(sl.title);
      sl.items.forEach((it, i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const x = 0.5 + col * 4.6, y = 1.15 + row * 0.92;
        badge(s, x, y + 0.08, String(i + 1), i % 2 ? HEX.sky : HEX.teal);
        s.addText([{ text: it[0], options: { bold: true, fontSize: 15, color: HEX.text, breakLine: true } }, { text: it[1], options: { fontSize: 12, color: HEX.muted } }],
          { x: x + 0.55, y, w: 3.85, h: 0.82, valign: "top", margin: 0.02, isTextBox: true });
      });
      break;
    }
    case "flow": {
      s = base(sl.title);
      const n = sl.steps.length, gap = 0.12, w = (9.0 - gap * (n - 1)) / n;
      sl.steps.forEach((st, i) => {
        const x = 0.5 + i * (w + gap);
        const fill = st[2] === "out" ? HEX.coralT : st[2] === "test" ? HEX.amberT : HEX.mint;
        card(s, x, 1.15, w, 1.55, st[0], st[1], fill, st[2] === "out" ? HEX.coral : HEX.teal, 12);
        if (i < n - 1) s.addText("›", { x: x + w - 0.02, y: 1.7, w: gap + 0.04, h: 0.4, fontSize: 20, color: HEX.muted, align: "center", margin: 0, isTextBox: true });
      });
      bullets(s, sl.bullets, 0.5, 2.95, 5.4, 1.95, 14);
      imgBox(s, 6.1, 2.95, 3.4, 1.95, sl.image);
      break;
    }
    case "textImage": {
      s = base(sl.title);
      if (sl.callout) {
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 1.1, w: 5.4, h: 0.85, rectRadius: 0.1, fill: { color: HEX.amberT }, line: { color: HEX.amberT } });
        s.addText(sl.callout, { x: 0.65, y: 1.13, w: 5.1, h: 0.8, fontSize: 15, italic: true, color: HEX.text, valign: "middle", margin: 0, isTextBox: true });
        bullets(s, sl.bullets, 0.5, 2.1, 5.4, 2.8, 14);
      } else bullets(s, sl.bullets, 0.5, 1.15, 5.4, 3.75, 15);
      imgBox(s, 6.1, 1.15, 3.4, 3.7, sl.image);
      break;
    }
    case "letters": {
      s = base(sl.title);
      sl.groups.forEach((g, gi) => {
        const y = 1.1 + gi * 1.27;
        s.addText(g.name, { x: 0.5, y, w: 1.35, h: 1.15, fontSize: 15, bold: true, color: g.color === "sky" ? HEX.sky : g.color === "amber" ? "B7791F" : HEX.teal, valign: "middle", margin: 0, isTextBox: true });
        const n = g.items.length, gap = 0.1, w = (7.65 - gap * (n - 1)) / n;
        g.items.forEach((it, i) => {
          const fill = g.color === "sky" ? HEX.skyT : g.color === "amber" ? HEX.amberT : HEX.mint;
          s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.85 + i * (w + gap), y, w, h: 1.15, rectRadius: 0.1, fill: { color: fill }, line: { color: fill } });
          s.addText([{ text: it[0], options: { fontSize: 22, bold: true, color: HEX.text, breakLine: true } }, { text: it[1], options: { fontSize: 11, color: HEX.text } }],
            { x: 1.85 + i * (w + gap) + 0.06, y: y + 0.04, w: w - 0.12, h: 1.07, align: "center", valign: "middle", margin: 0, isTextBox: true });
        });
      });
      break;
    }
    case "table": {
      s = base(sl.title);
      const rows = [sl.header.map((h) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.teal }, fontSize: 12, align: "center", valign: "middle" } }))]
        .concat(sl.rows.map((r) => r.map((c, ci) => {
          const v = String(c);
          const fill = v === "●" ? HEX.mint2 : v === "◐" ? HEX.amberT : v === "○" ? HEX.ph : HEX.white;
          return { text: v, options: { fontSize: ci === 0 ? 12 : 13, bold: ci === 0, color: HEX.text, align: ci === 0 ? "left" : "center", valign: "middle", fill: { color: ci === 0 ? HEX.white : fill } } };
        })));
      s.addTable(rows, { x: 0.5, y: 1.1, w: sl.w || 9.0, colW: sl.colW, rowH: sl.rowH || 0.36, border: { type: "solid", pt: 0.75, color: "D5DBE1" }, margin: 0.04 });
      if (sl.legend) s.addText(sl.legend, { x: 0.5, y: sl.legendY || 4.6, w: 9.0, h: 0.32, fontSize: 11, color: HEX.muted, margin: 0, isTextBox: true });
      break;
    }
    case "cards": {
      s = base(sl.title);
      const cols = sl.cols || 3, n = sl.cards.length, rowsN = Math.ceil(n / cols), gap = 0.18;
      const w = (9.0 - gap * (cols - 1)) / cols, hTot = sl.h || 3.7, h = (hTot - gap * (rowsN - 1)) / rowsN;
      sl.cards.forEach((c, i) => {
        const x = 0.5 + (i % cols) * (w + gap), y = (sl.y || 1.12) + Math.floor(i / cols) * (h + gap);
        const fill = c[2] === "amber" ? HEX.amberT : c[2] === "sky" ? HEX.skyT : c[2] === "coral" ? HEX.coralT : HEX.mint;
        card(s, x, y, w, h, c[0], c[1], fill, c[2] === "coral" ? HEX.coral : c[2] === "sky" ? HEX.sky : HEX.teal, sl.size || 13);
      });
      if (sl.image) imgBox(s, sl.image[0], sl.image[1], sl.image[2], sl.image[3], sl.image[4]);
      break;
    }
    case "steps7": {
      s = base(sl.title);
      const n = sl.steps.length, gap = 0.08, w = (9.0 - gap * (n - 1)) / n;
      sl.steps.forEach((st, i) => {
        const x = 0.5 + i * (w + gap);
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.1, w, h: 0.95, rectRadius: 0.1, fill: { color: i < 3 ? HEX.skyT : i < 6 ? HEX.mint : HEX.amberT }, line: { color: "FFFFFF" } });
        s.addText([{ text: String(i + 1), options: { bold: true, fontSize: 16, color: HEX.teal, breakLine: true } }, { text: st, options: { fontSize: 11, color: HEX.text } }],
          { x: x + 0.04, y: 1.12, w: w - 0.08, h: 0.91, align: "center", valign: "middle", margin: 0, isTextBox: true });
      });
      sl.sod.forEach((c, i) => card(s, 0.5 + i * 3.06, 2.25, 2.88, 1.6, c[0], c[1], i === 0 ? HEX.coralT : i === 1 ? HEX.skyT : HEX.amberT, i === 0 ? HEX.coral : i === 1 ? HEX.sky : "B7791F", 13));
      s.addText(sl.note, { x: 0.5, y: 4.0, w: 9.0, h: 0.85, fontSize: 14, color: HEX.text, valign: "top", margin: 0.02, isTextBox: true });
      break;
    }
    case "rpnap": {
      s = base(sl.title);
      s.addText(sl.big, { x: 0.5, y: 1.1, w: 2.7, h: 1.0, fontSize: 54, bold: true, color: HEX.coral, margin: 0, isTextBox: true });
      s.addText(sl.bigLabel, { x: 0.5, y: 2.1, w: 2.8, h: 0.9, fontSize: 13, color: HEX.text, valign: "top", margin: 0, isTextBox: true });
      const rows = [sl.exHeader.map((h) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.teal }, fontSize: 12, align: "center" } }))]
        .concat(sl.ex.map((r) => r.map((c, ci) => ({ text: String(c), options: { fontSize: 13, align: ci === 0 ? "left" : "center", color: HEX.text, bold: ci >= r.length - 2 && ci > 0, fill: { color: ci === r.length - 1 ? (c === "H" ? HEX.coralT : c === "M" ? HEX.amberT : HEX.mint) : HEX.white } } }))));
      s.addTable(rows, { x: 3.5, y: 1.1, w: 6.0, colW: [2.1, 0.6, 0.6, 0.6, 1.0, 1.1], rowH: 0.38, border: { type: "solid", pt: 0.75, color: "D5DBE1" }, margin: 0.04 });
      bullets(s, sl.bullets, 0.5, 3.15, 9.0, 1.75, 14);
      break;
    }
    case "case": {
      s = base(sl.title);
      sl.cards.forEach((c, i) => card(s, 0.5, 1.1 + i * 1.27, 4.9, 1.15, c[0], c[1], i === 1 ? HEX.skyT : i === 2 ? HEX.amberT : HEX.mint, i === 1 ? HEX.sky : HEX.teal, 12));
      imgBox(s, 5.6, 1.1, 3.9, 3.68, sl.image);
      break;
    }
    case "method": {
      s = base(sl.title);
      sl.steps.forEach((st, i) => {
        const y = 1.05 + i * 0.54;
        badge(s, 0.5, y + 0.05, String(i + 1), i === sl.steps.length - 1 ? HEX.coral : HEX.teal);
        s.addText([{ text: st[0] + "  ", options: { bold: true, color: HEX.text } }, { text: st[1], options: { color: HEX.muted } }], { x: 1.05, y, w: 4.95, h: 0.55, fontSize: 13, valign: "middle", margin: 0, isTextBox: true });
      });
      imgBox(s, 6.2, 1.1, 3.3, 3.7, sl.image);
      break;
    }
    case "map": {
      s = base(sl.title);
      const B = sl.boxes; // [label, sub, x, y, w, h, tint]
      B.forEach((b) => {
        const fill = b[6] === "sky" ? HEX.skyT : b[6] === "amber" ? HEX.amberT : b[6] === "coral" ? HEX.coralT : HEX.mint;
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: b[2], y: b[3], w: b[4], h: b[5], rectRadius: 0.1, fill: { color: fill }, line: { color: "C9D3DC", width: 0.75 } });
        s.addText([{ text: b[0], options: { bold: true, fontSize: 12, color: HEX.text, breakLine: true } }, { text: b[1], options: { fontSize: 10, color: HEX.muted } }],
          { x: b[2] + 0.06, y: b[3] + 0.03, w: b[4] - 0.12, h: b[5] - 0.06, align: "center", valign: "middle", margin: 0, isTextBox: true });
      });
      (sl.arrows || []).forEach((a) => s.addShape(pres.shapes.LINE, { x: a[0], y: a[1], w: a[2], h: a[3], line: { color: HEX.muted, width: 1.25, endArrowType: "triangle" }, flipV: !!a[4], flipH: !!a[5] }));
      break;
    }
    case "timeline": {
      s = base(sl.title);
      s.addShape(pres.shapes.LINE, { x: 0.6, y: 2.55, w: 8.8, h: 0, line: { color: HEX.teal, width: 2 } });
      const n = sl.items.length, step = 7.9 / (n - 1);
      sl.items.forEach((it, i) => {
        const x = 1.05 + i * step, up = i % 2 === 0;
        s.addShape(pres.shapes.OVAL, { x: x - 0.09, y: 2.46, w: 0.18, h: 0.18, fill: { color: it[2] === "tca" ? HEX.amber : HEX.teal }, line: { color: HEX.white, width: 1 } });
        s.addText([{ text: it[0], options: { bold: true, fontSize: 14, color: it[2] === "tca" ? "B7791F" : HEX.teal, breakLine: true } }, { text: it[1], options: { fontSize: 10.5, color: HEX.text } }],
          { x: x - 0.62, y: up ? 1.1 : 2.75, w: 1.24, h: 1.3, align: "center", valign: up ? "bottom" : "top", margin: 0, isTextBox: true });
      });
      imgBox(s, 0.5, 4.2, 9.0, 0.7, sl.image);
      break;
    }
    case "stats": {
      s = base(sl.title);
      sl.stats.forEach((st, i) => {
        const x = 0.5 + i * 2.3;
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.1, w: 2.15, h: 1.75, rectRadius: 0.1, fill: { color: i === 0 ? HEX.coralT : HEX.mint }, line: { color: i === 0 ? HEX.coralT : HEX.mint } });
        s.addText([{ text: st[0], options: { fontSize: 28, bold: true, color: i === 0 ? HEX.coral : HEX.teal, breakLine: true } }, { text: st[1], options: { fontSize: 11, color: HEX.text } }],
          { x: x + 0.08, y: 1.15, w: 1.99, h: 1.65, align: "center", valign: "middle", margin: 0, isTextBox: true });
      });
      bullets(s, sl.bullets, 0.5, 3.05, 9.0, 1.85, 13);
      break;
    }
    case "refs": {
      s = base(sl.title);
      const half = Math.ceil(sl.items.length / 2);
      [sl.items.slice(0, half), sl.items.slice(half)].forEach((col, ci) => {
        s.addText(col.map((r, i) => ({ text: r, options: { breakLine: i < col.length - 1, paraSpaceAfter: 4 } })),
          { x: 0.5 + ci * 4.6, y: 1.05, w: 4.4, h: 4.1, fontSize: 10, color: HEX.text, valign: "top", margin: 0, isTextBox: true });
      });
      break;
    }
  }
  if (sl.refs) refs(s, sl.refs);
  if (sl.notes) s.addNotes(sl.notes);
}

(async () => {
  const out = path.join(__dirname, K.meta.file);
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("written", out, slideNo, "slides");
})();
