// Modellvorhersage je Abschnitt der Zwischenzeiten (0–5, 5–10 … 35–40, 40–Ziel): Höhenmeter (200-m-Fenster wie in der App)
// und relativer Steigungsaufschlag der App (Mittel von paceRatio über den Abschnitt minus 1, Standard 1,0 s je Höhenmeter
// bei 4:00 /km), getrennt nach bergauf (excAuf) und bergab (excAb). Braucht den lokalen Server im Repo-Wurzelordner:
//   python3 -m http.server 8765   (dann hier: node modell_segmente.js)  → modell_seg9.json
const { chromium } = require('playwright');
const fs = require('fs');
const APPS = (process.argv[2] || "boston newyork chicago berlin london valencia amsterdam athen").split(" ");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.addInitScript(() => { try { localStorage.clear(); } catch (e) {} });
  const out = {};
  for (const app of APPS) {
    await p.goto(`http://localhost:8765/${app}/`, { waitUntil: 'networkidle' }); await p.waitForTimeout(200);
    out[app] = await p.evaluate(() => {
      const { ratio } = paceRatio(), W = WIN[200], gr = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, L];
      const seg = [];
      for (let s = 0; s + 1 < gr.length; s++) {
        const a = gr[s], bb = gr[s + 1]; let su = 0, sa = 0, sd = 0, n = 0;
        for (let i = Math.round(a / STEP); i < Math.round(bb / STEP) && i < ratio.length; i++) { const r = ratio[i] - 1; su += r; if (r > 0) sa += r; else sd += r; n++; }
        seg.push({ von: a, bis: bb, auf: +(valAt(W.up, bb) - valAt(W.up, a)).toFixed(1), ab: +(valAt(W.dn, bb) - valAt(W.dn, a)).toFixed(1),
          h0: +hAt(a).toFixed(1), h1: +hAt(bb).toFixed(1), exc: +(su / n).toFixed(5), excAuf: +(sa / n).toFixed(5), excAb: +(sd / n).toFixed(5) });
      }
      return { L, secRef: S.secRef, ref: S.ref, seg };
    });
  }
  fs.writeFileSync('modell_seg9.json', JSON.stringify(out, null, 1));
  for (const [app, d] of Object.entries(out)) console.log(app.padEnd(10), d.seg.map(s => (s.exc * 100).toFixed(1).padStart(5)).join(" "), "| ↑", d.seg.reduce((x, s) => x + s.auf, 0).toFixed(0));
  await b.close();
})();
