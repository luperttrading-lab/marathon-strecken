# Strecke aus der Garmin-Connect-Strecke des Veranstalters: Die Seiten „Marathon“ und „Halbmarathon“ (grazmarathon.at/bewerbe/marathon/,
# …/halbmarathon/) betten unter „Strecke 2027“ die Garmin-Strecke 265629398 ein („Graz Halb- und Marathon 2026 (21km Schleife) NEU“,
# angelegt 01.05.2024, geändert 21.09.2026). Die Einbettung https://connect.garmin.com/modern/course/embed/265629398 liefert ohne
# Anmeldung die ganze Strecke im Seitentext (Next.js, ../dl/garmin/embed_265629398.html -> course_265629398.json, ohne Namen des
# Anlegers): 2548 Punkte mit Garmin-Höhen (die App nimmt sie nicht), 21 337 m. Eine Runde; der Marathon läuft sie zweimal
# (Staffelübergaben bei km 10 und 31,1 an derselben Stelle, Höhenbild „Auf einen Blick“ mit zwei gleichen Hälften). Die Linie folgt
# den OSM-Straßen (im Median 1,5 m daneben, 99 % bis 7 m; längere gerade Stücke sind gerade Straßen).
# Bereinigt: Vier kurze Spitzen, in denen die Linie über eine Kreuzung hinaus- und auf derselben Spur zurückläuft (Rest des Routenplaners
# beim Setzen von Wegpunkten: Joanneumring/Neutorgasse, Wielandgasse, Schönaugürtel/Conrad-von-Hötzendorf-Straße, Schönaugürtel/
# Schönaugasse, zusammen 96 m Linie), werden herausgeschnitten. Die Wende Nord in der Weinzöttlstraße (Hin- und Rückweg auf derselben
# Fahrbahn) bleibt.
# -> runde.json {"pts": [[lat, lon, Garmin-Höhe]…], "d": laufende Länge geodätisch, "spitzen": [[Linienmeter, Länge]…] der Rohlinie,
#     "wende": [Index Wende Süd, Index Wende Nord]}
import json, re
import numpy as np
from pyproj import Geod, Transformer
from scipy.spatial import cKDTree
def kurs(datei):
    s = open(datei, encoding="utf-8").read()
    teile = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', s, flags=re.S)
    txt = "".join(json.loads('"' + p + '"') for p in teile)
    i = txt.find('{"course":'); tiefe = 0
    for j in range(i, len(txt)):
        if txt[j] == "{": tiefe += 1
        elif txt[j] == "}":
            tiefe -= 1
            if tiefe == 0: break
    return json.loads(txt[i:j + 1])["course"]
o = kurs("../dl/garmin/embed_265629398.html")
json.dump({k: v for k, v in o.items() if k not in ("firstName", "lastName", "displayName", "userProfilePk")},
          open("../dl/garmin/course_265629398.json", "w"), ensure_ascii=False)
pts = [(p["latitude"], p["longitude"], p["elevation"]) for p in o["geoPoints"]]
n0 = len(pts)
pts = [p for i, p in enumerate(pts) if i == 0 or (round(p[0], 7), round(p[1], 7)) != (round(pts[i - 1][0], 7), round(pts[i - 1][1], 7))]
G = Geod(ellps="WGS84")
def laenge(pts):
    _, _, dd = G.inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
    return np.r_[0, np.cumsum(dd)]
d0 = laenge(pts); A = np.array(pts)
print(f"{o['courseName'].strip()}: {n0} Punkte, {len(pts)} ohne doppelte, {d0[-1]:.1f} m (Garmin {o['distanceMeter']} m); geändert {o['updateDate']}")
# Spitzen: Punkt, zu dem die Linie nach 4–60 m bis auf 1 m zurückkehrt (Linie alle 0,5 m), außer an der Wende Nord (nördlichster Punkt)
T = Transformer.from_crs(4326, 25833, always_xy=True)
s = np.arange(0, d0[-1], 0.5); x, y = T.transform(np.interp(s, d0, A[:, 1]), np.interp(s, d0, A[:, 0])); Y = np.c_[x, y]; b = cKDTree(Y)
nord = d0[int(np.argmax(A[:, 0]))]
spitzen, i = [], 0
while i < len(Y):
    spaeter = [j for j in b.query_ball_point(Y[i], 1.0) if 4 < s[j] - s[i] < 60]
    if spaeter and abs(s[i] - nord) > 300:
        j = max(spaeter); spitzen.append((float(s[i]), float(s[j] - s[i]))); i = j + 1
    else: i += 1
# Schnitt genau am Fuß der Spitze: Punkt bei a einfügen, alles zwischen a und a + l weglassen (beide Stellen liegen höchstens 1 m auseinander)
def bei(x): return tuple(float(np.interp(x, d0, A[:, k])) for k in range(3))
neu, rest = [], list(zip(d0, pts))
for a, l in spitzen:
    neu += [p for x, p in rest if x <= a] + [bei(a)]; rest = [(x, p) for x, p in rest if x >= a + l]
    print(f"  Spitze bei Linienmeter {a:.0f} ({bei(a)[0]:.5f}, {bei(a)[1]:.5f}): {l:.1f} m Linie entfernt")
pts = neu + [p for _, p in rest]
dist = laenge(pts); dd = np.diff(dist)
print(f"Bereinigt: {len(pts)} Punkte, {dist[-1]:.1f} m, Abstand Median {np.median(dd):.1f} m, max {dd.max():.0f} m")
print("Anfang", pts[0], "Ende", pts[-1], "Abstand Anfang–Ende", round(G.inv(pts[0][1], pts[0][0], pts[-1][1], pts[-1][0])[2], 1), "m")
A = np.array(pts); wende = [int(np.argmin(A[:, 0])), int(np.argmax(A[:, 0]))]
print(f"Wende Süd bei Linienmeter {dist[wende[0]]:.0f}, Wende Nord bei {dist[wende[1]]:.0f}")
json.dump({"pts": pts, "d": dist.tolist(), "spitzen": spitzen, "wende": wende}, open("runde.json", "w"))
