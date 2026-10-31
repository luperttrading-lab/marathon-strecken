# Höhenprofil für die App -> clean.json. Grundlage: swissALTI3D 0,5 m (dgm.py, dgm_vergleich.json „gel05“). Muster: werkzeuge/zermatt/work/clean.py,
# aber ohne GPX-Höhen (die Linie kommt aus OSM-Wegen, route_osm.py).
# 1. Überdeckte Stücke (bedeckt.py: OSM tunnel=* oder covered=yes unter der Linie), in denen das Geländemodell mehr als 1,5 m über der
#    Geraden zwischen den Portalen liegt: Es misst dort die Decke, nicht den Weg. Geschätzt als Gerade zwischen den Portalen.
# 2. Brücken: Das Geländemodell lässt Brücken weg und misst darunter den Bach. Oberflächenmodell an den Kandidaten aus deck.py (OSM-Brücken,
#    Senken). Eine Brücke ist ein Stück bis 120 m, auf dem das Oberflächenmodell glatt ist (Mitte und 25-%-Quantil auf 1 m gleich), mehr als
#    0,8 m über dem Geländemodell liegt, auf 1,5 m auf der Geraden zwischen den Wegstücken davor und danach bleibt (also Weghöhe, keine Bäume)
#    und das Geländemodell darunter mehr als 0,8 m absinkt: Dort gilt die Fahrbahn aus dem Oberflächenmodell (gemessen). Nicht so gefundene
#    OSM-Brücken (Bäume darüber) werden als Gerade zwischen ihren Enden geschätzt, wenn das Modell mehr als 1,5 m darunter fällt. Senken ohne
#    Brücke (Bachgräben, die der Weg durchquert, Kehren am Hang) bleiben gemessen.
# Keine weitere Glättung: build.py nimmt den Median über 30 m.
import json
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); s = np.array(v["s"]); k = official(s)
raw = np.array(v["gel05"], float); h = raw.copy()
dj = json.load(open("deck.json")); deck = np.full(len(h), np.nan); mitte = np.full(len(h), np.nan)
deck[dj["i"]] = dj["deck"]; mitte[dj["i"]] = dj["mitte"]
st = json.load(open("strassen.json"))
def street(i): return st[min(len(st) - 1, i)][1] or st[min(len(st) - 1, i)][6] or ""
osmbr = np.zeros(len(h), bool); osmbr[:len(st)] = np.array([o[3] not in ("", "no") for o in st])[:len(h)]
bed = np.zeros(len(h), bool)
for s_, _, _ in json.load(open("bedeckt.json")): bed[int(round(s_ / 10))] = True
bed2 = bed.copy(); bed2[1:] |= bed[:-1]; bed2[:-1] |= bed[1:]
regions = []
def gruppen(m):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []
# 1. überdeckte Stücke
geschaetzt = np.zeros(len(h), bool)
for g in gruppen(bed2):
    a0, b0 = max(0, g.min() - 1), min(len(h) - 1, g.max() + 1)
    gerade = np.interp(np.arange(a0, b0 + 1), [a0, b0], [raw[a0], raw[b0]]); ueber_ = float((raw[a0:b0 + 1] - gerade).max())
    nm = street(int(np.median(g)))
    if ueber_ < 1.5:
        print(f"  überdeckt km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {nm:20s}: Modell höchstens {ueber_:.2f} m über der Geraden, bleibt gemessen")
        continue
    h[a0:b0 + 1] = gerade; geschaetzt[a0:b0 + 1] = True
    regions.append({"a": float(k[a0]), "b": float(k[b0]), "art": "überdeckt", "name": nm, "decke": float(raw[a0:b0 + 1].max()),
                    "fahrbahn": [float(raw[a0]), float(raw[b0])]})
    print(f"  überdeckt km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {nm:20s}: Modell bis {raw[a0:b0 + 1].max():.2f} "
          f"(Decke, {ueber_:.1f} m über der Geraden), Gerade {raw[a0]:.2f} → {raw[b0]:.2f}")
# 2. Brücken
osm_name = lambda i: st[min(len(st) - 1, i)][1] or ""
glatt_ = ~np.isnan(deck) & (np.abs(deck - mitte) < 1.0)
ueber = glatt_ & (deck - raw > 0.8)
for d_ in (1,):   # Lücken von einem Punkt (Geländer, Leuchte) schliessen
    luecke = ~ueber[1:-1] & ueber[:-2] & ueber[2:]; ueber[1:-1] |= luecke
ueber &= ~geschaetzt
erledigt = np.zeros(len(h), bool)
boden = glatt_ & (np.abs(deck - raw) < 0.4)          # Oberfläche = Gelände: kein Bauwerk, Weg auf dem Boden
def enden(a, b, n=3):
    """Stück nach aussen bis zum nächsten Bodenpunkt verlängern (höchstens n Punkte je Seite)."""
    for _ in range(n):
        if a > 0 and not boden[a - 1] and not np.isnan(deck[a - 1]) and raw[a - 1] < raw[max(0, a - 2)] - 0.3: a -= 1
        else: break
    for _ in range(n):
        if b < len(h) - 1 and not boden[b + 1] and not np.isnan(deck[b + 1]) and raw[b + 1] < raw[min(len(h) - 1, b + 2)] - 0.3: b += 1
        else: break
    return a, b
for g in gruppen(ueber):
    a, b = enden(g.min(), g.max()); a0, b0 = max(0, a - 1), min(len(h) - 1, b + 1)
    if (b0 - a0) * 10 > 120: continue
    gerade = np.interp(np.arange(a, b + 1), [a0, b0], [raw[a0], raw[b0]])
    tief = float((gerade - raw[a:b + 1]).max()); seg = deck[a:b + 1]
    ok = ueber[a:b + 1] & glatt_[a:b + 1]
    if tief < 0.8 or not ok.any() or np.max(np.abs(seg[ok] - gerade[ok])) > 1.5: continue   # keine Senke, oder Oberfläche nicht auf Weghöhe (Bäume)
    xi = np.arange(a, b + 1); neu_ = np.interp(xi, np.r_[a0, xi[ok], b0], np.r_[raw[a0], seg[ok], raw[b0]])   # unruhige Punkte zwischen den Nachbarn
    h[a:b + 1] = np.maximum(neu_, raw[a:b + 1]); erledigt[a0:b0 + 1] = True
    br = bool(osmbr[a0:b0 + 1].any())
    regions.append({"a": float(k[a0]), "b": float(k[b0]), "art": "Brücke gemessen", "name": osm_name(int(np.median(g))), "gelaende": float(raw[a:b + 1].min()),
                    "fahrbahn": [float(h[a:b + 1].min()), float(h[a:b + 1].max())],
                    "osm": br, "senke": tief})
    print(f"  Brücke gemessen  km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {street(int(np.median(g))):20s}: Gelände {raw[a:b + 1].min():.2f}, "
          f"Fahrbahn {h[a:b + 1].min():.2f}–{h[a:b + 1].max():.2f}, Senke {tief:.2f}{' (OSM-Brücke)' if br else ''}")
# OSM-Brücken ohne brauchbares Oberflächenmodell (Bäume): Gerade zwischen den Enden, wenn das Geländemodell mehr als 1,5 m darunter fällt
for g in gruppen(osmbr & ~erledigt & ~geschaetzt):
    a, b = enden(g.min(), g.max()); a0, b0 = max(0, a - 1), min(len(h) - 1, b + 1)
    gerade = np.interp(np.arange(a, b + 1), [a0, b0], [raw[a0], raw[b0]]); tief = float((gerade - raw[a:b + 1]).max())
    if tief < 1.5:
        if tief > 0.5: print(f"  OSM-Brücke km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} bleibt gemessen (Senke {tief:.2f} m)")
        continue
    h[a:b + 1] = gerade; geschaetzt[a:b + 1] = True
    regions.append({"a": float(k[a0]), "b": float(k[b0]), "art": "Brücke geschätzt", "name": osm_name(int(np.median(g))), "gelaende": float(raw[a:b + 1].min()),
                    "fahrbahn": [float(h[a:b + 1].min()), float(h[a:b + 1].max())],
                    "osm": True, "senke": tief})
    print(f"  Brücke geschätzt km {k[a0] / 1000:6.3f}–{k[b0] / 1000:6.3f} ({(b0 - a0) * 10:3d} m) {street(int(np.median(g))):20s}: Gelände {raw[a:b + 1].min():.2f}, "
          f"Gerade {raw[a0]:.2f} → {raw[b0]:.2f}, Senke {tief:.2f}")
d_ = np.abs(np.diff(h)); print(f"  Stufen über 3 m je 10 m: {(d_ > 3).sum()}, größte {d_.max():.2f} m bei km {k[np.argmax(d_)] / 1000:.2f}")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "geschaetzt": geschaetzt.astype(int).tolist(), "regions": regions,
           "quelle": "swissALTI3D 0,5 m + swissSURFACE3D an Brücken"}, open("clean.json", "w"), ensure_ascii=False)
