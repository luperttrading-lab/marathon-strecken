# Bodenhöhen alle 10 m (Linienmeter) aus dem RGE ALTI 1 m der IGN (Laser- und Bildkorrelation, Höhen über NGF-IGN69,
# Licence Ouverte Etalab) über den Höhendienst der Géoplateforme, je 100 Punkte -> dgm2026_10m.json
import json, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
URL = "https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json"
def q(a):
    b = min(a + 100, len(ss))
    qs = urllib.parse.urlencode({"lon": "|".join(f"{v:.7f}" for v in lo[a:b]), "lat": "|".join(f"{v:.7f}" for v in la[a:b]), "resource": "ign_rge_alti_wld", "zonly": "true"}, safe="|")
    for att in range(6):   # nur GET: POST beantwortet der Dienst mit „unexpected error“
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(URL + "?" + qs, headers={"User-Agent": "marathon-profile-check/1.0"}), timeout=90))
            return a, [None if v is None or v < -100 else float(v) for v in r["elevations"]]
        except Exception: time.sleep(2 + 3 * att)
    return a, [None] * (b - a)
t0 = time.time(); H = [None] * len(ss)
with cf.ThreadPoolExecutor(3) as ex:
    for a, v in ex.map(q, range(0, len(ss), 100)): H[a:a + len(v)] = v
res = [[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, H)]
print(len(res), "Punkte in", round(time.time() - t0), "s; fehlend:", sum(r[3] is None for r in res))
hv = [r[3] for r in res if r[3] is not None]; print("Höhe min/max", round(min(hv), 1), round(max(hv), 1))
json.dump(res, open("dgm2026_10m.json", "w"))
