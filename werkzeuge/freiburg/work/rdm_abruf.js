// RaceDayMap des Veranstalters (app.racedaymap.com/<karte>, eingebettet auf mein-freiburgmarathon.de/lauf/marathon/) im Browser öffnen
// und alle Antworten mit Daten (JSON, GPX, GeoJSON) nach ../dl/racedaymap/ schreiben. Aufruf: NODE_PATH=/opt/node-tools/node_modules node rdm_abruf.js 2027-marathon
const { chromium } = require('playwright'); const fs = require('fs');
const karte = process.argv[2] || '2027-marathon'; const OUT = '../dl/racedaymap/' + karte; fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1200, height: 900 } })).newPage();
  let n = 0; const liste = [];
  p.on('response', async r => {
    const u = r.url(); const ct = (r.headers()['content-type'] || '');
    if (/json|gpx|xml|geo|octet|protobuf/.test(ct) || /\.(json|gpx|geojson|pbf)(\?|$)/.test(u)) {
      if (/tile|sentry|\/web\/p\//.test(u) && !/route|course|map/.test(u)) return;
      try { const buf = await r.body(); const f = `${OUT}/r${String(n++).padStart(3, '0')}.dat`; fs.writeFileSync(f, buf); liste.push([f, r.status(), ct, buf.length, u]); } catch (e) {}
    }
  });
  await p.goto('https://app.racedaymap.com/' + karte, { waitUntil: 'networkidle', timeout: 90000 }); await p.waitForTimeout(5000);
  await p.screenshot({ path: OUT + '/bild.png' });
  fs.writeFileSync(OUT + '/liste.json', JSON.stringify(liste, null, 1));
  for (const x of liste) console.log(x.slice(1).join(' '), x[0]);
  await b.close();
})();
