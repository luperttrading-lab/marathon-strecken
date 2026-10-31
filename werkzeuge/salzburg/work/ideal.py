# (Kopie aus werkzeuge/freiburg/work/ideal.py)
# Ideallinie: kürzester Weg in einem Band von ±w Metern um eine Linie (gespannte Schnur), wie bei der Vermessung einer Laufstrecke
# (die vermessene Linie schneidet jede Kurve; die gezeichnete Linie der RaceDayMap folgt den Straßenmitten von OSM).
# Verfahren: Linie alle 4 m, wiederholt glätten (Mittel der Nachbarn) und jeden Punkt in das Band um die Ausgangslinie zurücksetzen
# (Abstand zu den 0,5-m-Punkten der Ausgangslinie in einem Fenster um die eigene Stelle). Start und Ende bleiben fest.
import numpy as np
from scipy.spatial import cKDTree
def dicht(X, schritt):
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
    s = np.append(np.arange(0, d[-1], schritt), d[-1])
    return np.c_[np.interp(s, d, X[:, 0]), np.interp(s, d, X[:, 1])], s
def laenge(X): return float(np.hypot(*np.diff(X, axis=0).T).sum())
def ideal(X, w, schritt=4.0, iter=6000, fenster=80.0):
    """X: Linie in Metern (UTM). Gibt (Ideallinie, Linienmeter der Ausgangslinie je Punkt) zurück."""
    F, sf = dicht(X, 0.5)
    P, s0 = dicht(X, schritt)
    baum = cKDTree(F)
    k = 24
    for it in range(iter):
        Q = P.copy(); Q[1:-1] = 0.5 * (P[:-2] + P[2:]); Q[1:-1] = 0.5 * (P[1:-1] + Q[1:-1])
        dd, j = baum.query(Q, k=k)
        # nur Punkte der Ausgangslinie in der Nähe der eigenen Stelle (verhindert Sprünge auf andere Teile der Strecke)
        ok = np.abs(sf[j] - s0[:, None]) < fenster
        dd = np.where(ok, dd, np.inf); m = np.argmin(dd, axis=1); dmin = dd[np.arange(len(P)), m]; jj = j[np.arange(len(P)), m]
        fern = np.isinf(dmin)
        if fern.any():   # kein Nachbar im Fenster: auf den Punkt der Ausgangslinie an der eigenen Stelle
            jj[fern] = np.searchsorted(sf, s0[fern]).clip(0, len(F) - 1); dmin[fern] = np.hypot(*(Q[fern] - F[jj[fern]]).T)
        zu = dmin > w
        if zu.any():
            v = Q[zu] - F[jj[zu]]; Q[zu] = F[jj[zu]] + v * (w / dmin[zu])[:, None]
        Q[0] = P[0]; Q[-1] = P[-1]; P = Q
    return P, s0
