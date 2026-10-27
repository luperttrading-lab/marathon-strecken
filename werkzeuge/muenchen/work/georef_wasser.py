# Endgültige Lage der Strecke: Ähnlichkeit aus 12 Passpunkten an Gewässern (wasser_versatz.py -> ../dl/fit_wasser.json),
# Restfehler 2–9 m. Die Anpassung nur an Straßen (georef.py) blieb in einem Nebenminimum hängen (0,7 % Maßstab, 0,5° Drehung,
# am Olympiasee 70 m daneben). -> ../dl/strecke_georef.json
import json, math, numpy as np
from scipy.spatial import cKDTree
R = 6378137.0
F = json.load(open("../dl/fit_wasser.json")); s, Rm, t = F["s"], np.array(F["R"]), np.array(F["t"])
P = np.array(json.load(open("../dl/pdf_linie.json")), float); P[:, 1] = -P[:, 1]
X = s * P @ Rm.T + t; lat = np.degrees(2 * np.arctan(np.exp(X[:, 1] / R)) - np.pi / 2); lon = np.degrees(X[:, 0] / R)
c = math.cos(math.radians(48.15)); L = (6371008.8 * np.hypot(np.radians(np.diff(lat)), np.radians(np.diff(lon)) * c)).sum()
road = []
for w in json.load(open("../dl/osm_wege.json"))["elements"]:
    g = w.get("geometry")
    if g and len(g) > 1:
        m = np.c_[[R * math.radians(q["lon"]) for q in g], [R * math.log(math.tan(math.pi / 4 + math.radians(q["lat"]) / 2)) for q in g]]
        for a, b in zip(m[:-1], m[1:]): n = max(1, int(np.hypot(*(b - a)) / 4)); road.append(a + (b - a) * np.linspace(0, 1, n + 1)[:-1, None])
d, _ = cKDTree(np.vstack(road)).query(X); k = 1 / c
print(f"Länge {L / 1000:.3f} km, Abstand zur Straße Median {np.median(d) / k:.1f} m, 90 % {np.percentile(d, 90) / k:.1f} m")
json.dump({"lat": lat.tolist(), "lon": lon.tolist(), "s": s, "R": Rm.tolist(), "t": t.tolist(), "k": k}, open("../dl/strecke_georef.json", "w"))
