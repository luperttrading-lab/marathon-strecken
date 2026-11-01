# Wo liegt die Runde? Alle 50 Linienmeter: Gemeinde und Stadtteil (OSM admin_level 8 und 9: Gießen, Pohlheim, Hausen …), Wald- und
# Schutzflächen (landuse=forest, Naturschutzgebiet) und der nächste Flurname (OSM place=locality, z. B. „Sauweide“, „Rabennest“; so
# heißen die Waldstücke auf den Forstkarten). Die Flächen kommen einzeln über die OSM-API (api.openstreetmap.org/api/0.6/relation/<id>/full,
# eine Abfrage je Sekunde, ../dl/orte/), die Flurnamen aus den Kartenausschnitten von osm.py (../dl/osmapi/). Muster:
# werkzeuge/hannover/work/orte.py.
# -> orte.json [[Linienmeter, Gemeinde, Stadtteil, Wald, Schutzgebiet, Flurname, Abstand zum Flurnamen in m], …]
import glob, json, os, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
from matplotlib.path import Path
from pyproj import Transformer
T = Transformer.from_crs(4326, 25832, always_xy=True)
os.makedirs("../dl/orte", exist_ok=True)
ids = {}
for f in glob.glob("../dl/osmapi/t_*.xml"):
    for rel in ET.parse(f).getroot().iter("relation"):
        tg = {t.get("k"): t.get("v") for t in rel.iter("tag")}
        if (tg.get("boundary") == "administrative" and tg.get("admin_level") in ("8", "9")) or tg.get("landuse") == "forest" \
                or tg.get("leisure") == "nature_reserve" or tg.get("historic") == "monastery":
            ids[rel.get("id")] = tg
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
    art = ("a" + tg["admin_level"]) if tg.get("boundary") == "administrative" else "wald" if tg.get("landuse") == "forest" else \
          "nsg" if tg.get("leisure") == "nature_reserve" else "kloster"
    FL.append((tg.get("name", "") or "(ohne Namen)", art, A, I))
    print(f"  {rid:>9s} {art:7s} {tg.get('name', '')}")
# Wald als einfache Flächen (Wege mit landuse=forest / natural=wood) aus den Kartenausschnitten dazu
WALD = []
for f in glob.glob("../dl/osmapi/t_*.xml"):
    r = ET.parse(f).getroot(); kn = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in r.iter("node")}
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        refs = [x.get("ref") for x in w.iter("nd")]
        if (tg.get("landuse") == "forest" or tg.get("natural") == "wood") and len(refs) > 3 and refs[0] == refs[-1] and all(k in kn for k in refs):
            WALD.append(Path(np.array([kn[k] for k in refs])))
# Flurnamen
FLUR = {}
for f in glob.glob("../dl/osmapi/t_*.xml"):
    for n in ET.parse(f).getroot().iter("node"):
        tg = {t.get("k"): t.get("v") for t in n.iter("tag")}
        if tg.get("place") == "locality" and tg.get("name"): FLUR[n.get("id")] = (tg["name"], float(n.get("lon")), float(n.get("lat")))
fn = [v[0] for v in FLUR.values()]; fx, fy = T.transform([v[1] for v in FLUR.values()], [v[2] for v in FLUR.values()]); FX = np.c_[fx, fy]
print(len(FLUR), "Flurnamen:", ", ".join(sorted(set(fn))))
g = json.load(open("linie.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 50.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    drin = {}
    for n, art, A, I in FL:
        if any(a.contains_point((lo, la)) for a in A) and not any(i.contains_point((lo, la)) for i in I): drin.setdefault(art, n)
    wald = drin.get("wald") or ("Wald" if any(p.contains_point((lo, la)) for p in WALD) else "")
    x, y = T.transform(lo, la); dist = np.hypot(*(FX - [x, y]).T); j = int(np.argmin(dist))
    out.append([float(s), drin.get("a8", ""), drin.get("a9", ""), wald, drin.get("nsg", ""), fn[j], round(float(dist[j]))])
json.dump(out, open("orte.json", "w"), ensure_ascii=False)
from itertools import groupby
from common import official
for key, grp in groupby(out, key=lambda o: tuple(o[1:6])):
    grp = list(grp); print(f"km {float(official(grp[0][0])) / 1000:5.2f} {len(grp) * 50:5d} m  {' | '.join(key)}  ({min(o[6] for o in grp)}–{max(o[6] for o in grp)} m)")
