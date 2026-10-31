# Höhen bereinigen -> clean.json {k (offizielle Meter), h, raw, regions}. Grundlage DGM1 Niedersachsen (dgm.py, alle 10 Linienmeter).
# Ein Geländemodell kennt keine Brücken und keine Tunnel:
# - Brücken (OSM bridge=*, strassen.json): Das DGM misst darunter Wasser (Mittellandkanal 50,3 m, Leine, Ihme) oder einen Graben.
#   Dort gilt die Fahrbahn aus dem Oberflächenmodell DOM1 derselben Befliegung (deck.py, 25-%-Quantil 5 × 5 m), wenn das DOM über dem
#   DGM liegt und nicht mehr als 3 m über den Brückenenden (Bäume, Leuchten). Gemessen, nicht geschätzt: zählt nicht zu D.bridges.
#   Arthur-Menge-Ufer (km 1,65), Pasteurallee und Noltemeyerbrücke über den Mittellandkanal (km 18,75 und 19,8), Wilhelmshavener Straße
#   (km 39,9), Königsworther Straße (km 40,4), Brühlstraße (km 41,2); Bernadotteallee (km 24,6, 10 m) hat das DGM mit Fahrbahn.
# - Unterführungen (OSM tunnel=yes): Fernroder Straße unter den Gleisen des Hauptbahnhofs (km 12,1–12,25, 140 m) und Kopernikusstraße
#   unter der Bahn in der Nordstadt (km 36,18–36,24, 70 m). DGM und DOM messen dort das Bahngelände darüber (bis 6 m höher). Gerade
#   zwischen den gemessenen Enden: geschätzt, in D.bridges (schraffiert).
# Danach Kontrolle: keine Stufe über 1,5 m je 10 m mehr (sonst Ausgabe). Muster: werkzeuge/koeln/work/clean.py, honolulu/work/clean.py.
import json
import numpy as np
from common import official
r = json.load(open("dgm2026_10m.json")); st = json.load(open("strassen.json"))
s = np.array([x[0] for x in r]); raw = np.array([x[3] for x in r], float); k = official(s)
h = raw.copy(); regions = []
def gruppen(idx):
    g = []
    for i in idx:
        if g and i - g[-1][-1] <= 3: g[-1].append(i)
        else: g.append([i])
    return g
def ix(lm): return int(round(lm / 10))
# Brückendecks aus dem DOM
deck = {round(a): (q, name) for a, q, _, name in json.load(open("deck.json"))}
for gg in gruppen([i for i, x in enumerate(st) if x[3] not in ("", "no")]):
    a, b = gg[0] - 1, gg[-1] + 1
    ende = max(raw[max(0, a - 2):a + 1].max(), raw[b:b + 3].max())
    n = 0
    for i in range(a, b + 1):
        q = deck.get(round(s[i]), (None,))[0]
        if q is not None and q - raw[i] > 0.3 and q < ende + 3: h[i] = q; n += 1
    print(f"Brücke {st[gg[0]][2]:24s} km {k[gg[0]]/1000:6.2f}–{k[gg[-1]]/1000:6.2f}: {n} Punkte aus dem DOM, "
          f"DGM tiefster {raw[a:b+1].min():5.2f} m, Deck {h[a:b+1].min():5.2f}–{h[a:b+1].max():5.2f} m")
# Unterführungen: Gerade zwischen den Enden
for gg in gruppen([i for i, x in enumerate(st) if x[4] == "yes"]):
    a, b = gg[0] - 1, gg[-1] + 1
    if max(abs(raw[i] - (raw[a] + (raw[b] - raw[a]) * (i - a) / (b - a))) for i in range(a, b + 1)) < 1.0:
        print("Tunnel ohne Buckel:", st[gg[0]][2], k[gg[0]]); continue
    h[a:b + 1] = raw[a] + (raw[b] - raw[a]) * (np.arange(a, b + 1) - a) / (b - a)
    regions.append({"a": float(k[a]), "b": float(k[b]), "kind": "Unterführung", "name": st[gg[0]][2], "ha": float(raw[a]),
                    "hb": float(raw[b]), "extrem": float(raw[a:b + 1].max())})
for o in regions:
    print(f"Unterführung {o['name']:20s} km {o['a']/1000:6.2f}–{o['b']/1000:6.2f} ({o['b']-o['a']:.0f} m): {o['ha']:.2f} -> {o['hb']:.2f} m, "
          f"im Modell bis {o['extrem']:.2f} m")
d = np.diff(h)
for i in np.where(np.abs(d) > 1.5)[0]: print(f"  Stufe bleibt: km {k[i]/1000:.2f} {h[i]:.2f} -> {h[i+1]:.2f}")
print("größte Stufe je 10 m:", round(float(np.abs(d).max()), 2), "m bei km", round(float(k[np.argmax(np.abs(d))]) / 1000, 2))
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions}, open("clean.json", "w"), ensure_ascii=False)
