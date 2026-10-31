# Zuordnung Linienmeter der Linie der Google-Karte (linie.json) -> offizielle Meter, über die Ideallinie (ideal.py, schnur_szg.py).
# Aufbau der Strecke (Streckenplan 2026, Seite „Powerade Staffel Marathon“): Start auf der Staatsbrücke (A), Runde 1 bis zum
# Herbert-von-Karajan-Platz (B), dann über den Universitätsplatz (Halbmarathon-Zwischenzeit, Staffelwechsel 2), Residenzplatz und
# Mozartplatz in Runde 2, die am Rudolfskai wieder auf Runde 1 trifft und am Herbert-von-Karajan-Platz (B) vorbei über die
# Hofstallgasse ins Ziel am Max-Reinhardt-Platz (F) führt. Der Halbmarathon läuft A–B–F (eine Runde, ins selbe Ziel), also misst
# die Schleife B–B genau einen Halbmarathon, A–B plus B–F ebenfalls. Beide Teile werden deshalb je für sich auf 21 097,5 m gestreckt.
# B: letzter Punkt vor dem Ziel, an dem die Linie der zweiten Runde höchstens 2,5 m neben der ersten liegt (die Linie der Karte
# ist dort für beide Runden dieselbe Aufzeichnung).
# -> strecke.json {"lm": Linienmeter (Tabelle), "off": offizielle Meter, "A", "B1", "B2", "F", "w", "c1", "c2"}
import json, sys
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
W = float(sys.argv[1]) if len(sys.argv) > 1 else json.load(open("ideal_wahl.json"))["w"]
HM = 21097.5
T = Transformer.from_crs(4326, 31258, always_xy=True)
g = json.load(open("linie.json")); d = np.array(g["d"]); P = np.array(g["pts"])
M = json.load(open("marken.json"))["punkte"]
A = next(p[1] for p in M if p[3].startswith("Start")); F = next(p[1] for p in M if p[3].startswith("FINISH"))
ss = np.arange(0, d[-1], 2.0); x, y = T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0])); X = np.c_[x, y]
r1 = ss < 21800; baum = cKDTree(X[r1])
B2 = B1 = None
for i in np.where((ss > F - 800) & (ss < F))[0]:
    dd, j = baum.query(X[i])
    if dd <= 2.5: B2, B1 = float(ss[i]), float(ss[r1][j])
I = json.load(open(f"ideal_{W:g}.json")); f_lm = np.array(I["lm"]); f_id = np.array(I["ideal"])
def o(s): return np.interp(s, f_lm, f_id)
c1 = HM / ((o(B1) - o(A)) + (o(F) - o(B2))); c2 = HM / (o(B2) - o(B1))
lm = np.append(np.arange(0, d[-1], 2.0), d[-1])
off = np.where(lm <= B1, (o(lm) - o(A)) * c1,
      np.where(lm <= B2, (o(B1) - o(A)) * c1 + (o(lm) - o(B1)) * c2, (o(B1) - o(A)) * c1 + HM + (o(lm) - o(B2)) * c1))
off = np.clip(off, 0, 2 * HM); assert np.all(np.diff(off) >= 0)
print(f"w = {W} m: Ideallinie A–B {o(B1) - o(A):.1f} m + B–F {o(F) - o(B2):.1f} m = {(o(B1) - o(A)) + (o(F) - o(B2)):.1f} m (Faktor {c1:.5f}); "
      f"Schleife B–B {o(B2) - o(B1):.1f} m (Faktor {c2:.5f}); Linie A {A:.0f}, B {B1:.0f} / {B2:.0f}, F {F:.0f}")
json.dump({"lm": lm.round(2).tolist(), "off": off.round(2).tolist(), "A": A, "B1": B1, "B2": B2, "F": F, "w": W, "c1": c1, "c2": c2},
          open("strecke.json", "w"))
