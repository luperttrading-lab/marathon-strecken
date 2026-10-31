// Kopf der Normalansicht, Brücke Grabenstraße im Läuferblick (schraffiert), Staffel-Einstellung. Server wie pruefen.js (8791).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 })).newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('pageerror', e => fehler.push(e.message));
  await p.goto('http://localhost:8791/graz/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(600); }
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(800);
  await p.screenshot({ path: 'shots/kopf_normalansicht.png' });
  console.log('Kopf:', await p.evaluate(() => [document.querySelector('.eyebrow')?.textContent, document.querySelector('h1').textContent, document.querySelector('.sub')?.textContent?.slice(0, 120)]));
  console.log('Staffel-Einstellung sichtbar:', await p.evaluate(() => !document.getElementById('staffel').hidden));
  await p.click('#run-open'); await p.waitForTimeout(600);
  await p.evaluate(() => { S.relay = true; S.vp = true; setPos(15970); dirty = true; });
  await p.click('#dots button[data-go="1"]'); await p.waitForTimeout(1200);
  await p.screenshot({ path: 'shots/lauf_zahlen_km16_grabenstrasse_staffel.png' });
  await p.evaluate(() => { setPos(9770); dirty = true; }); await p.waitForTimeout(800);
  await p.screenshot({ path: 'shots/lauf_zahlen_km9_wechsel_1.png' });
  console.log('Fehler:', fehler.length ? fehler : 'keine'); await b.close();
})();
