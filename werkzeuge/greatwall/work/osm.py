# OSM rund um die Strecke -> ../dl/osm_all.json: alle Wege mit Tags und Knoten (Straßen, Pfade, Treppen, Mauer, Flüsse, Orte),
# dazu die Knoten mit Tags (Dörfer, Türme). Overpass war am 30.10.2026 aus dieser Umgebung nicht erreichbar (overpass-api.de
# Verbindung abgebrochen), deshalb über die OSM-API (api.openstreetmap.org/api/0.6/map) in Rechtecken von 0,02° (gut
# 2,2 × 1,7 km; die Gegend ist dünn erfasst), eine Abfrage je Sekunde; Rohantworten in ../dl/osmapi/.
# Abgedeckt: 40,10–40,32° N, 117,33–117,59° O (Huangyaguan bis Xiaying und Baitan mit Rand, so weit wie die Kartenstufen 12/13).
import json, os, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.02
FLAECHE = (40.10, 40.32, 117.33, 117.59)
la0, la1, lo0, lo1 = FLAECHE
KS = [(round(la0 + i * S, 4), round(lo0 + j * S, 4)) for i in range(int(round((la1 - la0) / S))) for j in range(int(round((lo1 - lo0) / S)))]
print(len(KS), "Rechtecke", flush=True)
knoten, ntags, wege = {}, {}, {}
for n, (la, lo) in enumerate(KS):
    f = f"{CACHE}/t_{la:.2f}_{lo:.2f}.xml"
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        url = f"https://api.openstreetmap.org/api/0.6/map?bbox={lo:.4f},{la:.4f},{lo + S:.4f},{la + S:.4f}"
        for att in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time download)"})
                data = urllib.request.urlopen(req, timeout=180).read(); open(f, "wb").write(data); break
            except Exception as e: print("  Fehler", n, e, flush=True); time.sleep(5 + 10 * att)
        time.sleep(1)
    r = ET.parse(f).getroot()
    for nd in r.iter("node"):
        i = int(nd.get("id")); knoten[i] = (float(nd.get("lat")), float(nd.get("lon")))
        tg = {t.get("k"): t.get("v") for t in nd.iter("tag")}
        if tg: ntags[i] = tg
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        wege[int(w.get("id"))] = (tg, [int(x.get("ref")) for x in w.iter("nd")])
    if n % 10 == 0: print(f"{n}/{len(KS)}: {len(wege)} Wege", flush=True)
benutzt = {k for _, refs in wege.values() for k in refs} | set(ntags)
json.dump({"ways": {str(k): v for k, v in wege.items()}, "nodes": {str(k): knoten[k] for k in benutzt if k in knoten},
           "ntags": {str(k): v for k, v in ntags.items()}}, open("../dl/osm_all.json", "w"), ensure_ascii=False)
print(len(wege), "Wege,", len(benutzt), "Knoten,", len(ntags), "Knoten mit Tags")
