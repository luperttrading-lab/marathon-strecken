# Kilometer-Stützpunkte -> marken.json {"steine": [[km, Linienmeter, Abstand zur Linie], …], "km": [[km, Linienmeter], …]}.
# Der Veranstalter veröffentlicht keine Lage seiner Kilometerschilder oder Zeitmatten (Zeitnahme alle 5 km und bei 21,1 km; der
# Streckenplan ist schematisch). Entlang der Strecke stehen aber feste Steine der „Κλασσική Διαδρομή Μαραθωνίου Δρόμου“ (Klassische
# Marathonstrecke, int_name „Athens Classic Marathon Course“) mit Kilometerzahl; in OSM eingetragen sind 33 (Agia Paraskevi,
# Mesogeion/Kapodistriou), 34 (Chalandri), 37 (Ampelokipoi, Mesogeion) und 39 (Vasilissis Sofias an der Kreuzung Kifissias/
# Alexandras; Knoten 13476572295, 13580665683, 13479112628, 13476418218; Suche in Nominatim nach dem Namen fand keine weiteren).
# Stein 39 steht genau dort, wo die Beschreibung des Veranstalters km 39 nennt („just around the corner“).
# Auf der berichtigten Linie (linie.py) liegt die Linie an allen Steinen und im Ziel 142–163 m über dem Kilometer; die 160 m kommen
# also aus den ersten 33 km (Mittellinie der Straßen statt Ideallinie, Schleife um den Tymvos). Stützpunkte: Start, Mittel der Steine
# 33 und 34 (sie liegen 1022 Linienmeter auseinander, einer ist wohl gut 10 m versetzt eingetragen), 37, 39, Ziel = 42 195 m.
import json
import numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 2100, always_xy=True)
g = json.load(open("gpx2026.json")); P = np.array(g["pts"]); d = np.array(g["d"])
xy = np.array([T.transform(b, a) for a, b, _ in P]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
def proj(la, lo):
    p = np.array(T.transform(lo, la)); a = xy[:-1]; v = xy[1:] - a
    t = np.clip(((p - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); q = a + v * t[:, None]; e = np.hypot(*(q - p).T); i = int(np.argmin(e))
    return float(np.interp(dl[i] + t[i] * np.hypot(*v[i]), dl, d)), float(e[i])
o = json.load(open("../dl/osm_netz.json"))
steine = []
for k, (tg, ll) in o["punkte"].items():
    if tg.get("highway") == "milestone" or tg.get("historic") == "milestone":
        if "μαραθ" not in tg.get("name", "").lower(): continue
        km = float(tg.get("distance") or tg.get("ref")); s, e = proj(*ll)
        steine.append([km, round(s, 1), round(e, 1)])
steine.sort()
L = d[-1]
for km, s, e in steine: print(f"Stein {km:.0f}: Linienmeter {s:8.1f} ({e:4.1f} m neben der Linie), Linie − km = {s - km * 1000:+.0f} m")
print(f"Ziel: Linienmeter {L:.1f}, Linie − km = {L - 42195:+.0f} m")
st = {km: s for km, s, _ in steine}
knoten = [[33.5, round((st[33] + st[34]) / 2, 1)], [37.0, st[37]], [39.0, st[39]]]
json.dump({"steine": steine, "km": knoten}, open("marken.json", "w"), indent=0)
print("Stützpunkte:", knoten)
