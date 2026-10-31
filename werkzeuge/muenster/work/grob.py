# Grobe Einpassung des Streckenplans (PDF-Punkte -> ETRS89/UTM 32N), nur als Ausgang für osm.py und georef.py: Beschriftungen
# bekannter Orte im Kartengrund (Mitte des Worts in PDF-Punkten) gegen ihre Lage in OSM (Nominatim-Suche, eine Abfrage je Sekunde,
# Antworten in ../dl/nominatim/). Eine Beschriftung steht neben oder auf dem Ort, also nur auf 50–150 m genau; affin über alle.
# -> grob.json {"M": 3×2-Matrix [x, y, 1] @ M = [E, N], "rest": [Abweichung je Ort in m]}
import json, os, time, urllib.parse, urllib.request
import numpy as np
from pyproj import Transformer
T = Transformer.from_crs(4326, 25832, always_xy=True)
os.makedirs("../dl/nominatim", exist_ok=True)
ORTE = [((886, 606), "Schloss Münster"), ((1009, 629), "St.-Paulus-Dom, Münster"), ((1101, 725), "Münster Hauptbahnhof"),
        ((851, 692), "Zentralfriedhof, Münster"), ((750, 835), "Mühlenhof-Freilichtmuseum, Münster"), ((999, 564), "Buddenturm, Münster"),
        ((761, 401), "Eissporthalle Steinfurter Straße, Münster"), ((878, 27), "Lepramuseum, Münster"),
        ((1026, 669), "Kunstmuseum Pablo Picasso, Münster"), ((844, 604), "Botanischer Garten, Münster")]
P, Z, namen = [], [], []
for (x, y), q in ORTE:
    f = "../dl/nominatim/" + q.replace(" ", "_").replace(",", "").replace("/", "_") + ".json"
    if not os.path.exists(f):
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1})
        req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial, one-time lookup)"})
        open(f, "wb").write(urllib.request.urlopen(req, timeout=60).read()); time.sleep(1.1)
    r = json.load(open(f))
    if not r: print("nicht gefunden:", q); continue
    E, N = T.transform(float(r[0]["lon"]), float(r[0]["lat"]))
    P.append([x, y, 1]); Z.append([E, N]); namen.append(f'{q} ({r[0]["display_name"][:50]})')
P, Z = np.array(P, float), np.array(Z)
M = np.linalg.lstsq(P, Z, rcond=None)[0]; rest = np.hypot(*(P @ M - Z).T)
for n, r in zip(namen, rest): print(f"{r:6.0f} m  {n}")
print("Maßstab x/y m/pt", np.hypot(*M[0]).round(3), np.hypot(*M[1]).round(3), "Median", round(float(np.median(rest))), "m")
json.dump({"M": M.tolist(), "rest": rest.tolist()}, open("grob.json", "w"))
