import json, re, os, shutil, math
from PIL import Image, ImageDraw
W = "../"
OUT = W + "pwa/"
VERSION = "1.0"
src = open(W + "hamburg-marathon-steigung.html", encoding="utf-8").read()
cut = src.index('<div class="wrap">')
head, body = src[:cut], src[cut:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
# ---- Kopf: Versionsnummer als sichtbarer Auslöser der Update-Prüfung
a = '<span class="eyebrow">Haspa Marathon Hamburg · Kurs 2025/2026</span>'
assert body.count(a) == 1
body = body.replace(a, '<span class="eyebrow">Haspa Marathon Hamburg · Kurs 2025/2026 · <button type="button" class="ver" id="app-ver" aria-label="Nach Update suchen">v' + VERSION + '</button></span>')
# ---- Banner direkt im body, vor allem anderen
banner = '''<div class="update" id="update" hidden role="status" aria-live="polite">
  <span id="update-text"></span>
  <button type="button" class="update-btn" id="update-go">Jetzt laden</button>
</div>
'''
css = '''<style>
:root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; } img { max-width: 100%; } [hidden] { display: none !important; }
/* Versionsnummer: gepunktet unterstrichen, damit man sieht, dass man tippen kann */
.ver { font: inherit; color: inherit; letter-spacing: inherit; text-transform: inherit; background: none; border: 0; padding: 0; min-height: 0; text-decoration: underline dotted; text-underline-offset: 3px; cursor: pointer; }
/* Update-Banner: liegt über der Seite (fixed), schiebt nichts, blendet weich ein */
.update { position: fixed; left: 12px; right: 12px; top: max(env(safe-area-inset-top), 12px); z-index: 60; display: flex; align-items: center; justify-content: space-between; gap: 12px;
  background: #34c759; color: #06240e; padding: 12px 14px; border-radius: 14px; font: 600 15px/1.3 system-ui, -apple-system, sans-serif; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  opacity: 0; transition: opacity 0.35s ease; pointer-events: none; }
.update.an { opacity: 1; pointer-events: auto; }
.update[hidden] { display: none; }
.update.info { background: #2d2d33; color: #f2f2f7; font-weight: 500; }
.update .update-btn { flex: none; min-height: 36px; padding: 8px 14px; font-size: 15px; background: #06240e; color: #fff; border: 0; border-radius: 10px; }
@media (prefers-reduced-motion: reduce) { .update { transition: none; } }
</style>
'''
update_js = r'''<script>
const APP_VERSION = '__V__';
/* Updates, die auf dem iPhone ankommen: Service Worker (Netz zuerst), aktive Prüfung, Meldung danach */
(() => {
  const updateEl = document.getElementById("update");
  let ausTimer = null, infoTimer = null, checking = false, announced = null;
  const einblenden = () => { clearTimeout(ausTimer); updateEl.hidden = false; void updateEl.offsetWidth; updateEl.classList.add("an"); };
  const ausblenden = () => { updateEl.classList.remove("an"); clearTimeout(ausTimer); ausTimer = setTimeout(() => { if (!updateEl.classList.contains("an")) updateEl.hidden = true; }, 380); };
  const showInfo = (text, sekunden = 2) => {
    updateEl.className = "update info"; document.getElementById("update-text").textContent = text;
    document.getElementById("update-go").hidden = true; einblenden(); clearTimeout(infoTimer);
    if (sekunden) infoTimer = setTimeout(() => { if (updateEl.classList.contains("info")) ausblenden(); }, sekunden * 1000);
  };
  const zeigeBanner = text => { updateEl.className = "update"; document.getElementById("update-text").textContent = text; document.getElementById("update-go").hidden = false; einblenden(); };
  // Zustand sofort sichern: Position, Einstellungen liegen schon im Speicher
  const speichereAlles = () => { try { if (typeof S !== "undefined") localStorage.setItem("hhm-pos", JSON.stringify(Math.round(S.pos))); } catch (_) {} };
  updateEl.addEventListener("click", () => { if (updateEl.classList.contains("info")) ausblenden(); });
  document.getElementById("update-go").addEventListener("click", () => { speichereAlles(); location.reload(); });

  async function checkForUpdate(manual = false) {
    if (checking) return;
    if (!manual && document.visibilityState !== "visible") return;
    if (!navigator.onLine) { if (manual) showInfo("Offline – Prüfung nicht möglich"); return; }
    checking = true;
    try {
      const res = await fetch("version.json", { cache: "no-store" });
      if (!res.ok) return;
      const v = (await res.json()).version;
      if (v && v !== APP_VERSION) announceUpdate(v, manual);
      else if (manual) showInfo("Version " + APP_VERSION + " ist aktuell", 4);
    } catch (_) { if (manual) showInfo("Prüfung fehlgeschlagen"); }
    finally { checking = false; }
  }
  function announceUpdate(v, manual) {
    if (announced === v && !manual) return;
    announced = v; speichereAlles();
    zeigeBanner("Neue Version " + v + " ist da");
    // keine Eingabefelder; nur nicht mitten im Abspielen neu laden
    const laeuft = typeof S !== "undefined" && S.playing;
    if (manual || !laeuft) setTimeout(() => { speichereAlles(); location.reload(); }, manual ? 1500 : 3000);
  }
  window.addEventListener("pageshow", () => setTimeout(checkForUpdate, 800));
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") checkForUpdate(); });
  document.getElementById("app-ver").addEventListener("click", () => checkForUpdate(true));

  // Nach einem Update einmal sagen, welche Fassung jetzt läuft (beim allerersten Start still)
  let vorher = null;
  try { vorher = localStorage.getItem("hhm.gesehen"); } catch (_) {}
  if (vorher !== APP_VERSION) {
    try { localStorage.setItem("hhm.gesehen", APP_VERSION); } catch (_) {}
    if (vorher) setTimeout(() => showInfo("Version " + APP_VERSION + " ist geladen", 4), 400);
  }
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
})();
</script>
'''.replace("__V__", VERSION)
meta = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="HH-Marathon">
<meta name="theme-color" content="#0b141c" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#edf1f4" media="(prefers-color-scheme: light)">
<meta name="description" content="Steigungsprofil des Hamburg-Marathons: Höhe, Steigung, Pace-Modell und Karte.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png" type="image/png">
'''
html = meta + css + head + "</head>\n<body>\n" + banner + body.rstrip() + "\n" + update_js + "</body>\n</html>\n"
os.makedirs(OUT, exist_ok=True)
open(OUT + "index.html", "w", encoding="utf-8").write(html)
open(OUT + "version.json", "w").write(json.dumps({"version": VERSION}) + "\n")
# ---- Kartenstücke
maps = sorted(f for f in os.listdir(W + "assets") if f.startswith("karte-"))
for f in maps: shutil.copy(W + "assets/" + f, OUT + f)
# ---- Service Worker: eigene Dateien Netz zuerst, Schriften Cache zuerst; Karte vorab für offline
sw = '''const CACHE = "hh-marathon-profil";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./version.json"];
const KARTE = __MAPS__;

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL).then(() => c.addAll(KARTE).catch(() => {}))));
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const eigen = new URL(req.url).origin === self.location.origin;
  if (eigen) {
    // Netz zuerst und beim Server nachfragen; der Cache ist nur die Rückfallebene ohne Netz
    e.respondWith(
      fetch(req.url, { cache: "no-cache", credentials: "same-origin" }).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
        return res;
      }).catch(() => caches.match(req).then(hit => hit || caches.match("./index.html")))
    );
  } else {
    // Schriften von Google ändern sich nicht: Cache zuerst
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok || res.type === "opaque") { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    })));
  }
});
'''.replace("__MAPS__", json.dumps(["./" + f for f in maps]))
open(OUT + "sw.js", "w").write(sw)
# ---- Manifest
man = {"name": "Steigungsprofil Hamburg-Marathon", "short_name": "HH-Marathon", "lang": "de", "start_url": "./", "scope": "./", "display": "standalone",
       "background_color": "#0b141c", "theme_color": "#0b141c", "description": "Höhe, Steigung, Pace-Modell und Karte für den Hamburg-Marathon.",
       "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
open(OUT + "manifest.webmanifest", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
# ---- Symbol: Höhenprofil der Strecke, Farbe nach Steigung, auf Nachtblau
D = json.loads(re.search(r"const D = (\{.*?\});\n", src, re.S).group(1))
H = [v / 100 for v in D["h"]][:4220]
def icon(size):
    S4 = size * 4
    im = Image.new("RGB", (S4, S4), (11, 20, 28)); dr = ImageDraw.Draw(im)
    for y in range(S4):  # leichter Verlauf
        t = y / S4; dr.line([(0, y), (S4, y)], fill=(int(11 + 16 * t), int(20 + 40 * t), int(28 + 70 * t)))
    m = int(S4 * 0.14); x0, x1 = m, S4 - m; base = int(S4 * 0.74); top = int(S4 * 0.30)
    n = len(H); step = max(1, n // 300)
    pts = []
    for i in range(0, n, step):
        x = x0 + (x1 - x0) * i / (n - 1); y = base - (H[i] - 0) / 42 * (base - top); pts.append((x, y))
    cols = [(13, 102, 128), (58, 148, 173), (149, 201, 214), (197, 206, 213), (240, 192, 96), (229, 131, 58), (195, 53, 42)]
    edges = [-3, -1.5, -0.5, 0.5, 1.5, 3]
    for j in range(len(pts) - 1):
        i = j * step; i2 = min(n - 1, i + 100); i1 = max(0, i - 100)
        g = (H[i2] - H[i1]) / ((i2 - i1) * 10) * 100; c = 0
        while c < len(edges) and g >= edges[c]: c += 1
        (xa, ya), (xb, yb) = pts[j], pts[j + 1]
        dr.polygon([(xa, ya), (xb + 1, yb), (xb + 1, base), (xa, base)], fill=cols[c])
    dr.line(pts, fill=(229, 236, 241), width=max(2, S4 // 90), joint="curve")
    dr.rectangle([x0, base, x1, base + max(2, S4 // 120)], fill=(106, 156, 255))
    return im.resize((size, size), Image.LANCZOS)
for s, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
    icon(s).save(OUT + name, optimize=True)
# ---- README und .nojekyll
open(OUT + ".nojekyll", "w").write("")
open(OUT + "README.md", "w", encoding="utf-8").write("""# Steigungsprofil Hamburg-Marathon

Wischbares Höhen- und Steigungsprofil der Strecke des Haspa Marathon Hamburg (Kurs 2025/2026), als Web-App für den Home-Bildschirm.
Inoffiziell, kein Angebot des Veranstalters.

**App:** https://luperttrading-lab.github.io/hamburg-marathon-profil/ – in Safari öffnen, *Teilen → Zum Home-Bildschirm*.

## Datenquellen

- Strecke und Kilometerpunkte: veröffentlichte GPX- und KMZ-Dateien des Veranstalters (haspa-marathon-hamburg.de, mhv-maps.de).
- Höhe: Digitales Geländemodell DGM1 Hamburg, © Freie und Hansestadt Hamburg, LGV, Datenlizenz Deutschland – Namensnennung 2.0 (dl-de/by-2-0).
  Brücken und der Wallringtunnel sind durch Geraden ersetzt, eine Geländekante in der Breiten Straße ist ausgeglichen.
- Karte: © OpenStreetMap-Mitwirkende (ODbL), Kartenbilder von tile.openstreetmap.org, für hellen und dunklen Modus umgefärbt.
- Straßennamen: © OpenStreetMap-Mitwirkende, über Nominatim.
- Pace-Modell: Energiekosten des Laufens nach Minetti u. a. (2002), auf einstellbare Kosten je Höhenmeter skaliert.

## Updates

`APP_VERSION` in `index.html` und `version.json` bei jeder Änderung gemeinsam hochzählen. Die App prüft beim Öffnen und beim Zurückholen aus dem Hintergrund,
ein Tipp auf die Versionsnummer im Kopf prüft von Hand.
""")
print("Dateien:", len(os.listdir(OUT)), "Größe index.html:", os.path.getsize(OUT + "index.html") // 1024, "KB")
