import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); h = np.array([np.nan if x[3] is None else x[3] for x in r])
print("fehlend:", np.isnan(h).sum(), "min", np.nanmin(h), "max", np.nanmax(h))
k = official(s)
# lokale Steigung 10 m
dh = np.diff(h); ds = np.diff(k)
g = dh/ds*100
# Sprünge > 8 % über 10 m
idx = np.where(np.abs(g) > 8)[0]
groups = []
for i in idx:
    if groups and i - groups[-1][-1] <= 15: groups[-1].append(i)
    else: groups.append([i])
for gr in groups:
    a, b = max(gr[0]-5, 0), min(gr[-1]+6, len(h)-1)
    print(f"km {k[a]/1000:6.2f}-{k[b]/1000:6.2f}  h: " + " ".join(f"{v:.1f}" for v in h[a:b+1]))
