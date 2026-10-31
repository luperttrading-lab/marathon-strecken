# Strecke aus der Google-Karte des Veranstalters „Strecke Salzburg Marathon“ (verlinkt im „Eventguide Lauffestspiele der
# Mozartstadt 2026“ auf salzburg-marathon.at, mid=1vlZE3NUVGTzmIZemOiiAyM9z0kypvUw), als KML:
# https://www.google.com/maps/d/kml?mid=1vlZE3NUVGTzmIZemOiiAyM9z0kypvUw&forcekml=1 (../dl/karten/karte_….kml).
# Ordner „MARATHON Strecke“: eine Linie (900 Punkte, laut Beschreibung „importierte Daten … 28. Februar 2024, Entfernung 43,1 km“;
# beide Runden, vom Start auf der Staatsbrücke bis zum Ziel am Max-Reinhardt-Platz), Start, Ziel, zwei Staffelzonen,
# Verpflegung, Wasser, Cheering Zones und Musikspots 2026; Ordner „MARATHON KM PUNKTE“: KM 3 bis KM 42 (km 1 und 2 fehlen).
# Der Kurs ist laut den Streckenplänen 2024, 2025 und 2026 derselbe.
# -> linie.json (Punkte und laufende Länge, geodätisch GRS80), marken.json (Linienmeter jeder Marke und jedes Punkts)
import json, re, sys, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer, Geod
NS = {"k": "http://www.opengis.net/kml/2.2"}
T = Transformer.from_crs(4326, 31258, always_xy=True)   # MGI / Austria GK M31 (Salzburg), nur zum Projizieren
r = ET.parse("../dl/karten/karte_1vlZE3NUVGTzmIZemOiiAyM9z0kypvUw.kml").getroot()
linien, punkte = {}, []
for fo in r.iter("{http://www.opengis.net/kml/2.2}Folder"):
    ordner = " ".join(fo.find("k:name", NS).text.split())
    for pm in fo.findall("k:Placemark", NS):
        n = " ".join((pm.find("k:name", NS).text or "").split())
        ls = pm.find(".//k:LineString/k:coordinates", NS); pt = pm.find(".//k:Point/k:coordinates", NS)
        if ls is not None: linien[n] = [(float(c.split(",")[1]), float(c.split(",")[0])) for c in ls.text.split()]
        elif pt is not None:
            lo, la = map(float, pt.text.strip().split(",")[:2]); punkte.append((ordner, n, la, lo))
assert len(linien) == 1
pts = list(linien.values())[0]
xy = np.array([T.transform(lo, la) for la, lo in pts]); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
_, _, dd = Geod(ellps="GRS80").inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
dd = np.asarray(dd); d = np.r_[0, np.cumsum(dd)]
print(f"Linie: {len(pts)} Punkte, {d[-1]:.1f} m geodätisch ({dl[-1]:.1f} m GK); Abstand Median {np.median(dd):.1f} m, max {dd.max():.0f} m")
def projiziere(la, lo, s_von=0, s_bis=1e9, erwartet=None):
    """Linienmeter (GK) des nächsten Punkts der Linie im Fenster [s_von, s_bis]; liegen mehrere Stellen höchstens 15 m neben dem
    Punkt (beide Runden auf derselben Straße), gilt die nächste zur erwarteten Stelle."""
    p = np.array(T.transform(lo, la)); kand = []
    for i in range(len(xy) - 1):
        if dl[i + 1] < s_von or dl[i] > s_bis: continue
        a_, b_ = xy[i], xy[i + 1]; v = b_ - a_; t = np.clip(np.dot(p - a_, v) / (np.dot(v, v) or 1), 0, 1); q = a_ + t * v
        kand.append((float(np.hypot(*(p - q))), float(dl[i] + t * np.hypot(*v))))
    dmin = min(k[0] for k in kand)
    if erwartet is None: return min(kand)[::-1]
    nah = [k for k in kand if k[0] <= max(15, dmin + 1)]
    best = min(nah, key=lambda k: abs(k[1] - erwartet)); return best[1], best[0]
fak = dl[-1] / 42195
marken = {"km": [], "punkte": []}
for o, n, la, lo in punkte:
    m = re.fullmatch(r"KM (\d+)", n)
    if m:
        km = int(m.group(1)); s_, e_ = projiziere(la, lo, (km - 1.5) * 1000 * fak, (km + 1.5) * 1000 * fak, km * 1000 * fak)
        marken["km"].append([km, s_, round(e_, 1)])
# Punkte mit zwei Durchgängen (Runde 1 und 2) je zweimal; erwartete Lage aus der km-Angabe des Verpflegungsplans
# („Versorgungsaufbau“, verlinkt auf der Seite „Wichtige Informationen PUMA Salzburg Marathon“ 2026)
KM = {"Start PUMA Salzburg Marathon": [0], "FINISH LINE PUMA SALZBURG MARATHON": [42.195], "Relay Zone 1": [15.2, 36.3],
      "Relay Zone 2": [21.1], "Aid Station Hellbrunn": [5.5, 26.6], "Aid Station Leopoldskron": [10.9, 32.0],
      "Aid Station Maxglan": [15.2, 36.3], "Aid Station Markus-Sittikus-Straße": [19.4, 40.5], "Aid Station Finish Area": [21.2, 42.195],
      "Water Station Gneis": [9.8, 30.9], "Water Station NaWi (2nd lap only)": [23.2]}
for o, n, la, lo in punkte:
    if n not in KM: continue
    for km in KM[n]:
        s_, e_ = projiziere(la, lo, max(0, (km - 1.5) * 1000 * fak), (km + 1.5) * 1000 * fak, km * 1000 * fak)
        marken["punkte"].append([km, s_, round(e_, 1), n, la, lo])
for k in marken:   # Linienmeter geodätisch wie in linie.json
    marken[k] = sorted([[m[0], round(float(np.interp(m[1], dl, d)), 1)] + m[2:] for m in marken[k]])
json.dump({"pts": pts, "d": d.tolist()}, open("linie.json", "w"))
json.dump(marken, open("marken.json", "w"), ensure_ascii=False, indent=0)
prev = None
for km, s, e in marken["km"]:
    print(f"KM {km:2d}: {s:8.1f} m  ({e:4.1f} m neben der Linie)" + (f"  Abstand {s - prev[1]:6.1f} je km {(s - prev[1]) / (km - prev[0]):6.1f}" if prev else ""))
    prev = (km, s)
for p in marken["punkte"]: print(f"{p[0]:6.2f} km: {p[1]:8.1f} m  ({p[2]:4.1f} m)  {p[3]}")
