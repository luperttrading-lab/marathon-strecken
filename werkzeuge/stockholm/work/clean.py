# Höhenprofil für die App -> clean.json. Zwei Wege (Entscheidung und Begründung in UEBERGABE.md, Daten 5):
#   python3 clean.py            (Standard, „gpx“): die in die GPX-Datei des Veranstalters eingebetteten Höhen. Sie sind glatt, liegen
#       an den Kais auf 2–3 m und enthalten die Brückendecks (Västerbron 30,6 m über Riddarfjärden bei 26 m Durchfahrtshöhe); im
#       offenen Gelände (Djurgården, Gärdet, Norr Mälarstrand) stimmen sie mit FABDEM überein. Brücken bleiben so, wie sie die
#       Datei zeigt (gemessen, nicht schraffiert); nur Stufen über 1,5 m je 10 m würden bereinigt (es gibt keine).
#   python3 clean.py fabdem [HW] (Gegenprobe): FABDEM, bereinigt wie folgt.
# FABDEM-Weg (Grundlage dgm2026_10m.json, 1″-Raster, dgm.py):
# 1. Brücken aus OSM (bridge=yes auf der Linie, strassen.json): Die Stockholmer Brücken liegen über Wasser, das FABDEM (wie
#    Copernicus) auf 0 m setzt; das Brückendeck fehlt im Modell. Enden oben auf den Rampen (höchster Punkt bis 40 m außerhalb der
#    OSM-Brücke), gerade gezogen, wo das Modell innen mehr als 1,0 m unter der Geraden liegt; „geschätzt“, in der App schraffiert.
#    Västerbron (950 m, über Långholmen und Riddarfjärden) ebenso: In Wirklichkeit steigt die Fahrbahn zur Mitte über dem
#    Hauptstrom an (Durchfahrtshöhe 26 m, die GPX-Höhen des Veranstalters zeigen 30,6 m); ohne frei zugängliches Oberflächenmodell
#    bleibt es bei der Geraden zwischen den Rampenenden (siehe UEBERGABE.md, Offen).
# 2. Wasser außerhalb der Brücken: Punkte, an denen das Modell unter 1,0 m fällt (Kaimauern an Skeppsbron, Strandvägen,
#    Norr Mälarstrand: das 30-m-Raster mischt Straße und Wasser), werden aus den Nachbarn ersetzt.
# 3. Das 30-m-Raster zeigt in der Stadt Stufen und Buckel von Häusern, Felsen und Mauern (Södermalm, Kungsholmen, Norrmalm;
#    FABDEM rechnet Gebäude nur teilweise heraus). Deshalb wie in Athen (Innenstadt) auf der ganzen Strecke robust geglättet:
#    lokal gewichtete Ausgleichsgerade über ±HW m (LOWESS, Tricube, drei Runden mit Bisquare-Gewichten gegen Ausreißer).
#    Brücken bleiben dabei gerade (sie gehen mit Gewicht 1 ein und werden danach wieder gesetzt).
import json, sys, numpy as np
from common import official
QUELLE = sys.argv[1] if len(sys.argv) > 1 else "gpx"
HW = float(sys.argv[2]) if len(sys.argv) > 2 else 150.0
v = json.load(open("dgm_vergleich.json"))
s = np.array(v["s"]); k = official(s)
raw = np.array(v[QUELLE], float)
st = json.load(open("strassen.json"))
def street(gpx_m):
    o = st[min(len(st) - 1, int(round(gpx_m / 10)))]; return o[2] or ""
h = raw.copy(); est = np.zeros(len(h), bool); bname = {}
n = min(len(h), len(st))
br = np.zeros(len(h), bool); br[:n] = [o[3] not in ("", "no") for o in st[:n]]
def gruppen(m, luecke):
    idx = np.where(m)[0]
    return np.split(idx, np.where(np.diff(idx) > luecke)[0] + 1) if len(idx) else []
brueck = []
for g in (gruppen(br, 3) if QUELLE == "fabdem" else []):
    a0, b0 = int(g.min()), int(g.max()) + 1
    nm = st[int(np.median(g))][2] or "Brücke"
    a = max(0, a0 - 4) + int(np.argmax(h[max(0, a0 - 4):a0 + 1])); b = b0 + int(np.argmax(h[b0:min(len(h), b0 + 5)]))
    line = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
    dev = (line - h[a:b + 1]).max()
    if dev > 1.0:
        h[a:b + 1] = line; est[a + 1:b] = True; brueck.append((a, b, nm))
        for i in range(a + 1, b): bname[i] = nm
    print(f"  Brücke km {k[a0] / 1000:6.2f}–{k[b0] / 1000:6.2f} ({(b0 - a0) * 10:4d} m) {nm:22s} Modell {raw[a0:b0 + 1].min():5.1f}–{raw[a0:b0 + 1].max():5.1f} m, "
          f"Enden km {k[a] / 1000:6.2f} / {k[b] / 1000:6.2f} ({h[a]:.1f} / {h[b]:.1f} m), unter der Geraden {dev:4.1f} m  {'gerade gezogen' if dev > 1.0 else 'gemessen'}")
if QUELLE == "gpx":
    for g in gruppen(br, 3):
        a0, b0 = int(g.min()), int(g.max()) + 1
        print(f"  Brücke km {k[a0] / 1000:6.2f}–{k[b0] / 1000:6.2f} ({(b0 - a0) * 10:4d} m) {st[int(np.median(g))][2]:22s} GPX {raw[a0:b0 + 1].min():5.1f}–{raw[a0:b0 + 1].max():5.1f} m, "
              f"FABDEM {np.array(v['fabdem'])[a0:b0 + 1].min():5.1f}–{np.array(v['fabdem'])[a0:b0 + 1].max():5.1f} m")
    d_ = np.abs(np.diff(h)); print(f"  Stufen über 1,5 m je 10 m: {(d_ > 1.5).sum()}, größte {d_.max():.2f} m")
    json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": [], "quelle": QUELLE}, open("clean.json", "w"), ensure_ascii=False)
    raise SystemExit
wasser = (h < 1.0) & ~est
for g in gruppen(wasser, 1):
    print(f"  Wasser im Modell km {k[g.min()] / 1000:6.2f}–{k[g.max()] / 1000:6.2f} ({street(s[g.min()])}), {raw[g].min():.1f} m")
ok = ~wasser
h = np.interp(np.arange(len(h)), np.where(ok)[0], h[ok])
def lowess(x, y, hw, runden=3, fest=None):
    w_rob = np.ones_like(y); out = y.copy()
    for _ in range(runden + 1):
        for i in range(len(x)):
            lo, hi = np.searchsorted(x, x[i] - hw), np.searchsorted(x, x[i] + hw)
            xx = x[lo:hi]; dd = np.abs(xx - x[i]); ww = (1 - (dd / hw) ** 3) ** 3 * w_rob[lo:hi]
            X = np.c_[np.ones(len(xx)), xx - x[i]]
            out[i] = np.linalg.lstsq(X.T @ (X * ww[:, None]), X.T @ (y[lo:hi] * ww), rcond=None)[0][0]
        res = y - out; sres = np.median(np.abs(res)) * 6 or 1; u = res / sres; w_rob = np.where(np.abs(u) < 1, (1 - u ** 2) ** 2, 0)
        if fest is not None: w_rob[fest] = 1.0
    return out
vorher = h.copy()
h = lowess(k, h, HW, fest=est)
for a, b, nm in brueck:   # Brücken wieder gerade zwischen den geglätteten Enden
    h[a:b + 1] = h[a] + (h[b] - h[a]) * (np.arange(a, b + 1) - a) / max(1, b - a)
dv = np.abs(h - vorher)[~est]
print(f"  geglättet (±{HW:.0f} m): Abweichung vom Modell Median {np.median(dv):.1f} m, 90 % {np.percentile(dv, 90):.1f} m, höchstens {dv.max():.1f} m bei km {k[~est][np.argmax(dv)] / 1000:.2f}")
out = []
for a, b, nm in brueck:
    out.append({"a": float(k[a]), "b": float(k[b]), "kind": "Brücke", "name": nm, "ha": float(h[a]), "hb": float(h[b]), "extrem": float(raw[a + 1:b].min())})
for o in out: print(f"km {o['a'] / 1000:6.2f}-{o['b'] / 1000:6.2f} {o['b'] - o['a']:5.0f} m  {o['kind']:8s} {o['name']:22s} {o['ha']:6.1f} -> {o['hb']:6.1f}  (Modell {o['extrem']:6.1f})")
json.dump({"k": k.tolist(), "h": h.tolist(), "raw": raw.tolist(), "regions": out, "hw": HW, "quelle": QUELLE}, open("clean.json", "w"), ensure_ascii=False)
