// Prüfung der Hausrunde im Browser (Chromium über Playwright, 393 × 852, Faktor 2), Server: python3 -m http.server 8791 im Repo.
// Aufruf: NODE_PATH=/opt/node-tools/node_modules node pruefen.js   (Bilder nach shots/)
const { chromium } = require('playwright');
const URL = 'http://localhost:8791/clhuypnhhjcf/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2, acceptDownloads: true });
  const p = await ctx.newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
  p.on('pageerror', e => fehler.push('pageerror ' + e.message));
  let abgebrochen = 0;
  p.on('requestfailed', r => { const t = (r.failure() || {}).errorText || ''; if (/ERR_ABORTED/.test(t) && /karte-/.test(r.url())) abgebrochen++; else fehler.push('requestfailed ' + r.url() + ' ' + t); });
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  const info = await p.evaluate(async () => {
    const reg = await navigator.serviceWorker.getRegistration(); const keys = await caches.keys(); let n = 0;
    for (const k of keys) if (k.startsWith('hrs-')) n += (await (await caches.open(k)).keys()).length;
    return { version: APP_VERSION, knopf: document.getElementById('app-ver').textContent, sw: !!(reg && (reg.active || reg.installing || reg.waiting)), caches: keys, eintraege: n,
             titel: document.title, h1: document.querySelector('h1').textContent, L, LTXT, MARA, KMSCHRITT, marks: D.marks.map(m => m.s), bridges: D.bridges.length,
             termine: D.termine, RENNTAG, start: S.start, posMax: document.getElementById('pos').max };
  });
  console.log(JSON.stringify(info));
  const karten = await p.evaluate(async () => {
    const ausD = Object.values(D.tiles).flatMap(t => t.chunks.map(c => './karte-dunkel-' + c[4] + '.jpg')).sort();
    const sw = await (await fetch('sw.js')).text(); const ausSW = JSON.parse(sw.match(/const KARTE = (\[.*?\]);/s)[1]).sort();
    const fehlt = []; for (const f of ausD) { const r = await fetch(f, { cache: 'no-store' }); if (!r.ok) fehlt.push(f); else await r.blob(); }
    return { d: ausD.length, sw: ausSW.length, gleich: JSON.stringify(ausD) === JSON.stringify(ausSW), fehlt };
  });
  console.log('Kartenstücke', JSON.stringify(karten));
  // Modellzeit: Voreinstellung, Kosten, und welche Rundenzeit „10 000 m auf der Bahn“ = 40:00 ergibt
  const zeit = await p.evaluate(() => {
    const r = { voreinstellung: hms(S.goal), flachPace: mss2(P.p0), kosten: Math.round(S.goal - P.p0 * L / 1000), steig: document.getElementById('goal-steig').textContent,
                bahn: [...document.querySelectorAll('#bahn span')].map((s, i) => s.textContent + ' ' + document.querySelectorAll('#bahn b')[i].textContent) };
    const g0 = S.goal; let a = 30 * 60, z = 50 * 60;
    const t10 = () => { const k = Math.log(4.667) / Math.log(4.2195); return P.p0 * L / 1000 * Math.pow(42.195 / (L / 1000), k) / 4.667; };
    for (let i = 0; i < 40; i++) { const m = (a + z) / 2; S.goal = m; buildPace(); if (t10() < 2400) a = m; else z = m; }
    S.goal = Math.round((a + z) / 2); recompute();
    r.runde_bei_10km_40 = hms(S.goal); r.bahn10 = document.getElementById('bahn-10').textContent; r.flachPace40 = mss2(P.p0); r.kosten40 = Math.round(S.goal - P.p0 * L / 1000);
    r.flach985 = mss(P.p0 * L / 1000);   // dieselbe Anstrengung auf flachen 9,85 km
    r.hm = Object.fromEntries([50, 100, 200, 1000].map(w => [w, Math.round(valAt(WIN[w].up, L))]));
    S.goal = g0; recompute(); return r; });
  console.log(JSON.stringify(zeit));
  // Zwischenzeiten-Beschriftungen je Modus, Zuschauer-Tabelle, Text unter der Zielzeit
  const texte = await p.evaluate(() => {
    const r = {};
    for (const m of ['km', 'five', 'ten', 'hm']) { S.split = m; renderSplits(); r[m] = [...document.querySelectorAll('#split-body tr')].map(t => t.cells[0].textContent); r[m + '_fuss'] = document.getElementById('split-foot').textContent.trim().replace(/\s+/g, ' '); }
    S.split = 'km'; renderSplits();
    r.plan = [...document.querySelectorAll('#plan-body tr')].map(t => [...t.cells].map(c => c.textContent).join(' | '));
    r.planNote = document.getElementById('plan-note').textContent; r.splitNote = document.getElementById('split-note').textContent;
    r.goalNote = document.getElementById('goal-note').textContent; r.hmNote = document.getElementById('hm-note').textContent; r.speedNote = document.getElementById('speed-note').textContent;
    r.ruleNote = document.getElementById('rule-note').textContent; r.bergNote = [...document.querySelectorAll('.berg-note')].map(x => x.hidden ? '-' : x.textContent);
    r.klapp = [...document.querySelectorAll('.klapp-kopf')].map(k => k.textContent.trim().replace(/\s+/g, ' '));
    r.rampen = [...document.querySelectorAll('#ramp-body tr')].slice(0, 6).map(t => t.textContent.trim().replace(/\s+/g, ' '));
    r.hmMethods = [...document.querySelectorAll('#hm-methods tr')].map(t => t.textContent.trim().replace(/\s+/g, ' '));
    r.wellenNote = document.getElementById('wellen-note').hidden; r.staffel = document.getElementById('staffel').hidden;
    r.zielRad = [GW.h.value, GW.m.value, GW.s.value]; r.startRad = [GW.sh.value, GW.sm.value];
    return r; });
  for (const [k, v] of Object.entries(texte)) console.log(k + ':', JSON.stringify(v));
  // alle Abschnitte aufklappen, Breiten
  await p.evaluate(() => { for (const k of document.querySelectorAll('.klapp-kopf')) if (k.getAttribute('aria-expanded') !== 'true') k.click(); });
  await p.waitForTimeout(800);
  for (const w of [320, 375, 393, 430]) {
    await p.setViewportSize({ width: w, height: 852 }); await p.waitForTimeout(600);
    for (const m of ['km', 'five', 'hm']) {
      const r = await p.evaluate((m) => { S.split = m; renderSplits(); return { doc: document.documentElement.scrollWidth, win: innerWidth,
        tabellen: [...document.querySelectorAll('table')].filter(t => t.offsetParent).map(t => [t.closest('section')?.id || '', t.scrollWidth, t.parentElement.clientWidth]) }; }, m);
      const zuBreit = r.tabellen.filter(t => t[1] > t[2] + 1);
      console.log(`Breite ${w} (${m}): Seite ${r.doc}/${r.win}, ${r.tabellen.length} Tabellen, zu breit: ${JSON.stringify(zuBreit)}`);
    }
  }
  await p.setViewportSize({ width: 393, height: 852 }); await p.evaluate(() => { S.split = 'km'; renderSplits(); });
  await p.evaluate(() => { for (const k of document.querySelectorAll('.klapp-kopf')) if (k.getAttribute('aria-expanded') === 'true') k.click(); window.scrollTo(0, 0); });
  await p.waitForTimeout(500);
  console.log('Fehler bis hier:', fehler.length ? fehler : 'keine');
  await b.close();
})();
