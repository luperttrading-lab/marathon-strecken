import json, time, urllib.request, urllib.parse, sys
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
scale = d[-1] / 42195.0
marks = [(6.9,"Elbchaussee"),(11.3,"Fischmarkt"),(12.3,"Landungsbrücken"),(13.1,"Hafencity-Speicherstadt"),(16.3,"Jungfernstieg"),(21.098,"Sierichstraße"),(27.7,"City Nord Überseering"),(30.7,"Ohlsdorf"),(32.7,"Maienweg"),(37.1,"Eppendorfer Baum"),(38.2,"Außenalster")]
def at(m):
    for i in range(1, len(d)):
        if d[i] >= m:
            f = (m - d[i-1]) / (d[i]-d[i-1])
            return [pts[i-1][k] + f*(pts[i][k]-pts[i-1][k]) for k in range(3)]
    return pts[-1]
for km, name in marks:
    out = []
    for off in (-300, 0, 300):
        la, lo, e = at(km*1000*scale + off)
        url = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode({"lat": la, "lon": lo, "format": "json", "zoom": 17})
        req = urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0 (private use)"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=20)); a = r.get("address", {})
            out.append(a.get("road") or a.get("pedestrian") or a.get("footway") or r.get("display_name","")[:40])
        except Exception as ex:
            out.append("ERR " + str(ex)[:30])
        time.sleep(1.1)
    print(f"{km:6.2f} {name:24s} -> {out}")
