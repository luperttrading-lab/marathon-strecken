# Strecke aus der OpenRunner-Karte des Veranstalters: Die Seite „Plans“ (marathondumedoc.com/plans/, „Parcours 2026“) bettet die
# OpenRunner-Strecke 23032885 ein (embed code 51556f65…); deren Daten liefert die öffentliche API des Einbettens
# (api.openrunner.com/api/v2/embedded-routes/<code>, ../dl/embedded.json): Linie als Polyline (580 Punkte, OpenRunner-Länge
# 42 245 m), Höhen alle 100 m (Quelle unbekannt) und 46 Punkte (Verpflegung, „Dégustation“, Austern, Entrecôte, Käse, Eis,
# Sanität) mit Linienmeter („sticked_distance_in_meter“). -> openrunner.json
import json
from pyproj import Geod
d = json.load(open("../dl/embedded.json"))["data"]
def dec(t, n=2):
    out, i, acc = [], 0, [0] * n
    while i < len(t):
        for k in range(n):
            s = a = c = 0
            while True:
                s = ord(t[i]) - 63; i += 1; c |= (s & 31) << a; a += 5
                if s < 32: break
            acc[k] += ~(c >> 1) if c & 1 else c >> 1
        out.append([v * 1e-5 for v in acc])
    return out
pts = dec(d["shape"]["full_encoded"])
el = [round(v[0] * 1e5) for v in dec(d["elevation"]["full_encoded"], 1)]   # ganze Meter (Polyline ohne Faktor 1e5)
G = Geod(ellps="GRS80")
dd = [0.0]
for a, b in zip(pts[:-1], pts[1:]): dd.append(dd[-1] + G.inv(a[1], a[0], b[1], b[0])[2])
pois = [{"m": p["sticked_distance_in_meter"], "lat": float(p["latitude"]), "lon": float(p["longitude"]), "titel": p["title"],
         "text": (p.get("content") or "").strip()} for p in d["pois"]]
json.dump({"pts": pts, "d": dd, "hoehe100": el, "laenge_or": d["length"], "pois": pois}, open("openrunner.json", "w"), ensure_ascii=False)
print(len(pts), "Punkte, geodätisch", round(dd[-1], 1), "m, OpenRunner", d["length"], "m; Start", pts[0], "Ende", pts[-1])
print("Höhen alle 100 m:", len(el), "Werte, roh", el[:5], "…")
