// Bilder der Startansicht (Kopf, Karte, Profil) und der Zuschauer-Tabelle mit den drei Starts. Server wie pruefen.js (8781).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('pageerror', e => fehler.push(e.message));
  await p.goto('http://localhost:8781/stockholm/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(600); }
  await p.screenshot({ path: 'shots/start_kopf.png' });
  await p.evaluate(() => window.scrollTo(0, 600)); await p.waitForTimeout(600);
  await p.screenshot({ path: 'shots/start_profil.png' });
  const z = await p.evaluate(() => { const s = [...document.querySelectorAll('section')].find(x => /Zuschauer/.test(x.getAttribute('aria-label') || x.dataset.t || ''));
    if (!s) return null; const k = s.querySelector('.klapp-kopf'); if (k && k.getAttribute('aria-expanded') !== 'true') k.click(); return s.id; });
  await p.waitForTimeout(800);
  if (z) { await p.evaluate(id => document.getElementById(id).scrollIntoView(), z); await p.waitForTimeout(500); await p.screenshot({ path: 'shots/zuschauer_starts.png' }); }
  console.log('Zuschauer-Abschnitt', z, 'Wellen-Hinweis:', await p.evaluate(() => (document.getElementById('wellen-note') || {}).textContent));
  console.log('Fehler:', fehler.length ? fehler : 'keine'); await b.close();
})();
