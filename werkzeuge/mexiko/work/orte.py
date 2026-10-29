# Colonia und Alcaldía alle 100 m (Linienmeter) über die Rückwärtssuche von Nominatim (OpenStreetMap, zoom=17, eine Abfrage je
# Sekunde) -> orte2026.json [Linienmeter, Colonia, Alcaldía], Rohantworten in ../dl/nominatim.json. Colonia nur aus „neighbourhood“
# (in OSM als Fläche erfasst), sonst „village“ (Ciudad Universitaria); „quarter“ und „suburb“ ordnet Nominatim nach dem nächsten
# Ortspunkt zu und lag oft daneben (Reforma „Condesa“, Bosque de Chapultepec „San Miguel Chapultepec“). Bereinigung in namen.py.
import json, os, time, urllib.request, urllib.parse, numpy as np
CACHE = "../dl/nominatim.json"; cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); P = np.array([p[:2] for p in g["pts"]])
out = []
for n, s in enumerate(np.arange(0, d[-1], 100.0)):
    la, lo = float(np.interp(s, d, P[:, 0])), float(np.interp(s, d, P[:, 1])); key = f"{la:.5f},{lo:.5f}"
    if key not in cache:
        u = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode({"lat": la, "lon": lo, "format": "jsonv2", "zoom": 17, "addressdetails": 1, "accept-language": "es"})
        for att in range(4):
            try:
                cache[key] = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"}), timeout=30)); break
            except Exception as e: print("  Fehler", s, e, flush=True); time.sleep(5 + 5 * att)
        time.sleep(1.1)
        if n % 25 == 0: json.dump(cache, open(CACHE, "w"), ensure_ascii=False); print(f"{s / 1000:5.1f} km", flush=True)
    a = cache.get(key, {}).get("address", {})
    out.append([float(s), a.get("neighbourhood") or a.get("village") or "", a.get("city_district") or a.get("borough") or a.get("county") or ""])
json.dump(cache, open(CACHE, "w"), ensure_ascii=False)
json.dump(out, open("orte2026.json", "w"), ensure_ascii=False)
from itertools import groupby
print("Colonias:", [(k, len(list(v)) * 100) for k, v in groupby(o[1] for o in out)])
print("Alcaldías:", [(k, len(list(v)) * 100) for k, v in groupby(o[2] for o in out)])
