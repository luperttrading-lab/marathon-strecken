# Strecke aus der Google-Karte des Veranstalters (Valencia Ciudad del Running / S.D. Correcaminos, eingebettet auf
# valenciaciudaddelrunning.com/maraton/recorrido-maraton/, Karte „42KVALENCIA INFO CARRERA“, Ordner „42K 2025“): Linie
# „RECORRIDO · RACE LINE“, km 0 (Start), META (Ziel), 42 Kilometermarken, Halbmarathon, Getränkestellen (AVITUALLAMIENTO),
# Gel-Stellen (RED POINT ENERVIT). Der Plan 2026 des Veranstalters (recorrido-42k-valencia-2026.pdf) zeigt denselben Weg
# (vergleich.py). -> gpx2026.json (Punkte und laufende Länge), marken.json (Linienmeter jeder Marke)
import json, math, re, xml.etree.ElementTree as ET
import numpy as np
NS = {"k": "http://www.opengis.net/kml/2.2"}
r = ET.parse("../dl/karte_1BEeuxU3kRDyxewR7Pp4Rqu_7Knajvxo.kml").getroot()
def hav(p, q):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
linien, punkte = {}, {}
for fo in r.iter("{http://www.opengis.net/kml/2.2}Folder"):
    ordner = fo.find("k:name", NS).text.strip()
    for pm in fo.findall("k:Placemark", NS):
        n = " ".join((pm.find("k:name", NS).text or "").split())
        ls = pm.find(".//k:LineString/k:coordinates", NS); pt = pm.find(".//k:Point/k:coordinates", NS)
        if ls is not None: linien[n] = [(float(c.split(",")[1]), float(c.split(",")[0])) for c in ls.text.split()]
        elif pt is not None: lo, la = map(float, pt.text.strip().split(",")[:2]); punkte.setdefault(ordner, []).append((n, la, lo))
for n, p in linien.items(): print("Linie", n, len(p), "Punkte", round(sum(hav(a, b) for a, b in zip(p, p[1:])) / 1000, 3), "km", p[0], p[-1])
# Hauptlinie; „RECORRIDO 2“ ist nur die zweite Fahrbahn der ersten 1000 m (Startfeld auf beiden Seiten der Plaça d'Europa)
pts = linien["RECORRIDO · RACE LINE"]
from pyproj import Transformer
T = Transformer.from_crs(4326, 25830, always_xy=True)   # ETRS89 / UTM 30N
xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
def projiziere(la, lo, s_von=0, s_bis=1e9, erwartet=None):
    """Linienmeter des nächsten Punkts der Linie im Fenster [s_von, s_bis]. Die Strecke läuft teils auf derselben Straße hin
    und zurück (Tarongers, Blasco Ibáñez, Port): liegen mehrere Stellen höchstens 15 m neben der Marke, gilt die, die der
    erwarteten am nächsten ist."""
    p = np.array(T.transform(lo, la)); kand = []
    for i in range(len(xy) - 1):
        if dl[i + 1] < s_von or dl[i] > s_bis: continue
        a_, b_ = xy[i], xy[i + 1]; v = b_ - a_; t = np.clip(np.dot(p - a_, v) / (np.dot(v, v) or 1), 0, 1); q = a_ + t * v
        kand.append((float(np.hypot(*(p - q))), float(dl[i] + t * np.hypot(*v))))
    dmin = min(k[0] for k in kand)
    if erwartet is not None:
        nah = [k for k in kand if k[0] <= max(15, dmin + 1)]
        best = min(nah, key=lambda k: abs(k[1] - erwartet))
    else: best = min(kand)
    return best[1], best[0]
alle = [p for o in punkte.values() for p in o]
start = [p for p in punkte["42K 2025"] if p[0] == "km 0"][0]; ziel = [p for p in punkte["42K 2025"] if p[0].startswith("META")][0]
s0, e0 = projiziere(start[1], start[2], 0, 500); s1, e1 = projiziere(ziel[1], ziel[2], dl[-1] - 500, dl[-1])
print(f"Linie {dl[-1]:.0f} m; Start bei {s0:.1f} m ({e0:.1f} m daneben), Ziel bei {s1:.1f} m ({e1:.1f} m daneben), Linienende {dl[-1]:.1f}")
def schnitt(s):
    i = min(max(1, np.searchsorted(dl, s)), len(dl) - 1); f = (s - dl[i - 1]) / ((dl[i] - dl[i - 1]) or 1)
    return i, (pts[i - 1][0] + f * (pts[i][0] - pts[i - 1][0]), pts[i - 1][1] + f * (pts[i][1] - pts[i - 1][1]))
i0, p0 = schnitt(s0); i1, p1 = schnitt(s1)
neu = [p0] + pts[i0:i1] + [p1]
# Linienmeter geodätisch (GRS80); Haversine auf der Kugel wäre hier 0,05 % zu kurz
from pyproj import Geod
_, _, dd = Geod(ellps="GRS80").inv([p[1] for p in neu[:-1]], [p[0] for p in neu[:-1]], [p[1] for p in neu[1:]], [p[0] for p in neu[1:]])
d = [0.0] + np.cumsum(dd).tolist()
json.dump({"pts": [(la, lo, 0.0) for la, lo in neu], "d": d}, open("gpx2026.json", "w"))
pts = neu; xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
print(f"geschnitten: {dl[-1]:.0f} m in UTM, geodätisch {d[-1]:.1f} m, {len(pts)} Punkte")
marken = {"km": [], "verpflegung": [], "gel": []}
fak = dl[-1] / 42195.0
def km_aus(n):
    m = re.search(r"KM\s*(\d+)(?:['’,](\d+))?", n, re.I)
    return float(m.group(1) + ("." + m.group(2) if m.group(2) else ""))
for n, la, lo in punkte["42K 2025"]:
    if n.startswith("MEDIA MARAT"): km = 21.0975
    elif re.fullmatch(r"km \d+", n) and n != "km 0": km = float(n.split()[1])
    else: continue
    s_, e_ = projiziere(la, lo, (km - 1.2) * 1000 * fak, (km + 1.2) * 1000 * fak, km * 1000 * fak); marken["km"].append([km, round(float(s_), 1), round(float(e_), 1)])
for n, la, lo in punkte["AVITUALLAMIENTO · PROVISIONING"]:
    if n.startswith("AVITUALLAMIENTO"): k = "verpflegung"
    elif n.startswith("RED POINT"): k = "gel"
    else: continue
    km = km_aus(n); s_, e_ = projiziere(la, lo, (km - 1.2) * 1000 * fak, (km + 1.2) * 1000 * fak, km * 1000 * fak)
    marken[k].append([km, round(float(s_), 1), round(float(e_), 1)])
# Linienmeter wie in gpx2026.json (geodätisch), nicht in UTM (Maßstab in UTM 30N bei 0,36° W gut 1,0002)
for k in marken: marken[k] = sorted([m, round(float(np.interp(s_, dl, d)), 1), e_] for m, s_, e_ in marken[k])
json.dump(marken, open("marken.json", "w"), indent=0)
km = np.array(marken["km"])
print("Abstand der km-Marken zur Linie: max %.0f m" % km[:, 2].max(), [(m, e) for m, s, e in marken["km"] if e > 10])
voll = km[km[:, 0] == np.round(km[:, 0])]
print("Linienmeter je km (Marke zu Marke):", [int(round(x)) for x in np.diff(np.r_[0, voll[:, 1]])], "Rest", round(d[-1] - voll[-1, 1]))
print("Verpflegung (km, Linienmeter, Abstand):", marken["verpflegung"]); print("Gel:", marken["gel"])
