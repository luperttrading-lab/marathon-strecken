# Nur Abgleich: Kilometermarken der dynamischen Karte (marken.json aus parse.py) und die Orte der Getränkestellen und Kontrollen des
# Veranstalters gegen die gleichmäßig gestreckte GPX-Linie (common.py). Die Karte ist von Hand gesetzt: Marken bis 225 m daneben.
import json, numpy as np
from common import official
M = json.load(open("marken.json"))["km"]
ab = np.array([float(official(m[1])) - m[0] * 1000 for m in M]); neu = np.array([m[3] >= "2026" for m in M])
print(f"{len(M)} Marken: offizieller km an der Marke minus Aufschrift Median {np.median(ab):+.0f} m, |Abweichung| Median {np.median(np.abs(ab)):.0f} m, "
      f"90 % {np.percentile(np.abs(ab), 90):.0f} m, höchstens {np.abs(ab).max():.0f} m (km {M[int(np.argmax(np.abs(ab)))][0]:g}); Stand 2026: {neu.sum()} Marken, "
      f"|Abweichung| Median {np.median(np.abs(ab[neu])):.0f} m")
for m, a in zip(M, ab): print(f"  km {m[0]:5.1f}  {a:+6.0f} m  (Stand {m[3]})")
