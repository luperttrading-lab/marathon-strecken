import json, time, urllib.request, urllib.parse, math
g = json.load(open("gpx2026.json")); pts, d = g["pts"], g["d"]
def hav(a, b):
    R=6371008.8; la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]))
    x=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(x))
qs = [(11.3,"Fischauktionshalle, Hamburg"),(12.3,"St. Pauli Landungsbrücken, Hamburg"),(13.1,"Speicherstadt, Hamburg"),(16.3,"Jungfernstieg, Hamburg"),(27.7,"Überseering, Hamburg"),(30.7,"Ohlsdorf Bahnhof, Hamburg"),(37.1,"Eppendorfer Baum, Hamburg")]
for km, q in qs:
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1})
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "marathon-profile-check/1.0"}), timeout=20))
    time.sleep(1.1)
    if not r: print(km, q, "nicht gefunden"); continue
    p = (float(r[0]["lat"]), float(r[0]["lon"]))
    # alle lokalen Minima der Distanz < 400 m
    ds = [hav(p, x) for x in pts]
    hits = [(round(d[i]/1000,2), round(ds[i])) for i in range(1,len(pts)-1) if ds[i] <= ds[i-1] and ds[i] <= ds[i+1] and ds[i] < 400]
    print(f"Bild {km:5.1f} {q:38s} GPX-km/Abstand: {hits}")
