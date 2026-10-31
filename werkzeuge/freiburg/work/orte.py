# Stadtteil alle 100 m (Linienmeter der Marathonlinie, strecke2026.json): die Stadtteile Freiburgs (OSM admin_level 10: Brühl,
# Mooswald, Betzenhausen, Weingarten, Haslach, Sankt Georgen, Wiehre, Oberau, Altstadt, Stühlinger …), so wie der Veranstalter die
# Strecke beschreibt; die feineren Stadtbezirke (admin_level 11: Mooswald-Ost, Haslach-Haid …) sind Verwaltung. Die Grenzen kommen als
# OSM-Relationen; osm.py fand ihre Kennungen in den Kartenausschnitten, die vollständigen Flächen kommen einzeln über die OSM-API
# (api.openstreetmap.org/api/0.6/relation/<id>/full, eine Abfrage je Sekunde, ../dl/orte/). Muster: werkzeuge/hannover/work/orte.py.
# Viele Straßen der Strecke sind selbst die Grenze: je 40 m links und rechts nachsehen, bei zwei Stadtteilen „links / rechts“.
# „Sankt Georgen“ heißt wie bei der Stadt „St. Georgen“.
# -> orte2026.json [Linienmeter, Name, Stadtteil in der Mitte, ""]
import glob, json, os, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
from matplotlib.path import Path
def ort(n): return {"Sankt Georgen": "St. Georgen"}.get(n, n or "")
os.makedirs("../dl/orte", exist_ok=True)
ids = {}
for f in glob.glob("../dl/osmapi/t_*.xml"):
    for rel in ET.parse(f).getroot().iter("relation"):
        tg = {t.get("k"): t.get("v") for t in rel.iter("tag")}
        if tg.get("boundary") == "administrative" and tg.get("admin_level") == "10": ids[rel.get("id")] = tg
print(len(ids), "Flächen")
def ring_zusammen(wege):
    wege = [list(w) for w in wege if len(w) >= 2]; ringe = []
    while wege:
        r = wege.pop(0)
        while r[0] != r[-1]:
            for i, w in enumerate(wege):
                if w[0] == r[-1]: r += w[1:]; wege.pop(i); break
                if w[-1] == r[-1]: r += w[::-1][1:]; wege.pop(i); break
                if w[-1] == r[0]: r = w + r[1:]; wege.pop(i); break
                if w[0] == r[0]: r = w[::-1] + r[1:]; wege.pop(i); break
            else: break
        if r[0] == r[-1]: ringe.append(r)
    return ringe
FL = []
for rid, tg in sorted(ids.items()):
    f = f"../dl/orte/rel_{rid}.xml"
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        req = urllib.request.Request(f"https://api.openstreetmap.org/api/0.6/relation/{rid}/full", headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
        open(f, "wb").write(urllib.request.urlopen(req, timeout=180).read()); time.sleep(1)
    r = ET.parse(f).getroot()
    kn = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in r.iter("node")}
    wg = {w.get("id"): [x.get("ref") for x in w.iter("nd")] for w in r.iter("way")}
    rel = [x for x in r.iter("relation") if x.get("id") == rid][0]
    aussen = [wg[m.get("ref")] for m in rel.iter("member") if m.get("type") == "way" and m.get("role") in ("outer", "") and m.get("ref") in wg]
    innen = [wg[m.get("ref")] for m in rel.iter("member") if m.get("type") == "way" and m.get("role") == "inner" and m.get("ref") in wg]
    A = [Path(np.array([kn[k] for k in ring])) for ring in ring_zusammen(aussen)]
    I = [Path(np.array([kn[k] for k in ring])) for ring in ring_zusammen(innen)]
    if not A: print("  keine Fläche:", tg.get("name")); continue
    FL.append((tg.get("name"), tg.get("admin_level"), A, I))
g = json.load(open("strecke2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
# Je 40 m links und rechts der Linie nachsehen; liegen beide Seiten in verschiedenen Stadtteilen, heißt die Stelle „links / rechts“.
def wo(la, lo):
    drin = {lv: n for n, lv, A, I in FL if any(a.contains_point((lo, la)) for a in A) and not any(i.contains_point((lo, la)) for i in I)}
    return drin.get("10", ""), ""
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    la2, lo2 = np.interp(min(s + 20, d[-1]), d, P[:, 0]), np.interp(min(s + 20, d[-1]), d, P[:, 1])
    la1, lo1 = np.interp(max(s - 20, 0), d, P[:, 0]), np.interp(max(s - 20, 0), d, P[:, 1])
    ex, ny = (lo2 - lo1) * np.cos(np.radians(la)), (la2 - la1); n = np.hypot(ex, ny) or 1
    qx, qy = -ny / n, ex / n                                   # nach links (Grad Länge auf Grad Breite umgerechnet)
    seiten = []
    for f in (1, -1):
        dl_, de_ = wo(la + f * qy * 40 / 111320, lo + f * qx * 40 / (111320 * np.cos(np.radians(la))))
        seiten.append(ort(de_ or dl_))
    dimos, einheit = wo(la, lo)
    mitte = ort(einheit or dimos)
    namen = [x for x in dict.fromkeys(seiten) if x] or [mitte]
    out.append([float(s), " / ".join(namen), dimos, einheit])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: o[1]):
    grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:6.2f} {len(grp) * 100:6d} m  {key:20s} {grp[0][2]} / {grp[0][3]}")
