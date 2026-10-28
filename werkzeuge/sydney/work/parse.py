# Offizielle Linie des Veranstalters (TCS Sydney Marathon, ../dl/sydney2026_offiziell.gpx = goandrace.com, 650 Punkte, 42,08 km)
# direkt übernommen: Die Strecke läuft oft auf derselben Straße hin und zurück (Wendepunkte bei km 12, 18, 20–26, 28, 35, 39–42),
# das Anlegen auf das OSM-Netz (match.py) verlor dort Stücke. Die Linie liegt auf den Straßen (siehe streets.py). -> gpx2026.json
import json, math, re
t = open("../dl/sydney2026_offiziell.gpx").read()
P = [(float(a), float(b)) for a, b in re.findall(r'lat="([-\d.]+)"\s+lon="([-\d.]+)"', t)]
def hav(p, q):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
d = [0.0]
for i in range(1, len(P)): d.append(d[-1] + hav(P[i - 1], P[i]))
json.dump({"pts": [(a, b, 0.0) for a, b in P], "d": d}, open("gpx2026.json", "w"))
print(len(P), "Punkte", round(d[-1]), "m")
