const CACHE = "gwm-marathon-profil";
const INDEX = new URL("./index.html", self.location).href;
const SHELL = ["./", "./index.html", "../manifest.webmanifest", "../icon-192.png", "../apple-touch-icon.png", "./version.json"];
const KARTE = ["./karte-dunkel-z11-0-0.jpg", "./karte-dunkel-z11-0-1.jpg", "./karte-dunkel-z11-1-0.jpg", "./karte-dunkel-z11-1-1.jpg", "./karte-dunkel-z12-0-0.jpg", "./karte-dunkel-z13-0-0.jpg", "./karte-dunkel-z13-0-1.jpg", "./karte-dunkel-z14-0-0.jpg", "./karte-dunkel-z14-0-1.jpg", "./karte-dunkel-z14-1-0.jpg", "./karte-dunkel-z14-1-1.jpg", "./karte-dunkel-z15-0-0.jpg", "./karte-dunkel-z15-0-1.jpg", "./karte-dunkel-z15-0-2.jpg", "./karte-dunkel-z15-1-0.jpg", "./karte-dunkel-z15-1-1.jpg", "./karte-dunkel-z15-1-2.jpg"];

self.addEventListener("install", e => {
  // SHELL am HTTP-Cache vorbei frisch holen (sonst kann eine bis zu 10 min alte Kopie in den Speicher kommen)
  // Kartenbilder seit 2.3 nicht mehr hier: die Startseite richtet alle Strecken ein (ohne Karten ≈ 2 MB, mit ≈ 80 MB). Die Karten
  // einer Strecke kommen auf Auftrag „karten“ beim Öffnen der Strecke, alle zusammen per Knopf auf der Startseite
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL.map(s => new Request(s, { cache: "reload" })))));
  self.skipWaiting();
});

// Auftrag „karten“ (seit 2.3, von der eigenen Seite beim Öffnen mit Netz): fehlende Kartenbilder ablegen, vorhandene nicht neu holen
self.addEventListener("message", e => {
  if (e.data !== "karten") return;
  const abs = s => new URL(s, self.location).href;
  e.waitUntil(caches.open(CACHE).then(async c => {
    for (const k of KARTE) if (!(await c.match(abs(k)))) await c.add(new Request(k, { cache: "reload" })).catch(() => {});
  }).catch(() => {}));
});

self.addEventListener("activate", e => {
  // nur eigene alte Caches löschen: Startseite und andere Strecken teilen sich denselben Speicher
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("gwm-") && k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const u = new URL(req.url), eigen = u.origin === self.location.origin;
  if (eigen) {
    // Netz zuerst und beim Server nachfragen; der Cache ist nur die Rückfallebene ohne Netz. Seit 30.10.2026 nur im eigenen
    // Speicher und ohne ?… im Schlüssel: caches.match ohne Namen fand offline auch alte Kopien aus anderen Speichern
    const key = u.origin + u.pathname;
    e.respondWith(
      fetch(req.url, { cache: "no-cache", credentials: "same-origin" }).then(res => {
        if (res.ok && !res.redirected) {
          const a = res.clone(), b = req.mode === "navigate" ? res.clone() : null;
          caches.open(CACHE).then(c => { c.put(key, a); if (b) c.put(INDEX, b); });   // die Seite auch als index.html, die Rückfallebene
        }
        return res;
      }).catch(() => caches.open(CACHE).then(c => c.match(key).then(hit => hit || (req.mode === "navigate" ? c.match(INDEX) : undefined))))
    );
  } else {
    // Schriften von Google ändern sich nicht: Cache zuerst
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok || res.type === "opaque") { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    })));
  }
});
