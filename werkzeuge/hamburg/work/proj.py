import json, math
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
K = json.load(open("kml.json"))
lat0 = math.radians(53.57)
def xy(lat, lon): return (math.radians(lon)*math.cos(lat0)*6371008.8, math.radians(lat)*6371008.8)
P = [xy(p[0], p[1]) for p in pts]
def project(q, start_m=0.0, maxdist=80):
    """first local-minimum projection after start_m with distance < maxdist"""
    Q = xy(q[1], q[0]); best = None
    for i in range(1, len(P)):
        if d[i] < start_m: continue
        ax, ay = P[i-1]; bx, by = P[i]; dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy or 1e-9
        t = max(0, min(1, ((Q[0]-ax)*dx+(Q[1]-ay)*dy)/L2))
        px, py = ax+t*dx, ay+t*dy; dist = math.hypot(Q[0]-px, Q[1]-py)
        s = d[i-1] + t*(d[i]-d[i-1])
        if dist < maxdist and (best is None or dist < best[1]): best = (s, dist)
        elif best is not None and s > best[0] + 400: break
    return best
km = {}
pos = 0.0
for nm, gtyp, cs in K["HMH26_Marathon_KM_Punkte"]:
    r = project(cs[0], pos)
    km[nm] = r
    if r: pos = r[0] - 50
for nm, r in km.items():
    print(f"{nm:6s} GPX {r[0]/1000:7.3f} km  Abstand {r[1]:5.1f} m" if r else f"{nm} --")
json.dump({k: v for k, v in km.items()}, open("kmproj.json", "w"))
