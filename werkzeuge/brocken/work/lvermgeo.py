# DGM1 und DOM1 Sachsen-Anhalt (LVermGeo, Open Data, Geodatenportal Sachsen-Anhalt): Kacheln 2 × 2 km, offen ohne Anmeldung über die
# Kachelauswahl der Seiten https://www.lvermgeo.sachsen-anhalt.de/de/gdp-dgm1.html bzw. …/gdp-dom1.html. Die Seite enthält das
# Kachelverzeichnis als GeoJSON (EPSG:4647, Eigenschaft „id“, Beschriftung „32EEE5NNNN“, ../dl/lvermgeo/*_kacheln.geojson); der Knopf
# „Download“ ruft …/de/mod/2,2913,501/ajax/1/prepare/?items=<id>&format=zip (DOM1: mod/3,2926,501) und bekommt einen Link
# …/ajax/1/download/?file=mapdownloader-<hash>.zip zurück. Im ZIP: GeoTIFF (Float32, LZW, 2000 × 2000, NoData −9999, ETRS89/UTM 32N,
# EPSG:25832, Höhen NHN DHHN2016, Quasigeoid GCG2016), eine .meta-Datei (Aktualität = Laserbefliegung, Fortführung, Genauigkeit 0,15 m)
# und die Nutzungsbedingungen des LVermGeo (Version 5.0): offene Daten unter „Datenlizenz Deutschland – Namensnennung – Version 2.0“,
# Bereitsteller „© GeoBasis-DE / LVermGeo ST“.
# Ablage ../dl/dgm1/, ../dl/dom1/ (ZIP, TIF, meta.json). Bilinear zwischen den Rastermitten (Pixel 1 m, Mitte auf x,5 m).
# Muster: werkzeuge/freiburg/work/lgl.py (DGM1/DOM1 Baden-Württemberg). Eine Abfrage je Sekunde.
import glob, json, os, time, urllib.request, zipfile
import numpy as np, tifffile
_D = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 MarathonProfil/1.0 (private, non-commercial)",
      "Referer": "https://www.lvermgeo.sachsen-anhalt.de/de/gdp-dgm1.html"}
PREP = {"dgm1": "https://www.lvermgeo.sachsen-anhalt.de/de/mod/2,2913,501/ajax/1/prepare/?items={id}&format=zip",
        "dom1": "https://www.lvermgeo.sachsen-anhalt.de/de/mod/3,2926,501/ajax/1/prepare/?items={id}&format=zip"}
_verz = {}
def verzeichnis(art):
    if art not in _verz:
        gj = json.load(open(os.path.join(_D, f"../dl/lvermgeo/{art}_kacheln.geojson")))
        _verz[art] = {(round((f["geometry"]["bbox"][0] - 32000000) / 1000), round(f["geometry"]["bbox"][1] / 1000)): f["properties"]["id"]
                      for f in gj["features"]}
    return _verz[art]
def _hole(url, ziel=None, timeout=600):
    for att in range(5):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
            if ziel: open(ziel, "wb").write(data)
            return data
        except Exception as ex:
            print("  Fehler", url[-60:], ex, flush=True); time.sleep(5 + 15 * att)
    raise RuntimeError("nicht geladen: " + url)
def _tif(art, e, n):
    """2-km-Kachel mit linker unterer Ecke e, n (km, gerade) -> Pfad der TIF (lädt einmal)"""
    d = os.path.join(_D, f"../dl/{art}"); os.makedirs(d, exist_ok=True)
    alt = glob.glob(f"{d}/{art}_32_{e}_{n}_2_st*.tif")
    if alt: return alt[0]
    kid = verzeichnis(art).get((e, n))
    if kid is None: return None
    link = _hole(PREP[art].format(id=kid), timeout=600).decode().strip(); time.sleep(1)
    zf = f"{d}/{art}_32_{e}_{n}_2_st.zip"; _hole(link, zf); time.sleep(1)
    z = zipfile.ZipFile(zf); tif = None
    for nm in z.namelist():
        if nm.endswith(".tif") or nm.endswith(".meta"):
            z.extract(nm, d)
            if nm.endswith(".tif"): tif = os.path.join(d, nm)
            else:
                m = {}
                for z_ in z.read(nm).decode("utf-8", "replace").split("\n"):
                    if ":" in z_ and not z_.startswith(" "):
                        k, v = z_.split(":", 1)
                        if v.strip(): m[k.strip()] = v.strip()
                mf = f"{d}/meta.json"; mm = json.load(open(mf)) if os.path.exists(mf) else {}
                mm[nm] = m; json.dump(mm, open(mf, "w"), indent=1, ensure_ascii=False)
    os.remove(zf)
    return tif
_cache = {}
def kachel(art, e, n):
    k = (art, e, n)
    if k not in _cache:
        f = _tif(art, e, n)
        if f is None: _cache[k] = None
        else:
            with tifffile.TiffFile(f) as t:
                p = t.pages[0]; Z = p.asarray().astype(np.float32)
                tp = p.tags["ModelTiepointTag"].value; sc = p.tags["ModelPixelScaleTag"].value
                assert abs(tp[3] - e * 1000) < 0.01 and abs(tp[4] - (n + 2) * 1000) < 0.01 and sc[0] == 1 and Z.shape == (2000, 2000), (f, tp, sc, Z.shape)
            Z[Z < -1000] = np.nan; _cache[k] = Z
    return _cache[k]
def _wert(art, x, y):
    e, n = int(x // 2000) * 2, int(y // 2000) * 2; Z = kachel(art, e, n)
    if Z is None: return np.nan
    c = int(np.floor(x - e * 1000)); r = int(np.floor((n + 2) * 1000 - y))
    return Z[r, c] if 0 <= r < 2000 and 0 <= c < 2000 else np.nan
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
