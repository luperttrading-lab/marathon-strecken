# Verpflegung und Staffelwechsel: Punkte der My-Maps-Karte des Veranstalters (Ebenen „EP's & VP's“ und „Wechselzonen“,
# kml_punkte.json) auf die Linie projiziert, in offizielle Meter umgerechnet. Die Strecke läuft zweimal über die Fritz-Behrens-Allee
# (km 13,3–14,3 und 24,7–25,7); deshalb wird jeder Punkt nur in einem Fenster ±2,5 km um seine Sollstelle gesucht (VP und EP n bei (n + 1) · 2,5 km,
# „nach jeweils 5 km Verpflegungspunkte, dazwischen Erfrischungspunkte“, Seite „Streckenservice“; Wechselzonen bei der km-Angabe
# des Veranstalters). Gegenprobe: dieselben Stellen im Digitalen Zwilling der Stadt (Verpflegungspunkt.geojson,
# Erfrischungspunkt_2026.geojson, Wechselzonen_2026.geojson). Refill-Station laut Streckenplan 2026 (grüner Ring) an VP 3, 7 und 11.
# -> stationen.json [[Name, offizielle Meter, Abstand zur Linie, Zwilling-Meter]]
import json, re
import numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array(g["pts"])
X = np.array(T.transform(P[:, 1], P[:, 0])).T
dl = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; fak = d[-1] / dl[-1]
def proj(lat, lon, soll_km, fenster=2500):
    soll = soll_km * 1000 * d[-1] / 42195; q = np.array(T.transform(lon, lat)); best = None
    for i in range(len(X) - 1):
        if abs(d[i] - soll) > fenster and abs(d[i + 1] - soll) > fenster: continue
        a, b = X[i], X[i + 1]; v = b - a; L = np.hypot(*v)
        t = 0 if L < 1e-9 else min(1, max(0, np.dot(q - a, v) / L ** 2))
        ab = float(np.hypot(*(q - a - t * v)))
        if best is None or ab < best[0]: best = (ab, float(official((dl[i] + t * L) * fak)))
    return best
def soll(name):
    m = re.match(r"(VP|EP) (\d+)", name)
    if m: return (int(m.group(2)) + 1) * 2.5
    return float(re.search(r"KM ([\d,]+)", name).group(1).replace(",", "."))
k = json.load(open("kml_punkte.json"))["punkte"]
zw = {}
for f in ("Verpflegungspunkt.geojson", "Erfrischungspunkt_2026.geojson"):
    for x in json.load(open("../dl/zwilling/" + f))["features"]:
        i = x["properties"]["id"]; lo, la = x["geometry"]["coordinates"][:2]; zw[("VP " if i % 2 else "EP ") + str(i)] = (la, lo)
for x in json.load(open("../dl/zwilling/Wechselzonen_2026.geojson"))["features"]:
    lo, la = x["geometry"]["coordinates"][:2]; zw["WZ " + x["properties"]["Wechselzone"].split()[0]] = (la, lo)
out = []
for fn in ("EP's & VP's", "Wechselzonen"):
    for n, la, lo in k[fn]:
        so = soll(n); ab, m = proj(la, lo, so)
        kurz = n if fn != "Wechselzonen" else "WZ " + n.split()[1]
        z = zw.get(kurz); zm = proj(z[0], z[1], so)[1] if z else None
        out.append([n, round(m), round(ab, 1), round(zm) if zm else None])
out.sort(key=lambda x: x[1])
for n, m, ab, zm in out: print(f"{n:40s} km {m/1000:6.2f}  ({ab:4.1f} m neben der Linie)   Zwilling km {zm/1000:6.2f}  Diff {m - zm:+5d} m")
json.dump(out, open("stationen.json", "w"), ensure_ascii=False)
