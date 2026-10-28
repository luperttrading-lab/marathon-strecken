# Linienmeter <-> offizielle Meter. Die Linie (Straßenmitte) ist 1,9 % länger als die vermessene Ideallinie; Chicago hat 37
# Abbiegungen auf breiten Straßen. Geeicht über die Meilen- und 5-km-Marken der offiziellen Karte (kmproj.json, auf ±20 m
# genau gezeichnet): stückweise linear mit Stützstellen alle 5 km Linienmeter, kleinste Quadrate, Ausreißer über 80 m
# (Marken an Wendepunkten, die auf die Gegenrichtung fallen) werden verworfen. Start = 0, Ziel = 42 195.
import json, numpy as np
kmp = json.load(open("kmproj.json")); GL = json.load(open("gpx2026.json"))["d"][-1]
S = np.array([v[0] for v in kmp.values()]); O = np.array([v[2] for v in kmp.values()]); NAMEN = list(kmp)
KN = np.r_[np.arange(0, GL, 5000.0), GL]
def basis(s): return np.array([np.interp(s, KN, np.eye(len(KN))[j]) for j in range(len(KN))]).T
ok = np.ones(len(S), bool)
for _ in range(5):
    B = basis(S[ok]); y = O[ok].copy()
    # Start und Ziel fest: erste und letzte Stützstelle herausnehmen
    y2 = y - B[:, -1] * 42195.0; Bm = B[:, 1:-1]; w, *_ = np.linalg.lstsq(Bm, y2, rcond=None)
    V = np.r_[0.0, w, 42195.0]; res = O - basis(S) @ V
    neu = np.abs(res) <= 80
    if (neu == ok).all(): break
    ok = neu
assert np.all(np.diff(V) > 0)
def official(s): return np.interp(s, KN, V)
def gpx_of(k): return np.interp(k, V, KN)
if __name__ == "__main__":
    for n, s, o, r, k in zip(NAMEN, S, O, res, ok): print(f"{n:8s} Linie {s/1000:7.3f}  offiziell {o/1000:7.3f}  Rest {r:6.0f} m {'' if k else 'verworfen'}")
    print("Faktor je 5 km:", np.round(np.diff(V) / np.diff(KN), 4))
