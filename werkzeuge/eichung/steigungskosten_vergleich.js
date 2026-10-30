// Steigungskosten der App bei 1,0 und 0,87 s je Höhenmeter (Zielzeit 3:00 und 4:00), lokaler Server wie bei modell_segmente.js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.addInitScript(() => { try { localStorage.clear(); } catch (e) {} });
  for (const app of ["berlin", "boston", "newyork", "rennsteig"]) {
    await p.goto(`http://localhost:8765/${app}/`, { waitUntil: 'networkidle' }); await p.waitForTimeout(200);
    const r = await p.evaluate(() => { const out = [];
      for (const g of [3 * 3600, 4 * 3600]) for (const v of [1.0, 0.87]) { S.goal = g; S.secRef = v; S.secHm = S.secRef * 240 / S.ref; recompute(); out.push(Math.round(S.goal - P.p0 * L / 1000)); }
      return out; });
    console.log(app.padEnd(10), `3:00 → ${r[0]} s / ${r[1]} s   4:00 → ${r[2]} s / ${r[3]} s`);
  }
  await b.close();
})();
