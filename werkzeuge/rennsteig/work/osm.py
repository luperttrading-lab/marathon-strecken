# OSM-Wege entlang der Strecke (Overpass-Spiegel maps.mail.ru; andere Spiegel sind in dieser Umgebung gesperrt).
# Stückweise: je 8 Punkte der Outdooractive-Linie (~700 m) ein Rechteck mit 300 m Rand, Wege mit Geometrie und Knoten-IDs.
# Der Spiegel antwortet unzuverlässig (meist sofort 504, größere Abfragen fast immer): wiederholen, jedes fertige Stück
# in ../dl/osm_teile/ ablegen, damit ein Neustart nichts verliert.
import json, os, time, urllib.request, urllib.parse
os.makedirs("../dl/osm_teile", exist_ok=True)
L = json.load(open("../dl/outdooractive_linie.json")); P = L if isinstance(L[0], (list, tuple)) else L["pts"]
URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"; ways = {}
def holen(q):
    for att in range(300):
        try:
            r = urllib.request.urlopen(urllib.request.Request(URL, urllib.parse.urlencode({"data": q}).encode(), headers={"User-Agent": "marathon-profile/1.0 (private use)"}), timeout=180)
            return json.loads(r.read())["elements"], att + 1
        except Exception:
            time.sleep(1.5)
    raise SystemExit("Overpass nicht erreichbar")
for i in range(0, len(P), 8):
    seg = P[max(0, i - 1):i + 9]; la = [p[0] for p in seg]; lo = [p[1] for p in seg]
    bb = (min(la) - 0.0027, min(lo) - 0.0043, max(la) + 0.0027, max(lo) + 0.0043)
    f = f"../dl/osm_teile/{i}.json"
    if os.path.exists(f): el, n = json.load(open(f)), 0
    else:
        el, n = holen('[out:json][timeout:120];way["highway"](%.5f,%.5f,%.5f,%.5f);out geom;' % bb); json.dump(el, open(f, "w"))
    for w in el: ways[w["id"]] = w
    print(i, len(el), "Wege, gesamt", len(ways), "Versuche", n, flush=True)
json.dump({"elements": list(ways.values())}, open("../dl/osm_wege.json", "w"))
print("fertig", len(ways), "Wege", flush=True)
