#!/usr/bin/env python3
"""Höhen aus den freien Höhenmodellen von swisstopo, für beliebige Punkte in der Schweiz (und Liechtenstein).

Wiederverwendbar für alle Schweizer Strecken (Zürich, später Jungfrau, Zermatt, Luzern): nur diese eine Datei kopieren oder importieren
(``sys.path.insert(0, ".../werkzeuge/zuerich/work"); from swissalti import Modell``).

Modelle (Sammlungen der STAC-API von data.geo.admin.ch, frei seit 01.03.2021, „Open Government Data“, Quellenangabe Pflicht:
„© swisstopo“ bzw. „Quelle: Bundesamt für Landestopografie swisstopo“, https://www.swisstopo.admin.ch/de/nutzungsbedingungen-kostenlose-geodaten-und-geodienste):

  ``swissalti3d``            swissALTI3D, Geländemodell ohne Bewuchs und Bebauung (Brücken entfernt: über Wasser misst es die Wasserfläche),
                             0,5 m oder 2 m, aus Laserscans (Mittelland seit 2019 neu beflogen), Nachführung im 6-Jahres-Zyklus.
  ``swisssurface3d-raster``  swissSURFACE3D Raster, Oberflächenmodell (mit Gebäuden, Bäumen, Brücken), 0,5 m, aus derselben Befliegung.
                             Für Brückendecks: dort, wo das Geländemodell die Brücke weglässt (Muster: werkzeuge/koeln/dom.py mit DOM1 NRW).

Kacheln: 1 × 1 km in LV95 (EPSG:2056), Name z. B. ``swissalti3d_2026_2683-1246`` = Jahrgang 2026, Ostwert 2683 km, Nordwert 1246 km
(linke untere Ecke). Höhen in m über Meer im Landeshöhennetz LN02 (EPSG:5728, „_5728“ im Dateinamen; LHN95 weicht im Mittelland um
wenige Zentimeter ab). Für eine Kachel gibt es oft mehrere Jahrgänge (z. B. 2020 und 2026); genommen wird der neueste, mit ``jahr=``
ein bestimmter (Jahrgang <= jahr). Die GeoTIFF sind Cloud-Optimized (COG, interne Kacheln, Deflate/LZW): geladen werden nur der
Dateikopf und die gebrauchten internen Kacheln per HTTP-Range (bei 0,5 m statt rund 15 MB je km² nur ein paar 100 KB entlang einer
Linie). Alles landet im Zwischenspeicher (Standard ``../dl/swisstopo/`` neben dieser Datei); ein zweiter Lauf braucht kein Netz.

Beispiel:
    from swissalti import Modell
    gel = Modell("swissalti3d", gsd=0.5)
    ober = Modell("swisssurface3d-raster")
    h = gel.wgs84([47.3668, 47.3650], [8.5431, 8.5450])      # Arrays, bilinear; nan außerhalb oder ohne Daten
    print(gel.kacheln_info())                                # verwendete Kacheln mit Jahrgang und Datei

Aufruf zum Ausprobieren:  python3 swissalti.py 47.36685 8.54314 [lat lon …]   (Höhen aus beiden Modellen und die Kacheln)
"""
import hashlib, io, json, os, sys, time, urllib.request
import numpy as np
import tifffile
from pyproj import Transformer

STAC = "https://data.geo.admin.ch/api/stac/v0.9/collections/{}/items"
UA = {"User-Agent": "MarathonProfil/1.0 (private, non-commercial; swissalti.py)"}
ZWISCHEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dl", "swisstopo")
_ZU_LV95 = Transformer.from_crs(4326, 2056, always_xy=True)


def _hole(url, a=None, b=None, ordner=ZWISCHEN, versuche=6):
    """Datei oder Bytebereich a..b laden, mit Zwischenspeicher und Wiederholung (429/5xx: warten)."""
    os.makedirs(os.path.join(ordner, "teile"), exist_ok=True)
    f = os.path.join(ordner, "teile", hashlib.md5(f"{url} {a} {b}".encode()).hexdigest())
    if os.path.exists(f) and (a is None or os.path.getsize(f) == b - a + 1):
        return open(f, "rb").read()
    kopf = dict(UA)
    if a is not None:
        kopf["Range"] = f"bytes={a}-{b}"
    for n in range(versuche):
        try:
            d = urllib.request.urlopen(urllib.request.Request(url, headers=kopf), timeout=120).read()
            if a is None or len(d) == b - a + 1:
                open(f, "wb").write(d)
                return d
        except Exception as e:                       # noqa: BLE001 – Netzfehler, 429, 5xx: später noch einmal
            print(f"  swissalti: {e} ({url.rsplit('/', 1)[-1]}), Versuch {n + 1}", file=sys.stderr, flush=True)
        time.sleep(2 + 4 * n)
    raise IOError(f"{url} {a}-{b} nicht geladen")


def _groesse(url, ordner=ZWISCHEN):
    os.makedirs(os.path.join(ordner, "teile"), exist_ok=True)
    f = os.path.join(ordner, "teile", hashlib.md5(("HEAD " + url).encode()).hexdigest())
    if os.path.exists(f):
        return int(open(f).read())
    n = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD", headers=UA), timeout=60).headers["Content-Length"])
    open(f, "w").write(str(n))
    return n


class _Fern(io.RawIOBase):
    """Dateiähnlicher Zugriff auf eine entfernte Datei in Blöcken zu 64 KB (für den TIFF-Kopf)."""
    B = 1 << 16

    def __init__(self, url, groesse, ordner):
        self.url, self.size, self.pos, self.cache, self.ordner = url, groesse, 0, {}, ordner

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos

    def seek(self, o, w=0):
        self.pos = o if w == 0 else (self.pos + o if w == 1 else self.size + o)
        return self.pos

    def _blk(self, i):
        if i not in self.cache:
            self.cache[i] = _hole(self.url, i * self.B, min(self.size, (i + 1) * self.B) - 1, self.ordner)
        return self.cache[i]

    def read(self, n=-1):
        if n < 0:
            n = self.size - self.pos
        out = []
        while n > 0 and self.pos < self.size:
            i = self.pos // self.B
            o = self.pos - i * self.B
            c = self._blk(i)[o:o + n]
            out.append(c)
            self.pos += len(c)
            n -= len(c)
        return b"".join(out)

    def readinto(self, b):
        d = self.read(len(b))
        b[:len(d)] = d
        return len(d)


class _COG:
    """Volle Auflösung (erste Seite) eines COG; Werte an LV95-Koordinaten bilinear über die Pixelmitten."""

    def __init__(self, url, ordner):
        self.url, self.ordner = url, ordner
        self.tf = tifffile.TiffFile(_Fern(url, _groesse(url, ordner), ordner))
        p = self.p = self.tf.pages[0]
        tp = p.tags["ModelTiepointTag"].value
        sc = p.tags["ModelPixelScaleTag"].value
        gk = p.tags["GeoKeyDirectoryTag"].value
        gk = {gk[i]: gk[i + 3] for i in range(4, len(gk), 4)}
        self.x0, self.y0, self.sx, self.sy = tp[3], tp[4], sc[0], sc[1]
        if gk.get(1025, 1) != 2:                     # RasterPixelIsArea: Ecke des ersten Pixels -> Mitte
            self.x0 += self.sx / 2
            self.y0 -= self.sy / 2
        self.H, self.W = p.shape[:2]
        self.tw, self.th = p.tilewidth, p.tilelength
        self.nx = -(-self.W // self.tw)
        nd = p.tags.get("GDAL_NODATA")
        self.nodata = float(str(nd.value).strip("\x00")) if nd else None
        self.kach = {}

    def _kachel(self, i, j):
        if (i, j) not in self.kach:
            k = i * self.nx + j
            a, n = self.p.dataoffsets[k], self.p.databytecounts[k]
            if n == 0:
                z = np.full((self.th, self.tw), np.nan)
            else:
                z = self.p.decode(_hole(self.url, a, a + n - 1, self.ordner), k)[0].reshape(self.th, self.tw).astype(float)
                if self.nodata is not None:
                    z[z == self.nodata] = np.nan
                z[z < -1000] = np.nan
            self.kach[(i, j)] = z
        return self.kach[(i, j)]

    def _wert(self, r, c):
        out = np.full(r.shape, np.nan)
        ok = (r >= 0) & (r < self.H) & (c >= 0) & (c < self.W)
        for n in np.where(ok)[0]:
            i, j = r[n] // self.th, c[n] // self.tw
            out[n] = self._kachel(i, j)[r[n] - i * self.th, c[n] - j * self.tw]
        return out

    def __call__(self, x, y):
        fx = (np.asarray(x, float) - self.x0) / self.sx
        fy = (self.y0 - np.asarray(y, float)) / self.sy
        c0, r0 = np.floor(fx).astype(int), np.floor(fy).astype(int)
        ax, ay = fx - c0, fy - r0
        # Am Kachelrand (äußerste halbe Pixelreihe) fehlt der Nachbar: dort den nächsten Pixel nehmen
        c0 = np.clip(c0, 0, self.W - 2)
        r0 = np.clip(r0, 0, self.H - 2)
        ax, ay = np.clip(fx - c0, 0, 1), np.clip(fy - r0, 0, 1)
        v00, v01 = self._wert(r0, c0), self._wert(r0, c0 + 1)
        v10, v11 = self._wert(r0 + 1, c0), self._wert(r0 + 1, c0 + 1)
        return (v00 * (1 - ax) + v01 * ax) * (1 - ay) + (v10 * (1 - ax) + v11 * ax) * ay


class Modell:
    """Ein swisstopo-Höhenmodell (Sammlung der STAC-API) in einer Auflösung, gesucht und geladen nach Bedarf."""

    def __init__(self, sammlung="swissalti3d", gsd=0.5, jahr=None, ordner=ZWISCHEN):
        if not sammlung.startswith("ch.swisstopo."):
            sammlung = "ch.swisstopo." + sammlung
        self.sammlung, self.gsd, self.jahr, self.ordner = sammlung, float(gsd), jahr, ordner
        self.cogs, self.wahl = {}, {}
        os.makedirs(ordner, exist_ok=True)

    def _stac(self, e, n):
        """Alle Jahrgänge der Kachel (e, n) in km: [(jahr, url)] mit passender Auflösung, aus der STAC-API (zwischengespeichert)."""
        f = os.path.join(self.ordner, f"stac_{self.sammlung}_{self.gsd:g}_{e}-{n}.json")
        if os.path.exists(f):
            return json.load(open(f))
        lo, la = Transformer.from_crs(2056, 4326, always_xy=True).transform(e * 1000 + 500, n * 1000 + 500)
        url = STAC.format(self.sammlung) + f"?bbox={lo - 0.0005},{la - 0.0005},{lo + 0.0005},{la + 0.0005}&limit=100"
        j = json.loads(_hole(url, ordner=self.ordner))
        aus = []
        for it in j.get("features", []):
            if not it["id"].endswith(f"_{e}-{n}"):
                continue
            jahr = int(it["id"].split("_")[-2])
            for a in it["assets"].values():
                href = a["href"]
                if href.endswith(".tif") and abs(float(a.get("eo:gsd") or a.get("gsd") or href.split("_")[-3]) - self.gsd) < 1e-6:
                    aus.append((jahr, href))
        aus.sort()
        json.dump(aus, open(f, "w"))
        return aus

    def _cog(self, e, n):
        if (e, n) not in self.cogs:
            jg = [x for x in self._stac(e, n) if self.jahr is None or x[0] <= self.jahr]
            if not jg:
                self.cogs[(e, n)] = None
            else:
                self.wahl[(e, n)] = jg[-1]
                self.cogs[(e, n)] = _COG(jg[-1][1], self.ordner)
        return self.cogs[(e, n)]

    def lv95(self, x, y):
        """Höhe (m ü. M., LN02) an LV95-Koordinaten, bilinear; nan ohne Daten."""
        x, y = np.atleast_1d(np.asarray(x, float)), np.atleast_1d(np.asarray(y, float))
        h = np.full(x.shape, np.nan)
        ke, kn = np.floor(x / 1000).astype(int), np.floor(y / 1000).astype(int)
        for e, n in sorted(set(zip(ke.tolist(), kn.tolist()))):
            c = self._cog(e, n)
            if c is None:
                continue
            sel = (ke == e) & (kn == n)
            h[sel] = c(x[sel], y[sel])
        return h

    def wgs84(self, lat, lon):
        x, y = _ZU_LV95.transform(np.asarray(lon, float), np.asarray(lat, float))
        return self.lv95(x, y)

    def kacheln_info(self):
        return {f"{e}-{n}": {"jahr": j, "datei": u.rsplit("/", 1)[-1]} for (e, n), (j, u) in sorted(self.wahl.items())}


if __name__ == "__main__":
    a = [float(v) for v in sys.argv[1:]]
    if len(a) < 2 or len(a) % 2:
        print(__doc__)
        sys.exit(1)
    la, lo = np.array(a[0::2]), np.array(a[1::2])
    for name, gsd in (("swissalti3d", 0.5), ("swissalti3d", 2.0), ("swisssurface3d-raster", 0.5)):
        m = Modell(name, gsd)
        h = m.wgs84(la, lo)
        print(f"{name} {gsd} m: " + "  ".join(f"{v:.2f}" for v in h), m.kacheln_info())
