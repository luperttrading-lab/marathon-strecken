import json, math, sys, time, urllib.request, concurrent.futures as cf
src, out, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
g = json.load(open(src)); pts, d = g["pts"], g["d"]
def at(m):
    for i in range(1, len(d)):
        if d[i] >= m:
            f = (m - d[i-1])/((d[i]-d[i-1]) or 1)
            return pts[i-1][0] + f*(pts[i][0]-pts[i-1][0]), pts[i-1][1] + f*(pts[i][1]-pts[i-1][1])
    return pts[-1][0], pts[-1][1]
ss = [k*step for k in range(int(d[-1]//step)+1)] + [d[-1]]
def q(s):
    la, lo = at(s); dd = 0.00005
    url = ("https://geodienste.hamburg.de/HH_WMS_DGM1?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo"
           "&LAYERS=WMS_DGM1_HAMBURG&QUERY_LAYERS=WMS_DGM1_HAMBURG&CRS=EPSG:4326&STYLES="
           f"&BBOX={la-dd:.7f},{lo-dd:.7f},{la+dd:.7f},{lo+dd:.7f}&WIDTH=11&HEIGHT=11&I=5&J=5&INFO_FORMAT=text/plain")
    for attempt in range(4):
        try:
            t = urllib.request.urlopen(url, timeout=30).read().decode()
            v = [l.split("'")[1] for l in t.splitlines() if "value_0" in l]
            return s, la, lo, (float(v[0]) if v else None)
        except Exception as ex:
            time.sleep(1 + 2*attempt)
    return s, la, lo, None
t0 = time.time()
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(q, ss))
print(len(res), "Punkte in", round(time.time()-t0), "s; fehlend:", sum(r[3] is None for r in res))
json.dump(res, open(out, "w"))
