# Hochstraßen und Brücken messen statt schätzen: auf den Stücken, die OSM als Brücke führt (../dl/kanten.json, je 10 m Zugabe),
# Fahrbahn = Gelände (LiDAR2025 2 m DTM) + Höhe über Grund (LiDAR2025 Height Map 1 m, normalisiertes Oberflächenmodell) der
# Stadt Kapstadt, beide über GetFeatureInfo des WMS. Höhe über Grund unter 1,5 m zählt als Boden. Auf den Rampen davor und danach
# (100 m) nur das DTM 2025: es zeigt die aufgeschütteten Rampen, das Stadtmodell 2019 (GLM) nicht; die Höhe über Grund dort wäre
# oft eine Überführung über den Läufern (km 3,3). Fahrzeuge und Laternen: gleitender Median über 50 m.
# Sonst das Geländemodell aus dgm.py. -> lidar.json {"h": [...], "deck": [[i, DTM, über Grund], ...]}
import json, time, urllib.request, concurrent.futures as cf
import numpy as np
W = "https://cityimg.capetown.gov.za/erdas-iws/ogc/wms/GeoSpatial%20Datasets"
r = json.load(open("dgm2026_10m.json")); s = np.array([x[0] for x in r]); h = np.array([np.nan if x[3] is None else x[3] for x in r])
g = json.load(open("gpx2026.json")); dg = np.array(g["d"]); kan = json.load(open("../dl/kanten.json"))
zone = np.zeros(len(s), bool); bruecke = np.zeros(len(s), bool)
for i_, b in enumerate(kan["bridge"]):
    if b and b != "no": zone[(s >= dg[i_] - 100) & (s <= dg[i_ + 1] + 100)] = True; bruecke[(s >= dg[i_] - 10) & (s <= dg[i_ + 1] + 10)] = True
idx = np.where(zone)[0]; print(len(idx), "Punkte auf Brücken und Hochstraßen")
def wert(L, a, b):
    e = 0.0002
    u = (f"{W}?service=WMS&version=1.3.0&request=GetFeatureInfo&layers={L}&query_layers={L}&styles=&crs=EPSG:4326"
         f"&bbox={a - e:.7f},{b - e:.7f},{a + e:.7f},{b + e:.7f}&width=81&height=81&i=40&j=40&format=image/png&info_format=application/json")
    for att in range(5):
        try:
            bands = json.load(urllib.request.urlopen(u, timeout=40))["layers"][0]["raw"]["bands"]
            return float(bands[0]["value"]), float(bands[1]["value"]) if len(bands) > 1 else 255.0
        except Exception: time.sleep(1 + 2 * att)
    return np.nan, 0.0
def q(i):
    a, b = r[i][1], r[i][2]
    dtm, _ = wert("Elevation_DTM_2m", a, b); hoch, maske = wert("Elevation_Height_Map_1m", a, b)
    return i, dtm, (hoch if maske > 0 else 0.0)
deck = {}
with cf.ThreadPoolExecutor(8) as ex:
    for i, dtm, hoch in ex.map(q, idx): deck[int(i)] = (dtm, hoch)
hh = h.copy(); roh = {}
for i in idx:
    dtm, hoch = deck[int(i)]
    roh[int(i)] = dtm + hoch if hoch > 1.5 and bruecke[i] else dtm
# Median über 50 m (5 Punkte) innerhalb jeder Zone
for i in idx:
    nb = [roh[j] for j in range(i - 2, i + 3) if j in roh and not np.isnan(roh[j])]
    if nb: hh[i] = float(np.median(nb))
json.dump({"h": [None if np.isnan(v) else float(v) for v in hh], "deck": [[int(i), deck[int(i)][0], deck[int(i)][1]] for i in idx]}, open("lidar.json", "w"))
for i in idx[::10]: print(f"  {s[i]:7.0f} m  Gelände {h[i]:5.1f}  DTM2025 {deck[int(i)][0]:5.1f}  über Grund {deck[int(i)][1]:5.1f}  ->  {hh[i]:5.1f}")
