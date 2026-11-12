/* Shared drawing of the CAN module (MCP2551): board (TOP / BOTTOM, with copper tracks) and schematic.
   Used by the HW TCA app and by the HW part of the FMEA app, so both always show the same design.
   Units on the board: 1 = 1 mm. All drawing functions take an options object:
   { top, sel, refs, hl, pin, tps, label, ledColor }
     top   true = TOP view, false = BOTTOM view (mirrored)
     sel   selected part ("U1") or ""
     refs  Set of parts in focus (others are dimmed) or null for no dimming
     hl    nets to highlight (["CANH", "CANL"])
     pin   selected pin ("U1:7") or ""
     tps   test points { NET: true }
     label aria-label of the drawing
     ledColor  colour word under LED1 in the schematic */
(function () {
  "use strict";
  const PARTS = {
    J1:   { x: 4,  y: 15, w: 5.4, h: 21.4, tht: true, pins: 4, vertical: true },
    LED1: { x: 15, y: 6,  w: 4,   h: 2.2 },
    R5:   { x: 31, y: 6,  w: 4,   h: 2.2 },
    C3:   { x: 24, y: 17, w: 4,   h: 2.2 },
    U1:   { x: 37, y: 19, w: 10,  h: 12, soic: true },
    R3:   { x: 51, y: 10, w: 4,   h: 2.2 },
    R1:   { x: 51, y: 20, w: 4,   h: 2.2 },
    C1:   { x: 51, y: 26, w: 4,   h: 2.2 },
    R2:   { x: 51, y: 32, w: 4,   h: 2.2 },
    C2:   { x: 51, y: 38, w: 4,   h: 2.2 },
    R4:   { x: 71, y: 21, w: 4,   h: 2.2 },
    JP1:  { x: 70, y: 6,  w: 7.9, h: 3.4, tht: true, pins: 2, vertical: false },
    J2:   { x: 84, y: 17, w: 5.4, h: 16.3, tht: true, pins: 3, vertical: true }
  };
  /* nets of every pin (schematic of the MCP2551 module, LED1/R5 added) */
  const PIN_NETS = {
    U1: { 1: "TXD", 2: "GND", 3: "VDD", 4: "RXD", 5: null, 6: "CANL", 7: "CANH", 8: "RS" },
    J1: { 1: "VDD", 2: "TXD", 3: "RXD", 4: "GND" },
    J2: { 1: "CANH", 2: "CANL", 3: "GND" }
  };
  const TWO_TERM = {
    C3: ["VDD", "GND"], R3: ["RS", "GND"], R4: ["CANH", "N_TERM"], JP1: ["N_TERM", "CANL"],
    R1: ["CANH", "N_F1"], C1: ["N_F1", "GND"], R2: ["CANL", "N_F2"], C2: ["N_F2", "GND"],
    LED1: ["VDD", "N_LED"], R5: ["N_LED", "GND"]
  };
  const NETS = ["VDD", "GND", "TXD", "RXD", "CANH", "CANL", "RS", "N_TERM", "N_F1", "N_F2", "N_LED", "VREF"];
  const NET_COLOR = { VDD: "#FF6B5A", GND: "#C9D1D9", TXD: "#FFD23F", RXD: "#3EC1D3", RS: "#FF9F1C", CANH: "#F15BB5", CANL: "#4D96FF",
    N_TERM: "#B983FF", N_F1: "#9BE564", N_F2: "#2EC4B6", N_LED: "#FFE66D" };
  const PIN_NAMES = { U1: { 1: "TXD", 2: "VSS", 3: "VDD", 4: "RXD", 5: "VREF", 6: "CANL", 7: "CANH", 8: "RS" }, J1: { 1: "VDD", 2: "TXD", 3: "RXD", 4: "GND" }, J2: { 1: "CAN_H", 2: "CAN_L", 3: "GND" } };
  const VALUES = { R1: "100 Ω", R2: "100 Ω", R3: "4,7 kΩ", R4: "120 Ω", R5: "1 kΩ", C1: "560 pF", C2: "560 pF", C3: "100 nF", U1: "MCP2551", LED1: "LED", JP1: "jumper", J1: "4 pini", J2: "3 pini" };
  const TP_POS = { VDD: [17, 14], GND: [20, 43], TXD: [31, 24.4], RXD: [31, 31.4], RS: [65, 10], CANH: [66, 21.2], N_F1: [64, 19.2], CANL: [65, 32], N_F2: [60, 36.2],
    N_TERM: [79, 14], N_LED: [24, 9] };
  /* every pin: { ref, pin, net } (two-terminal parts: pin 1 = first net, pin 2 = second net; LED1: A / K) */
  const PINS = (() => {
    const out = [];
    Object.keys(PIN_NETS).forEach((ref) => Object.keys(PIN_NETS[ref]).forEach((pin) => { if (PIN_NETS[ref][pin]) out.push({ ref: ref, pin: pin, net: PIN_NETS[ref][pin] }); }));
    Object.keys(TWO_TERM).forEach((ref) => TWO_TERM[ref].forEach((net, i) => out.push({ ref: ref, pin: ref === "LED1" ? (i ? "K" : "A") : String(i + 1), net: net })));
    return out;
  })();
  const pinsOn = (net) => PINS.filter((x) => x.net === net);
  const netsOf = (ref) => PINS.filter((x) => x.ref === ref);
  const CONNECTORS = { J1: true, J2: true };
  /* pad centre in board coordinates (TOP view, mm) */
  function padXY(ref, pin) {
    const p = PARTS[ref];
    if (p.tht) {
      const n = p.pins, i = (ref === "JP1" ? (pin === "1" ? 0 : 1) : +pin - 1), step = 2.54;
      return p.vertical ? [p.x + p.w / 2, p.y + 2 + i * (p.h - 4) / Math.max(1, n - 1)] : [p.x + 1.7 + i * step * 1.4, p.y + p.h / 2];
    }
    if (p.soic) {
      const k = +pin;
      return k <= 4 ? [p.x - 0.7, p.y + 1.95 + (k - 1) * 3] : [p.x + p.w + 0.7, p.y + 1.95 + (8 - k) * 3];
    }
    const first = pin === "1" || pin === "A";
    return [first ? p.x + 0.55 : p.x + p.w - 0.55, p.y + p.h / 2];
  }

  /* copper: tracks on TOP (T) and BOTTOM (B), vias, ground pour on BOTTOM.
     Widths: signals 0.35 mm, CAN pair 0.4 mm, supply 0.6 mm. */
  const TRACKS = [
    { net: "VDD", l: "T", w: 0.6, p: [[6.7, 17], [23.45, 17], [24.55, 18.1]] },
    { net: "VDD", l: "T", w: 0.6, p: [[10.5, 17], [10.5, 9.2], [12.6, 7.1], [15.55, 7.1]] },
    { net: "VDD", l: "T", w: 0.6, p: [[24.55, 18.1], [24.55, 20.4]] },
    { net: "VDD", l: "B", w: 0.6, p: [[24.55, 20.4], [24.55, 25.6], [33.2, 25.6]] },
    { net: "VDD", l: "T", w: 0.6, p: [[33.2, 25.6], [34.55, 26.95], [36.3, 26.95]] },
    { net: "N_LED", l: "T", w: 0.35, p: [[18.45, 7.1], [31.55, 7.1]] },
    { net: "TXD", l: "T", w: 0.35, p: [[6.7, 22.8], [30, 22.8], [31.85, 20.95], [36.3, 20.95]] },
    { net: "RXD", l: "T", w: 0.35, p: [[6.7, 28.6], [30, 28.6], [31.35, 29.95], [36.3, 29.95]] },
    { net: "RS", l: "T", w: 0.35, p: [[47.7, 20.95], [48.9, 20.95], [48.9, 12.6], [50.4, 11.1], [51.55, 11.1]] },
    { net: "CANH", l: "T", w: 0.4, p: [[47.7, 23.95], [78, 23.95], [82.9, 19], [86.7, 19]] },
    { net: "CANH", l: "T", w: 0.4, p: [[50.6, 23.95], [50.6, 22.05], [51.55, 21.1]] },
    { net: "CANH", l: "T", w: 0.4, p: [[70, 23.95], [70, 22.1], [71.55, 22.1]] },
    { net: "CANL", l: "T", w: 0.4, p: [[47.7, 26.95], [48.8, 26.95], [48.8, 29.8], [62, 29.8], [66, 25.8], [80, 25.8], [80.65, 25.15], [86.7, 25.15]] },
    { net: "CANL", l: "T", w: 0.4, p: [[50.6, 29.8], [50.6, 32.15], [51.55, 33.1]] },
    { net: "CANL", l: "B", w: 0.4, p: [[75.26, 7.7], [79.5, 11.9], [79.5, 25.15], [86.7, 25.15]] },
    { net: "N_F1", l: "T", w: 0.35, p: [[54.45, 21.1], [61.6, 21.1]] },
    { net: "N_F1", l: "B", w: 0.35, p: [[61.6, 21.1], [61.6, 25.2], [50.2, 25.2]] },
    { net: "N_F1", l: "T", w: 0.35, p: [[50.2, 25.2], [51.55, 26.55], [51.55, 27.1]] },
    { net: "N_F2", l: "T", w: 0.35, p: [[54.45, 33.1], [54.45, 34.6], [51.55, 37.5], [51.55, 39.1]] },
    { net: "N_TERM", l: "T", w: 0.35, p: [[74.45, 22.1], [74.45, 12], [71.7, 9.25], [71.7, 7.7]] },
    /* ground: short TOP stubs to vias into the BOTTOM pour */
    { net: "GND", l: "T", w: 0.5, p: [[36.3, 23.95], [34.4, 23.95]] },
    { net: "GND", l: "T", w: 0.5, p: [[27.45, 18.1], [34.2, 18.1]] },
    { net: "GND", l: "T", w: 0.5, p: [[34.45, 7.1], [41.5, 7.1]] },
    { net: "GND", l: "T", w: 0.5, p: [[54.45, 11.1], [61.6, 11.1]] },
    { net: "GND", l: "T", w: 0.5, p: [[54.45, 27.1], [61.6, 27.1]] },
    { net: "GND", l: "T", w: 0.5, p: [[54.45, 39.1], [61.6, 39.1]] }
  ];
  const VIAS = [
    { net: "VDD", x: 24.55, y: 20.4 }, { net: "VDD", x: 33.2, y: 25.6 },
    { net: "N_F1", x: 61.6, y: 21.1 }, { net: "N_F1", x: 50.2, y: 25.2 },
    { net: "GND", x: 34.4, y: 23.95 }, { net: "GND", x: 34.2, y: 18.1 }, { net: "GND", x: 41.5, y: 7.1 },
    { net: "GND", x: 61.6, y: 11.1 }, { net: "GND", x: 61.6, y: 27.1 }, { net: "GND", x: 61.6, y: 39.1 }
  ];
  const W = 94, H = 50;

  function pinOf(o) { if (!o.pin) return null; const k = o.pin.split(":"); return PINS.find((q) => q.ref === k[0] && q.pin === k[1]) || null; }
  const poly = (pts, X) => pts.map((q) => X(q[0]).toFixed(2) + "," + q[1]).join(" ");

  function board(o) {
    const top = o.top !== false, sel = o.sel || "", HL = o.hl || [], tps = o.tps || {};
    const X = (x) => (top ? x : W - x);
    const focus = (ref) => !o.refs || o.refs.has(ref);
    let g = '<rect class="pcb" x="0.5" y="0.5" width="' + (W - 1) + '" height="' + (H - 1) + '" rx="2"/>';
    /* copper: the far side first (faint), then the near side; the ground pour belongs to BOTTOM */
    const near = top ? "T" : "B", far = top ? "B" : "T";
    if (!top) g += '<rect class="pour' + (HL.includes("GND") ? " on" : "") + '" x="2" y="2" width="' + (W - 4) + '" height="' + (H - 4) + '" rx="1.5"/>';
    const trk = (layer, cls) => TRACKS.filter((t) => t.l === layer).map((t) => {
      const on = HL.includes(t.net);
      const clear = layer === "B" && !top && t.net !== "GND" ? '<polyline class="clear" stroke-width="' + (t.w + 1) + '" points="' + poly(t.p, X) + '"/>' : "";
      return clear + '<polyline class="trk ' + cls + (on ? " on" : "") + '" data-tnet="' + t.net + '" stroke-width="' + t.w + '"' + (on ? ' style="stroke:' + (NET_COLOR[t.net] || "#fff") + '"' : "") + ' points="' + poly(t.p, X) + '"/>';
    }).join("");
    g += '<g class="cu far">' + trk(far, "far") + "</g>";
    if (!top) g += VIAS.filter((v) => v.net !== "GND").map((v) => '<circle class="clear" cx="' + X(v.x) + '" cy="' + v.y + '" r="1.1"/>').join("");
    g += '<g class="cu near">' + trk(near, "near") + "</g>";
    g += VIAS.map((v) => { const on = HL.includes(v.net);
      return '<circle class="via' + (on ? " on" : "") + '" cx="' + X(v.x) + '" cy="' + v.y + '" r="0.6"' + (on ? ' style="stroke:' + (NET_COLOR[v.net] || "#fff") + '"' : "") + '/><circle class="vhole" cx="' + X(v.x) + '" cy="' + v.y + '" r="0.25"/>'; }).join("");
    g += '<text class="silk" text-anchor="' + (top ? "end" : "start") + '" x="' + (top ? W - 3 : 3) + '" y="' + (H - 3) + '">MCP2551 CAN · ' + (top ? "TOP" : "BOTTOM") + "</text>";
    Object.keys(PARTS).forEach((ref) => {
      const p = PARTS[ref];
      const x = top ? p.x : W - p.x - p.w;
      const linked = HL.length && ref !== sel && PINS.some((q) => q.ref === ref && HL.includes(q.net));
      const cls = "comp" + (ref === sel ? " sel" : "") + (linked ? " linked" : "") + (focus(ref) || linked || ref === sel ? "" : " dim");
      let inner = "";
      if (p.tht) {
        const n = p.pins; const step = 2.54;
        for (let i = 0; i < n; i++) {
          const cx = p.vertical ? x + p.w / 2 : x + 1.7 + i * step * 1.4;
          const cy = p.vertical ? p.y + 2 + i * (p.h - 4) / Math.max(1, n - 1) : p.y + p.h / 2;
          inner += '<circle class="tht" cx="' + cx + '" cy="' + cy + '" r="1.05"/><circle class="hole" cx="' + cx + '" cy="' + cy + '" r="0.45"/>';
        }
        if (top) inner = '<rect class="body" x="' + x + '" y="' + p.y + '" width="' + p.w + '" height="' + p.h + '" rx="0.6" opacity="0.92"/>' + inner;
        inner += '<rect class="outline" x="' + (x - 0.6) + '" y="' + (p.y - 0.6) + '" width="' + (p.w + 1.2) + '" height="' + (p.h + 1.2) + '" rx="0.8"/>';
      } else if (top) {
        if (p.soic) {
          for (let i = 0; i < 4; i++) {
            const py = p.y + 1.5 + i * 3;
            inner += '<rect class="pad" x="' + (x - 1.8) + '" y="' + py + '" width="2.2" height="0.9"/><rect class="pad" x="' + (x + p.w - 0.4) + '" y="' + py + '" width="2.2" height="0.9"/>';
          }
          inner += '<rect class="body" x="' + x + '" y="' + p.y + '" width="' + p.w + '" height="' + p.h + '" rx="0.4"/><circle cx="' + (x + 1.3) + '" cy="' + (p.y + 1.3) + '" r="0.5" fill="var(--silk)"/>';
        } else {
          inner += '<rect class="pad" x="' + x + '" y="' + p.y + '" width="1.1" height="' + p.h + '"/><rect class="pad" x="' + (x + p.w - 1.1) + '" y="' + p.y + '" width="1.1" height="' + p.h + '"/>' +
            '<rect class="body" x="' + (x + 1.1) + '" y="' + p.y + '" width="' + (p.w - 2.2) + '" height="' + p.h + '"/>';
        }
        inner += '<rect class="outline" x="' + (x - 2) + '" y="' + (p.y - 0.6) + '" width="' + (p.w + 4) + '" height="' + (p.h + 1.2) + '" rx="0.8"/>';
      } else {
        /* SMD part seen from BOTTOM: it sits on the other side, show its place so it can still be clicked */
        inner += '<rect class="ghost" x="' + x + '" y="' + p.y + '" width="' + p.w + '" height="' + p.h + '" rx="0.4"/>' +
          '<rect class="outline" x="' + (x - 2) + '" y="' + (p.y - 0.6) + '" width="' + (p.w + 4) + '" height="' + (p.h + 1.2) + '" rx="0.8"/>';
      }
      let lx, ly, anchor = "start";
      if (p.soic) { lx = x + p.w / 2; ly = p.y + p.h / 2 + 1; anchor = "middle"; }
      else if (p.tht) { lx = x + p.w / 2; ly = p.y - 1.4; anchor = "middle"; }
      else { lx = x + p.w + 0.8; ly = p.y + p.h / 2 + 1.05; }
      const hx = p.soic ? x - 2.5 : x - 2.2, hw = p.soic ? p.w + 5 : p.w + (p.tht ? 4.4 : 9);
      const hy = p.tht ? p.y - 4.4 : p.y - 1.2, hh = p.tht ? p.h + 5.6 : p.h + 2.4;
      const hit = '<rect class="hit" x="' + hx + '" y="' + hy + '" width="' + hw + '" height="' + hh + '"/>';
      g += '<g class="' + cls + '" data-ref="' + ref + '" tabindex="0" role="button" aria-label="' + ref + '">' + hit + inner +
        '<text class="silk" text-anchor="' + anchor + '" x="' + lx + '" y="' + ly + '">' + ref + "</text></g>";
    });
    Object.keys(TP_POS).forEach((n) => {
      if (!tps[n]) return;
      const pt = TP_POS[n]; const x = X(pt[0]);
      g += '<g class="tpm"><circle cx="' + x + '" cy="' + pt[1] + '" r="1.2"/><text text-anchor="middle" x="' + x + '" y="' + (pt[1] + 3.6) + '">' + n + "</text></g>";
    });
    const own = pinOf(o);
    HL.forEach((net) => {
      const col = NET_COLOR[net] || "#fff";
      g += pinsOn(net).map((q) => { const pt = padXY(q.ref, q.pin); return '<circle class="pin-on" cx="' + X(pt[0]) + '" cy="' + pt[1] + '" r="0.85" fill="' + col + '"/>'; }).join("");
      if (sel && own && own.net === net) {
        const pt = padXY(own.ref, own.pin), pp = PARTS[own.ref];
        let left = pt[0] < pp.x + pp.w / 2; if (!top) left = !left;
        const dy = pp.tht && pp.vertical ? 0.8 : (pp.soic ? 0.8 : -1.3);
        const off = pp.soic || (pp.tht && pp.vertical) ? 4.3 : 1.3;
        if (left && X(pt[0]) - off < 9) left = false; else if (!left && X(pt[0]) + off > W - 9) left = true;
        g += '<text class="netlbl" fill="' + col + '" text-anchor="' + (left ? "end" : "start") + '" x="' + (X(pt[0]) + (left ? -off : off)) + '" y="' + (pt[1] + dy) + '">' + net + "</text>";
      }
    });
    PINS.forEach((q) => {
      const pt = padXY(q.ref, q.pin), pp = PARTS[q.ref];
      if (!top && !pp.tht) return;  /* SMD pads are on the other side */
      const on = o.pin === q.ref + ":" + q.pin;
      g += '<circle class="padhit' + (on ? " on" : "") + (q.ref === sel ? " own" : "") + '" data-pin="' + q.ref + ":" + q.pin + '" cx="' + X(pt[0]) + '" cy="' + pt[1] + '" r="1.25"><title>' + q.ref + " " + q.pin + " · " + q.net + "</title></circle>";
      if (q.ref === sel) {
        let left = pt[0] < pp.x + pp.w / 2; if (!top) left = !left;
        const vert = pp.tht && pp.vertical;
        g += '<text class="pinno" text-anchor="middle" x="' + (X(pt[0]) + (vert ? (left ? -2.6 : 2.6) : 0)) + '" y="' + (pt[1] + (vert ? 0.8 : (pp.soic ? 0.8 : 3.4))) + '"' + (pp.soic ? ' dx="' + (left ? -2.4 : 2.4) + '"' : "") + ">" + q.pin + "</text>";
      }
    });
    return '<svg class="board' + (HL.length ? " hl" : "") + '" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + (o.label || "PCB") + '">' + g + "</svg>";
  }

  /* simplified schematic, for reading nets and test points */
  function sch(o) {
    const sel = o.sel || "", HL = o.hl || [], tps = o.tps || {};
    const focus = (ref) => !o.refs || o.refs.has(ref);
    let g = "";
    const ln = (x1, y1, x2, y2) => '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '"/>';
    const dot = (x, y) => '<circle class="jn" cx="' + x + '" cy="' + y + '" r="3"/>';
    const txt = (x, y, s, cls, anchor) => '<text class="' + (cls || "lbl") + '" x="' + x + '" y="' + y + '"' + (anchor ? ' text-anchor="' + anchor + '"' : "") + ">" + s + "</text>";
    const gnd = (x, y) => '<g class="gnd">' + ln(x, y, x, y + 8) + ln(x - 9, y + 8, x + 9, y + 8) + ln(x - 6, y + 12, x + 6, y + 12) + ln(x - 3, y + 16, x + 3, y + 16) + "</g>";
    const comp = (ref, inner) => { const lk = HL.length && ref !== sel && PINS.some((q) => q.ref === ref && HL.includes(q.net));
      return '<g class="comp' + (ref === sel ? " sel" : "") + (lk ? " linked" : "") + (focus(ref) || lk || ref === sel ? "" : " dim") + '" data-ref="' + ref + '" tabindex="0" role="button" aria-label="' + ref + '">' + inner + "</g>"; };
    const res = (ref, val, x, y1, y2) => comp(ref, ln(x, y1, x, y1 + 10) + '<rect class="body" x="' + (x - 6) + '" y="' + (y1 + 10) + '" width="12" height="' + (y2 - y1 - 20) + '"/>' + ln(x, y2 - 10, x, y2) +
      txt(x + 11, (y1 + y2) / 2 - 2, ref, "ref") + txt(x + 11, (y1 + y2) / 2 + 11, val, "val"));
    const cap = (ref, val, x, y1, y2) => { const m = (y1 + y2) / 2; return comp(ref, ln(x, y1, x, m - 4) + '<line class="plate" x1="' + (x - 10) + '" y1="' + (m - 4) + '" x2="' + (x + 10) + '" y2="' + (m - 4) + '"/><line class="plate" x1="' + (x - 10) + '" y1="' + (m + 4) + '" x2="' + (x + 10) + '" y2="' + (m + 4) + '"/>' + ln(x, m + 4, x, y2) +
      txt(x + 13, m - 2, ref, "ref") + txt(x + 13, m + 11, val, "val")); };
    const WIRES = {
      VDD: [[70, 130, 95, 130], [95, 130, 95, 40], [95, 40, 320, 40], [320, 40, 320, 120], [140, 40, 140, 52], [200, 40, 200, 56]],
      TXD: [[70, 170, 260, 170]], RXD: [[70, 210, 260, 210]], RS: [[225, 250, 260, 250]],
      GND: [[70, 250, 82, 250], [82, 250, 82, 262], [300, 300, 300, 318], [640, 315, 652, 315], [652, 315, 652, 330]],
      CANH: [[380, 170, 640, 170], [430, 170, 430, 180], [560, 170, 560, 180]], CANL: [[380, 280, 640, 280], [480, 280, 480, 290], [560, 256, 560, 280]]
    };
    const SPOTS = { N_F1: [430, 215], N_F2: [480, 325], N_TERM: [560, 222], N_LED: [140, 84] };
    g += '<g class="wire">';
    Object.keys(WIRES).forEach((net) => {
      const on = HL.includes(net);
      g += WIRES[net].map((w) => '<line' + (on ? ' class="on" style="stroke:' + (net === "GND" ? "var(--ink)" : NET_COLOR[net]) + '"' : "") + ' x1="' + w[0] + '" y1="' + w[1] + '" x2="' + w[2] + '" y2="' + w[3] + '"/>').join("");
    });
    g += "</g>";
    g += dot(140, 40) + dot(200, 40) + dot(430, 170) + dot(560, 170) + dot(480, 280) + dot(560, 280);
    const gOn = HL.includes("GND");
    const gndH = (x, y) => gnd(x, y).replace('<g class="gnd">', '<g class="gnd' + (gOn ? " on" : "") + '">');
    g += gndH(82, 262) + gndH(300, 318) + gndH(652, 330);
    g += comp("J1", '<rect class="body" x="20" y="110" width="50" height="160" rx="3"/>' + txt(45, 102, "J1", "ref", "middle") +
      [["1", "VDD", 130], ["2", "TXD", 170], ["3", "RXD", 210], ["4", "GND", 250]].map((p) => txt(28, p[2] + 4, p[0], "pin") + txt(64, p[2] + 4, p[1], "pinr", "end")).join(""));
    g += comp("J2", '<rect class="body" x="640" y="150" width="50" height="185" rx="3"/>' + txt(665, 142, "J2", "ref", "middle") +
      [["1", "CAN_H", 170], ["2", "CAN_L", 280], ["3", "GND", 315]].map((p) => txt(683, p[2] + 4, p[0], "pin", "end") + txt(645, p[2] + 4, p[1], "pinl")).join(""));
    g += comp("U1", '<rect class="body" x="260" y="120" width="120" height="180" rx="3"/>' + txt(320, 205, "U1", "ref", "middle") + txt(320, 220, "MCP2551", "val", "middle") +
      txt(266, 174, "1 TXD", "pinl") + txt(266, 214, "4 RXD", "pinl") + txt(266, 254, "8 RS", "pinl") + txt(320, 136, "3 VDD", "pin", "middle") +
      txt(374, 174, "CANH 7", "pinr", "end") + txt(374, 284, "CANL 6", "pinr", "end") + txt(300, 294, "2 VSS", "pin", "middle") + txt(352, 294, "5 VREF", "pin", "middle") +
      ln(352, 300, 352, 312) + '<path class="nc" d="M346,306 l12,12 M358,306 l-12,12"/>');
    g += comp("LED1", ln(140, 52, 140, 60) + '<path class="body" d="M131,60 h18 l-9,14 z"/>' + ln(131, 74, 149, 74) + ln(140, 74, 140, 84) +
      '<path class="arrow" d="M151,62 l9,-6 M155,56 l5,0 l0,5 M153,70 l9,-6 M157,64 l5,0 l0,5"/>' + txt(112, 70, "LED1", "ref", "end") + txt(112, 82, o.ledColor || "verde", "val", "end"));
    g += res("R5", "1 kΩ", 140, 84, 140);
    g += gndH(140, 140);
    g += cap("C3", "100 nF", 200, 56, 104) + gndH(200, 104);
    g += res("R3", "4,7 kΩ", 225, 250, 300) + gndH(225, 300);
    g += res("R1", "100 Ω", 430, 180, 215) + cap("C1", "560 pF", 430, 215, 237) + gndH(430, 237);
    g += res("R2", "100 Ω", 480, 290, 325) + cap("C2", "560 pF", 480, 325, 347) + gndH(480, 347);
    g += res("R4", "120 Ω", 560, 180, 222);
    g += comp("JP1", ln(560, 222, 560, 230) + '<circle class="pinc" cx="560" cy="234" r="4"/><circle class="pinc" cx="560" cy="252" r="4"/><rect class="jbar" x="553" y="229" width="14" height="28" rx="3"/>' + ln(560, 256, 560, 280) + txt(574, 247, "JP1", "ref"));
    g += txt(210, 34, "VDD", "net") + txt(160, 165, "TXD", "net") + txt(160, 205, "RXD", "net") + txt(232, 245, "RS", "net") +
      txt(600, 165, "CANH", "net") + txt(600, 275, "CANL", "net") + txt(422, 219, "N_F1", "netsm", "end") + txt(472, 329, "N_F2", "netsm", "end") + txt(552, 226, "N_TERM", "netsm", "end") + txt(146, 90, "N_LED", "netsm");
    Object.keys(SPOTS).forEach((net) => { if (!HL.includes(net)) return; const p = SPOTS[net]; g += '<circle class="nethl" cx="' + p[0] + '" cy="' + p[1] + '" r="7" style="stroke:' + NET_COLOR[net] + '"/>'; });
    const SCH_PIN = {
      "J1:1": [70, 130], "J1:2": [70, 170], "J1:3": [70, 210], "J1:4": [70, 250], "J2:1": [640, 170], "J2:2": [640, 280], "J2:3": [640, 315],
      "U1:1": [260, 170], "U1:4": [260, 210], "U1:8": [260, 250], "U1:3": [320, 120], "U1:7": [380, 170], "U1:6": [380, 280], "U1:2": [300, 300],
      "LED1:A": [140, 52], "LED1:K": [140, 84], "R5:1": [140, 84], "R5:2": [140, 140], "C3:1": [200, 56], "C3:2": [200, 104], "R3:1": [225, 250], "R3:2": [225, 300],
      "R1:1": [430, 180], "R1:2": [430, 215], "C1:1": [430, 215], "C1:2": [430, 237], "R2:1": [480, 290], "R2:2": [480, 325], "C2:1": [480, 325], "C2:2": [480, 347],
      "R4:1": [560, 180], "R4:2": [560, 222], "JP1:1": [560, 222], "JP1:2": [560, 280]
    };
    Object.keys(SCH_PIN).sort((a, b) => (a.split(":")[0] === sel) - (b.split(":")[0] === sel)).forEach((k) => {
      const pt = SCH_PIN[k], ref = k.split(":")[0];
      g += '<circle class="pinhit' + (o.pin === k ? " on" : "") + (ref === sel ? " own" : "") + '" data-pin="' + k + '" cx="' + pt[0] + '" cy="' + pt[1] + '" r="6"><title>' + k.replace(":", " ") + "</title></circle>";
    });
    const TP_SCH = { VDD: [260, 40], TXD: [120, 170], RXD: [120, 210], RS: [245, 250], CANH: [520, 170], CANL: [520, 280], GND: [300, 318], N_F1: [430, 215], N_F2: [480, 325], N_TERM: [560, 222], N_LED: [140, 84] };
    Object.keys(TP_SCH).forEach((n) => { if (!tps[n]) return; const p = TP_SCH[n]; g += '<g class="tps"><circle cx="' + p[0] + '" cy="' + p[1] + '" r="5"/><text x="' + (p[0] + 7) + '" y="' + (p[1] - 6) + '">TP</text></g>'; });
    return '<svg class="sch' + (HL.length ? " hl" : "") + '" viewBox="0 0 700 372" role="img" aria-label="' + (o.label || "schematic") + '">' + g + "</svg>";
  }

  window.PCB = { PARTS: PARTS, PIN_NETS: PIN_NETS, TWO_TERM: TWO_TERM, NETS: NETS, NET_COLOR: NET_COLOR, PIN_NAMES: PIN_NAMES, VALUES: VALUES,
    TP_POS: TP_POS, PINS: PINS, pinsOn: pinsOn, netsOf: netsOf, CONNECTORS: CONNECTORS, padXY: padXY, TRACKS: TRACKS, VIAS: VIAS, board: board, sch: sch };
})();
