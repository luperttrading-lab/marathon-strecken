# OSM-Daten entlang der Strecke über die OSM-API (api.openstreetmap.org/api/0.6/map) in Rechtecken von 0,004° × 0,006°
# (gut 440 × 410 m). Overpass war am 30.10.2026 aus dieser Umgebung nicht nutzbar (maps.mail.ru und overpass.private.coffee
# 504, overpass-api.de Verbindung abgebrochen, overpass.kumi.systems Zeitüberschreitung). Rechtecke: alle, deren Mitte höchstens
# 850 m neben der grob eingepassten Linie des Streckenplans liegt (Plan affin über Bahnhofssymbole eingepasst, bis 360 m daneben,
# darum der breite Rand); eine Abfrage je Sekunde, Rohantworten in ../dl/osmapi/.
# -> ../dl/osm_netz.json: alle Wege mit highway (Tags, Knoten-IDs), Knotenkoordinaten
import json, os, sys, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
DLA, DLO = 0.004, 0.006
T = Transformer.from_crs(4326, 28992, always_xy=True)
if len(sys.argv) > 1 and sys.argv[1] == "grob":
    # grobe Linie: Plan affin über die Bahnhofssymbole (Centraal, Zuid, RAI, Bijlmer ArenA; Metro Weesperplein, Waterlooplein,
    # Nieuwmarkt, Wibautstraat) nach RD New
    P = {(1128.2, 50.9): (52.37890, 4.90058), (411.0, 1158.9): (52.33881, 4.87319), (752.2, 1118.9): (52.33703, 4.89023),
         (1637.2, 1834.0): (52.31224, 4.94709), (1067.9, 529.5): (52.3613, 4.9078), (989.0, 372.0): (52.3672, 4.9024),
         (955.9, 235.2): (52.3721, 4.9007), (1140.5, 728.9): (52.3552, 4.9116)}
    A = np.array([[x, y, 1] for x, y in P]); B = np.array([T.transform(lo, la) for la, lo in P.values()])
    M = np.linalg.lstsq(A, B, rcond=None)[0]
    pts = np.vstack([np.array(z) for z in json.load(open("../dl/pdf_linie.json"))["rot"]])
    linie = np.c_[pts, np.ones(len(pts))] @ M; RAND = 850
else:
    g = json.load(open("gpx2026.json")); linie = np.array([T.transform(p[1], p[0]) for p in g["pts"]]); RAND = 250
baum = cKDTree(linie)
lo_, la_ = Transformer.from_crs(28992, 4326, always_xy=True).transform(linie[:, 0], linie[:, 1])
zellen = []
for i in range(int((la_.min() - 0.012) / DLA), int((la_.max() + 0.012) / DLA) + 1):
    for j in range(int((lo_.min() - 0.018) / DLO), int((lo_.max() + 0.018) / DLO) + 1):
        if baum.query(T.transform((j + 0.5) * DLO, (i + 0.5) * DLA))[0] < RAND: zellen.append((i, j))
print(len(zellen), "Rechtecke", flush=True)
for n, (i, j) in enumerate(zellen):
    f = f"{CACHE}/map_{i}_{j}.xml"
    if os.path.exists(f) and os.path.getsize(f) > 100: continue
    bb = (j * DLO, i * DLA, (j + 1) * DLO, (i + 1) * DLA)
    url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + ",".join(f"{v:.4f}" for v in bb)
    for att in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
            data = urllib.request.urlopen(req, timeout=180).read(); open(f + ".tmp", "wb").write(data); os.replace(f + ".tmp", f); break
        except Exception as e: print("  Fehler", i, j, e, flush=True); time.sleep(5 + 10 * att)
    time.sleep(1)
    if n % 20 == 0: print(n, "von", len(zellen), flush=True)
# Wege mit highway, die Laufbahn im Stadion (leisure=track) und alle Knoten, die sie brauchen; dazu Wasserflächen (natural=water, waterway=riverbank/canal als Fläche)
knoten, wege = {}, {}
for f in sorted(os.listdir(CACHE)):
    if not f.endswith(".xml"): continue
    r = ET.parse(f"{CACHE}/{f}").getroot()
    for nd in r.iter("node"): knoten[int(nd.get("id"))] = (float(nd.get("lat")), float(nd.get("lon")))
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        if "highway" in tg or tg.get("leisure") == "track" or tg.get("natural") == "water" or tg.get("water") or tg.get("waterway") in ("riverbank", "canal", "river"):
            wege[int(w.get("id"))] = {"tags": tg, "nd": [int(x.get("ref")) for x in w.iter("nd")]}
noetig = {k for w in wege.values() for k in w["nd"]}
json.dump({"wege": {str(k): v for k, v in wege.items()}, "knoten": {str(k): v for k, v in knoten.items() if k in noetig}}, open("../dl/osm_netz.json", "w"))
print(len(wege), "Wege,", len(noetig), "Knoten")
