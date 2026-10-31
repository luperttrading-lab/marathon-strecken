# Marathonlinie aus zwei Runden der RaceDayMap (runde.json) und Zuordnung Linienmeter -> offizielle Meter.
# - Runde 1: vom Start (Anfang der Linie, Westrand des Neuen Messplatzes) bis zum Abzweig vor dem Zieleinlauf (Punkt der Linie am
#   Südrand des Messplatzes, dem Start am nächsten), dann gerade über den Messplatz zurück zum Start. Wie die Marathonläufer dort genau
#   in die zweite Runde geführt werden, zeigt kein Plan (2019: „Der Zieleinlauf befindet sich auf dem Messegelände beziehungsweise für
#   die Marathonläufer_innen geht es hier in die zweite Runde“); der Weg ist so lang wie der zum Ziel (je etwa 130 m, eben).
# - Runde 2: die ganze Linie bis zum Ziel (Ende der Linie, auf dem Messplatz).
# Kilometer: Die Linie folgt den Straßenmitten von OSM und ist je Runde 21 654 m lang, 2,6 % mehr als der Halbmarathon (21 097,5 m,
# eine Runde). Vermessen wird die kürzeste Linie, die an jeder Ecke innen bleibt; auf dieser Strecke mit vielen rechtwinkligen Ecken
# (Wiehre, Altstadt, Stühlinger) macht das viel aus. ideal.py spannt eine Schnur in einem Band von ±w m um die Linie (ideal_w.py); w ist
# so gewählt, dass die Runde 21 097,5 m misst. Jeder Linienmeter bekommt die Länge der Ideallinie bis dorthin, gestreckt auf die
# offizielle Rundenlänge. Der Überschuss sitzt so an den Ecken statt gleichmäßig verteilt.
# -> strecke2026.json {"pts": [[lat, lon]…], "d": Linienmeter (geodätisch), "lm": Tabelle Linienmeter, "off": offizielle Meter,
#     "runde2": Linienmeter, an dem Runde 2 beginnt}
import json, sys
import numpy as np
from pyproj import Geod
W = sys.argv[1] if len(sys.argv) > 1 else json.load(open("ideal_wahl.json"))["w"]
G = Geod(ellps="WGS84")
r = json.load(open("runde.json")); P = [tuple(p) for p in r["pts"]]; d = np.array(r["d"]); L = d[-1]
def dist(a, b): return G.inv(a[1], a[0], b[1], b[0])[2]
# Abzweig: Punkt in den letzten 300 m, der dem Start am nächsten liegt
kand = [i for i in range(len(P)) if d[i] > L - 300]
iab = min(kand, key=lambda i: dist(P[i], P[0]))
verb = dist(P[iab], P[0]); rest = L - d[iab]
print(f"Abzweig Punkt {iab} bei Linienmeter {d[iab]:.0f}: {verb:.0f} m zum Start, {rest:.0f} m zum Ziel")
# Zuordnung Linienmeter der Runde -> Meter auf der Ideallinie
I = json.load(open(f"ideal_{float(W):g}.json")); f_lm = np.array(I["lm"]); f_id = np.array(I["ideal"])
def f(x): return np.interp(x, f_lm, f_id)
HM = 21097.5
pts = P[:iab + 1] + [P[0]] + P[1:]
dd = [0.0]
for a, b in zip(pts[:-1], pts[1:]): dd.append(dd[-1] + dist(a, b))
dd = np.array(dd); r2 = dd[iab + 1]
# Runde 1 samt Rückweg auf 21 097,5 m, Runde 2 auf 21 097,5 m
c1 = HM / (f(d[iab]) + verb); c2 = HM / f(L)
lm = np.r_[np.arange(0, d[iab], 2.0), d[iab], r2, r2 + np.arange(2.0, L, 2.0), r2 + L]
off = np.where(lm <= d[iab], f(np.minimum(lm, d[iab])) * c1,
      np.where(lm <= r2, f(d[iab]) * c1 + (lm - d[iab]) * c1, HM + f(np.clip(lm - r2, 0, L)) * c2))
off[-1] = 2 * HM
assert np.all(np.diff(off) >= 0)
print(f"Marathonlinie {dd[-1]:.1f} m; Runde 2 ab Linienmeter {r2:.1f}; Faktoren {c1:.5f} / {c2:.5f}; w = {W} m")
for k in range(0, 43):
    x = np.interp(k * 1000, off, lm)
    if k % 5 == 0 or k in (21, 22): print(f"  km {k:2d}: Linienmeter {x:7.0f} (gleichmäßig wäre {k * 1000 * dd[-1] / 42195:7.0f})")
json.dump({"pts": [list(p) for p in pts], "d": dd.tolist(), "lm": lm.round(2).tolist(), "off": off.round(2).tolist(), "runde2": float(r2),
           "abzweig": iab, "w": float(W)}, open("strecke2026.json", "w"))
