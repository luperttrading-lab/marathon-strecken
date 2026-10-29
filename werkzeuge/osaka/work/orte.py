# Bezirk (区) alle 100 m (Linienmeter) über den Adressdienst der GSI (mreversegeocoder.gsi.go.jp, Gemeindeschlüssel) -> orte2026.json
import json, time, urllib.request, numpy as np
BEZIRK = {"27102": "Miyakojima", "27103": "Fukushima", "27104": "Konohana", "27106": "Nishi", "27107": "Minato", "27108": "Taishō",
          "27109": "Tennōji", "27111": "Naniwa", "27115": "Higashinari", "27116": "Ikuno", "27117": "Asahi", "27118": "Jōtō",
          "27119": "Abeno", "27122": "Nishinari", "27127": "Kita", "27128": "Chūō"}
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out, unbekannt = [], set()
for s in np.arange(0, d[-1], 100.0):
    la, lo = np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1]); cd = ""
    for att in range(4):
        try:
            r = json.load(urllib.request.urlopen(f"https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat={la:.6f}&lon={lo:.6f}", timeout=20))
            cd = (r.get("results") or {}).get("muniCd", ""); break
        except Exception: time.sleep(2 + 2 * att)
    if cd and cd not in BEZIRK: unbekannt.add(cd)
    out.append([float(s), BEZIRK.get(cd, "")]); time.sleep(0.15)
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print([(k, len(list(v)) * 100) for k, v in groupby(o[1] for o in out)], "unbekannt:", unbekannt)
