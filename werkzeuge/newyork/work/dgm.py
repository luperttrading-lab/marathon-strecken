# Bodenhöhen alle 10 m (Linienmeter) aus dem USGS 3DEP (1-m-Laser-Geländemodell, NAVD88) über den ImageServer, je 100 Punkte
import json, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
URL = "https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer/getSamples"
def q(a):
    b = min(a + 100, len(ss)); geo = {"points": [[float(lo[i]), float(la[i])] for i in range(a, b)], "spatialReference": {"wkid": 4326}}
    body = urllib.parse.urlencode({"geometry": json.dumps(geo), "geometryType": "esriGeometryMultipoint", "returnFirstValueOnly": "true", "interpolation": "RSP_BilinearInterpolation", "f": "json"}).encode()
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(URL, data=body, headers={"User-Agent": "marathon-profile-check/1.0"}), timeout=90))
            v = [None] * (b - a)
            for smp in r["samples"]: v[smp["locationId"]] = float(smp["value"]) if smp.get("value") not in (None, "NoData") else None
            return a, v
        except Exception: time.sleep(2 + 3 * att)
    return a, [None] * (b - a)
t0 = time.time(); H = [None] * len(ss)
with cf.ThreadPoolExecutor(4) as ex:
    for a, v in ex.map(q, range(0, len(ss), 100)): H[a:a + len(v)] = v
res = [[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", sum(r[3] is None for r in res))
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open("dgm2026_10m.json", "w"))
