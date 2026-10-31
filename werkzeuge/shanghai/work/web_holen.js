// Seiten des Veranstalters (shang-ma.com, Vue-App) in Chromium öffnen und die Antworten der API (apih5.shang-ma.com/app) als JSON
// nach ../dl/api/ legen; die POST-Abfragen verschlüsselt die Seite selbst, deshalb über den Browser statt direkt.
// Aufruf: NODE_PATH=/opt/node-tools/node_modules node web_holen.js <URL> [Name] [Sprache zh-CN|en-US]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const OUT = path.join(__dirname, '../dl/api');
(async () => {
  const url = process.argv[2]; const name = process.argv[3] || 'seite'; const sprache = process.argv[4] || 'zh-CN';
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY || 'http://127.0.0.1:43261' } });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 2000 }, locale: sprache, ignoreHTTPSErrors: false });
  const p = await ctx.newPage(); let n = 0;
  p.on('response', async r => {
    const u = r.url();
    if (!/apih5\.shang-ma\.com|app_config|hard_coding/.test(u)) return;
    try { const t = await r.text(); n++; fs.writeFileSync(path.join(OUT, `${name}_${String(n).padStart(2, '0')}.json`), JSON.stringify({ url: u, method: r.request().method(), body: t })); } catch (e) {}
  });
  try { await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 }); } catch (e) { console.log('goto', e.message); }
  await p.waitForTimeout(4000);
  fs.writeFileSync(path.join(OUT, `${name}.txt`), await p.evaluate(() => document.body.innerText));
  fs.writeFileSync(path.join(OUT, `${name}.html`), await p.content());
  await p.screenshot({ path: path.join(OUT, `${name}.png`), fullPage: true });
  console.log(name, 'API-Antworten', n, 'URL', p.url());
  await b.close();
})();
