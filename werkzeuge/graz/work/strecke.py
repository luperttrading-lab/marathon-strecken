# Marathonlinie aus zwei Runden der Garmin-Strecke (runde.json) und Zuordnung Linienmeter -> offizielle Meter. Kopie von
# werkzeuge/freiburg/work/strecke.py.
# - Start und Ziel vor der Oper am Opernring (Lageplan „Start-/Zielbereich“ des Veranstalters: eine Linie „Start/Ziel“, gestartet wird
#   nach Südwesten, der Zieleinlauf kommt in einer abgetrennten Spur von Südwesten zurück). Die Garmin-Linie beginnt am Opernring auf der
#   Höhe der Burggasse und endet 34 m davor (südwestlich) in der Zielspur.
# - Runde 1: die ganze Linie bis zu ihrem Ende, dann gerade 34 m zurück zum Anfang. Wie die Marathonläufer am Ende der ersten Runde
#   wenden, zeigt kein Plan (etwa 30 m, eben).
# - Runde 2: die ganze Linie bis zum Ziel (Ende der Linie).
# Kilometer: Die Linie folgt den Straßenmitten von OSM und ist nach dem Bereinigen (parse.py) 21 244 m lang, 0,7 % mehr als der
# Halbmarathon (21 097,5 m, eine Runde, AIMS-vermessen). Vermessen wird die kürzeste Linie; ideal.py spannt eine Schnur in einem Band
# von ±w m um die Linie (ideal_w.py, Wenden fest). Jeder Linienmeter bekommt die Länge der Ideallinie bis dorthin, gestreckt auf die
# offizielle Rundenlänge. Aufruf: python3 strecke.py [w] (sonst ideal_wahl.json).
# -> strecke2026.json {"pts": [[lat, lon]…], "d": Linienmeter (geodätisch), "lm": Tabelle Linienmeter, "off": offizielle Meter,
#     "runde2": Linienmeter, an dem Runde 2 beginnt, "abzweig": Index des Endes von Runde 1}
import json, sys
import numpy as np
from pyproj import Geod
W = sys.argv[1] if len(sys.argv) > 1 else json.load(open("ideal_wahl.json"))["w"]
G = Geod(ellps="WGS84")
r = json.load(open("runde.json")); P = [tuple(p[:2]) for p in r["pts"]]; d = np.array(r["d"]); L = d[-1]
def dist(a, b): return G.inv(a[1], a[0], b[1], b[0])[2]
iab = len(P) - 1
verb = dist(P[iab], P[0])
print(f"Ende der Linie {L:.0f} m, {verb:.0f} m vor dem Anfang")
I = json.load(open(f"ideal_{float(W):g}.json")); f_lm = np.array(I["lm"]); f_id = np.array(I["ideal"])
def f(x): return np.interp(x, f_lm, f_id)
HM = 21097.5
pts = P + P
dd = [0.0]
for a, b in zip(pts[:-1], pts[1:]): dd.append(dd[-1] + dist(a, b))
dd = np.array(dd); r2 = dd[iab + 1]
c1 = HM / (f(L) + verb); c2 = HM / f(L)
lm = np.r_[np.arange(0, L, 2.0), L, r2, r2 + np.arange(2.0, L, 2.0), r2 + L]
off = np.where(lm <= L, f(np.minimum(lm, L)) * c1,
      np.where(lm <= r2, f(L) * c1 + (lm - L) * c1, HM + f(np.clip(lm - r2, 0, L)) * c2))
off[-1] = 2 * HM
assert np.all(np.diff(off) >= 0)
print(f"Marathonlinie {dd[-1]:.1f} m; Runde 2 ab Linienmeter {r2:.1f}; Ideallinie je Runde {f(L):.1f} m; Faktoren {c1:.5f} / {c2:.5f}; w = {W} m")
for k in range(0, 43):
    x = np.interp(k * 1000, off, lm)
    if k % 5 == 0 or k in (21, 22): print(f"  km {k:2d}: Linienmeter {x:7.0f} (gleichmäßig wäre {k * 1000 * dd[-1] / 42195:7.0f})")
json.dump({"pts": [list(p) for p in pts], "d": dd.tolist(), "lm": lm.round(2).tolist(), "off": off.round(2).tolist(), "runde2": float(r2),
           "abzweig": iab, "w": float(W)}, open("strecke2026.json", "w"))
