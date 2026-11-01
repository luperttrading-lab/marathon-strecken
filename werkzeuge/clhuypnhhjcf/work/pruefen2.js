// Bilder der Hausrunde: Kopf, Karte mit km-Marken, Läuferblick, Zwischenzeiten, Zuschauer, Zielzeit-Rad, „Ohne Höhenmeter“,
// Pace-Band, Zielkarte. Server wie pruefen.js (8791). Aufruf: NODE_PATH=/opt/node-tools/node_modules node pruefen2.js
const { chromium } = require('playwright');
const URL = 'http://localhost:8791/clhuypnhhjcf/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2, acceptDownloads: true });
  const p = await ctx.newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('pageerror', e => fehler.push('pageerror ' + e.message));
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  // Vollbild (Start): Karte, dann herausgezoomt mit allen km-Marken
  await p.screenshot({ path: 'shots/01_vollbild_start.png' });
  await p.evaluate(() => { setPos(2500); dirty = true; });
  await p.click('#dots button[data-go="0"]'); await p.waitForTimeout(800);
  for (let i = 0; i < 6; i++) { if (!(await p.isEnabled('#map-out'))) break; await p.click('#map-out'); await p.waitForTimeout(300); }
  await p.waitForTimeout(1200); await p.screenshot({ path: 'shots/02_karte_uebersicht.png' });
  await p.click('#map-in'); await p.waitForTimeout(1000); await p.screenshot({ path: 'shots/02b_karte_stufe.png' });
  // Läuferblick an Stellen: Unterführung, höchster Punkt, Schiffenberg; Zahlen-Seite
  for (const [km, seite, name] of [[1.03, 1, 'unterfuehrung'], [5.37, 1, 'hoechster_punkt'], [6.38, 0, 'schiffenberg_karte'], [9.06, 1, 'unterfuehrung_zurueck']]) {
    await p.evaluate(([km]) => { setPos(km * 1000); dirty = true; }, [km]);
    await p.click(`#dots button[data-go="${seite}"]`); await p.waitForTimeout(1000);
    await p.screenshot({ path: `shots/03_lauf_${name}.png` });
    console.log('Laufansicht', km, JSON.stringify(await p.evaluate(() => ['r-km', 'r-street', 'r-quarter', 'r-h', 'r-grade'].map(i => (document.getElementById(i) || {}).textContent))));
  }
  // Ausschnitt 10 km (länger als die Runde) und 0,5 km
  for (const z of [10000, 500]) {
    await p.evaluate(z => { S.zoom = z; ZW.set(z); setPos(3000); dirty = true; }, z); await p.waitForTimeout(800);
    await p.screenshot({ path: `shots/04_lauf_ausschnitt_${z}.png` });
  }
  await p.evaluate(() => { S.zoom = 5000; ZW.set(5000); dirty = true; });
  // Zielkarte
  await p.evaluate(() => { setPos(9000); setPos(L); }); await p.waitForTimeout(1500);
  await p.screenshot({ path: 'shots/05_zielkarte.png' });
  console.log('Zielkarte', JSON.stringify(await p.evaluate(() => ['z-sub', 'z-zeit', 'z-auf', 'z-ab', 'z-satz', 'r-km'].map(i => document.getElementById(i).textContent))));
  await p.click('#ziel'); await p.waitForTimeout(500);
  // normale Ansicht: Kopf
  if (await p.isVisible('#run-close')) { await p.click('#run-close'); await p.waitForTimeout(600); }
  await p.evaluate(() => { setPos(0); window.scrollTo(0, 0); }); await p.waitForTimeout(600);
  await p.screenshot({ path: 'shots/06_kopf.png' });
  const oeffne = async (sel) => { await p.evaluate(sel => { const s = document.querySelector(sel); const k = s.querySelector('.klapp-kopf'); if (k.getAttribute('aria-expanded') !== 'true') k.click(); }, sel); await p.waitForTimeout(700);
    await p.evaluate(sel => document.querySelector(sel).scrollIntoView(), sel); await p.waitForTimeout(500); };
  const zu = async (sel) => { await p.evaluate(sel => { const k = document.querySelector(sel).querySelector('.klapp-kopf'); if (k.getAttribute('aria-expanded') === 'true') k.click(); }, sel); await p.waitForTimeout(400); };
  // Zwischenzeiten je km, je 5 km, Hälften
  const zw = await p.evaluate(() => document.getElementById('split-body').closest('section.klapp').id);
  await oeffne('#' + zw);
  for (const m of ['km', 'five', 'ten', 'hm']) { await p.click(`[data-split="${m}"]`); await p.waitForTimeout(500); await p.evaluate(id => document.getElementById(id).scrollIntoView(), zw); await p.waitForTimeout(300);
    await p.screenshot({ path: `shots/07_zwischenzeiten_${m}.png`, fullPage: false }); }
  await p.click('[data-split="km"]');
  // Pace-Band
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#band')]); await dl.saveAs('shots/08_paceband.png'); console.log('Pace-Band', dl.suggestedFilename());
  await zu('#' + zw);
  // Für Zuschauer
  await oeffne('#plan'); await p.screenshot({ path: 'shots/09_zuschauer.png' }); await zu('#plan');
  // Einstellungen: Zielzeit-Rad, 0 Stunden, „Ohne Höhenmeter“
  await oeffne('#einstellungen');
  await p.evaluate(() => document.getElementById('goal-wheels').scrollIntoView({ block: 'center' })); await p.waitForTimeout(500);
  await p.screenshot({ path: 'shots/10_zielzeit_rad.png' });
  // 0 Stunden ist voreingestellt (0:40:xx); einmal auf 1 Stunde und zurück über die Räder
  console.log('Rad Stunden min/max:', JSON.stringify(await p.evaluate(() => [GW.h.value, document.querySelectorAll('#wg-h .wv, #wg-h [data-v]').length])));
  await p.evaluate(() => document.getElementById('bahn').scrollIntoView({ block: 'center' })); await p.waitForTimeout(400);
  await p.screenshot({ path: 'shots/11_ohne_hoehenmeter.png' });
  await p.click('button.info[popovertarget="bahn-info"]'); await p.waitForTimeout(500); await p.screenshot({ path: 'shots/12_ohne_hoehenmeter_info.png' });
  await p.keyboard.press('Escape'); await zu('#einstellungen');
  // Rampen und Quellen
  await oeffne('#rampen'); await p.screenshot({ path: 'shots/13_rampen.png' }); await zu('#rampen');
  await oeffne('#quellen'); await p.screenshot({ path: 'shots/14_quellen.png' });
  await p.evaluate(() => document.getElementById('img-note').scrollIntoView({ block: 'center' })); await p.waitForTimeout(300); await p.screenshot({ path: 'shots/15_quellen_abgleich.png' });
  console.log('Fehler:', fehler.length ? fehler : 'keine'); await b.close();
})();
