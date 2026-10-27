# Offizielle Kilometerpunkte (Karte maps.scc-events.com) auf die Ideallinie projizieren -> kmproj.json
import json, math
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
LOC = json.load(open("../dl/locations.json"))
lat0 = math.radians(52.5)
def xy(lat, lon): return (math.radians(lon)*math.cos(lat0)*6371008.8, math.radians(lat)*6371008.8)
P = [xy(p[0], p[1]) for p in pts]
def project(q, start_m=0.0, maxdist=80, window=2500):
    """beste Projektion zwischen start_m und start_m + window mit Abstand < maxdist; q = (lat, lon).
    Das Fenster verhindert Treffer auf späteren Durchläufen derselben Straße."""
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
    kms = sorted([l for l in LOC if l["cat"] == "km" and l["name"].startswith("KM")], key=lambda l: int(l["name"].split()[1]))
    km, pos = {}, 0.0
    for l in kms:
        r = project((l["lat"], l["lon"]), pos); km[l["name"]] = r
        if r: pos = r[0] - 50
    km["Start"] = (0.0, 0.0)                                    # die Ideallinie beginnt an der Startlinie; eine eigene Startmarke gibt es nicht
    l = [x for x in LOC if x["name"] == "Ziel"][0]; km["Ziel"] = project((l["lat"], l["lon"]), d[-1] - 3000, 150, 4000)
    prev = None
    for nm, r in km.items():
        if not r: print(nm, "--"); continue
        step = "" if prev is None or not nm.startswith("KM") else f"  Abschnitt {r[0]-prev:6.0f} m"
        print(f"{nm:6s} GPX {r[0]/1000:7.3f} km  Abstand {r[1]:5.1f} m{step}")
        if nm.startswith("KM"): prev = r[0]
    json.dump(km, open("kmproj.json", "w"))
