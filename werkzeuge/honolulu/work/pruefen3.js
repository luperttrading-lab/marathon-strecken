// Abschnitt „Woher die Zahlen kommen“: Bild und Höhenmeter je Messart. Server wie pruefen.js (8791).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 })).newPage();
  await p.goto('http://localhost:8791/honolulu/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(500); }
  const id = await p.evaluate(() => { const s = document.getElementById('hm-methods').closest('section'); const k = s.querySelector('.klapp-kopf');
    if (k && k.getAttribute('aria-expanded') !== 'true') k.click(); return s.id; });
  await p.waitForTimeout(800);
  console.log(await p.evaluate(() => [...document.querySelectorAll('#hm-methods tr')].map(r => r.textContent.trim().replace(/\s+/g, ' ')).join(' | ')));
  await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(500);
  await p.screenshot({ path: 'shots/quellen.png' });
  await b.close();
})();
