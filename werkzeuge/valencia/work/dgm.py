# Bodenhöhen alle 10 m (Linienmeter) aus dem MDT02 des IGN (PNOA-LiDAR, zweite Befliegung, 2-m-Raster aus den Bodenpunkten,
# Klasse 2) über den INSPIRE-WMS des IGN (servicios.idee.es/wms-inspire/mdt, Ebene EL.ElevationGridCoverage), GetFeatureInfo
# je Punkt (Antwort „MDT02_H30“, GRAY_INDEX in Metern mit Nachkommastellen). Höhen orthometrisch über dem Meer (REDNAP,
# Pegel Alicante; Geoid EGM08-REDNAP). Der WCS desselben Dienstes (Elevacion25830_5) liefert nur auf ganze Meter gerundete
# Werte und taugt für eine flache Strecke nicht. Das Netz bricht hier oft ab (Connection reset): Wiederholungen, Zwischenstand
# in ../dl/mdt02_cache.json. -> dgm2026_10m.json [Linienmeter, Breite, Länge, Höhe]
import json, os, re, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 25830, always_xy=True)
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
CACHE = "../dl/mdt02_cache.json"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
URL = ("https://servicios.idee.es/wms-inspire/mdt?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&LAYERS=EL.ElevationGridCoverage"
       "&QUERY_LAYERS=EL.ElevationGridCoverage&STYLES=&CRS=EPSG:25830&BBOX={x0:.2f},{y0:.2f},{x1:.2f},{y1:.2f}&WIDTH=3&HEIGHT=3&I=1&J=1"
       "&INFO_FORMAT=text/plain&FEATURE_COUNT=1")
def frage(xy):
    x, y = xy; key = f"{x:.2f},{y:.2f}"
    if key in cache: return key, cache[key]
    for att in range(12):
        try:
            req = urllib.request.Request(URL.format(x0=x - 1, y0=y - 1, x1=x + 1, y1=y + 1), headers={"User-Agent": "marathon-profile-check/1.0"})
            t = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
            m = re.search(r"FeatureType '[^']*:([^']+)'.*?GRAY_INDEX = ([-\d.eE]+)", t, re.S)
            if m: return key, [float(m.group(2)), m.group(1)]
            if "Results for FeatureType" not in t: raise ValueError(t[:200])
            return key, [None, ""]
        except Exception as e:
            time.sleep(1 + att)
    return key, None
xy = [T.transform(b, a) for a, b in zip(la, lo)]
t0 = time.time(); n = 0
with cf.ThreadPoolExecutor(8) as ex:
    for key, v in ex.map(frage, xy):
        if v is not None: cache[key] = v
        n += 1
        if n % 200 == 0:
            json.dump(cache, open(CACHE, "w")); print(n, "von", len(xy), round(time.time() - t0), "s", flush=True)
json.dump(cache, open(CACHE, "w"))
res, quelle, fehlt = [], {}, 0
for s, a, b, (x, y) in zip(ss, la, lo, xy):
    v = cache.get(f"{x:.2f},{y:.2f}")
    if v is None or v[0] is None or v[0] < -100: fehlt += 1; res.append([float(s), float(a), float(b), None]); continue
    quelle[v[1]] = quelle.get(v[1], 0) + 1; res.append([float(s), float(a), float(b), v[0]])
print(len(res), "Punkte in", round(time.time() - t0), "s; Quellen:", quelle, "fehlend:", fehlt)
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 2), round(max(hv), 2))
if fehlt: sys.exit("Es fehlen Höhen: dgm.py noch einmal starten")
json.dump(res, open("dgm2026_10m.json", "w"))
