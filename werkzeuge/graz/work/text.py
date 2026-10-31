# Text einer gespeicherten Seite ohne Navigation ausgeben (Hilfe beim Lesen der Seiten in ../dl/seiten/). Aufruf: python3 text.py <datei> [Anfangswort]
import re, html, sys
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
t = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>", "", s, flags=re.S)
t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
if len(sys.argv) > 2 and sys.argv[2] in t: t = t[t.index(sys.argv[2]):]
print(t)
