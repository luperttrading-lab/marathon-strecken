// Kopf der Seite (Karte und Profil der ganzen Strecke) in der normalen Ansicht, oben. Server wie pruefen.js (8792).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 })).newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('pageerror', e => fehler.push(e.message));
  await p.goto('http://localhost:8792/shanghai/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(600); }
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(600);
  await p.screenshot({ path: 'shots/oben_karte.png' });
  // Zahlen-Ansicht an der Brücke über den Longhua Gang
  await p.evaluate(() => { setPos(26600); }); await p.click('#dots button[data-go="1"]'); await p.waitForTimeout(1000);
  await p.screenshot({ path: 'shots/oben_zahlen_km26_6.png' });
  console.log('Fehler:', fehler.length ? fehler : 'keine'); await b.close();
})();
