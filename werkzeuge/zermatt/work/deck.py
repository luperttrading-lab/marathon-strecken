# Fahrbahn der Brücken aus dem Oberflächenmodell swissSURFACE3D Raster 0,5 m (swisstopo; swissalti.py). Das Geländemodell swissALTI3D
# lässt Brücken weg und misst darunter das Bachbett (Vispa, Seitenbäche) oder die Bahn. Stellen: OSM-Brücken unter der Linie
# (strassen.json) und Senken, in denen das Geländemodell mehr als 0,8 m unter der Geraden zwischen den Punkten 60 m davor und danach liegt
# (am Hang statt des Medians wie in Luzern: Bergwege steigen bis 30 %), je 40 m Rand. Je 10-m-Punkt das 25-%-Quantil von 5 × 5 Werten im
# Abstand 1 m (darunter Wasser oder Böschung neben der Fahrbahn, darüber Geländer, Fahrzeuge; Muster: werkzeuge/luzern/work/deck.py).
# -> deck.json {"i": [Index im 10-m-Raster], "deck": [Höhe], "mitte": [Wert in der Mitte], "gpx": [...], "gel": [...]}
import json
import numpy as np
from swissalti import Modell
from common import official
v = json.load(open("dgm_vergleich.json")); E = np.array(v["E"]); N = np.array(v["N"]); h = np.array(v["gel05"]); g = np.array(v["gpx"])
st = json.load(open("strassen.json")); k = official(np.array(v["s"]))
kand = np.zeros(len(h), bool)
kand[:len(st)] |= np.array([o[3] not in ("", "no") for o in st])[:len(h)]
idx_ = np.arange(len(h)); a_ = np.clip(idx_ - 6, 0, len(h) - 1); b_ = np.clip(idx_ + 6, 0, len(h) - 1)
sehne = np.where(b_ > a_, h[a_] + (h[b_] - h[a_]) * (idx_ - a_) / np.maximum(b_ - a_, 1), h)
kand |= h < sehne - 0.8
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
for gr in np.split(np.arange(len(idx)), np.where(np.diff(idx) > 1)[0] + 1):
    a, b = idx[gr[0]], idx[gr[-1]]
    print(f"km {k[a] / 1000:6.3f}–{k[b] / 1000:6.3f} {st[min(a + 4, len(st) - 1)][1]}")
    for j in gr:
        i = idx[j]; print(f"   {i * 10:6d} km {k[i] / 1000:6.3f}  Gelände {h[i]:7.2f}  Oberfläche 25 % {deck[j]:7.2f} (Mitte {mitte[j]:7.2f})  GPX {g[i]:7.2f}"
                          f"{'  OSM-Brücke' if i < len(st) and st[i][3] not in ('', 'no') else ''}")
