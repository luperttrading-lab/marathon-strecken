# Labestationen und Staffelübergaben.
# Quelle der Labestationen: Übersichtsgrafik „Auf einen Blick – der Graz-Marathon“ (Kleine Zeitung/MJK) auf der Seite „Labestationen“
# des Veranstalters (https://www.grazmarathon.at/laeuferinformation/serviceleistungen/labestationen/, Bild
# 2025-10-10-GM-Hoehenprofil-1.jpg, hochgeladen im Oktober 2025 und zum Lauf 2026 unverändert auf der Seite): neun Labestationen auf
# einer Kilometerskala, je Station, was es gibt (Wasser, Peeroton, Cola, Bananen, Erste Hilfe, Eigenverpflegung, Gel), dazu die
# „Hotspots“ (Wende Süd, Styria Tower, Kunsthaus, Wiener Straße, Keplerbrücke, Maut Andritz, Wende Nord, Schloßbergplatz, Neutorgasse,
# Hauptplatz, Eisernes Tor) und die drei Staffelübergaben. Die Grafik ist schematisch (dieselben Orte liegen in den zwei Runden bis
# 0,4 km verschieden weit vom Start); die Stationen werden deshalb zwischen den beiden nächsten Hotspots, deren Lage auf der Linie
# feststeht, linear eingehängt (Pixel der Grafik -> Linienmeter). Genauigkeit etwa ±0,2 km.
# Text der Seite „Labestationen“: „Peeroton Gel nur auf der Labestation auf Kilometer 35!!“ (die Grafik zeigt Gel auch bei km 13);
# Eigenverpflegung nur für Marathonläufer an „Labestation 2 & 8: Keplerstraße (ca. KM 10 und KM 31)“ und „Labestation 6: Radetzkystr. Höhe
# Pestalozzistr. – Marathon auf zweiter Runde (ca. KM 22)“ (die Grafik zeigt Eigenverpflegung an der 2., 5. und 7. ihrer neun
# Stationen; die Nummern des Textes passen nicht zu ihr).
# Staffelübergaben laut Seite „Staffelmarathon“: Körösistraße Ecke Wickenburggasse (ca. 10 km und 31,1 km), Schlossberghotel (19,1 km;
# Grafik „19,3 km Schloßbergplatz“).
# -> stationen.json [[Art, Kurzname, Linienmeter der Marathonlinie, Text]]
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
from common import official
from nominatim import ort
T = Transformer.from_crs(4326, 25833, always_xy=True)
S = json.load(open("strecke2026.json")); d = np.array(S["d"]); Q = np.array(S["pts"]); R2 = S["runde2"]; DAB = S["d"][S["abzweig"]]
st = json.load(open("strassen.json"))
ss = np.arange(0, d[-1], 2.0); E, N = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); baum = cKDTree(np.c_[E, N])
def strasse_lm(nm, welche=0):
    """Mitte der Brücke/Straße nm in Runde 1 (welche=0) bzw. 2 (1)."""
    x = [o[0] for o in st if o[2] == nm]; r1 = [v for v in x if v <= DAB]; r2 = [v for v in x if v >= R2]
    v = (r1, r2)[welche]; return (min(v) + max(v)) / 2
# Hotspots (Pixel der Grafik, Originalgröße 2347 px, gemessen in der Zeile „Erste Hilfe“ bzw. an den roten Linien; Anzeige 2000 px breit,
# hier in Anzeigepixeln) und ihre Lage auf der Linie.
la_ = np.interp(ss, d, Q[:, 0])
ws = [float(ss[np.argmin(np.where(ss <= DAB, la_, 99))]), float(ss[np.argmin(np.where(ss >= R2, la_, 99))])]
wn = [float(ss[np.argmax(np.where(ss <= DAB, la_, -99))]), float(ss[np.argmax(np.where(ss >= R2, la_, -99))])]
def nah(q, a, b):
    """nächste Stelle der Linie zum Ort q (lat, lon) zwischen den Linienmetern a und b"""
    e, n = T.transform(q[1], q[0]); m = (ss >= a) & (ss <= b); i = np.where(m)[0][np.argmin(np.hypot(E[m] - e, N[m] - n))]
    return float(ss[i])
STY, KUN, MAU, SCH, HAU, EIS = (ort(x)[:2] for x in ("Styria Media Center, Graz", "Kunsthaus Graz", "Andritzer Maut, Graz", "Schloßbergplatz, Graz",
                                                     "Hauptplatz, Graz", "Am Eisernen Tor, Graz"))
L = float(d[-1])
anker = [(160.2, 0.0),
         (276.9, ws[0]), (340.9, nah(STY, ws[0], wn[0])), (449.9, nah(KUN, ws[0], wn[0])), (578.0, strasse_lm("Keplerbrücke", 0)),
         (680.0, nah(MAU, ws[0], wn[0])), (781.4, wn[0]), (869.2, nah(MAU, wn[0], DAB)), (990.2, nah(SCH, wn[0], DAB)),
         (1033.7, nah(HAU, wn[0] + 4000, DAB)), (1051.6, nah(EIS, wn[0] + 5000, DAB)),
         (1165.7, ws[1]), (1233.1, nah(STY, ws[1], wn[1])), (1366.0, nah(KUN, ws[1], wn[1])), (1485.0, strasse_lm("Keplerbrücke", 1)),
         (1569.7, nah(MAU, ws[1], wn[1])), (1670.2, wn[1]), (1767.4, nah(MAU, wn[1], L)), (1890.1, nah(SCH, wn[1], L)),
         (1934.4, nah(HAU, wn[1] + 4000, L)), (1952.3, nah(EIS, wn[1] + 5000, L)), (1961.7, L)]
ax = np.array([a for a, _ in anker]); al = np.array([b for _, b in anker])
assert np.all(np.diff(al) > 0), anker
def px2lm(x): return float(np.interp(x, ax, al))
print("Anker (Pixel -> km):", [(a, round(float(official(b)) / 1000, 2)) for a, b in anker])
W, P, C, B, EV, GEL = "Wasser", "Peeroton Mineralvitamindrink", "Cola", "Bananen", "Eigenverpflegung", "Peeroton Gel"
LABE = [(340.9, [W, P]), (570.1, [W, P, C, B, EV]), (716.7, [W, P, C, B, GEL]), (920.3, [W, P, C, B]), (1083.1, [W, P, B, EV]),
        (1233.1, [W, P]), (1475.9, [W, P, C, B, EV]), (1617.4, [W, P, C, B, GEL]), (1818.5, [W, P, C, B])]
# Dieselbe Station liegt in beiden Runden an derselben Stelle: Paare (1, 6), (2, 7), (3, 8), (4, 9) auf die mittlere Lage in der Runde
# gesetzt (die Grafik zeigt sie bis 0,26 km verschieden, Station 3/8 bei Andritz); Station 5 gibt es nur in Runde 2.
lm = [px2lm(x) for x, _ in LABE]
for a, b in ((0, 5), (1, 6), (2, 7), (3, 8)):
    m = (lm[a] + (lm[b] - R2)) / 2; print(f"Station {a + 1}/{b + 1}: Runde {float(official(lm[a])) / 1000:.2f} / {float(official(lm[b] - R2)) / 1000:.2f} km -> {float(official(m)) / 1000:.2f}")
    lm[a], lm[b] = m, m + R2
out = []
for n, ((x, was), l) in enumerate(zip(LABE, lm), 1):
    out.append(["Labe", str(n), l, was])
# Staffelübergaben: Ecke Körösistraße/Wickenburggasse = Anfang der Körösistraße nach der Keplerbrücke (Runde 1 und 2), Schlossberghotel
ue1 = [o[0] for o in st if o[2] == "Körösistraße"]; k1 = min(v for v in ue1 if v <= DAB); k3 = min(v for v in ue1 if v >= R2)
sh = nah(ort("Schlossberghotel, Graz")[:2], wn[0], DAB)
out += [["Wechsel", "1", k1, "Körösistraße Ecke Wickenburggasse"], ["Wechsel", "2", sh, "Schlossberghotel (Kaiser-Franz-Josef-Kai)"],
        ["Wechsel", "3", k3, "Körösistraße Ecke Wickenburggasse"]]
out.sort(key=lambda o: o[2])
for o in out: print(f"{o[0]:8s} {o[1]:2s} km {float(official(o[2])) / 1000:6.2f}  {o[3]}")
json.dump(out, open("stationen.json", "w"), ensure_ascii=False)
