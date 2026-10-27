# Linienmeter <-> offizielle Meter: stückweise linear über Start, Meilen- und 5-km-Marken, Halbmarathon und Ziel
import json, numpy as np
kmp = json.load(open("kmproj.json"))
anc = sorted((v[0], v[2]) for v in kmp.values())
A_s = np.array([a[0] for a in anc]); A_k = np.array([a[1] for a in anc])
assert np.all(np.diff(A_s) > 0) and np.all(np.diff(A_k) > 0), "Marken nicht aufsteigend"
def official(s): return np.interp(s, A_s, A_k)
def gpx_of(k): return np.interp(k, A_k, A_s)
