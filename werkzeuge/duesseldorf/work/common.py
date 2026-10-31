# Linienmeter <-> offizielle Meter: gleichmäßig gestreckt, Start = Anfang der Planlinie, Ziel = ihr Ende (42 195 m). Die 42 Kilometer-
# schilder im Plan sitzen neben der Linie und taugen nur zur Gegenprobe (marken.py).
import json, numpy as np
g = json.load(open("strecke2026.json")); GL = g["d"][-1]
def official(s): return np.asarray(s, dtype=float) * 42195.0 / GL
def gpx_of(k): return np.asarray(k, dtype=float) * GL / 42195.0
