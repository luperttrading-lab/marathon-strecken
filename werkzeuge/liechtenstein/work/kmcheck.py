# Nur Abgleich: Linienmeter der Orte, die der Veranstalter mit Kilometern nennt (Postenliste, Marschtabelle, Programm, Reglement) bzw. der
# Laufbericht 2023 von marathon4you.de, gegen die Linie aus OSM (gpx2026.json) und die gleichmäßig auf 42,195 km gedehnten Kilometer
# (common.py). Lage der Orte aus OSM (Haltestellen, Gebäude, Sättel) bzw. swissNAMES3D (geo.admin.ch). Abstand = Ort neben der Linie.
import json
import numpy as np
from pyproj import Transformer
from common import official
T = Transformer.from_crs(4326, 2056, always_xy=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array(g["pts"])
x, y = T.transform(P[:, 1], P[:, 0]); X = np.c_[x, y]
dd = np.arange(0, d[-1], 5.0); Xd = np.c_[np.interp(dd, d, X[:, 0]), np.interp(dd, d, X[:, 1])]
ORTE = [("Rheinparkstadion (Laufbericht: Kilometerschild 8)", 2757160, 1223000, 8.0),
        ("Haltestelle Vaduz Lochgass (Marschtabelle alt: km 8, Start damals Ospelt)", 2757141, 1223847, None),
        ("Marktplatzgarage, Posten 2", 2757984, 1222892, 10.0), ("Park-Hotel Sonnenhof (Laufbericht km 11)", 2758105, 1223895, 11.0),
        ("Schloss Vaduz (Laufbericht km 12)", 2758204, 1223031, 12.0), ("Rotenboden, Posten 4", 2759327, 1221753, 15.0),
        ("Masescha Kapelle, Posten 5", 2759633, 1222318, 17.5), ("Silum, Posten 6", 2760517, 1222201, 20.0),
        ("Kulm (Sattel 1450 m)", 2761147, 1220852, None), ("Sücka (Marschtabelle km 24)", 2761360, 1220620, 24.0),
        ("Gänglesee (Laufbericht: Verpflegung km 25)", 2762396, 1219449, 25.0), ("Grund (Posten 8 Steg, Parkplatz Grund)", 2762471, 1219460, 25.0),
        ("Steg, Ort", 2761805, 1220827, None), ("Vordervalorsch (Marschtabelle km 28)", 2762530, 1222386, 28.0),
        ("Rietle Schaan (Posten 9 Valorsch/Rietle Stall)", 2763799, 1223408, 31.0), ("Güschglehötta (Posten 10)", 2764756, 1222233, 33.0),
        ("Sassförkle (Laufbericht: kurz vor km 34; Posten 11 Saas Fürkle km 35)", 2764745, 1220995, 34.0),
        ("Schlucher-Treff (Ziel)", 2764652, 1219208, None), ("Kehrplatz unter dem Turna-Stall, Posten 13", 2765417, 1217909, 38.5)]
print(f"Linie {d[-1]:.0f} m, Faktor auf 42 195 m: {42195 / d[-1]:.4f}")
for nm, e, n, km in ORTE:
    a = np.hypot(Xd[:, 0] - e, Xd[:, 1] - n)
    # alle Durchgänge (lokale Minima unter 150 m)
    idx = [i for i in range(len(a)) if a[i] < 150 and a[i] == a[max(0, i - 60):i + 61].min()]
    txt = "; ".join(f"Linie {dd[i] / 1000:6.2f} km = {float(official(dd[i])) / 1000:5.2f} km ({a[i]:.0f} m daneben)" for i in idx) or f"nicht in 150 m (nächster {a.min():.0f} m)"
    print(f"  {nm:70s} Veranstalter {km if km else '–':>5}  {txt}")
