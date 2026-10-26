import re, math, json, sys
src = sys.argv[1]
txt = open(src).read()
pts = [(float(a), float(b), float(c)) for a, b, c in re.findall(r'<trkpt lat="([\d.]+)" lon="([\d.]+)">\s*<ele>([-\d.]+)</ele>', txt)]
def hav(p, q):
    R = 6371008.8
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    a = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(a))
d = [0.0]
for i in range(1, len(pts)):
    d.append(d[-1] + hav(pts[i-1], pts[i]))
print("points", len(pts), "length km", round(d[-1]/1000, 3))
print("first", pts[0], "last", pts[-1])
json.dump({"pts": pts, "d": d}, open("gpx2024.json", "w"))
