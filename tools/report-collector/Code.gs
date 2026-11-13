/**
 * Lab report collector (Google Apps Script, bound to the "Rapoarte laboratoare" spreadsheet).
 *
 * The lab apps (HW TCA, SW TCA, FMEA) POST each finished report here. For every report the script
 *   1. saves the HTML report in Drive, in "Rapoarte laboratoare/<lab>",
 *   2. saves the structured data of the report (values, work data, first copy of the analysis) as a JSON file next to it,
 *   3. appends a row to the sheet tab of that lab (time, name, group, variant, summary, links, active time, pastes).
 * After a report, the apps may send an anonymous feedback form (kind: "feedback"): no name, group or variant;
 * it goes to the "Feedback" tab with the date only, at a random row, so it cannot be matched to a report.
 *
 * Setup: see README.md in this folder.
 */
const LABS = { "HW-TCA": "HW TCA", "SW-TCA": "SW TCA", "FMEA": "FMEA" };
const ROOT_FOLDER = "Rapoarte laboratoare";
const TZ = "Europe/Bucharest";
const MAX_HTML = 3 * 1024 * 1024;
/* the collection spreadsheet; used when the script is not opened from the sheet (Extensions → Apps Script) */
const SHEET_ID = "1eMkpwfwd6qLFUVOAyjTyhx1PH0IPEYksB_Z8L51ah3k";
const HEADER = ["Primit", "Nume", "Grupa", "Varianta", "Rezumat", "Raport (Drive)", "Limba", "Date (JSON)", "Timp activ (min)", "Modificări", "Lipiri"];
const MAX_JSON = 2 * 1024 * 1024;

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    const lab = String(d.lab || "");
    if (!LABS[lab]) return out_({ ok: false, error: "unknown lab" });
    if (d.kind === "feedback") return feedback_(lab, d);
    const name = clean_(d.name, 80), group = clean_(d.group, 20), variant = clean_(d.variant, 10);
    if (!name || !variant) return out_({ ok: false, error: "name and variant are required" });
    const html = String(d.html || "");
    if (!html || html.length > MAX_HTML) return out_({ ok: false, error: "report missing or too large" });

    const now = new Date();
    const stamp = Utilities.formatDate(now, TZ, "yyyy-MM-dd_HH-mm-ss");
    const fileName = [lab, group, variant, name, stamp].join("_").replace(/[^\w\-.]+/g, "_") + ".html";
    const file = labFolder_(lab).createFile(fileName, html, MimeType.HTML);

    let dataUrl = "", activeMin = "", edits = "", pastes = "";
    if (d.data && typeof d.data === "object") {
      const json = JSON.stringify(Object.assign({ lab: lab, variant: variant, receivedAt: now.toISOString() }, d.data));
      if (json.length <= MAX_JSON) dataUrl = labFolder_(lab).createFile(fileName.replace(/\.html$/, ".json"), json, MimeType.PLAIN_TEXT).getUrl();
      const w = d.data.work || {};
      if (typeof w.activeSec === "number") activeMin = Math.round(w.activeSec / 6) / 10;
      if (typeof w.editCount === "number") edits = w.editCount;
      if (Array.isArray(w.pastes)) pastes = w.pastes.length;
    }
    sheetFor_(lab).appendRow([now, safe_(name), safe_(group), safe_(variant), safe_(clean_(d.summary, 500)), file.getUrl(), clean_(d.lang, 5), dataUrl, activeMin, edits, pastes]);
    return out_({ ok: true, received: Utilities.formatDate(now, TZ, "dd.MM.yyyy HH:mm") });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/* Health check: opening the web app URL in a browser shows {"ok":true,...,"version":...}.
   The version tells which code the deployment runs. */
const VERSION = "2026-11-14";
function doGet() {
  return out_({ ok: true, service: "lab-reports", version: VERSION, labs: Object.keys(LABS) });
}

/* Run from the editor (Run → testPost): writes a test row and a test report, without the web app. */
function testPost() {
  const r = doPost({ postData: { contents: JSON.stringify({ lab: "HW-TCA", lang: "ro", name: "TEST", group: "0", variant: "H0", summary: "test din editor", html: "<p>test</p>",
    data: { v: 1, state: { test: true }, work: { start: new Date().toISOString(), activeSec: 600, editCount: 3, edits: {}, pastes: [] }, firstReportView: null } }) } });
  Logger.log(r.getContent());
}

/* Anonymous feedback. Only the date is stored and the row lands at a random position, so the order of the rows
   says nothing about who sent what.
   qv 2 (from 14 Nov 2026): 13 answers 1-5 = the 10 System Usability Scale items + 3 lab items, tab "Feedback SUS",
   with the SUS score (0-100: odd items score-1, even items 5-score, sum × 2.5).
   qv 1 (older pages still open in a browser): 5 answers, tab "Feedback". */
const FB_HEADER = ["Data", "Laborator", "Limba", "Q1 funcții / nevoi", "Q2 ușor de folosit", "Q3 proveniența valorilor", "Q4 aș face singur analiza", "Q5 util pentru industrie", "Comentariu"];
const SUS_HEADER = ["Data", "Laborator", "Limba", "SUS1", "SUS2", "SUS3", "SUS4", "SUS5", "SUS6", "SUS7", "SUS8", "SUS9", "SUS10", "Scor SUS",
  "Q11 proveniența valorilor", "Q12 aș face singur analiza", "Q13 util pentru industrie", "Comentariu"];
function feedback_(lab, d) {
  const n = Array.isArray(d.answers) ? d.answers.length : 0;
  const want = n === 13 ? 13 : 5;
  const a = Array.isArray(d.answers) ? d.answers.slice(0, want).map((x) => Math.round(Number(x))) : [];
  if (a.length !== want || a.some((x) => !(x >= 1 && x <= 5))) return out_({ ok: false, error: want + " answers from 1 to 5 are required" });
  const date = Utilities.formatDate(new Date(), TZ, "yyyy-MM-dd"), comment = safe_(clean_(d.comment, 1000));
  let row, sh;
  if (want === 13) {
    let sum = 0;
    for (let i = 0; i < 10; i++) sum += i % 2 === 0 ? a[i] - 1 : 5 - a[i];
    row = [date, LABS[lab], clean_(d.lang, 5)].concat(a.slice(0, 10), [sum * 2.5], a.slice(10), [comment]);
    sh = fbSheet_("Feedback SUS", SUS_HEADER);
  } else {
    row = [date, LABS[lab], clean_(d.lang, 5)].concat(a, [comment]);
    sh = fbSheet_("Feedback", FB_HEADER);
  }
  const last = sh.getLastRow();
  const at = 2 + Math.floor(Math.random() * last); /* between row 2 and last + 1 */
  if (at > last) sh.appendRow(row);
  else { sh.insertRowBefore(at); sh.getRange(at, 1, 1, row.length).setValues([row]); }
  return out_({ ok: true });
}
function fbSheet_(name, header) {
  const ss = book_();
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(header); sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, header.length).setFontWeight("bold");
  }
  return sh;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
function clean_(v, max) {
  return String(v == null ? "" : v).replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max);
}
/* Keep spreadsheet formulas out of student-entered text. */
function safe_(s) {
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}
function rootFolder_() {
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty("ROOT_ID");
  if (id) {
    try { return DriveApp.getFolderById(id); } catch (e) { /* folder deleted: create a new one */ }
  }
  const f = DriveApp.createFolder(ROOT_FOLDER);
  props.setProperty("ROOT_ID", f.getId());
  return f;
}
function labFolder_(lab) {
  const root = rootFolder_();
  const it = root.getFoldersByName(LABS[lab]);
  return it.hasNext() ? it.next() : root.createFolder(LABS[lab]);
}
function book_() {
  return SpreadsheetApp.getActiveSpreadsheet() || SpreadsheetApp.openById(SHEET_ID);
}
function sheetFor_(lab) {
  const ss = book_();
  let sh = ss.getSheetByName(LABS[lab]);
  if (!sh) {
    sh = ss.insertSheet(LABS[lab]);
    sh.appendRow(HEADER);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEADER.length).setFontWeight("bold");
    sh.getRange("A:A").setNumberFormat("dd.mm.yyyy hh:mm");
  }
  /* sheets made before the JSON columns existed: add the missing header cells */
  const have = sh.getRange(1, 1, 1, HEADER.length).getValues()[0];
  HEADER.forEach((h, i) => { if (!have[i]) sh.getRange(1, i + 1).setValue(h).setFontWeight("bold"); });
  return sh;
}

/* Run once from the editor (Run → setup) to create the tabs and the Drive folder and to grant the permissions. */
function setup() {
  Object.keys(LABS).forEach((lab) => { sheetFor_(lab); labFolder_(lab); });
  const ss = book_();
  const first = ss.getSheets()[0];
  if (!(first.getName() in { "HW TCA": 1, "SW TCA": 1, "FMEA": 1 }) && first.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(first);
  Logger.log("Gata: tab-urile HW TCA, SW TCA, FMEA și folderul „" + ROOT_FOLDER + "” există.");
}

/* ---------------------------------------------------------------- course materials
 * importMaterials(): copies the lecture decks from GitHub into Drive, folder "Materiale curs laboratoare",
 * converted to Google Slides. Run it again after an update: the old copy goes to the trash and a fresh one is made.
 * Your own edits live in Drive; re-importing replaces them, so rename your edited copy first if you want to keep it. */
const MATERIALS_FOLDER = "Materiale curs laboratoare";
const MATERIALS = [
  { name: "HW TCA – curs (RO)", url: "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/main/materials/HW_TCA_curs_RO.pptx" },
  { name: "HW TCA – lecture (EN)", url: "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/main/materials/HW_TCA_lecture_EN.pptx" }
];
function importMaterials() {
  const folder = (function () { const it = DriveApp.getFoldersByName(MATERIALS_FOLDER); return it.hasNext() ? it.next() : DriveApp.createFolder(MATERIALS_FOLDER); })();
  MATERIALS.forEach(function (m) {
    const blob = UrlFetchApp.fetch(m.url).getBlob();
    const old = folder.getFilesByName(m.name);
    while (old.hasNext()) old.next().setTrashed(true);
    const boundary = "mat" + Date.now();
    const meta = { name: m.name, mimeType: "application/vnd.google-apps.presentation", parents: [folder.getId()] };
    const body = Utilities.newBlob("--" + boundary + "\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + JSON.stringify(meta) +
      "\r\n--" + boundary + "\r\nContent-Type: " + MimeType.MICROSOFT_POWERPOINT + "\r\n\r\n").getBytes()
      .concat(blob.getBytes()).concat(Utilities.newBlob("\r\n--" + boundary + "--").getBytes());
    const res = UrlFetchApp.fetch("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,webViewLink", {
      method: "post", contentType: "multipart/related; boundary=" + boundary, payload: body,
      headers: { Authorization: "Bearer " + ScriptApp.getOAuthToken() }, muteHttpExceptions: true
    });
    Logger.log(m.name + ": " + res.getContentText());
  });
}
