# Marken auf der Linie: die 46 Punkte der OpenRunner-Karte des Veranstalters (openrunner.json) auf die Linie projiziert (nächster
# Linienpunkt; liegt die Linie an zwei Stellen nah, die nächste zum OpenRunner-Linienmeter), dazu die Châteaux der Plaquette.
# Liste der Verpflegungsstände mit km aus der Plaquette Prestige 2026 (Seite 12, „Les responsables des stands de ravitaillement“,
# nur Name des Stands und km übernommen, keine Personennamen). -> marken.json
import json, numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 2154, always_xy=True)
o = json.load(open("openrunner.json")); P = np.array(o["pts"]); d = np.array(o["d"])
x, y = T.transform(P[:, 1], P[:, 0]); xy = np.c_[x, y]
fak = d[-1] / o["laenge_or"]
def projiziere(la, lo, erwartet=None):
    p = np.array(T.transform(lo, la)); kand = []
    for i in range(len(xy) - 1):
        a, b = xy[i], xy[i + 1]; v = b - a; t = np.clip(np.dot(p - a, v) / (np.dot(v, v) or 1), 0, 1); q = a + t * v
        kand.append((float(np.hypot(*(p - q))), float(d[i] + t * (d[i + 1] - d[i]))))
    dmin = min(c[0] for c in kand)
    if erwartet is None: return min(kand)[1], dmin
    nah = [c for c in kand if c[0] <= max(30, dmin + 1)]
    best = min(nah, key=lambda c: abs(c[1] - erwartet)); return best[1], best[0]
out = []
for p in o["pois"]:
    art = p["text"] or p["titel"]
    s, e = projiziere(p["lat"], p["lon"], p["m"] * fak if p["m"] >= 0 else None)
    out.append({"art": art, "or_m": p["m"], "s": round(s, 1), "km": round(float(official(s)) / 1000, 3), "daneben": round(e, 1), "lat": p["lat"], "lon": p["lon"]})
out.sort(key=lambda m: m["s"])
# Châteaux der Stände (Plaquette 2026) aus OSM, zur Probe, ob der nächste Wasser-Punkt der Karte dort liegt
from namen import CHATEAUX
STAENDE = [("Château Grand-Puy-Lacoste", 3), ("Château Larose-Trintaudon", 7), ("Château Lagrange", 10), ("Château Beychevelle", 12),
           ("Château Ducru-Beaucaillou", 13), ("Saint-Julien", 16), ("Château Pichon-Longueville Comtesse de Lalande", 18),
           ("Cave La Rose Pauillac", 21), ("Château d'Armailhac", 23), ("Château Lafite-Rothschild", 25), ("Château Lafon-Rochet", 27),
           ("Le Crock", 30), ("Château Tronquoy-Lalande", 33), ("Château Phélan-Ségur", 34), ("Château Montrose", 37), ("Gironde 1", 39)]
staende = []
for n, km in STAENDE:
    c = [(cx, cy) for cn, cx, cy in CHATEAUX if cn == n]
    lage = None
    if c:
        lo, la = Transformer.from_crs(2154, 4326, always_xy=True).transform(*c[0]); s, e = projiziere(la, lo, km * 1000 * d[-1] / 42195)
        lage = {"km": round(float(official(s)) / 1000, 3), "daneben": round(e)}
    w = min((m for m in out if m["art"] == "Bouteille d'eau"), key=lambda m: abs(m["km"] - km - 0.3))
    staende.append({"name": n, "km_plaquette": km, "osm": lage, "wasser_km": w["km"]})
    print(f"  Stand {n:48s} km {km:2d} (Plaquette)  Château in OSM: {lage}  nächster Wasser-Punkt der Karte km {w['km']:.2f}")
json.dump({"punkte": out, "staende": staende}, open("marken.json", "w"), ensure_ascii=False, indent=0)
for m in out: print(f"  km {m['km']:6.3f} ({m['daneben']:5.1f} m daneben, OpenRunner {m['or_m']:6d})  {m['art']}")
