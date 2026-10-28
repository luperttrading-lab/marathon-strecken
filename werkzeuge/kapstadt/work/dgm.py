# Bodenhöhen alle 10 m (Linienmeter) aus dem Geländemodell der Stadt Kapstadt: CCT Ground Level Map 2019, 5 m, aus den
# Laserscans 2018/2019 (bare earth, ±0,3 m, Höhen über SA Land Levelling Datum). Abgefragt Punkt für Punkt über
# GetFeatureInfo des WMS (ERDAS APOLLO), der neben der Graustufe den Rohwert liefert („raw“, Band 0, 0,1 m). -> dgm2026_10m.json
import json, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
WMS = "https://cityimg.capetown.gov.za/erdas-iws/ogc/wms/GeoSpatial%20Datasets"
L = "Elevation_CCT_GLM2019_5m_DEM"
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
def q(i):
    a, b = la[i], lo[i]; e = 0.0004   # Kasten ±0,0004°, 81 × 81 Bildpunkte, Mitte = Punkt
    url = (f"{WMS}?service=WMS&version=1.3.0&request=GetFeatureInfo&layers={L}&query_layers={L}&styles=&crs=EPSG:4326"
           f"&bbox={a - e:.7f},{b - e:.7f},{a + e:.7f},{b + e:.7f}&width=81&height=81&i=40&j=40&format=image/png&info_format=application/json")
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(url, timeout=40))
            v = r["layers"][0]["raw"]["bands"][0]["value"]
            return i, (None if v is None or v < -100 else float(v))
        except Exception: time.sleep(1 + 2 * att)
    return i, None
t0 = time.time(); H = [None] * len(ss)
with cf.ThreadPoolExecutor(8) as ex:
    for i, v in ex.map(q, range(len(ss))): H[i] = v
res = [[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", sum(r[3] is None for r in res))
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open("dgm2026_10m.json", "w"))
