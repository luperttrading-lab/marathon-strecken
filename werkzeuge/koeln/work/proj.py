# Ohne offizielle Kilometerpunkte: Start und Ziel sind Anfang und Ende der Linie -> kmproj.json
# (common.py streckt damit die ganze Linie gleichmäßig auf 42 195 m; die gezeichnete Linie ist 0,2 % kürzer)
import json
g = json.load(open("gpx2026.json")); d = g["d"]
km = {"Start": [0.0, 0.0], "Ziel": [d[-1], 0.0]}
print("Start 0 m, Ziel", round(d[-1]), "m GPX ->", round(42195 / d[-1] * 100 - 100, 2), "% Streckung")
json.dump(km, open("kmproj.json", "w"))
