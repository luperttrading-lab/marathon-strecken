# Linie der Strecke aus dem Streckenplan 2025 des Veranstalters und OSM -> linie2025.json {"pts": [[lat, lon], …], "d": [laufende Länge in
# m, UTM 51N], "info": [["osm", Weg] oder ["plan", 0] je Punkt], "wegpunkte": [[Name, Linienmeter], …], "wende_longteng": Meter}.
#
# Eine GPX-Datei gibt der Veranstalter nicht heraus; der Plan für 2026 ist noch nicht veröffentlicht (Stand 31.10.2026: „敬请期待“). Die
# Linie folgt dem Plan 2025 (gleich dem Plan 2024; die Wettkampfordnung 2026 nennt dieselben Orte, siehe UEBERGABE.md). Der Plan ist
# eine stark vereinfachte Zeichnung (eingepasst liegt die Linie bis 450 m neben den Straßen, georef.py); er dient deshalb nur für die
# Reihenfolge der Straßen, die er beschriftet. Die Linie selbst besteht aus OSM-Wegen:
#   Wegpunkte sind die Kreuzungen, an denen die Strecke laut Plan abbiegt (OSM-Knoten, an dem sich die Wege beider Namen treffen),
#   dazwischen der kürzeste Weg im OSM-Netz, wobei Wege mit dem Namen der Straße, auf der das Stück laut Plan läuft, einfach zählen,
#   Wege ohne Namen 1,3-fach, Fuß- und Radwege 2-fach (am Ufer einfach) und alle anderen benannten Straßen 4-fach. Hochstraßen (Namen
#   mit 高架), große Brücken (大桥: Nanpu, Lupu), Tunnel, Rampen und highway=motorway bleiben draußen.
# Wendepunkte (der Plan zeigt sie nur ungefähr): Bansongyuan Lu an der Kreuzung Nanchezhan Lu; die Stichstraße bei km 37 (im Plan
# „Fenggu Rd.“, in OSM Ruijiang Lu) an der Kreuzung Yunjin Lu; die Wende auf der Longteng Dadao im Süden so, dass die Linie 42 195 m
# lang wird (der Plan zeigt sie kurz hinter km 32; Kontrolle in marken.py).
# Start: Zhongshan Dongyi Lu zwischen Fuzhou Lu und Hankou Lu, ein Drittel des Wegs von der Fuzhou Lu (Startplan „起点示意图“ 2025).
# Ziel: vom Tor 12 an der Zhongshan Nan'er Lu durch den Xujiahui-Sportpark bis zur Ziellinie südlich der Sponsorenfläche zwischen
# Hallenstadion und Stadion, gezeichnet nach dem Zielplan „终点示意图“ 2025 (eingepasst an Stadion, Hallenstadion und Schwimmhalle).
import json, math, heapq, sys
import numpy as np
from scipy.spatial import cKDTree
from geo import utm, wgs, dicht, laenge, osm, kreuzung
N, W, _ = osm()
STRASSE = {"trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "trunk_link", "primary_link", "secondary_link",
           "tertiary_link", "living_street", "road", "pedestrian", "service"}
FUSS = {"footway", "path", "cycleway"}
def zulaessig(tg):
    hw = tg.get("highway"); nm = tg.get("name", "")
    if hw not in STRASSE | FUSS: return False
    if "高架" in nm or "隧道" in nm or "匝道" in nm or "大桥" in nm or hw.endswith("_link"): return False
    if tg.get("tunnel") not in (None, "no"): return False
    return True        # Brücken bleiben drin: Die Longteng Dadao überquert den Longhua Gang auf einer Brücke (layer 2)
XY, ADJ, EDGE = {}, {}, {}
for wid, (tg, refs) in W.items():
    if not zulaessig(tg): continue
    refs = [r for r in refs if r in N]
    for r in refs:
        if r not in XY: x, y = utm(*N[r]); XY[r] = np.array([float(x), float(y)]); ADJ[r] = []
    for a, b in zip(refs[:-1], refs[1:]):
        if a == b: continue
        L = float(np.hypot(*(XY[a] - XY[b])))
        EDGE[(a, b)] = EDGE[(b, a)] = (L, wid)
        ADJ[a].append(b); ADJ[b].append(a)
def kosten(e, namen, ufer):
    L, wid = e; tg = W[wid][0]; nm = tg.get("name", ""); hw = tg["highway"]
    if hw in FUSS: f = 1.0 if ufer else 2.0        # auch der Radweg „龙腾大道“ neben der Fahrbahn
    elif nm and nm in namen: f = 1.0
    elif not nm: f = 1.3
    else: f = 4.0
    return L * f
def dijkstra(a, b, namen, ufer=False):
    dist = {a: 0.0}; vor = {}; h = [(0.0, a)]
    while h:
        c, u = heapq.heappop(h)
        if u == b: break
        if c > dist.get(u, 1e18): continue
        for v in ADJ[u]:
            nc = c + kosten(EDGE[(u, v)], namen, ufer)
            if nc < dist.get(v, 1e18): dist[v] = nc; vor[v] = u; heapq.heappush(h, (nc, v))
    weg = [b]
    while weg[-1] != a: weg.append(vor[weg[-1]])
    return weg[::-1]
def knoten_bei(p, namen=None, art=None):
    """Netzknoten nächst p (UTM), wahlweise nur auf Wegen mit einem der Namen bzw. der Art."""
    best = None
    for (a, b), (L, wid) in EDGE.items():
        tg = W[wid][0]
        if namen and tg.get("name") not in namen: continue
        if art and tg.get("highway") not in art: continue
        d = float(np.hypot(*(XY[a] - p)))
        if best is None or d < best[0]: best = (d, a)
    return best[1]
def kr(n1, n2, nahe=None):
    return knoten_bei(kreuzung(n1, n2, nahe), {n1, n2})
# --- Strecke: Wegpunkte und die Straßen bis zum nächsten Wegpunkt
fz = kreuzung("中山东一路", "福州路"); hk = kreuzung("中山东一路", "汉口路")
START = knoten_bei(fz + (hk - fz) / 3.0, {"中山东一路"})
def ll(la, lo): return np.array([float(v) for v in utm(la, lo)])
STRECKE = [
    ("Start", START, {"中山东一路", "中山东二路"}),
    ("Xinkaihe Lu", kr("中山东二路", "新开河路"), {"新开河路", "人民路"}),
    ("Renmin Lu/Henan Nanlu", kr("人民路", "河南南路"), {"河南南路", "河南中路"}),
    ("Henan Zhonglu/Nanjing Donglu", kr("河南中路", "南京路步行街"), {"南京路步行街"}),
    ("Nanjing Donglu/Hubei Lu", kr("南京路步行街", "湖北路"), {"湖北路"}),
    ("Hubei Lu/Jiujiang Lu", kr("湖北路", "九江路"), {"九江路"}),
    ("Jiujiang Lu/Nanjing Xilu", kr("九江路", "南京西路"), {"南京西路"}),
    ("Nanjing Xilu/Huashan Lu", kr("南京西路", "华山路"), {"华山路"}),
    ("Huashan Lu/Changshu Lu", kr("华山路", "常熟路"), {"常熟路"}),
    ("Changshu Lu/Huaihai Zhonglu", kr("常熟路", "淮海中路"), {"淮海中路"}),
    ("Huaihai Zhonglu/Madang Lu", kr("淮海中路", "马当路"), {"马当路"}),
    ("Madang Lu/Xingye Lu", kr("马当路", "兴业路"), {"兴业路"}),
    ("Xingye Lu/Huangpi Nanlu", kr("兴业路", "黄陂南路"), {"湖滨路", "黄陂南路", "兴业路"}),
    ("Hubin Lu/Jinan Lu", kr("湖滨路", "济南路"), {"济南路"}),
    ("Jinan Lu/Zizhong Lu", kr("济南路", "自忠路"), {"自忠路"}),
    ("Zizhong Lu/Huangpi Nanlu", kr("自忠路", "黄陂南路"), {"黄陂南路"}),
    ("Huangpi Nanlu/Huaihai Zhonglu", kr("黄陂南路", "淮海中路"), {"淮海中路"}),
    ("Huaihai Zhonglu/Xizang Nanlu", kr("淮海中路", "西藏南路"), {"西藏南路"}),
    ("Xizang Nanlu/Gaoxiong Lu", kr("西藏南路", "高雄路"), {"高雄路"}),
    ("Gaoxiong Lu/Zhizaoju Lu", kr("高雄路", "制造局路"), {"制造局路"}),
    ("Zhizaoju Lu/Longhua Donglu", kr("制造局路", "龙华东路"), {"龙华东路", "半淞园路"}),
    ("Wende Bansongyuan Lu", kr("半淞园路", "南车站路"), {"半淞园路"}),
    ("Bansongyuan Lu/Wangda Lu", kr("半淞园路", "望达路"), {"望达路"}),
    ("Wangda Lu/Miaojiang Lu", kr("望达路", "苗江路"), {"苗江路", "外马路"}),
    ("Waima Lu/Bansongyuan Lu", kr("外马路", "半淞园路"), {"半淞园路"}),
    ("Bansongyuan Lu/Lujiabang Lu", kr("半淞园路", "陆家浜路"), {"陆家浜路"}),
    ("Lujiabang Lu/Waima Lu", kr("陆家浜路", "外马路"), {"外马路"}),
    ("Uferweg (Nanpu-Brücke)", knoten_bei(ll(31.20667, 121.49770), art=FUSS), set()),
    ("Uferweg (Huayuangang Lu)", knoten_bei(ll(31.20366, 121.49516), art=FUSS), {"苗江路"}),
    ("Miaojiang Lu/Longhua Donglu", kr("苗江路", "龙华东路"), {"龙华东路"}),
    ("Longhua Donglu/Furun Lu", kr("龙华东路", "富润路"), {"富润路"}),
    ("Furun Lu/Jiangbin Lu", kr("富润路", "江滨路"), {"江滨路"}),
    ("Jiangbin Lu/Ruining Lu", kr("江滨路", "瑞宁路"), {"瑞宁路"}),
    ("Ruining Lu/Longteng Dadao", kr("瑞宁路", "龙腾大道"), {"龙腾大道"}),
    ("Wende Longteng Dadao", None, {"龙腾大道"}),
    ("Longteng Dadao/Ruijiang Lu", kr("龙腾大道", "瑞江路"), {"瑞江路"}),
    ("Wende Ruijiang Lu", kr("瑞江路", "云锦路"), {"瑞江路"}),
    ("Ruijiang Lu/Longteng Dadao", None, {"龙腾大道"}),
    ("Longteng Dadao/Longheng Donglu", kr("龙腾大道", "龙恒东路"), {"龙恒东路"}),
    ("Longheng Donglu/Wanping Nanlu", kr("龙恒东路", "宛平南路"), {"宛平南路", "云锦路"}),
    ("Wanping Nanlu/Longhua Lu", kr("宛平南路", "龙华路"), {"龙华路"}),
    ("Longhua Lu/Longhua Xilu", kr("龙华路", "龙华西路"), {"龙华西路"}),
    ("Longhua Xilu/Zhongshan Nan'erlu", kr("龙华西路", "中山南二路"), {"中山南二路"}),
]
UFER = {"Lujiabang Lu/Waima Lu", "Uferweg (Nanpu-Brücke)", "Uferweg (Huayuangang Lu)"}
STRECKE[37] = (STRECKE[37][0], STRECKE[35][1], STRECKE[37][2])        # zurück an dieselbe Kreuzung
# Ziel nach dem Zielplan (Vorschaubild 1500 px breit): eingepasst an drei Bauten (Mitte im Plan von Hand, Schwerpunkt in OSM)
ZP = {"上海体育场": (785, 705), "上海体育馆": (388, 710), "上海游泳馆": (640, 980)}
def schwerpunkt(name):
    for tg, refs in W.values():
        if tg.get("name") == name and len(refs) > 3:
            q = np.array([N[r] for r in refs if r in N]); x, y = utm(q[:, 0], q[:, 1]); return np.array([x.mean(), y.mean()])
    raise KeyError(name)
zs = np.array(list(ZP.values()), float); zd = np.array([schwerpunkt(n) for n in ZP])
ca, cb = zs.mean(0), zd.mean(0); za = (zs - ca)[:, 0] - 1j * (zs - ca)[:, 1]; zb = (zd - cb)[:, 0] + 1j * (zd - cb)[:, 1]
kz = (np.conj(za) @ zb) / (np.conj(za) @ za)
def zab(p):
    p = np.asarray(p, float) - ca; z = kz * (p[..., 0] - 1j * p[..., 1]); return np.stack([z.real, z.imag], -1) + cb
print("Zielplan eingepasst: Maßstab", round(abs(kz), 3), "m/px, Restfehler", np.round(np.hypot(*(zab(zs) - zd).T), 1).tolist(), "m")
ZIELWEG = zab([(517, 1103), (563, 1008), (610, 913), (623, 869), (636, 825), (630, 800), (597, 778), (563, 772), (530, 770)])
STRECKE.append(("Tor 12", knoten_bei(ZIELWEG[0], {"中山南二路"}), set()))
# Longteng Dadao nach Süden als Kette von Knoten (für die Wende)
A = STRECKE[33][1]
sued = max((r for tg, refs in W.values() if tg.get("name") == "龙腾大道" and tg.get("highway") in STRASSE for r in refs if r in XY),
           key=lambda r: -XY[r][1])
LT = dijkstra(A, sued, {"龙腾大道"}); LTs = laenge(np.array([XY[k] for k in LT]))
assert all(W[EDGE[(u, v)][1]][0].get("highway") not in FUSS for u, v in zip(LT[:-1], LT[1:])), "Longteng Dadao über einen Radweg"
def bauen(s_wende):
    k = int(np.searchsorted(LTs, s_wende, side="right")) - 1; k = min(max(k, 0), len(LT) - 2)
    STRECKE[34] = ("Wende Longteng Dadao", LT[k], {"龙腾大道"})
    # genaue Wende zwischen zwei Knoten: das Reststück hin und zurück
    f = (s_wende - LTs[k]) / (LTs[k + 1] - LTs[k]); spitze = XY[LT[k]] + (XY[LT[k + 1]] - XY[LT[k]]) * f
    wid_lt = int(EDGE[(LT[k], LT[k + 1])][1])
    pts, info, marken = [XY[STRECKE[0][1]]], [], [(STRECKE[0][0], 0)]
    for (n1, a, namen), (n2, b, _) in zip(STRECKE[:-1], STRECKE[1:]):
        if a != b:
            t = dijkstra(a, b, namen, n1 in UFER)
            for u, v in zip(t[:-1], t[1:]): info.append(["osm", int(EDGE[(u, v)][1])]); pts.append(XY[v])
        if n2 == "Wende Longteng Dadao" and f > 0:
            info.append(["osm", wid_lt]); pts.append(spitze); info.append(["osm", wid_lt]); pts.append(XY[LT[k]])
        marken.append((n2, len(pts) - 1 - (1 if n2 == "Wende Longteng Dadao" and f > 0 else 0)))
    info.append(info[-1])
    for p in ZIELWEG[1:]: pts.append(p); info.append(["plan", 0])
    pts = np.array(pts); d = laenge(pts)
    return pts, info, d, [(n, float(d[i])) for n, i in marken]
s = 4000.0
for it in range(8):
    pts, info, d, marken = bauen(s)
    if abs(d[-1] - 42195.0) < 0.05: break
    s += (42195.0 - d[-1]) / 2
    print(f"  Wende Longteng {s:7.1f} m südlich der Ruining Lu -> Linie {d[-1]:8.1f} m")
pts, info, d, marken = bauen(s)
lat, lon = wgs(pts[:, 0], pts[:, 1])
json.dump({"pts": np.c_[lat, lon].round(7).tolist(), "d": d.round(2).tolist(), "info": info,
           "wegpunkte": [[n, round(x, 1)] for n, x in marken], "wende_longteng": round(s, 1)}, open("linie2025.json", "w"), ensure_ascii=False)
print(f"Linie {d[-1]:.1f} m, {len(pts)} Punkte, Wende auf der Longteng Dadao {s:.0f} m südlich der Ruining Lu")
vor = 0.0
for n, x in marken:
    print(f"  {n:34s} {x:8.0f} m   (+{x - vor:5.0f})"); vor = x
