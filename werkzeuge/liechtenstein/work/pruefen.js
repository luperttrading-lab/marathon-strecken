// Prüfung der Liechtenstein-App im Browser (Chromium über Playwright, 393 × 852, Faktor 2), Server: python3 -m http.server 8793 im Repo.
// Aufruf: NODE_PATH=/opt/node-tools/node_modules node pruefen.js
const { chromium } = require('playwright');
const URL = 'http://localhost:8793/liechtenstein/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
  p.on('pageerror', e => fehler.push('pageerror ' + e.message));
  p.on('requestfailed', r => fehler.push('requestfailed ' + r.url()));
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  const info = await p.evaluate(async () => {
    const reg = await navigator.serviceWorker.getRegistration(); const keys = await caches.keys(); let n = 0;
    for (const k of keys) if (k.startsWith('lgt-')) n += (await (await caches.open(k)).keys()).length;
    return { version: APP_VERSION, knopf: document.getElementById('app-ver').textContent, sw: !!(reg && (reg.active || reg.installing || reg.waiting)), caches: keys, eintraege: n,
             titel: document.title, h1: document.querySelector('h1').textContent, marks: D.marks.length, bridges: D.bridges.length };
  });
  console.log(JSON.stringify(info));
  // Modellzeit: Voreinstellung (4:00 /km im Flachen) und Kosten bei 2:50 und 4:00
  const zeit = await p.evaluate(() => { const r = {}; r.voreinstellung = S.goal; r.kostenVor = Math.round(S.goal - P.p0 * L / 1000);
    for (const g of [2 * 3600 + 50 * 60, 4 * 3600]) { S.goal = g; recompute(); r['kosten_' + g] = Math.round(S.goal - P.p0 * L / 1000); r['flach_' + g] = P.p0; }
    return r; });
  console.log(JSON.stringify(zeit));
  // alle Abschnitte aufklappen
  await p.evaluate(() => { for (const k of document.querySelectorAll('.klapp-kopf')) if (k.getAttribute('aria-expanded') !== 'true') k.click(); });
  await p.waitForTimeout(800);
  for (const w of [320, 375, 393, 430]) {
    await p.setViewportSize({ width: w, height: 852 }); await p.waitForTimeout(600);
    const r = await p.evaluate(() => ({ doc: document.documentElement.scrollWidth, win: innerWidth,
      tabellen: [...document.querySelectorAll('table')].filter(t => t.offsetParent).map(t => [t.closest('section')?.id || '', t.scrollWidth, t.parentElement.clientWidth]) }));
    const zuBreit = r.tabellen.filter(t => t[1] > t[2] + 1);
    console.log(`Breite ${w}: Seite ${r.doc}/${r.win}, ${r.tabellen.length} Tabellen, zu breit: ${JSON.stringify(zuBreit)}`);
  }
  await p.setViewportSize({ width: 393, height: 852 });
  await p.evaluate(() => { for (const k of document.querySelectorAll('.klapp-kopf')) if (k.getAttribute('aria-expanded') === 'true') k.click(); window.scrollTo(0, 0); });
  await p.waitForTimeout(500);
  
  // Laufansicht (Vollbild) an mehreren Stellen, Karte und Zahlen
  if (await p.isVisible('#run-open')) { await p.click('#run-open'); await p.waitForTimeout(600); }
  for (const [km, seite, name] of [[0.03, 0, 'karte_start_bendern'], [5.0, 1, 'zahlen_km5_binnendamm'], [10.1, 0, 'karte_km10_vaduz_marktplatz'], [11.3, 0, 'karte_km11_vaduz_schleife'], [12.6, 1, 'zahlen_km12_schloss'], [15.4, 0, 'karte_km15_rotenboden'], [17.6, 1, 'zahlen_km17_masescha'], [21.5, 0, 'karte_km21_silumer_kulm'], [21.9, 1, 'zahlen_km21_abstieg_suecka'], [25.5, 0, 'karte_km25_steg_wechsel'], [30.8, 1, 'zahlen_km30_valorsch'], [32.9, 1, 'zahlen_km32_steilste'], [34.4, 0, 'karte_km34_sassfoerkle'], [37.0, 0, 'karte_km37_malbun'], [38.8, 1, 'zahlen_km38_turna'], [40.8, 0, 'karte_km40_pradamee'], [42.1, 0, 'karte_ziel_malbun']]) {
    await p.evaluate(([km]) => { setPos(km * 1000); }, [km]);
    await p.click(`#dots button[data-go="${seite}"]`); await p.waitForTimeout(1200);
    await p.screenshot({ path: `shots/lauf_${name}.png` });
    const t = await p.evaluate(() => [document.getElementById('r-km').textContent, document.getElementById('r-street').textContent, document.getElementById('r-quarter').textContent, document.getElementById('r-h').textContent, document.getElementById('r-grade').textContent]);
    console.log('Laufansicht', km, JSON.stringify(t));
  }
  // Verpflegung im Profil eingeschaltet, Karte herausgezoomt (Übersicht)
  await p.evaluate(() => { S.vp = true; setPos(30000); dirty = true; });
  await p.click('#dots button[data-go="0"]');
  for (let i = 0; i < 4; i++) { await p.click('#map-out'); await p.waitForTimeout(300); }
  await p.waitForTimeout(1200); await p.screenshot({ path: 'shots/lauf_karte_uebersicht_km30_verpflegung.png' });
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(400); }
  // Tipp auf die Version
  await p.click('#app-ver'); await p.waitForTimeout(2000);
  console.log('Update-Meldung:', await p.evaluate(() => document.getElementById('update-text').textContent));
  console.log('Fehler:', fehler.length ? fehler : 'keine');
  await b.close();
})();
