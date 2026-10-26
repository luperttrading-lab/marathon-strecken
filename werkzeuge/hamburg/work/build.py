import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
L = 42195.0; STEP = 10
c = json.load(open("clean.json")); K = json.load(open("kml.json")); kmp = json.load(open("kmproj.json"))
k = np.array(c["k"]); hc = np.array(c["h"])
grid = np.arange(0, 42200 + 1, STEP, dtype=float)
hg = np.interp(np.minimum(grid, L), k, hc)
# gleitender Median über 3 Punkte (30 m)
hm = hg.copy()
for i in range(1, len(hg) - 1): hm[i] = np.median(hg[i-1:i+2])
# Straßen
st = json.load(open("streets2026.json"))
segs, prev = [], None
last_road, last_q = "", ""
for s_gpx, road, q in st:
    road = road or last_road; q = q or last_q
    km_ = float(official(s_gpx))
    if road != prev: segs.append([round(km_), road, q]); prev = road
    last_road, last_q = road, q
# Kennedybrücke-Lücke und Tunnel benennen
for sg in segs:
    pass
# Brücken/Tunnel
bridges = []
for r in c["regions"]:
    nm = r["name"] or "Kennedybrücke"
    if r["b"] - r["a"] > 300: kind, nm = "Tunnel", "Wallringtunnel"
    else: kind = "Brücke"
    bridges.append({"a": round(r["a"]), "b": round(r["b"]), "name": nm, "kind": kind})
# Tunnel als Straßensegment eintragen
tun = [b for b in bridges if b["kind"] == "Tunnel"][0]
segs = [s for s in segs if not (tun["a"] <= s[0] <= tun["b"])]
segs.append([tun["a"], "Wallringtunnel", "Altstadt"]); 
after = [s for s in segs if s[0] > tun["b"]]
segs.append([tun["b"], "Steintorwall", "Altstadt"])
segs.sort(key=lambda s: s[0])
# Wallringtunnel-Einträge aus Nominatim außerhalb des Tunnels umbenennen
for s in segs:
    if s[1] == "Wallringtunnel" and not (tun["a"] - 5 <= s[0] <= tun["b"]): s[1] = "Steintorwall"
# Markierungen
exec(open("proj.py").read().split("km = {}")[0])
def okm(pt, start=0): 
    r = project(pt, start, 150); return float(official(r[0])) if r else None
marks = []
for nm, gt, cs in K["HMH26_Staffelstrecke"]:
    if nm.startswith("Staffelwechsel"): marks.append({"k": round(okm(cs[0])), "s": "Wechsel " + nm.split()[-1], "c": "relay", "n": nm})
for nm, gt, cs in K["HMH26_VPS_WS"]:
    kk = okm(cs[0])
    marks.append({"k": round(kk), "s": "Verpflegung" if nm.startswith("Verpfl") else "Wasser", "c": "food" if nm.startswith("Verpfl") else "water", "n": nm})
marks.append({"k": 21098, "s": "Halbmarathon", "c": "half", "n": "Halbmarathon"})
marks.sort(key=lambda m: m["k"])
data = {"len": L, "step": STEP, "h": [int(round(v * 100)) for v in hm], "streets": segs, "marks": marks, "bridges": bridges}
json.dump(data, open("data.json", "w"), ensure_ascii=False, separators=(",", ":"))
# Kontrollen
def at(x): return float(np.interp(x, grid, hm))
def asc(w):
    xs = grid[grid <= L]; g = np.array([(at(min(x + w/2, L)) - at(max(x - w/2, 0))) / (min(x + w/2, L) - max(x - w/2, 0)) for x in xs])
    dh = (g[1:] + g[:-1]) / 2 * STEP
    return dh[dh > 0].sum(), -dh[dh < 0].sum(), np.abs(g).max() * 100, xs[np.argmax(g)], g.min()*100, xs[np.argmin(g)]
for w in (50, 200, 1000):
    u, d_, gmax, xmax, gmin, xmin = asc(w)
    print(f"Fenster {w:5d} m: ↑ {u:5.1f} m  ↓ {d_:5.1f} m  steilste bergauf {gmax:4.1f} % bei km {xmax/1000:.2f}, bergab {gmin:4.1f} % bei km {xmin/1000:.2f}")
print("Höhe min/max", hm.min(), hm.max(), "Start", at(0), "Ziel", at(L))
print("Straßensegmente", len(segs), "Marken", len(marks))
for m in marks: print(f"  {m['k']/1000:6.2f} {m['n']:28s} {at(m['k']):5.1f} m")
