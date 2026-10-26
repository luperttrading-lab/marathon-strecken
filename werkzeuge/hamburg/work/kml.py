import zipfile, re, sys, json
base = sys.argv[1]
def kml(name): return zipfile.ZipFile(f"{base}/{name}.kmz").read("doc.kml").decode("utf-8")
def placemarks(t):
    out = []
    for pm in re.findall(r"<Placemark>(.*?)</Placemark>", t, re.S):
        nm = re.search(r"<name>(.*?)</name>", pm, re.S); nm = nm.group(1).strip() if nm else ""
        geo = "LineString" if "<LineString" in pm else ("Point" if "<Point" in pm else "?")
        co = re.search(r"<coordinates>(.*?)</coordinates>", pm, re.S)
        cs = [tuple(map(float, c.split(",")[:2])) for c in co.group(1).split()] if co else []
        out.append((nm, geo, cs))
    return out
res = {}
for n in ["HMH26_Marathon", "HMH26_Marathon_KM_Punkte", "HMH26_Staffelstrecke", "HMH26_VPS_WS"]:
    pms = placemarks(kml(n))
    print(n, len(pms))
    for nm, g, cs in pms[:60]:
        print("   ", repr(nm[:60]), g, len(cs), cs[0] if cs else "")
    res[n] = pms
json.dump(res, open("kml.json", "w"))
