# Nur Abgleich: Höhenmeter und Kennzahlen der Höhenquellen im selben Verfahren wie die App (offizielle km, 10-m-Raster, Median über 30 m,
# Steigung über das Messfenster): bereinigt (App), Geländemodell ohne Bereinigung, swissALTI3D 2 m mit denselben Brücken und Tunneln,
# GPX-Höhen (MySchweizMobil) und das Höhenprofil der TrackMaxx-Karte des Veranstalters (100 Punkte). Dazu die einfache Summe aller
# Anstiege Punkt für Punkt, wie sie GPX-Programme und Webdienste zeigen. Der Veranstalter nennt „Höhenmeter +175m / -175m“ und schreibt,
# „diverse GPX-Files sowie Webdienste“ zeigten „fälschlich einen Wert von 220m“ (Seite „Marathon“, Reiter „Streckenplan“).
import json, re
import numpy as np
from common import official
v = json.load(open("dgm_vergleich.json")); c = json.load(open("clean.json"))
k = official(np.array(v["s"])); L = 42195.0; grid = np.arange(0, L + 1, 10.0)
raw = np.array(v["gel05"]); app = np.array(c["h"]); gpx = np.array(v["gpx"]); g2 = np.array(v["gel2"])
g2b = g2.copy(); ers = np.abs(app - raw) > 0.01; g2b[ers] = app[ers]          # 2 m mit denselben Brücken und Tunneln
m = json.load(open("../dl/trackmaxx/getmap.json")); tr = [t for t in m["tracks"] if t["caption"] == "42.2 km"][0]
tm = np.array([[float(a) for a in z.split(",")] for z in tr["elevationprofile"].split()])
def kenn(h, kk=k):
    hg = np.interp(grid, kk, h); hm = hg.copy()
    for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i - 1:i + 2])
    at = lambda x: float(np.interp(x, grid, hm))
    def asc(w):
        gr = np.array([(at(min(x + w / 2, L)) - at(max(x - w / 2, 0))) / (min(x + w / 2, L) - max(x - w / 2, 0)) for x in grid])
        dh = (gr[1:] + gr[:-1]) / 2 * 10; return dh[dh > 0].sum(), -dh[dh < 0].sum()
    return hm, asc(200), asc(1000)[0], asc(50)[0], asc(100)[0]
def summe(h): return float(np.clip(np.diff(h), 0, None).sum())
ref = None
print("| Quelle | Start | Ziel | min (km) | max (km) | ↑/↓ 200 m | ↑ 100 m | ↑ 50 m | ↑ 1 km | ↑ Punkt für Punkt | gegen App (Median) | r |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
t = open("../dl/gpx/scml_42km_definitiv.gpx", encoding="utf-8").read()
gpx_roh = np.array([float(x) for x in re.findall(r"<ele>([^<]+)</ele>", t)])
for nm, h, kk, pp in (("App (swissALTI3D 0,5 m, Brücken aus swissSURFACE3D, Tunnel geschätzt)", app, k, summe(app)),
                      ("swissALTI3D 0,5 m ohne Bereinigung", raw, k, summe(raw)),
                      ("swissALTI3D 2 m, gleiche Brücken und Tunnel", g2b, k, summe(g2b)),
                      ("GPX-Höhen des Veranstalters (MySchweizMobil)", gpx, k, summe(gpx_roh)),
                      ("Höhenprofil der TrackMaxx-Karte (100 Punkte, ganze Meter)", tm[:, 1], tm[:, 0] * 1000 * 42195 / 42190, summe(tm[:, 1]))):
    hm, (u, d), u1k, u50, u100 = kenn(h, kk)
    if ref is None: ref = hm
    print(f"| {nm} | {hm[0]:.1f} | {hm[-1]:.1f} | {hm.min():.1f} ({grid[hm.argmin()] / 1000:.2f}) | {hm.max():.1f} ({grid[hm.argmax()] / 1000:.2f}) | "
          f"{u:.0f}/{d:.0f} | {u100:.0f} | {u50:.0f} | {u1k:.0f} | {pp:.0f} | {np.median(hm - ref):+.2f} | {np.corrcoef(hm, ref)[0, 1]:.3f} |")
print("GPX roh: Punkte", len(gpx_roh), "Summe ↑", round(summe(gpx_roh), 1), "↓", round(summe(gpx_roh[::-1]), 1))
# je 5 km
hm = kenn(app)[0]
for a in range(0, 42, 5):
    s = (grid >= a * 1000) & (grid <= min(L, (a + 5) * 1000)); x = hm[s]
    print(f"km {a:2d}–{min(42.2, a + 5):4.1f}: {x.min():.1f}–{x.max():.1f} m")
