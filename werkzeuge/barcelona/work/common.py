# Linienmeter <-> offizielle Meter. Die Linie (linie.py) ist 2,2 % länger als 42,195 km: Straßenmitte statt Ideallinie an rund 45
# Ecken (Eixample-Kreuzungen mit abgeschrägten Ecken), Plätze und die Wende auf der Diagonal; der maßstäbliche Plan des Veranstalters
# ist gleich lang. Die 42 Kilometerkästchen des Plans (marken.py) stehen für die Lesbarkeit teils 150–300 m neben ihrer Stelle
# (Abstand Marke zu Marke 670–1290 Linienmeter). Deshalb keine Eichung Marke für Marke, sondern eine robuste Ausgleichsgerade
# stückweise: Knoten alle 5 km Linie, Start = 0 und Ziel = 42 195 m fest, Huber-Gewichte (ab 200 m Abweichung weniger Gewicht).
# Restabweichung der Kästchen: siehe python3 common.py.
import json, numpy as np
GL = json.load(open("gpx2026.json"))["d"][-1]
_m = np.array(json.load(open("marken.json"))["km"]); _k = _m[:, 0] * 1000; _s = _m[:, 1]
KNOTEN = np.r_[np.arange(0, GL - 2500, 5000.0), GL]
_B = np.array([np.interp(_s, KNOTEN, np.eye(len(KNOTEN))[j]) for j in range(len(KNOTEN))]).T
_y = _k - _B[:, -1] * 42195.0; _Bi = _B[:, 1:-1]; _w = np.ones(len(_s))
for _ in range(30):
    _sol = np.linalg.lstsq(_Bi * np.sqrt(_w)[:, None], _y * np.sqrt(_w), rcond=None)[0]
    _r = _Bi @ _sol - _y; _w = np.where(np.abs(_r) < 200, 1.0, 200 / np.maximum(np.abs(_r), 1e-9))
WERTE = np.r_[0.0, _sol, 42195.0]
assert np.all(np.diff(WERTE) > 0), "Eichung nicht monoton"
def official(s): return np.interp(np.asarray(s, float), KNOTEN, WERTE)
def gpx_of(k): return np.interp(np.asarray(k, float), WERTE, KNOTEN)
if __name__ == "__main__":
    print(f"Linie {GL:.0f} m; Knoten (Linie -> offiziell):", [(round(a), round(b)) for a, b in zip(KNOTEN, WERTE)])
    print("Maßstab je Abschnitt:", np.round(np.diff(WERTE) / np.diff(KNOTEN), 3).tolist())
    r = official(_s) - _k
    print(f"Kästchen nach der Eichung: Median |Abweichung| {np.median(np.abs(r)):.0f} m, RMS {np.sqrt((r ** 2).mean()):.0f} m, max {np.abs(r).max():.0f} m")
    print("je km:", [(int(k / 1000), int(round(x))) for k, x in zip(_k, r)])
