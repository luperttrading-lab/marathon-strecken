# OSM-Wege (highway) im Umkreis von 40 m um die Linie -> ../dl/osm_wege.json (Aufbau wie eine Overpass-Antwort mit „out tags geom“).
# Overpass war am 29.10.2026 aus dieser Umgebung nicht nutzbar (maps.mail.ru 504, overpass-api.de Verbindung abgebrochen,
# kumi.systems Zeitüberschreitung). Deshalb über die OSM-API (api.openstreetmap.org/api/0.6/map) in kleinen Rechtecken
# entlang der Linie (je 400 Linienmeter plus 0,0006° Rand), eine Abfrage je Sekunde; Rohantworten in ../dl/osmapi/.
import json, os, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
ss = np.arange(0, d[-1] + 50, 50.0); la = np.interp(ss, d, P[:, 0]); lo = np.interp(ss, d, P[:, 1])
knoten, wege = {}, {}
for n, i in enumerate(range(0, len(ss), 8)):
    j = slice(i, i + 9); R = 0.0006
    bb = (lo[j].min() - R, la[j].min() - R, lo[j].max() + R, la[j].max() + R)
    f = f"{CACHE}/map_{n:03d}.xml"
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + ",".join(f"{v:.5f}" for v in bb)
        for att in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
                open(f, "wb").write(urllib.request.urlopen(req, timeout=120).read()); break
            except Exception as e: print("  Fehler", n, e); time.sleep(5 + 5 * att)
        time.sleep(1)
    r = ET.parse(f).getroot()
    for nd in r.iter("node"): knoten[int(nd.get("id"))] = (float(nd.get("lat")), float(nd.get("lon")))
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        if "highway" in tg: wege[int(w.get("id"))] = (tg, [int(x.get("ref")) for x in w.iter("nd")])
    if n % 10 == 0: print(f"{ss[i] / 1000:5.1f} km: {len(wege)} Wege", flush=True)
# nur Wege, die höchstens 40 m an die Linie herankommen (wie „around:40“)
T = Transformer.from_crs(4326, 32653, always_xy=True)
lx, ly = T.transform(np.interp(np.arange(0, d[-1], 5.0), d, P[:, 1]), np.interp(np.arange(0, d[-1], 5.0), d, P[:, 0])); baum = cKDTree(np.c_[lx, ly])
out = []
for wid, (tg, refs) in wege.items():
    geo = [knoten[k] for k in refs if k in knoten]
    if len(geo) < 2: continue
    wx, wy = T.transform([q[1] for q in geo], [q[0] for q in geo])
    t = np.linspace(0, len(wx) - 1, 5 * len(wx)); wx, wy = np.interp(t, np.arange(len(geo)), wx), np.interp(t, np.arange(len(geo)), wy)
    if baum.query(np.c_[wx, wy])[0].min() > 40: continue
    out.append({"type": "way", "id": wid, "tags": tg, "geometry": [{"lat": a, "lon": b} for a, b in geo]})
json.dump({"elements": out}, open("../dl/osm_wege.json", "w"), ensure_ascii=False)
print(len(out), "Wege höchstens 40 m neben der Linie (von", len(wege), ")")
