# Amtliches Strassenverzeichnis (swisstopo, Ebene ch.swisstopo.amtliches-strassenverzeichnis, geo.admin.ch „identify“): Strassen
# (Linien) mit ihren amtlichen Namen, dazu benannte Gebiete (Flächen, in Lauterbrunnen und Wengen werden viele Häuser über Gebiete
# adressiert). In OSM fehlen ausserhalb der Orte viele Namen (Stechelbergstrasse, Strassen in Wilderswil und Gsteigwiler), deshalb als
# zweite Quelle. Abfrage in Rechtecken von 0,01° entlang der Linie (höchstens 60 m daneben), eine je Sekunde, Rohantworten in
# ../dl/strassenverz/. -> strassenverz.json [[Linienmeter, Strasse (Linie bis 15 m daneben, Richtung bis 35°) oder "", Gebiet oder ""], …]
import json, os, time, urllib.request
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from matplotlib.path import Path
T = Transformer.from_crs(4326, 2056, always_xy=True)
CACHE = "../dl/strassenverz"; os.makedirs(CACHE, exist_ok=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); Q = np.array([p[:2] for p in g["pts"]])
S = 0.01
dd = np.arange(0, d[-1], 20.0); la = np.interp(dd, d, Q[:, 0]); lo = np.interp(dd, d, Q[:, 1])
KS = sorted({(int(np.floor((a + da) / S)), int(np.floor((b + db) / S))) for a, b in zip(la, lo) for da in (-0.0006, 0, 0.0006) for db in (-0.0008, 0, 0.0008)})
print(len(KS), "Rechtecke", flush=True)
merk = {}
for i, j in KS:
    f = f"{CACHE}/r_{i}_{j}.json"
    if not os.path.exists(f):
        bb = f"{j * S:.3f},{i * S:.3f},{(j + 1) * S:.3f},{(i + 1) * S:.3f}"
        url = ("https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryEnvelope&geometry=" + bb +
               "&imageDisplay=1000,1000,96&mapExtent=" + bb + "&tolerance=0&layers=all:ch.swisstopo.amtliches-strassenverzeichnis"
               "&returnGeometry=true&geometryFormat=geojson&sr=4326&limit=200")
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=60).read()
        open(f, "wb").write(data); time.sleep(1)
    r = json.load(open(f))["results"]
    if len(r) >= 200: print("  Achtung: 200 Treffer in", f)
    for x in r: merk[x["id"]] = x
print(len(merk), "Einträge", flush=True)
pk, pr, pn, flaechen = [], [], [], []
for x in merk.values():
    nm = x["properties"].get("stn_label", ""); gm = x["geometry"]
    if gm["type"] in ("LineString", "MultiLineString"):
        for ln in (gm["coordinates"] if gm["type"] == "MultiLineString" else [gm["coordinates"]]):
            P = np.array(ln)[:, :2]; xx, yy = T.transform(P[:, 0], P[:, 1]); P = np.c_[xx, yy]
            for a, b in zip(P[:-1], P[1:]):
                L = np.hypot(*(b - a))
                if L < 0.01: continue
                for f_ in np.linspace(0, 1, max(2, int(L / 3) + 1)): pk.append(a + f_ * (b - a)); pr.append((b - a) / L); pn.append(nm)
    elif gm["type"] in ("Polygon", "MultiPolygon"):
        for poly in (gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]):
            R = np.array(poly[0])[:, :2]; xx, yy = T.transform(R[:, 0], R[:, 1]); flaechen.append((nm, Path(np.c_[xx, yy])))
pk = np.array(pk); pr = np.array(pr); baum = cKDTree(pk)
ss = np.arange(0, d[-1], 10.0); x, y = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); X = np.c_[x, y]
rl = np.array([X[min(len(X) - 1, i + 2)] - X[max(0, i - 2)] for i in range(len(X))]); rl /= np.maximum(np.hypot(*rl.T), 1e-9)[:, None]
out = []
for i, (s, p) in enumerate(zip(ss, X)):
    best = None
    for j in baum.query_ball_point(p, 15.0):
        if abs(float(np.dot(pr[j], rl[i]))) < np.cos(np.radians(35)): continue
        dist = float(np.hypot(*(pk[j] - p)))
        if best is None or dist < best[0]: best = (dist, pn[j])
    geb = [nm for nm, P in flaechen if P.contains_point(p)]
    out.append([float(s), best[1] if best else "", geb[0] if geb else ""])
json.dump(out, open("strassenverz.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp)
    print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 10:5d} m  {key:30s} Gebiete: {', '.join(dict.fromkeys(o[2] for o in grp if o[2]))}")
