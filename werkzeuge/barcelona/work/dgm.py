# Bodenhöhen alle 10 m (Linienmeter) per WMS-GetFeatureInfo je Punkt. Aufruf: python3 dgm.py [quelle]
#   amb25 (Standard, genommen): „Model d'elevacions del terreny de l'àrea metropolitana de Barcelona 25cm provinent de Lidar 2022“
#          im Servei WMS d'elevacions territorial des ICGC (geoserveis.icgc.cat/servei/catalunya/elevacions-territorial/wms), ohne
#          Anmeldung, Antwort value_0 in m mit Nachkommastellen;
#   icgc50 / icgc1: Geländemodell Katalonien 50 cm bzw. 1 m (LiDAR 2021–2023), gleicher Dienst;
#   ign2   : IGN MDT02 (PNOA-LiDAR, zweite Abdeckung, 2-m-Raster) über den INSPIRE-WMS des IGN (servicios.idee.es/wms-inspire/mdt), wie Valencia.
# Alle in EPSG:25831 abgefragt, Höhen über dem Meer (Pegel Alicante; die Modelle stimmen entlang der Linie auf Zentimeter überein,
# vergleich_dgm.py). Zwischenstand je Quelle in ../dl/dgm_<quelle>_cache.json.
# -> dgm2026_10m.json (nur amb25) bzw. ../dl/dgm_<quelle>_10m.json [Linienmeter, Breite, Länge, Höhe]
import json, os, re, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from pyproj import Transformer
Q = sys.argv[1] if len(sys.argv) > 1 else "amb25"
ICGC = ("https://geoserveis.icgc.cat/servei/catalunya/elevacions-territorial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo"
        "&LAYERS={L}&QUERY_LAYERS={L}&STYLES=&CRS=EPSG:25831&BBOX={x0:.2f},{y0:.2f},{x1:.2f},{y1:.2f}&WIDTH=3&HEIGHT=3&I=1&J=1"
        "&INFO_FORMAT=text/plain&FEATURE_COUNT=1")
IGN = ("https://servicios.idee.es/wms-inspire/mdt?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&LAYERS=EL.ElevationGridCoverage"
       "&QUERY_LAYERS=EL.ElevationGridCoverage&STYLES=&CRS=EPSG:25831&BBOX={x0:.2f},{y0:.2f},{x1:.2f},{y1:.2f}&WIDTH=3&HEIGHT=3&I=1&J=1"
       "&INFO_FORMAT=text/plain&FEATURE_COUNT=1")
QUELLEN = {"icgc50": (ICGC, "model-elevacions-terreny-catalunya-lidar-50cm-2021-2023", 0.25),
           "icgc1": (ICGC, "model-elevacions-terreny-catalunya-lidar-1m-2021-2023", 0.5),
           "amb25": (ICGC, "model-elevacions-terreny-amb-lidar-25cm-2022", 0.125),
           "ign2": (IGN, "", 1.0)}
URL, LAYER, HALB = QUELLEN[Q]       # halbe Kantenlänge des 3×3-Rechtecks: mittleres Pixel etwa eine Rasterzelle
T = Transformer.from_crs(4326, 25831, always_xy=True)
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
CACHE = f"../dl/dgm_{Q}_cache.json"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def frage(xy):
    x, y = xy; key = f"{x:.2f},{y:.2f}"
    if key in cache: return key, cache[key]
    for att in range(12):
        try:
            u = URL.format(L=LAYER, x0=x - 3 * HALB, y0=y - 3 * HALB, x1=x + 3 * HALB, y1=y + 3 * HALB)
            t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=40).read().decode("utf-8", "replace")
            m = re.search(r"value_0 = '([-\d.eE]+)'", t) or re.search(r"GRAY_INDEX = ([-\d.eE]+)", t)
            if m: return key, float(m.group(1))
            if "Feature" not in t and "Results for" not in t: raise ValueError(t[:200])
            return key, None
        except Exception as e:
            time.sleep(1 + att)
    return key, "fehlt"
xy = [T.transform(b, a) for a, b in zip(la, lo)]
t0 = time.time(); n = 0
with cf.ThreadPoolExecutor(6) as ex:
    for key, v in ex.map(frage, xy):
        if v != "fehlt": cache[key] = v
        n += 1
        if n % 250 == 0:
            json.dump(cache, open(CACHE, "w")); print(Q, n, "von", len(xy), round(time.time() - t0), "s", flush=True)
json.dump(cache, open(CACHE, "w"))
res, fehlt = [], 0
for s, a, b, (x, y) in zip(ss, la, lo, xy):
    v = cache.get(f"{x:.2f},{y:.2f}")
    if v is None or v < -100: fehlt += 1; res.append([float(s), float(a), float(b), None]); continue
    res.append([float(s), float(a), float(b), v])
hv = [r[3] for r in res if r[3] is not None]
print(Q, len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", fehlt, "Höhe min/max", round(min(hv), 2), round(max(hv), 2))
if fehlt: sys.exit("Es fehlen Höhen: dgm.py noch einmal starten")
json.dump(res, open("dgm2026_10m.json" if Q == "amb25" else f"../dl/dgm_{Q}_10m.json", "w"))
