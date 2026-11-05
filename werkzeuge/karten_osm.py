# Kartenbilder einer Strecke auf die unveränderte OpenStreetMap-Karte umstellen (seit Marathon 2.19, Nutzer: „Y, dunkel und
# Original“): Für jedes Stück in D.tiles der Strecke ein Bild karte-osm-<stück>.jpg (JPEG 70) aus den Original-Kacheln in
# werkzeuge/<strecke>/dl/tiles; das dunkle Bild rechnet seitdem die App selbst (Kern, drawMap). Danach karte-dunkel-*.jpg löschen und
# die Kartenliste KARTE in <strecke>/sw.js auf die neuen Namen setzen. Fehlt eine Kachel, wird sie nur nachgeladen, wenn das bisherige
# dunkle Bild an der Stelle Karteninhalt zeigt (sonst war sie schon beim Bau nicht da: Ränder außerhalb des Korridors).
# Aufruf aus werkzeuge/:  python3 karten_osm.py <strecke> [<strecke> …]   (danach: python3 kern/kern.py --version 2.N --schreiben)
# Nach jedem neuen Bau der Kartenbilder (tiles.py, tiles_z11.py, tiles_rand.py schreiben weiter karte-dunkel-*) wieder laufen lassen.
import json, os, re, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UA = {"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"}
GRUND = (242, 239, 233)   # Füllfarbe der Bauskripte, wo keine Kachel lag

def laden(f, z, x, y):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    for att in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
            open(f, "wb").write(data); time.sleep(0.15); return True
        except Exception:
            time.sleep(2 + 3 * att)
    return False

def strecke(app):
    pfad = os.path.join(REPO, app); idx = open(f"{pfad}/index.html", encoding="utf-8").read()
    D = json.loads(re.search(r"const D = (\{.*?\});\n", idx, re.S).group(1))
    raw = os.path.join(REPO, "werkzeuge", app, "dl", "tiles"); os.makedirs(raw, exist_ok=True)
    # 1) fehlende Kacheln mit Inhalt im dunklen Bild nachladen
    holen = []
    for z, T in D["tiles"].items():
        for cx, cy, cw, ch, nm in T["chunks"]:
            dunkel = f"{pfad}/karte-dunkel-{nm}.jpg"
            A = np.asarray(Image.open(dunkel).convert("L"), float) if os.path.exists(dunkel) else None
            for ty in range((T["y0"] + cy) // 256, (T["y0"] + cy + ch - 1) // 256 + 1):
                for tx in range((T["x0"] + cx) // 256, (T["x0"] + cx + cw - 1) // 256 + 1):
                    f = f"{raw}/osm_{z}_{tx}_{ty}.png"
                    if os.path.exists(f) and os.path.getsize(f) > 100: continue
                    if A is not None:
                        x0, y0 = tx * 256 - T["x0"] - cx, ty * 256 - T["y0"] - cy
                        teil = A[max(0, y0):max(0, y0 + 256), max(0, x0):max(0, x0 + 256)]
                        if teil.size == 0 or teil.std() < 3: continue   # dort lag beim Bau keine Kachel
                    holen.append((f, int(z), tx, ty))
    holen = sorted(set(holen))
    with cf.ThreadPoolExecutor(2) as ex: ok = list(ex.map(lambda a: laden(*a), holen))
    # 2) Bilder schreiben
    alt = neu = 0; luecken = 0
    for z, T in D["tiles"].items():
        for cx, cy, cw, ch, nm in T["chunks"]:
            im = Image.new("RGB", (cw, ch), GRUND)
            for ty in range((T["y0"] + cy) // 256, (T["y0"] + cy + ch - 1) // 256 + 1):
                for tx in range((T["x0"] + cx) // 256, (T["x0"] + cx + cw - 1) // 256 + 1):
                    f = f"{raw}/osm_{z}_{tx}_{ty}.png"
                    if os.path.exists(f) and os.path.getsize(f) > 100:
                        im.paste(Image.open(f).convert("RGB"), (tx * 256 - T["x0"] - cx, ty * 256 - T["y0"] - cy))
                    else: luecken += 1
            ziel = f"{pfad}/karte-osm-{nm}.jpg"; im.save(ziel, "JPEG", quality=70, optimize=True); neu += os.path.getsize(ziel)
            d = f"{pfad}/karte-dunkel-{nm}.jpg"
            if os.path.exists(d): alt += os.path.getsize(d); os.remove(d)
    # 3) Kartenliste im Service Worker
    sw = open(f"{pfad}/sw.js", encoding="utf-8").read()
    liste = sorted("./" + f for f in os.listdir(pfad) if f.startswith("karte-osm-") and f.endswith(".jpg"))
    sw = re.sub(r"const KARTE = \[.*?\];", "const KARTE = " + json.dumps(liste) + ";", sw, count=1, flags=re.S)
    open(f"{pfad}/sw.js", "w", encoding="utf-8").write(sw)
    print(f"{app}: {len(holen)} Kacheln nachgeladen ({sum(ok)} ok), {luecken} Lücken ohne Kachel, dunkel {alt/1e6:.2f} MB -> Original {neu/1e6:.2f} MB")

if __name__ == "__main__":
    for a in sys.argv[1:]: strecke(a)
