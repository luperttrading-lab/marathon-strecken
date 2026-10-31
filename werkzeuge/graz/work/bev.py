# Laser-Höhenmodelle des BEV (Bundesamt für Eich- und Vermessungswesen, Österreich) ohne ganze Kacheln: ALS DTM (Geländemodell) und
# ALS DSM (Oberflächenmodell), Höhenraster 1 m, CC BY 4.0. Wiederverwendbar (Graz, Salzburg …): als Modul importieren oder kopieren.
#
# Daten: https://data.bev.gv.at/download/ALS/<DTM|DSM>/<Stichtag>/ALS_<DTM|DSM>_CRS3035RES50000mN<N>E<E>.tif
#   55 Kacheln von 50 × 50 km für ganz Österreich (Kachelübersicht: https://data.bev.gv.at/download/ALS/ALS_Kacheluebersicht.zip),
#   N und E = linke untere Ecke in ETRS89 / LAEA Europe (EPSG 3035), Vielfache von 50 000 m. Je Kachel 50 001 × 50 001 Zellen float32,
#   Zellmitte auf ganzen Metern (Zeile 0, Spalte 0 = E, N + 50 000), gekachelt 512 × 512, LZW mit Gleitkomma-Prädiktor, kein Wert -9999,
#   je Datei 8–10 GB. Höhen über EVRF2000 (EPSG 9274 laut Metadaten), nicht über Adria (Gebrauchshöhen; in Wien liegen die
#   Adria-Höhen der Stadt rund 0,5 m höher, siehe werkzeuge/wien/UEBERGABE.md). Stichtage 15.09.2019, 2021–2025 (ATOM-Feed
#   https://data.bev.gv.at/geonetwork/srv/atom/describe/service?uuid=208cff7a-c8aa-42fe-bf4f-2b8156e37528); der Stichtag ist das
#   Erstellungsdatum, das Flugjahr je Gebiet steht in der Aktualitätsübersicht (flugjahr()). Metadaten DTM:
#   https://data.bev.gv.at/geonetwork/srv/metadata/ec12896e-1ecd-47ad-8d48-44d236e383cc
#
# Verfahren: Die Datei wird über HTTP-Range gelesen (HttpFile, Blöcke zu 64 KB); tifffile liest daraus Kopf und Kachelverzeichnis
# (≈ 150 KB) und dann nur die 512-m-Teilkacheln, die gebraucht werden (je ≈ 0,3–1 MB). Jede Teilkachel wird einmal als .npy im
# Zwischenspeicher abgelegt (Standard: ../dl/bev neben diesem Skript), danach geht alles ohne Netz.
#
# Benutzung (Koordinaten WGS 84):
#   import bev
#   dtm = bev.Modell("DTM")                 # Stichtag bev.STICHTAG
#   h = dtm.hoehe(lon, lat)                 # bilinear, Arrays oder Zahlen, NaN ohne Wert
#   dsm = bev.Modell("DSM")
#   q = dsm.quantil(lon, lat, r=2, q=25)    # Quantil der Zellen im Umkreis r (Fahrbahn auf Brücken ohne Geländer, Leuchten)
#   bev.flugjahr(lon, lat)                  # [(Gebiet, Flugjahr), …] aus der Aktualitätsübersicht des Stichtags
# Kommandozeile: python3 bev.py <lat> <lon>  (DTM, DSM und Flugjahr an einem Punkt, zum Ausprobieren)
import io, os, struct, sys, time, urllib.request, zipfile
import numpy as np
import tifffile
from pyproj import Transformer

STICHTAG = "20250915"
BASIS = "https://data.bev.gv.at/download/ALS"
UA = {"User-Agent": "marathon-profile-check/1.0 (private, non-commercial)"}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dl/bev")
_T = Transformer.from_crs(4326, 3035, always_xy=True)


def _hole(url, rng=None, versuche=6):
    h = dict(UA)
    if rng: h["Range"] = f"bytes={rng[0]}-{rng[1]}"
    for v in range(versuche):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=120).read()
        except Exception as e:
            if v == versuche - 1: raise
            print(f"  bev: {e}, neuer Versuch", file=sys.stderr); time.sleep(5 + 10 * v)


class HttpFile(io.RawIOBase):
    """Datei über HTTP-Range lesen: nur die gebrauchten 64-KB-Blöcke, im Speicher gehalten (Kopie von werkzeuge/wien/work/httpfile.py)."""
    def __init__(self, url, size, block=1 << 16):
        self.url, self.size, self.pos, self.block, self.cache = url, size, 0, block, {}
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off); return self.pos
    def _blk(self, i):
        if i not in self.cache:
            a = i * self.block; b = min(self.size, a + self.block) - 1
            self.cache[i] = _hole(self.url, (a, b))
        return self.cache[i]
    def read(self, n=-1):
        if n is None or n < 0: n = self.size - self.pos
        out = bytearray()
        while n > 0 and self.pos < self.size:
            i = self.pos // self.block; o = self.pos - i * self.block; d = self._blk(i)[o:o + n]
            out += d; self.pos += len(d); n -= len(d)
        return bytes(out)
    def readinto(self, b):
        d = self.read(len(b)); b[:len(d)] = d; return len(d)


def kachel_id(x, y):
    """50-km-Kachel des BEV zu einem Punkt in EPSG 3035."""
    return f"CRS3035RES50000mN{int(y // 50000) * 50000}E{int(x // 50000) * 50000}"


class Modell:
    def __init__(self, art="DTM", stichtag=STICHTAG, cache=CACHE):
        assert art in ("DTM", "DSM")
        self.art, self.stichtag, self.cache = art, stichtag, os.path.join(cache, f"{art}_{stichtag}")
        os.makedirs(self.cache, exist_ok=True)
        self.dateien, self.bloecke, self.geladen = {}, {}, 0

    def url(self, kid): return f"{BASIS}/{self.art}/{self.stichtag}/ALS_{self.art}_{kid}.tif"

    def _datei(self, kid):
        if kid not in self.dateien:
            u = self.url(kid)
            r = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers=UA), timeout=60)
            tf = tifffile.TiffFile(HttpFile(u, int(r.headers["Content-Length"]))); p = tf.pages[0]
            sx, sy = p.tags["ModelPixelScaleTag"].value[:2]; x0, y0 = p.tags["ModelTiepointTag"].value[3:5]
            assert (sx, sy) == (1.0, 1.0), (sx, sy)
            self.dateien[kid] = dict(tf=tf, p=p, x0=x0, y0=y0, tw=p.tilewidth, tl=p.tilelength, ntx=-(-p.shape[1] // p.tilewidth),
                                     nod=float(p.tags["GDAL_NODATA"].value), shape=p.shape)
        return self.dateien[kid]

    def _block(self, kid, i, j):
        k = (kid, i, j)
        if k not in self.bloecke:
            f = os.path.join(self.cache, f"{kid}_{i}_{j}.npy")
            if os.path.exists(f): self.bloecke[k] = np.load(f)
            else:
                D = self._datei(kid); p = D["p"]; idx = j * D["ntx"] + i; fh = D["tf"].filehandle
                fh.seek(p.dataoffsets[idx]); roh = fh.read(p.databytecounts[idx])
                a = p.decode(roh, idx)[0].reshape(D["tl"], D["tw"]).astype(np.float32)
                a[a == D["nod"]] = np.nan; np.save(f, a); self.bloecke[k] = a; self.geladen += 1
        return self.bloecke[k]

    def zelle(self, x, y):
        """Wert der 1-m-Zelle, deren Mitte (ganze Meter in EPSG 3035) bei x, y liegt."""
        kid = kachel_id(x, y); e0 = int(x // 50000) * 50000; n0 = int(y // 50000) * 50000
        c = int(round(x)) - e0; r = n0 + 50000 - int(round(y))            # Spalte, Zeile in der 50-km-Kachel
        if r < 0: return self.zelle(x, y + 0.6)                               # Rand (Zeile 0 gehört zur Kachel darunter)
        return float(self._block(kid, c // 512, r // 512)[r % 512, c % 512])

    def bilinear(self, x, y):
        x0, y0 = np.floor(x), np.floor(y); fx, fy = x - x0, y - y0
        q = [self.zelle(x0, y0), self.zelle(x0 + 1, y0), self.zelle(x0, y0 + 1), self.zelle(x0 + 1, y0 + 1)]
        if not np.all(np.isfinite(q)): return np.nan
        return q[0] * (1 - fx) * (1 - fy) + q[1] * fx * (1 - fy) + q[2] * (1 - fx) * fy + q[3] * fx * fy

    def fenster(self, x, y, r=2.0):
        """Werte aller Zellen, deren Mitte höchstens r Meter von x, y entfernt ist (ohne fehlende)."""
        v = []
        for dx in range(-int(np.ceil(r)) - 1, int(np.ceil(r)) + 2):
            for dy in range(-int(np.ceil(r)) - 1, int(np.ceil(r)) + 2):
                cx, cy = np.round(x) + dx, np.round(y) + dy
                if (cx - x) ** 2 + (cy - y) ** 2 <= r * r:
                    a = self.zelle(cx, cy)
                    if np.isfinite(a): v.append(a)
        return np.array(v)

    def hoehe(self, lon, lat):
        """Bilinear interpolierte Höhe (EVRF2000) an WGS-84-Punkten."""
        x, y = _T.transform(np.atleast_1d(lon), np.atleast_1d(lat))
        h = np.array([self.bilinear(a, b) for a, b in zip(x, y)])
        return h if np.ndim(lon) else float(h[0])

    def quantil(self, lon, lat, r=2.0, q=25):
        x, y = _T.transform(np.atleast_1d(lon), np.atleast_1d(lat))
        out = []
        for a, b in zip(x, y):
            v = self.fenster(a, b, r); out.append(float(np.percentile(v, q)) if len(v) else np.nan)
        return np.array(out) if np.ndim(lon) else out[0]


# Aktualität: Flugjahr je Gebiet (Shapefile ALS_<Jahr>_Meta_DTM_DSM_3035 im ZIP des Stichtags)
_META = {}
def _shp_polygone(b):
    """Polygone (Typ 5) eines Shapefiles: Liste von Ringen je Datensatz."""
    out, o = [], 100
    while o < len(b):
        _, laenge = struct.unpack(">ii", b[o:o + 8]); typ = struct.unpack("<i", b[o + 8:o + 12])[0]; r = o + 8
        if typ == 5:
            np_, npkt = struct.unpack("<ii", b[r + 36:r + 44]); teile = struct.unpack(f"<{np_}i", b[r + 44:r + 44 + 4 * np_])
            pk = np.frombuffer(b[r + 44 + 4 * np_:r + 44 + 4 * np_ + 16 * npkt], dtype="<f8").reshape(-1, 2)
            out.append([pk[a:e] for a, e in zip(teile, list(teile[1:]) + [npkt])])
        else: out.append([])
        o = r + 2 * laenge
    return out
def _dbf(b):
    n, hl, rl = struct.unpack("<IHH", b[4:12]); felder, i = [], 32
    while b[i] != 0x0D:
        felder.append((b[i:i + 11].split(b"\0")[0].decode(), b[i + 16])); i += 32
    zeilen = []
    for k in range(n):
        o = hl + k * rl + 1; z = {}
        for name, l in felder: z[name] = b[o:o + l].decode("utf-8", "replace").strip(); o += l
        zeilen.append(z)
    return zeilen
def flugjahr(lon, lat, stichtag=STICHTAG, cache=CACHE):
    from matplotlib.path import Path
    if stichtag not in _META:
        f = os.path.join(cache, f"Metadatenuebersicht_SHP_DTM_DSM_{stichtag}.zip")
        if not os.path.exists(f):
            os.makedirs(cache, exist_ok=True)
            open(f, "wb").write(_hole(f"{BASIS}/DTM/{stichtag}/Metadatenuebersicht_SHP_DTM_DSM_{stichtag}.zip"))
        z = zipfile.ZipFile(f); namen = z.namelist()
        shp = [n for n in namen if n.endswith(".shp")][0]; dbf = shp[:-4] + ".dbf"
        _META[stichtag] = list(zip(_shp_polygone(z.read(shp)), _dbf(z.read(dbf))))
    x, y = _T.transform(lon, lat); out = []
    for ringe, z in _META[stichtag]:
        drin = sum(Path(r).contains_point((x, y)) for r in ringe) % 2 == 1   # Löcher: gerade Anzahl
        if drin: out.append(tuple(z.values()))
    return out


if __name__ == "__main__":
    la, lo = float(sys.argv[1]), float(sys.argv[2])
    x, y = _T.transform(lo, la)
    print(f"EPSG 3035: {x:.1f} {y:.1f}, Kachel {kachel_id(x, y)}")
    for art in ("DTM", "DSM"):
        m = Modell(art); print(f"{art} {m.stichtag}: {m.hoehe(lo, la):.2f} m (bilinear), 25-%-Quantil r = 2 m: {m.quantil(lo, la):.2f} m; "
                              f"{m.geladen} Teilkacheln neu geladen; {m.url(kachel_id(x, y))}")
    print("Flugjahr:", flugjahr(lo, la))
