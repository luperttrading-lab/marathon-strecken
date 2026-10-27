# Örtlicher Versatz der PDF-Karte gegenüber OSM, gemessen an Wasserflächen: PDF-Seen und Flüsse (transformiert) gegen
# die Wasserfarbe der OSM-Kacheln (Zoom 16), beste Verschiebung per Kreuzkorrelation.
import json, math, os, urllib.request
import numpy as np
from PIL import Image, ImageDraw
G = json.load(open("../dl/strecke_georef.json")); s, Rm, t = G["s"], np.array(G["R"]), np.array(G["t"]); R = 6378137.0
rings = [np.array(p, float) for p in json.load(open("../dl/pdf_wasserflaechen.json"))]
def tomerc(P): P = P.copy(); P[:, 1] = -P[:, 1]; return s * P @ Rm.T + t
def px(lat, lon, z):
    n = 256 * 2 ** z; return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
def merc2px(X, z):
    n = 256 * 2 ** z; return np.c_[(X[:, 0] / (2 * math.pi * R) + 0.5) * n, (0.5 - X[:, 1] / (2 * math.pi * R)) * n]
Z = 16
def versatz(lat, lon, half=700):
    m = half / (6371008.8 * math.cos(math.radians(lat))) * 180 / math.pi * 1.0; dl = half / 111320
    x0, y1 = px(lat - dl, lon - m, Z); x1, y0 = px(lat + dl, lon + m, Z); tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256; im = Image.new("RGB", (W, H))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            f = f"/tmp/muc/t{Z}_{tx}_{ty}.png"
            if not os.path.exists(f): open(f, "wb").write(urllib.request.urlopen(urllib.request.Request(f"https://tile.openstreetmap.org/{Z}/{tx}/{ty}.png", headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=30).read())
            im.paste(Image.open(f).convert("RGB"), ((tx - tx0) * 256, (ty - ty0) * 256))
    A = np.asarray(im).astype(int); osm = (np.abs(A - [170, 211, 223]).max(2) < 8).astype(float)
    mk = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(mk)
    for r in rings:
        p = merc2px(tomerc(r), Z) - [tx0 * 256, ty0 * 256]
        if p[:, 0].max() < 0 or p[:, 0].min() > W or p[:, 1].max() < 0 or p[:, 1].min() > H: continue
        dr.polygon([tuple(q) for q in p], fill=255)
    pdf = np.asarray(mk) > 0
    if pdf.sum() < 500 or osm.sum() < 500: return None
    F = np.fft.fft2(osm) * np.conj(np.fft.fft2(pdf.astype(float))); C = np.real(np.fft.ifft2(F))
    lim = 160; C2 = np.full_like(C, -1)
    for dy in range(-lim, lim + 1, 1): pass
    yy, xx = np.meshgrid(np.r_[0:lim + 1, H - lim:H], np.r_[0:lim + 1, W - lim:W], indexing="ij"); C2[yy, xx] = C[yy, xx]
    iy, ix = np.unravel_index(np.argmax(C2), C2.shape); dy = iy if iy <= H // 2 else iy - H; dx = ix if ix <= W // 2 else ix - W
    mpp = 2 * math.pi * R / (256 * 2 ** Z)   # Mercator-Meter je Pixel
    ov0 = (osm * pdf).sum() / pdf.sum(); ov1 = C2.max() / pdf.sum()
    return dx * mpp, -dy * mpp, ov0, ov1, int(pdf.sum()), mpp * math.cos(math.radians(lat))
for name, lat, lon in [("Olympiasee", 48.1705, 11.5510), ("Kleinhesseloher See", 48.1585, 11.5985), ("Englischer Garten Süd/Eisbach", 48.1460, 11.5900), ("Isar Praterinsel", 48.1375, 11.5900), ("Isar Deutsches Museum", 48.1305, 11.5845), ("Isar Tivoli", 48.1510, 11.6020)]:
    r = versatz(lat, lon)
    if r: print(f"{name:30s} Versatz Ost {r[0] * r[5] / (2 * math.pi * R / (256 * 2 ** Z)):+6.0f} m, Nord {r[1] * r[5] / (2 * math.pi * R / (256 * 2 ** Z)):+6.0f} m   Deckung vorher {r[2]:.2f} nachher {r[3]:.2f}  ({r[4]} px)")
    else: print(name, "zu wenig Wasser")

# Passpunkte über die ganze Karte: Mitte jeder Region (Mercator) -> + gemessener Versatz; daraus eine neue Ähnlichkeit
def merc_ll(lat, lon): return np.array([R * math.radians(lon), R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))])
REG = [("Olympiasee", 48.1705, 11.5510), ("Kleiner Olympiasee", 48.1695, 11.5440), ("Kleinhesseloher See", 48.1585, 11.5985), ("Englischer Garten Eisbach", 48.1460, 11.5900),
       ("Isar Praterinsel", 48.1375, 11.5900), ("Isar Deutsches Museum", 48.1305, 11.5845), ("Isar Tivoli", 48.1510, 11.6020), ("Isar Reichenbachbrücke", 48.1235, 11.5770),
       ("Isar Wittelsbacherbrücke", 48.1175, 11.5640), ("Isar Föhring", 48.1650, 11.6100), ("Schwabinger Bach", 48.1700, 11.6000), ("Nymphenburger Kanal Ost", 48.1640, 11.5600)]
src, dst, wt = [], [], []
for name, lat, lon in REG:
    r = versatz(lat, lon)
    if not r or r[3] < 0.5: print(name, "übersprungen", r and round(r[3], 2)); continue
    M = merc_ll(lat, lon); P = np.linalg.solve(s * Rm, M - t); P[1] = -P[1]   # PDF-Punkt (pt) an der Regionsmitte
    src.append([P[0], -P[1]]); dst.append(M + [r[0], r[1]]); wt.append(r[3])
    print(f"{name:28s} Ost {r[0] * math.cos(math.radians(lat)):+5.0f} m, Nord {r[1] * math.cos(math.radians(lat)):+5.0f} m, Deckung {r[2]:.2f} -> {r[3]:.2f}")
src, dst = np.array(src), np.array(dst)
def umeyama(src, dst):
    ms, md = src.mean(0), dst.mean(0); A, B = src - ms, dst - md
    U, S_, Vt = np.linalg.svd(B.T @ A / len(src)); D = np.eye(2)
    if np.linalg.det(U @ Vt) < 0: D[1, 1] = -1
    Rr = U @ D @ Vt; ss = np.trace(np.diag(S_) @ D) / (A ** 2).sum(1).mean(); return ss, Rr, md - ss * Rr @ ms
s2, R2, t2 = umeyama(src, dst); res = dst - (s2 * src @ R2.T + t2); k = 1 / math.cos(math.radians(48.15))
print(f"neue Ähnlichkeit: Maßstab {s2 / k:.4f} m/pt (vorher {s / k:.4f}), Drehung {math.degrees(math.atan2(R2[1, 0], R2[0, 0])):.3f}°, Restfehler je Passpunkt (m):", np.round(np.hypot(*res.T) / k, 0))
json.dump({"s": s2, "R": R2.tolist(), "t": t2.tolist(), "pass": len(src)}, open("../dl/fit_wasser.json", "w"))
