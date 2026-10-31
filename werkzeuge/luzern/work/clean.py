# Höhenprofil für die App -> clean.json. Grundlage: swissALTI3D 0,5 m (dgm.py, dgm_vergleich.json „gel05“).
# 1. Überdeckte Stücke (bedeckt.py: OSM tunnel=* oder covered=yes unter der Linie), in denen das Geländemodell mehr als 1,5 m über der
#    Höhe der GPX-Datei liegt: Es misst dort die Decke, nicht die Fahrbahn. Geschätzt als Gerade zwischen den Portalen (bis das Modell
#    wieder auf 0,5 m bei der GPX-Höhe liegt), schraffiert in der App (D.bridges): Seestrasse in Hergiswil unter der A2 (zweimal hin und
#    zurück) und der Tunnel der Hergiswilerstrasse beim Kreisel Schlüssel (nur auf dem Rückweg; hin läuft die Strecke auf dem Veloweg
#    darüber). Unterführungen unter Brücken (Langensandbrücke, Velotunnel in Tribschen) misst das Modell richtig: Brücke weg, Boden sichtbar.
# 2. Brücken: Das Geländemodell lässt Brücken weg und misst darunter den See (433,6 m), den Bach oder die Bahn. Kandidaten (deck.py) sind
#    Stellen, an denen das Oberflächenmodell mehr als 0,5 m über dem Geländemodell liegt, Punkte unter 434,2 m und Senken über 0,8 m unter
#    dem Median der 120 m um die Stelle. Ersetzt wird nur, wo das Geländemodell zwischen den Rändern des Stücks mehr als 0,5 m unter der
#    Geraden liegt (sonst führt eine Brücke ÜBER die Strecke, etwa die A2 in Hergiswil oder die A8 in Alpnachstad). Ist das
#    Oberflächenmodell dort glatt (Mitte und 25-%-Quantil auf 0,6 m gleich), gilt seine Fahrbahn (gemessen); sonst stehen Bäume darüber,
#    und das Stück wird als Gerade geschätzt, wenn das Modell mehr als 1,5 m darunter fällt (St. Niklausenstrasse km 6,55).
# Keine weitere Glättung: build.py nimmt den Median über 30 m.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
raw = np.array(v["gel05"], float); gpx = np.array(v["gpx"]); h = raw.copy()
dj = json.load(open("deck.json")); deck = np.full(len(h), np.nan); mitte = np.full(len(h), np.nan)
deck[dj["i"]] = dj["deck"]; mitte[dj["i"]] = dj["mitte"]
st = json.load(open("strassen.json"))
def street(i): return st[min(len(st) - 1, i)][1] or ""
bed = np.zeros(len(h), bool)
for s_, _, _ in json.load(open("bedeckt.json")): bed[int(round(s_ / 10))] = True
bed2 = bed.copy(); bed2[1:] |= bed[:-1]; bed2[:-1] |= bed[1:]
regions = []
def gruppen(m):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []
# 1. überdeckte Stücke
geschaetzt = np.zeros(len(h), bool)
for g in gruppen(bed2 & (raw - gpx > 1.5)):
    a, b = g.min(), g.max()
    for _ in range(5):
        if a > 0 and raw[a - 1] - gpx[a - 1] > 0.5: a -= 1
    for _ in range(5):
        if b < len(h) - 1 and raw[b + 1] - gpx[b + 1] > 0.5: b += 1
    a0, b0 = a - 1, b + 1
    h[a0:b0 + 1] = np.interp(np.arange(a0, b0 + 1), [a0, b0], [raw[a0], raw[b0]]); geschaetzt[a0:b0 + 1] = True
    regions.append({"a": float(k[a0]), "b": float(k[b0]), "art": "überdeckt", "name": street(int(np.median(g))), "decke": float(raw[a:b + 1].max()),
                    "fahrbahn": [float(raw[a0]), float(raw[b0])], "gpx": [float(gpx[a:b + 1].min()), float(gpx[a:b + 1].max())]})
    print(f"  überdeckt km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {street(int(np.median(g))):20s}: Modell bis {raw[a:b + 1].max():.2f} (Decke), "
          f"Gerade {raw[a0]:.2f} → {raw[b0]:.2f}, GPX dort {gpx[a:b + 1].min():.2f}–{gpx[a:b + 1].max():.2f}")
# 2. Brücken
umg = np.array([np.median(np.r_[raw[max(0, i - 6):i], raw[i + 1:i + 7]]) for i in range(len(raw))])
kand = (~np.isnan(deck) & (deck - raw > 0.5)) | (raw < 434.2) | (raw < umg - 0.8)
kand &= ~geschaetzt
for g in gruppen(kand):
    a, b = g.min(), g.max(); a0, b0 = max(0, a - 1), min(len(h) - 1, b + 1)
    gerade = np.interp(np.arange(a, b + 1), [a0, b0], [raw[a0], raw[b0]])
    tief = float((gerade - raw[a:b + 1]).max())
    if tief < 0.5: continue                       # keine Senke: Brücke über der Strecke oder Bäume über flacher Straße
    seg = deck[a:b + 1]; glatt = not np.isnan(seg).any() and np.all(np.abs(seg - mitte[a:b + 1]) < 0.6) and np.all(seg < gerade + 10)
    if glatt:
        h[a:b + 1] = np.maximum(seg, raw[a:b + 1]); art = "gemessen"
    elif tief < 1.5: continue                     # flache Mulde im Wald (Stutzstrasse km 5,95): echt, keine Brücke
    else:
        h[a:b + 1] = gerade; geschaetzt[a:b + 1] = True; art = "geschätzt"
    regions.append({"a": float(k[a0]), "b": float(k[b0]), "art": "Brücke " + art, "name": street(int(np.median(g))), "gelaende": float(raw[a:b + 1].min()),
                    "fahrbahn": [float(h[a:b + 1].min()), float(h[a:b + 1].max())], "gpx": [float(gpx[a:b + 1].min()), float(gpx[a:b + 1].max())]})
    print(f"  Brücke {art:9s} km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {street(int(np.median(g))):20s}: Gelände {raw[a:b + 1].min():.2f}, "
          f"Fahrbahn {h[a:b + 1].min():.2f}–{h[a:b + 1].max():.2f}, GPX {gpx[a:b + 1].min():.2f}–{gpx[a:b + 1].max():.2f}")
d_ = np.abs(np.diff(h)); print(f"  Stufen über 1,0 m je 10 m: {(d_ > 1.0).sum()}, größte {d_.max():.2f} m bei km {k[np.argmax(d_)] / 1000:.2f}")
print(f"  GPX-Höhen minus bereinigt: Median {np.median(gpx - h):+.2f} m, 95 % zwischen {np.percentile(gpx - h, 2.5):+.2f} und {np.percentile(gpx - h, 97.5):+.2f} m, "
      f"größte {np.abs(gpx - h).max():.2f} m bei km {k[np.argmax(np.abs(gpx - h))] / 1000:.2f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "geschaetzt": geschaetzt.astype(int).tolist(), "regions": regions,
           "quelle": "swissALTI3D 0,5 m + swissSURFACE3D an Brücken"}, open("clean.json", "w"), ensure_ascii=False)
