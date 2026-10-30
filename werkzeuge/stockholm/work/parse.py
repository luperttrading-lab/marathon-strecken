# Strecke aus der GPX-Datei des Veranstalters (Seite „Banan“/„The course“, Knopf „GPX-FIL“:
# stockholmmarathon.se/wp-content/uploads/2026/05/SM26h.gpx_.zip, Track „SM26h“, erstellt mit GPS Visualizer, 3715 Punkte,
# ../dl/gpx/SM26h.gpx). Dazu die Kilometermarken der „dynamischen Karte“ des Veranstalters (CARTO-Konto „marathon“, Tabelle km,
# Karte „SM“, ../dl/carto/km.geojson; Beschreibung „4 km. Löparna passerar 12.12 - 12.46.“), Start und Ziel derselben Tabelle und
# ihre Linie (Tabelle bana, SM Lap1) als Gegenprobe.
# -> gpx2026.json (Punkte mit GPX-Höhe und laufende Länge, geodätisch GRS80), marken.json (Linienmeter jeder Marke)
import json, re, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer, Geod
T = Transformer.from_crs(4326, 3006, always_xy=True)   # SWEREF99 TM
NS = "{http://www.topografix.com/GPX/1/1}"
r = ET.parse("../dl/gpx/SM26h.gpx").getroot()
pts = [(float(p.get("lat")), float(p.get("lon")), float(p.find(NS + "ele").text)) for p in r.iter(NS + "trkpt")]
# doppelte Punkte weg
pts = [p for i, p in enumerate(pts) if i == 0 or (p[0], p[1]) != (pts[i - 1][0], pts[i - 1][1])]
G = Geod(ellps="GRS80")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
dd = np.array(dd); d = np.r_[0, np.cumsum(dd)]
xy = np.array([T.transform(p[1], p[0]) for p in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
print(f"GPX: {len(pts)} Punkte, {d[-1]:.1f} m geodätisch ({dl[-1]:.1f} m in SWEREF99 TM), Abstand bis {dd.max():.0f} m, Median {np.median(dd):.1f} m")
json.dump({"pts": pts, "d": d.tolist()}, open("gpx2026.json", "w"))
def projiziere(la, lo, s_von=0, s_bis=1e9, erwartet=None):
    p = np.array(T.transform(lo, la)); kand = []
    for i in range(len(xy) - 1):
        if dl[i + 1] < s_von or dl[i] > s_bis: continue
        a_, b_ = xy[i], xy[i + 1]; v = b_ - a_; t = np.clip(np.dot(p - a_, v) / (np.dot(v, v) or 1), 0, 1); q = a_ + t * v
        kand.append((float(np.hypot(*(p - q))), float(dl[i] + t * np.hypot(*v))))
    dmin = min(k[0] for k in kand)
    if erwartet is None: return min(kand)[::-1]
    nah = [k for k in kand if k[0] <= max(20, dmin + 1)]
    best = min(nah, key=lambda k: abs(k[1] - erwartet)); return best[1], best[0]
fak = dl[-1] / 42195
F = [f for f in json.load(open("../dl/carto/km.geojson"))["features"] if f["properties"].get("map") == "SM"]
marken = {"km": [], "andere": []}
for f in F:
    p = f["properties"]; lo, la = f["geometry"]["coordinates"]
    m = re.match(r"(\d+(?:,\d+)?) km", p.get("description") or "")
    if p["name"] in ("Start", "Mål"):
        s_, e_ = projiziere(la, lo)
        marken["andere"].append([p["name"], round(s_, 1), round(e_, 1), p["updated_at"][:10], p.get("description")])
        continue
    km = float(m.group(1).replace(",", "."))
    s_, e_ = projiziere(la, lo, (km - 2) * 1000 * fak, (km + 2) * 1000 * fak, km * 1000 * fak)
    zeit = re.search(r"passerar ([\d.]+) - ([\d.]+)", p["description"])
    marken["km"].append([km, round(s_, 1), round(e_, 1), p["updated_at"][:10], zeit.groups() if zeit else None])
marken["km"].sort()
for k in ("km",):
    for m in marken[k]: m[1] = round(float(np.interp(m[1], dl, d)), 1)   # geodätisch wie gpx2026.json
for m in marken["andere"]: m[1] = round(float(np.interp(m[1], dl, d)), 1)
json.dump(marken, open("marken.json", "w"), ensure_ascii=False, indent=0)
vor = (0.0, 0.0)
for km, s_, e_, upd, z in marken["km"]:
    print(f"  km {km:5.1f}  Linie {s_:8.1f} m  ({e_:5.1f} m daneben, Stand {upd})  Linie - km {s_ - km * 1000:+7.1f}  seit vorher {s_ - vor[1]:6.0f} m je {1000 * (km - vor[0]):.0f}  {z}")
    vor = (km, s_)
print(f"  Ende     Linie {d[-1]:8.1f} m  Linie - km {d[-1] - 42195:+7.1f}")
for m in marken["andere"]: print("  ", m)
# Gegenprobe: Linie der Karte (Tabelle bana, SM Lap1)
B = [f for f in json.load(open("../dl/carto/bana.geojson"))["features"] if f["properties"].get("map") == "SM" and f["properties"].get("stylegroup") == "Lap1"]
if B:
    cs = [c for ln in B[0]["geometry"]["coordinates"] for c in ln]
    bx = np.array([T.transform(lo, la) for lo, la in cs])
    from scipy.spatial import cKDTree
    dichte = np.vstack([xy[i] + f * (xy[i + 1] - xy[i]) for i in range(len(xy) - 1) for f in np.linspace(0, 1, max(2, int(np.hypot(*(xy[i + 1] - xy[i])) / 2)))])
    dist, _ = cKDTree(dichte).query(bx)
    lb = np.hypot(*np.diff(bx, axis=0).T).sum()
    print(f"Karte (bana SM Lap1, Stand {B[0]['properties']['updated_at'][:10]}): {len(cs)} Punkte, {lb:.0f} m; Abstand zur GPX-Linie Median {np.median(dist):.1f} m, "
          f"95 % {np.percentile(dist, 95):.1f} m, max {dist.max():.0f} m")
