# OSM-Wege entlang der Strecke -> ../dl/osm_netz.json ({"ways": {id: [tags, [knoten…]]}, "nodes": {id: [lat, lon]}, "punkte": {…},
# "rel": {id: [tags, [Weg-IDs]]}}), alle Wege mit highway sowie Bahn- und Wasserwege, Knoten mit Tags und Routen-Relationen (Wanderwege).
# Über die OSM-API (api.openstreetmap.org/api/0.6/map) in Rechtecken von 0,005° (556 × 380 m auf 47,1° Breite), alle Rechtecke höchstens
# 450 m neben der Linie des Streckenplans (plan.py; Grafik mit bis 150 m Lagefehler), eine Abfrage je Sekunde, bei 509/429 warten und
# wiederholen; Rohantworten in ../dl/osmapi/ (Muster: werkzeuge/zermatt/work/osm.py). Overpass war aus dieser Umgebung nicht erreichbar.
import json, os, sys, time, urllib.request, urllib.error, xml.etree.ElementTree as ET
NUR_CACHE = "--cache" in sys.argv          # zum Ausprobieren: nur schon geladene Rechtecke
import numpy as np
from pyproj import Transformer
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.005
TI = Transformer.from_crs(2056, 4326, always_xy=True)
pl = np.array(json.load(open("../dl/plan_lv95.json"))["lv95"])[::5]
lo, la = TI.transform(pl[:, 0], pl[:, 1])
KS = set()
for a, b in zip(la, lo):
    for da in np.linspace(-0.0041, 0.0041, 5):          # ±450 m Breite
        for db in np.linspace(-0.006, 0.006, 5):        # ±450 m Länge
            KS.add((int(np.floor((a + da) / S)), int(np.floor((b + db) / S))))
KS = sorted(KS)
print(len(KS), "Rechtecke", flush=True)
knoten, wege, punkte, rel = {}, {}, {}, {}
for n, (i, j) in enumerate(KS):
    f = f"{CACHE}/t_{i}_{j}.xml"
    if NUR_CACHE and not os.path.exists(f): continue
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        bb = (j * S, i * S, (j + 1) * S, (i + 1) * S)
        url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + ",".join(f"{v:.4f}" for v in bb)
        for att in range(8):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
                data = urllib.request.urlopen(req, timeout=180).read(); open(f, "wb").write(data); break
            except urllib.error.HTTPError as e:
                print("  HTTP", e.code, n, flush=True); time.sleep(15 + 20 * att)
            except Exception as e:
                print("  Fehler", n, e, flush=True); time.sleep(5 + 10 * att)
        time.sleep(1)
    r = ET.parse(f).getroot()
    for nd in r.iter("node"):
        k = int(nd.get("id")); knoten[k] = (float(nd.get("lat")), float(nd.get("lon")))
        tg = {t.get("k"): t.get("v") for t in nd.iter("tag")}
        if tg and any(x in tg for x in ("highway", "railway", "ele", "distance", "milestone", "name", "amenity", "barrier")): punkte[k] = [tg, knoten[k]]
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        refs = [int(x.get("ref")) for x in w.iter("nd")]
        if any(x in tg for x in ("highway", "railway", "waterway")) or tg.get("natural") == "water" or tg.get("man_made") == "bridge":
            wege[int(w.get("id"))] = (tg, refs)
    for re_ in r.iter("relation"):
        tg = {t.get("k"): t.get("v") for t in re_.iter("tag")}
        if tg.get("type") == "route":
            rel.setdefault(int(re_.get("id")), [tg, []])
            rel[int(re_.get("id"))][1] = sorted(set(rel[int(re_.get("id"))][1]) | {int(m.get("ref")) for m in re_.iter("member") if m.get("type") == "way"})
    if n % 25 == 0: print(f"{n}/{len(KS)}: {len(wege)} Wege", flush=True)
benutzt = {k for _, refs in wege.values() for k in refs}
json.dump({"ways": {str(k): v for k, v in wege.items()}, "nodes": {str(k): knoten[k] for k in benutzt if k in knoten},
           "punkte": {str(k): v for k, v in punkte.items()}, "rel": {str(k): v for k, v in rel.items()}},
          open("../dl/osm_netz_teil.json" if NUR_CACHE else "../dl/osm_netz.json", "w"), ensure_ascii=False)
print(len(wege), "Wege,", len(benutzt), "Knoten,", len(punkte), "Punkte mit Tags,", len(rel), "Routen")
