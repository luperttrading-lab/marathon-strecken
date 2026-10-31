# Höhenprofil für die App -> clean.json. Grundlage: swissALTI3D 0,5 m (dgm.py, dgm_vergleich.json „gel05“). Muster: werkzeuge/luzern/work/clean.py.
# Überdeckte Stücke: keine. Die drei kurzen Unterführungen in OSM (Lauterbrunnen km 25,9 unter der Bahn, Wengen km 31,8 unter der
# Bahn, Mendelssohnweg km 34,6) misst das Geländemodell richtig (Bahn weg, Boden sichtbar; bedeckt.py, Modell nicht über den Höhen der
# Linie des Veranstalters).
# Brücken: Das Geländemodell lässt Brücken weg und misst darunter die Lütschine oder den Bach. Kandidaten (deck.py) sind OSM-Brücken,
# Senken unter der Geraden über ±40 m und Stellen, an denen die Höhen der Linie des Veranstalters über dem Geländemodell liegen.
# Je zusammenhängendem Stück: Gerade zwischen den Rändern; liegt das Geländemodell dort nirgends 0,8 m darunter, bleibt es (keine
# Senke: kleine Brücke über einen Graben, Bäume über dem Weg). Sonst
#   - gemessen, wo das Oberflächenmodell glatt ist (Mitte und 25-%-Quantil auf 0,6 m gleich, nicht über 3 m über der Geraden), dort
#     über dem Geländemodell liegt (die Brücke ist zu sehen) und OSM eine Brücke hat oder die Linie des Veranstalters in der Senke mehr
#     als 1 m über dem Geländemodell liegt: seine Fahrbahn;
#   - geschätzt (Gerade), wo Bäume oder Geländer das Oberflächenmodell stören, OSM eine Brücke hat und die Linie des Veranstalters in
#     der Senke mehr als 1 m über dem Geländemodell liegt;
#   - sonst bleibt das Geländemodell (echte Mulde im Weg, am Berg häufig: Bachgräben mit Durchlass, Kehren; die Linie des Veranstalters
#     und das Oberflächenmodell zeigen dort dieselbe Mulde).
# Keine weitere Glättung: build.py nimmt den Median über 30 m.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
raw = np.array(v["gel05"], float); gpx = np.array(v["gpx"]); h = raw.copy()
dj = json.load(open("deck.json")); deck = np.full(len(h), np.nan); mitte = np.full(len(h), np.nan)
deck[dj["i"]] = dj["deck"]; mitte[dj["i"]] = dj["mitte"]
st = json.load(open("strassen.json"))
def street(i): o = st[min(len(st) - 1, i)]; return o[1] or o[6] or ""
osmbr = np.zeros(len(h), bool); osmbr[:len(st)] = np.array([o[3] not in ("", "no") for o in st])[:len(h)]
regions = []
def gruppen(m):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []
geschaetzt = np.zeros(len(h), bool)
ger = np.array([np.interp(i, [i - 4, i + 4], [raw[i - 4], raw[i + 4]]) if 4 <= i < len(raw) - 4 else raw[i] for i in range(len(raw))])
kand = (ger - raw > 0.8) | (gpx - raw > 1.0) | osmbr
kand2 = kand.copy(); kand2[1:] |= kand[:-1]; kand2[:-1] |= kand[1:]          # je 10 m Rand
for g in gruppen(kand2):
    a, b = g.min(), g.max(); a0, b0 = max(0, a - 1), min(len(h) - 1, b + 1)
    gerade = np.interp(np.arange(a, b + 1), [a0, b0], [raw[a0], raw[b0]])
    tief = float((gerade - raw[a:b + 1]).max())
    if tief < 0.8: continue
    seg = deck[a:b + 1]; senke = (gerade - raw[a:b + 1]) > 0.8
    glatt = (not np.isnan(seg).any() and np.all(np.abs(seg - mitte[a:b + 1]) < 0.6) and np.all(seg < gerade + 3)
             and np.all(seg > raw[a:b + 1] - 0.3))
    bruecke = osmbr[a:b + 1].any(); gpxhoch = float((gpx[a:b + 1] - raw[a:b + 1])[senke].max())
    if glatt and float((seg - raw[a:b + 1]).max()) > 0.5 and (bruecke or gpxhoch > 1.0):
        h[a:b + 1] = np.maximum(seg, raw[a:b + 1]); art = "gemessen"        # Brücke im Oberflächenmodell sichtbar
    elif bruecke and gpxhoch > 1.0:
        h[a:b + 1] = gerade; geschaetzt[a:b + 1] = True; art = "geschätzt"  # Brücke laut OSM, Linie des Veranstalters bestätigt die Senke nicht
    else:
        continue                                                            # echte Mulde (Linie und Oberflächenmodell gleich dem Gelände)
    regions.append({"a": float(k[a0]), "b": float(k[b0]), "art": "Brücke " + art, "name": street(int(np.median(g))), "osm": bool(bruecke),
                    "gelaende": float(raw[a:b + 1].min()), "fahrbahn": [float(h[a:b + 1].min()), float(h[a:b + 1].max())],
                    "gpx": [float(gpx[a:b + 1].min()), float(gpx[a:b + 1].max())], "tief": tief})
    print(f"  Brücke {art:9s} km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {street(int(np.median(g))):24.24s} OSM {'ja  ' if bruecke else 'nein'} "
          f"Gelände {raw[a:b + 1].min():7.1f} (bis {tief:4.1f} m unter der Geraden), Fahrbahn {h[a:b + 1].min():7.1f}–{h[a:b + 1].max():7.1f}, "
          f"Linie {gpx[a:b + 1].min():7.1f}–{gpx[a:b + 1].max():7.1f}")
d_ = np.abs(np.diff(h)); print(f"  Stufen über 3,0 m je 10 m: {(d_ > 3.0).sum()}, größte {d_.max():.2f} m bei km {k[np.argmax(d_)] / 1000:.2f}")
print(f"  Linie (draped) minus bereinigt: Median {np.median(gpx - h):+.2f} m, 95 % zwischen {np.percentile(gpx - h, 2.5):+.2f} und "
      f"{np.percentile(gpx - h, 97.5):+.2f} m, größte {np.abs(gpx - h).max():.2f} m bei km {k[np.argmax(np.abs(gpx - h))] / 1000:.2f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "geschaetzt": geschaetzt.astype(int).tolist(), "regions": regions,
           "quelle": "swissALTI3D 0,5 m + swissSURFACE3D an Brücken"}, open("clean.json", "w"), ensure_ascii=False)
