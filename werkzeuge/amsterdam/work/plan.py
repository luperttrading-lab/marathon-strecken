# Abbildung Plan (pt) -> RD New (m) und WGS84 aus ../dl/einpassung.json: je Stützpunkt eine lokale affine Abbildung, gaußförmig
# nach dem Abstand zum Stützpunkt überblendet (Sigma 70 pt, gut 250 m).
import json, numpy as np
from pyproj import Transformer
_e = json.load(open("../dl/einpassung.json"))
_C = np.array(_e["stuetz"]); _M = np.array(_e["lokal"]); _sig = _e["sigma"]
_TI = Transformer.from_crs(28992, 4326, always_xy=True)
def nach_rd(q):
    q = np.atleast_2d(np.asarray(q, float)); out = np.zeros((len(q), 2))
    for n, x in enumerate(q):
        w = np.exp(-(np.hypot(*(_C - x).T) / _sig) ** 2); w = w / w.sum() if w.sum() > 1e-12 else np.eye(len(_C))[np.argmin(np.hypot(*(_C - x).T))]
        out[n] = np.einsum("k,kj->j", w, np.einsum("i,kij->kj", np.r_[x, 1.0], _M))
    return out
def nach_wgs(q):
    xy = nach_rd(q); lo, la = _TI.transform(xy[:, 0], xy[:, 1]); return np.c_[la, lo]
