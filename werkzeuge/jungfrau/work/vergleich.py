# Nur Abgleich: Höhenmeter und Kennzahlen der Höhenquellen im selben Verfahren wie die App (offizielle km, 10-m-Raster, Median über 30 m,
# Steigung über das Messfenster): bereinigt (App), Geländemodell ohne Bereinigung, swissALTI3D 2 m mit denselben Brücken, Höhen der Linie
# des Veranstalters („3D_DRAPED“). Dazu die einfache Summe aller Anstiege Punkt für Punkt, wie GPX-Programme sie zeigen, für die volle
# Linie (67 296 Punkte). Der Veranstalter nennt „1953 Höhenmeter“, Start 567 m, Ziel 2320 m. Dazu Höhen und Anstiege je Abschnitt.
# Muster: werkzeuge/luzern/work/vergleich.py
import json, re
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); c = json.load(open("clean.json"))
k = official(np.array(v["s"])); L = 42195.0; grid = np.arange(0, L + 1, 10.0)
raw = np.array(v["gel05"]); app = np.array(c["h"]); gpx = np.array(v["gpx"]); g2 = np.array(v["gel2"])
g2b = g2.copy(); ers = np.abs(app - raw) > 0.01; g2b[ers] = app[ers]          # 2 m mit denselben Brücken
def kenn(h, kk=k):
    hg = np.interp(grid, kk, h); hm = hg.copy()
    for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i - 1:i + 2])
    at = lambda x: float(np.interp(x, grid, hm))
    def asc(w):
        gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
        dh = (gr[1:] + gr[:-1]) / 2 * 10; return dh[dh > 0].sum(), -dh[dh < 0].sum(), gr
    return hm, asc(200), asc(1000)[0], asc(50)[0], asc(100)[0]
def summe(h): return float(np.clip(np.diff(h), 0, None).sum())
t = open("../dl/kmz/doc.kml", encoding="iso-8859-1").read()
roh = np.array([float(x.split(",")[2]) for x in re.search(r"<coordinates>(.*?)</coordinates>", t, re.S).group(1).split()])
ref = None
print("| Quelle | Start | Ziel | min (km) | max | ↑/↓ 200 m | ↑ 100 m | ↑ 50 m | ↑ 1 km | ↑ Punkt für Punkt | gegen App (Median) | r |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for nm, h, pp in (("App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D bzw. geschätzt)", app, summe(app)),
                  ("swissALTI3D 0,5 m ohne Bereinigung", raw, summe(raw)),
                  ("swissALTI3D 2 m, gleiche Brücken", g2b, summe(g2b)),
                  ("Höhen der Linie des Veranstalters (3D_DRAPED, 10-m-Raster; Punkt für Punkt: alle 67 296 Punkte)", gpx, summe(roh))):
    hm, (u, d, gr), u1k, u50, u100 = kenn(h)
    if ref is None: ref = hm
    print(f"| {nm} | {hm[0]:.1f} | {hm[-1]:.1f} | {hm.min():.1f} ({grid[hm.argmin()] / 1000:.2f}) | {hm.max():.1f} | "
          f"{u:.0f}/{d:.0f} | {u100:.0f} | {u50:.0f} | {u1k:.0f} | {pp:.0f} | {np.median(hm - ref):+.2f} | {np.corrcoef(hm, ref)[0, 1]:.4f} |")
hm, (u, d, gr), *_ = kenn(app)
# Abschnitte nach den Zeitmesspunkten 2026 (Race-Info, Datasport)
P = [(0, "Start Höheweg"), (3300, "Höheweg"), (5000, "ALDI"), (10400, "Wilderswil"), (15100, "Zweilütschinen"), (21100, "Lauterbrunnen Staubbach"),
     (25900, "Stocki"), (30700, "Wengen"), (38500, "Abzweigung Wixi"), (L, "Ziel Eigergletscher")]
print("\nAbschnitt | km | Höhe von → bis | ↑ / ↓ (200 m) | mittlere Steigung | steilste 200 m")
for (a, na), (b, nb) in zip(P[:-1], P[1:]):
    s = (grid >= a) & (grid <= b); gg = gr[s]; dh = (gg[1:] + gg[:-1]) / 2 * 10
    print(f"{na} – {nb} | {a/1000:.1f}–{b/1000:.1f} | {hm[s][0]:.0f} → {hm[s][-1]:.0f} m | {dh[dh > 0].sum():.0f} / {-dh[dh < 0].sum():.0f} | "
          f"{(hm[s][-1] - hm[s][0]) / (b - a) * 100:+.1f} % | {gg.max() * 100:+.1f} % bei km {grid[s][np.argmax(gg)] / 1000:.2f}")
for x in (0, 5000, 10000, 15000, 20000, 21098, 25000, 26000, 28800, 30700, 33400, 36300, 38500, 38900, 40220, 41000, 41500, L):
    print(f"  km {x / 1000:6.3f}: {float(np.interp(x, grid, hm)):7.1f} m")
