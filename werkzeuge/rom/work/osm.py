# OSM-Straßennetz rund um die Strecke -> ../dl/osm_netz.json (Wege mit highway, ihre Knoten; Aufbau: {"ways": {id: [tags, [knoten…]]},
# "nodes": {id: [lat, lon]}}), dazu ../dl/osm_wasser.json (Tiber: natural=water / waterway=riverbank als Flächen, für clean.py).
# Overpass war am 30.10.2026 aus dieser Umgebung nicht nutzbar (overpass-api.de Verbindung abgebrochen, maps.mail.ru 504,
# kumi.systems und private.coffee Zeitüberschreitung). Deshalb über die OSM-API (api.openstreetmap.org/api/0.6/map) in Rechtecken
# von 0,005° (gut 550 × 420 m), eine Abfrage je Sekunde; Rohantworten in ../dl/osmapi/. Abgedeckt: das Rechteck um die ganze Strecke
# (Ostiense/Portuense im Süden bis Acqua Acetosa im Norden, Trionfale im Westen bis Colosseo im Osten). Die Linie baut linie.py.
import json, os, sys, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.005
FLAECHE = (41.855, 41.945, 12.440, 12.500)
def kacheln():
    la0, la1, lo0, lo1 = FLAECHE
    return sorted((i, j) for i in range(int(np.floor(la0 / S)), int(np.ceil(la1 / S))) for j in range(int(np.floor(lo0 / S)), int(np.ceil(lo1 / S))))
KS = kacheln()
print(len(KS), "Rechtecke", flush=True)
knoten, wege, wasser_w, wasser_r, alle = {}, {}, {}, {}, {}
for n, (i, j) in enumerate(KS):
    f = f"{CACHE}/t_{i}_{j}.xml"
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        bb = (j * S, i * S, (j + 1) * S, (i + 1) * S)
        url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + ",".join(f"{v:.4f}" for v in bb)
        for att in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
                data = urllib.request.urlopen(req, timeout=180).read(); open(f, "wb").write(data); break
            except Exception as e: print("  Fehler", n, e, flush=True); time.sleep(5 + 10 * att)
        time.sleep(1)
    r = ET.parse(f).getroot()
    for nd in r.iter("node"): knoten[int(nd.get("id"))] = (float(nd.get("lat")), float(nd.get("lon")))
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        refs = [int(x.get("ref")) for x in w.iter("nd")]
        alle[int(w.get("id"))] = refs
        if "highway" in tg: wege[int(w.get("id"))] = (tg, refs)
        if tg.get("natural") == "water" or tg.get("waterway") == "riverbank" or tg.get("water") == "river": wasser_w[int(w.get("id"))] = (tg, refs)
    for rel in r.iter("relation"):
        tg = {t.get("k"): t.get("v") for t in rel.iter("tag")}
        if tg.get("natural") == "water" or tg.get("waterway") == "riverbank":
            wasser_r[int(rel.get("id"))] = (tg, [(m.get("role"), int(m.get("ref"))) for m in rel.iter("member") if m.get("type") == "way"])
    if n % 20 == 0: print(f"{n}/{len(KS)}: {len(wege)} Wege", flush=True)
benutzt = {k for _, refs in wege.values() for k in refs}
json.dump({"ways": {str(k): v for k, v in wege.items()}, "nodes": {str(k): knoten[k] for k in benutzt if k in knoten}},
          open("../dl/osm_netz.json", "w"), ensure_ascii=False)
# Wasserflächen: geschlossene Wege und die Außenringe der Relationen (Teilwege, soweit in den Rechtecken enthalten)
for _, mm in wasser_r.values():
    for _, wid in mm:
        if wid in alle and wid not in wasser_w: wasser_w[wid] = ({}, alle[wid])
wb = {k for _, refs in wasser_w.values() for k in refs}
json.dump({"ways": {str(k): v for k, v in wasser_w.items()}, "relations": {str(k): v for k, v in wasser_r.items()},
           "nodes": {str(k): knoten[k] for k in wb if k in knoten}}, open("../dl/osm_wasser.json", "w"), ensure_ascii=False)
print(len(wege), "Wege,", len(benutzt), "Knoten;", len(wasser_w), "Wasserwege,", len(wasser_r), "Wasserrelationen")
