# Streckenplan 2026 des Veranstalters (Seite „赛事路线图“ Nr. 3289, veröffentlicht bis 25.11.2026; Rasterbild 5686 × 7885 px,
# ../dl/bilder/5Inp4haCyXKZme35.jpg) auf den Plan 2025 eingepasst, damit die Georeferenz des Plans 2025 (georef.json) auch für 2026 gilt:
#   blaue Linienpixel wie plan.py, dann Ähnlichkeitsabbildung 2026-Pixel -> 2025-Pixel (Maßstab, Drehung, Verschiebung) per ICP gegen
#   ../dl/plan_blau.npy, nur über den Teil bis km 15 (Kurs dort unverändert) und mit Abschneiden großer Abstände.
#   -> ../dl/plan2026_blau.npy (2026-Pixel in 2025-Pixel umgerechnet, jedes 3. Pixel) und plan2026.json (Abbildung, Restfehler).
# Nur zum Nachzeichnen und für die Kontrolle (karte_pruefen.py mit Plan 2026), die Linie selbst baut linie.py aus OSM-Straßen.
import json
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from scipy.spatial import cKDTree
Image.MAX_IMAGE_PIXELS = None
A = np.asarray(Image.open("../dl/bilder/5Inp4haCyXKZme35.jpg").convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
blau = (R < 90) & (G > 85) & (G < 150) & (B > 150) & (B - R > 100)
# große zusammenhängende Flächen (Linie samt Kreisen), keine Schrift und Symbole
# (der blaue Verlauf am Rand des Plakats hat dieselbe Farbe: nur die größte Fläche, die den Bildrand nicht berührt)
lab, n = nd.label(nd.binary_dilation(blau, iterations=2)); gr = nd.sum(np.ones_like(lab), lab, range(1, n + 1)); sl = nd.find_objects(lab)
innen = [k for k in range(1, n + 1) if sl[k - 1][0].start > 0 and sl[k - 1][1].start > 0 and sl[k - 1][0].stop < A.shape[0] and sl[k - 1][1].stop < A.shape[1]]
linie = max(innen, key=lambda k: gr[k - 1])
ys, xs = np.where(blau & (lab == linie)); P26 = np.c_[xs, ys][::3].astype(float)
P25 = np.load("../dl/plan_blau.npy").astype(float)
# Anfang: gleiche Kartenbreite angenommen, Lage über km 1 (aus dem Vergleich der Vorschaubilder)
s, th, t = 4739 / 5686, 0.0, np.array([71.0, -19.0])
def abb(p, s, th, t): c, si = np.cos(th), np.sin(th); return s * (p @ np.array([[c, si], [-si, c]])) + t
# nur der unveränderte Nordteil (2025-Pixel: oberhalb von km 15, y < 0,52 × Höhe)
nord25 = P25[P25[:, 1] < 0.52 * 6571]; baum = cKDTree(nord25)
for it in range(40):
    Q = abb(P26, s, th, t); sel = Q[:, 1] < 0.50 * 6571
    d, j = baum.query(Q[sel]); grenze = max(6.0, np.percentile(d, 80)); ok = d < grenze
    a, b = P26[sel][ok], nord25[j[ok]]
    ma, mb = a.mean(0), b.mean(0); a0, b0 = a - ma, b - mb
    za, zb = a0[:, 0] + 1j * a0[:, 1], b0[:, 0] + 1j * b0[:, 1]; k = (np.conj(za) @ zb) / (np.conj(za) @ za)
    s, th = abs(k), -np.angle(k); t = mb - abb(ma[None], s, th, np.zeros(2))[0]
Q = abb(P26, s, th, t); d, _ = cKDTree(nord25).query(Q[Q[:, 1] < 0.50 * 6571])
print(f"Maßstab {s:.5f}, Drehung {np.degrees(th):.3f}°, Verschiebung {t.round(1)}; Nordteil Abstand Median {np.median(d):.1f} px, 90 % {np.percentile(d, 90):.1f} px")
np.save("../dl/plan2026_blau.npy", Q.astype(np.float32))
json.dump({"s": s, "th": th, "t": t.tolist(), "median_px": float(np.median(d)), "p90_px": float(np.percentile(d, 90))}, open("plan2026.json", "w"), indent=1)
