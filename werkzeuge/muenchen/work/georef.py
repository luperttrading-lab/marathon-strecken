# Strecke 2026 aus dem PDF des Veranstalters (eine Vektorlinie, Karte von mapz.com auf OpenStreetMap-Basis) auf echte
# Koordinaten legen: Ähnlichkeitstransformation (Maßstab, Drehung, Verschiebung) PDF -> Web-Mercator, iterativ an die
# Straßen aus OpenStreetMap angepasst (ICP mit schrumpfendem Suchradius). -> ../dl/strecke_georef.json
import json, math, sys
import numpy as np
from scipy.spatial import cKDTree
R = 6378137.0
def merc(lat, lon): return np.array([R * np.radians(lon), R * np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))]).T
def unmerc(xy): return np.degrees(2 * np.arctan(np.exp(xy[:, 1] / R)) - np.pi / 2), np.degrees(xy[:, 0] / R)
P = np.array(json.load(open("../dl/pdf_linie.json")), float); P[:, 1] = -P[:, 1]   # PDF-y zeigt nach unten
# gleichmäßig alle 0,5 pt für die Anpassung
seg = np.hypot(*np.diff(P, axis=0).T); cum = np.concatenate([[0], np.cumsum(seg)])
u = np.arange(0, cum[-1], 0.5); Q = np.c_[np.interp(u, cum, P[:, 0]), np.interp(u, cum, P[:, 1])]
# Straßen alle 4 m (Mercator-Meter)
osm = json.load(open("../dl/osm_wege.json")); road = []
for w in osm["elements"]:
    g = w.get("geometry")
    if not g or len(g) < 2: continue
    m = merc(np.array([p["lat"] for p in g]), np.array([p["lon"] for p in g]))
    for a, b in zip(m[:-1], m[1:]):
        n = max(1, int(np.hypot(*(b - a)) / 4)); t = np.linspace(0, 1, n + 1)[:-1, None]; road.append(a + (b - a) * t)
road = np.vstack(road); tree = cKDTree(road); print("Straßenpunkte", len(road))
def umeyama(src, dst):   # Ähnlichkeit: dst ≈ s·R·src + t
    ms, md = src.mean(0), dst.mean(0); A, B = src - ms, dst - md
    U, S, Vt = np.linalg.svd(B.T @ A / len(src)); D = np.eye(2)
    if np.linalg.det(U @ Vt) < 0: D[1, 1] = -1
    Rm = U @ D @ Vt; s = np.trace(np.diag(S) @ D) / (A ** 2).sum(1).mean()
    return s, Rm, md - s * Rm @ ms
# Startwert: Ziel (Ende der Linie) im Olympiastadion, Maßstab aus der Länge (42,195 km), Norden oben
k = 1 / math.cos(math.radians(48.15)); s0 = 42195 * k / cum[-1]; ziel = merc(np.array([48.1731]), np.array([11.5466]))[0]
best = None
for dx in range(-800, 801, 200):
    for dy in range(-800, 801, 200):
        s, Rm = s0, np.eye(2); t = ziel + [dx, dy] - s * P[-1]
        for rad in (600, 300, 150, 80, 40, 25, 25, 25):
            X = s * Q @ Rm.T + t; d, i = tree.query(X); ok = d < rad
            if ok.sum() < 200: break
            s, Rm, t = umeyama(Q[ok], road[i[ok]])
        X = s * Q @ Rm.T + t; d, _ = tree.query(X); score = np.median(d)
        if best is None or score < best[0]: best = (score, s, Rm, t, (dx, dy))
score, s, Rm, t, start = best
# Stufe 2: das ganze Straßennetz aus dem PDF (Vektoren, ../dl/pdf_strassen.json) an OSM ausrichten, erst global, dann je
# 700-m-Zelle eine Verschiebung (die Karte ist generalisiert, örtlich bis ~60 m versetzt, z. B. am Olympiasee)
S_ = np.array(json.load(open("../dl/pdf_strassen.json")), float); S_[:, 1] = -S_[:, 1]
for rad in (40, 25, 15, 15):
    X = s * S_ @ Rm.T + t; d, i = tree.query(X); ok = d < rad; s, Rm, t = umeyama(S_[ok], road[i[ok]])
X = s * S_ @ Rm.T + t; CELL = 700
gx = np.arange(X[:, 0].min(), X[:, 0].max() + CELL, CELL); gy = np.arange(X[:, 1].min(), X[:, 1].max() + CELL, CELL)
OFF = np.zeros((len(gx), len(gy), 2)); N_ = np.zeros((len(gx), len(gy)))
for a_ in range(len(gx)):
    for b_ in range(len(gy)):
        m = (abs(X[:, 0] - gx[a_]) < CELL) & (abs(X[:, 1] - gy[b_]) < CELL); Xc = X[m]
        if len(Xc) < 300: continue
        off = np.zeros(2)
        for rad in (50, 30, 20, 15):
            d, i = tree.query(Xc + off); ok = d < rad
            if ok.sum() < 150: break
            off += np.median(road[i[ok]] - (Xc[ok] + off), axis=0)
        OFF[a_, b_] = off; N_[a_, b_] = len(Xc)
def off_at(Y):   # bilinear zwischen den Zellmitten
    fx = np.clip((Y[:, 0] - gx[0]) / CELL, 0, len(gx) - 1.001); fy = np.clip((Y[:, 1] - gy[0]) / CELL, 0, len(gy) - 1.001)
    i0, j0 = fx.astype(int), fy.astype(int); u_, v_ = (fx - i0)[:, None], (fy - j0)[:, None]
    return OFF[i0, j0] * (1 - u_) * (1 - v_) + OFF[i0 + 1, j0] * u_ * (1 - v_) + OFF[i0, j0 + 1] * (1 - u_) * v_ + OFF[i0 + 1, j0 + 1] * u_ * v_
mag = np.hypot(OFF[..., 0], OFF[..., 1])[N_ > 0]; print(f"Zellen {int((N_ > 0).sum())}, örtliche Verschiebung Median {np.median(mag):.1f} m, max {mag.max():.1f} m")
X = s * P @ Rm.T + t; X = X + off_at(X); XQ = s * Q @ Rm.T + t; d, _ = tree.query(XQ + off_at(XQ))
lat, lon = unmerc(X)
L = sum(2 * 6371008.8 * math.asin(math.sqrt(math.sin(math.radians(lat[j+1]-lat[j]) / 2) ** 2 + math.cos(math.radians(lat[j])) * math.cos(math.radians(lat[j+1])) * math.sin(math.radians(lon[j+1]-lon[j]) / 2) ** 2)) for j in range(len(lat) - 1))
print(f"Start {start}, Maßstab {s/k:.3f} m/pt, Drehung {math.degrees(math.atan2(Rm[1,0], Rm[0,0])):.2f}°, Abstand zur Straße: Median {np.median(d):.1f} m, 90 % {np.percentile(d, 90):.1f} m, max {d.max():.0f} m, Länge {L/1000:.3f} km")
json.dump({"lat": lat.tolist(), "lon": lon.tolist(), "s": s, "R": Rm.tolist(), "t": t.tolist(), "k": k}, open("../dl/strecke_georef.json", "w"))
