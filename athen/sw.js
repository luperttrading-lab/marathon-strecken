const CACHE = "ath-marathon-profil";
const SHELL = ["./", "./index.html", "../manifest.webmanifest", "../icon-192.png", "../apple-touch-icon.png", "./version.json"];
const KARTE = ["./karte-dunkel-z11-0-0.jpg", "./karte-dunkel-z11-0-1.jpg", "./karte-dunkel-z11-1-0.jpg", "./karte-dunkel-z11-1-1.jpg", "./karte-dunkel-z12-0-0.jpg", "./karte-dunkel-z12-0-1.jpg", "./karte-dunkel-z12-1-0.jpg", "./karte-dunkel-z12-1-1.jpg", "./karte-dunkel-z13-0-0.jpg", "./karte-dunkel-z13-0-1.jpg", "./karte-dunkel-z13-1-0.jpg", "./karte-dunkel-z13-1-1.jpg", "./karte-dunkel-z14-0-2.jpg", "./karte-dunkel-z14-0-3.jpg", "./karte-dunkel-z14-1-1.jpg", "./karte-dunkel-z14-1-2.jpg", "./karte-dunkel-z14-2-0.jpg", "./karte-dunkel-z14-2-1.jpg", "./karte-dunkel-z14-2-2.jpg", "./karte-dunkel-z14-3-0.jpg", "./karte-dunkel-z14-3-1.jpg", "./karte-dunkel-z14-3-2.jpg", "./karte-dunkel-z15-0-4.jpg", "./karte-dunkel-z15-0-5.jpg", "./karte-dunkel-z15-1-4.jpg", "./karte-dunkel-z15-1-5.jpg", "./karte-dunkel-z15-2-3.jpg", "./karte-dunkel-z15-2-4.jpg", "./karte-dunkel-z15-3-4.jpg", "./karte-dunkel-z15-4-4.jpg", "./karte-dunkel-z15-5-0.jpg", "./karte-dunkel-z15-5-1.jpg", "./karte-dunkel-z15-5-2.jpg", "./karte-dunkel-z15-5-3.jpg", "./karte-dunkel-z15-5-4.jpg", "./karte-dunkel-z15-6-0.jpg", "./karte-dunkel-z15-6-1.jpg", "./karte-dunkel-z15-6-2.jpg", "./karte-dunkel-z15-6-3.jpg", "./karte-dunkel-z15-6-4.jpg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL).then(() => c.addAll(KARTE).catch(() => {}))));
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  // nur eigene alte Caches löschen: Startseite und andere Strecken teilen sich denselben Speicher
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("ath-") && k !== CACHE).map(k => caches.delete(k)))));
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
