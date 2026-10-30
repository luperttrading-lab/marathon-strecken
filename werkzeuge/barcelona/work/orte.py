# Barri und Districte alle 100 m (Linienmeter) über die Rückwärtssuche von Nominatim (OpenStreetMap, zoom 17, Sprache ca; eine
# Abfrage je 1,1 s, Rohantworten in ../dl/nominatim/). In Barcelona steht der Barri unter „quarter“, der Districte unter „suburb“
# (OSM-Grenzen admin_level 10 bzw. 9, gleich den 73 Barris und 10 Districtes der Stadt). Die Flächen der Stadt (Open Data BCN,
# „Unitats administratives“) waren aus dieser Umgebung nicht abrufbar (403). -> orte2026.json [Linienmeter, Barri, Districte]
import json, os, time, urllib.request, urllib.parse
import numpy as np
D = "../dl/nominatim"; os.makedirs(D, exist_ok=True)
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for s in np.arange(0, d[-1], 100.0):
    la, lo = float(np.interp(s, d, P[:, 0])), float(np.interp(s, d, P[:, 1]))
    f = f"{D}/{la:.5f}_{lo:.5f}.json"
    if not os.path.exists(f):
        u = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode({"lat": f"{la:.5f}", "lon": f"{lo:.5f}", "zoom": 17, "format": "jsonv2", "accept-language": "ca"})
        for att in range(6):
            try:
                t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=30).read()
                open(f, "wb").write(t); break
            except Exception as e: print("  Fehler", s, e, flush=True); time.sleep(5 + 10 * att)
        time.sleep(1.1)
    a = json.load(open(f)).get("address", {})
    out.append([float(s), a.get("quarter", ""), a.get("suburb", "")])
    if len(out) % 50 == 0: print(len(out), out[-1], flush=True)
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print("Barris:", [(k, len(list(v)) * 100) for k, v in groupby(o[1] for o in out)])
print("Districtes:", [(k, len(list(v)) * 100) for k, v in groupby(o[2] for o in out)])
