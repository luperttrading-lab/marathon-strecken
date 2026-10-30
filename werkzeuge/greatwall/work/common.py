# Linienmeter <-> offizielle Meter. Die Linie (linie.py) ist 1,8 % länger als 42,195 km: Mauer und Festung nach OSM mit allen
# Knicken, Haarnadelkurven der Bergstraßen nach OSM, kleine Übergänge zwischen OSM-Weg und gezeichneter Linie, Wege über den Platz.
# Bezugspunkte (marken.py): Kilometerschilder der Karte (Gewicht 1), Tor zur Mauer km 35 (fester Knoten, Lage aus dem Ausschnitt),
# Getränkestellen mit den Kilometern der Höhenkurve (Gewicht 0,5; auf der Mauer 0,3, weil die Karte die Strecke dort 30–120 m neben
# die Mauer zeichnet), dazu die Form der Höhenkurve des Veranstalters (form.py: Zuordnung an Hängen alle 500 m, Gewicht 0,5).
# Nicht verwendet: Schild „27 KM“ und Getränke 13 (26,9). Beide stehen in der Karte dicht beieinander am Hügel vor Da Ping'an, nach
# der Linie aber 0,4–0,45 km vor der Stelle, die Linienlänge (Getränke 12 bei 25,3 und 14 bei 28,9 passen) und die Form der
# Höhenkurve (Gipfel bei km 27,4) ergeben. Stückweise linear mit Knoten alle 3 km Linie, Start = 0, Tor = 35 000 m und Ziel = 42 195 m fest,
# robust nach Huber (ab 150 m Abweichung weniger Gewicht). Restabweichung: python3 common.py.
import json, numpy as np
GL = json.load(open("linie.json"))["d"][-1]
AUSGENOMMEN = {(27.0, "Kilometerschild"), (26.9, "Getränke 13")}
_R = [r for r in json.load(open("marken.json"))["ref"] if (r["km"], r["was"]) not in AUSGENOMMEN]
_R += [{"km": a["km"], "d": a["d"], "was": "Form"} for a in json.load(open("form.json"))["anker"]]
_k = np.array([r["km"] * 1000 for r in _R]); _s = np.array([r["d"] for r in _R])
_g = np.array([1.0 if r["was"].startswith("Tor") else 1.0 if r["was"] == "Kilometerschild" else
               0.3 if r["was"] in ("Getränke 3", "Getränke 4", "Getränke 5") else 0.5 for r in _R])
# Feste Knoten: Start 0, Tor zur Mauer = 35 000 m (Runners Guide: „not reached 35 km at 13:50“, Seite des Veranstalters: „gate
# leading to the wall … (KM 35)“), Ziel 42 195 m; dazwischen frei alle 3 km Linie.
_lin = json.load(open("linie.json")); _tor = _lin["d"][[i for i, t in enumerate(_lin["teil"]) if t == "Nordmauer zu Tower 6"][0] - 1]
_frei = [x for x in np.arange(3000, GL - 1500, 3000.0) if abs(x - _tor) > 1000]
KNOTEN = np.array(sorted([0.0, _tor, GL] + _frei)); FEST = {0.0: 0.0, _tor: 35000.0, GL: 42195.0}
_fi = [j for j, x in enumerate(KNOTEN) if x in FEST]; _ui = [j for j, x in enumerate(KNOTEN) if x not in FEST]
_B = np.array([np.interp(_s, KNOTEN, np.eye(len(KNOTEN))[j]) for j in range(len(KNOTEN))]).T
_y = _k - _B[:, _fi] @ np.array([FEST[KNOTEN[j]] for j in _fi]); _Bi = _B[:, _ui]; _w = np.ones(len(_s))
for _ in range(30):
    _ww = _w * _g
    _sol = np.linalg.lstsq(_Bi * np.sqrt(_ww)[:, None], _y * np.sqrt(_ww), rcond=None)[0]
    _r = _Bi @ _sol - _y; _w = np.where(np.abs(_r) < 150, 1.0, 150 / np.maximum(np.abs(_r), 1e-9))
WERTE = np.zeros(len(KNOTEN)); WERTE[_ui] = _sol
for j in _fi: WERTE[j] = FEST[KNOTEN[j]]
assert np.all(np.diff(WERTE) > 0), "Eichung nicht monoton"
def official(s): return np.interp(np.asarray(s, float), KNOTEN, WERTE)
def gpx_of(k): return np.interp(np.asarray(k, float), WERTE, KNOTEN)
if __name__ == "__main__":
    print(f"Linie {GL:.0f} m; Knoten (Linie -> offiziell):", [(round(a), round(b)) for a, b in zip(KNOTEN, WERTE)])
    print("Maßstab je Abschnitt:", np.round(np.diff(WERTE) / np.diff(KNOTEN), 3).tolist())
    r = official(_s) - _k
    art = np.array(["Form" if rr["was"] == "Form" else "Getränke" if rr["was"].startswith("Getr") else "Schild/Tor" for rr in _R])
    for nm in ("Schild/Tor", "Getränke", "Form"):
        gr = art == nm
        print(f"{nm}: {gr.sum()} Punkte, Median |Abweichung| {np.median(np.abs(r[gr])):.0f} m, RMS {np.sqrt((r[gr] ** 2).mean()):.0f} m, max {np.abs(r[gr]).max():.0f} m")
    for rr, x in sorted(zip(_R, r), key=lambda t: t[0]["km"]): print(f"  km {rr['km']:6.2f} {rr['was']:16s} {x:+5.0f} m")
    R0 = json.load(open("marken.json"))["ref"]
    for rr in R0:
        if (rr["km"], rr["was"]) in AUSGENOMMEN: print(f"  ausgenommen: km {rr['km']} {rr['was']}: nach Eichung bei km {official(rr['d']) / 1000:.2f}")
