# Bodenhöhen alle 10 m (Linienmeter) aus dem NSW 5m Elevation ImageServer (NSW Spatial Services, getSamples, je 100 Punkte als
# Multipoint; Geländemodell aus 1-m/2-m-Laser und 5-m-Photogrammetrie, Höhen über AHD) -> dgm2026_10m.json
import json, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
URL = "https://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_5M_Elevation/ImageServer/getSamples"
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
def q(a):
    b = min(a + 100, len(ss))
    geo = json.dumps({"points": [[float(x), float(y)] for x, y in zip(lo[a:b], la[a:b])], "spatialReference": {"wkid": 4326}})
    data = urllib.parse.urlencode({"geometry": geo, "geometryType": "esriGeometryMultipoint", "returnFirstValueOnly": "true",
                                   "interpolation": "RSP_BilinearInterpolation", "f": "json"}).encode()
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(URL, data=data), timeout=90))
            out = [None] * (b - a)
            for smp in r["samples"]:
                v = smp.get("value"); out[smp["locationId"]] = None if v in (None, "NoData", "") else float(v)
            return a, out
        except Exception: time.sleep(2 + 3 * att)
    return a, [None] * (b - a)
t0 = time.time(); H = [None] * len(ss)
with cf.ThreadPoolExecutor(4) as ex:
    for a, v in ex.map(q, range(0, len(ss), 100)): H[a:a + len(v)] = v
res = [[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", sum(r[3] is None for r in res))
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open("dgm2026_10m.json", "w"))
