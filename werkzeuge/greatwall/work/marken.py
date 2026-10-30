# Bezugspunkte für die Kilometer -> marken.json: Stelle auf der Linie (m) und Kilometer des Veranstalters.
# Quellen: Kilometerschilder der Karte (weiße gestrichelte Linie vom Schild zur Strecke; schwarz = Marathon, schwarz-rot = Marathon
# und Halbmarathon: km 4, 10, 15, 21, 27, 32, 38), Getränkestellen der Karte (blaue Linie vom Symbol zur Strecke) mit den Kilometern
# der Höhenkurve des Veranstalters (Nummer und km über der Kurve; die Stellen 1–7 liegen auf Hin- und Rückweg), Tor zur Mauer
# (Ausschnitt Start/Ziel: „35 KM“, „Marathon 6 hour cut off“ an Tempel 1) und „42 KM“ (Ausschnitt, Talstraße vor dem Platz).
# Je Bezugspunkt alle Durchgänge der Linie in der Nähe (bis 80 m, auf der Mauer 150 m: dort ist die Strecke neben das Mauersymbol
# gezeichnet); gewählt wird der Durchgang, der nach der Länge der Linie am besten zum Kilometer passt.
import json
import numpy as np
from geo import gleich, laenge
P = json.load(open("plan2026.json")); M = np.array(json.load(open("georef.json"))["M"])
L = json.load(open("linie.json")); X = np.c_[L["x"], L["y"]]; D = np.array(L["d"]); GL = D[-1]
G, Gd = gleich(X, 5.0)
def ab(p): return np.asarray(p, float) @ M[:2] + M[2]
def durchgaenge(xy, R):
    dist = np.hypot(*(G - xy).T); out = []; i = 0
    while i < len(G):
        if dist[i] < R:
            j = i
            while j + 1 < len(G) and dist[j + 1] < R: j += 1
            k = i + int(np.argmin(dist[i:j + 1])); out.append((float(Gd[k]), float(dist[k]))); i = j + 1
        else: i += 1
    return out
REF = []
def bezug(km, xy, was, R=80):
    c = durchgaenge(xy, R)
    if not c: print("  kein Durchgang:", was, km); return
    soll = km * 1000 * GL / 42195
    d, abst = min(c, key=lambda t: abs(t[0] - soll))
    REF.append({"km": km, "d": round(d, 1), "abstand": round(abst, 1), "was": was, "durchgaenge": len(c)})
# Kilometerschilder des Marathons (14 und 20 sind nur Halbmarathon)
for k in P["km"]:
    if k["km"] in (14, 20): continue
    bezug(k["km"], ab(k["pt"]), "Kilometerschild")
# Getränkestellen: Kartenstelle -> Nummer nach Lage (Inhalt und Reihenfolge wie in der Höhenkurve), km aus der Höhenkurve
STELLEN = {1: (2.6, 39.6), 2: (5.1, 37.1), 3: (5.5, 36.7), 4: (6.1, 36.1), 5: (6.4, 35.8), 6: (8.1, 34.9), 7: (11.5, 31.5),
           8: (14.2,), 9: (16.6,), 10: (19.5,), 11: (22.7,), 12: (25.3,), 13: (26.9,), 14: (28.9,)}
# Zuordnung der Kartensymbole (Stelle der blauen Linie an der Strecke, pt) zu den Nummern der Höhenkurve
KARTE = {1: (303.2, 172.4), 2: (371.0, 54.7), 3: (363.6, 35.7), 4: (309.6, 18.1), 5: (284.1, 32.2), 6: (226.1, 74.9), 7: (245.7, 440.9),
         8: (192.3, 657.5), 9: (255.9, 766.5), 10: (443.7, 800.3), 11: (510.6, 592.0), 12: (334.7, 561.0), 13: (446.2, 515.6),
         14: (326.2, 521.2)}
for nr, kms in STELLEN.items():
    if nr == 6: continue
    xy = ab(KARTE[nr]); R = 150 if nr in (3, 4, 5) else 80
    for km in kms: bezug(km, xy, f"Getränke {nr}", R)
# Getränke 6 steht am Ostrand des Platzes an der Talstraße (Symbol der Karte und des Ausschnitts): dort, wo die Linie den Platz
# verlässt (km 8,1) bzw. betritt (km 34,9). Die Linie der Karte läuft über den Platz mehrfach durch dieselbe Stelle.
T = L["teil"]
i_aus = max(i for i, t in enumerate(T) if t == "Platz zur Straße"); i_ein = min(i for i, t in enumerate(T) if t == "Platz zum Tor") - 1
REF.append({"km": 8.1, "d": round(float(D[i_aus]), 1), "abstand": 0.0, "was": "Getränke 6", "durchgaenge": 1})
REF.append({"km": 34.9, "d": round(float(D[i_ein]), 1), "abstand": 0.0, "was": "Getränke 6", "durchgaenge": 1})
# Tor zur Mauer (km 35): Knoten auf der Nordmauer, zweiter Durchgang
i_tor = [i for i, t in enumerate(L["teil"]) if t == "Nordmauer zu Tower 6"][0] - 1
REF.append({"km": 35.0, "d": round(float(D[i_tor]), 1), "abstand": 0.0, "was": "Tor (Cut-off)", "durchgaenge": 2})
json.dump({"linie_m": GL, "ref": sorted(REF, key=lambda r: r["d"])}, open("marken.json", "w"), ensure_ascii=False, indent=0)
print(f"Linie {GL:.0f} m, Faktor 42195/Linie = {42195 / GL:.4f}")
for r in sorted(REF, key=lambda r: r["d"]):
    print(f"  km {r['km']:5.1f}  Linie {r['d'] / 1000:6.2f} km  ·Faktor {r['d'] * 42195 / GL / 1000:6.2f}  Abweichung {r['d'] * 42195 / GL / 1000 - r['km']:+5.2f}  "
          f"(Abstand {r['abstand']:.0f} m, {r['durchgaenge']} Durchgänge) {r['was']}")
