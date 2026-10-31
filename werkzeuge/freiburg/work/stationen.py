# Verpflegung und Wechselstellen: Punkte der RaceDayMap des Veranstalters (rdm_marken.json aus der Karte „2027-marathon“, Ebenen
# „Wasserstation“, „Verpflegungsstation“, „Wechselstelle Schülermarathon“) auf die Runde gelotet, je Runde einmal (der Marathon
# läuft die Runde zweimal). Die Karte „2027“ der Programmseite hat dieselbe Linie, aber andere, offenbar unfertige Punkte (Wasser bei
# km 1,3 / 2,2 / 5,2, eine Verpflegung bei km 7,5): nicht genutzt. Was es gibt, steht in der Starterinformation 2026: „ca. alle 2,5km im
# Wechsel Verpflegungs- und Wasserstellen … An den Verpflegungsstellen (KM 5 | KM 10 | KM 15 | KM 21) werden neben Wasser, Bananen auch
# isotonische Getränke … angeboten. Bei KM 15 gibt es zudem Gele. Bei KM 17,5 gibt es zusätzlich alkoholfreies Bier und Weizen von
# GANTER und Cola.“ Die Verpflegung bei km 21 fehlt in der RaceDayMap; der Streckenplan 2026 zeigt sie neben dem Start am Messplatz
# (Symbol im Plan, Bildpunkt 1950/860 der Anwohnerinformation, über georef.py auf die Linie gelotet).
# Wechselstellen A–F des badenova Schülermarathons (Staffel mit sieben Läufern über die Runde, Start 11:00/11:15 Uhr; Namen laut
# Starterinformation Schülermarathon 2026). Der Marathon kommt an jeder zweimal vorbei.
# -> stationen.json [[Art, Name, Linienmeter in der Runde, Abstand zur Linie]]
import json
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 25832, always_xy=True)
g = json.load(open("runde.json")); d = np.array(g["d"]); Q = np.array(g["pts"])
ss = np.arange(0, d[-1], 2.0); E, N = T.transform(np.interp(ss, d, Q[:, 1]), np.interp(ss, d, Q[:, 0])); baum = cKDTree(np.c_[E, N])
def lot(e, n): dist, i = baum.query([e, n]); return float(ss[i]), float(dist)
WECHSEL = ["Husserlstraße / Wilhelm-von-Möllendorff-Straße", "Unterer Mühlenweg / Gilgenmatten", "Wiehre-Stadion / Wiesentalstraße",
           "Peter-Sprung-Straße / Dreikönigstraße", "Otto-Wels-Straße / Fabrikstraße", "Kreuzstraße / Mathildenstraße"]
out = []
w = []
for art, label, la, lo, _ in json.load(open("rdm_marken.json")):
    s, dist = lot(*T.transform(lo, la))
    if art == "Wechselstelle Schülermarathon": w.append([s, dist])
    else: out.append([{"Wasserstation": "Wasser", "Verpflegungsstation": "Verpflegung"}[art], "", s, round(dist, 1)])
for (s, dist), name, buchst in zip(sorted(w), WECHSEL, "ABCDEF"): out.append(["Wechsel", f"{buchst}|{name}", s, round(dist, 1)])
pk = json.load(open("plan_km.json")); M = np.array(pk["M"])
e, n = np.array([1950.0, 860.0, 1.0]) @ M; s, dist = lot(e, n)
out.append(["Verpflegung", "km 21 (Plan)", s, round(dist, 1)])
out.sort(key=lambda x: x[2])
for x in out: print(x)
json.dump(out, open("stationen.json", "w"), ensure_ascii=False)
