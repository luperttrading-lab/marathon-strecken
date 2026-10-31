# Höhen bereinigen -> clean.json {k (offizielle Meter), h, raw, regions}. Grundlage: Laser-Geländemodell des BEV (dgm.py, alle 10 Linienmeter).
# Ein Geländemodell kennt keine Brücken: Auf den beiden Murbrücken (Alfred-Stingl-Brücke, bis Februar 2026 Augartenbrücke, und
# Keplerbrücke) misst es den Fluss bis 10 m tiefer, auf den kurzen Brücken der Grabenstraße und der Weinzöttlstraße über Bäche bis 5 m.
# Dort gilt die Fahrbahn aus dem Oberflächenmodell des BEV (deck.py, ALS DSM derselben Befliegung, 25-%-Quantil im Umkreis von 2 m), wenn
# sie über dem Geländemodell und nicht mehr als 3 m über den Brückenenden liegt (sonst Bäume, Leuchten, Oberleitungen); einzelne Spitzen
# werden auf den höheren Nachbarn gekappt, und die Fahrbahn bleibt nicht unter der Geraden zwischen den Enden (wo die Linie am Rand des
# Decks liegt). Gemessen, nicht geschätzt. Geprüft wird je OSM-Brücke mit zwei Punkten (20 m) Rand, weil die Senke im Geländemodell
# breiter ist als der OSM-Weg (Grabenstraße auf dem Rückweg).
# Danach drei Senken gerade gezogen (GERADE, unten), eine davon als geschätzte Brücke gezeigt. Kontrolle: Stufen über 1,5 m je 10 m.
# Runde 2 übernimmt die bereinigten Höhen von Runde 1 an derselben Stelle der Runde (Muster: werkzeuge/freiburg/work/clean.py).
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
deck = {round(a): (q, name) for a, q, _, name in json.load(open("deck.json"))}
S0_DAB = json.load(open("strecke2026.json"))["d"][json.load(open("strecke2026.json"))["abzweig"]]
for gg in gruppen([i for i, x in enumerate(st) if x[3] not in ("", "no")]):
    a, b = gg[0] - 2, gg[-1] + 2
    ende = max(raw[max(0, a - 2):a + 1].max(), raw[b:b + 3].max())
    n = 0
    for i in range(a, b + 1):
        q = deck.get(round(s[i]), (None,))[0]
        if q is not None and q - raw[i] > 0.3 and q < ende + 3: h[i] = q; n += 1
    for i in range(a + 1, b): h[i] = min(h[i], max(h[i - 1], h[i + 1]))   # einzelne Spitzen (Leuchte, Fahrzeug) abschneiden
    gerade = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
    m = h[a:b + 1] < gerade - 0.3; h[a:b + 1] = np.maximum(h[a:b + 1], gerade)
    print(f"Brücke {st[gg[0]][2] or '(ohne Namen)':24s} km {k[gg[0]]/1000:6.2f}–{k[gg[-1]]/1000:6.2f}: {n} Punkte aus dem DSM, {int(m.sum())} auf die Gerade, "
          f"DTM tiefster {raw[a:b+1].min():6.2f} m, Fahrbahn {h[a:b+1].min():6.2f}–{h[a:b+1].max():6.2f} m, Enden {h[a]:.2f} / {h[b]:.2f}")
# Drei Stellen, an denen das Geländemodell nach den Brücken noch eine Senke über 1,5 m je 10 m zeigt (Runde 1; Runde 2 übernimmt sie):
# - Grieskai am Kopf der Tegetthoffbrücke (km 6,35): ein Punkt 5 m tief, wo die Brücke samt Widerlager aus dem Modell genommen ist; die
#   Straße läuft eben durch (davor und danach 349,1–349,4 m). Gerade, nicht gezeigt.
# - Grabenstraße über dem Schöcklbach (km 11,89, Bach in OSM verdolt, tunnel=yes): ein Punkt 2,3 m tief. Gerade, nicht gezeigt.
# - Grabenstraße auf dem Rückweg (km 15,95–15,99): Die stadteinwärts führende Fahrbahn ist eine Brücke über den Straßenbahntunnel
#   (OSM layer 2), die Linie liegt 11 m neben dem OSM-Weg, das Modell misst bis 5 m tiefer, das Oberflächenmodell ebenso (Rand des
#   Decks). Gerade zwischen den Rampen (358,5 → 358,7 m; die Fahrbahn stadtauswärts misst das Oberflächenmodell mit 358,8–359,0 m):
#   geschätzt, schraffiert.
GERADE = [(6300, 6400, None), (11860, 11910, None), (15930, 16000, "Grabenstraße")]
for ka, kb, name in GERADE:
    sel = np.where((k >= ka) & (k <= kb) & (s <= S0_DAB))[0]
    # gute Enden: letzter Punkt vor und erster nach der Senke, der höchstens 0,5 m von seinem äußeren Nachbarn abweicht
    tief = sel[np.argmin(h[sel])]
    a = tief - 1
    while a > sel[0] and abs(h[a] - h[a - 1]) > 0.5: a -= 1
    b = tief + 1
    while b < sel[-1] and abs(h[b] - h[b + 1]) > 0.5: b += 1
    vorher = h[a:b + 1].copy(); h[a:b + 1] = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / (b - a)
    print(f"Gerade km {k[a]/1000:.3f}–{k[b]/1000:.3f}: {h[a]:.2f} -> {h[b]:.2f} m, Modell bis {vorher.min():.2f} m" + (f" ({name}, geschätzt)" if name else ""))
    if name:
        R2_ = json.load(open("strecke2026.json"))["runde2"]
        for plus in (0.0, R2_):   # dieselbe Stelle in Runde 2 (Linienmeter + Beginn der Runde 2)
            regions.append({"a": float(official(s[a] + plus)), "b": float(official(s[b] + plus)), "kind": "Brücke", "name": name,
                            "ha": float(h[a]), "hb": float(h[b]), "extrem": float(vorher.min())})
# Runde 2 ist dieselbe Strecke: Höhen aus Runde 1 an derselben Stelle der Runde. Die letzten Meter (Übergang am Start) bleiben gemessen.
S = json.load(open("strecke2026.json")); r2 = S["runde2"]; dab = S["d"][S["abzweig"]]
l1 = s <= dab; l2 = (s >= r2) & (s - r2 <= dab)
neu2 = np.interp(s[l2] - r2, s[l1], h[l1])
print(f"Runde 2 aus Runde 1: {int(l2.sum())} Punkte, Unterschied zur eigenen Messung bis {np.abs(neu2 - h[l2]).max():.2f} m, "
      f"im Mittel {np.abs(neu2 - h[l2]).mean():.3f} m; größte Unterschiede bei km",
      [round(float(k[l2][j]) / 1000, 2) for j in np.argsort(-np.abs(neu2 - h[l2]))[:5]])
h[l2] = neu2
# verbliebene Stufen
d = np.diff(h); stufen = np.where(np.abs(d) > 1.5)[0]
for i in stufen: print(f"  Stufe bleibt: km {k[i]/1000:.2f} {h[i]:.2f} -> {h[i+1]:.2f} ({st[min(len(st)-1, int(round(s[i]/10)))][2]})")
print("größte Stufe je 10 m:", round(float(np.abs(d).max()), 2), "m bei km", round(float(k[np.argmax(np.abs(d))]) / 1000, 2))
for o_ in regions: print(f"geschätzt: {o_['name']} km {o_['a']/1000:.3f}–{o_['b']/1000:.3f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": regions}, open("clean.json", "w"), ensure_ascii=False)
