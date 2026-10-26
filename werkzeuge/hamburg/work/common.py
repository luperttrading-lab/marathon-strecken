import json, numpy as np
kmp = json.load(open("kmproj.json"))
g = json.load(open("gpx2026.json")); GL = g["d"][-1]
anc = [(0.0, 0.0)] + sorted([(v[0], int(k.split()[1])*1000.0) for k, v in kmp.items() if k.startswith("KM")]) + [(GL, 42195.0)]
A_s = np.array([a[0] for a in anc]); A_k = np.array([a[1] for a in anc])
def official(s): return np.interp(s, A_s, A_k)
def gpx_of(k): return np.interp(k, A_k, A_s)
