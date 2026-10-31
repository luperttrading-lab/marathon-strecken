# Nachbau des Pace-Modells aus dem gemeinsamen Kern (hamburg/index.html, Stand Marathon 2.6) in Python, dazu frei
# wählbare Steigungskosten für die Eichung. Liest nur `const D` (Höhen D.h in cm, 10-m-Schritt) aus <app>/index.html.
import re, json, os
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def lade(app):
    s = open(f"{REPO}/{app}/index.html", encoding="utf-8").read()
    D = json.loads(re.search(r"^const D = (\{.*\});\s*$", s, re.M).group(1))
    return Strecke(D)

def minetti(i):
    return 155.4 * i**5 - 30.4 * i**4 - 43.3 * i**3 + 46.3 * i**2 + 19.5 * i + 3.6

# --- Kern: Pace-Faktor (paceFaktor, pfAuf, pfAb), S.down = 0,5, BERGAB = { r: 0.5, w: 1, xm: -8, gm: 12 }
B_R, B_W, B_XM, B_GM = 0.5, 1.0, -8.0, 12.0

def pf_auf(x, sec=1.0):                       # x in %, ≥ 0; Faktor − 1
    return sec / 0.24 / (19.5 / 3.6) * (minetti(x / 100) / 3.6 - 1)

def pf_ab(x, sec=1.0):                        # x in %, < 0; Faktor − 1 bei „halb“
    s0, tief, h = B_R * sec / 24, B_GM / 100 * sec, -B_XM
    t = (x - B_XM) / h
    v = -tief * (2 * t**3 - 3 * t**2 + 1) + s0 * h * (t**3 - t**2)
    return np.where(x >= B_XM, v, -tief)

def pace_faktor(gi, sec=1.0, ab=1.0, auf=None):
    """Pace-Faktor wie im Kern (gi Steigung als Bruch). sec: Kosten je Höhenmeter (1,0 s bei 4:00 /km);
    ab: Faktor auf die Bergab-Kurve (1 = „halb“); auf: eigene Funktion x(%) → Faktor − 1 bergauf (statt Minetti skaliert).
    Übergang auf ±1 % wie im Kern (Hermite), mit der jeweiligen Bergauf-Funktion."""
    x = np.asarray(gi, float) * 100
    fa = (lambda xx: pf_auf(xx, sec)) if auf is None else auf
    d = 2 * 0.5 * ab
    unten = lambda xx: d * pf_ab(xx, sec)
    w, e = B_W, 1e-3
    out = np.where(x >= 0, fa(np.maximum(x, 0)), unten(np.minimum(x, -1e-9)))
    # Hermite-Stücke
    s_auf0 = sec / 24 if auf is None else float((fa(np.array(e)) - fa(np.array(0.0))) / e)   # Steigung bei 0 (Kern: S.secHm/24)
    sm = (s_auf0 + d * B_R * sec / 24) / 2
    m_auf = (fa(np.array(w + e)) - fa(np.array(w - e))) / (2 * e)
    m_ab = (unten(np.array(-w + e)) - unten(np.array(-w - e))) / (2 * e)
    t = x / w
    oben = (-2 * t**3 + 3 * t**2) * fa(np.array(w)) + (t**3 - t**2) * w * m_auf + (t**3 - 2 * t**2 + t) * w * sm
    t2 = (x + w) / w
    untn = (2 * t2**3 - 3 * t2**2 + 1) * unten(np.array(-w)) + (t2**3 - 2 * t2**2 + t2) * w * m_ab + (t2**3 - t2**2) * w * sm
    out = np.where((x >= 0) & (x < w), oben, out)
    out = np.where((x < 0) & (x > -w), untn, out)
    return 1 + out

class Strecke:
    def __init__(self, D):
        self.D = D; self.L = D["len"]; self.STEP = D["step"]; self.H = np.array(D["h"], float) / 100; self.N = len(self.H)
        self.x = np.arange(self.N) * self.STEP
        self.win = {w: self._fenster(w) for w in (100, 200)}

    def h_at(self, x):
        return np.interp(np.clip(x, 0, (self.N - 1) * self.STEP), self.x, self.H)

    def _fenster(self, w):                    # buildWindow(w): g in %, up/dn kumuliert
        a = np.clip(self.x - w / 2, 0, self.L); b = np.clip(self.x + w / 2, 0, self.L)
        g = np.where(b > a, (self.h_at(b) - self.h_at(a)) / np.maximum(b - a, 1e-9) * 100, 0)
        dh = (g[:-1] + g[1:]) / 2 / 100 * self.STEP
        up = np.concatenate([[0], np.cumsum(np.maximum(0, dh))]); dn = np.concatenate([[0], np.cumsum(np.maximum(0, -dh))])
        return {"g": g, "up": up, "dn": dn}

    def ratio(self, **kw):                    # paceRatio() mit RECHEN = 100
        return pace_faktor(self.win[100]["g"] / 100, **kw)

    def kum(self, ratio, hoehe=0.0):
        """kumulierte gewichtete Meter (Trapez); hoehe: Aufschlag je m Höhe über dem Meer (App: 0,062/2240), relativ zum Start"""
        r = ratio
        if hoehe:
            r = r * (1 + hoehe * self.H) / (1 + hoehe * self.H[0])
        return np.concatenate([[0], np.cumsum((r[:-1] + r[1:]) / 2 * self.STEP)])

    def at(self, arr, x):
        return float(np.interp(x, self.x, arr))

    def abschnitt(self, a, b, w=200):
        W = self.win[w]
        return {"von": a, "bis": b, "len": b - a, "auf": self.at(W["up"], b) - self.at(W["up"], a),
                "ab": self.at(W["dn"], b) - self.at(W["dn"], a), "h0": float(self.h_at(a)), "h1": float(self.h_at(b))}

    def zeit_4min(self):                      # Modellzeit bei 4:00 /km im Flachen (s), wie die Voreinstellung der App
        return 240 * self.at(self.kum(self.ratio()), self.L) / 1000

    def hm_nach_klasse(self, a, b, kanten):
        """Höhenmeter bergauf (Rechenfenster 100 m wie das Modell) zwischen a und b, aufgeteilt nach Steigungsklassen [%]"""
        g = self.win[100]["g"]; gm = (g[:-1] + g[1:]) / 2; dh = gm / 100 * self.STEP
        xm = (self.x[:-1] + self.x[1:]) / 2; sel = (xm >= a) & (xm < b)
        out = []
        for lo, hi in zip(kanten[:-1], kanten[1:]):
            m = sel & (gm >= lo) & (gm < hi); out.append(float(dh[m].sum()) if lo >= 0 else float(-dh[m].sum()))
        return out
