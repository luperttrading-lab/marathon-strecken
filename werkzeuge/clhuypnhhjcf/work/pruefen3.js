// Randfälle des längenunabhängigen Kerns an der kurzen Runde: Zielzeit 0 Stunden und sehr kurz, geteilter Plan, Live ohne Termin,
// Kosten mit 200-m-Fenster gerechnet (Vergleich), Unterführung im Läuferblick. Server wie pruefen.js (8791).
const { chromium } = require('playwright');
const URL = 'http://localhost:8791/clhuypnhhjcf/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('pageerror', e => fehler.push('pageerror ' + e.message));
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
  // Kosten wie im Kern, aber mit 200-m- statt 100-m-Fenster gerechnet, bei Zielzeit, die 10 000 m = 40:00 ergibt
  console.log(JSON.stringify(await p.evaluate(() => {
    const kosten = w => { const g = WIN[w].g; let sum = 0; for (let i = 1; i < N; i++) sum += (paceFaktor(g[i - 1] / 100) + paceFaktor(g[i] / 100)) / 2 * STEP; return sum / 1000; };
    const f10 = Math.pow(10 / (L / 1000), Math.log(4.667) / Math.log(4.2195));   // flache 9,85 km -> 10 km (Riegel wie der Kern)
    const p0 = 2400 / f10 / (L / 1000);   // Flach-Pace, bei der 10 000 m 40:00 dauern
    return { flach985: mss(p0 * L / 1000), runde100: mss(p0 * kosten(100)), runde200: mss(p0 * kosten(200)), faktor100: (p0 * kosten(100) / 2400).toFixed(4), faktor200: (p0 * kosten(200) / 2400).toFixed(4) };
  })));
  // Zielzeit sehr kurz (0:00:00 über die Räder-Logik) und 0:35:00
  for (const [h, m, s] of [[0, 0, 0], [0, 5, 0], [0, 35, 0]]) {
    const r = await p.evaluate(([h, m, s]) => { S.goal = Math.max(60, h * 3600 + m * 60 + s); recompute(); return [hms(S.goal), mss2(P.p0), document.getElementById('goal-note').textContent, document.getElementById('bahn-10').textContent, document.getElementById('goal-steig').textContent]; }, [h, m, s]);
    console.log('Zielzeit', h, m, s, JSON.stringify(r));
  }
  await p.screenshot({ path: 'shots/16_zielzeit_0_35.png' });
  // geteilter Plan und Live ohne Termin
  const p2 = await ctx.newPage(); p2.on('pageerror', e => fehler.push('p2 ' + e.message)); p2.on('console', m => { if (m.type() === 'error') fehler.push('p2 ' + m.text()); });
  await p2.goto(URL + '?ziel=0:45:10&start=19:30', { waitUntil: 'networkidle' }); await p2.waitForTimeout(1500);
  console.log('Gast', JSON.stringify(await p2.evaluate(() => [hms(S.goal), uhr(S.start), GAST, document.getElementById('plan-note').textContent])));
  await p2.evaluate(() => live()); await p2.waitForTimeout(1500);
  console.log('Live', JSON.stringify(await p2.evaluate(() => [S.live, document.getElementById('play').textContent, Math.round(S.pos)])));
  await p2.evaluate(() => stop()); await p2.close();
  // Unterführung im Läuferblick bei 1 km Ausschnitt
  await p.evaluate(() => { S.goal = 2437; recompute(); document.body.classList.add('run'); S.zoom = 1000; ZW.set(1000); setPos(1030); dirty = true; });
  await p.click('#dots button[data-go="1"]'); await p.waitForTimeout(1000);
  await p.screenshot({ path: 'shots/17_lauf_unterfuehrung_1km.png' });
  // Plan-Teilen-Text (ohne navigator.share: Zwischenablage)
  console.log('Fehler:', fehler.length ? fehler : 'keine'); await b.close();
})();
