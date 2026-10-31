# OSM-Wege entlang der Strecke -> ../dl/osm_netz.json ({"ways": {id: [tags, [knoten…]]}, "nodes": {id: [lat, lon]},
# alle Wege mit highway sowie Bahn- und Wasserwege, dazu Knoten mit Tags in "punkte"). Kopie von werkzeuge/duesseldorf/work/osm.py:
# über die OSM-API (api.openstreetmap.org/api/0.6/map) in Rechtecken von 0,005° (gut 555 × 345 m), nur die Rechtecke höchstens
# 300 m neben der grob eingepassten Planlinie (grob.json, auf etwa 70 m genau), eine Abfrage je Sekunde, bei 509/429 warten und
# wiederholen, Rohantworten in ../dl/osmapi/.
import json, os, time, urllib.request, urllib.error, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.005
Ti = Transformer.from_crs(25832, 4326, always_xy=True)
P = np.array(json.load(open("plan_pdf.json"))["pts"]); M = np.array(json.load(open("grob.json"))["M"])
X = np.c_[P, np.ones(len(P))] @ M
s = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; dd = np.arange(0, s[-1], 20.0)
lo, la = Ti.transform(np.interp(dd, s, X[:, 0]), np.interp(dd, s, X[:, 1]))
# Rechtecke im Umkreis von 300 m (0,0027° Breite, 0,0044° Länge bei 52° N)
KS = set()
for a, b in zip(la, lo):
    for da in (-0.0027, 0, 0.0027):
        for db in (-0.0044, 0, 0.0044): KS.add((int(np.floor((a + da) / S)), int(np.floor((b + db) / S))))
KS = sorted(KS)
print(len(KS), "Rechtecke", flush=True)
knoten, wege, punkte, rels = {}, {}, {}, {}
for n, (i, j) in enumerate(KS):
    f = f"{CACHE}/t_{i}_{j}.xml"
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        bb = (j * S, i * S, (j + 1) * S, (i + 1) * S)
        url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + ",".join(f"{v:.4f}" for v in bb)
        for att in range(6):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
                data = urllib.request.urlopen(req, timeout=180).read(); open(f, "wb").write(data); break
            except urllib.error.HTTPError as e:
                print("  HTTP", e.code, n, flush=True); time.sleep(30 if e.code in (429, 509) else 5 + 10 * att)
            except Exception as e: print("  Fehler", n, e, flush=True); time.sleep(5 + 10 * att)
        time.sleep(1)
    r = ET.parse(f).getroot()
    for nd in r.iter("node"):
        k = int(nd.get("id")); knoten[k] = (float(nd.get("lat")), float(nd.get("lon")))
        tg = {t.get("k"): t.get("v") for t in nd.iter("tag")}
        if tg and any(x in tg for x in ("highway", "railway", "ele", "distance", "milestone", "name")): punkte[k] = [tg, knoten[k]]
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        refs = [int(x.get("ref")) for x in w.iter("nd")]
        if any(x in tg for x in ("highway", "railway", "waterway")) or tg.get("natural") == "water" or tg.get("man_made") == "bridge":
            wege[int(w.get("id"))] = (tg, refs)
    if n % 20 == 0: print(f"{n}/{len(KS)}: {len(wege)} Wege", flush=True)
benutzt = {k for _, refs in wege.values() for k in refs}
json.dump({"ways": {str(k): v for k, v in wege.items()}, "nodes": {str(k): knoten[k] for k in benutzt if k in knoten},
           "punkte": {str(k): v for k, v in punkte.items()}}, open("../dl/osm_netz.json", "w"), ensure_ascii=False)
print(len(wege), "Wege,", len(benutzt), "Knoten,", len(punkte), "Punkte mit Tags")
