# OSM-Wege im Gebiet der Strecke -> ../dl/osm_netz.json ({"ways": {id: [tags, [knoten…]]}, "nodes": {id: [lat, lon]}, "punkte": …},
# alle Wege mit highway sowie Bahn- und Wasserwege, dazu Knoten mit Tags). Overpass war am 31.10.2026 aus dieser Umgebung nicht nutzbar
# (overpass-api.de Verbindung abgebrochen, maps.mail.ru 504, kumi.systems und private.coffee Zeitüberschreitung); deshalb wie in Athen
# und Stockholm über die OSM-API (api.openstreetmap.org/api/0.6/map) in Rechtecken von 0,005° (gut 475 × 555 m), eine Abfrage je Sekunde,
# Rohantworten in ../dl/osmapi/.
# Eine GPX-Datei der Strecke gibt es nicht (siehe UEBERGABE.md); das Gebiet folgt deshalb beim ersten Lauf einer groben Linie durch
# bekannte Punkte der Strecke (KORRIDOR, 1,2 km breit nach jeder Seite), danach – sobald linie.py die Linie gebaut hat – der Linie
# selbst (300 m nach jeder Seite). OSM-Koordinaten sind WGS 84 (keine GCJ-02-Verschiebung).
import json, os, time, urllib.request, xml.etree.ElementTree as ET
import numpy as np
CACHE = "../dl/osmapi"; os.makedirs(CACHE, exist_ok=True)
S = 0.005
# grobe Punkte (lat, lon): Bund, Xinkaihe Lu, Henan Zhonglu, Nanjing Donglu, Jing'an-Tempel, Changshu Lu/Huaihai Zhonglu, Xintiandi,
# Xizang Nanlu, Lujiabang Lu, Longhua Donglu, Ruining Lu, Longteng Dadao bis zur Wende, Longhua-Tempel, Xujiahui-Sportpark
KORRIDOR = [(31.2400, 121.4900), (31.2275, 121.4935), (31.2282, 121.4855), (31.2395, 121.4855), (31.2300, 121.4700), (31.2235, 121.4455),
            (31.2135, 121.4475), (31.2195, 121.4745), (31.2245, 121.4855), (31.2000, 121.4880), (31.2045, 121.4995), (31.1960, 121.4840),
            (31.1830, 121.4620), (31.1650, 121.4600), (31.1480, 121.4560), (31.1755, 121.4473), (31.1834, 121.4358)]
if os.path.exists("linie.json"):
    L = json.load(open("linie.json")); pts = np.array([[p[0], p[1]] for p in L["wgs"]]); puf = 300.0
else:
    k = np.array(KORRIDOR); pts = np.vstack([k[i] + (k[i + 1] - k[i]) * f for i in range(len(k) - 1) for f in np.linspace(0, 1, 60)]); puf = 1200.0
dla = puf / 111320; dlo = puf / (111320 * np.cos(np.radians(31.2)))
KS = set()
for a, b in pts:
    for da in np.linspace(-dla, dla, 5):
        for db in np.linspace(-dlo, dlo, 5): KS.add((int(np.floor((a + da) / S)), int(np.floor((b + db) / S))))
KS = sorted(KS)
print(len(KS), "Rechtecke", flush=True)
knoten, wege, punkte = {}, {}, {}
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
    for nd in r.iter("node"):
        k = int(nd.get("id")); knoten[k] = (float(nd.get("lat")), float(nd.get("lon")))
        tg = {t.get("k"): t.get("v") for t in nd.iter("tag")}
        if tg and any(x in tg for x in ("highway", "railway", "ele", "distance", "milestone", "name")): punkte[k] = [tg, knoten[k]]
    for w in r.iter("way"):
        tg = {t.get("k"): t.get("v") for t in w.iter("tag")}
        refs = [int(x.get("ref")) for x in w.iter("nd")]
        if any(x in tg for x in ("highway", "railway", "waterway")) or tg.get("natural") == "water" or tg.get("man_made") == "bridge" \
                or tg.get("leisure") in ("stadium", "sports_centre", "track", "park") or tg.get("building") == "stadium":
            wege[int(w.get("id"))] = (tg, refs)
    if n % 25 == 0: print(f"{n}/{len(KS)}: {len(wege)} Wege", flush=True)
benutzt = {k for _, refs in wege.values() for k in refs}
json.dump({"ways": {str(k): v for k, v in wege.items()}, "nodes": {str(k): knoten[k] for k in benutzt if k in knoten},
           "punkte": {str(k): v for k, v in punkte.items()}}, open("../dl/osm_netz.json", "w"), ensure_ascii=False)
print(len(wege), "Wege,", len(benutzt), "Knoten,", len(punkte), "Punkte mit Tags")
