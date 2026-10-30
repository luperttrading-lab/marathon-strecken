# Bodenhöhen alle 10 Linienmeter aus dem Höhendienst der Géoplateforme der IGN (data.geopf.fr/altimetrie, ohne Anmeldung,
# Licence Ouverte Etalab 2.0), nur per GET, je 100 Punkte (wie Paris):
#   ign_rge_alti_wld            RGE ALTI 1 m (Höhen über NGF-IGN69)          -> dgm2026_10m.json [[Linienmeter, lat, lon, h], …]
#   ign_lidar_hd_mnt_multi_wld  LiDAR HD, Geländemodell 50 cm (ohne Interpolation) -> Gegenprobe in dgm_vergleich.json
import json, sys, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
dd = np.array(d); la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, dd, la_); lo = np.interp(ss, dd, lo_)
URL = "https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json"
def hole(res):
    def q(a):
        b = min(a + 100, len(ss))
        qs = urllib.parse.urlencode({"lon": "|".join(f"{v:.7f}" for v in lo[a:b]), "lat": "|".join(f"{v:.7f}" for v in la[a:b]), "resource": res, "zonly": "true"}, safe="|")
        for att in range(6):
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(URL + "?" + qs, headers={"User-Agent": "marathon-profile-check/1.0"}), timeout=90))
                return a, [None if v is None or v < -100 else float(v) for v in r["elevations"]]
            except Exception: time.sleep(2 + 3 * att)
        return a, [None] * (b - a)
    H = [None] * len(ss)
    with cf.ThreadPoolExecutor(3) as ex:
        for a, v in ex.map(q, range(0, len(ss), 100)): H[a:a + len(v)] = v
    print(res, len(H), "Punkte, fehlend", sum(h is None for h in H), "min/max", min(h for h in H if h is not None), max(h for h in H if h is not None))
    return H
rge = hole("ign_rge_alti_wld"); lid = hole("ign_lidar_hd_mnt_multi_wld")
json.dump([[float(s), float(x), float(y), h] for s, x, y, h in zip(ss, la, lo, rge)], open("dgm2026_10m.json", "w"))
json.dump({"s": ss.tolist(), "lat": la.tolist(), "lon": lo.tolist(), "rge": rge, "lidar": lid}, open("dgm_vergleich.json", "w"))
