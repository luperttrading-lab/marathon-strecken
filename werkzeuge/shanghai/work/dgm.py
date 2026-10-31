# Höhen entlang der Linie alle 10 Linienmeter aus FABDEM, Copernicus GLO-30 und SRTM 1″ (hoehen.py) -> dgm_vergleich.json {"s":
# [Linienmeter], "lat", "lon", "fabdem", "cop30", "srtm"}; FABDEM (gewählt, siehe vergleich.py und UEBERGABE.md) zusätzlich als
# dgm2025_10m.json [[Linienmeter, lat, lon, h], …] wie bei den anderen Strecken. Ein Laser- oder amtliches Geländemodell für Shanghai
# ist nicht frei zugänglich (siehe UEBERGABE.md).
import json
import numpy as np
from hoehen import modell
from geo import utm, wgs
g = json.load(open("linie2025.json")); P = np.array(g["pts"]); d = np.array(g["d"])
s = np.append(np.arange(0, d[-1], 10.0), d[-1])
x, y = utm(P[:, 0], P[:, 1])
lat, lon = wgs(np.interp(s, d, x), np.interp(s, d, y))
out = {"s": s.round(1).tolist(), "lat": lat.round(7).tolist(), "lon": lon.round(7).tolist()}
for m in ("fabdem", "cop30", "srtm"):
    h = modell(m)(lat, lon); out[m] = np.round(h, 2).tolist()
    print(f"{m:7s} Start {h[0]:6.1f}  min {np.nanmin(h):6.1f}  max {np.nanmax(h):6.1f} bei Linienmeter {s[np.nanargmax(h)]:7.0f}  Ziel {h[-1]:6.1f}  fehlend {np.isnan(h).sum()}")
json.dump(out, open("dgm_vergleich.json", "w"))
json.dump([[float(a), float(b), float(c), float(e)] for a, b, c, e in zip(out["s"], out["lat"], out["lon"], out["fabdem"])],
          open("dgm2025_10m.json", "w"))
print(len(s), "Punkte")
