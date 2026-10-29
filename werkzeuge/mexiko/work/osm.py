# OSM-Straßennetz rund um die Strecke -> ../dl/osm_netz.json (Wege mit highway, ihre Knoten; Aufbau: {"ways": {id: [tags, [knoten…]]},
# "nodes": {id: [lat, lon]}}). Overpass war am 29.10.2026 aus dieser Umgebung wieder nicht nutzbar (overpass-api.de Verbindung
# abgebrochen, maps.mail.ru, kumi.systems und private.coffee Zeitüberschreitung). Deshalb über die OSM-API
# (api.openstreetmap.org/api/0.6/map) in Rechtecken von 0,004° (gut 400 m), eine Abfrage je Sekunde; Rohantworten in ../dl/osmapi/.
# Abgedeckt: Insurgentes Sur von Ciudad Universitaria bis zur Glorieta de Insurgentes (450 m beiderseits der Achse), Roma/Condesa,
# Bosque de Chapultepec und Polanco, Reforma bis zum Zócalo (Rechtecke). Die Linie selbst baut linie.py aus diesem Netz.
import json, os, sys, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.004
FLAECHEN = [(19.403, 19.427, -99.181, -99.159),    # Roma, Condesa, Hipódromo
            (19.413, 19.446, -99.211, -99.163),    # Bosque de Chapultepec (1. Sektion), Polanco, Anzures, Granada
            (19.425, 19.444, -99.165, -99.129)]    # Reforma, Tabacalera, Centro bis zum Zócalo
ACHSE = [(19.3290, -99.1910), (19.3470, -99.1880), (19.3610, -99.1840), (19.3787, -99.1785), (19.3935, -99.1745), (19.4020, -99.1705), (19.4100, -99.1660)]
def kacheln():
    ks = set()
    for la0, la1, lo0, lo1 in FLAECHEN:
        for i in range(int(np.floor(la0 / S)), int(np.ceil(la1 / S))):
            for j in range(int(np.floor(lo0 / S)), int(np.ceil(lo1 / S))): ks.add((i, j))
    for (a0, b0), (a1, b1) in zip(ACHSE[:-1], ACHSE[1:]):
        for f in np.linspace(0, 1, 40):
            la, lo = a0 + f * (a1 - a0), b0 + f * (b1 - b0)
            for dla in (-0.0042, 0, 0.0042):
                for dlo in (-0.0045, 0, 0.0045): ks.add((int(np.floor((la + dla) / S)), int(np.floor((lo + dlo) / S))))
    return sorted(ks)
KS = kacheln()
print(len(KS), "Rechtecke", flush=True)
knoten, wege = {}, {}
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
        if "highway" in tg: wege[int(w.get("id"))] = (tg, [int(x.get("ref")) for x in w.iter("nd")])
    if n % 20 == 0: print(f"{n}/{len(KS)}: {len(wege)} Wege", flush=True)
benutzt = {k for _, refs in wege.values() for k in refs}
json.dump({"ways": {str(k): v for k, v in wege.items()}, "nodes": {str(k): knoten[k] for k in benutzt if k in knoten}},
          open("../dl/osm_netz.json", "w"), ensure_ascii=False)
print(len(wege), "Wege,", len(benutzt), "Knoten")
