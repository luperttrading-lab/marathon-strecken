# Strecke aus der Google-Karte des Veranstalters (Osaka Marathon, auf osaka-marathon.com/2026/info/course/ eingebettet,
# Karte „大阪マラソン2026 Osaka Marathon 2026“; die Seite für 2027 zeigt dieselbe Streckenkarte): Linie „走路 Route“,
# Start (大阪府庁前), Ziel (大阪城公園), Kilometermarken alle 5 km und Halbmarathon (中間点), Getränkestellen (給水) und
# Kontrollpunkte (収容関門) mit Kilometerangabe im Namen.
# -> gpx2026.json (Punkte und laufende Länge), marken.json (Linienmeter jeder Marke)
import json, math, re, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Geod, Transformer
NS = {"k": "http://www.opengis.net/kml/2.2"}
r = ET.parse("../dl/karte_1pWXP58aD4dUxOsWy6nTnC8iqO31PGfc.kml").getroot()
G = Geod(ellps="WGS84")
def laenge(p, q): return G.inv(p[1], p[0], q[1], q[0])[2]   # Meter auf dem Ellipsoid
linien, punkte = [], {}
for fo in r.iter("{http://www.opengis.net/kml/2.2}Folder"):
    ordner = fo.find("k:name", NS).text.split()[0]
    for pm in fo.findall("k:Placemark", NS):
        n = (pm.find("k:name", NS).text or "").strip()
        lss = pm.findall(".//k:LineString/k:coordinates", NS); pt = pm.find(".//k:Point/k:coordinates", NS)
        for ls in lss: linien.append((ordner, n, [(float(c.split(",")[1]), float(c.split(",")[0])) for c in ls.text.split()]))
        if not lss and pt is not None: lo, la = map(float, pt.text.strip().split(",")[:2]); punkte.setdefault(ordner, []).append((n, la, lo))
pts = [p for o, n, p in linien if o == "走路" and n.startswith("走路")][0]   # in Laufrichtung, ein Stück
print("Linie", len(pts), "Punkte", round(sum(laenge(a, b) for a, b in zip(pts, pts[1:])) / 1000, 3), "km", pts[0], pts[-1])
T = Transformer.from_crs(4326, 32653, always_xy=True)   # UTM 53N
xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
def projiziere(la, lo, s_von=0, s_bis=1e9, erwartet=None):
    """Linienmeter des nächsten Punkts der Linie im Fenster [s_von, s_bis]. Die Strecke läuft auf drei Stichen (Minato-dōri,
    Naniwa-suji, Matsuyamachi-suji) auf derselben Straße hin und zurück: liegen mehrere Stellen höchstens 15 m neben der
    Marke, gilt die, die der erwarteten am nächsten ist."""
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
start = [p for p in punkte["走路"] if p[0] == "START"][0]; ziel = [p for p in punkte["走路"] if p[0] == "FINISH"][0]
s0, e0 = projiziere(start[1], start[2], 0, 500); s1, e1 = projiziere(ziel[1], ziel[2], dl[-1] - 500, dl[-1])
print(f"Linie {dl[-1]:.0f} m (UTM); Start bei {s0:.0f} m ({e0:.0f} m daneben), Ziel bei {s1:.0f} m ({e1:.0f} m daneben)")
def schnitt(s):
    i = min(max(1, np.searchsorted(dl, s)), len(dl) - 1); f = (s - dl[i - 1]) / ((dl[i] - dl[i - 1]) or 1)
    return i, (pts[i - 1][0] + f * (pts[i][0] - pts[i - 1][0]), pts[i - 1][1] + f * (pts[i][1] - pts[i - 1][1]))
i0, p0 = schnitt(s0); i1, p1 = schnitt(s1)
neu = [p0] + pts[i0:i1] + [p1]
d = [0.0]
for i in range(1, len(neu)): d.append(d[-1] + laenge(neu[i - 1], neu[i]))
json.dump({"pts": [(la, lo, 0.0) for la, lo in neu], "d": d}, open("gpx2026.json", "w"))
pts = neu; xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
print(f"geschnitten: {dl[-1]:.0f} m UTM, {d[-1]:.0f} m auf dem Ellipsoid, {len(pts)} Punkte")
# Marken auf die Linie: im Fenster um die erwartete Stelle (km k bei k/42,195 der Linie, ±1,5 km)
marken = {"km": [], "verpflegung": [], "kontrolle": []}
fak = dl[-1] / 42195.0
for n, la, lo in punkte["距離表示"]:
    km = 21.0975 if "中間" in n else float(re.match(r"(\d+)km", n).group(1))
    s_, e_ = projiziere(la, lo, (km - 1.5) * 1000 * fak, (km + 1.5) * 1000 * fak, km * 1000 * fak); marken["km"].append([km, round(float(s_), 1), round(float(e_), 1)])
for n, la, lo in punkte["給水"]:
    m = re.match(r"([\d.]+)km", n)
    if not m: continue   # „スタート前給水“ im Startbereich
    km = float(m.group(1)); s_, e_ = projiziere(la, lo, (km - 1.5) * 1000 * fak, (km + 1.5) * 1000 * fak, km * 1000 * fak)
    marken["verpflegung"].append([km, round(float(s_), 1), round(float(e_), 1), n])
for n, la, lo in punkte["救護所・収容関門"]:
    m = re.match(r"([\d.]+)km収容関門", n)
    if not m: continue
    km = float(m.group(1)); s_, e_ = projiziere(la, lo, (km - 1.5) * 1000 * fak, (km + 1.5) * 1000 * fak, km * 1000 * fak)
    marken["kontrolle"].append([km, round(float(s_), 1), round(float(e_), 1)])
# Linienmeter wie in gpx2026.json (Ellipsoid), nicht in UTM: die Projektion rechnet in UTM 53N
for k in marken: marken[k] = sorted([m[0], round(float(np.interp(m[1], dl, d)), 1), *m[2:]] for m in marken[k])
json.dump(marken, open("marken.json", "w"), indent=0, ensure_ascii=False)
km = np.array([m[:3] for m in marken["km"]])
print("Abstand der km-Marken zur Linie: max %.0f m" % km[:, 2].max())
print("km-Marken (km, Linienmeter, Abstand):", marken["km"])
print("Linienmeter je Abschnitt:", [(a[0], b[0], round(b[1] - a[1])) for a, b in zip([[0, 0]] + marken["km"], marken["km"] + [[42.195, d[-1]]])])
print("Verpflegung (km, Linienmeter, Abstand):", [m[:3] for m in marken["verpflegung"]])
print("Kontrollen (km, Linienmeter, Abstand):", marken["kontrolle"])
