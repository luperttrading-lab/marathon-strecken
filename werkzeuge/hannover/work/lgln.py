# Kacheln DGM1 und DOM1 Niedersachsen (LGLN, OpenGeoData.NI) lesen: GeoTIFF 1 × 1 km, 1-m-Raster, ETRS89/UTM 32N (EPSG:25832),
# Höhen NHN (DHHN2016). Kachelliste aus den Übersichten des LGLN (arcgis-geojson.s3.eu-de.cloud-object-storage.appdomain.cloud/
# {dgm1,dom1}/lgln-opengeodata-{dgm1,dom1}.geojson, ../dl/lgln/idx_*.geojson; daraus kacheln_*.json mit den 35 Kacheln an der Strecke).
# Die Kacheln liegen offen auf dgm1.s3… bzw. dom1.s3…, ohne Anmeldung. Ablage ../dl/dgm1/, ../dl/dom1/. Bilinear zwischen den
# Rastermitten (Lage aus ModelTiepoint/ModelPixelScale; PixelIsArea oder PixelIsPoint wird beachtet). rasterio gibt es nicht:
# tifffile und numpy. Muster: werkzeuge/stockholm/work/hoehen.py.
import json, os, time, urllib.request
import numpy as np, tifffile
_D = os.path.dirname(os.path.abspath(__file__))
_cache = {}
def _datei(art, e0, n0):
    liste = json.load(open(os.path.join(_D, f"../dl/lgln/kacheln_{art}.json")))
    v = liste.get(f"{e0}_{n0}")
    if not v: return None
    url = sorted(v, key=lambda x: x[1])[-1][0]                 # jüngste Kachel
    f = os.path.join(_D, f"../dl/{art}/", os.path.basename(url))
    if not os.path.exists(f) or os.path.getsize(f) < 1000:
        for att in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"})
                data = urllib.request.urlopen(req, timeout=120).read(); open(f, "wb").write(data); break
            except Exception as ex:
                print("  Fehler", url, ex, flush=True); time.sleep(3 + 5 * att)
    return f
def kachel(art, e0, n0):
    k = (art, e0, n0)
    if k not in _cache:
        f = _datei(art, e0, n0)
        if f is None: _cache[k] = None; return None
        with tifffile.TiffFile(f) as t:
            p = t.pages[0]
            gk = p.tags["GeoKeyDirectoryTag"].value; gk = {gk[i]: gk[i + 3] for i in range(4, len(gk), 4)}
            tp = p.tags["ModelTiepointTag"].value; sc = p.tags["ModelPixelScaleTag"].value
            Z = p.asarray().astype(float)
            nd = p.tags.get("GDAL_NODATA")
            if nd is not None:
                try: Z[Z == float(nd.value)] = np.nan
                except ValueError: pass
            Z[Z < -1000] = np.nan
        punkt = gk.get(1025) == 2
        x0 = tp[3] + (0 if punkt else sc[0] / 2); y0 = tp[4] - (0 if punkt else sc[1] / 2)   # Mitte des ersten Pixels
        _cache[k] = (Z, x0, y0, sc[0], sc[1])
    return _cache[k]
def hoehe(art, E, N):
    """bilinear; Punkte am Kachelrand nehmen die Nachbarkachel dazu (Raster über zwei Kacheln zusammengesetzt)"""
    E = np.atleast_1d(np.asarray(E, float)); N = np.atleast_1d(np.asarray(N, float)); out = np.full(len(E), np.nan)
    for i, (e, n) in enumerate(zip(E, N)):
        def wert(x, y):
            K = kachel(art, int(x // 1000), int(y // 1000))
            if K is None: return np.nan
            Z, x0, y0, sx, sy = K
            c = int(round((x - x0) / sx)); r = int(round((y0 - y) / sy))
            if 0 <= r < Z.shape[0] and 0 <= c < Z.shape[1]: return Z[r, c]
            return np.nan
        # Rastermitten um den Punkt (1-m-Raster, Mitten bei ganzen Metern + 0,5)
        cx = np.floor(e - 0.5) + 0.5; cy = np.floor(n - 0.5) + 0.5; fx = e - cx; fy = n - cy
        v = [wert(cx, cy), wert(cx + 1, cy), wert(cx, cy + 1), wert(cx + 1, cy + 1)]
        out[i] = v[0] * (1 - fx) * (1 - fy) + v[1] * fx * (1 - fy) + v[2] * (1 - fx) * fy + v[3] * fx * fy
    return out
def info(art, e0, n0):
    f = _datei(art, e0, n0)
    with tifffile.TiffFile(f) as t:
        p = t.pages[0]
        return {k.name: (k.value if not hasattr(k.value, "__len__") or len(str(k.value)) < 200 else "…") for k in p.tags.values()}
def fenster(art, E, N, r=2, q=25):
    """Quantil q der Rasterwerte im Quadrat (2r+1) × (2r+1) m um jeden Punkt (für Brückendecks aus dem DOM: darunter Wasser am Rand,
    darüber Fahrzeuge, Leuchten, Geländer; Muster: werkzeuge/koeln/work/dom.py)"""
    E = np.atleast_1d(np.asarray(E, float)); N = np.atleast_1d(np.asarray(N, float)); out = np.full(len(E), np.nan)
    for i, (e, n) in enumerate(zip(E, N)):
        v = []
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                x, y = e + dx, n + dy; K = kachel(art, int(x // 1000), int(y // 1000))
                if K is None: continue
                Z, x0, y0, sx, sy = K; c = int(round((x - x0) / sx)); rr = int(round((y0 - y) / sy))
                if 0 <= rr < Z.shape[0] and 0 <= c < Z.shape[1] and not np.isnan(Z[rr, c]): v.append(Z[rr, c])
        if v: out[i] = np.percentile(v, q)
    return out
