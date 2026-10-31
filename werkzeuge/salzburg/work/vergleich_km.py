# Nur Abgleich: Wo lägen Kilometermarken, Staffelzonen und Verpflegung der Google-Karte nach der Zuordnung über die Ideallinie
# (ideal_<w>.json, gestreckt auf 42 195 m)? Aufruf: python3 vergleich_km.py <w>
import json, sys, numpy as np
w = sys.argv[1]
I = json.load(open(f"ideal_{w}.json")); lm = np.array(I["lm"]); ia = np.array(I["ideal"]); f = 42195 / ia[-1]
def off(x): return float(np.interp(x, lm, ia)) * f
M = json.load(open("marken.json"))
print(f"w = {w}: Ideallinie {ia[-1]:.1f} m, Faktor {f:.5f}")
d = []
for km, s, e in M["km"]:
    o = off(s); d.append(o - km * 1000); print(f"  KM {km:2d}: {o / 1000:7.3f}  ({o - km * 1000:+5.0f} m)")
d = np.array(d); print(f"  Kilometermarken: Abweichung Median {np.median(d):+.0f} m, Mittel {d.mean():+.0f}, Spanne {d.min():+.0f} … {d.max():+.0f}, |d| 90 % bis {np.percentile(np.abs(d), 90):.0f}")
for km, s, e, n, *_ in M["punkte"]: print(f"  {n:40s} Plan {km:6.2f}  hier {off(s) / 1000:7.3f}  ({off(s) - km * 1000:+5.0f} m)")
