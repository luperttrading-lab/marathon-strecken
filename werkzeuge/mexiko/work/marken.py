# Kilometermarken und Getränkestellen aus dem Streckenplan 2026 des Veranstalters (../dl/ruta-maraton-cdmx-2026.jpg, 1200 × 795 px,
# Pressebild von media.dondeir.com; die Karte ist um 90° gedreht, Norden rechts). Der Plan hat keine Koordinaten: Er wird affin auf
# die Linie (gpx2026.json) eingepasst (ICP: Pixel der dunkelblauen Streckenlinie gegen die Linie, Startwerte aus fünf Passpunkten:
# Glorieta de Insurgentes, Fuente de Cibeles, Ángel de la Independencia, Monumento a la Revolución, Zócalo). Danach die Kreise:
# dunkeltürkis mit weißer Zahl = Kilometer 5, 10 … 40 (dort auch Electrolit), hellgrün = Getränkestelle „Agua Skarch“ bei 2,5, 7,5 …
# 37,5 km. Jeder Kreis wird auf die Linie projiziert, in einem Fenster um die erwartete Stelle (km × Linienlänge / 42,195 ± 1,5 km);
# wo die Strecke mehrmals vorbeikommt (Masaryk hin und zurück), gilt unter den Stellen bis 40 m über dem kleinsten Abstand die
# nächste zur erwarteten. Die Marke 42 sitzt neben der Strecke (Zeiger) und wird nicht verwendet. -> marken.json
import json, numpy as np
from PIL import Image
from pyproj import Transformer
from scipy import ndimage
from scipy.spatial import cKDTree
T = Transformer.from_crs(4326, 32614, always_xy=True)
a = np.asarray(Image.open("../dl/ruta-maraton-cdmx-2026.jpg").convert("RGB")).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
linie = (r < 175) & (b - r >= 4) & (b >= g) & (r + g + b < 500); linie[600:, :700] = False   # ohne Legende und Profil
yy, xx = np.nonzero(linie); MP = np.c_[xx, yy].astype(float); baum = cKDTree(MP)
G = json.load(open("gpx2026.json")); d = np.array(G["d"]); P = np.array([p[:2] for p in G["pts"]]); L = d[-1]
ss = np.arange(0, L, 10.0); Q = np.c_[T.transform(np.interp(ss, d, P[:, 1]), np.interp(ss, d, P[:, 0]))]
PASS = {"px": [[945.8, 402.5], [908, 367.5], [980.8, 354.2], [1076.5, 483], [1031.2, 687.5]],
        "geo": [[19.42355, -99.16300], [19.42002, -99.16631], [19.42700, -99.16767], [19.43617, -99.15462], [19.43260, -99.13320]]}
geo = np.array([T.transform(lo, la) for la, lo in PASS["geo"]])
A, *_ = np.linalg.lstsq(np.c_[geo, np.ones(len(geo))], np.array(PASS["px"], float), rcond=None)      # UTM -> Pixel
for _ in range(40):
    dist, j = baum.query(np.c_[Q, np.ones(len(Q))] @ A); ok = dist < np.percentile(dist, 80)
    A, *_ = np.linalg.lstsq(np.c_[Q[ok], np.ones(ok.sum())], MP[j[ok]], rcond=None)
dist, j = baum.query(np.c_[Q, np.ones(len(Q))] @ A)
B, *_ = np.linalg.lstsq(np.c_[MP[j], np.ones(len(j))], Q, rcond=None)                                 # Pixel -> UTM
print(f"Plan auf Linie: Abstand Median {np.median(dist):.1f} px, 90 % {np.percentile(dist, 90):.1f} px; Maßstab {np.sqrt(abs(np.linalg.det(B[:2]))):.1f} m/px")
def kreise(maske, n_min, n_max):
    lab, n = ndimage.label(ndimage.binary_closing(maske, iterations=2)); out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if n_min <= len(xs) <= n_max and np.ptp(xs) <= 18 and np.ptp(ys) <= 18: out.append((xs.mean(), ys.mean(), len(xs)))
    return out
km_k = kreise((r < 110) & (g > 70) & (g < 150) & (b > 70) & (b < 150) & (abs(g - b) < 30) & (g > r + 15), 25, 200)
wa_k = kreise((g > r + 45) & (g > b + 25) & (g > 120) & (r < 140), 60, 120)
# Kilometerkreise mit zweistelliger Zahl zerfallen an der Zahl in zwei Teile: Teile näher als 12 px zusammenfassen
def zusammen(ks):
    ks = sorted(ks); out = []
    for k in ks:
        for o in out:
            if np.hypot(o[0] - k[0], o[1] - k[1]) < 12: o[0] = (o[0] * o[2] + k[0] * k[2]) / (o[2] + k[2]); o[1] = (o[1] * o[2] + k[1] * k[2]) / (o[2] + k[2]); o[2] += k[2]; break
        else: out.append(list(k))
    return out
km_k = [k for k in zusammen(km_k) if 80 <= k[2] <= 200]
def auf_linie(px, py, erwartet):
    e, n = np.r_[px, py, 1] @ B
    sel = np.abs(ss - erwartet) <= 1500; dd = np.hypot(Q[sel, 0] - e, Q[sel, 1] - n); s = ss[sel]
    nah = dd <= dd.min() + 40; i = np.argmin(np.where(nah, np.abs(s - erwartet), np.inf))
    return float(s[i]), float(dd[i])
def zuordnen(ks, kms):
    out = []
    for km in kms:
        erw = km * 1000 * L / 42195
        best = min(ks, key=lambda k: auf_linie(k[0], k[1], erw)[1] + abs(auf_linie(k[0], k[1], erw)[0] - erw) / 10)
        s, dd = auf_linie(best[0], best[1], erw); out.append([km, round(s, 1), round(dd, 1), round(best[0], 1), round(best[1], 1)])
    return out
marken = {"km": zuordnen(km_k, [5, 10, 15, 20, 25, 30, 35, 40]),
          "verpflegung": [m + ["Agua Skarch"] for m in zuordnen(wa_k, [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5])]}
json.dump(marken, open("marken.json", "w"), indent=0, ensure_ascii=False)
print("km-Kreise (km, Linienmeter, Abstand zur Linie, Pixel):"); [print("  ", m) for m in marken["km"]]
print("Getränkestellen:"); [print("  ", m) for m in marken["verpflegung"]]
