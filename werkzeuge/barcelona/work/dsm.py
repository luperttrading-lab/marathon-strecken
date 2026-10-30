# Oberflächenmodell auf den Brücken: Das Geländemodell (dgm.py) misst unter einer Brücke den Boden (Bahneinschnitt, Trog der Ronda
# Litoral). Das Oberflächenmodell derselben Befliegung („Model de superfícies de l'àrea metropolitana de Barcelona 25cm provinent de
# Lidar 2022“, gleicher ICGC-Dienst) misst das Brückendeck, aber auch Fahrzeuge und Geländer; clean.py nimmt davon den Median über
# 30 m. Abgefragt alle Punkte der Linie (10-m-Raster) bis 60 m vor und hinter jeder OSM-Brücke (bridge=yes, höchstens 12 m neben der
# Linie, ohne Fuß- und Radwege). -> ../dl/dsm_bruecken.json {"x,y": Höhe}
import json, re, time, urllib.request, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25831, always_xy=True)
r = json.load(open("dgm2026_10m.json"))
gx, gy = T.transform([x[2] for x in r], [x[1] for x in r]); baum = cKDTree(np.c_[gx, gy])
N = json.load(open("../dl/osm_netz.json")); KN = N["nodes"]
nahe = set()
for wid, (tg, refs) in N["ways"].items():
    if tg.get("bridge") in (None, "no") or tg.get("highway") in ("motorway", "motorway_link", "footway", "steps", "cycleway", "path", "pedestrian", "corridor", "proposed", "construction"): continue
    P = [KN[str(q)] for q in refs if str(q) in KN]
    if len(P) < 2: continue
    wx, wy = T.transform([q[1] for q in P], [q[0] for q in P])
    wx, wy = np.interp(np.linspace(0, len(wx) - 1, 4 * len(wx)), np.arange(len(wx)), wx), np.interp(np.linspace(0, len(wy) - 1, 4 * len(wy)), np.arange(len(wy)), wy)
    dd, ii = baum.query(np.c_[wx, wy])
    for i in np.unique(ii[dd < 12]): nahe |= set(range(max(0, i - 6), min(len(r), i + 7)))
U = ("https://geoserveis.icgc.cat/servei/catalunya/elevacions-territorial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo"
     "&LAYERS={L}&QUERY_LAYERS={L}&STYLES=&CRS=EPSG:25831&BBOX={x0:.3f},{y0:.3f},{x1:.3f},{y1:.3f}&WIDTH=3&HEIGHT=3&I=1&J=1&INFO_FORMAT=text/plain&FEATURE_COUNT=1")
L = "model-superficies-amb-lidar-25cm-2022"
out = {}
for i in sorted(nahe):
    x, y = gx[i], gy[i]
    for att in range(8):
        try:
            t = urllib.request.urlopen(urllib.request.Request(U.format(L=L, x0=x - 0.375, y0=y - 0.375, x1=x + 0.375, y1=y + 0.375),
                                                              headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=30).read().decode()
            m = re.search(r"value_0 = '([-\d.eE]+)'", t); out[f"{x:.2f},{y:.2f}"] = float(m.group(1)) if m else None; break
        except Exception: time.sleep(1 + att)
json.dump(out, open("../dl/dsm_bruecken.json", "w"))
print(len(out), "Punkte im Oberflächenmodell")
