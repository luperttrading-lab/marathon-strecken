# Brücken: das Geländemodell (DTM) misst darunter Wasser, Docks oder Einschnitte. Auf den Brücken der Strecke (OSM bridge=yes
# bzw. movable, Spannen in ZONEN, offizielle km) gilt das Oberflächenmodell (LZ-DSM, last return) der Environment Agency, das die
# Fahrbahn misst. Verworfen werden DSM-Werte unter dem Gelände oder mehr als 5 m über den Brückenenden (Türme und Gehwege der
# Tower Bridge, Laternen, Busse), dort linear dazwischen. Nicht als Brücke: Trafalgar Way (km 30,95, darüber die DLR-Hochbahn),
# Westferry Circus (km 24,1: die Strecke läuft im Tunnel darunter), Upper Thames Street (Tunnel und Durchfahrten).
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json")); s = np.array([x[0] for x in r]); dtm = np.array([x[3] for x in r]); k = official(s)
dsm = np.array([x[3] for x in json.load(open("dsm2026_10m.json"))])
ZONEN = [("Shooters Hill Road über die A102", 0.88, 1.03), ("Creek Road über den Deptford Creek", 11.17, 11.25),
         ("Salter Road", 17.12, 17.20), ("Tower Bridge", 19.79, 20.19), ("Narrow Street, Limehouse Basin", 22.91, 22.99),
         ("Narrow Street", 23.03, 23.07), ("Marsh Wall", 28.23, 28.27), ("Bank Street", 29.25, 29.37),
         ("Churchill Place", 30.03, 30.27), ("Poplar High Street", 31.86, 31.91), ("Commercial Road", 33.38, 33.42), ("Commercial Road", 33.70, 33.75)]
h = dtm.copy(); src = np.zeros(len(s), int)
at = lambda km: int(np.argmin(np.abs(k - km * 1000)))
for nm, a, b in ZONEN:
    ia, ib = at(a), at(b); ii = np.arange(ia, ib + 1)
    ende = max(dtm[ia], dtm[ib]); ok = (dsm[ii] >= dtm[ii] - 0.2) & (dsm[ii] <= ende + 5)
    ok[0] = ok[-1] = True; v = np.where(ok, dsm[ii], np.nan); v[0], v[-1] = dtm[ia], dtm[ib]
    h[ii] = np.interp(ii, ii[np.isfinite(v)], v[np.isfinite(v)]); src[ii] = 1
    print(f"{nm:36s} km {k[ia]/1000:6.2f}-{k[ib]/1000:6.2f}  Enden {dtm[ia]:5.1f}/{dtm[ib]:5.1f}  Fahrbahn max {h[ii].max():5.1f}  (Gelände min {dtm[ii].min():5.1f}, verworfen {(~ok).sum()})")
json.dump({"h": h.tolist(), "src": src.tolist()}, open("lidar.json", "w"))
