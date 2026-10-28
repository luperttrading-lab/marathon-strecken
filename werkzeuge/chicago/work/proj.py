# Offizielle Meilen- und 5-km-Marken auf die Linie projizieren -> kmproj.json (Name -> [Linienmeter, Abstand, offizielle Meter])
import json, math
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
LOC = json.load(open("../dl/locations.json"))
lat0 = math.radians(41.88)
def xy(lat, lon): return (math.radians(lon)*math.cos(lat0)*6371008.8, math.radians(lat)*6371008.8)
P = [xy(p[0], p[1]) for p in pts]
def project(q, start_m=0.0, maxdist=80, window=2500):
    """beste Projektion zwischen start_m und start_m + window mit Abstand < maxdist; q = (lat, lon)"""
    Q = xy(q[0], q[1]); best = None
    for i in range(1, len(P)):
        if d[i] < start_m: continue
        if d[i-1] > start_m + window: break
        ax, ay = P[i-1]; bx, by = P[i]; dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy or 1e-9
        t = max(0, min(1, ((Q[0]-ax)*dx+(Q[1]-ay)*dy)/L2))
        px, py = ax+t*dx, ay+t*dy; dist = math.hypot(Q[0]-px, Q[1]-py)
        s = d[i-1] + t*(d[i]-d[i-1])
        if dist < maxdist and (best is None or dist < best[1]): best = (s, dist)
    return best
if __name__ == "__main__":
    km, pos, prev = {}, 0.0, None
    for l in sorted([l for l in LOC if l["cat"] == "km"], key=lambda l: l["m"]):
        r = project((l["lat"], l["lon"]), max(0, pos - 50), 150, 3500)
        if not r: print(l["name"], "--"); continue
        km[l["name"]] = [r[0], r[1], l["m"]]; pos = r[0]
        flag = "" if prev is None else f"  Faktor {(r[0]-prev[0])/(l['m']-prev[1]):.3f}"
        print(f"{l['name']:26s} offiziell {l['m']/1000:7.3f} km  Linie {r[0]/1000:7.3f} km  Abstand {r[1]:5.1f} m{flag}")
        prev = (r[0], l["m"])
    json.dump(km, open("kmproj.json", "w"))
