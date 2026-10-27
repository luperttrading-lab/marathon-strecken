# Höhen alle 10 m (Meter der Ideallinie) aus dem DGM1 Berlin (1-m-Laserscan) per WMS-GetFeatureInfo, Ebene c_dgm1
import json, sys, time, urllib.request, concurrent.futures as cf
import numpy as np
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1])
la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
def q(i):
    a, b, e = la[i], lo[i], 0.00005
    url = ("https://gdi.berlin.de/services/wms/dgm1?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&LAYERS=c_dgm1&QUERY_LAYERS=c_dgm1"
           f"&CRS=EPSG:4326&STYLES=&BBOX={a-e:.7f},{b-e:.7f},{a+e:.7f},{b+e:.7f}&WIDTH=11&HEIGHT=11&I=5&J=5&INFO_FORMAT=application/json")
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=30))
            v = r["features"][0]["properties"]["Höhe_in_Meter_über_NHN"]
            return i, float(v)
        except Exception:
            time.sleep(1 + 2 * att)
    return i, None
t0 = time.time(); H = [None] * len(ss)
with cf.ThreadPoolExecutor(8) as ex:
    for i, v in ex.map(q, range(len(ss))): H[i] = v
res = [[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", sum(r[3] is None for r in res))
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open("dgm2026_10m.json", "w"))
