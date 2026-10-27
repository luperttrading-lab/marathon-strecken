# Offizielle Ideallinie 2026 (Karte maps.scc-events.com, Ebene „Strecke Läufer:innen“) -> gpx2026.json,
# dazu die Marken derselben Ebene (KM-Punkte, Ziellinie, Verpflegung, Erfrischungen) -> ../dl/locations.json
import json, math
K = json.load(open("../dl/karte.json"))
F = [f for f in K["features"] if f["properties"].get("layer") == 130]
line = [f for f in F if f["geometry"]["type"] == "LineString" and (f["properties"].get("names") or {}).get("de") == "Ideallinie"][0]
pts = [(c[1], c[0], 0.0) for c in line["geometry"]["coordinates"]]
def hav(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    a = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(a))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i-1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1]/1000, 3), "Start", pts[0][:2], "Ende", pts[-1][:2])
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
CAT = {"Verpflegungspunkt": "verpflegung", "Erfrischungen": "wasser", "Ziellinie": "km"}
locs = []
for f in F:
    if f["geometry"]["type"] != "Point": continue
    nm = (f["properties"].get("names") or {}).get("de", "")
    cat = "km" if nm.startswith("KM ") else CAT.get(nm)
    if cat: locs.append({"name": "Ziel" if nm == "Ziellinie" else nm, "lat": f["geometry"]["coordinates"][1], "lon": f["geometry"]["coordinates"][0], "cat": cat})
json.dump(locs, open("../dl/locations.json", "w"), ensure_ascii=False, indent=0)
print(len(locs), "Marken")
