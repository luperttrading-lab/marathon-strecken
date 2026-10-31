# OSM-Wege entlang der Strecke -> ../dl/osm_netz.json ({"ways": {id: [tags, [knoten…]]}, "nodes": {id: [lat, lon]}, "punkte": {…}}),
# alle Wege mit highway sowie Bahn- und Wasserwege, dazu Knoten mit Tags. Über die OSM-API (api.openstreetmap.org/api/0.6/map) in
# Rechtecken von 0,005° (556 × 380 m auf 47,0° Breite), nur die Rechtecke höchstens 150 m neben der GPX-Linie, eine Abfrage je Sekunde,
# bei 509/429 warten und wiederholen; Rohantworten in ../dl/osmapi/ (Kopie von werkzeuge/zuerich/work/osm.py).
import json, os, time, urllib.request, urllib.error, xml.etree.ElementTree as ET
import numpy as np
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.005
g = json.load(open("gpx2026.json")); P = np.array([[p[0], p[1]] for p in g["pts"]]); d = np.array(g["d"])
# Linie alle 20 m, Rechtecke im Umkreis von 150 m (0,00135° Breite, 0,00199° Länge auf 47,0° Breite)
dd = np.arange(0, d[-1], 20.0); la = np.interp(dd, d, P[:, 0]); lo = np.interp(dd, d, P[:, 1])
KS = set()
for a, b in zip(la, lo):
    for da in (-0.00135, 0, 0.00135):
        for db in (-0.00199, 0, 0.00199): KS.add((int(np.floor((a + da) / S)), int(np.floor((b + db) / S))))
KS = sorted(KS)
print(len(KS), "Rechtecke", flush=True)
knoten, wege, punkte = {}, {}, {}
for n, (i, j) in enumerate(KS):
    f = f"{CACHE}/t_{i}_{j}.xml"
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
        if tg and any(x in tg for x in ("highway", "railway", "ele", "distance", "milestone", "name", "amenity")): punkte[k] = [tg, knoten[k]]
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
