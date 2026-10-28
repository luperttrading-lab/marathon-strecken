# Strecke aus der Google-Karte des Veranstalters (Tokyo Marathon Foundation, auf marathon.tokyo/en/about/course/ eingebettet,
# Stand Kurs 2026; die Seite für 2027 zeigt dieselbe Karte): Linie „走路 Route“, Start (Tokyo Metropolitan Government),
# Ziel (Gyoko-dori vor dem Bahnhof Tokio), 42 Kilometermarken, Halbmarathon, Getränkestellen, Kontrollpunkte.
# -> gpx2026.json (Punkte und laufende Länge), marken.json (Linienmeter jeder Marke)
import json, math, re, xml.etree.ElementTree as ET
import numpy as np
NS = {"k": "http://www.opengis.net/kml/2.2"}
r = ET.parse("../dl/karte_1jGYjkrF_m5K3rWgYJu1XqyMbjHPq2pQ.kml").getroot()
def hav(p, q):
    R = 6371008.8; la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
linien, punkte = [], {}
for fo in r.iter("{http://www.opengis.net/kml/2.2}Folder"):
    ordner = fo.find("k:name", NS).text
    for pm in fo.findall("k:Placemark", NS):
        n = (pm.find("k:name", NS).text or "").strip()
        lss = pm.findall(".//k:LineString/k:coordinates", NS); pt = pm.find(".//k:Point/k:coordinates", NS)
        for ls in lss: linien.append((ordner, n, [(float(c.split(",")[1]), float(c.split(",")[0])) for c in ls.text.split()]))
        if not lss and pt is not None: lo, la = map(float, pt.text.strip().split(",")[:2]); punkte.setdefault(ordner, []).append((n, la, lo))
for o, n, p in linien: print("Linie", o, n.replace("\n", " "), len(p), "Punkte", round(sum(hav(a, b) for a, b in zip(p, p[1:])) / 1000, 3), "km", p[0], p[-1])
# Die Linie liegt in zwei Stücken rückwärts vor (Ziel -> Wendepunkt Ueno-hirokoji, Wendepunkt -> Start): umdrehen, zusammensetzen
(_, _, a), (_, _, b) = linien
pts = a[::-1] + b[::-1][1:]
assert hav(a[0], b[-1]) < 1, "Stücke schließen nicht aneinander"
from pyproj import Transformer
T = Transformer.from_crs(4326, 32654, always_xy=True)   # UTM 54N
xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
def projiziere(la, lo, s_von=0, s_bis=1e9, erwartet=None):
    """Linienmeter des nächsten Punkts der Linie im Fenster [s_von, s_bis]. Die Strecke läuft teils auf derselben Straße hin
    und zurück (Wendepunkte): liegen mehrere Stellen höchstens 15 m neben der Marke, gilt die, die der erwarteten am nächsten ist."""
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
start = [p for p in punkte["走路　Route"] if p[0].startswith("スタート")][0]; ziel = [p for p in punkte["走路　Route"] if p[0].startswith("フィニッシュ")][0]
s0, e0 = projiziere(start[1], start[2], 0, 500); s1, e1 = projiziere(ziel[1], ziel[2], dl[-1] - 500, dl[-1])
print(f"Linie {dl[-1]:.0f} m; Start bei {s0:.0f} m ({e0:.0f} m daneben), Ziel bei {s1:.0f} m ({e1:.0f} m daneben)")
# Linie auf Start und Ziel schneiden
def schnitt(s):
    i = min(np.searchsorted(dl, s), len(dl) - 1); f = (s - dl[i - 1]) / ((dl[i] - dl[i - 1]) or 1)
    return i, (pts[i - 1][0] + f * (pts[i][0] - pts[i - 1][0]), pts[i - 1][1] + f * (pts[i][1] - pts[i - 1][1]))
i0, p0 = schnitt(s0); i1, p1 = schnitt(s1)
neu = [p0] + pts[i0:i1] + [p1]
d = [0.0]
for i in range(1, len(neu)): d.append(d[-1] + hav(neu[i - 1], neu[i]))
json.dump({"pts": [(la, lo, 0.0) for la, lo in neu], "d": d}, open("gpx2026.json", "w"))
pts = neu; xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
print(f"geschnitten: {dl[-1]:.0f} m (Haversine {d[-1]:.0f} m), {len(pts)} Punkte")
# Marken auf die Linie: im Fenster um die erwartete Stelle (km k bei k/42,195 der Linie, ±1,2 km)
marken = {"km": [], "verpflegung": [], "kontrolle": []}
fak = dl[-1] / 42195.0
for n, la, lo in punkte["距離表示　Kilometer Markers"]:
    km = 21.0975 if "Half" in n or "中間" in n else float(re.match(r"(\d+)km", n).group(1))
    s_, e_ = projiziere(la, lo, (km - 1.2) * 1000 * fak, (km + 1.2) * 1000 * fak, km * 1000 * fak); marken["km"].append([km, round(float(s_), 1), round(float(e_), 1)])
for n, la, lo in punkte["給水所 Aid Stations"]:
    km = float(re.search(r"(\d+)km", n).group(1)); s_, e_ = projiziere(la, lo, (km - 1.2) * 1000 * fak, (km + 1.2) * 1000 * fak)
    marken["verpflegung"].append([km, round(float(s_), 1), round(float(e_), 1)])
for n, la, lo in punkte["収容関門　Checkpoints"]:
    km = float(re.search(r"([\d.]+)km", n).group(1)); s_, e_ = projiziere(la, lo, (km - 1.2) * 1000 * fak, (km + 1.2) * 1000 * fak)
    marken["kontrolle"].append([km, round(float(s_), 1), round(float(e_), 1)])
# Linienmeter wie in gpx2026.json (Haversine), nicht in UTM: die Projektion rechnet in UTM 54N (Maßstab gut 0,999 hier)
for k in marken: marken[k] = sorted([m, round(float(np.interp(s_, dl, d)), 1), e_] for m, s_, e_ in marken[k])
json.dump(marken, open("marken.json", "w"), indent=0)
km = np.array(marken["km"])
print("Abstand der km-Marken zur Linie: max %.0f m" % km[:, 2].max())
voll = km[km[:, 0] == np.round(km[:, 0])]
print("Linienmeter je km (Marke zu Marke):", [int(round(x)) for x in np.diff(np.r_[0, voll[:, 1]])])
print("Verpflegung (km, Linienmeter, Abstand):", marken["verpflegung"])
