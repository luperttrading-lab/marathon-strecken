# Hilfsskript: Seite des Veranstalters laden (einmal, ../dl/seiten/<name>.html) und als Text ausgeben.
# Aufruf: python3 seite.py <name> <url> [Suchwort …]
import html, os, re, sys, time, urllib.request
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dl", "seiten")
os.makedirs(D, exist_ok=True)
def hole(name, url):
    f = os.path.join(D, name + ".html")
    if not os.path.exists(f):
        r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (MarathonProfil, private)"})
        open(f, "wb").write(urllib.request.urlopen(r, timeout=60).read()); time.sleep(1)
    return open(f, encoding="utf-8", errors="replace").read()
def text(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<footer.*?</footer>", " ", t, flags=re.S)
    t = re.sub(r"<(br|/p|/li|/h\d|/div|/tr)[^>]*>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return "\n".join(z for z in (re.sub(r"[ \t]+", " ", x).strip() for x in t.split("\n")) if z)
if __name__ == "__main__":
    t = hole(sys.argv[1], sys.argv[2]); x = text(t)
    if len(sys.argv) > 3 and sys.argv[3] == "--links":
        for l in sorted(set(re.findall(r'href="([^"]+)"', t))):
            if re.search(r"\.(pdf|gpx|kml|kmz|zip)|fileadmin|drive|maps|strava|komoot|outdooractive|trackmaxx|datasport|raceresult", l, re.I): print(l)
    else:
        print(x)
