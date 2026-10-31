# DGM1 und DOM1 Baden-Württemberg (LGL, Open GeoData, https://opengeodata.lgl-bw.de/): Kacheln 2 × 2 km als ZIP, offen ohne
# Anmeldung unter https://opengeodata.lgl-bw.de/data/dgm/dgm1_32_<E>_<N>_2_bw.zip bzw. …/data/dom1/dom1_32_<E>_<N>_2_bw.zip (E ungerade,
# N gerade, in km; Muster aus der Produktliste des Portals, assets/config/local/odp-products.json). Je ZIP vier 1-km-Kacheln: DGM1 als
# Text (XYZ, „413000.50 5316999.50 261.58“, Rastermitten auf x,5 m, von Nordwesten zeilenweise), DOM1 als GeoTIFF (Float32, TFW).
# ETRS89/UTM 32N (EPSG:25832), Höhen NHN (DHHN2016, Quasigeoid GCG2016). Metadaten je Kachel (CSV): Aktualität (Laserbefliegung),
# Genauigkeit 0,15 m. Lizenz: Datenlizenz Deutschland – Namensnennung – 2.0, „Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0“.
# Ablage ../dl/dgm1/, ../dl/dom1/; die 1-km-Raster werden einmal als .npy abgelegt. Bilinear zwischen den Rastermitten.
# Muster: werkzeuge/hannover/work/lgln.py (DGM1/DOM1 Niedersachsen).
import glob, io, json, os, time, urllib.request, zipfile
import numpy as np, tifffile
_D = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 MarathonProfil/1.0 (private, non-commercial)"}
URL = {"dgm1": "https://opengeodata.lgl-bw.de/data/dgm/dgm1_32_{e}_{n}_2_bw.zip", "dom1": "https://opengeodata.lgl-bw.de/data/dom1/dom1_32_{e}_{n}_2_bw.zip"}
_cache = {}
META = {}
def _zip(art, e2, n2):
    f = os.path.join(_D, f"../dl/{art}/{art}_32_{e2}_{n2}_2_bw.zip")
    if not os.path.exists(f) or os.path.getsize(f) < 10000:
        for att in range(5):
            try:
                data = urllib.request.urlopen(urllib.request.Request(URL[art].format(e=e2, n=n2), headers=UA), timeout=300).read()
                open(f, "wb").write(data); break
            except Exception as ex:
                print("  Fehler", art, e2, n2, ex, flush=True); time.sleep(5 + 10 * att)
        time.sleep(1)
    return f
def _npy(art, e, n):
    """1-km-Raster (1000 × 1000, Zeile 0 = Norden) als .npy; aus dem ZIP der 2-km-Kachel"""
    f = os.path.join(_D, f"../dl/{art}/npy/{art}_{e}_{n}.npy")
    if os.path.exists(f): return f
    os.makedirs(os.path.dirname(f), exist_ok=True)
    e2 = e if e % 2 == 1 else e - 1; n2 = n if n % 2 == 0 else n - 1
    z = zipfile.ZipFile(_zip(art, e2, n2))
    namen = {os.path.basename(x): x for x in z.namelist()}
    for k, v in namen.items():
        if k.endswith(".csv"): META[k] = z.read(v).decode("utf-8", "replace").strip().split("\n")[-1]
    stamm = [k for k in namen if k.startswith(f"{art}_32_{e}_{n}_1_bw") and (k.endswith(".xyz") or k.endswith(".tif"))]
    if not stamm: return None
    k = stamm[0]
    if k.endswith(".xyz"):
        a = np.loadtxt(io.BytesIO(z.read(namen[k])), dtype=np.float64)
        Z = np.full((1000, 1000), np.nan, np.float32)
        c = np.round(a[:, 0] - e * 1000 - 0.5).astype(int); r = np.round(n * 1000 + 999.5 - a[:, 1]).astype(int)
        Z[r, c] = a[:, 2]
    else:
        Z = tifffile.imread(io.BytesIO(z.read(namen[k]))).astype(np.float32)
        tfw = [float(x) for x in z.read(namen[k[:-4] + ".tfw"]).decode().split()]
        assert abs(tfw[4] - (e * 1000 + 0.5)) < 0.01 and abs(tfw[5] - (n * 1000 + 999.5)) < 0.01 and Z.shape == (1000, 1000), (k, tfw, Z.shape)
    Z[Z < -1000] = np.nan
    np.save(f, Z)
    m = os.path.join(_D, f"../dl/{art}/meta.json"); alt = json.load(open(m)) if os.path.exists(m) else {}
    alt.update(META); json.dump(alt, open(m, "w"), indent=1)
    return f
def kachel(art, e, n):
    k = (art, e, n)
    if k not in _cache:
        f = _npy(art, e, n); _cache[k] = np.load(f) if f else None
    return _cache[k]
def _wert(art, x, y):
    e, n = int(x // 1000), int(y // 1000); Z = kachel(art, e, n)
    if Z is None: return np.nan
    c = int(round(x - e * 1000 - 0.5)); r = int(round(n * 1000 + 999.5 - y))
    return Z[r, c] if 0 <= r < 1000 and 0 <= c < 1000 else np.nan
def hoehe(art, E, N):
    E = np.atleast_1d(np.asarray(E, float)); N = np.atleast_1d(np.asarray(N, float)); out = np.full(len(E), np.nan)
    for i, (e, n) in enumerate(zip(E, N)):
        cx = np.floor(e - 0.5) + 0.5; cy = np.floor(n - 0.5) + 0.5; fx = e - cx; fy = n - cy
        v = [_wert(art, cx, cy), _wert(art, cx + 1, cy), _wert(art, cx, cy + 1), _wert(art, cx + 1, cy + 1)]
        out[i] = v[0] * (1 - fx) * (1 - fy) + v[1] * fx * (1 - fy) + v[2] * (1 - fx) * fy + v[3] * fx * fy
    return out
def fenster(art, E, N, r=2, q=25):
    """Quantil q der Rasterwerte im Quadrat (2r+1) × (2r+1) m um jeden Punkt (Brückendecks aus dem DOM)"""
    E = np.atleast_1d(np.asarray(E, float)); N = np.atleast_1d(np.asarray(N, float)); out = np.full(len(E), np.nan)
    for i, (e, n) in enumerate(zip(E, N)):
        v = [_wert(art, e + dx, n + dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1)]
        v = [x for x in v if not np.isnan(x)]
        if v: out[i] = np.percentile(v, q)
    return out
