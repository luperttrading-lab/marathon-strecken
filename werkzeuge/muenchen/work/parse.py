# Offizielle Strecke 2026 (GPX des Veranstalters, marathonmuenchen.org/gpx-downloads, „Marathon-Muenchen.gpx“)
# -> gpx2026.json mit Punkten und laufender Länge, ../dl/locations.json mit Start und Ziel (Kilometerpunkte gibt es nicht).
# georef.py / wasser_versatz.py / georef_wasser.py haben vorher die Linie aus dem PDF auf Koordinaten gelegt; sie liegt im
# Mittel 7 m (max. 28 m) neben dieser GPX und dient nur noch als Gegenprobe.
import re, math, json
txt = open("../dl/Marathon-Muenchen.gpx", encoding="utf-8").read()
pts = [(float(a), float(b), 0.0) for a, b in re.findall(r'<trkpt lat="([\d.-]+)" lon="([\d.-]+)"', txt)]
def hav(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    a = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(a))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i-1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1]/1000, 3), "Start", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
json.dump([{"cat": "km", "name": "Start", "lat": pts[0][0], "lon": pts[0][1]}, {"cat": "km", "name": "Ziel", "lat": pts[-1][0], "lon": pts[-1][1]}], open("../dl/locations.json", "w"))
