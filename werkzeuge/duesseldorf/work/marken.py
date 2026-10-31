# Nur Abgleich: Kilometerschilder des Streckenplans (42 Kästen „N km“, plan_pdf.json) gegen die gleichmäßig gestreckte Linie.
# Die Kästen stehen 15–40 pt (60–160 m) neben der Linie, ohne Strich zur Stelle; gemessen wird der Lotfußpunkt der Kastenmitte. Wo
# mehrere Durchgänge in Reichweite liegen, gilt der nächste zum erwarteten km (Zuordnung der Reihe nach, km 1 bis 42).
import json
import numpy as np
pl = json.load(open("plan_pdf.json")); P = np.array(pl["pts"]); U = np.array(json.load(open("georef.json"))["plan"])
S = np.r_[0, np.cumsum(np.hypot(*np.diff(U, axis=0).T))]; S *= 42195 / S[-1]
def kand(x, y):
    q = np.array([x, y]); a = P[:-1]; b = P[1:]; v = b - a
    t = np.clip(((q - a) * v).sum(1) / np.maximum((v * v).sum(1), 1e-9), 0, 1); Q = a + t[:, None] * v
    d = np.hypot(*(Q - q).T); s = S[:-1] + t * np.diff(S)
    return s[d < d.min() + 20]
K = [kand(x, y) for x, y, _, _ in pl["km"]]
frei, ab = set(range(len(K))), []
for km in range(1, 43):
    best = min(((abs(K[i] - km * 1000).min(), i) for i in frei), default=None)
    if best is None or best[0] > 300: print(f"km {km}: kein Schild in Reichweite"); continue
    i = best[1]; frei.discard(i); s = K[i][np.argmin(abs(K[i] - km * 1000))]; ab.append(s - km * 1000)
ab = np.array(ab)
print(f"{len(ab)} Schilder: Abweichung Median {np.median(ab):+.0f} m, |Abweichung| Median {np.median(abs(ab)):.0f} m, 90 % {np.percentile(abs(ab), 90):.0f} m, "
      f"max {abs(ab).max():.0f} m; km 1–10 {np.median(ab[:10]):+.0f}, 11–21 {np.median(ab[10:21]):+.0f}, 22–31 {np.median(ab[21:31]):+.0f}, 32–42 {np.median(ab[31:]):+.0f} m")
print("übrig:", len(frei), "Kasten (ohne km-Zuordnung)")
