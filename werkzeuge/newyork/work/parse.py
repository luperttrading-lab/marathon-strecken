# Offizielle Strecke 2026 (Google-Karte von NYRR, Linie „Course (BLUE)“) -> gpx2026.json,
# dazu Meilen-, 5-km-, Halbmarathon- und Zielmarke der blauen Startwelle sowie die Getränkestellen -> ../dl/locations.json
import json, math, re
t = open("../dl/strecke.kml", encoding="utf-8").read()
PM = []
for pm in re.findall(r"<Placemark>(.*?)</Placemark>", t, re.S):
    nm = re.sub(r"<!\[CDATA\[|\]\]>", "", re.search(r"<name>(.*?)</name>", pm, re.S).group(1)).strip()
    co = [tuple(map(float, x.split(",")[:2])) for x in re.search(r"<coordinates>(.*?)</coordinates>", pm, re.S).group(1).split()]
    PM.append((nm, "<LineString>" in pm, co))
line = [co for nm, ls, co in PM if ls and nm == "Course (BLUE)"][0]
pts = [(la, lo, 0.0) for lo, la in line]
def hav(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    return 2*R*math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
d = [0.0]
for i in range(1, len(pts)): d.append(d[-1] + hav(pts[i-1], pts[i]))
print("Punkte", len(pts), "Länge km", round(d[-1]/1000, 3))
json.dump({"pts": pts, "d": d}, open("gpx2026.json", "w"))
MI = 1609.344; locs = []
for nm, ls, co in PM:
    if ls: continue
    lo, la = co[0]; m = None
    blue = ("(" not in nm) or ("BLUE" in nm) or ("ALL COURSES" in nm)
    if re.match(r"Mile \d+", nm) and blue: m = int(nm.split()[1]) * MI
    elif re.match(r"\d+K\b", nm) and blue: m = int(nm.split("K")[0]) * 1000.0
    elif re.match(r"\d+M$", nm): m = int(nm[:-1]) * MI
    elif nm.startswith("HALF MARATHON"): m = 21097.5
    elif nm == "FINISH": m = 42195.0
    elif nm == "BLUE START": m = 0.0
    if m is not None: locs.append({"name": nm, "lat": la, "lon": lo, "cat": "km", "m": m})
    elif re.match(r"Fluid(/Medical)? \d+", nm): locs.append({"name": nm, "lat": la, "lon": lo, "cat": "wasser", "mile": int(re.findall(r"\d+", nm)[0])})
locs.sort(key=lambda l: (l["cat"], l.get("m", 0), l.get("mile", 0)))
json.dump(locs, open("../dl/locations.json", "w"), ensure_ascii=False, indent=0)
print(sum(l["cat"] == "km" for l in locs), "Marken,", sum(l["cat"] == "wasser" for l in locs), "Getränkestellen")
