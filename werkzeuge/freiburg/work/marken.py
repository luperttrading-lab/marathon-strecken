# Nur Abgleich: Kilometerkästen des Streckenplans 2026 (georef.py -> plan_km.json, 17 von 20 Kästen gefunden; 1, 11 und 18 berühren die
# Linie und werden nicht als eigene Fläche erkannt) gegen die Kilometer der App (Ideallinie, common.py) und gegen gleichmäßige Streckung.
# Die Kästen stehen 85–115 m neben der Linie (Kasten 9: 233 m), ihr Lotfußpunkt ist daher auf etwa ±0,1 km unsicher.
import json
from common import official
pk = json.load(open("plan_km.json")); L = json.load(open("runde.json"))["d"][-1]
nr = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20]   # Reihenfolge längs der Linie, fehlende 1, 11, 18
print(" km  Linienmeter  App (Ideallinie)  gleichmäßig   Abw. App  Abw. gleichm.")
for (s, dist, x, y), k in zip(pk["kaesten"], nr):
    o = float(official(s)); u = s * 21097.5 / L
    print(f"{k:3d}  {s:9.0f}  {o / 1000:10.3f}  {u / 1000:12.3f}   {o - k * 1000:+7.0f}  {u - k * 1000:+9.0f}")
