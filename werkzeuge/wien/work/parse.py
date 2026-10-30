# Strecke aus der Google-Karte des Veranstalters (Vienna City Marathon, verlinkt auf vienna-marathon.com/?go=course als
# „Interaktiver Streckenplan – Sonntag“, Karte „43. Vienna City Marathon 2026 Marathon und Halbmarathon“, 19. April 2026),
# als KML: google.com/maps/d/kml?mid=1POyNKcbwqhpoS9gAsxzPgN4fyLDRwfQ&forcekml=1 (../dl/karte_….kml). Ordner
# „Marathon & Powerade Staffelmarathon“: Linie „Marathon 42,195 km“ (404 Punkte), 42 Kilometermarken, drei Staffelwechsel;
# Ordner „Start | Finish“: START A (Blöcke 1, 3, 5 = Elite, A, C, E), START B (Blöcke 2, 4, 6 auf der anderen Fahrbahn,
# eigene Linie „Streckenführung für Startblöcke 2,4,6“ bis zur Lassallestraße), FINISH; Ordner „Streckenbereich –
# Verpflegungspunkte“. Die App folgt START A.
# Start: Die Karte setzt START A an die Spitze des Elite-Blocks; bis zur Marke km 1 sind es auf der Linie aber nur 928 m, von
# Marke zu Marke danach 961–1052 m (Median 1009 m), auf den geraden ersten 2 km 997 m. Die Kilometerschilder passen also zu einer
# Startlinie rund 70 m weiter hinten auf der Wagramer Straße, Richtung U1-Station Kaisermühlen-VIC (der Startblockplan 2026 ist
# schematisch und zeigt die Startlinie nur ungefähr dort). Die Linie wird deshalb geradeaus auf der Wagramer Straße verlängert, so
# dass der erste Kilometer so lang ist wie der zweite (70 m). Ohne Verlängerung: VORLAUF = 0 setzen.
# -> gpx2026.json (Punkte und laufende Länge, geodätisch GRS80), marken.json (Linienmeter jeder Marke)
import json, re, xml.etree.ElementTree as ET
import numpy as np
from pyproj import Transformer, Geod
NS = {"k": "http://www.opengis.net/kml/2.2"}
T = Transformer.from_crs(4326, 31256, always_xy=True)   # MGI / Austria GK East, wie das Geländemodell der Stadt Wien
r = ET.parse("../dl/karte_1POyNKcbwqhpoS9gAsxzPgN4fyLDRwfQ.kml").getroot()
linien, punkte = {}, {}
for fo in r.iter("{http://www.opengis.net/kml/2.2}Folder"):
    ordner = " ".join(fo.find("k:name", NS).text.split())
    for pm in fo.findall("k:Placemark", NS):
        n = " ".join((pm.find("k:name", NS).text or "").split()); bes = re.sub(r"<br\s*/?>", " ", pm.findtext("k:description", "", NS))
        ls = pm.find(".//k:LineString/k:coordinates", NS); pt = pm.find(".//k:Point/k:coordinates", NS)
        if ls is not None: linien[n] = [(float(c.split(",")[1]), float(c.split(",")[0])) for c in ls.text.split()]
        elif pt is not None: lo, la = map(float, pt.text.strip().split(",")[:2]); punkte.setdefault(ordner, []).append((n, la, lo, " ".join(bes.split())))
pts = linien["Marathon 42,195 km"]
def xy_of(p): return np.array([T.transform(lo, la) for la, lo in p])
def projiziere(xy, dl, la, lo, s_von=0, s_bis=1e9, erwartet=None):
    """Linienmeter des nächsten Punkts der Linie im Fenster [s_von, s_bis]; liegen mehrere Stellen höchstens 15 m neben der
    Marke (Hin- und Rückweg auf derselben Straße: Hauptallee, Schüttelstraße, Ring), gilt die nächste zur erwarteten."""
    p = np.array(T.transform(lo, la)); kand = []
    for i in range(len(xy) - 1):
        if dl[i + 1] < s_von or dl[i] > s_bis: continue
        a_, b_ = xy[i], xy[i + 1]; v = b_ - a_; t = np.clip(np.dot(p - a_, v) / (np.dot(v, v) or 1), 0, 1); q = a_ + t * v
        kand.append((float(np.hypot(*(p - q))), float(dl[i] + t * np.hypot(*v))))
    dmin = min(k[0] for k in kand)
    if erwartet is None: return min(kand)[::-1]
    nah = [k for k in kand if k[0] <= max(15, dmin + 1)]
    best = min(nah, key=lambda k: abs(k[1] - erwartet)); return best[1], best[0]
xy = xy_of(pts); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
km_roh = sorted((int(n.split()[1]), la, lo) for n, la, lo, _ in punkte["Marathon & Powerade Staffelmarathon"] if re.fullmatch(r"km \d+", n))
fak = dl[-1] / 42195
s1 = projiziere(xy, dl, km_roh[0][1], km_roh[0][2], 0, 2000, 1000 * fak)[0]; s2 = projiziere(xy, dl, km_roh[1][1], km_roh[1][2], 1000, 3000, 2000 * fak)[0]
VORLAUF = round((s2 - s1) - s1, 1)
richt = xy[0] - xy[np.searchsorted(dl, 150)]; richt /= np.hypot(*richt)   # Wagramer Straße, gerade
neu0 = xy[0] + VORLAUF * richt
lo0, la0 = Transformer.from_crs(31256, 4326, always_xy=True).transform(*neu0)
print(f"Linie {dl[-1]:.0f} m (GK), km 1 bei {s1:.0f} m, km 2 bei {s2:.0f} m -> Start {VORLAUF} m weiter hinten: {la0:.6f}, {lo0:.6f}")
pts = [(la0, lo0)] + pts
fin = [p for p in punkte["Start | Finish"] if p[0] == "FINISH"][0]
xy = xy_of(pts); dl = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
s_z, e_z = projiziere(xy, dl, fin[1], fin[2], dl[-1] - 300, dl[-1])
print(f"Ziel (FINISH) bei {s_z:.1f} m, {e_z:.1f} m neben der Linie, Linienende {dl[-1]:.1f} m")
_, _, dd = Geod(ellps="GRS80").inv([p[1] for p in pts[:-1]], [p[0] for p in pts[:-1]], [p[1] for p in pts[1:]], [p[0] for p in pts[1:]])
d = [0.0] + np.cumsum(dd).tolist()
json.dump({"pts": [(la, lo, 0.0) for la, lo in pts], "d": d, "vorlauf": VORLAUF}, open("gpx2026.json", "w"))
print(f"geodätisch {d[-1]:.1f} m, {len(pts)} Punkte (GK {dl[-1]:.1f} m)")
fak = dl[-1] / 42195
marken = {"km": [], "punkte": []}
for km, la, lo in km_roh:
    s_, e_ = projiziere(xy, dl, la, lo, (km - 1.5) * 1000 * fak, (km + 1.5) * 1000 * fak, km * 1000 * fak); marken["km"].append([km, s_, round(e_, 1)])
# Verpflegung, Wasserstellen, Gel, Staffelwechsel: Lage aus der Karte, km-Angabe aus der Beschreibung („4,8 km / 29,8 km“: zwei
# Durchgänge an derselben Stelle)
for ordner in ("Streckenbereich - Verpflegungspunkte | Erste Hilfe / Route area - refreshment points | first aid", "Marathon & Powerade Staffelmarathon"):
    for n, la, lo, bes in punkte[ordner]:
        if re.fullmatch(r"km \d+", n) or n.startswith("Rotes Kreuz"): continue
        m = re.match(r"(?:KM\s*)?(\d+(?:,\d+)?)(?:\s*km)?(?:\s*/\s*(\d+(?:,\d+)?)\s*km)?", bes)
        if n.startswith("Powerade Staffelmarathon Ü"): kms = [{"1": 15.5, "2": 23.5, "3": 30.5}[n[26]]]   # km laut Plan („location at K 15,5“)
        elif m: kms = [float(x.replace(",", ".")) for x in m.groups() if x]
        else: continue
        for km in kms:
            s_, e_ = projiziere(xy, dl, la, lo, (km - 1.5) * 1000 * fak, (km + 1.5) * 1000 * fak, km * 1000 * fak)
            marken["punkte"].append([km, s_, round(e_, 1), n, bes.split("Erste*r")[0].strip()])
# Linienmeter wie in gpx2026.json (geodätisch), nicht in GK
for k in marken:
    marken[k] = sorted([[m[0], round(float(np.interp(m[1], dl, d)), 1)] + m[2:] for m in marken[k]])
json.dump(marken, open("marken.json", "w"), ensure_ascii=False, indent=0)
km = marken["km"]
print("Abstand der km-Marken zur Linie: max %.1f m" % max(m[2] for m in km))
print("Linienmeter je km (Marke zu Marke):", [int(round(b[1] - a)) for a, b in zip([0] + [m[1] for m in km], km)], "Rest", round(d[-1] - km[-1][1]))
for m in marken["punkte"]: print(f"  {m[0]:6.2f} km -> Linie {m[1]:7.0f} m ({m[2]:4.1f} m daneben)  {m[3][:45]} | {m[4][:60]}")
