# Straßennamen und Ort alle 150 m (GPX-Meter) per Nominatim-Rückwärtssuche, 1 Abfrage/s -> streets2026.json
import json, time, urllib.request, urllib.parse
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
def at(m):
    for i in range(1, len(d)):
        if d[i] >= m:
            f = (m - d[i-1])/((d[i]-d[i-1]) or 1)
            return pts[i-1][0] + f*(pts[i][0]-pts[i-1][0]), pts[i-1][1] + f*(pts[i][1]-pts[i-1][1])
    return pts[-1][0], pts[-1][1]
out, s = [], 0.0
while s <= d[-1]:
    la, lo = at(s)
    url = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode({"lat": la, "lon": lo, "format": "json", "zoom": 17, "addressdetails": 1})
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"}), timeout=20))
        a = r.get("address", {})
        ort = a.get("suburb") or a.get("neighbourhood") or a.get("quarter") or ""   # Community Area (Loop, Near North Side, Lincoln Park …); feinere Viertel wechseln an jeder Blockgrenze
        out.append([s, a.get("road") or a.get("pedestrian") or a.get("footway") or a.get("cycleway") or "", ort])
    except Exception as ex:
        out.append([s, "", ""])
    time.sleep(1.1)
    s += 150
json.dump(out, open("streets2026.json", "w"), ensure_ascii=False)
print(len(out), "Punkte, leer:", sum(1 for o in out if not o[1]))
