# Fahrbahn der Brücken aus dem Oberflächenmodell swissSURFACE3D Raster 0,5 m (swisstopo; swissalti.py). Das Geländemodell swissALTI3D
# lässt Brücken weg und misst darunter die Lütschine oder den Bach (bis 12 m tiefer). Kandidaten: OSM-Brücken unter der Linie
# (strassen.json), Senken über 0,8 m unter der Geraden über ±40 m und Stellen, an denen die Höhen der Linie des Veranstalters
# („3D_DRAPED“, sie führen über die Brücken) mehr als 1,0 m über dem Geländemodell liegen; je 40 m Rand. Kein Kriterium „Sprung je 10 m“
# wie in Luzern: am Berg steigt die Strecke bis 3 m je 10 m. Je 10-m-Punkt das 25-%-Quantil von 5 × 5 Werten im Abstand 1 m (Muster:
# werkzeuge/luzern/work/deck.py). -> deck.json {"i": [Index im 10-m-Raster], "deck": [Höhe], "mitte": [Wert in der Mitte], "gpx": [...], "gel": [...]}
import json
import numpy as np
from swissalti import Modell
from common import official
v = json.load(open("dgm_vergleich.json")); E = np.array(v["E"]); N = np.array(v["N"]); h = np.array(v["gel05"]); g = np.array(v["gpx"])
st = json.load(open("strassen.json")); k = official(np.array(v["s"]))
kand = np.zeros(len(h), bool)
kand[:len(st)] |= np.array([o[3] not in ("", "no") for o in st])[:len(h)]
ger = np.array([np.interp(i, [i - 4, i + 4], [h[i - 4], h[i + 4]]) if 4 <= i < len(h) - 4 else h[i] for i in range(len(h))])
kand |= ger - h > 0.8
kand |= g - h > 1.0
idx = np.where(kand)[0]; rand = set()
for i in idx: rand.update(range(max(0, i - 4), min(len(h), i + 5)))
idx = np.array(sorted(rand))
ober = Modell("swisssurface3d-raster", 0.5)
off = np.array([(a, b) for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)], float)
O = ober.lv95((E[idx, None] + off[:, 0]).ravel(), (N[idx, None] + off[:, 1]).ravel()).reshape(len(idx), len(off))
deck = np.nanpercentile(O, 25, axis=1); mitte = O[:, 12]
json.dump({"i": idx.tolist(), "deck": np.round(deck, 3).tolist(), "mitte": np.round(mitte, 3).tolist(), "gpx": g[idx].round(2).tolist(),
           "gel": h[idx].round(3).tolist(), "kacheln": ober.kacheln_info()}, open("deck.json", "w"))
print(len(idx), "Punkte,", len(ober.kacheln_info()), "Kacheln", {x["jahr"] for x in ober.kacheln_info().values()})
