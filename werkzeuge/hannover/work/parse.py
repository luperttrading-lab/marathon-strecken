# Strecke aus der Google-My-Maps-Karte des Veranstalters („Interaktive Karte“ auf marathon-hannover.de/strecken/streckenverlauf.html,
# eingebettet als google.com/maps/d/embed?mid=1uoNL65nZY9ycqJT8_tkXr18USC2-Blw; als KML ohne Anmeldung:
# google.com/maps/d/kml?mid=1uoNL65nZY9ycqJT8_tkXr18USC2-Blw&forcekml=1 -> ../dl/kml/mymaps.kml). Ebenen: Linien „Marathon“,
# „Halbmarathon“, „10km - Lauf“, Kilometerpunkte je Lauf, „EP's & VP's“ (15 Erfrischungs- und Verpflegungspunkte) und
# „Wechselzonen“ (5 Staffelwechsel). Höhen hat die Linie keine (0).
# -> gpx2026.json (Punkte [lat, lon] der Marathonlinie und laufende Länge, geodätisch WGS 84), kml_punkte.json (alle Punkte)
import json, re
import numpy as np
from pyproj import Geod
s = open("../dl/kml/mymaps.kml", encoding="utf-8").read()
def cdata(x): return re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", x, flags=re.S).strip()
linien, punkte = {}, {}
for f in re.findall(r"<Folder>(.*?)</Folder>", s, flags=re.S):
    fn = cdata(re.search(r"<name>(.*?)</name>", f, flags=re.S).group(1))
    for p in re.findall(r"<Placemark>(.*?)</Placemark>", f, flags=re.S):
        n = cdata(re.search(r"<name>(.*?)</name>", p, flags=re.S).group(1))
        cs = [tuple(map(float, c.split(",")[:2])) for c in re.search(r"<coordinates>(.*?)</coordinates>", p, flags=re.S).group(1).split()]
        if "<LineString" in p: linien[n] = [(la, lo) for lo, la in cs]
        else: punkte.setdefault(fn, []).append([n, cs[0][1], cs[0][0]])
pts = linien["Marathon"]; n0 = len(pts)
pts = [p for i, p in enumerate(pts) if i == 0 or (round(p[0], 7), round(p[1], 7)) != (round(pts[i - 1][0], 7), round(pts[i - 1][1], 7))]
G = Geod(ellps="WGS84")
_, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
dd = np.array(dd); d = np.r_[0, np.cumsum(dd)]
print(f"Marathon: {n0} Punkte, {len(pts)} ohne doppelte, {d[-1]:.1f} m geodätisch, Abstand bis {dd.max():.0f} m, Median {np.median(dd):.1f} m")
for k, v in linien.items():
    _, _, x = G.inv([p[1] for p in v[:-1]], [p[0] for p in v[:-1]], [p[1] for p in v[1:]], [p[0] for p in v[1:]])
    print(f"  Linie {k}: {len(v)} Punkte, {sum(x):.1f} m")
print("Start", pts[0], "Ende", pts[-1])
json.dump({"pts": pts, "d": d.tolist()}, open("gpx2026.json", "w"))
json.dump({"linien": linien, "punkte": punkte}, open("kml_punkte.json", "w"), ensure_ascii=False)
