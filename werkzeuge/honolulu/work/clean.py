# Höhenprofil für die App -> clean.json. Grundlage: USGS-3DEP-Bodenmodell 1 m (dgm.py, dgm_vergleich.json „lidar“), dazu die
# Fahrbahnhöhen aus der Punktwolke an den Brücken (deck.py, deck.json).
# 1. Brücken, die das Modell weglässt: Wo auf einer OSM-Brücke (strassen.json) die Fahrbahn aus der Punktwolke mehr als 0,5 m über dem
#    Modell liegt, gilt die Fahrbahn (gemessen, nicht schraffiert). Das betrifft nur die Kalākaua Avenue über den Ala-Wai-Kanal
#    (km 7,24–7,28: Modell 0,6 m = Wasserfläche, Fahrbahn 3,2–3,9 m). Die übrigen kleinen Brücken über Bäche und Kanäle hat das Modell
#    als Durchlass mit Fahrbahn drin (Punktwolke und Modell auf 10 cm gleich).
# 2. Lücken: An vier Stellen in Hawaiʻi Kai hat das Modell keinen Wert (Wasserflächen unter Kalanianaʻole Highway, Hawaiʻi Kai Drive
#    und Keahole Street, 20–40 m), und auch die Punktwolke hat dort im Umkreis von 10 m keine Punkte. Wo die Punktwolke einen Wert hat,
#    gilt er; sonst gerade zwischen den gemessenen Enden (Enden höchstens 0,2 m verschieden). Diese Stücke gelten als geschätzt
#    (schraffiert, regions).
# Keine weitere Glättung: Das Laser-Modell misst die Fahrbahn auf Zentimeter; build.py nimmt den Median über 30 m.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
raw = np.array(v["lidar"], float); h = raw.copy()
dj = json.load(open("deck.json")); deck = np.array([np.nan if x is None else x for x in dj["deck"]])
st = json.load(open("strassen.json"))
n = min(len(h), len(st)); br = np.zeros(len(h), bool); br[:n] = [o[3] not in ("", "no") for o in st[:n]]
def street(i): return st[min(len(st) - 1, i)][2] or ""
def gruppen(m, luecke):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > luecke)[0] + 1) if len(idx) else []
# 1. Fahrbahn statt Wasser
gemessen = br & np.isfinite(deck) & (np.isnan(raw) | (deck - raw > 0.5))
for g in gruppen(gemessen & np.isfinite(raw), 2):
    a, b = g.min(), g.max()
    print(f"  Fahrbahn aus der Punktwolke km {k[a] / 1000:6.3f}–{k[b] / 1000:6.3f} {street(a)}: Modell {raw[a:b + 1].min():.2f}–{raw[a:b + 1].max():.2f} m, "
          f"Fahrbahn {deck[a:b + 1].min():.2f}–{deck[a:b + 1].max():.2f} m")
h[gemessen] = deck[gemessen]
# 2. Lücken
regions = []
for g in gruppen(np.isnan(h), 1):
    a, b = int(g.min()) - 1, int(g.max()) + 1
    h[a:b + 1] = np.interp(np.arange(a, b + 1), [a, b], [h[a], h[b]])
    nm = street(int(np.median(g)))
    regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Brücke", "name": nm, "ha": float(h[a]), "hb": float(h[b])})
    print(f"  Lücke km {k[a] / 1000:6.3f}–{k[b] / 1000:6.3f} ({(b - a) * 10} m) {nm}: gerade {h[a]:.2f} -> {h[b]:.2f} m")
d_ = np.abs(np.diff(h)); print(f"  Stufen über 1,5 m je 10 m: {(d_ > 1.5).sum()}, größte {d_.max():.2f} m bei km {k[np.argmax(d_)] / 1000:.2f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": np.where(np.isnan(raw), h, raw).tolist(), "regions": regions, "quelle": "lidar"},
          open("clean.json", "w"), ensure_ascii=False)
