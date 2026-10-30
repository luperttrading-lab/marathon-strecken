# Höhenmodelle gegen die Höhenkurve des Veranstalters (planprofil.json) -> vergleich.json, ../dl/vergleich.png
# Modelle: Copernicus GLO-30 (Oberflächenmodell, TanDEM-X 2011–2015) und SRTM 1″ (Radar 2000, ebenfalls Oberfläche; Kachel
# N40E117 aus den AWS Terrain Tiles, elevation-tiles-prod/skadi, ohne Anmeldung). Beide alle 10 m entlang der Linie, Kilometer nach
# common.py. Höhenmeter wie in der App: Steigung über ein Fenster (50 / 200 m / 1 km), Summe der positiven Anteile.
import json
import numpy as np
from common import official
from dgm import lade, abtasten
R = np.array(json.load(open("dgm_cop30_10m.json"))); s = R[:, 0]; lat = R[:, 1]; lon = R[:, 2]
k = official(s) / 1000
mod = {"Copernicus GLO-30": R[:, 3]}
raw = np.fromfile("../dl/dem/N40E117.hgt", ">i2").reshape(3601, 3601).astype(float)
# .hgt: Zeile 0 = 41° N, Spalte 0 = 117° O, Punkte auf den Bogensekunden (Pixelmitte = Gitterpunkt)
mod["SRTM 1″"] = abtasten(raw, 117.0, 41.0, 1 / 3600, 1 / 3600, lat, lon, mitte=False)
PP = np.array(json.load(open("planprofil.json"))); org = np.interp(k, PP[:, 0], PP[:, 1])
grid = np.arange(0, 42.195, 0.01)
def auf(k, h): return np.interp(grid, k, h)
def hm(h, w):
    n = int(round(w / 10)); hh = np.r_[np.full(n // 2, h[0]), h, np.full(n // 2, h[-1])]
    g = (hh[n:] - hh[:-n])[: len(h)]
    return g[g > 0].sum() * 10 / w, -g[g < 0].sum() * 10 / w
res = {}
for name, h in list(mod.items()) + [("Veranstalter", org)]:
    hg = auf(k, h)
    r = {"start": hg[0], "ziel": hg[-1], "min": hg.min(), "km_min": grid[hg.argmin()], "max": hg.max(), "km_max": grid[hg.argmax()]}
    for w in (10, 50, 200, 1000): r[f"auf{w}"], r[f"ab{w}"] = hm(hg, w)
    if name != "Veranstalter":
        og = auf(k, org); dd = hg - og
        r["median_diff"] = float(np.median(dd)); r["mad"] = float(np.median(np.abs(dd - np.median(dd)))); r["korr"] = float(np.corrcoef(hg, og)[0, 1])
    res[name] = {a: round(float(b), 3) for a, b in r.items()}
    print(f"{name:18s} Start {r['start']:5.0f}  Ziel {r['ziel']:5.0f}  min {r['min']:5.0f} (km {r['km_min']:4.1f})  max {r['max']:5.0f} (km {r['km_max']:4.1f})  "
          f"↑ 10 m {r['auf10']:5.0f} · 50 m {r['auf50']:5.0f} · 200 m {r['auf200']:5.0f} · 1 km {r['auf1000']:5.0f}" +
          (f"  gegen Veranstalter: Median {r['median_diff']:+.1f} m, MAD {r['mad']:.1f} m, Korrelation {r['korr']:.3f}" if "korr" in r else ""))
json.dump(res, open("vergleich.json", "w"), ensure_ascii=False, indent=1)
try:
    from PIL import Image, ImageDraw, ImageFont
    Wd, Hd = 2400, 700; im = Image.new("RGB", (Wd, Hd), "white"); dr = ImageDraw.Draw(im); f = ImageFont.load_default(size=16)
    def px(km_, h_): return [(40 + a / 42.2 * (Wd - 60), Hd - 30 - (b - 180) / 360 * (Hd - 60)) for a, b in zip(km_, h_)]
    for hh in range(200, 541, 50): y = px([0], [hh])[0][1]; dr.line([(40, y), (Wd - 20, y)], fill=(225, 225, 225)); dr.text((2, y - 8), str(hh), fill="black", font=f)
    for kk in range(0, 43, 2): x = px([kk], [0])[0][0]; dr.line([(x, 20), (x, Hd - 30)], fill=(235, 235, 235)); dr.text((x - 6, Hd - 26), str(kk), fill="black", font=f)
    dr.line(px(grid, auf(k, org)), fill=(0, 0, 0), width=3)
    for (name, h), col in zip(mod.items(), [(220, 60, 30), (30, 120, 220)]): dr.line(px(grid, auf(k, h)), fill=col, width=2)
    dr.text((60, 25), "schwarz: Veranstalter · rot: Copernicus GLO-30 · blau: SRTM 1″", fill="black", font=f)
    im.save("../dl/vergleich.png")
except Exception as e: print("Bild:", e)
