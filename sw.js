const CACHE = "start-marathon-2";   // -2 seit 30.10.2026: leert den alten Speicher mit veralteten Kopien der Strecken
const INDEX = new URL("./index.html", self.location).href;
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./version.json"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL.map(s => new Request(s, { cache: "reload" })))));   // am HTTP-Cache vorbei
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  // nur eigene alte Caches löschen: Startseite und andere Strecken teilen sich denselben Speicher
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("start-") && k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const u = new URL(req.url), eigen = u.origin === self.location.origin;
  if (eigen) {
    if (u.pathname.slice(new URL(self.registration.scope).pathname.length).includes("/")) return;   // Ordner der Strecken: deren eigener Service Worker
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
