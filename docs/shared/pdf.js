/* Report download as PDF (16 Nov 2026).
 * The report (a complete HTML document) is rendered in an off-screen iframe, so its styles
 * never touch the app page, and turned into an A4 landscape PDF by html2pdf.js
 * (vendor/html2pdf.bundle.min.js, MIT, loaded only when the button is pressed).
 * If the PDF cannot be made, onFail() is called and the app falls back to the .html file. */
(function () {
  const LIB = new URL("vendor/html2pdf.bundle.min.js", document.currentScript.src).href;
  const W = 1120; // px width the report is laid out at (fits A4 landscape)
  function download(html, fileName, onDone, onFail) {
    const fr = document.createElement("iframe");
    fr.setAttribute("aria-hidden", "true"); fr.tabIndex = -1;
    fr.style.cssText = "position:fixed;left:-12000px;top:0;width:" + W + "px;height:900px;border:0;visibility:hidden";
    document.body.appendChild(fr);
    let finished = false;
    const end = (ok, err) => { if (finished) return; finished = true; setTimeout(() => fr.remove(), 1500); ok ? onDone && onDone() : onFail && onFail(err); };
    const timer = setTimeout(() => end(false, new Error("timeout")), 60000);
    try {
      const doc = fr.contentDocument; doc.open(); doc.write(html); doc.close();
      const st = doc.createElement("style");
      st.textContent = "html,body{background:#fff!important;color:#111!important}body{margin:0!important;padding:0 6px!important;max-width:none!important}" +
        "tr,li,img,pre,.card,.tracerow{break-inside:avoid;page-break-inside:avoid}h1,h2,h3{break-after:avoid;page-break-after:avoid}";
      doc.head.appendChild(st);
      const s = doc.createElement("script"); s.src = LIB;
      s.onerror = () => { clearTimeout(timer); end(false, new Error("library not loaded")); };
      s.onload = () => {
        const w = fr.contentWindow;
        /* options built in the iframe's own realm: html2pdf checks "instanceof Array", which fails for arrays from the parent page */
        const opt = w.JSON.parse(JSON.stringify({
          margin: [8, 8, 10, 8], filename: fileName,
          image: { type: "jpeg", quality: 0.9 },
          html2canvas: { scale: 2, backgroundColor: "#ffffff", windowWidth: W, logging: false },
          jsPDF: { unit: "mm", format: "a4", orientation: "landscape", compress: true },
          pagebreak: { mode: ["css", "legacy"], avoid: ["tr", "li", "h2", "h3", "pre", ".card"] }
        }));
        w.html2pdf().set(opt).from(doc.body).save().then(() => { clearTimeout(timer); end(true); }, (e) => { clearTimeout(timer); end(false, e); });
      };
      doc.head.appendChild(s);
    } catch (e) { clearTimeout(timer); end(false, e); }
  }
  window.LabPDF = { download };
})();
