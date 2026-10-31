// Kopf der Normalansicht und Ende von „Woher die Zahlen kommen“ (Abgleich-Text). Server wie pruefen.js (8792).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 })).newPage();
  await p.goto('http://localhost:8792/duesseldorf/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(500); }
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(500);
  await p.screenshot({ path: 'shots/kopf.png' });
  console.log(await p.evaluate(() => [document.querySelector('.eyebrow')?.textContent, document.querySelector('h1')?.textContent, document.querySelector('.sub')?.textContent].join(' | ')));
  const id = await p.evaluate(() => { const s = document.getElementById('hm-methods').closest('section'); const k = s.querySelector('.klapp-kopf');
    if (k && k.getAttribute('aria-expanded') !== 'true') k.click(); return s.id; });
  await p.waitForTimeout(800);
  await p.evaluate(id => { const s = document.getElementById(id); window.scrollTo(0, s.getBoundingClientRect().bottom + scrollY - 852); }, id); await p.waitForTimeout(500);
  await p.screenshot({ path: 'shots/quellen_ende.png' });
  await b.close();
})();
