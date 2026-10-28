/**
 * Lab report collector (Google Apps Script, bound to the "Rapoarte laboratoare" spreadsheet).
 *
 * The lab apps (HW TCA, SW TCA, FMEA) POST each finished report here. For every report the script
 *   1. saves the HTML report in Drive, in "Rapoarte laboratoare/<lab>",
 *   2. appends a row to the sheet tab of that lab (time, name, group, variant, summary, link).
 *
 * Setup: see README.md in this folder.
 */
const LABS = { "HW-TCA": "HW TCA", "SW-TCA": "SW TCA", "FMEA": "FMEA" };
const ROOT_FOLDER = "Rapoarte laboratoare";
const TZ = "Europe/Bucharest";
const MAX_HTML = 3 * 1024 * 1024;
/* the collection spreadsheet; used when the script is not opened from the sheet (Extensions → Apps Script) */
const SHEET_ID = "1eMkpwfwd6qLFUVOAyjTyhx1PH0IPEYksB_Z8L51ah3k";
const HEADER = ["Primit", "Nume", "Grupa", "Varianta", "Rezumat", "Raport (Drive)", "Limba"];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    const lab = String(d.lab || "");
    if (!LABS[lab]) return out_({ ok: false, error: "unknown lab" });
    const name = clean_(d.name, 80), group = clean_(d.group, 20), variant = clean_(d.variant, 10);
    if (!name || !variant) return out_({ ok: false, error: "name and variant are required" });
    const html = String(d.html || "");
    if (!html || html.length > MAX_HTML) return out_({ ok: false, error: "report missing or too large" });

    const now = new Date();
    const stamp = Utilities.formatDate(now, TZ, "yyyy-MM-dd_HH-mm-ss");
    const fileName = [lab, group, variant, name, stamp].join("_").replace(/[^\w\-.]+/g, "_") + ".html";
    const file = labFolder_(lab).createFile(fileName, html, MimeType.HTML);

    sheetFor_(lab).appendRow([now, safe_(name), safe_(group), safe_(variant), safe_(clean_(d.summary, 500)), file.getUrl(), clean_(d.lang, 5)]);
    return out_({ ok: true, received: Utilities.formatDate(now, TZ, "dd.MM.yyyy HH:mm") });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/* Health check: opening the web app URL in a browser shows {"ok":true,...,"version":...}.
   The version tells which code the deployment runs. */
const VERSION = "2026-10-28";
function doGet() {
  return out_({ ok: true, service: "lab-reports", version: VERSION, labs: Object.keys(LABS) });
}

/* Run from the editor (Run → testPost): writes a test row and a test report, without the web app. */
function testPost() {
  const r = doPost({ postData: { contents: JSON.stringify({ lab: "HW-TCA", lang: "ro", name: "TEST", group: "0", variant: "H0", summary: "test din editor", html: "<p>test</p>" }) } });
  Logger.log(r.getContent());
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
