# Strecke des Brocken-Marathons aus der GPX-Datei des Veranstalters: Seite „Strecken“ (https://harz-gebirgslauf.de/strecken.html),
# Knopf „Streckenkarte anzeigen“ lädt per Leaflet-GPX /files/GPX/HGL_Brocken_Marathon_1180_HM.gpx (Last-Modified 29.02.2024,
# ../dl/gpx/). Inhalt: eine Strava-Route („Brockenmarathon 1180 Hm“, Strava-Routenplaner, © OpenStreetMap-Mitwirkende 2020),
# 1163 Punkte, Start und Ziel an der Himmelpforte in Wernigerode-Hasserode. Die Höhen der Datei (Strava) werden nicht benutzt.
# -> linie.json {"pts": [[lat, lon]…], "d": Linienmeter (geodätisch, WGS84), "ele": Höhen der GPX (nur Vergleich)}
import json, xml.etree.ElementTree as ET
from pyproj import Geod
G = Geod(ellps="WGS84"); NS = "{http://www.topografix.com/GPX/1/1}"
r = ET.parse("../dl/gpx/HGL_Brocken_Marathon_1180_HM.gpx").getroot()
pts = [(float(p.get("lat")), float(p.get("lon")), float(p.find(NS + "ele").text)) for p in r.iter(NS + "trkpt")]
# doppelte Punkte weg
P = [pts[0]] + [b for a, b in zip(pts[:-1], pts[1:]) if (a[0], a[1]) != (b[0], b[1])]
d = [0.0]
for a, b in zip(P[:-1], P[1:]): d.append(d[-1] + G.inv(a[1], a[0], b[1], b[0])[2])
print(len(P), "Punkte,", round(d[-1], 1), "m; Start", P[0][:2], "Ziel", P[-1][:2], "Abstand Start–Ziel", round(G.inv(P[0][1], P[0][0], P[-1][1], P[-1][0])[2], 1), "m")
json.dump({"pts": [[a, b] for a, b, _ in P], "d": d, "ele": [round(e, 2) for _, _, e in P]}, open("linie.json", "w"))
