# Rohhöhen -> clean.json, ohne Brückensuche. Die anderen Strecken suchen Brücken an Stufen > 1,5 m auf 10 m im DGM1.
# Das 20-m-Raster hat solche Stufen an steilen Hängen (bis 2,2 m auf 10 m) und keine Brücken mehr; über Straßen und
# Bäche führt der Rennsteig hier ebenerdig. Deshalb bleiben die Höhen unverändert, die Liste der Brücken bleibt leer.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from common import official
r = json.load(open("dgm2026_10m.json"))
s = np.array([x[0] for x in r]); raw = np.array([x[3] for x in r], float); k = official(s)
print("Punkte", len(raw), "größte Stufe je 10 m", round(float(np.abs(np.diff(raw)).max()), 2), "m")
json.dump({"k": k.tolist(), "h": raw.tolist(), "raw": raw.tolist(), "regions": []}, open("clean.json", "w"), ensure_ascii=False)
