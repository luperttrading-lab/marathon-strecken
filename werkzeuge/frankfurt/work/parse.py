# Offizielle GPX 2026 (Route aus OpenLayers, ohne Höhen) -> gpx2026.json mit Punkten und laufender Länge
import re, math, json
txt = open("../dl/strecke.gpx").read()
pts = [(float(a), float(b), 0.0) for a, b in re.findall(r'<rtept lat="([\d.]+)" lon="([\d.]+)"', txt)]
def hav(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    a = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(a))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i-1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1]/1000, 3), "Start", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
