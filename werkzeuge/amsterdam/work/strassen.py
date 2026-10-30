# Straße je 10 Linienmeter aus den OSM-Wegen, auf denen die Linie liegt (linie_wege.json, linie.py): Name wie in OSM (niederländisch),
# Brücke, Tunnel, highway. Die Torontobrug trägt in OSM keinen Namen (Name laut Streckenplan). Im Stadion „Olympisch Stadion“.
# -> strassen.json [Linienmeter, Name, Brücke, Tunnel/überdeckt, highway, OSM-Weg]
import json, numpy as np
from itertools import groupby
g = json.load(open("gpx2026.json")); d = np.array(g["d"]); W = json.load(open("linie_wege.json"))
net = json.load(open("../dl/osm_netz.json"))["wege"]
NAMENLOS = {"10211542": "Torontobrug", "10211544": "Torontobrug", "1565876966": "Torontobrug", "1565876968": "Torontobrug", "1565876969": "Torontobrug"}
out = []
for s in np.arange(0, d[-1], 10.0):
    i = min(len(W) - 1, int(np.searchsorted(d, s, side="right")) - 1); w = W[i]
    if w == "stadion": out.append([float(s), "Olympisch Stadion", "", "", "track", "stadion"]); continue
    t = net[w]["tags"]
    nm = t.get("name") or t.get("bridge:name") or NAMENLOS.get(w, "")
    tun = t.get("tunnel", "") if t.get("tunnel") not in (None, "no") else ("covered" if t.get("covered") == "yes" else "")
    out.append([float(s), nm, t.get("bridge", "") if t.get("bridge") not in (None, "no") else "", tun, t.get("highway", ""), w])
json.dump(out, open("strassen.json", "w"), ensure_ascii=False)
for (n, b, tu), grp in groupby(out, key=lambda o: (o[1], o[2], o[3])):
    grp = list(grp); print(f"{grp[0][0]:7.0f} {len(grp) * 10:5d} m  {n or '–'} {'BRÜCKE ' + b if b else ''} {'TUNNEL ' + tu if tu else ''}")
