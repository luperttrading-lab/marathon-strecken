# (Kopie aus werkzeuge/wien/work/httpfile.py)
# Datei über HTTP-Range lesen (für tifffile): nur die Byte-Blöcke, die gebraucht werden, je 64 KB, im Speicher gehalten. Für die
# gekachelten GeoTIFFs des BEV (als.py, dsm.py), die als ganze Datei 8–9 GB groß sind.
import urllib.request, io
class HttpFile(io.RawIOBase):
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
            req = urllib.request.Request(self.url, headers={"Range": f"bytes={a}-{b}", "User-Agent": "marathon-profile-check/1.0"})
            self.cache[i] = urllib.request.urlopen(req, timeout=120).read()
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
