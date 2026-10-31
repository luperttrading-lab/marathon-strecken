# Höhenprofil für die App -> clean.json. Grundlage: swissALTI3D 0,5 m (dgm.py, dgm_vergleich.json „gel05“), an den Brücken die Fahrbahn
# aus swissSURFACE3D (deck.py, deck.json).
# Brücken: Das Geländemodell lässt Brücken weg. Wo es unter die Umgebung fällt (Wasser unter 406,6 m: Quaibrücke fünfmal, Schanzengraben
# an Dreikönigbrücke und General-Guisan-Quai je zweimal; oder mehr als 0,8 m unter dem Median der 60 m um die Stelle: Seestrasse über
# den Dorfbach und den Heslibach in Küsnacht), gilt die Fahrbahn aus dem Oberflächenmodell (25-%-Quantil, gemessen, nicht
# schraffiert), je 10 m Rand. Wo das Oberflächenmodell über der Linie eine andere Brücke zeigt (Dufourstrasse über die
# Bellerivestrasse bei km 11,36 und 33,08), fällt das Geländemodell nicht ab und bleibt.
# Keine weitere Glättung: Das Laser-Modell misst die Fahrbahn auf Zentimeter; build.py nimmt den Median über 30 m.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
raw = np.array(v["gel05"], float); h = raw.copy()
dj = json.load(open("deck.json")); deck = np.full(len(h), np.nan); deck[dj["i"]] = dj["deck"]
st = json.load(open("strassen.json"))
def street(i): return st[min(len(st) - 1, i)][1] or ""
umg = np.array([np.median(np.r_[raw[max(0, i - 3):i], raw[i + 1:i + 4]]) for i in range(len(raw))])
dip = (raw < 406.6) | (raw < umg - 0.8)
idx = np.where(dip)[0]
regions = []
for g in (np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []):
    a, b = max(0, g.min() - 1), min(len(h) - 1, g.max() + 1)
    seg = deck[a:b + 1]
    if np.isnan(seg).any(): raise SystemExit(f"Oberflächenmodell fehlt bei km {k[a] / 1000:.3f}")
    h[a:b + 1] = seg
    regions.append({"a": float(k[a]), "b": float(k[b]), "name": street(int(np.median(g))), "gelaende": float(raw[g].min()),
                    "fahrbahn": [float(seg.min()), float(seg.max())]})
    print(f"  Fahrbahn aus swissSURFACE3D km {k[a] / 1000:6.3f}–{k[b] / 1000:6.3f} ({(b - a) * 10:3d} m) {street(int(np.median(g))):22s}: "
          f"Gelände {raw[g].min():.2f}, Fahrbahn {seg.min():.2f}–{seg.max():.2f} m")
d_ = np.abs(np.diff(h)); print(f"  Stufen über 1,5 m je 10 m: {(d_ > 1.5).sum()}, größte {d_.max():.2f} m bei km {k[np.argmax(d_)] / 1000:.2f}")
g = np.array(v["gpx"]); print(f"  GPX-Höhen minus bereinigt: Median {np.median(g - h):+.2f} m, 95 % zwischen {np.percentile(g - h, 2.5):+.2f} und {np.percentile(g - h, 97.5):+.2f} m, "
                              f"größte {np.abs(g - h).max():.2f} m bei km {k[np.argmax(np.abs(g - h))] / 1000:.2f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions, "quelle": "swissALTI3D 0,5 m + swissSURFACE3D an Brücken"},
          open("clean.json", "w"), ensure_ascii=False)
