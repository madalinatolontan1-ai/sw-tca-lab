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

/* Health check: opening the web app URL in a browser shows {"ok":true,...}. */
function doGet() {
  return out_({ ok: true, service: "lab-reports", labs: Object.keys(LABS) });
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
function sheetFor_(lab) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
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
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const first = ss.getSheets()[0];
  if (first.getName() !== "HW TCA" && first.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(first);
}
