# Bodenhöhen alle 10 m (Linienmeter) aus dem Höhenmodell des INEGI (Continuo de Elevaciones Mexicano), Tipo Terreno, bilinear,
# Blätter E14A39E1, B1, B2, B3, B4 (inegi.py, inegi_dgm.py). Verwendet: AUSGABE (siehe UEBERGABE.md, „Höhe“); die beiden anderen
# Ausgaben werden zum Vergleich mit abgelesen -> dgm2026_10m.json [Linienmeter, Breite, Länge, Höhe], dgm_vergleich.json
import json, sys, numpy as np
from inegi_dgm import lade, hoehe
AUSGABE = sys.argv[1] if len(sys.argv) > 1 else "5m2011"
g = json.load(open("gpx2026.json")); pts, d = g["pts"], np.array(g["d"])
la_ = np.array([p[0] for p in pts]); lo_ = np.array([p[1] for p in pts])
ss = np.append(np.arange(0, d[-1], 10.0), d[-1]); la = np.interp(ss, d, la_); lo = np.interp(ss, d, lo_)
alle = {}
for a in ("5m2011", "5m201x", "15m2020"):
    R = lade(a); h, q = zip(*[hoehe(R, x, y) for x, y in zip(la, lo)])
    alle[a] = [None if v is None else round(v, 3) for v in h]
    fehlt = sum(v is None for v in h); from collections import Counter
    print(a, "fehlend", fehlt, dict(Counter(q)))
json.dump({"s": ss.tolist(), **alle}, open("dgm_vergleich.json", "w"))
h = alle[AUSGABE]; assert all(v is not None for v in h), "Lücken im Modell"
json.dump([[float(s), float(a), float(b), v] for s, a, b, v in zip(ss, la, lo, h)], open("dgm2026_10m.json", "w"))
print("verwendet", AUSGABE, "Höhe min/max", min(h), max(h))
# Der Start liegt am Südende der Brücke der Insurgentes am Estadio Olímpico; für die Fahrbahnhöhe dort braucht clean.py die Rampe
# davor: 25 m südlich des Starts, auf der Verlängerung der Linie -> dgm_vorstart.json [Linienmeter (negativ), Höhe]
R = lade(AUSGABE); v = np.array([la_[1] - la_[0], lo_[1] - lo_[0]]); v /= np.hypot(v[0], v[1] * np.cos(np.radians(la_[0]))) * 111320 / 25
json.dump([-25.0, hoehe(R, la_[0] - v[0], lo_[0] - v[1])[0]], open("dgm_vorstart.json", "w"))
print("Rampe 25 m vor dem Start:", json.load(open("dgm_vorstart.json")))
