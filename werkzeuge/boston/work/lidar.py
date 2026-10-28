# Brücken: das Geländemodell misst darunter (Fluss, Gleise, Autobahn). Auf den Spannen gilt die Fahrbahn aus der
# USGS-Punktwolke (deck.py: unteres Zehntel der Punkte im Umkreis von 4 m, die über dem Boden liegen), wo mindestens 100 Punkte
# sie tragen; Lücken linear. Die Spannen stehen ausdrücklich in ZONEN (offizielle km): eine automatische Wahl würde unter
# der Bowker-Überführung (Charlesgate, km 40,9) und unter Bäumen am Commonwealth Avenue die Höhe darüber nehmen.
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json")); s = np.array([x[0] for x in r]); dem = np.array([x[3] for x in r]); k = official(s)
dj = json.load(open("deck.json")); deck = np.array([np.nan if v is None else v for v in dj["deck"]]); n = np.array(dj["n"])
ZONEN = [  # Name, Spanne von, bis (offizielle km)
    ("Union Street über den Sudbury River (Ashland)", 6.29, 6.31),
    ("Union Street über den Sudbury River, zweite Brücke", 6.61, 6.64),
    ("Washington Street über die Route 9 (Wellesley)", 23.80, 23.84),
    ("Washington Street über den Charles River", 25.54, 25.58),
    ("Washington Street über die I-95 / Route 128", 26.18, 26.25),
    ("Washington Street über die Green Line D (Newton)", 27.05, 27.06),
    ("Beacon Street über Mass Pike (I-90) und Bahn", 40.13, 40.27),
    ("Commonwealth Avenue über den Muddy River (Charlesgate)", 40.93, 40.95),
]
h = dem.copy(); src = np.zeros(len(s), int)
at = lambda km: int(np.argmin(np.abs(k - km * 1000)))
for nm, a, b in ZONEN:
    ia, ib = at(a), at(b); ii = np.arange(ia, ib + 1); ok = np.isfinite(deck[ii]) & (n[ii] >= 100)
    assert ok.any(), nm
    h[ii] = np.interp(ii, ii[ok], deck[ii][ok]); src[ii] = 1
    print(f"{nm:55s} km {k[ia]/1000:6.3f}-{k[ib]/1000:6.3f}  Boden davor {dem[ia-1]:5.1f} danach {dem[ib+1]:5.1f}  Fahrbahn {h[ia]:5.1f} … {h[ib]:5.1f}  (Gelände darunter min {dem[ii].min():5.1f})")
json.dump({"h": h.tolist(), "src": src.tolist()}, open("lidar.json", "w"))
