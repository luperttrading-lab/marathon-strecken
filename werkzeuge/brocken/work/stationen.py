# Verpflegung: die neun Stellen laut Veranstalter (Seite „Strecken“, Brocken-Marathon, Tabelle „Verpflegungsstelle / bei km / Ausgabe in der
# Zeit“): Ilsetal 9 (9:00–10:30 Uhr), Stempelsbuche 15 (9:30–11:30), Eiserner Tisch (Tränke) 17 (10:00–12:00), Knochenbrecher 21
# (10:15–12:30), Brockenbett 24 (10:30–13:00), Skihütte Hohnekopf 30 (10:30–13:30), Steinerne Renne 34 (10:45–14:00), Mönchsbuche 37
# (11:00–14:15), Kastanienplatz (Tränke) 39 (11:00–14:30). „Tränke“ = nur Getränke. Seine Kilometer sind ganze Zahlen; die Lage kommt
# deshalb aus dem Ort: wo OpenStreetMap den Namen an der Strecke kennt (Wegweiser Stempelsbuche, Ort Knochenbrecherkurve, Wegweiser
# Brockenstraße/Glashüttenweg = Brockenbett, Anfang des Wanderwegs „Brockenbett – Glashüttenweg – Drei Annen Hohne“, Haltestelle und
# Wegweiser Hohnepfahl an den Skihütten, Naturdenkmal Mönchsbuche, Ort Kastanienplatz), sonst aus dem „V“ der Streckenkarte (georef.py,
# etwa ±0,2 km): Ilsetal, Eiserner Tisch, Steinerne Renne (das „V“ steht am Forsthaus Hanneckenbruch).
# -> stationen.json [[Art, Name, km laut Veranstalter, Ausgabe, Linienmeter, Herkunft, Abstand zur Linie]]
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("gelegt.json")); d = np.array(g["d"]); Q = np.array(g["pts"])
ss = np.arange(0, d[-1], 2.0); E, N = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); baum = cKDTree(np.c_[E, N])
o = json.load(open("../dl/osm_netz.json"))["punkte"]
def osm(name, **tags):
    kand = [(la, lo) for tg, (la, lo) in o.values() if tg.get("name") == name and all(tg.get(k) == v for k, v in tags.items())]
    assert kand, name
    best = None
    for la, lo in kand:
        dist, i = baum.query(T.transform(lo, la))
        if best is None or dist < best[1]: best = (float(ss[i]), float(dist))
    return best
V = sorted(json.load(open("karte_km.json"))["v"])          # [Linienmeter, Abstand, x, y], nach Linienmeter
def karte(km):   # das „V“ der Karte, das dem Kilometer des Veranstalters am nächsten liegt (ohne Start/Ziel und Legende)
    f = d[-1] / 42195.0
    v = min((x for x in V if x[1] < 400 and 1000 < x[0] < d[-1] - 1000), key=lambda x: abs(x[0] - km * 1000 * f))
    return float(v[0]), float(v[1])
VP = [("food", "Ilsetal", 9, "9:00–10:30", "karte"),
      ("food", "Stempelsbuche", 15, "9:30–11:30", ("Stempelsbuche", {"tourism": "information"})),
      ("water", "Eiserner Tisch", 17, "10:00–12:00", "karte"),
      ("food", "Knochenbrecher", 21, "10:15–12:30", ("Knochenbrecherkurve", {"place": "locality"})),
      ("food", "Brockenbett", 24, "10:30–13:00", ("Brockenstraße Glashüttenweg", {"tourism": "information"})),
      ("food", "Skihütte Hohnekopf", 30, "10:30–13:30", ("Hohnepfahl", {"tourism": "information"})),
      ("food", "Steinerne Renne", 34, "10:45–14:00", "karte"),
      ("food", "Mönchsbuche", 37, "11:00–14:15", ("Mönchsbuche", {"natural": "tree"})),
      ("water", "Kastanienplatz", 39, "11:00–14:30", ("Kastanienplatz", {"place": "locality"}))]
out = []
for art, name, km, zeit, q in VP:
    if q == "karte": s, dist = karte(km); her = "Streckenkarte"
    else: s, dist = osm(q[0], **q[1]); her = "OSM " + q[0]
    out.append([art, name, km, zeit, s, her, round(dist, 1)])
    print(f"{name:20s} km {km:2d} laut Veranstalter, hier km {s * 42195 / d[-1] / 1000:5.2f} ({her}, {dist:.0f} m neben der Linie)")
json.dump(out, open("stationen.json", "w"), ensure_ascii=False)
