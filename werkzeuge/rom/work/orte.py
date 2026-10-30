# Ortsteil alle 100 m (Linienmeter): Rione, Quartiere oder Suburbio der Stadt Rom (die amtliche Gliederung nach Ortsnamen, „suddivisione
# toponomastica“: 22 Rioni in der Altstadt, 35 Quartieri, 6 Suburbi). In OSM als Relationen boundary=place mit ref „R. I“ … „Q. XX“ …
# „S. XI“ (osm.py fand ihre Kennungen in den Kacheln); die vollständigen Flächen kommen einzeln über die OSM-API
# (api.openstreetmap.org/api/0.6/relation/<id>/full, eine Abfrage je Sekunde, ../dl/orte/). Gewählt statt der 15 Municipi, weil das
# ganze Zentrum ein Municipio ist (Municipio I: von Testaccio bis Prati); die Rioni sind die Namen auf den Straßenschildern der Altstadt.
# -> orte2026.json [Linienmeter, Name, ref]
import glob, json, os, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
from matplotlib.path import Path
os.makedirs("../dl/orte", exist_ok=True)
ids = {}
for f in glob.glob("../dl/osmapi/t_*.xml"):
    for rel in ET.parse(f).getroot().iter("relation"):
        tg = {t.get("k"): t.get("v") for t in rel.iter("tag")}
        if tg.get("boundary") == "place" and tg.get("place") in ("quarter", "suburb") and tg.get("ref", "")[:2] in ("R.", "Q.", "S.", "XI"):
            ids[rel.get("id")] = tg
print(len(ids), "Flächen")
def ring_zusammen(wege):
    """Wege (Knotenlisten) zu geschlossenen Ringen verbinden"""
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
        open(f, "wb").write(urllib.request.urlopen(req, timeout=120).read()); time.sleep(1)
    r = ET.parse(f).getroot()
    kn = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in r.iter("node")}
    wg = {w.get("id"): [x.get("ref") for x in w.iter("nd")] for w in r.iter("way")}
    rel = [x for x in r.iter("relation") if x.get("id") == rid][0]
    aussen = [wg[m.get("ref")] for m in rel.iter("member") if m.get("type") == "way" and m.get("role") in ("outer", "") and m.get("ref") in wg]
    innen = [wg[m.get("ref")] for m in rel.iter("member") if m.get("type") == "way" and m.get("role") == "inner" and m.get("ref") in wg]
    A = [Path(np.array([kn[k] for k in ring])) for ring in ring_zusammen(aussen)]
    I = [Path(np.array([kn[k] for k in ring])) for ring in ring_zusammen(innen)]
    if not A: print("  keine Fläche:", tg.get("name")); continue
    FL.append((tg.get("name"), tg.get("ref", ""), A, I))
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])
    treffer = [(n, ref) for n, ref, A, I in FL if any(a.contains_point((lo, la)) for a in A) and not any(i.contains_point((lo, la)) for i in I)]
    out.append([float(s), treffer[0][0] if treffer else "", treffer[0][1] if treffer else ""])
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print([(k, len(list(v)) * 100) for k, v in groupby(o[1] for o in out)])
