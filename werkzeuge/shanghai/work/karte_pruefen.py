# Nur zur Kontrolle: Ausschnitt mit den OSM-Straßen (chinesische Namen), der eingepassten blauen Linie des Plans (hellblau), den
# Kilometerkreisen (rot) und – falls vorhanden – der gebauten Linie (rot) als Bild.
# Aufruf: python3 karte_pruefen.py <lat> <lon> <Breite in m> <Ausgabe.png>
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from geo import utm, osm
la, lo, B, aus = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
cx, cy = (float(v) for v in utm(la, lo)); sc = 1400 / B
M = np.array(json.load(open("georef.json"))["M"]); P = json.load(open("plan2025.json"))
def ab(p): return np.asarray(p, float) @ M[:2] + M[2]
im = Image.new("RGB", (1400, 1400), (255, 255, 255)); d = ImageDraw.Draw(im)
f = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 15)
def px(q): q = np.atleast_2d(q); return list(zip((q[:, 0] - cx) * sc + 700, (cy - q[:, 1]) * sc + 700))
N, W, _ = osm()
BL = np.load("../dl/plan_blau.npy").astype(float); X = ab(BL)
sel = (np.abs(X[:, 0] - cx) < B * 0.6) & (np.abs(X[:, 1] - cy) < B * 0.6)
for p in px(X[sel]): d.point(p, fill=(140, 190, 255))
texte = []
for wid, (tg, refs) in W.items():
    hw = tg.get("highway")
    if not hw or hw in ("steps", "corridor", "elevator"): continue
    ll = np.array([N[r] for r in refs if r in N])
    if len(ll) < 2: continue
    x, y = utm(ll[:, 0], ll[:, 1]); q = np.c_[x, y]
    if not ((np.abs(q[:, 0] - cx) < B * 0.6) & (np.abs(q[:, 1] - cy) < B * 0.6)).any(): continue
    col = (120, 120, 120)
    if hw in ("motorway", "motorway_link") or "高架" in tg.get("name", ""): col = (240, 150, 150)
    elif tg.get("tunnel") not in (None, "no"): col = (200, 160, 60)
    elif hw in ("service", "cycleway", "footway", "path", "pedestrian"): col = (60, 170, 90) if hw in ("footway", "path", "pedestrian") else (200, 200, 200)
    d.line(px(q), fill=col, width=3 if hw in ("trunk", "primary", "secondary") else 1)
    if tg.get("name"): texte.append((px(q[len(q) // 2])[0], tg["name"], col))
for (u, v), t, col in texte: d.text((u + 2, v + 2), t, fill=(60, 60, 60) if col == (120, 120, 120) else col, font=f)
for k, v in P["km"].items():
    u, w = px(ab(v[:2]))[0]; d.ellipse((u - 5, w - 5, u + 5, w + 5), outline=(220, 0, 0), width=2); d.text((u + 6, w - 8), k, fill=(220, 0, 0), font=f)
if os.path.exists("linie2025.json"):
    L = json.load(open("linie2025.json")); ll = np.array(L["pts"]); x, y = utm(ll[:, 0], ll[:, 1]); d.line(px(np.c_[x, y]), fill=(230, 30, 30), width=2)
im.save(aus); print(aus)
