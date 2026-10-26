from PIL import Image
import numpy as np, json
im = np.asarray(Image.open("/root/.claude/uploads/805a3bc9-e74c-5887-8311-58844dad1e09/291eb48a-image.jpg").convert("RGB")).astype(float)
R,G,B = im[...,0], im[...,1], im[...,2]
X0, PXKM = 77.0, (249-77)/6.9
def km2x(k): return X0 + PXKM*k
W = im.shape[1]
h = np.full(W, np.nan)
for x in range(78, 1130):
    col = slice(245, 272)
    r, g, b = R[col, x], G[col, x], B[col, x]
    isred = (r > 180) & (r - g > 40)
    a = np.clip((255 - g)/(255 - 6), 0, 1) * isred
    h[x] = a.sum()
# Spalten mit senkrechten Linien/Markern verwerfen (dunkel oder blau)
bad = set()
for x in range(78, 1130):
    seg = im[240:272, x]
    if (seg[:,0] < 120).any() or ((seg[:,2] > seg[:,0] + 30)).any(): bad.update(range(x-2, x+3))
xs = np.arange(W); good = np.array([(x not in bad) and 78 <= x < 1130 for x in xs])
hi = np.interp(xs, xs[good], h[good])
labels = [(0,20),(6.9,32),(11.3,7),(12.3,6),(13.1,2),(16.3,7),(21.098,9),(27.7,17),(30.7,12),(32.7,8),(37.1,12),(38.2,11),(42.195,20)]
H = []
for k, m in labels:
    x = int(round(km2x(k))); x = min(max(x, 79), 1128)
    H.append(np.mean(hi[x-3:x+4]))
H = np.array(H); M = np.array([m for _, m in labels])
A = np.vstack([np.ones_like(H), H]).T
coef, *_ = np.linalg.lstsq(A, M, rcond=None)
pred = A @ coef
print("Meter = %.2f + %.2f * px" % tuple(coef))
for (k, m), hp, p in zip(labels, H, pred): print(f"km {k:6.2f} Bild {m:3d} m  px {hp:5.2f}  Fit {p:5.1f}  Rest {m-p:+5.1f}")
print("RMSE", np.sqrt(np.mean((M-pred)**2)))
km = (xs - X0)/PXKM; sel = (km >= 0) & (km <= 42.195)
json.dump({"km": km[sel].tolist(), "m": (coef[0] + coef[1]*hi[sel]).tolist()}, open("bild_digit.json", "w"))
